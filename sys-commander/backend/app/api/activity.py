# -*- coding: utf-8 -*-
"""Task Route for Demo application."""
import re
from flask import Flask, request, Blueprint, jsonify
from flask_restplus import Namespace, Api, Resource, fields
from backend.app import apiblueprint as api, app_celerey as app_celery, app, db, restapi

from backend.app.services.activity_service import ActivityService


api = Namespace('activities', description='Activity Resources')
restapi.add_namespace (api, '/activities')


activity_service = ActivityService()

@api.route("/")
class ActivityListAll(Resource):
    @api.doc("get all celery activities")
    def get(self):
        # task_service.all()
        print ("get all celery activities")
        i = app_celery.control.inspect()   
        activeTasks = i.active()
        scheduledTasks = i.reserved() 
        finishedTasks = "done placeholder" #i.done()
    
        return jsonify( activeTasks, scheduledTasks, finishedTasks )


@api.route("/active")
class ActivityListActive(Resource):
    @api.doc("get all active celery activities")
    def get(self):
        print ("get all active celery activities")
        i = app_celery.control.inspect()   
        activeTasks = i.active()
    
        return jsonify( activeTasks )


@api.route("/scheduled")
class ActivityListScheduled(Resource):
    @api.doc("get all scheduled activities")
    def get(self):
        print ("get all scheduled celery activities")
        i = app_celery.control.inspect()
        scheduledTasks = i.reserved() 
    
        return jsonify( scheduledTasks )


@api.route("/finished")
class ActivityListFinished(Resource):
    @api.doc("get all finished celery activities")
    def get(self):
        print ("get all scheduled celery activities")
        i = app_celery.control.inspect()
        doneTasks = "done placeholder"  #i.done() 
    
        return jsonify( doneTasks )

@api.route("/<int:id>")
@api.doc(params={'id': 'Activity id'})
class Activity(Resource):
    @api.doc("get celery task by ID")
    def get(self):
        print("get task-info of activity: {}".format(id))
        return jsonify({"status": 200, "msg":"Details for Celery Task %d are"%id } )
