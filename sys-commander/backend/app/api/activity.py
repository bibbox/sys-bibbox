# -*- coding: utf-8 -*-
"""Task Route for Demo application."""
import re
from flask import Flask, request, Blueprint, jsonify
from flask_restplus import Namespace, Api, Resource, fields
from backend.app import apiblueprint as api, app_celerey as app_celery, app, db, restapi

from backend.app.services.activity_service import ActivityService
from backend.app.services.log_service import LogService


api = Namespace('activities', description='Activity Resources')
restapi.add_namespace (api, '/activities')


activity_service = ActivityService()
log_service = LogService()

'''
TODO
I've implemented these wrong - needs rework
 - Lukas
'''

@api.route("/")
class ActivityListAll(Resource):
    @api.doc("get all activities")
    def get(self):


        as_ = ActivityService()
        reply = as_.selectAll()
        return reply, 202

        # task_service.all()

        # print ("get all celery activities")
        # i = app_celery.control.inspect()   
        # activeTasks = i.active()
        # scheduledTasks = i.reserved() 
        # finishedTasks = "done placeholder" #i.done()
    
        # return jsonify( activeTasks, scheduledTasks, finishedTasks )

@api.route("/logs/<int:id>")
class ActivityListAll(Resource):
    @api.doc("get all logs from one activity")
    def get(self, id):
        ls = LogService()
        logs = ls.selectLogsFromActivity(id)
        return logs, 202


# @api.route("/active")
# class ActivityListActive(Resource):
#     @api.doc("get all active celery activities")
#     def get(self):
#         print ("get all active celery activities")
#         i = app_celery.control.inspect()   
#         activeTasks = i.active()
    
#         return jsonify( activeTasks )


# @api.route("/scheduled")
# class ActivityListScheduled(Resource):
#     @api.doc("get all scheduled activities")
#     def get(self):
#         print ("get all scheduled celery activities")
#         i = app_celery.control.inspect()
#         scheduledTasks = i.reserved() 
    
#         return jsonify( scheduledTasks )


# @api.route("/finished")
# class ActivityListFinished(Resource):
#     @api.doc("get all finished celery activities")
#     def get(self):
#         print ("get all scheduled celery activities")
#         i = app_celery.control.inspect()
#         doneTasks = "done placeholder"  #i.done() 
    
#         return jsonify( doneTasks )

@api.route("/active")
class Activity(Resource):
    @api.doc("get active activities")
    def get(self):
        return jsonify({"status": 200, "msg":"Details for Activity"} )
