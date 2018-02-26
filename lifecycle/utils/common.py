"""
Common functions
This is being developed for the MF2C Project: http://www.mf2c-project.eu/

Copyright: Roi Sucasas Font, Atos Research and Innovation, 2017.

This code is licensed under an Apache 2.0 license. Please, refer to the LICENSE.TXT file for more information

Created on 27 sept. 2017

@author: Roi Sucasas - ATOS
"""


from flask import Response, json, jsonify
from lifecycle.utils.logs import LOG


# Generate response 200
def gen_response_ok(message, key, value, key2=None, value2=None):
    dict = {'error': False, 'message': message}
    dict[key] = value
    if not (key2 is None) and not (value2 is None):
        dict[key2] = value2
    LOG.debug("Generate response OK; dict=" + str(dict))
    return dict


# Generate response ERROR
def gen_response(status, message, key, value, key2=None, value2=None):
    dict = {'error': True, 'message': message}
    dict[key] = value
    if not (key2 is None) and not (value2 is None):
        dict[key2] = value2
    LOG.debug('Generate response ' + str(status) + "; dict=" + str(dict))
    return Response(json.dumps(dict), status=status, content_type='application/json')