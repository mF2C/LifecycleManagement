"""
Interactions with other mF2C components
This is being developed for the MF2C Project: http://www.mf2c-project.eu/

Copyright: Roi Sucasas Font, Atos Research and Innovation, 2017.

This code is licensed under an Apache 2.0 license. Please, refer to the LICENSE.TXT file for more information

Created on 09 feb. 2018

@author: Roi Sucasas - ATOS
"""

import requests
import json, ast
import config
from common.logs import LOG


###############################################################################
# LIFECYCLE interactions
# lifecycle_deploy: call to parent's lifceycle; forwards a "submit service" request
def lifecycle_parent_deploy(parent, service_id, user_id, agreement_id):
    LOG.debug("LIFECYCLE: MF2C: lifecycle_parent_deploy: forward request to parent: " + str(parent) + ", service_id: " + str(service_id) +
              ", user_id: " + str(user_id) + ", agreement_id: " + agreement_id)
    try:
        LOG.info("LIFECYCLE: MF2C: lifecycle_parent_deploy: HTTP POST: http://" + parent['url'] + ":" + str(config.dic['SERVER_PORT']) + "/api/v2/lm/service")
        r = requests.post("http://" + parent['url'] + ":" + str(config.dic['SERVER_PORT']) + "/api/v2/lm/service",
                          json={"service_id": service_id, "user_id": user_id, "agreement_id": agreement_id},
                          verify=config.dic['VERIFY_SSL'])
        LOG.debug("LIFECYCLE: MF2C: lifecycle_parent_deploy: response: " + str(r))

        if r.status_code >= 200 and r.status_code <= 204:
            LOG.debug('LIFECYCLE: MF2C: lifecycle_parent_deploy: status_code=' +  str(r.status_code))
            return True

        LOG.error('LIFECYCLE: MF2C: lifecycle_parent_deploy: Error: status_code=' + str(r.status_code))
        return False
    except:
        LOG.error('LIFECYCLE: MF2C: lifecycle_parent_deploy: Exception')
        return False


# lifecycle_get_agent_info: get type of agent: docker, docker-swarm, ...
def lifecycle_get_agent_info(agent):
    LOG.debug("LIFECYCLE: MF2C: lifecycle_get_agent_info: agent: " + str(agent))
    try:
        LOG.info("LIFECYCLE: MF2C: lifecycle_get_agent_info: HTTP GET: http://" + agent['url'] + ":" + str(config.dic['SERVER_PORT']) + "/api/v2/lm/agent-info")
        r = requests.get("http://" + agent['url'] + ":" + str(config.dic['SERVER_PORT']) + "/api/v2/lm/agent-info",
                          verify=config.dic['VERIFY_SSL'])
        LOG.debug("LIFECYCLE: MF2C: lifecycle_get_agent_info: response: " + str(r))

        json_data = json.loads(r.text)

        if r.status_code == 200:
            LOG.debug('LIFECYCLE: MF2C: lifecycle_get_agent_info: status_code=' + str(r.status_code) + '; response: ' + str(json_data))
            return json_data

        LOG.error('LIFECYCLE: MF2C: lifecycle_get_agent_info: Error: status_code=' + str(r.status_code))
        return None
    except:
        LOG.error('LIFECYCLE: MF2C: lifecycle_parent_deploy: Exception')
        return None


