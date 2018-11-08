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
# lifecycle_deploy: call to lifceycle from other agent in order to deploy a service
def lifecycle_deploy(service, agent):
    LOG.debug("Lifecycle-Management: MF2C: lifecycle_deploy: " + str(service) + ", " + str(agent))
    try:
        LOG.info("Lifecycle-Management: MF2C: lifecycle_deploy: HTTP POST: " +
                 "https://" + agent['url'] + ":" + str(config.dic['SERVER_PORT']) + "/api/v1/lifecycle/service-instance-operations")
        r = requests.post("https://" + agent['url'] + ":" + str(config.dic['SERVER_PORT']) + "/api/v1/lifecycle/service-instance-operations",
                          json={"service": service,
                                "agent": agent},
                          verify=config.dic['VERIFY_SSL'])
        LOG.debug("Lifecycle-Management: MF2C: lifecycle_operation: r:" + str(r))
        json_data = json.loads(r.text)
        agent = json_data['agent']
        LOG.debug("Lifecycle-Management: MF2C: lifecycle_deploy:" + str(agent))

        if r.status_code == 200:
            LOG.debug('Lifecycle-Management: MF2C: lifecycle_deploy: status_code=' + str(r.status_code) + '; response: ' + str(json_data))
            return ast.literal_eval(agent)

        LOG.error('Lifecycle-Management: MF2C: lifecycle_deploy: Error: status_code=' + str(r.status_code))
        return None
    except:
        LOG.error('Lifecycle-Management: MF2C: lifecycle_deploy: Exception')
        return None


# lifecycle_operation: call to lifceycle from other agent in order to start/stop... a service
def lifecycle_operation(agent, operation):
    LOG.debug("Lifecycle-Management: MF2C: lifecycle_operation: " + str(agent) + ", " + operation)
    try:
        LOG.info("Lifecycle-Management: MF2C: lifecycle_operation: HTTP PUT: " +
                 "https://" + agent['url'] + ":" + str(config.dic['SERVER_PORT']) + "/api/v1/lifecycle/service-instance-operations")
        r = requests.put("https://" + agent['url'] + ":" + str(config.dic['SERVER_PORT']) + "/api/v1/lifecycle/service-instance-operations",
                         json={"operation": operation,
                               "agent": agent},
                         verify=config.dic['VERIFY_SSL'])
        LOG.debug("Lifecycle-Management: MF2C: lifecycle_operation: r:" + str(r))
        json_data = json.loads(r.text)
        agent = json_data['agent']
        LOG.debug("Lifecycle-Management: MF2C: lifecycle_operation:" + str(agent))

        if r.status_code == 200:
            LOG.debug('Lifecycle-Management: MF2C: lifecycle_operation: status_code=' +  str(r.status_code) + '; response: ' + str(json_data))
            return ast.literal_eval(agent)

        LOG.error('Lifecycle-Management: MF2C: lifecycle_operation: Error: status_code=' +  str(r.status_code))
        return None
    except:
        LOG.error('Lifecycle-Management: MF2C: lifecycle_operation: Exception')
        return None


###############################################################################
# Interactions with other mF2C components
# CALL TO LANDSCAPER & RECOMMENDER: get service's recipe / get available resources for a recipe
#   =>  POST http://192.168.252.41:46020/mf2c/optimal
# 	    BODY: service json
def get_optimal_resources(service):
    LOG.debug("Lifecycle-Management: MF2C: get_available_resources: service: " + str(service))
    LOG.info("Lifecycle-Management: MF2C: get_available_resources: HTTP POST: " +
             str(config.dic['URL_PM_RECOM_LANDSCAPER']) + "/optimal")
    try:
        # url = 'http://localhost:46020/mf2c/optimal'
        # res = requests.post(url, json=json_recipe, headers=headers)
        # if res.ok:
        #     print
        #     'Optimal Done'
        #     json_data = json.loads(res.text)
        #     print
        #     json_data

        r = requests.post(str(config.dic['URL_PM_RECOM_LANDSCAPER']) + "/optimal",
                          json=service,
                          headers={"Accept": "text/json",
                                   "Content-Type": "application/json"},
                          verify=config.dic['VERIFY_SSL'],
                          timeout=config.dic['TIMEOUT_ANALYTICSENGINE'])

        LOG.debug("Lifecycle-Management: MF2C: get_available_resources: r:" + str(r))
        json_data = json.loads(r.text)
        LOG.debug("Lifecycle-Management: MF2C: get_available_resources: json_data:" + str(json_data))

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
            LOG.debug('Lifecycle-Management: MF2C: get_available_resources: status_code=' +  str(r.ok)) #r.status_code))

            # create list of agents
            list_of_agents = []
            for elem in json_data:
                list_of_agents.append({"agent_ip": elem['node_name']})

            LOG.debug("Lifecycle-Management: MF2C: get_available_resources: list_of_agents:" + str(list_of_agents))
            return list_of_agents

        LOG.error('Lifecycle-Management: MF2C: get_available_resources: Error: status_code=' +  str(r.status_code))
        return None
    except:
        LOG.error('Lifecycle-Management: MF2C: get_available_resources: Exception')
        return None


