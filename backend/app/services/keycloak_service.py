from keycloak import KeycloakOpenID, KeycloakAdmin, KeycloakGetError#, KeycloakOpenIDConnection
from functools import wraps
from flask import request
# from backend.app import app

import dotenv
import os


dotenv.load_dotenv()

keycloak_openid = KeycloakOpenID(
    server_url=os.getenv('KEYCLOAK_SERVER_URL'),
    realm_name=os.getenv('KEYCLOAK_REALM'),
    client_id=os.getenv('KEYCLOAK_CLIENT_ID'),
    client_secret_key=os.getenv('KEYCLOAK_CLIENT_SECRET'),
)


class KeycloakRoles:
    admin = 'bibbox-admin'
    standard = 'bibbox-standard'
    demo = 'bibbox-demo'


# auth decorator
def auth_token_required(*decorator_args, **decorator_kwargs):
    """
    Decorator to check if a valid token is present in the request header.
    kwargs:
        required_roles: list of roles that are required to access the route (currently only 'bibbox-admin' is needed for admin routes)
    """
    def wrapper(f):
        @wraps(f)
        def decorated(*args, **kwargs):
            # Get roles from decorator kwargs or default to an empty list
            required_roles = decorator_kwargs.get('required_roles', [])
            
            # additional checks: TODO: implement
            # additional_checks = decorator_kwargs.get('additional_checks', [])
            # for check in additional_checks:
            #     if check == 'can_delete':
            #         uid = None
            #         iid = None
                    
            #         flag = does_user_have_permissions(uid, iid)


            token = None
            if 'Authorization' in request.headers:
                token = request.headers['Authorization'].split()[1]
            if not token:
                return {'error': 'Token is missing!'}, 401
            
            try:
                KEYCLOAK_PUBLIC_KEY = "-----BEGIN PUBLIC KEY-----\n" + keycloak_openid.public_key() + "\n-----END PUBLIC KEY-----"
                options = {"verify_signature": True, "verify_aud": False, "verify_exp": True}

                # decode token sent with request with the public key from keycloak
                token_info = keycloak_openid.decode_token(token, key=KEYCLOAK_PUBLIC_KEY, algorithms=['RS256'], options=options)

                if required_roles:
                    # Check if user has the required realm roles
                    if not token_info['realm_access']['roles']:
                        return {'error': 'Token invalid!'}, 403
                    
                    else:
                        user_roles: list = token_info['realm_access']['roles']
                        
                        # # if bibbox-admin in roles, then add all realm-management roles to user_realm_roles
                        # if 'bibbox-admin' in required_roles:
                        #     user_roles.extend(token_info['resource_access']['realm-management']['roles'])


                        for role in required_roles:
                            if role not in user_roles:
                                return {'error': 'Missing Permissions.', 'token_info': token_info if 'token_info' in locals() else None, 
                    'token': token,}, 403

            except Exception as ex:
                # TODO: modify this response, currently verbose to debug
                return {
                    'error': str(ex), 
                    'token': token,
                    'token_info': token_info if 'token_info' in locals() else None
                    #'kc_env' : {k: v for k, v in os.environ.items() if k.startswith('KEYCLOAK')},
                    }, 401

            return f(*args, **kwargs)
        return decorated

    # Check if decorator arguments were passed and return either the wrapper function or the decorated function
    if len(decorator_args) == 1 and callable(decorator_args[0]):
        return wrapper(decorator_args[0])
    else:
        return wrapper

def get_user_id_by_token(token):
    try:
        KEYCLOAK_PUBLIC_KEY = "-----BEGIN PUBLIC KEY-----\n" + keycloak_openid.public_key() + "\n-----END PUBLIC KEY-----"
        options = {"verify_signature": True, "verify_aud": False, "verify_exp": True}

        # decode token sent with request with the public key from keycloak
        user_info= keycloak_openid.decode_token(token, key=KEYCLOAK_PUBLIC_KEY, algorithms=['RS256'], options=options).get('sub',None)

    except Exception as ex:
        # TODO: modify this response, currently verbose to debug
        return {
            'error': str(ex),
            'token': token,
            'user_info': user_info if 'user_info' in locals() else None
            #'kc_env' : {k: v for k, v in os.environ.items() if k.startswith('KEYCLOAK')},
        }

    return user_info

