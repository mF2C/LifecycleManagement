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
        LOG.debug("LIFECYCLE: MF2C: lifecycle_parent_deploy: response: " + str(r) + ", " + str(r.json()))

        if r.status_code >= 200 and r.status_code <= 204:
            return True

        LOG.error("LIFECYCLE: MF2C: lifecycle_parent_deploy: Error: status_code=" + str(r.status_code) + "; Returning None ...")
    except:
        LOG.exception("LIFECYCLE: MF2C: lifecycle_parent_deploy: Exception; Returning False ...")
    return False


# DEPLOY A SERVICE
# lifecycle_deploy: call to lifceycle from other agent in order to deploy a service
def lifecycle_deploy(service, agent):
    LOG.debug("LIFECYCLE: MF2C: lifecycle_deploy: deploy service in agent: " + str(service) + ", " + str(agent))
    try:
        LOG.info("LIFECYCLE: MF2C: lifecycle_deploy: HTTP POST: http://" + agent['url'] + ":" + str(config.dic['SERVER_PORT']) + "/api/v2/lm/service-instance-int")
        r = requests.post("http://" + agent['url'] + ":" + str(config.dic['SERVER_PORT']) + "/api/v2/lm/service-instance-int",
                          json={"service": service,
                                "agent": agent},
                          verify=config.dic['VERIFY_SSL'])
        LOG.debug("LIFECYCLE: MF2C: lifecycle_deploy: response: " + str(r) + ", " + str(r.json()))

        if r.status_code == 200:
            json_data = json.loads(r.text)
            agent = json_data['agent']
            LOG.debug("LIFECYCLE: MF2C: lifecycle_deploy: result: agent: " + str(agent))
            return ast.literal_eval(agent)

        LOG.error("LIFECYCLE: MF2C: lifecycle_deploy: Error: status_code=" + str(r.status_code) + "; Returning None ...")
    except:
        LOG.exception("LIFECYCLE: MF2C: lifecycle_deploy: Exception; Returning None ...")
    return None


# START / STOP SERVICE INSTANCE
# lifecycle_operation: call to lifceycle from other agent in order to start/stop... a service
def lifecycle_operation(service, agent, operation):
    LOG.debug("LIFECYCLE: MF2C: lifecycle_operation: " + str(service) + ", " + str(agent) + ", " + operation)
    try:
        LOG.info("LIFECYCLE: MF2C: lifecycle_operation: HTTP PUT: http://" + agent['url'] + ":" + str(config.dic['SERVER_PORT']) + "/api/v2/lm/service-instance-int")
        r = requests.put("http://" + agent['url'] + ":" + str(config.dic['SERVER_PORT']) + "/api/v2/lm/service-instance-int",
                         json={"service": service,
                               "operation": operation,
                               "agent": agent},
                         verify=config.dic['VERIFY_SSL'])
        LOG.debug("LIFECYCLE: MF2C: lifecycle_operation: response: " + str(r) + ", " + str(r.json()))

        if r.status_code == 200:
            json_data = json.loads(r.text)
            agent = json_data['agent']
            LOG.debug("LIFECYCLE: MF2C: lifecycle_operation: agent: " + str(agent))
            return ast.literal_eval(agent)

        LOG.error("LIFECYCLE: MF2C: lifecycle_operation: Error: status_code=" +  str(r.status_code) + "; Returning None ...")
    except:
        LOG.exception("LIFECYCLE: MF2C: lifecycle_operation: Exception; Returning None ...")
    return None


# lifecycle_um_info: call to lifceycle from other agent in order to get sharing model and user profile
def lifecycle_um_check_avialability(agent):
    LOG.debug("LIFECYCLE: MF2C: lifecycle_um_check_avialability: " + str(agent))
    try:
        LOG.info("LIFECYCLE: MF2C: lifecycle_um_check_avialability: HTTP GET: http://" + agent['url'] + ":" + str(config.dic['SERVER_PORT']) + "/api/v2/lm/check-agent-um")
        r = requests.get("http://" + agent['url'] + ":" + str(config.dic['SERVER_PORT']) + "/api/v2/lm/check-agent-um",
                         verify=config.dic['VERIFY_SSL'])
        LOG.debug("LIFECYCLE: MF2C: lifecycle_um_check_avialability: response: " + str(r) + ", " + str(r.json()))

        if r.status_code == 200:
            json_data = json.loads(r.text)
            LOG.debug("LIFECYCLE: MF2C: lifecycle_um_check_avialability: json_data=" + str(json_data))
            return json_data

        LOG.error("LIFECYCLE: MF2C: lifecycle_um_check_avialability: Error: status_code=" +  str(r.status_code) + "; Returning None ...")
    except:
        LOG.exception("LIFECYCLE: MF2C: lifecycle_um_check_avialability: Exception; Returning None ...")
    return None


