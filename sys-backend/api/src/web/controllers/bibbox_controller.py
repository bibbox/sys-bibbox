import connexion
import six
import json
import sys  
#from .. import util

sys.path.insert(1, "/opt/bibbox/sys-bibbox/sys-backend")
from bibboxbackend import AppController


def listApps():  # noqa: E501
    """Get a list of all apps in the store

     
    """
    try:
        controller = AppController()
        response = controller.listApps(), 200
    except KeyError:
        response = {}, 404
    #response = "hello"

    return response




def listInstalledApps():  # noqa: E501
    """Get a list of all apps in the store

     
    """
    try:
        controller = AppController()
        response = controller.listInstalledApps(), 200
    except KeyError:
        response = {}, 404
    #response = "hello"

    return response

listApps()