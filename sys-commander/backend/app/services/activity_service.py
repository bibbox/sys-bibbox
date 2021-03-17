# -*- coding: utf-8 -*-
"""

ActivityService class - This class holds the method related to Activity manipulations.

"""

from backend.app.models.activity import Activity
from backend.app.services import SQLAlchemyService


class ActivityService(SQLAlchemyService):
    __model__ = Activity

    def __init__(self):
        # Creating a parent class ref to access parent class methods.
        self.parentClassRef = super(TaskService, self)

    def update(self, id):
        # Update "state" value, f.e. after finishing activity
        # load activity with id from db, set state to ____.
        # commit
        pass