###############################################################################
# USER MANAGEMENT
#   Calls to local User Management
###############################################################################


# SET UM INFORMATION
# set_lifecycle_um_properties: call to lifceycle from other agent in order to update user management properties
def user_management_set_um_properties(apps=0):
    LOG.debug("LIFECYCLE: MF2C: user_management_set_um_properties: localhost - local UM: Updating UM properties ...")
    try:
        LOG.info("LIFECYCLE: MF2C: user_management_set_um_properties: HTTP PUT: " + str(config.dic['URL_AC_USER_MANAGEMENT']) + "/user-profile")
        r = requests.put(str(config.dic['URL_AC_USER_MANAGEMENT']) + "/user-profile",
                         json={"apps_running": apps},
                         verify=config.dic['VERIFY_SSL'])
        LOG.debug("LIFECYCLE: MF2C: user_management_set_um_properties: response: " + str(r) + ", " + str(r.json()))

        if r.status_code == 200:
            json_data = json.loads(r.text)
            LOG.debug('LIFECYCLE: MF2C: user_management_set_um_properties: json_data=' + str(json_data))
            return json_data

        LOG.error("LIFECYCLE: MF2C: user_management_set_um_properties: Error: status_code=" + str(r.status_code) + "; Returning None ...")
    except:
        LOG.exception("LIFECYCLE: MF2C: user_management_set_um_properties: Exception; Returning None ...")
    return None


# CHECK AVIALABILITY
# user_management_check_avialability: call to local UM to check if it's possible to deploy a service
def user_management_check_avialability():
    LOG.debug("LIFECYCLE: MF2C: user_management_check_avialability: localhost - local UM: Checking avialability ...")
    try:
        LOG.info("LIFECYCLE: MF2C: user_management_check_avialability: HTTP GET: " + str(config.dic['URL_AC_USER_MANAGEMENT']) + "/check")
        r = requests.get(str(config.dic['URL_AC_USER_MANAGEMENT']) + "/check",
                         verify=config.dic['VERIFY_SSL'])
        LOG.debug("LIFECYCLE: MF2C: user_management_check_avialability: response: " + str(r) + ", " + str(r.json()))

        json_data = json.loads(r.text)
        LOG.debug("LIFECYCLE: MF2C: user_management_check_avialability: json_data=" + str(json_data))
        if r.status_code == 200 and not json_data['result'] is None:
            return json_data

        LOG.error("LIFECYCLE: MF2C: user_management_check_avialability: Error: status_code=" + str(r.status_code) + "; Returning None ...")
    except:
        LOG.exception("LIFECYCLE: MF2C: user_management_check_avialability: Exception; Returning None ...")
    return None


# GET CURRENT USER / DEVICE
# user_management_get_current: call to local UM to get current values (user, device)
def user_management_get_current(val):
    LOG.debug("LIFECYCLE: MF2C: user_management_get_current: Getting current " + val + " from localhost - UM: Checking avialability ...")
    try:
        LOG.info("LIFECYCLE: MF2C: user_management_get_current: HTTP GET: " + str(config.dic['URL_AC_USER_MANAGEMENT']) + "/current/" + val)
        r = requests.get(str(config.dic['URL_AC_USER_MANAGEMENT']) + "/current/" + val,
                         verify=config.dic['VERIFY_SSL'])
        LOG.debug("LIFECYCLE: MF2C: user_management_get_current: response: " + str(r) + ", " + str(r.json()))

        json_data = json.loads(r.text)
        LOG.debug("LIFECYCLE: MF2C: user_management_get_current: json_data=" + str(json_data))
        if r.status_code == 200 and not json_data['result'] is None:
            return json_data

        LOG.error("LIFECYCLE: MF2C: user_management_get_current: Error: status_code=" + str(r.status_code) + "; Returning None ...")
    except:
        LOG.exception("LIFECYCLE: MF2C: user_management_get_current: Exception; Returning None ...")
    return None


