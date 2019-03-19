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
# LIFECYCLE
#   Calls to other agents' Lifecycle Managers
###############################################################################


# FORWARD REQUEST TO LEADER
# lifecycle_deploy: call to parent's lifceycle; forwards a "submit service" request
def lifecycle_parent_deploy(leader_ip, service_id, user_id, agreement_id, service_instance_id):
    LOG.debug("LIFECYCLE: MF2C: lifecycle_parent_deploy: forward request to leader: " + leader_ip + ", service_id: " + str(service_id) +
              ", user_id: " + str(user_id) + ", agreement_id: " + agreement_id + ", service_instance_id: " + service_instance_id)
    try:
        LOG.info("LIFECYCLE: MF2C: lifecycle_parent_deploy: HTTP POST: http://" + leader_ip + ":" + str(config.dic['SERVER_PORT']) + "/api/v2/lm/service")
        r = requests.post("http://" + leader_ip + ":" + str(config.dic['SERVER_PORT']) + "/api/v2/lm/service",
                          json={"service_id": service_id,
                                "user_id": user_id,
                                "agreement_id": agreement_id,
                                "service_instance_id": service_instance_id},
                          verify=config.dic['VERIFY_SSL'])
        LOG.debug("LIFECYCLE: MF2C: lifecycle_parent_deploy: response: " + str(r))

        if r.status_code >= 200 and r.status_code <= 204:
            LOG.debug('LIFECYCLE: MF2C: lifecycle_parent_deploy: status_code=' +  str(r.status_code))
            return True

        LOG.error('LIFECYCLE: MF2C: lifecycle_parent_deploy: Error: status_code=' + str(r.status_code))
        return False
    except:
        LOG.exception('LIFECYCLE: MF2C: lifecycle_parent_deploy: Exception')
        return False


# DEPLOY A SERVICE
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
        LOG.exception('LIFECYCLE: MF2C: lifecycle_deploy: Exception')
        return None


# START / STOP SERVICE INSTANCE
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
        LOG.exception('LIFECYCLE: MF2C: lifecycle_operation: Exception')
        return None


# GET UM INFORMATION
# lifecycle_um_info: call to lifceycle from other agent in order to get sharing model and user profile
def lifecycle_um_info(agent):
    LOG.debug("LIFECYCLE: MF2C: lifecycle_um_info: " + str(agent))
    try:
        LOG.info("LIFECYCLE: MF2C: lifecycle_um_info: HTTP GET: http://" + agent['url'] + ":" + str(config.dic['SERVER_PORT']) + "/api/v2/lm/agent-um")
        r = requests.get("http://" + agent['url'] + ":" + str(config.dic['SERVER_PORT']) + "/api/v2/lm/agent-um",
                         verify=config.dic['VERIFY_SSL'])
        LOG.debug("LIFECYCLE: MF2C: lifecycle_um_info: response:" + str(r))

        json_data = json.loads(r.text)
        agent_um = json_data['agent_um']
        LOG.debug("LIFECYCLE: MF2C: lifecycle_um_info: agent_um: " + str(agent_um))

        if r.status_code == 200:
            LOG.debug('LIFECYCLE: MF2C: lifecycle_um_info: status_code=' +  str(r.status_code) + '; response: ' + str(json_data))
            return ast.literal_eval(agent_um)

        LOG.error('LIFECYCLE: MF2C: lifecycle_um_info: Error: status_code=' +  str(r.status_code))
        return None
    except:
        LOG.exception('LIFECYCLE: MF2C: lifecycle_um_info: Exception')
        return None


###############################################################################
# USER MANAGEMENT
#   Calls to local User Management
###############################################################################


# SET UM INFORMATION
# set_lifecycle_um_properties: call to lifceycle from other agent in order to update user management properties
def user_management_set_um_properties(apps=0):
    LOG.debug("LIFECYCLE: MF2C: user_management_set_um_properties: localhost - local UM ")
    try:
        LOG.debug("LIFECYCLE: MF2C: user_management_set_um_properties: Updating UM properties ...")
        LOG.info("LIFECYCLE: MF2C: user_management_set_um_properties: HTTP PUT: " + str(config.dic['URL_AC_USER_MANAGEMENT']) + "/user-profile")
        r = requests.put(str(config.dic['URL_AC_USER_MANAGEMENT']) + "/user-profile",
                         json={"apps_running": apps},
                         verify=config.dic['VERIFY_SSL'])

        json_data = json.loads(r.text)
        LOG.debug("LIFECYCLE: MF2C: user_management_set_um_properties: response: " + str(r) + ", json_data: " + str(json_data))

        if r.status_code == 200:
            LOG.debug('LIFECYCLE: MF2C: user_management_set_um_properties: status_code=' + str(r.status_code))
            return json_data

        LOG.error('LIFECYCLE: MF2C: user_management_set_um_properties: Error: status_code=' + str(r.status_code))
    except:
        LOG.exception('LIFECYCLE: MF2C: user_management_set_um_properties: Exception')
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
        LOG.exception('LIFECYCLE: MF2C: get_available_resources: Exception')
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
        LOG.exception('LIFECYCLE: MF2C: start_sla_agreement: Exception')
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
        LOG.exception('LIFECYCLE: MF2C: stop_sla_agreement: Exception')
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
        LOG.exception('LIFECYCLE: MF2C: stop_sla_agreement: Exception')
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
        id_service = service_instance['service']
        LOG.debug("LIFECYCLE: MF2C: service_management_qos: service: " + id_service + " service_instance_id: " + id)
        LOG.debug("LIFECYCLE: MF2C: service_management_qos: HTTP GET: " + str(config.dic['URL_AC_SERVICE_MNGMT']) + "/" + id)

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
        LOG.exception('LIFECYCLE: MF2C: service_management_qos: Exception')
        return None