# CALL TO SLA MANAGEMENT
# start_sla_agreement: start SLA agreement
# PUT /agreements/<id>/start   (stop)
def start_sla_agreement(agreement_id):
    agreement_id = agreement_id.replace('agreement/', '')
    LOG.debug("Lifecycle-Management: MF2C: start_sla_agreement: agreement_id: " + agreement_id)
    LOG.info("Lifecycle-Management: MF2C: start_sla_agreement: HTTP PUT: " +
             str(config.dic['URL_PM_SLA_MANAGER']) + "/agreements/" + agreement_id + "/start")
    try:
        r = requests.put(str(config.dic['URL_PM_SLA_MANAGER']) + "/agreements/" + agreement_id + "/start",
                         verify=config.dic['VERIFY_SSL'])

        LOG.debug("Lifecycle-Management: MF2C: start_sla_agreement:" + str(r))

        if r.status_code >= 200 and r.status_code <= 204:
            LOG.debug('Lifecycle-Management: MF2C: start_sla_agreement: status_code=' +  str(r.status_code))
            return True

        LOG.error('Lifecycle-Management: MF2C: start_sla_agreement: Error: status_code=' +  str(r.status_code))
        return False
    except:
        LOG.error('Lifecycle-Management: MF2C: start_sla_agreement: Exception')
        return False


# PUT /agreements/<id>/stop
def stop_sla_agreement(agreement_id):
    agreement_id = agreement_id.replace('agreement/', '')
    LOG.debug("Lifecycle-Management: MF2C: stop_sla_agreement: agreement_id: " + agreement_id)
    LOG.info("Lifecycle-Management: MF2C: start_sla_agreement: HTTP PUT: " +
             str(config.dic['URL_PM_SLA_MANAGER']) + "/agreements/" + agreement_id + "/stop")
    try:
        r = requests.put(str(config.dic['URL_PM_SLA_MANAGER']) + "/agreements/" + agreement_id + "/stop",
                         verify=config.dic['VERIFY_SSL'])

        LOG.debug("Lifecycle-Management: MF2C: stop_sla_agreement:" + str(r))

        if r.status_code == 200 or r.status_code == 201 or r.status_code == 202 or r.status_code == 204:
            LOG.debug('Lifecycle-Management: MF2C: stop_sla_agreement: status_code=' +  str(r.status_code))
            return True

        LOG.error('Lifecycle-Management: MF2C: stop_sla_agreement: Error: status_code=' +  str(r.status_code))
        return False
    except:
        LOG.error('Lifecycle-Management: MF2C: stop_sla_agreement: Exception')
        return False


# PUT /agreements/<id>/stop
# TODO
def terminate_sla_agreement(agreement_id):
    agreement_id = agreement_id.replace('agreement/', '')
    LOG.debug("Lifecycle-Management: MF2C: stop_sla_agreement: agreement_id: " + agreement_id)
    LOG.info("Lifecycle-Management: MF2C: start_sla_agreement: HTTP PUT: " +
             str(config.dic['URL_PM_SLA_MANAGER']) + "/agreements/" + agreement_id + "/stop")
    try:
        r = requests.put(str(config.dic['URL_PM_SLA_MANAGER']) + "/agreements/" + agreement_id + "/stop",
                         verify=config.dic['VERIFY_SSL'])

        LOG.debug("Lifecycle-Management: MF2C: stop_sla_agreement:" + str(r))

        if r.status_code == 200 or r.status_code == 201 or r.status_code == 202 or r.status_code == 204:
            LOG.debug('Lifecycle-Management: MF2C: stop_sla_agreement: status_code=' +  str(r.status_code))
            return True

        LOG.error('Lifecycle-Management: MF2C: stop_sla_agreement: Error: status_code=' +  str(r.status_code))
        return False
    except:
        LOG.error('Lifecycle-Management: MF2C: stop_sla_agreement: Exception')
        return False


# CALL TO QoS PROVIDING
# service_management_qos: Returns which agents can be used to execute a specific service
# GET /qos/<id>
#   where <id>: id of the service instance
# ==> Returns a copy of the service instance specifying the agents that can be used to execute that service
def service_management_qos(service_instance):
    try:
        id = service_instance['id']
        LOG.debug("Lifecycle-Management: MF2C: service_management_qos: service_instance_id: " + id)
        LOG.info("Lifecycle-Management: MF2C: service_management_qos: HTTP GET: " +
                 str(config.dic['URL_AC_SERVICE_MNGMT']) + "/qos/" + id)

        r = requests.get(str(config.dic['URL_AC_SERVICE_MNGMT']) + "/qos/" + id,
                         verify=config.dic['VERIFY_SSL'])

        LOG.debug("Lifecycle-Management: MF2C: service_management_qos:" + str(r))
        json_data = json.loads(r.text)
        LOG.debug("Lifecycle-Management: MF2C: service_management_qos:" + str(json_data) + ", status: " + str(json_data['status']))

        if json_data['status'] == 200:
            LOG.debug("Lifecycle-Management: MF2C: service_management_qos: status=" + str(json_data['status']) +
                      ", service: " + str(json_data["service-instance"]))
            return json_data["service-instance"]

        LOG.error("Lifecycle-Management: MF2C: service_management_qos: Error: status: " + str(json_data['status']))
        return None
    except:
        LOG.error('Lifecycle-Management: MF2C: service_management_qos: Exception')
        return None