###############################################################################
# Interactions with other mF2C components:


# CALL TO LANDSCAPER & RECOMMENDER: get service's recipe / get available resources for a recipe
#   =>  POST 'http://localhost:46020/mf2c/optimal'
# 	    BODY: service json
def recommender_get_optimal_resources(service):
    LOG.debug("LIFECYCLE: MF2C: recommender_get_optimal_resources: service: " + str(service))
    try:
        LOG.info("LIFECYCLE: MF2C: recommender_get_optimal_resources: HTTP POST: " + str(config.dic['URL_PM_RECOM_LANDSCAPER']) + "/optimal")
        r = requests.post(str(config.dic['URL_PM_RECOM_LANDSCAPER']) + "/optimal",
                          json=service,
                          headers={"Accept": "text/json", "Content-Type": "application/json"},
                          verify=config.dic['VERIFY_SSL'],
                          timeout=config.dic['TIMEOUT_ANALYTICSENGINE'])
        LOG.debug("LIFECYCLE: MF2C: recommender_get_optimal_resources: response: " + str(r) + ", " + str(r.json()))

        if r.ok: # status_code == 200:
            # RESPONSE EXAMPLE
            # json_data:
            # [
            #  {'compute saturation': 0.0, 'network saturation': 0.0, 'memory saturation': 0.0, 'memory utilization': 0.0,
            #   'network utilization': 0.0, 'type': 'machine', 'disk saturation': 0.0, 'node_name': 'machine-A',
            #   'compute utilization': 0.0, 'disk utilization': 0.0},
            #  ...
            # ]
            # ==> [{"agent_ip": "192.168.252.41"}, {"agent_ip": "192.168.252.42"}]

            json_data = json.loads(r.text)
            LOG.debug("LIFECYCLE: MF2C: recommender_get_optimal_resources: json_data=" + str(json_data))

            # create list of agents
            list_of_agents = []
            for elem in json_data:
                list_of_agents.append({"agent_ip": elem['node_name']})

            LOG.debug("LIFECYCLE: MF2C: recommender_get_optimal_resources: list_of_agents=" + str(list_of_agents))
            return list_of_agents

        LOG.error("LIFECYCLE: MF2C: get_available_resources: Error: status_code=" +  str(r.status_code) + "; Returning None ...")
    except:
        LOG.exception("LIFECYCLE: MF2C: recommender_get_optimal_resources: Exception; Returning None ...")
    return None

###############################################################################


# create_sla_agreement: create SLA agreement
# curl -k -X POST -d @resources/samples/create-agreement.json https://localhost:8090/mf2c/create-agreement
# {"template_id":"t01","agreement_id":"9be511e8-347f-4a40-b784-e80789e4c65b","parameters":{"user":"a-user-id"}}
def create_sla_agreement(template_id, user_id, service):
    LOG.debug("LIFECYCLE: MF2C: create_sla_agreement: template_id=" + template_id + ", user_id=" + user_id + ", service=" + service['name'])
    try:
        LOG.info("LIFECYCLE: MF2C: create_sla_agreement: HTTP POST: " + str(config.dic['URL_PM_SLA_MANAGER']) + "/mf2c/create-agreement")
        body = {"template_id": template_id,
                "parameters": {"user":user_id}}
        r = requests.post(str(config.dic['URL_PM_SLA_MANAGER']) + "/mf2c/create-agreement",
                          json=body,
                          verify=config.dic['VERIFY_SSL'])
        LOG.debug("LIFECYCLE: MF2C: create_sla_agreement: response: " + str(r) + ", " + str(r.json()))

        if r.status_code >= 200 and r.status_code <= 204:
            json_data = json.loads(r.text)
            LOG.debug("LIFECYCLE: MF2C: create_sla_agreement: json_data=" + str(json_data))
            return json_data['agreement_id']

        LOG.error("LIFECYCLE: MF2C: create_sla_agreement: Error: status_code=" +  str(r.status_code) + "; Returning None ...")
    except:
        LOG.exception("LIFECYCLE: MF2C: create_sla_agreement: Exception; Returning None ...")
    return None


