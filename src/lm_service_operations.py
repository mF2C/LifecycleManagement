'''
Service operations
This is being developed for the MF2C Project: http://www.mf2c-project.eu/

Copyright: Roi Sucasas Font, Atos Research and Innovation, 2017.

This code is licensed under an Apache 2.0 license. Please, refer to the LICENSE.TXT file for more information

Created on 27 sept. 2017

@author: Roi Sucasas - ATOS
'''

#!/usr/bin/python3

import logs
from flask import Response, json, jsonify


# Service Operation: start
def start(service_id):
    try:
        logs.info('Service_Operation: starting service [' + service_id + '] ...')
        # TODO

    except:
        logs.error('Error (0): Service_Operation: start: Exception')
    return Response(jsonify({'Service_Operation': 'start', 'service_id': service_id}), status=200, content_type='application/json')


# Service Operation: restart
def restart(service_id):
    try:
        logs.info('Service_Operation: restarting service [' + service_id + '] ...')
        # TODO

    except:
        logs.error('Error (0): Service_Operation: restart: Exception')
    return Response(jsonify({'Service_Operation': 'restart', 'service_id': service_id}), status=200, content_type='application/json')


# Service Operation: stop
def stop(service_id):
    try:
        logs.info('Service_Operation: stopping service [' + service_id + '] ...')
        # TODO

    except:
        logs.error('Error (0): Service_Operation: stop: Exception')
    return Response(jsonify({'Service_Operation': 'stop', 'service_id': service_id}), status=200, content_type='application/json')
