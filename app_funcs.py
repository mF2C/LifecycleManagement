"""
lifecycle manager rest-api methods

This is being developed for the MF2C Project: http://www.mf2c-project.eu/

Copyright: Roi Sucasas Font, Atos Research and Innovation, 2017.

This code is licensed under an Apache 2.0 license. Please, refer to the LICENSE.TXT file for more information

Created on 18 oct. 2018

@author: Roi Sucasas - ATOS
"""

import config as config
import lifecycle.lifecycle_operations as lifecycle_ops
import lifecycle.lifecycle_deployment as lifecycle_depl
import lifecycle.data.mF2C.handler_um as handler_um
import lifecycle.data.mF2C.handler_sla as handler_sla
import lifecycle.inter_lf_operations as operations
import lifecycle.data.data_adapter as data_adapter
import common.common as common
from common.common import OPERATION_START, OPERATION_STOP, OPERATION_RESTART, OPERATION_TERMINATE, OPERATION_START_JOB
from common.logs import LOG
from flask import Response, json


# getAgentConfig
def getAgentConfig():
    data = {
        'app': "Lifecycle Management REST API",
        'name': "Lifecycle Management REST API",
        'version': config.dic['VERSION'],
        'host': config.dic['HOST_IP'],
        'device-identifier': 'not-defined',
        'device-ip-address': 'not-defined',
        'user-identifier': 'not-defined',
        'properties': {
            'swarm-master': config.dic['DOCKER_SWARM'],
            'k8s-master': config.dic['K8S_MASTER'],
            'cimi-url': config.dic['CIMI_URL'],
            'mf2c': {
                'LIFECYCLE MANAGER': config.dic['URL_PM_LIFECYCLE'],
                'USER MANAGEMENT MODULE': config.dic['URL_AC_USER_MANAGEMENT'],
                'RECOMENDER_LANDSCAPER': config.dic['URL_PM_RECOM_LANDSCAPER'],
                'SERVICE MANAGER': config.dic['URL_AC_SERVICE_MNGMT'],
                'SLA MANAGER': config.dic['URL_PM_SLA_MANAGER']
            }
        }
    }
    resp = Response(json.dumps(data), status=200, mimetype='application/json')
    return resp


# getAgentInfo
def getAgentUMInfo():
    agent_um = {
        'device-id': 'not-defined',
        'user-id': 'not-defined',
        'user-profile': data_adapter.get_um_profile(),
        'sharing-model': data_adapter.get_um_sharing_model()
    }
    resp = Response(json.dumps(agent_um), status=200, mimetype='application/json')
    return resp


# getAgentInfo
def putAgentUMInfo(request):
    # 1. Parse and check input data
    data = request.get_json()

    # response
    resp = Response(json.dumps(data), status=200, mimetype='application/json')
    return resp


# getServiceInstance
def getServiceInstance(service_instance_id):
    if service_instance_id == "all":
        LOG.debug("LIFECYCLE: Lifecycle: get_all ")
        try:
            obj_response_cimi = common.ResponseCIMI()
            service_instances = data_adapter.get_all_service_instances(obj_response_cimi)

            if not service_instances is None:
                return common.gen_response_ok('Service instances content', 'service_instances', service_instances, "Msg", obj_response_cimi.msj)
            else:
                return common.gen_response(500, "Error in 'get_all' function", "Error_Msg", obj_response_cimi.msj)
        except:
            LOG.error('LIFECYCLE: Lifecycle: get_all: Exception')
            return common.gen_response(500, 'Exception', 'get_all', "-")
    else:
        LOG.debug("LIFECYCLE: Lifecycle: get: " + service_instance_id)
        try:
            obj_response_cimi = common.ResponseCIMI()
            service_instance = data_adapter.get_service_instance(service_instance_id, obj_response_cimi)

            if not service_instance is None and service_instance != -1:
                return common.gen_response_ok('Service instance content', 'service_instance_id', service_instance_id, 'service_instance', service_instance)
            else:
                return common.gen_response(500, "Error in 'get' function", "service_instance_id", service_instance_id, "Error_Msg", obj_response_cimi.msj)
        except:
            LOG.error('LIFECYCLE: Lifecycle: get: Exception')
            return common.gen_response(500, 'Exception', 'service_instance_id', service_instance_id)


# postServiceInstanceEvent
def postServiceInstanceEvent(request, service_instance_id):
    body = request.get_json()

    if not body or 'type' not in body or 'data' not in body:
        LOG.error('LIFECYCLE: REST API: postServiceInstanceEvent: Exception - parameter not found: type / data')
        return Response(json.dumps({'error': True, 'message': 'parameter not found: type / data'}), status=406, content_type='application/json')
    else:
        if body['type'] == "sla_notification":
            return handler_sla.handle_sla_notification(service_instance_id, body['data'])
        elif body['type'] == "um_warning":
            return handler_um.handle_warning(service_instance_id, body['data'])

    LOG.error("LIFECYCLE: REST API: postServiceInstanceEvent: type [" + body['type'] + "] not defined / implemented")
    return Response(json.dumps({'error': True, 'message': 'type not defined / implemented'}), status=501, content_type='application/json')