# start_sla_agreement: start SLA agreement
# PUT /agreements/<id>/start   (stop)
def sla_start_agreement(agreement_id):
    agreement_id = agreement_id.replace('agreement/', '')
    LOG.debug("LIFECYCLE: MF2C: start_sla_agreement: agreement_id: " + agreement_id)
    try:
        LOG.info("LIFECYCLE: MF2C: start_sla_agreement: HTTP PUT: " + str(config.dic['URL_PM_SLA_MANAGER']) + "/agreements/" + agreement_id + "/start")
        r = requests.put(str(config.dic['URL_PM_SLA_MANAGER']) + "/agreements/" + agreement_id + "/start",
                         verify=config.dic['VERIFY_SSL'])
        LOG.debug("LIFECYCLE: MF2C: start_sla_agreement: response: " + str(r) + ", " + str(r.json()))

        if r.status_code >= 200 and r.status_code <= 204:
            return True

        LOG.error("LIFECYCLE: MF2C: start_sla_agreement: Error: status_code=" +  str(r.status_code) + "; Returning False ...")
    except:
        LOG.exception("LIFECYCLE: MF2C: start_sla_agreement: Exception; Returning False ...")
    return False


# PUT /agreements/<id>/stop
def sla_stop_agreement(agreement_id):
    agreement_id = agreement_id.replace('agreement/', '')
    LOG.debug("LIFECYCLE: MF2C: stop_sla_agreement: agreement_id: " + agreement_id)
    try:
        LOG.info("LIFECYCLE: MF2C: start_sla_agreement: HTTP PUT: " + str(config.dic['URL_PM_SLA_MANAGER']) + "/agreements/" + agreement_id + "/stop")
        r = requests.put(str(config.dic['URL_PM_SLA_MANAGER']) + "/agreements/" + agreement_id + "/stop",
                         verify=config.dic['VERIFY_SSL'])
        LOG.debug("LIFECYCLE: MF2C: stop_sla_agreement: response: " + str(r) + ", " + str(r.json()))

        if r.status_code >= 200 and r.status_code <= 204:
            return True

        LOG.error("LIFECYCLE: MF2C: stop_sla_agreement: Error: status_code=" +  str(r.status_code) + "; Returning False ...")
    except:
        LOG.exception("LIFECYCLE: MF2C: stop_sla_agreement: Exception; Returning False ...")
    return False


# PUT /agreements/<id>/stop
# TODO
def sla_terminate_agreement(agreement_id):
    agreement_id = agreement_id.replace('agreement/', '')
    LOG.debug("LIFECYCLE: MF2C: sla_terminate_agreement: agreement_id: " + agreement_id)
    try:
        LOG.info("LIFECYCLE: MF2C: sla_terminate_agreement: HTTP PUT: " + str(config.dic['URL_PM_SLA_MANAGER']) + "/agreements/" + agreement_id + "/stop")
        r = requests.put(str(config.dic['URL_PM_SLA_MANAGER']) + "/agreements/" + agreement_id + "/stop",
                         verify=config.dic['VERIFY_SSL'])
        LOG.debug("LIFECYCLE: MF2C: sla_terminate_agreement: response: " + str(r) + ", " + str(r.json()))

        if r.status_code >= 200 and r.status_code <= 204:
            return True

        LOG.error("LIFECYCLE: MF2C: sla_terminate_agreement: Error: status_code=" +  str(r.status_code) + "; Returning False ...")
    except:
        LOG.exception("LIFECYCLE: MF2C: sla_terminate_agreement: Exception; Returning False ...")
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

        LOG.info("LIFECYCLE: MF2C: service_management_qos: HTTP GET: " + str(config.dic['URL_AC_SERVICE_MNGMT']) + "/" + id)
        r = requests.get(str(config.dic['URL_AC_SERVICE_MNGMT']) + "/" + id,
                         verify=config.dic['VERIFY_SSL'])
        LOG.debug("LIFECYCLE: MF2C: service_management_qos: response: " + str(r) + ", " + str(r.json()))

        json_data = json.loads(r.text)
        LOG.debug("LIFECYCLE: MF2C: service_management_qos: json_data=" + str(json_data) + ", status=" + str(json_data['status']))

        if json_data['status'] == 200:
            return json_data["service-instance"]

        LOG.error("LIFECYCLE: MF2C: service_management_qos: Error: status: " + str(json_data['status']) + "; Returning None ...")
    except:
        LOG.exception("LIFECYCLE: MF2C: service_management_qos: Exception; Returning None ...")
    return None
