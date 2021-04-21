# -*- coding: utf-8 -*-
"""

UserService class - This class holds the method related to User manipulations.

"""

from backend.app.models.user import User
from backend.app.services import SQLAlchemyService


class UserService(SQLAlchemyService):
    __model__ = User

    def __init__(self):
        # Creating a parent class ref to access parent class methods.
        self.parentClassRef = super(UserService, self)

