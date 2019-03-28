"""
lifecycle manager rest-api methods

This is being developed for the MF2C Project: http://www.mf2c-project.eu/

Copyright: Roi Sucasas Font, Atos Research and Innovation, 2017.

This code is licensed under an Apache 2.0 license. Please, refer to the LICENSE.TXT file for more information

Created on 18 oct. 2018

@author: Roi Sucasas - ATOS
"""

import config as config
import lifecycle.inter_lf_operations as operations
from common.common import OPERATION_START, OPERATION_STOP, OPERATION_RESTART, OPERATION_TERMINATE, OPERATION_START_JOB
from common.logs import LOG
from flask import Response, json


# getAgentConfig
def getAgentConfig():
    data = {
        'app': "(micro)Lifecycle Management REST API",
        'name': "(micro)Lifecycle Management REST API",
        'version': config.dic['VERSION'],
        'host': config.dic['HOST_IP'],
        'device-identifier': 'not-defined',
        'device-ip-address': 'not-defined',
        'user-identifier': 'not-defined',
        'properties': {
            'swarm-master': config.dic['DOCKER_SWARM'],
            'k8s-master': config.dic['K8S_MASTER']
        }
    }
    resp = Response(json.dumps(data), status=200, mimetype='application/json')
    return resp


# postServiceInt: deploy a service instance in the device / agent
def postServiceInt(request):
    data = request.get_json()
    if 'service' not in data or 'agent' not in data:
        LOG.error('LIFECYCLE: REST API: postServiceInt: Exception - parameter not found: service / agent')
        return Response(json.dumps({'error': True, 'message': 'parameter not found: service /  agent'}), status=406, content_type='application/json')
    return operations.deploy(data['service'], data['agent'])


# putServiceInt
def putServiceInt(request):
    data = request.get_json()
    if 'service' not in data or 'operation' not in data or 'agent' not in data:
        LOG.error('LIFECYCLE: REST API: putServiceInt: Exception - parameter not found: service / agent / operation')
        return Response(json.dumps({'error': True, 'message': 'parameter not found: service / agent / operation'}), status=406, content_type='application/json')

    # operations
    if data['operation'] == OPERATION_START:
        return operations.start(data['service'], data['agent'])
    elif data['operation'] == OPERATION_STOP:
        return operations.stop(data['service'], data['agent'])
    elif data['operation'] == OPERATION_RESTART:
        return operations.start(data['service'], data['agent'])
    elif data['operation'] == OPERATION_TERMINATE:
        return operations.terminate(data['service'], data['agent'])
    else:
        LOG.error('LIFECYCLE: REST API: putServiceInt: operation not defined / implemented')
        return Response(json.dumps({'error': True, 'message': 'operation not defined / implemented'}), status=501, content_type='application/json')
