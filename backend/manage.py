"""

"""

import unittest
import os
from coverage import coverage
# from flask_script import Manager, Server as _Server

from backend.app import db, app, create_app # , socketio
from backend.app.models.app  import BibboxApp
from backend.app.models.activity import Activity
from backend.app.models.catalogue import Catalogue
from backend.app.models.log import Log
# from backend.app.models.user import User

from flask.cli import FlaskGroup
from flask_script import Manager, Server as _Server

from passlib.apps import custom_app_context as pwd_context


COV = coverage(
    branch=True,
    include='app/*',
    omit=[
        'tests/*',
        'wsgi.py',
        'settings.py',
        '__init__.py',
        'app/*/__init__.py'
        'app/static/*'
        'app/templates/*'
        'app/import_policy/*'
        'app/models/*'
    ]
)

COV.start()

# create flask application instance

app = create_app ('production')
# cli = FlaskGroup(app) # new manager, as manager is deprecated in flask 2.x


manager = Manager(app)

print ("=========== MANAGE.PY ENVIRONMENT ============")
print ("FLASK_CONFIG = ", os.environ["FLASK_CONFIG"])
print ("SQLSTRING= ", app.config["DB_SERVICE"])


# # @manager.command
# def test():
#     """Runs the unit tests without test coverage."""
#     test_suite = unittest.TestLoader().discover('tests', pattern='test*.py')
#     result = unittest.TextTestRunner(verbosity=2).run(test_suite)
#     if result.wasSuccessful():
#         return 0
#     return 1

# # @manager.command
# def cov():
#     """Runs the unit tests with coverage."""
#     tests = unittest.TestLoader().discover('tests', pattern='test*.py')
#     result = unittest.TextTestRunner(verbosity=2).run(tests)
#     if result.wasSuccessful():
#         COV.stop()
#         COV.save()
#         print('Coverage Summary:')
#         COV.report()
#         COV.html_report(directory='tests/coverage')
#         COV.erase()
#         return 0
#     return 1


@manager.command
def recreate_db():
    db.drop_all()
    db.create_all()
    db.session.commit()

# @manager.command
# def seed_db():
#     """Seed the user table in test_db database."""
#     db.session.add(User(
#         username='admin',
#         email='v@bibbox.com',
#         password_hash =  pwd_context.encrypt('vendetta')
#     ))
    
#     db.session.commit()


@manager.command
def sync_app_catalogue():
    from backend.app.celerytasks.tasks import syncAppCatalogue
    syncAppCatalogue.delay(['bibbox'])


# @manager.command
# @app.cli.command('create-default-keycloak-user')
# def create_default_keycloak_user():
#     """Create a default user for keycloak."""
#     from backend.app.services.keycloak_service import KeycloakAdminService, KeycloakRoles
#     keycloak_admin = KeycloakAdminService()
#     keycloak_admin.create_user(
#         username='admin',
#         password='admin',
#         roles=[KeycloakRoles.admin]
#     )


# --------------------------------TEST SocketIO Implementation ------------------------------------

# class Server(_Server):
#     help = description = 'Runs the Socket.IO web server'

#     def __call__(self, app, host, port, use_debugger, use_reloader):
#         # override the default runserver command to start a Socket.IO server
#         if use_debugger is None:
#             use_debugger = app.debug
#             if use_debugger is None:
#                 use_debugger = True
#         if use_reloader is None:
#             use_reloader = app.debug
#         socketio.run(app,
#                      host=host,
#                      port=port,
#                      debug=use_debugger,
#                      use_reloader=use_reloader,
#                      **self.server_options)

# manager.add_command("runserver", Server())

#  -----------------------------------------------------------------------------------------------


if __name__ == '__main__':
    manager.run()
    