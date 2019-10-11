"""
lifecycle manager rest-api methods

This is being developed for the MF2C Project: http://www.mf2c-project.eu/

Copyright: Roi Sucasas Font, Atos Research and Innovation, 2017.

This code is licensed under an Apache 2.0 license. Please, refer to the LICENSE.TXT file for more information

Created on 18 oct. 2018

@author: Roi Sucasas - ATOS
"""


import config as config
import lifecycle.connectors.connector as connector
import lifecycle.operations as lifecycle_ops
import lifecycle.deployment as lifecycle_depl
import lifecycle.events.handler_um as handler_um
import lifecycle.events.handler_sla as handler_sla
import lifecycle.events.handler_qos as handler_qos
import lifecycle.int_operations as operations
import lifecycle.data.data_adapter as data_adapter
from lifecycle import common as common
from lifecycle.common import OPERATION_START, OPERATION_STOP, OPERATION_RESTART, OPERATION_TERMINATE, OPERATION_START_JOB
from lifecycle.logs import LOG
from flask import Response, json


# getAgentConfig
def getAgentConfig():
    data = {
        'app': "Lifecycle Management REST API",
        'name': "Lifecycle Management REST API",
        'mode': config.dic['LM_MODE'],
        'version': config.dic['VERSION'],
        'host': data_adapter.get_host_ip(),
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


# isUMAlive
def isUMAlive():
    if not connector.user_management_check_avialability() is None:
        return Response(json.dumps({'res': 'ok'}), status=200, mimetype='application/json')
    else:
        return common.gen_response(500, 'Exception', 'isUMAlive', "user_management_check_avialability returned None")


# getCheckAgentUMInfo
def getCheckAgentUMInfo():
    result = connector.user_management_check_avialability()
    if not result is None:
        agent_um = {
            "message": result['message'],
            "sharing_model": result['sharing_model'],
            "result": result['result']
        }
    else:
        agent_um = {
            "message": result['message'],
            "sharing_model": {},
            "result": False
        }
    resp = Response(json.dumps(agent_um), status=200, mimetype='application/json')
    return resp


# getCheckAgentSwarm
def getCheckAgentSwarm():
    result = data_adapter.get_check_swarm()

    if not result is None:
        agent_um = {
            'device-id': 'not-defined',
            'user-id': 'not-defined',
            'message': result['message'],
            'result': result['is_swarm_node']
        }
    else:
        agent_um = {
            'device-id': 'not-defined',
            'user-id': 'not-defined',
            'message': 'not-defined',
            'result': False
        }
    resp = Response(json.dumps(agent_um), status=200, mimetype='application/json')
    return resp


# getServiceInstance
def getServiceInstance(service_instance_id):
    if service_instance_id == "all":
        LOG.debug("[lifecycle.app_funcs] [getServiceInstance] Call to 'get all' ")
        try:
            obj_response_cimi = common.ResponseCIMI()
            service_instances = data_adapter.get_all_service_instances(obj_response_cimi)

            if not service_instances is None:
                return common.gen_response_ok('Service instances content', 'service_instances', service_instances, "Msg", obj_response_cimi.msj)
            else:
                return common.gen_response(500, "Error in 'get_all' function", "Error_Msg", obj_response_cimi.msj)
        except:
            LOG.exception("[lifecycle.app_funcs] [getServiceInstance] Exception. Returning error 500 ...")
            return common.gen_response(500, 'Exception', 'get_all', "-")
    else:
        LOG.debug("[lifecycle.app_funcs] [getServiceInstance] " + service_instance_id)
        try:
            obj_response_cimi = common.ResponseCIMI()
            service_instance = data_adapter.get_service_instance(service_instance_id, obj_response_cimi)

            if not service_instance is None and service_instance != -1:
                return common.gen_response_ok('Service instance content', 'service_instance_id', service_instance_id, 'service_instance', service_instance)
            elif service_instance == -1:
                return common.gen_response_ok('Service instance not found', 'service_instance_id', service_instance_id, 'service_instance', {})
            else:
                return common.gen_response(500, "Error in 'get' function", "service_instance_id", service_instance_id, "Error_Msg", obj_response_cimi.msj)
        except:
            LOG.exception('[lifecycle.app_funcs] [getServiceInstance] Exception. Returning error 500 ...')
            return common.gen_response(500, 'Exception', 'service_instance_id', service_instance_id)


# getServiceInstanceReport
def getServiceInstanceReport(service_instance_id):
    LOG.debug("[lifecycle.app_funcs] [getServiceInstanceReport] " + service_instance_id)
    try:
        service_instance_report = data_adapter.get_service_instance_report(service_instance_id)

        if not service_instance_report is None and service_instance_report != -1:
            return common.gen_response_ok('Service Operation Report content', 'service_instance_id', service_instance_id, 'report', service_instance_report)
        else:
            LOG.warning("[lifecycle.app_funcs] [getServiceInstanceReport] service_instance_report is None")
            return common.gen_response(500, "Error in 'get' function", "service_instance_id", service_instance_id)
    except:
        LOG.exception('[lifecycle.app_funcs] [getServiceInstanceReport] Exception')
        return common.gen_response(500, 'Exception', 'service_instance_id', service_instance_id)


# postServiceInstanceEvent
def postServiceInstanceEvent(request):
    body = request.get_json()
    if not body or 'type' not in body or 'data' not in body:
        LOG.error('[lifecycle.app_funcs] [postServiceInstanceEvent] Exception - parameter not found: type / data')
        return Response(json.dumps({'error': True, 'message': 'parameter not found: type / data'}), status=406, content_type='application/json')
    else:
        if body['type'] == "sla_notification":
            return handler_sla.handle_sla_notification(body['data'])
        elif body['type'] == "um_warning":
            return handler_um.handle_warning(body['data'])
        elif body['type'] == "qos_enforcement":
            return handler_qos.handle_qos_notification(body['data'])

    LOG.error("[lifecycle.app_funcs] [postServiceInstanceEvent] type [" + body['type'] + "] not defined / implemented")
    return Response(json.dumps({'error': True, 'message': 'type not defined / implemented'}), status=501, content_type='application/json')


# putServiceInstance: start / stop a service instance
def putServiceInstance(request, service_instance_id):
    data = request.get_json()
    if 'operation' not in data:
        LOG.error('[lifecycle.app_funcs] [putServiceInstance] Parameter not found: operation')
        return Response(json.dumps({'error': True, 'message': 'parameter not found: operation'}), status=406, content_type='application/json')

    # operations
    if data['operation'] == OPERATION_START:
        return lifecycle_ops.start(service_instance_id)
    elif data['operation'] == OPERATION_STOP:
        return lifecycle_ops.stop(service_instance_id)
    elif data['operation'] == OPERATION_RESTART:
        return lifecycle_ops.start(service_instance_id)
    else:
        LOG.error('[lifecycle.app_funcs] [putServiceInstance] operation not defined / implemented')
        return Response(json.dumps({'error': True, 'message': 'operation not defined / implemented'}), status=501, content_type='application/json')


# putServiceInstanceCOMPSs: start a COMPSs job
def putServiceInstanceCOMPSs(request, service_instance_id):
    data = request.get_json()
    if 'operation' not in data or 'ceiClass' not in data or 'className' not in data or 'hasResult' not in data or 'methodName' not in data or 'parameters' not in data:
        LOG.error('[lifecycle.app_funcs] [putServiceInstanceCOMPSs] Parameter not found: operation / ceiClass / className / hasResult / methodName / parameters')
        return Response(json.dumps({'error': True, 'message': 'Parameter not found: operation / ceiClass / className / hasResult / methodName / parameters'}),
                        status=406,
                        content_type='application/json')
    # operations
    if data['operation'] == OPERATION_START_JOB:
        if 'parameters' not in data:
            LOG.error('[lifecycle.app_funcs] [putServiceInstanceCOMPSs] Parameter not found: parameters')
            return Response(json.dumps({'error': True, 'message': 'parameter not found: parameters'}), status=406, content_type='application/json')
        return lifecycle_ops.start_job(data, service_instance_id)
    else:
        LOG.error('[lifecycle.app_funcs] [putServiceInstanceCOMPSs] operation not defined / implemented')
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
    LOG.info("***************************************************************************************")
    LOG.info("[lifecycle.app_funcs] [postService] Launching new service [" + str(data) + "] ...")

    # USER_ID:
    if 'user_id' not in data:
        LOG.debug("[lifecycle.app_funcs] [postService] Parameter not found: 'user_id'. Retrieving 'user_id' value from agent ...")
        res = connector.user_management_get_current("user") #data_adapter.get_um_current("user")
        user_id = "ADMIN" # TODO
        try:
            if res is not None and 'user_id' in res and res['user_id'].strip():
                user_id = res['user_id']
        except:
            LOG.exception("[lifecycle.app_funcs] [postService] Exception; Error parsing 'res' variable")
    else:
        user_id = data['user_id']
    LOG.info("[lifecycle.app_funcs] [postService] user: " + user_id)

    # SLA TEMPLATE
    #   (SERVICE) :sla_templates [{:href "sla-template/sla-template-id-1"}, {:href "sla-template/sla-template-id-2"}]
    if 'sla_template' not in data:
        LOG.error("[lifecycle.app_funcs] [postService] Parameter not found: 'sla_template'")
        sla_template_id = "SLA_TEMPLATE_ID" # TODO
    else:
        LOG.debug("[lifecycle.app_funcs] [postService] Parameter found: 'sla_template': " + data['sla_template'])
        sla_template_id = data['sla_template']
    LOG.info("[lifecycle.app_funcs] [postService] sla_template: " + sla_template_id)

    # SERVICE:
    if 'service' not in data and 'service_id' not in data:
        LOG.error('[lifecycle.app_funcs] [postService] Exception - parameter not found: service / service_id')
        return Response(json.dumps({'error': True, 'message': 'parameter not found: service /  service_id'}),
                        status=406,
                        content_type='application/json')

    # SERVICE_INSTANCE_ID:
    if 'service_instance_id' in data:
        LOG.info("[lifecycle.app_funcs] [postService] This is a 'FORWARD REQUEST' from one child agent!")
        service_instance_id = data['service_instance_id']
    else:
        service_instance_id = None

    # 2. Get service
    # OPTION: full service defined in the request
    if 'service' in data:
        service = data['service']
    # OPTION: standalone mode (no mF2C)
    elif common.is_standalone_mode():
        LOG.error("[lifecycle.app_funcs] [postService] Exception - STANDALONE_MODE enabled: parameters are not valid: ")
        return Response(json.dumps({'error': True, 'message': 'STANDALONE_MODE enabled: parameters are not valid'}),
                        status=500,
                        content_type='application/json')
    # OPTION: id service defined in the request
    else:
        service = data_adapter.get_service(data['service_id'])
        if service is None or service == -1:
            LOG.error("[lifecycle.app_funcs] [postService] Service not found!")
            return Response(json.dumps({"error": True, "message": "service not found; [id=" + data['service_id'] + "]"}),
                            status=500,
                            content_type='application/json')

    LOG.info("[lifecycle.app_funcs] [postService] Deploying service ...")
    LOG.info("[lifecycle.app_funcs] [postService] " + str(service))

    # 3. Submits the service
    # OPTION A: list of agents are defined in the request:
    #         submit function returns a json with the content of the 'service_instance'
    if 'agents_list' in data:
        # using a predefined list of agents:
        return lifecycle_depl.submit_service_in_agents(service,
                                                       user_id,
                                                       service_instance_id,
                                                       sla_template_id,
                                                       data['agents_list'],
                                                       check_service=True)
    # OPTION B: submits the service with the help of the other mF2C components (landscaper, recommender ...)
    else:
        # using agent_decision module (landscaper, recommender...):
        return lifecycle_depl.submit(service,
                                     user_id,
                                     service_instance_id,
                                     sla_template_id)


####################################################################################################################


# postServiceInt: deploy a service instance in the device / agent
def postServiceInt(request):
    LOG.info("######## DEPLOYMENT (remote call) ##################################################################")
    data = request.get_json()
    # check input parameters
    if 'service' not in data or 'service_instance' not in data or 'agent' not in data:
        LOG.error('[lifecycle.app_funcs] [postServiceInt] Exception - parameter not found: service / service_instance / agent')
        return Response(json.dumps({'error': True, 'message': 'parameter not found: service / service_instance / agent'}),
                        status=406,
                        content_type='application/json')
    # deploy operation (for internal calls - between LMs -)
    return operations.deploy(data['service'], data['service_instance'], data['agent'])


# putServiceInt
def putServiceInt(request):
    LOG.info("######## OPERATION (remote call) ##################################################################")
    data = request.get_json()
    # check input parameters
    if 'service' not in data or 'operation' not in data or 'agent' not in data:
        LOG.error('[lifecycle.app_funcs] [putServiceInt] Exception - parameter not found: agent / operation')
        return Response(json.dumps({'error': True, 'message': 'parameter not found: agent / operation'}),
                        status=406,
                        content_type='application/json')
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
        LOG.error('[lifecycle.app_funcs] [putServiceInt] operation not defined / implemented')
        return Response(json.dumps({'error': True, 'message': 'operation not defined / implemented'}),
                        status=501,
                        content_type='application/json')
