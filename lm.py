"""
lifecycle manager rest-api methods

This is being developed for the MF2C Project: http://www.mf2c-project.eu/

Copyright: Roi Sucasas Font, Atos Research and Innovation, 2017.

This code is licensed under an Apache 2.0 license. Please, refer to the LICENSE.TXT file for more information

Created on 18 oct. 2018

@author: Roi Sucasas - ATOS
"""

import lifecycle.lifecycle as lifecycle
import lifecycle.lifecycle_v2 as lifecycle_v2
import lifecycle.mF2C.handler_um as handler_um
import lifecycle.mF2C.handler_sla as handler_sla
import lifecycle.operations as operations
import lifecycle.mF2C.mf2c as mf2c
import common.common as common
from common.common import OPERATION_START, OPERATION_STOP, OPERATION_RESTART, OPERATION_TERMINATE, OPERATION_START_JOB
from common.logs import LOG
from flask import Response, json


#
def getServiceInstance(service_instance_id):
    if service_instance_id == "all":
        return lifecycle.get_all()
    else:
        return lifecycle.get(service_instance_id)


#
def postServiceInstanceEvent(request, service_instance_id):
    body = request.get_json()
    LOG.info('body: ' + str(body))
    if not body or 'type' not in body or 'data' not in body:
        LOG.error('Lifecycle-Management: REST API: post: Exception - parameter not found: type / data')
        return Response(json.dumps({'error': True, 'message': 'parameter not found: type / data'}),
                        status=406, content_type='application/json')
    else:
        if body['type'] == "sla_notification":
            return handler_sla.handle_sla_notification(service_instance_id, body['data'])
        elif body['type'] == "um_warning":
            return handler_um.handle_warning(service_instance_id, body['data'])
    LOG.error("Lifecycle-Management: REST API: post: type [" + body['type'] + "] not defined / implemented")
    return Response(json.dumps({'error': True, 'message': 'type not defined / implemented'}),
                    status=501, content_type='application/json')


#
def putServiceInstance(request, service_instance_id):
    data = request.get_json()
    if 'operation' not in data:
        LOG.error('Lifecycle-Management: REST API: put: Parameter not found: operation')
        return Response(
            json.dumps({'error': True, 'message': 'parameter not found: operation'}),
            status=406, content_type='application/json')
    # operations
    if data['operation'] == OPERATION_START:
        return lifecycle.start(service_instance_id)
    elif data['operation'] == OPERATION_STOP:
        return lifecycle.stop(service_instance_id)
    elif data['operation'] == OPERATION_RESTART:
        return lifecycle.start(service_instance_id)
    elif data['operation'] == OPERATION_START_JOB:
        if 'parameters' not in data:
            LOG.error('Lifecycle-Management: REST API: put: Parameter not found: parameters')
            return Response(json.dumps({'error': True, 'message': 'parameter not found: parameters'}),
                            status=406, content_type='application/json')
        return lifecycle.start_job(data, service_instance_id)
    else:
        LOG.error('Lifecycle-Management: REST API: put: operation not defined / implemented')
        return Response(json.dumps({'error': True, 'message': 'operation not defined / implemented'}),
                        status=501, content_type='application/json')


# deleteServiceInstance: deletes a service instance
def deleteServiceInstance(service_instance_id):
    if service_instance_id == "all":
        return lifecycle.terminate_all()
    else:
        return lifecycle.terminate(service_instance_id)