# service_management_get_service:
def service_management_get_service(service_id):
    try:
        LOG.debug("Lifecycle-Management: MF2C: service_management_get_service: " + service_id)
        LOG.info("Lifecycle-Management: MF2C: service_management_get_service: HTTP GET: " +
                 str(config.dic['URL_AC_SERVICE_MNGMT']) + "/categorizer/" + service_id)

        r = requests.get(str(config.dic['URL_AC_SERVICE_MNGMT']) + "/categorizer/" + service_id,
                         verify=config.dic['VERIFY_SSL'])

        LOG.debug("Lifecycle-Management: MF2C: service_management_get_service:" + str(r))
        json_data = json.loads(r.text)
        LOG.debug("Lifecycle-Management: MF2C: service_management_get_service:" + str(json_data) +
                  ", status: " + str(json_data['status']))

        if r.status_code == 200 and json_data['status'] == 404:
            LOG.error("Lifecycle-Management: MF2C: service_management_get_service: status_code=" + str(r.status_code) +
                      ", status: " + str(json_data['status']))
            return None
        elif r.status_code == 200:
            LOG.debug("Lifecycle-Management: MF2C: service_management_get_service: status_code=" + str(r.status_code) +
                      ", service: " + str(json_data["service"]))
            return json_data["service"]

        LOG.error('Lifecycle-Management: MF2C: service_management_get_service: Error: status_code=' + str(r.status_code))
        return None
    except:
        LOG.error('Lifecycle-Management: MF2C: service_management_get_service: Exception')
        return None


# CALL TO User Management (Profiling)
def user_management_profiling(user_id, remote=None):
    try:
        LOG.debug("Lifecycle-Management: MF2C: user_management_profiling: user_id: " + user_id)

        if remote is None:
            LOG.info("Lifecycle-Management: MF2C: user_management_profiling: HTTP GET: " +
                     str(config.dic['URL_AC_USER_MANAGEMENT']) + "/profiling/" + user_id)
            r = requests.get(str(config.dic['URL_AC_USER_MANAGEMENT']) + "/profiling/" + user_id,
                             verify=config.dic['VERIFY_SSL'])
        else:
            LOG.info("Lifecycle-Management: MF2C: user_management_profiling: HTTP GET: " +
                     "https://" + remote + ":46300/api/v1/user-management/profiling/" + user_id)
            r = requests.get("https://" + remote + ":46300/api/v1/user-management/profiling/" + user_id,
                             verify=config.dic['VERIFY_SSL'])
        json_data = json.loads(r.text)

        LOG.debug("Lifecycle-Management: MF2C: user_management_profiling:" + str(r) + ", json_data: " + str(json_data))
        if r.status_code == 200:
            LOG.debug('Lifecycle-Management: MF2C: user_management_profiling: status_code=' + str(r.status_code))
            return json_data

        LOG.error('Lifecycle-Management: MF2C: user_management_profiling: Error: status_code=' + str(r.status_code))
        return None
    except:
        LOG.error('Lifecycle-Management: MF2C: user_management_profiling: Exception')
        return None


# CALL TO User Management (Sharing Model)
def user_management_sharing_model(user_id, remote=None):
    try:
        LOG.debug("Lifecycle-Management: MF2C: user_management_sharing_model: user_id: " + user_id)

        if remote is None:
            LOG.info("Lifecycle-Management: MF2C: user_management_sharing_model: HTTP GET: " +
                     str(config.dic['URL_AC_USER_MANAGEMENT']) + "/sharingmodel/" + user_id)
            r = requests.get(str(config.dic['URL_AC_USER_MANAGEMENT']) + "/sharingmodel/" + user_id,
                             verify=config.dic['VERIFY_SSL'])
        else:
            LOG.info("Lifecycle-Management: MF2C: user_management_sharing_model: HTTP GET: " +
                     "https://" + remote + ":46300/api/v1/user-management/sharingmodel/" + user_id)
            r = requests.get("https://" + remote + ":46300/api/v1/user-management/sharingmodel/" + user_id,
                             verify=config.dic['VERIFY_SSL'])
        json_data = json.loads(r.text)

        LOG.debug("Lifecycle-Management: MF2C: user_management_sharing_model:" + str(r) + ", json_data: " + str(json_data))
        if r.status_code == 200:
            LOG.debug('Lifecycle-Management: MF2C: user_management_sharing_model: status_code=' + str(r.status_code))
            return json_data

        LOG.error('Lifecycle-Management: MF2C: user_management_sharing_model: Error: status_code=' + str(r.status_code))
        return None
    except:
        LOG.error('Lifecycle-Management: MF2C: user_management_sharing_model: Exception')
        return None
