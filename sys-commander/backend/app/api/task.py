# -*- coding: utf-8 -*-
"""Task Route for Demo application."""
import re
from flask import Flask, request, Blueprint, jsonify
from flask_restplus import Namespace, Api, Resource, fields
from backend.app import apiblueprint as api, app_celerey as app_celery, app, db, restapi

from backend.app.services.task_service import TaskService


api = Namespace('tasks', description='Task Resources')
restapi.add_namespace (api, '/tasks')


task_service = TaskService()

@api.route("/")
class TaskListAll(Resource):
    @api.doc("get all celery tasks")
    def get(self):
        # task_service.all()
        print ("get all celery tasks")
        i = app_celery.control.inspect()   
        activeTasks = i.active()
        scheduledTasks = i.reserved() 
        finishedTasks = "done placeholder" #i.done()
    
        return jsonify( activeTasks, scheduledTasks, finishedTasks )


@api.route("/active")
class TaskListActive(Resource):
    @api.doc("get all active celery tasks")
    def get(self):
        print ("get all active celery tasks")
        i = app_celery.control.inspect()   
        activeTasks = i.active()
    
        return jsonify( activeTasks )


@api.route("/scheduled")
class TaskListScheduled(Resource):
    @api.doc("get all scheduled tasks")
    def get(self):
        print ("get all scheduled celery tasks")
        i = app_celery.control.inspect()
        scheduledTasks = i.reserved() 
    
        return jsonify( scheduledTasks )


@api.route("/finished")
class TaskListFinished(Resource):
    @api.doc("get all finished celery tasks")
    def get(self):
        print ("get all scheduled celery tasks")
        i = app_celery.control.inspect()
        doneTasks = "done placeholder"  #i.done() 
    
        return jsonify( doneTasks )

@api.route("/<int:id>")
@api.doc(params={'id': 'task id'})
class Task(Resource):
    @api.doc("get celery task by ID")
    def get(self):
        print("get task-info of task: {}".format(id))
        return jsonify({"status": 200, "msg":"Details for Celery Task %d are"%id } )
