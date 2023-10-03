from flask import jsonify, request
from backend.app import app, db, restapi
from flask_restx import Namespace, Resource, fields
from backend.app.services.keycloak_service import KeycloakAdminService, auth_token_required, KeycloakRoles
from backend.app.services.socketio_service import emitUserRefresh, emitUserDeleted

api = Namespace('kc', description='KeyCloak Ressources')
restapi.add_namespace (api, '/kc')
kc_admin = KeycloakAdminService()

"""
Here we define the routes for the KeyCloak Admin API for managing Users

User Handling Routes:
    Get Users
    
    Create User
    Delete User
    Update User
    
    Set Roles for User (add, update)
        - bibbox-admin
        - bibbox-standard
"""

user_dictionary = api.model('User', {
    'username': fields.String(required=True),
    'email': fields.String,
    'password': fields.String(required=True),
    'firstName': fields.String,
    'lastName': fields.String,
    'roles' : fields.List(fields.String, required = True)
    # add roles?
})

user_role_mapping = api.model('User_Role_Mapping', {
    'user_role_mappings': fields.List(fields.Nested(api.model('User_Roles', {
        'user_id': fields.String(required=True),
        'roles': fields.List(fields.String(required=True))
    })), required=True)
})



@api.route('/users')
class Users(Resource):
    @api.doc("Get all Users")
    @auth_token_required(roles=[KeycloakRoles.admin])
    def get(self):
        try:
            users = kc_admin.get_users()
        except Exception as e:
            return {
                "error": "Could not get users from KeyCloak",
                "exception": str(e)
            }, 500
        
        return users, 200
    
    @api.doc("Create a new User")
    @api.expect(user_dictionary, validate=True)
    @auth_token_required(roles=[KeycloakRoles.admin])
    def post(self):
        kc_admin = KeycloakAdminService()
        try:
            message, status = kc_admin.create_user(request.json)
            emitUserRefresh()
        except Exception as e:
            return {
                "error": f"Could not create user in KeyCloak",
                "exception" : str(e),
                "request": request.json
            }, 500
        
        return message, status
    


# delete user
@api.route('/users/<string:user_id>')
class User(Resource):
    @api.doc("Delete a User")
    @auth_token_required(roles=[KeycloakRoles.admin])
    def delete(self, user_id):
        try:
            msg, status = kc_admin.delete_user(user_id)
            emitUserDeleted(user_id)
        except ValueError as e:
            return {"error": str(e)}, 400
        
        except Exception as e:
            return {"error": "Could not delete user from KeyCloak"}, 500
        
        return msg, status

    @api.doc("Get a User")
    @auth_token_required(roles=[KeycloakRoles.admin])
    def get(self, user_id):
        try:
            user, status = kc_admin.get_user_by_id(user_id)
        except Exception as e:
            return {
                "error": f"Could not get user from KeyCloak",
                "exception" : str(e)
            }, 500
        
        return user, status


    @api.doc("Update a User")
    @api.expect(user_dictionary, validate=True)
    @auth_token_required(roles=[KeycloakRoles.admin])
    def patch(self, user_id):
        try:
            user_dict = request.json
            user, status = kc_admin.update_user(user_id, user_dict)
            emitUserRefresh()
        except Exception as e:
            return {
                "error": f"Could not update user in KeyCloak",
                "exception" : str(e)
            }, 500
        
        return user, status




@api.route('/users/<string:user_id>/roles')
class UserRoles(Resource):
    @api.doc("Get all Roles of a User")
    @auth_token_required(roles=[KeycloakRoles.admin])
    def get(self, user_id):

        try:
            roles, status = kc_admin.get_realm_roles_of_user(user_id)
        except Exception as e:
            return {"error": "Could not get roles of user from KeyCloak",
                    'errormessage': str(e)}, 500
        
        return roles, status
    
    # @api.doc("Set Roles for a User")
    # # @api.expect({'roles': fields.List(fields.String, required=True, description='A list of role names to assign corresponding roles to the user')}, validate=True)
    # def post(self, user_id):
    #     try:
            
    #         list_of_roles = request.json['roles']
            
    #         # debug
    #         # list_of_roles = ['bibbox-admin']
            
    #         updated_roles = kc_admin.assign_realm_roles(user_id, list_of_roles)

    #     except ValueError as e:
    #         return {"error": str(e)}, 400
        
    #     except Exception as e:
    #         return {"error": "Could not add roles to user in KeyCloak",
    #                 "exception": str(e)}, 500
        
    #     return updated_roles, 200
    
    # @api.doc("Remove Roles from a User")
    # @api.expect({'roles': fields.List(fields.String, required=True, description='A list of role names to remove corresponding roles from the user')}, validate=True)
    # def delete(self, user_id):
    #     try:
    #         list_of_roles = request.json['roles']
    #         roles, status = kc_admin.remove_realm_roles(user_id, list_of_roles)

    #     except ValueError as e:
    #         return {"error": str(e)}, 400
        
    #     except Exception as e:
    #         return {"error": "Could not remove roles from user in KeyCloak"}, 500
        
    #     return roles, status
    
    # @api.doc("Set Roles for multiple Users")
    # @api.expect({'roles': fields.List(fields.String, required=True, description='A list of role names to assign corresponding roles to the user')}, validate=True)
    # def post(self, user_id):
    #     try:
    #         list_of_roles = request.json['roles']
    #         roles, status = kc_admin.assign_realm_roles(user_id, list_of_roles)

    #     except ValueError as e:
    #         return {"error": str(e)}, 400
        
    #     except Exception as e:
    #         return {"error": "Could not add roles to user in KeyCloak"}, 500
        
    #     return roles, status

@api.route('/users/names')
class UserNames(Resource):
    @api.doc("Get all Usernames")
    @auth_token_required(roles=[KeycloakRoles.admin])
    def get(self):
        try:
            names = kc_admin.get_usernames()
        except Exception as e:
            return {"error": "Could not get usernames from KeyCloak"}, 500
        
        return names, 200

@api.route('/users/names/<string:username>')
class UserNamesValidator(Resource):
    @api.doc("Check if username is already taken")
    @auth_token_required(roles=[KeycloakRoles.admin])
    def get(self, username):
        try:
            names = kc_admin.validate_username_availability(username=username)
        except Exception as e:
            return {"error": "Could not get usernames from KeyCloak"}, 500
        
        return names, 200





@api.route('/roles')
class Roles(Resource):
    @api.doc("Get all Roles")
    @auth_token_required(roles=[KeycloakRoles.admin])
    def get(self):
        try:
            roles = kc_admin.get_realm_roles()
        except Exception as e:
            print(e)
            return {"error": "Could not get roles from KeyCloak"}, 500
        
        return roles, 200

@api.route('/roles/update_role_mapping')
class RoleMappings(Resource):
    # update the roles of all users
    @api.doc("Update the roles of multiple users")
    @api.expect(user_role_mapping, validate=True)
    @auth_token_required(roles=[KeycloakRoles.admin])
    def post(self):
        try:
            msg, status = kc_admin.update_multiple_user_role_mappings(request.json['user_role_mappings'])
            emitUserRefresh()
        except Exception as e:
            return {
                "error": f"Could not update user roles in KeyCloak",
                "exception" : str(e),
            }, 500
        
        return msg, status