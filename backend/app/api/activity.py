# -*- coding: utf-8 -*-
"""Task Route for Demo application."""
import re
from flask import Flask, request, Blueprint, jsonify
from flask_restplus import Namespace, Api, Resource, fields
from backend.app import apiblueprint as api, app_celerey as app_celery, app, db, restapi

from backend.app.services.activity_service import ActivityService
from backend.app.services.log_service import LogService
from backend.app.bibbox.docker_handler import DockerHandler


api = Namespace('activities', description='Activity Resources')
restapi.add_namespace (api, '/activities')


activity_service = ActivityService()
log_service = LogService()

@api.route("/")
class ActivityListAll(Resource):
    @api.doc("get all activities")
    def get(self):
        as_ = ActivityService()
        reply = as_.selectAll()
        return reply, 202

@api.route("/logs/<int:activityID>")
class ActivityListAll(Resource):
    @api.doc("get all logs from one activity")
    def get(self, activityID):
        ls = LogService()
        logs = ls.selectLogsFromActivity(activityID)
        return logs, 202

@api.route("/syslogs")
class SysLogs(Resource):
    @api.doc("get all logs from sys-containers as dict")
    def get(self):
        logs = {}
        try:
            dh = DockerHandler()
            logs = dh.docker_getContainerLogs('sys-bibbox')
        except Exception as ex:
            print(ex)
            logs = {'error': ex}
        return logs, 200


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

# @api.route("/active")
# class Activity(Resource):
#     @api.doc("get active activities")
#     def get(self):
#         return jsonify({"status": 200, "msg":"Details for Activity"} )
