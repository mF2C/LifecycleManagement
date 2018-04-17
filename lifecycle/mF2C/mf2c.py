"""
Interactions with other mF2C components
This is being developed for the MF2C Project: http://www.mf2c-project.eu/

Copyright: Roi Sucasas Font, Atos Research and Innovation, 2017.

This code is licensed under an Apache 2.0 license. Please, refer to the LICENSE.TXT file for more information

Created on 09 feb. 2018

@author: Roi Sucasas - ATOS
"""

import requests
import json
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
        json_data = json.loads(r.text)
        agent = json_data['agent']
        LOG.debug("Lifecycle-Management: MF2C: lifecycle_deploy:" + str(agent))

        if r.status_code == 200 or r.status_code == 201 or r.status_code == 202:
            LOG.debug('Lifecycle-Management: MF2C: lifecycle_deploy: status_code=' + str(r.status_code) + '; response: ' + str(json_data))
            return True

        LOG.error('Lifecycle-Management: MF2C: lifecycle_deploy: Error: status_code=' + str(r.status_code))
        return False
    except:
        LOG.error('Lifecycle-Management: MF2C: lifecycle_deploy: Exception')
        return False


# lifecycle_operation: call to lifceycle from other agent in order to start/stop... a service
def lifecycle_operation(agent, operation):
    LOG.info("Lifecycle-Management: Dependencies: lifecycle_operation: " + str(agent) + ", " + operation)
    try:
        r = requests.put("https://" + agent['url'] + ":" + str(config.dic['SERVER_PORT']) + "/api/v1/lifecycle/service-instance-operations",
                         json={"operation": operation,
                               "agent": agent},
                         verify=config.dic['VERIFY_SSL'])
        json_data = json.loads(r.text)
        agent = json_data['agent']
        LOG.debug("Lifecycle-Management: MF2C: lifecycle_operation:" + str(agent))

        if r.status_code == 200 or r.status_code == 201 or r.status_code == 202:
            LOG.debug('Lifecycle-Management: Dependencies: lifecycle_operation: status_code=' +  str(r.status_code) + '; response: ' + str(json_data))
            return True

        LOG.error('Lifecycle-Management: Dependencies: lifecycle_operation: Error: status_code=' +  str(r.status_code))
        return False
    except:
        LOG.error('Lifecycle-Management: Dependencies: lifecycle_operation: Exception')
        return False


###############################################################################
# Interactions with other mF2C components
# get_resources: TODO CALL TO LANDSCAPER: get available resources for a recipe
def get_resources():
    LOG.warn("Lifecycle-Management: Dependencies: get_resources not implemented ")
    return config.dic['AVAILABLE_AGENTS']


# TODO CALL TO RECOMMENDER: get service's recipe
# TODO CALL TO QoS PROVIDING: get resources
# TODO CALL TO User Management: get resources
# TODO CALL TO DISTRIBUTED EXECUTION RUNTIME / COMPSS: allocate
# TODO CALL TO SLA:
# TODO CALL TO DISTRIBUTED EXECUTION RUNTIME / COMPSS: execute
