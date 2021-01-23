# -*- coding: utf-8 -*-
"""User Route for Demo application."""
import re
from flask import Blueprint
from flask import jsonify

from backend.app.api import api

from backend.app import app_celerey


@api.route("/tasks")
def  get_tasks():
    print ("get all celery tasks")
    i = app_celerey.control.inspect()   
    ativeTasks = i.active()
    scheduledTasks = i.reserved() 
  
    return jsonify( ativeTasks)

@api.route("/tasks/<int:id>")
def get_Task(id):
    return user
    return jsonify({"status": 200, "msg":"Details for Celery Task %d are"%id } )
