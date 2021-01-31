# -*- coding: utf-8 -*-
"""User Route for Demo application."""

from flask import Blueprint
from flask import Flask, request, jsonify

from backend.app import apiblueprint as api

route = Blueprint('command', __name__)

@app.route('/hello')
def publish_hello():
    sse.publish({"message": "Hello!"}, type='greeting')
    return "Message sent!"