# user management --------------------------------------------------------------------------------------------------------------------
class KeycloakAdminService():
    def __init__(self):
        # self.keycloak_api = keycloak_admin

        self.keycloak_api = KeycloakAdmin(
                                            server_url=os.getenv('KEYCLOAK_SERVER_URL'),
                                            realm_name=os.getenv('KEYCLOAK_REALM'),
                                            username=os.getenv('KEYCLOAK_USER'),
                                            password=os.getenv('KEYCLOAK_PASSWORD'),
                                            client_id=os.getenv('KEYCLOAK_ADMIN_CLIENT_ID'),
                                            client_secret_key=os.getenv('KEYCLOAK_ADMIN_CLIENT_SECRET'),
                                            auto_refresh_token=['get', 'put', 'post', 'delete']
                                        )
        
        
    def create_user(self, user_dict: dict):
        """
        Creates a new user in the keycloak realm.
        The user_dict must contain the following keys:
            - username
            - password
            - roles (contains the only default role for new users: bibbox-standard)
        The user_dict may contain the following keys:
            - email
            - firstName
            - lastName

        :param user_dict: dictionary containing the user information
        :type user_dict: dict
        :return: message and status code from keycloak server
        """


        try:
            user_representation = {
                'username': user_dict.get('username', None),
                'enabled': True,
                'credentials': [{
                    'type': 'password',
                    'value': user_dict.get('password', None),
                    'temporary': False,
                }],
            }

            if user_representation['username']:
                user_representation['username'] = user_representation['username'].lower()

            if None in user_representation.values():
                raise ValueError('Missing required key-value pair(s) in user dictionary')
            
            # check if user with username is available
            self.validate_username_availability(user_representation['username'])

            optional_fields = ['email', 'firstName', 'lastName']
            for key in optional_fields:
                if key in user_dict:
                    user_representation[key] = user_dict[key]
            self.keycloak_api.create_user(user_representation, exist_ok=False)


            user_id = self.get_user_by_username(user_representation['username'])['id']

            # assign realm roles, if none are provided, assign bibbox-standard
            self.assign_realm_roles(user_id, user_dict.get('roles', ['bibbox-standard']))

        except KeycloakGetError as ex:
            raise ex

        except Exception as ex:

            # if user was created, but realm roles could not be assigned, delete user again
            
            try:
                if user_id:
                    self.delete_user(user_id)
            except Exception as ex2:
                raise ex2

            raise ex
        
        else:
            return {'message': 'User created successfully.',
                    'userRepresentation': str(self.get_user(user_id))}, 201


    def delete_user(self, user_id: str):
        """
        Removes a user from the keycloak realm.

        :param user_id: id of the user to be deleted
        :type user_id: str
        """

        # check if user to be deleted is not the admin user
        if user_id == os.getenv('KEYCLOAK_ADMIN_USER_ID'):
            raise ValueError('Cannot delete realm-admin user.')


        if user_id not in [user['id'] for user in self.get_users()]:
            raise ValueError(f'User with id {user_id} does not exist.')
        else:
            self.keycloak_api.delete_user(user_id)
            return {'message': 'User deleted successfully.',
                    'userID': str(user_id)}, 200


    def update_user(self, user_id: str, user_dict: dict):
        """
        Updates a user in the keycloak realm.
        The user_dict may contain the following keys:
            - username
            - password
            - email
            - firstName
            - lastName

        Existing values not included in the user_dict will not be changed.


        :param user_id: id of the user to be updated
        :type user_id: str
        :param user_dict: dictionary containing the user information
        :type user_dict: dict
        """

        try:
          user_representation = {}

          optional_fields = ['username', 'email', 'firstName', 'lastName']
          for key in optional_fields:
              if key in user_dict:
                  user_representation[key] = user_dict[key]

          # cannot change username to an already existing username
          if user_representation['username'] in [user['username'] for user in self.get_users() if user['id'] != user_id ]:
              raise ValueError(f'User with username {user_representation["username"]} already exists.')
          if 'password' in user_dict:
            # Update User Password
            self.keycloak_api.set_user_password(user_id=user_id, password=user_dict['password'], temporary=True)



        # optional_credentials_dict = {
          #     'password': user_dict.get('password', None),
          #     'temporary': False,
          #     'type': 'password'
          # }

          # if None not in optional_credentials_dict.values():
          #     user_representation['credentials'] = [optional_credentials_dict]
          #

          # assign realm roles, if none are provided, assign bibbox-standard
          self.assign_realm_roles(user_id, user_dict.get('roles', ['bibbox-standard']))


          self.keycloak_api.update_user(user_id, user_representation)

        except Exception as ex:
            raise ex
        
        else:
            return {'message': 'User successfully updated.',
                    'userID': str(user_id)}, 201
        
    def get_user(self, user_id: str):
        """
        Returns a user from the keycloak realm.

        :param user_id: id of the user to be returned
        :type user_id: str
        :return: user object
        """
        #self.keycloak_api.get_user_id("username-keycloak")
        return self.keycloak_api.get_user(user_id)

    def get_user_by_id(self, user_id: str):
        """
        Returns a user from the keycloak realm.

        :param user_id: id of the user to be returned
        :type user_id: str
        :return: user object
        """
        return self.get_user(user_id),200

    def get_user_by_username(self, username: str):
        """
        Returns a user from the keycloak realm.

        :param username: username of the user to be returned
        :type username: str
        :return: user object
        """

        users = self.get_users()
        for user in users:
            if user['username'] == username:
                return user
        else:
            raise ValueError(f'User with username {username} does not exist.')


    def get_users(self) -> list:
        """
        Returns a list of all users in the keycloak realm.

        the keycloak api returns a list of users conforming to the UserRepresentation schema: https://www.keycloak.org/docs-api/18.0/rest-api/index.html#_userrepresentation
        these user objects are too complex for our purposes, so we only return the following attributes:
            - id
            - username
            - email
            - firstName
            - lastName

        We also add a 'roles' attribute, which contains a list of all bibbox-related realm roles assigned to the user.

        
        :return: list of users
        """
        kc_users = self.keycloak_api.get_users()

        users = []
        for user in kc_users:
            user_dict = {}
            required_attributes = ['id', 'username']
            for attribute in required_attributes:
                user_dict[attribute] = user[attribute]
            
            optional_attributes = ['email', 'firstName', 'lastName']
            for attribute in optional_attributes:
                if attribute in user:
                    user_dict[attribute] = user[attribute]

            user_dict['roles'] = self.get_realm_role_names_of_user(user['id'])

            users.append(user_dict)

        return users

    def get_usernames(self) -> list:
        """
        Returns a list of all usernames in the keycloak realm.

        :return: list of usernames
        """
        return [user['username'] for user in self.get_users()]


    # realm roles --------------------------------------------------------------------------------------------------------------------
    def _validate_realm_roles(self, realm_role_names: list):
        """
        Checks if all realm roles in the list of realm_role_names exist.
        
        :param realm_role_names: list of realm role names
        :type realm_role_names: list
        """
        valid_realm_role_names = self.get_realm_role_names()
        for role in realm_role_names:
            if role not in valid_realm_role_names:
                raise ValueError(f'Role {role} does not exist.')
        return True

    def validate_username_availability(self, username: str):
        """
        Checks if the username exists in the keycloak realm.

        :param username: username
        :type username: str
        """
        # check if username matches keycloak admin username from the env file
        # if username == os.getenv('KEYCLOAK_ADMIN_USERNAME'):
        #     raise ValueError('Username is reserved.')

        if username in self.get_usernames():
            raise ValueError(f'User {username} already exists.')
        return True
    
    def _validate_user_id(self, user_id: str):
        """
        Checks if the user_id exists in the keycloak realm.

        :param user_id: user_id
        :type user_id: str
        """
        if user_id not in [user['id'] for user in self.get_users()]:
            raise ValueError(f'User with id {user_id} does not exist.')
        return True



    def get_realm_roles(self):
        """
        returns all realm roles from current realm (specified in KEYCLOAK_REALM env var)
        """
        return self.keycloak_api.get_realm_roles()
    

    def get_realm_role_names(self) -> list:
        """
        returns all realm role names from current realm (specified in KEYCLOAK_REALM env var)
        """
        return [role['name'] for role in self.get_realm_roles()]

    def get_realm_roles_of_user(self, user_id: str):
        """
        returns all realm roles of a user

        :param user_id: id of user
        :type user_id: str
        """
        #self._validate_user_id(user_id)
        return self.keycloak_api.get_realm_roles_of_user(user_id)

    def get_realm_role_names_of_user(self, user_id: str) -> list:
        """
        returns all realm bibbox-specific role names of a user
        
        :param user_id: id of user
        :type user_id: str
        """
        realm_roles = [role['name'] for role in self.get_realm_roles_of_user(user_id)]
        bibbox_specific_realm_roles = [role for role in realm_roles if role.startswith('bibbox-')]

        return bibbox_specific_realm_roles

    def assign_realm_roles(self, user_id: str, realm_role_names: list):
        """
        assigns realm roles to a user, removing all other realm roles from user

        :param user_id: id of user
        :type user_id: str
        :param realm_role_names: list of realm role names
        :type realm_role_names: list
        """

        self._validate_realm_roles(realm_role_names) # check if all roles exist
        self._validate_user_id(user_id) # check if user exists

        realm_roles = [self.keycloak_api.get_realm_role(role) for role in realm_role_names]

        current_realm_roles = self.get_realm_role_names_of_user(user_id)
        self.remove_realm_roles(user_id, current_realm_roles)

        self.keycloak_api.assign_realm_roles(user_id, roles=realm_roles)

        updated_roles = self.get_realm_role_names_of_user(user_id)

        return updated_roles

    def remove_realm_roles(self, user_id: str, realm_role_names: list):
        """
        removes all bibbox-specific realm roles specified in realm_role_names from user with id user_id

        :param user_id: id of user
        :type user_id: str
        :param realm_role_names: list of realm role names to be removed
        :type realm_role_names: list
        """
        self._validate_realm_roles(realm_role_names)
        self._validate_user_id(user_id)

        realm_roles = [self.keycloak_api.get_realm_role(role) for role in realm_role_names if role.startswith('bibbox-')]

        return self.keycloak_api.delete_realm_roles_of_user(user_id, roles=realm_roles)


    def update_multiple_user_role_mappings(self, user_role_mapping: list):
        """
        Updates the realm role mappings of multiple users. The user_role_mapping list contains dicts with the user_id and a list of roles to be assigned to the user.
        For each mapping object, the current realm roles of the user are removed and the new roles are assigned.
        The new roles are checked for validity before the mapping is updated.
        
        :param user_role_mapping: list of dicts containing user_id and roles
        :type user_role_mapping: list
        """

        for element in user_role_mapping:
            self._validate_user_id(element['user_id'])
            self._validate_realm_roles(element['roles'])

        for element in user_role_mapping:
            current_realm_roles = self.get_realm_role_names_of_user(element['user_id'])
            self.remove_realm_roles(element['user_id'], current_realm_roles)
            self.assign_realm_roles(element['user_id'], element['roles'])

            # only remove bibbox roles

        return {'message': 'Roles updated successfully.',
                'users': str(self.get_users())}, 200