# lifecycle_deploy: call to lifceycle from other agent in order to deploy a service
def lifecycle_deploy(service, agent):
    LOG.debug("LIFECYCLE: MF2C: lifecycle_deploy: deploy service in agent: " + str(service) + ", " + str(agent))
    try:
        LOG.info("LIFECYCLE: MF2C: lifecycle_deploy: HTTP POST: http://" + agent['url'] + ":" + str(config.dic['SERVER_PORT']) + "/api/v2/lm/service-instance-int")
        r = requests.post("http://" + agent['url'] + ":" + str(config.dic['SERVER_PORT']) + "/api/v2/lm/service-instance-int",
                          json={"service": service, "agent": agent},
                          verify=config.dic['VERIFY_SSL'])
        LOG.debug("LIFECYCLE: MF2C: lifecycle_deploy: response: " + str(r))

        json_data = json.loads(r.text)
        agent = json_data['agent']
        LOG.debug("LIFECYCLE: MF2C: lifecycle_deploy: agent: " + str(agent))

        if r.status_code == 200:
            LOG.debug('LIFECYCLE: MF2C: lifecycle_deploy: status_code=' + str(r.status_code) + '; response: ' + str(json_data))
            return ast.literal_eval(agent)

        LOG.error('LIFECYCLE: MF2C: lifecycle_deploy: Error: status_code=' + str(r.status_code))
        return None
    except:
        LOG.error('LIFECYCLE: MF2C: lifecycle_deploy: Exception')
        return None


# lifecycle_operation: call to lifceycle from other agent in order to start/stop... a service
def lifecycle_operation(agent, operation):
    LOG.debug("LIFECYCLE: MF2C: lifecycle_operation: " + str(agent) + ", " + operation)
    try:
        LOG.info("LIFECYCLE: MF2C: lifecycle_operation: HTTP PUT: http://" + agent['url'] + ":" + str(config.dic['SERVER_PORT']) + "/api/v2/lm/service-instance-int")
        r = requests.put("http://" + agent['url'] + ":" + str(config.dic['SERVER_PORT']) + "/api/v2/lm/service-instance-int",
                         json={"operation": operation, "agent": agent},
                         verify=config.dic['VERIFY_SSL'])
        LOG.debug("LIFECYCLE: MF2C: lifecycle_operation: response:" + str(r))

        json_data = json.loads(r.text)
        agent = json_data['agent']
        LOG.debug("LIFECYCLE: MF2C: lifecycle_operation: agent: " + str(agent))

        if r.status_code == 200:
            LOG.debug('LIFECYCLE: MF2C: lifecycle_operation: status_code=' +  str(r.status_code) + '; response: ' + str(json_data))
            return ast.literal_eval(agent)

        LOG.error('LIFECYCLE: MF2C: lifecycle_operation: Error: status_code=' +  str(r.status_code))
        return None
    except:
        LOG.error('LIFECYCLE: MF2C: lifecycle_operation: Exception')
        return None


###############################################################################
# Interactions with other mF2C components:

# CALL TO LANDSCAPER & RECOMMENDER: get service's recipe / get available resources for a recipe
#   =>  POST http://192.168.252.41:46020/mf2c/optimal
# 	    BODY: service json
def recommender_get_optimal_resources(service):
    LOG.debug("LIFECYCLE: MF2C: get_available_resources: service: " + str(service))
    LOG.info("LIFECYCLE: MF2C: get_available_resources: HTTP POST: " + str(config.dic['URL_PM_RECOM_LANDSCAPER']) + "/optimal")
    try:
        # 'http://localhost:46020/mf2c/optimal'
        r = requests.post(str(config.dic['URL_PM_RECOM_LANDSCAPER']) + "/optimal",
                          json=service,
                          headers={"Accept": "text/json", "Content-Type": "application/json"},
                          verify=config.dic['VERIFY_SSL'],
                          timeout=config.dic['TIMEOUT_ANALYTICSENGINE'])
        LOG.debug("LIFECYCLE: MF2C: get_available_resources: response: " + str(r))

        json_data = json.loads(r.text)
        LOG.debug("LIFECYCLE: MF2C: get_available_resources: json_data: " + str(json_data))

        # EXAMPLE
        # json_data:
        # [
        #  {'compute saturation': 0.0, 'network saturation': 0.0, 'memory saturation': 0.0, 'memory utilization': 0.0,
        #   'network utilization': 0.0, 'type': 'machine', 'disk saturation': 0.0, 'node_name': 'machine-A',
        #   'compute utilization': 0.0, 'disk utilization': 0.0},
        #  {'compute saturation': 0.0, 'network saturation': 0.0, 'memory saturation': 0.0, 'memory utilization': 0.0,
        #   'network utilization': 0.0, 'type': 'machine', 'disk saturation': 0.0, 'node_name': 'machine-B',
        #   'compute utilization': 0.0, 'disk utilization': 0.0},
        #  {'compute saturation': 0.0, 'network saturation': 0.0, 'memory saturation': 0.0, 'memory utilization': 0.0,
        #   'network utilization': 0.0, 'type': 'machine', 'disk saturation': 0.0, 'node_name': '192.168.252.41',
        #   'compute utilization': 0.0, 'disk utilization': 0.0},
        #  {'compute saturation': 0.0, 'network saturation': 0.0, 'memory saturation': 0.0, 'memory utilization': 0.0,
        #   'network utilization': 0.0, 'type': 'machine', 'disk saturation': 0.0, 'node_name': 'tango-docker',
        #   'compute utilization': 0.0, 'disk utilization': 0.0}
        # ]
        # ==> [{"agent_ip": "192.168.252.41"}, {"agent_ip": "192.168.252.42"}]

        if r.ok: #status_code == 200:
            LOG.debug('LIFECYCLE: MF2C: get_available_resources: status_code=' +  str(r.ok)) #r.status_code))

            # create list of agents
            list_of_agents = []
            for elem in json_data:
                list_of_agents.append({"agent_ip": elem['node_name']})

            LOG.debug("LIFECYCLE: MF2C: get_available_resources: list_of_agents:" + str(list_of_agents))
            return list_of_agents

        LOG.error('LIFECYCLE: MF2C: get_available_resources: Error: status_code=' +  str(r.status_code))
        return None
    except:
        LOG.error('LIFECYCLE: MF2C: get_available_resources: Exception')
        return None

###############################################################################

# start_sla_agreement: start SLA agreement
# PUT /agreements/<id>/start   (stop)
def sla_start_agreement(agreement_id):
    agreement_id = agreement_id.replace('agreement/', '')
    LOG.debug("LIFECYCLE: MF2C: start_sla_agreement: agreement_id: " + agreement_id)
    LOG.info("LIFECYCLE: MF2C: start_sla_agreement: HTTP PUT: " + str(config.dic['URL_PM_SLA_MANAGER']) + "/agreements/" + agreement_id + "/start")
    try:
        r = requests.put(str(config.dic['URL_PM_SLA_MANAGER']) + "/agreements/" + agreement_id + "/start",
                         verify=config.dic['VERIFY_SSL'])
        LOG.debug("LIFECYCLE: MF2C: start_sla_agreement: response: " + str(r))

        if r.status_code >= 200 and r.status_code <= 204:
            LOG.debug('LIFECYCLE: MF2C: start_sla_agreement: status_code=' +  str(r.status_code))
            return True

        LOG.error('LIFECYCLE: MF2C: start_sla_agreement: Error: status_code=' +  str(r.status_code))
        return False
    except:
        LOG.error('LIFECYCLE: MF2C: start_sla_agreement: Exception')
        return False


# PUT /agreements/<id>/stop
def sla_stop_agreement(agreement_id):
    agreement_id = agreement_id.replace('agreement/', '')
    LOG.debug("LIFECYCLE: MF2C: stop_sla_agreement: agreement_id: " + agreement_id)
    LOG.info("LIFECYCLE: MF2C: start_sla_agreement: HTTP PUT: " + str(config.dic['URL_PM_SLA_MANAGER']) + "/agreements/" + agreement_id + "/stop")
    try:
        r = requests.put(str(config.dic['URL_PM_SLA_MANAGER']) + "/agreements/" + agreement_id + "/stop",
                         verify=config.dic['VERIFY_SSL'])
        LOG.debug("LIFECYCLE: MF2C: stop_sla_agreement: response: " + str(r))

        if r.status_code == 200 or r.status_code == 201 or r.status_code == 202 or r.status_code == 204:
            LOG.debug('LIFECYCLE: MF2C: stop_sla_agreement: status_code=' +  str(r.status_code))
            return True

        LOG.error('LIFECYCLE: MF2C: stop_sla_agreement: Error: status_code=' +  str(r.status_code))
        return False
    except:
        LOG.error('LIFECYCLE: MF2C: stop_sla_agreement: Exception')
        return False


