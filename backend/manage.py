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
from backend.app.models.keyvalue import KeyValue
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
    # Add initial keyvalue data
    db.session.add(KeyValue(keys='info', values='<h1 style=\"text-align:start\"><span style=\"color:rgb(0, 0, 0);\">Welcome to the BIBBOX - FAIR Toolbox</span></h1><p style=\"text-align:start\"><span style=\"color:rgb(0, 0, 0);\">The BIBBOX (Basic Infrastructure Building Box) offers an easy installation, deployment and integration of open-source software solutions (Apps) in the fields of bioinformatics and biobanking.</span></p><p style=\"text-align:start\"><span style=\"color:rgb(0, 0, 0);\">In the BIBBOX framework, the software tools are simply a group of Docker Containers, ready to be used. Therefore, they can run quickly and reliably in any computing environment. By providing a catalog of pre-configured bioinformatics tools and applications, the BIBBOX allows users to install and run them in a standardized and reproducible manner. Among other applications, the Bibbox enables the integration of a FAIR Data Point into the respective apps.</span></p><p style=\"text-align:start\"><span style=\"color:rgb(0, 0, 0);\">Some key features of BIBBOX include:</span></p><ul><li><p><strong><span style=\"color:rgb(0, 0, 0);\">Application Catalog:</span></strong><span style=\"color:rgb(0, 0, 0);\"> A collection of bioinformatics tools and applications for various research tasks.</span></p></li><li><p><strong><span style=\"color:rgb(0, 0, 0);\">Containerization:</span></strong><span style=\"color:rgb(0, 0, 0);\"> Utilizes Docker to encapsulate applications and ensure consistent execution.</span></p></li><li><p><strong><span style=\"color:rgb(0, 0, 0);\">User Management:</span></strong><span style=\"color:rgb(0, 0, 0);\"> Provides user access control and permission management.</span></p></li><li><p><strong><span style=\"color:rgb(0, 0, 0);\">Fair Data Point (FDP):</span></strong><span style=\"color:rgb(0, 0, 0);\"> Provides a standardized and interoperable component or service for facilitating the discovery, access, and sharing of research data, ensuring transparency, accessibility, and reusability.</span></p></li></ul><p style=\"text-align:start\"><span style=\"color:rgb(0, 0, 0);\">Enjoy exploring the myriad possibilities that BIBBOX offers to you!</span></p>'))
    db.session.add(KeyValue(keys='contact', values='<p style=\"text-align:center\"><a href=\"mailto:paul.torke@medunigraz.at\" target=\"\"><u><span style=\"color:rgb(13, 110, 253);\">Paul Torke &lt;paul.torke@medunigraz.at&gt;</span></u></a></p><p style=\"text-align:center\"><a href=\"mailto:emilian.jungwirth@medunigraz.at\" target=\"\"><u><span style=\"color:rgb(13, 110, 253);\">Emilian Jungwirth &lt;emilian.jungwirth@medunigraz.at&gt;</span></u></a></p><p style=\"text-align:center\"><a href=\"mailto:markus.plass@medunigraz.at\" target=\"\"><u><span style=\"color:rgb(13, 110, 253);\">Markus Plass &lt;markus.plass@medunigraz.at&gt;</span></u></a></p><p style=\"text-align:center\"><a href=\"mailto:heimo.mueller@meduni-graz.at\" target=\"\"><u><span style=\"color:rgb(13, 110, 253);\">Heimo M\u00fcller &lt;heimo.mueller@medunigraz.at&gt;</span></u></a></p><p style=\"text-align:center\"><span style=\"color:rgb(33, 37, 41);\"><br><br></span></p><p style=\"text-align:center\"><a href=\"https://bibbox.org/\" target=\"_blank\"><u><span style=\"color:rgb(13, 110, 253);\">http//</span></u></a><a href=\"bibbox.org\" target=\"_blank\"><u><span style=\"color:rgb(13, 110, 253);\">bibbox.org</span></u></a></p>'))
    db.session.add(KeyValue(keys='imprint', values='<p style=\"text-align:center\"><strong><span style=\"color:rgb(33, 37, 41);\">Medical University Graz<br></span></strong><span style=\"color:rgb(33, 37, 41);\">Neue Stiftingtalstra\u00dfe 6<br>8010 Graz</span></p><p style=\"text-align:center\"><strong><span style=\"color:rgb(33, 37, 41);\">E-Mail: </span></strong><a href=\"mailto:heimo.mueller@medunigraz.at\"><u><span style=\"color:rgb(13, 110, 253);\">heimo.mueller@</span></u></a><a href=\"medunigraz.at\" target=\"_blank\"><u><span style=\"color:rgb(13, 110, 253);\">medunigraz.at</span></u></a></p><p style=\"text-align:center\"><strong><span style=\"color:rgb(33, 37, 41);\">Implementation</span></strong><span style=\"color:rgb(33, 37, 41);\"> by </span><a href=\"https://www.medunigraz.at/forschungszentren-institute/diagnostik-forschungszentrum-fuer-molekulare-biomedizin/forschung/genetische-und-umweltbedingte-krankheitsmechanismen/team-mueller\"><u><span style=\"color:rgb(13, 110, 253);\">Team M\u00fcller</span></u></a> at Medical University Graz</p><p style=\"text-align:center\"><span style=\"color:rgb(33, 37, 41);\"><br></span></p><p style=\"text-align:center\"><span style=\"color:rgb(33, 37, 41);\">In course of the projects:</span></p><p style=\"text-align:center\"><strong><span style=\"color:rgb(33, 37, 41);\">CY-Biobank</span></strong><span style=\"color:rgb(33, 37, 41);\"> grant agreement Nr. 857122</span></p><p style=\"text-align:center\"><strong><span style=\"color:rgb(33, 37, 41);\">HEAP</span></strong><span style=\"color:rgb(33, 37, 41);\"> grant agreement Nr. 874662</span></p>'))
    db.session.add(KeyValue(keys='partners', values='<p style=\"text-align:center\"><a href=\"https://heap-exposome.eu/\" target=\"_blank\"><strong><u><span style=\"color:rgb(13, 110, 253);\">HEAP</span></u></strong></a></p><p style=\"text-align:center\"><a href=\"https://biobank.cy/\" target=\"_blank\"><strong><u><span style=\"color:rgb(13, 110, 253);\">CY-Biobank</span></u></strong></a></p><p style=\"text-align:center\"><a href=\"https://www.bbmri-eric.eu/\" target=\"_blank\"><strong><u><span style=\"color:rgb(13, 110, 253);\">BBMRI-ERIC</span></u></strong></a></p><p style=\"text-align:center\"><a href=\"http://b3africa.org/\" target=\"_blank\"><strong><u><span style=\"color:rgb(13, 110, 253);\">B3Africa</span></u></strong></a></p>'))

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
    