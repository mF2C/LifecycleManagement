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
from lifecycle import config
from lifecycle.utils.logs import LOG


###############################################################################
# LIFECYCLE interactions
# lifecycle_deploy: call to lifceycle from other agent in order to deploy a service
def lifecycle_deploy(service, agent):
    LOG.info("Lifecycle-Management: MF2C: lifecycle_deploy: " + str(service) + ", " + str(agent))
    try:
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
    LOG.info("Lifecycle-Management: MF2C: lifecycle_operation: " + str(agent) + ", " + operation)
    try:
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
# TODO CALL TO LANDSCAPER
# get_resources: get available resources for a recipe
def get_resources():
    LOG.warn("Lifecycle-Management: MF2C: get_resources not implemented ")
    return config.dic['AVAILABLE_AGENTS']


# CALL TO SLA MANAGEMENT
# start_sla_agreement: start SLA agreement
# PUT /agreements/<id>/start   (stop)
def start_sla_agreement(agreement_id):
    LOG.info("Lifecycle-Management: MF2C: start_sla_agreement: agreement_id: " + agreement_id)
    try:
        r = requests.put(str(config.dic['URL_PM_SLA_MANAGER']) + "/agreements/" + agreement_id + "/start",
                         verify=config.dic['VERIFY_SSL'])

        LOG.debug("Lifecycle-Management: MF2C: start_sla_agreement:" + str(r))

        if r.status_code == 200 or r.status_code == 201 or r.status_code == 202:
            LOG.debug('Lifecycle-Management: MF2C: start_sla_agreement: status_code=' +  str(r.status_code))
            return True

        LOG.error('Lifecycle-Management: MF2C: start_sla_agreement: Error: status_code=' +  str(r.status_code))
        return False
    except:
        LOG.error('Lifecycle-Management: MF2C: start_sla_agreement: Exception')
        return False


# PUT /agreements/<id>/stop
def stop_sla_agreement(agreement_id):
    LOG.info("Lifecycle-Management: MF2C: stop_sla_agreement: agreement_id: " + agreement_id)
    try:
        r = requests.put(str(config.dic['URL_PM_SLA_MANAGER']) + "/agreements/" + agreement_id + "/stop",
                         verify=config.dic['VERIFY_SSL'])

        LOG.debug("Lifecycle-Management: MF2C: stop_sla_agreement:" + str(r))

        if r.status_code == 200 or r.status_code == 201 or r.status_code == 202:
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
        LOG.info("Lifecycle-Management: MF2C: service_management_qos: service_instance_id: " + id)

        r = requests.get(str(config.dic['URL_AC_QoS_PROVIDING']) + "/qos/" + id,
                         verify=config.dic['VERIFY_SSL'])

        LOG.debug("Lifecycle-Management: MF2C: service_management_qos:" + str(r))

        if r.status_code == 200 or r.status_code == 201 or r.status_code == 202:
            LOG.debug('Lifecycle-Management: MF2C: service_management_qos: status_code=' + str(r.status_code))
            return r

        LOG.error('Lifecycle-Management: MF2C: service_management_qos: Error: status_code=' + str(r.status_code))
        return None
    except:
        LOG.error('Lifecycle-Management: MF2C: service_management_qos: Exception')
        return None


# CALL TO User Management (Profiling)
def user_management_profiling(user_id):
    try:
        LOG.info("Lifecycle-Management: MF2C: user_management_profiling: user_id: " + user_id)

        r = requests.get(str(config.dic['URL_AC_USER_MANAGEMENT']) + "/profiling/" + user_id,
                         verify=config.dic['VERIFY_SSL'])
        json_data = json.loads(r.text)

        LOG.debug("Lifecycle-Management: MF2C: user_management_profiling:" + str(r) + ", json_data: " + str(json_data))
        if r.status_code == 200 or r.status_code == 201 or r.status_code == 202:
            LOG.debug('Lifecycle-Management: MF2C: user_management_profiling: status_code=' + str(r.status_code))
            return json_data

        LOG.error('Lifecycle-Management: MF2C: user_management_profiling: Error: status_code=' + str(r.status_code))
        return None
    except:
        LOG.error('Lifecycle-Management: MF2C: user_management_profiling: Exception')
        return None


# CALL TO User Management (Sharing Model)
def user_management_sharing_model(user_id):
    try:
        LOG.info("Lifecycle-Management: MF2C: user_management_sharing_model: user_id: " + user_id)

        r = requests.get(str(config.dic['URL_AC_USER_MANAGEMENT']) + "/sharingmodel/" + user_id,
                         verify=config.dic['VERIFY_SSL'])
        json_data = json.loads(r.text)

        LOG.debug("Lifecycle-Management: MF2C: user_management_sharing_model:" + str(r) + ", json_data: " + str(json_data))
        if r.status_code == 200 or r.status_code == 201 or r.status_code == 202:
            LOG.debug('Lifecycle-Management: MF2C: user_management_sharing_model: status_code=' + str(r.status_code))
            return json_data

        LOG.error('Lifecycle-Management: MF2C: user_management_sharing_model: Error: status_code=' + str(r.status_code))
        return None
    except:
        LOG.error('Lifecycle-Management: MF2C: user_management_sharing_model: Exception')
        return None



# TODO CALL TO RECOMMENDER: get service's recipe
# TODO CALL TO DISTRIBUTED EXECUTION RUNTIME / COMPSS: allocate
# TODO CALL TO DISTRIBUTED EXECUTION RUNTIME / COMPSS: execute
