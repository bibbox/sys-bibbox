# -*- coding: utf-8 -*-
"""backend.api

    server blueprints/blueprints application package

"""

from flask import Blueprint

api = Blueprint('api', __name__)
from backend.app.api import default, user, catalogue, task 