#
def putServiceInstance(request, service_instance_id):
    data = request.get_json()
    if 'operation' not in data:
        LOG.error('LIFECYCLE: REST API: putServiceInstance: Parameter not found: operation')
        return Response(json.dumps({'error': True, 'message': 'parameter not found: operation'}), status=406, content_type='application/json')

    # operations
    if data['operation'] == OPERATION_START:
        return lifecycle_ops.start(service_instance_id)
    elif data['operation'] == OPERATION_STOP:
        return lifecycle_ops.stop(service_instance_id)
    elif data['operation'] == OPERATION_RESTART:
        return lifecycle_ops.start(service_instance_id)
    elif data['operation'] == OPERATION_START_JOB:
        if 'parameters' not in data:
            LOG.error('LIFECYCLE: REST API: putServiceInstance: Parameter not found: parameters')
            return Response(json.dumps({'error': True, 'message': 'parameter not found: parameters'}), status=406, content_type='application/json')
        return lifecycle_ops.start_job(data, service_instance_id)
    else:
        LOG.error('LIFECYCLE: REST API: putServiceInstance: operation not defined / implemented')
        return Response(json.dumps({'error': True, 'message': 'operation not defined / implemented'}), status=501, content_type='application/json')


# deleteServiceInstance: deletes a service instance
def deleteServiceInstance(service_instance_id):
    if service_instance_id == "all":
        return lifecycle_ops.terminate_all()
    else:
        return lifecycle_ops.terminate(service_instance_id)


# postService: deploy a service in one or more agents
def postService(request):
    # 1. Parse and check input data
    data = request.get_json()
	
    agreement_id = "AGREEMENT_ID"
    if 'user_id' not in data:
        LOG.warning('LIFECYCLE: REST API: postService: Exception - parameter not found: user_id')
        user_id = "ADMIN"
        #return Response(json.dumps({'error': True, 'message': 'parameter not found: user_id'}), status=406, content_type='application/json')
    else:
        user_id = data['user_id']

    if 'service' not in data and 'service_id' not in data:
        LOG.error('LIFECYCLE: REST API: postService: Exception - parameter not found: service / service_id')
        return Response(json.dumps({'error': True, 'message': 'parameter not found: service /  service_id'}), status=406, content_type='application/json')

    # check if user exists
    #if not data_adapter.exist_user(data['user_id']):
    #    return common.gen_response(404, "Error", "user_id", data['user_id'], "message", "User ID not found")

    # 2. Get service
    # OPTION: full service defined in the request
    if 'service' in data:
        service = data['service']
    # OPTION: standalone mode (no mF2C)
    elif common.is_standalone_mode():
        LOG.error("LIFECYCLE: REST API: postService: Exception - STANDALONE_MODE enabled: parameters are not valid: ")
        return Response(json.dumps({'error': True, 'message': 'STANDALONE_MODE enabled: parameters are not valid'}), status=500, content_type='application/json')
    # OPTION: id service defined in the request
    else:
        service = data_adapter.get_service(data['service_id'])
        if service is None:
            LOG.error("LIFECYCLE: REST API: postService: Exception - service not found!")
            return Response(json.dumps({"error": True, "message": "service not found; [id=" + data['service_id'] + "]"}), status=500, content_type='application/json')

    # 3. Submits the service
    # OPTION: list of agents are defined in the request:
    # submit function returns a json with the content of the 'service_instance'
    if 'agents_list' in data:
        # using a predefined list of agents:
        return lifecycle_depl.submit_service_in_agents(service,
                                                       user_id, #data['user_id'],
                                                       agreement_id,
                                                       data['agents_list'],
                                                       check_service=True)
    # OPTION: submits the service with the help of the other mF2C components (landscaper, recommender ...)
    else:
        # using agent_decision module (landscaper, recommender...):
        return lifecycle_depl.submit(service,
                                     user_id, #data['user_id'],
                                     agreement_id)


####################################################################################################################


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
    if 'operation' not in data or 'agent' not in data:
        LOG.error('LIFECYCLE: REST API: putServiceInt: Exception - parameter not found: agent / operation')
        return Response(json.dumps({'error': True, 'message': 'parameter not found: agent / operation'}), status=406, content_type='application/json')

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
        LOG.error('LIFECYCLE: REST API: put: operation not defined / implemented')
        return Response(json.dumps({'error': True, 'message': 'operation not defined / implemented'}), status=501, content_type='application/json')