# PUT /agreements/<id>/stop
# TODO
def sla_terminate_agreement(agreement_id):
    agreement_id = agreement_id.replace('agreement/', '')
    LOG.debug("LIFECYCLE: MF2C: stop_sla_agreement: agreement_id: " + agreement_id)
    LOG.info("LIFECYCLE: MF2C: start_sla_agreement: HTTP PUT: " + str(config.dic['URL_PM_SLA_MANAGER']) + "/agreements/" + agreement_id + "/stop")
    try:
        r = requests.put(str(config.dic['URL_PM_SLA_MANAGER']) + "/agreements/" + agreement_id + "/stop",
                         verify=config.dic['VERIFY_SSL'])
        LOG.debug("LIFECYCLE: MF2C: stop_sla_agreement: response: " + str(r))

        if r.status_code == 200 or r.status_code == 201 or r.status_code == 202 or r.status_code == 204:
            LOG.debug('LIFECYCLE: MF2C: stop_sla_agreement: status_code=' +  str(r.status_code))
            return True

        LOG.error('LIFECYCLE: MF2C: stop_sla_agreement: Error: status_code=' +  str(r.status_code))
        return False
    except:
        LOG.error('LIFECYCLE: MF2C: stop_sla_agreement: Exception')
        return False

###############################################################################

# CALL TO QoS PROVIDING
# service_management_qos: Returns which agents can be used to execute a specific service
# GET /qos/<id>
#   where <id>: id of the service instance
# ==> Returns a copy of the service instance specifying the agents that can be used to execute that service
def service_management_qos(service_instance):
    try:
        id = service_instance['id']
        LOG.debug("LIFECYCLE: MF2C: service_management_qos: service_instance_id: " + id)
        LOG.info("LIFECYCLE: MF2C: service_management_qos: HTTP GET: " + str(config.dic['URL_AC_SERVICE_MNGMT']) + "/qos/" + id)

        #r = requests.get(str(config.dic['URL_AC_SERVICE_MNGMT']) + "/qos/" + id, verify=config.dic['VERIFY_SSL'])
        r = requests.get(str(config.dic['URL_AC_SERVICE_MNGMT']) + "/" + id, verify=config.dic['VERIFY_SSL'])
        LOG.debug("LIFECYCLE: MF2C: service_management_qos: response: " + str(r))

        json_data = json.loads(r.text)
        LOG.debug("LIFECYCLE: MF2C: service_management_qos: " + str(json_data) + ", status: " + str(json_data['status']))

        if json_data['status'] == 200:
            LOG.debug("LIFECYCLE: MF2C: service_management_qos: status=" + str(json_data['status']) + ", service: " + str(json_data["service-instance"]))
            return json_data["service-instance"]

        LOG.error("LIFECYCLE: MF2C: service_management_qos: Error: status: " + str(json_data['status']))
        return None
    except:
        LOG.error('LIFECYCLE: MF2C: service_management_qos: Exception')
        return None

