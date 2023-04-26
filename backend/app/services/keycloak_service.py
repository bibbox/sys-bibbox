from keycloak import KeycloakOpenID #, KeycloakOpenIDConnection, KeycloakAdmin
from functools import wraps
from flask import request, jsonify
from backend.app import app
import dotenv
import os

# keycloak_openid = KeycloakOpenID(
#     server_url=app.config.KEYCLOAK_CONFIG['server_url'],
#     client_id=app.config.KEYCLOAK_CONFIG['client_id'],
#     realm_name=app.config.KEYCLOAK_CONFIG['realm_name'],
#     client_secret_key=app.config.KEYCLOAK_CONFIG['client_secret_key']
# )
dotenv.load_dotenv()

keycloak_openid = KeycloakOpenID(
    server_url=os.getenv('KEYCLOAK_SERVER_URL'),
    client_id=os.getenv('KEYCLOAK_CLIENT_ID'),
    realm_name=os.getenv('KEYCLOAK_REALM'),
    client_secret_key=os.getenv('KEYCLOAK_CLIENT_SECRET'),
)


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
                        
                        # if bibbox-admin in roles, then add all realm-management roles to user_realm_roles
                        if 'bibbox-admin' in required_roles:
                            user_roles.extend(token_info['resource_access']['realm-management']['roles'])


                        for role in required_roles:
                            if role not in user_roles:
                                return {'error': 'Missing Permissions.', 'token_info': token_info if 'token_info' in locals() else None, 
                    'token': token,}, 403



            except Exception as ex:
                # TODO: modify this response, currently verbose to debug
                return {
                    'error': str(ex), 
                    'token': token,
                    'token_info': token_info if 'token_info' in locals() else None,
                    'kc_env' : {k: v for k, v in os.environ.items() if k.startswith('KEYCLOAK')},
                    }, 401

            return f(*args, **kwargs)

        return decorated

    # Check if decorator arguments were passed and return either the wrapper function or the decorated function
    if len(decorator_args) == 1 and callable(decorator_args[0]):
        return wrapper(decorator_args[0])
    else:
        return wrapper


""" Example Token Payload:
{
  "exp": 1682505782,
  "iat": 1682503982,
  "auth_time": 1682503982,
  "jti": "25cc6997-a200-4d91-a0af-b5c81baf82f2",
  "iss": "http://localhost:5014/auth/realms/sys-bibbox",
  "aud": [
    "realm-management",
    "account"
  ],
  "sub": "2a9cb28b-a839-4e44-b1ff-94957c5671b0",
  "typ": "Bearer",
  "azp": "sys-bibbox-frontend",
  "nonce": "a5d43ea2-2a6f-4482-80b0-229b285fcdae",
  "session_state": "4e8d8ff0-63b5-41a3-a6e4-4c8a94dc8d85",
  "acr": "1",
  "allowed-origins": [
    "http://localhost:4200"
  ],
  "realm_access": {
    "roles": [
      "bibbox-standard",
      "offline_access",
      "default-roles-sys-bibbox",
      "uma_authorization",
      "bibbox-admin"
    ]
  },
  "resource_access": {
    "realm-management": {
      "roles": [
        "manage-realm",
        "manage-users"
      ]
    },
    "account": {
      "roles": [
        "manage-account",
        "manage-account-links",
        "view-profile"
      ]
    }
  },
  "scope": "openid profile email",
  "sid": "4e8d8ff0-63b5-41a3-a6e4-4c8a94dc8d85",
  "email_verified": true,
  "preferred_username": "admin",
  "given_name": "",
  "family_name": "",
  "email": "admin@admin.com"
}
"""






# class KeycloakService:
#     def __init__(self):
#         pass

#     def init_keycloak(config: dict) -> KeycloakOpenID:
#         keycloak_openid = KeycloakOpenID(server_url=config.KEYCLOAK_CONFIG['server_url'],
#                                         client_id=config.KEYCLOAK_CONFIG['client_id'],
#                                         realm_name=config.KEYCLOAK_CONFIG['realm_name'],
#                                         client_secret_key=config.KEYCLOAK_CONFIG['client_secret_key'])
#         return keycloak_openid


#     def get_keycloak_token(keycloak_openid: KeycloakOpenID, username: str, password: str) -> dict:
#         return keycloak_openid.token(username, password)


#     def get_userinfo(keycloak_openid: KeycloakOpenID, token: dict) -> dict:
#         return keycloak_openid.userinfo(token['access_token'])


#     def get_user_roles(keycloak_openid: KeycloakOpenID, token: dict) -> list:
#         return keycloak_openid.userinfo(token['access_token'])['resource_access']['account']['roles']

#     def logout(keycloak_openid: KeycloakOpenID, token: dict) -> bool:
#         return keycloak_openid.logout(token['refresh_token'])


# class KeycloakAdminService(KeycloakService):
#     def __init__(self, config: dict, admin_username: str, admin_password: str):
#         self.keycloak_connection = KeycloakOpenIDConnection(
#             server_url=config.KEYCLOAK_CONFIG['server_url'],
#             client_id=config.KEYCLOAK_CONFIG['client_id'],
#             realm_name=config.KEYCLOAK_CONFIG['realm_name'],
#             client_secret_key=config.KEYCLOAK_CONFIG['client_secret_key'],
#             verify=True,
#             username=admin_username,
#             password=admin_password
#         )
#         self.keycloak_admin = KeycloakAdmin(connection=self.keycloak_connection)

#     def create_new_user(self, user_dict: dict):
#         self.keycloak_admin.create_user(**user_dict)

#     def get_users(self):
#         return self.keycloak_admin.get_users()
    
#     def delete_user(self, user_id: str):
#         self.keycloak_admin.delete_user(user_id)

#     def get_realm_roles(self):
#         return self.keycloak_admin.get_realm_roles()
    
#     def assign_realm_roles(self, user_id: str, realm_roles: list):
#         self.keycloak_admin.assign_realm_roles(user_id, roles=realm_roles)



# admin functs