# postService1: deploy a service in one or more agents (deprecated)
def postService1(request):
    data = request.get_json()
    if 'user_id' not in data or 'agreement_id' not in data:
        LOG.error('Lifecycle-Management: REST API: post: Exception - parameter not found: user_id / agreement_id')
        return Response(json.dumps({'error': True, 'message': 'parameter not found: user_id / agreement_id'}),
                        status=406, content_type='application/json')
    elif 'service' not in data and 'service_id' not in data:
        LOG.error('Lifecycle-Management: REST API: post: Exception - parameter not found: service / service_id')
        return Response(json.dumps({'error': True, 'message': 'parameter not found: service /  service_id'}),
                        status=406, content_type='application/json')

    if 'service' in data:
        service = data['service']
    elif 'service' not in data and 'agents_list' not in data and common.is_standalone_mode():
        LOG.error("Lifecycle-Management: REST API: post: Exception - STANDALONE_MODE enabled: parameters are not valid: ")
        return Response(json.dumps({'error': True, 'message': 'STANDALONE_MODE enabled: parameters are not valid'}),
                        status=500, content_type='application/json')
    else:
        service = mf2c.service_management_get_service(data['service_id'])
        if service is None:
            LOG.error("Lifecycle-Management: REST API: post: Exception - service not found!")
            return Response(json.dumps({"error": True, "message": "service not found; [id=" + data['service_id'] + "]"}),
                            status=500, content_type='application/json')

    # submit function returns a json with the content of the 'service_instance'
    if 'agents_list' in data:
        # using a predefined list of agents:
        return lifecycle.submit_service_in_agents(service, data['user_id'], data['agreement_id'],
                                                  data['agents_list'], check_service=True)
    else:
        # using agent_decision module (landscaper, recommender...):
        return lifecycle.submit(service, data['user_id'], data['agreement_id'])


# postService: deploy a service in one or more agents
def postService(request):
    data = request.get_json()
    if 'user_id' not in data or 'agreement_id' not in data:
        LOG.error('Lifecycle-Management: REST API: post: Exception - parameter not found: user_id / agreement_id')
        return Response(json.dumps({'error': True, 'message': 'parameter not found: user_id / agreement_id'}),
                        status=406, content_type='application/json')
    elif 'service' not in data and 'service_id' not in data:
        LOG.error('Lifecycle-Management: REST API: post: Exception - parameter not found: service / service_id')
        return Response(json.dumps({'error': True, 'message': 'parameter not found: service /  service_id'}),
                        status=406, content_type='application/json')

    if 'service' in data:
        service = data['service']
    elif common.is_standalone_mode():
        LOG.error(
            "Lifecycle-Management: REST API: post: Exception - STANDALONE_MODE enabled: parameters are not valid: ")
        return Response(json.dumps({'error': True, 'message': 'STANDALONE_MODE enabled: parameters are not valid'}),
                        status=500, content_type='application/json')
    else:
        service = mf2c.service_management_get_service(data['service_id'])
        if service is None:
            LOG.error("Lifecycle-Management: REST API: post: Exception - service not found!")
            return Response(
                json.dumps({"error": True, "message": "service not found; [id=" + data['service_id'] + "]"}),
                status=500, content_type='application/json')

    # submit function returns a json with the content of the 'service_instance'
    if 'agents_list' in data:
        # using a predefined list of agents:
        return lifecycle_v2.submit_service_in_agents(service, data['user_id'], data['agreement_id'],
                                                     data['agents_list'], check_service=True)
    else:
        # using agent_decision module (landscaper, recommender...):
        return lifecycle_v2.submit(service, data['user_id'], data['agreement_id'])


####################################################################################################################


# postServiceInt: deploy a service instance in the device / agent
def postServiceInt(request):
    data = request.get_json()
    if 'service' not in data or 'agent' not in data:
        LOG.error('Lifecycle-Management: REST API: post: Exception - parameter not found: service / agent')
        return Response(json.dumps({'error': True, 'message': 'parameter not found: service /  agent'}),
                        status=406, content_type='application/json')
    return operations.deploy(data['service'], data['agent'])


#
def putServiceInt(request):
    data = request.get_json()
    if 'operation' not in data or 'agent' not in data:
        LOG.error('Lifecycle-Management: REST API: put: Exception - parameter not found: agent / operation')
        return Response(
            json.dumps({'error': True, 'message': 'parameter not found: agent / operation'}),
            status=406, content_type='application/json')
    # operations
    if data['operation'] == OPERATION_START:
        return operations.start(data['agent'])
    elif data['operation'] == OPERATION_STOP:
        return operations.stop(data['agent'])
    elif data['operation'] == OPERATION_RESTART:
        return operations.start(data['agent'])
    elif data['operation'] == OPERATION_TERMINATE:
        return operations.terminate(data['agent'])
    else:
        LOG.error('Lifecycle-Management: REST API: put: operation not defined / implemented')
        return Response(json.dumps({'error': True, 'message': 'operation not defined / implemented'}),
                        status=501, content_type='application/json')