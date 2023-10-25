# -*- coding: utf-8 -*-
"""

ActivityService class - This class holds the method related to Activity manipulations.

"""
import time
from datetime import datetime
from sqlalchemy import desc


from backend.app import db
from backend.app.models.activity import Activity
from backend.app.services import SQLAlchemyService
from backend.app.services.socketio_service import emitActivityRefresh
from backend.app.services.keycloak_service import KeycloakAdminService

class ActivityService(SQLAlchemyService):
    __model__ = Activity

    def __init__(self):
        # Creating a parent class ref to access parent class methods.
        self.parentClassRef = super(ActivityService, self)

    def create(self, name, type_,user_id= None):
        '''
        Inserts a new 'Activity' entry into the DB.
        Returns the ID of the newly created Activity.
        '''

        ac = Activity(
            name = name,
            type_ = type_,
            start_time = datetime.fromtimestamp(time.time()),
            finished_time = None,
            state = "RUNNING",
            result = None,
            user_id= user_id
        )

        db.session.add(ac)
        db.session.commit()
        db.session.refresh(ac)

        emitActivityRefresh()

        return ac.id


    def update(self, id, state, result):
        '''
        Updates state and/or result property of 'Activity' entry with given ID in DB.
        '''

        activity = db.session \
                        .query(Activity) \
                        .filter(Activity.id == id) \
                        .update({
                            'finished_time' : datetime.fromtimestamp(time.time()),
                            'state'         : state,
                            'result'        : result
        })

        db.session.commit()

        emitActivityRefresh()

    def selectAll(self,user_id=None, skip_others=True,limit=50):
        res = db.session.query(Activity).order_by(desc(Activity.id))
        activity_lst = list()
        kc_admin = KeycloakAdminService()
        for activity in res:
            if skip_others and user_id is not None and user_id != activity.user_id:
                continue
            user={
                "id": None,
                "username":None,
                "firstName": None,
                "lastName": None,
            }
            try:
                user_ = kc_admin.get_user(activity.user_id)
                user['id']=user_.get('id',None)
                user['username']=user_.get('username',None)
                user['firstName']=user_.get('firstName',None)
                user['lastName']=user_.get('lastName',None)

            except Exception as e:
                print(e)

            activity_lst.append({
                'id'            : activity.id,
                'name'          : activity.name, 
                'type'          : activity.type_, 
                'start_time'    : str(activity.start_time.strftime("%d.%m.%Y %H:%M:%S")),
                'finished_time' : str(activity.finished_time.strftime("%d.%m.%Y %H:%M:%S")) if activity.finished_time else '',
                'state'         : activity.state,
                'result'        : activity.result,
                'user_id'       : activity.user_id,
                'user'      : user
            })
            if len(activity_lst) >= limit:
                break
        return activity_lst
        