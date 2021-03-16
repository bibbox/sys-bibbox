# -*- coding: utf-8 -*-
"""

TaskService class - This class holds the method related to Task manipulations.

"""

from backend.app.models.task import Task
from backend.app.services import SQLAlchemyService


class TaskService(SQLAlchemyService):
    __model__ = Task

    def __init__(self):
        # Creating a parent class ref to access parent class methods.
        self.parentClassRef = super(TaskService, self)

    def update(self, id):
        # Update "state" value, f.e. after finishing task
        # load task with id from db, set state to ____.
        # commit
        pass