'''
# service_management_get_service:
def service_management_get_service(service_id):
    try:
        if service_id.find("service") < 0:
            service_id = "service/" + service_id

        LOG.debug("LIFECYCLE: MF2C: service_management_get_service: " + service_id)
        LOG.info("LIFECYCLE: MF2C: service_management_get_service: HTTP GET: " + str(config.dic['URL_AC_SERVICE_MNGMT']) + "/categorizer/" + service_id)

        r = requests.get(str(config.dic['URL_AC_SERVICE_MNGMT']) + "/categorizer/" + service_id,
                         verify=config.dic['VERIFY_SSL'])
        LOG.debug("LIFECYCLE: MF2C: service_management_get_service: response: " + str(r))

        json_data = json.loads(r.text)
        LOG.debug("LIFECYCLE: MF2C: service_management_get_service: " + str(json_data) + ", status: " + str(json_data['status']))

        if r.status_code == 200 and json_data['status'] == 404:
            LOG.error("LIFECYCLE: MF2C: service_management_get_service: status_code=" + str(r.status_code) + ", status: " + str(json_data['status']))
            return None
        elif r.status_code == 200:
            LOG.debug("LIFECYCLE: MF2C: service_management_get_service: status_code=" + str(r.status_code) + ", service: " + str(json_data["service"]))
            return json_data["service"]

        LOG.error('LIFECYCLE: MF2C: service_management_get_service: Error: status_code=' + str(r.status_code))
        return None
    except:
        LOG.error('LIFECYCLE: MF2C: service_management_get_service: Exception')
        return None
'''
###############################################################################

# CALL TO User Management (Profiling)
def user_management_profiling(user_id, remote=None):
    try:
        LOG.debug("LIFECYCLE: MF2C: user_management_profiling: user_id: " + user_id)

        if remote is None:
            LOG.info("LIFECYCLE: MF2C: user_management_profiling: HTTP GET: " + str(config.dic['URL_AC_USER_MANAGEMENT']) + "/profiling/" + user_id)
            r = requests.get(str(config.dic['URL_AC_USER_MANAGEMENT']) + "/profiling/" + user_id,
                             verify=config.dic['VERIFY_SSL'])
        else:
            LOG.info("LIFECYCLE: MF2C: user_management_profiling: HTTP GET: http://" + remote + ":46300/api/v2/um/profiling/" + user_id)
            r = requests.get("http://" + remote + ":46300/api/v2/um/profiling/" + user_id,
                             verify=config.dic['VERIFY_SSL'])
        json_data = json.loads(r.text)
        LOG.debug("LIFECYCLE: MF2C: user_management_profiling: response: " + str(r) + ", json_data: " + str(json_data))

        if r.status_code == 200:
            LOG.debug('LIFECYCLE: MF2C: user_management_profiling: status_code=' + str(r.status_code))
            return json_data

        LOG.error('LIFECYCLE: MF2C: user_management_profiling: Error: status_code=' + str(r.status_code))
        return None
    except:
        LOG.error('LIFECYCLE: MF2C: user_management_profiling: Exception')
        return None


# CALL TO User Management (Sharing Model)
def user_management_sharing_model(user_id, remote=None):
    try:
        LOG.debug("LIFECYCLE: MF2C: user_management_sharing_model: user_id: " + user_id)

        if remote is None:
            LOG.info("LIFECYCLE: MF2C: user_management_sharing_model: HTTP GET: " + str(config.dic['URL_AC_USER_MANAGEMENT']) + "/sharingmodel/" + user_id)
            r = requests.get(str(config.dic['URL_AC_USER_MANAGEMENT']) + "/sharingmodel/" + user_id,
                             verify=config.dic['VERIFY_SSL'])
        else:
            LOG.info("LIFECYCLE: MF2C: user_management_sharing_model: HTTP GET: http://" + remote + ":46300/api/v2/um/sharingmodel/" + user_id)
            r = requests.get("http://" + remote + ":46300/api/v2/um/sharingmodel/" + user_id,
                             verify=config.dic['VERIFY_SSL'])
        json_data = json.loads(r.text)
        LOG.debug("LIFECYCLE: MF2C: user_management_sharing_model: response: " + str(r) + ", json_data: " + str(json_data))

        if r.status_code == 200:
            LOG.debug('LIFECYCLE: MF2C: user_management_sharing_model: status_code=' + str(r.status_code))
            return json_data

        LOG.error('LIFECYCLE: MF2C: user_management_sharing_model: Error: status_code=' + str(r.status_code))
        return None
    except:
        LOG.error('LIFECYCLE: MF2C: user_management_sharing_model: Exception')
        return None

