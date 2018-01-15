"""
auth functions
This is being developed for the MF2C Project: http://www.mf2c-project.eu/

Copyright: Roi Sucasas Font, Atos Research and Innovation, 2017.

This code is licensed under an Apache 2.0 license. Please, refer to the LICENSE.TXT file for more information

Created on 27 sept. 2017

@author: Roi Sucasas - ATOS
"""

from flask import request, Response
from functools import wraps


# This function is called to check if a username / password combination is valid.
def __check_auth(username, password):
    return username == 'admin' and password == 'secret'


# Sends a 401 response that enables basic auth
def __authenticate():
    return Response("Could not verify your access level for that URL.\nYou have to login with proper credentials",
                    401,
                    {'WWW-Authenticate': 'Basic realm="Login Required"'})


#
def requires_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.authorization
        if not auth or not __check_auth(auth.username, auth.password):
            return __authenticate()
        return f(*args, **kwargs)
    return decorated