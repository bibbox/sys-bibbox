"""

"""

import unittest
import os
from coverage import coverage
from flask_script import Manager

from backend.app import db, create_app
from backend.app.models.user  import User
from backend.app.models.app  import BibboxApp
from backend.app.models.activity import Activity
from backend.app.models.log import Log

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

manager = Manager(app)

print ("=========== MANAGE.PY ENVIRONMENT ============")
print ("FLASK_CONFIG = ", os.environ["FLASK_CONFIG"])
print ("SQLSTRING= ", app.config["DB_SERVICE"])

@manager.command
def test():
    """Runs the unit tests without test coverage."""
    test_suite = unittest.TestLoader().discover('tests', pattern='test*.py')
    result = unittest.TextTestRunner(verbosity=2).run(test_suite)
    if result.wasSuccessful():
        return 0
    return 1

@manager.command
def cov():
    """Runs the unit tests with coverage."""
    tests = unittest.TestLoader().discover('tests', pattern='test*.py')
    result = unittest.TextTestRunner(verbosity=2).run(tests)
    if result.wasSuccessful():
        COV.stop()
        COV.save()
        print('Coverage Summary:')
        COV.report()
        COV.html_report(directory='tests/coverage')
        COV.erase()
        return 0
    return 1


@manager.command
def recreate_db():
    db.drop_all()
    db.create_all()
    db.session.commit()

@manager.command
def seed_db():
    """Seed the user table in test_db database."""
    db.session.add(User(
        username='v',
        email='v@bibbox.com',
        password_hash =  pwd_context.encrypt('vendetta')
    ))
    db.session.add(User(
        username='mue',
        email = 'heimo.mueller@mac.com',
        password_hash = pwd_context.encrypt('vendetta')
    ))
    db.session.add(User(
        username = 'admin',
        email = 'admin@admin.at',
        password_hash = pwd_context.encrypt('vendetta')
    ))


    ## start of debug-test. remove later
    try:
        # testing if task table works
        import time
        from datetime import datetime
        db.session.add(Activity(
            name = "test instance.installInstance",
            type_ = "INSTALLAPP",
            start_time = datetime.fromtimestamp(time.time() - 100),
            finished_time = datetime.fromtimestamp(time.time()),
            state = "FINISHED",
            result = "SUCCESS"
        ))

        db.session.add(Log(
            log_message = "this is test-log-message 1 for task with id 1",
            type_ = "INFO",
            activity_id = 1
        ))

        db.session.add(Log(
            log_message = "this is test-log-message 2 for task with id 1",
            type_ = "WARNING",
            activity_id = 1
        ))

    except Exception as ex:
        print("Adding Task entry failed. Reason: {}".format(ex))
    ## end of debug test


    db.session.commit()

if __name__ == '__main__':
    manager.run()
