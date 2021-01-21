import connexion
import six
import json
import sys  

sys.path.insert(1, "/opt/bibbox/sys-bibbox/sys-backend")
from helperFunctions import AppController
from mainFunctions import MainFunctions


def listApps():  # noqa: E501
    """Get a list of all apps in the store

     
    """
    try:
        controller = MainFunctions()
        response = controller.listAppsExtended(), 200
    except KeyError:
        response = {}, 404

    return response




def listInstalledApps():  # noqa: E501
    """Get a list of all apps in the store

     
    """
    try:
        controller = MainFunctions()
        response = controller.listInstalledApps(), 200
    except KeyError:
        response = {}, 404

    return response

def startApp(instanceName):
    """Start an app

     
    """
    try:
        controller = MainFunctions()
        response = controller.startApp(instanceName), 200
    except KeyError:
        response = {}, 404

    return response

def stopApp(instanceName):
    """Stop an app

     
    """
    try:
        controller = MainFunctions()
        response = controller.stopApp(instanceName), 200
    except KeyError:
        response = {}, 404

    return response

def removeApp(instanceName):
    """Start an app

     
    """
    try:
        controller = MainFunctions()
        response = controller.removeApp(instanceName), 200
    except KeyError:
        response = {}, 404

    return response

def copyApp(instanceName, newName):
    """Start an app

     
    """
    try:
        controller = MainFunctions()
        response = controller.copyApp(instanceName, newName), 200
    except KeyError:
        response = {}, 404

    return response

def getStatus(instanceName):
    """Start an app

     
    """
    try:
        controller = MainFunctions()
        response = controller.getStatus(instanceName), 200
    except KeyError:
        response = {}, 404

def startSystem():
    """Start an app

     
    """
    try:
        controller = MainFunctions()
        response = controller.startBibbox(), 200
    except KeyError:
        response = {}, 404

    return response

def stopSystem():
    """Start an app

     
    """
    try:
        controller = MainFunctions()
        response = controller.stopBibbox(), 200
    except KeyError:
        response = {}, 404

    return response

def checkSystem():
    """Start an app

     
    """
    try:
        controller = MainFunctions()
        response = controller.checkSystem(), 200
    except KeyError:
        response = {}, 404

    return response

def restartSystem():
    """Start an app

     
    """
    try:
        controller = MainFunctions()
        response = controller.restartBibbox(), 200
    except KeyError:
        response = {}, 404

    return response