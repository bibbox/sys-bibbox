# -*- coding: utf-8 -*-
"""backend.api

    server blueprints/blueprints application package

"""

from flask import Blueprint

api = Blueprint('api', __name__)
print ("HELLO IN INIT OF FLASK API .....")

from backend.app.api import default, user, task 