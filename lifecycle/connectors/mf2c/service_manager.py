"""
Interactions with other mF2C components
This is being developed for the MF2C Project: http://www.mf2c-project.eu/

Copyright: Roi Sucasas Font, Atos Research and Innovation, 2017.

This code is licensed under an Apache 2.0 license. Please, refer to the LICENSE.TXT file for more information

Created on 09 may. 2019

@author: Roi Sucasas - ATOS
"""

import requests, json
import config
from lifecycle.logs import LOG


# CALL TO QoS PROVIDING
# qos_providing: Returns which agents can be used to execute a specific service
# GET /qos/<id>
#   where <id>: id of the service instance
# ==> Returns a copy of the service instance specifying the agents that can be used to execute that service
def qos_providing(service_instance):
    try:
        if 'id' not in service_instance:
            LOG.error("[lifecycle.connectors.mf2c.service_manager] [qos_providing] 'id' not found in service instance; Returning None ...")
            return None

        id = service_instance['id']
        id_service = service_instance['service']
        LOG.debug("[lifecycle.connectors.mf2c.service_manager] [qos_providing] service: " + id_service + " service_instance_id: " + id)

        LOG.info("[lifecycle.connectors.mf2c.service_manager] [qos_providing] HTTP GET: " + str(config.dic['URL_AC_SERVICE_MNGMT']) + "/" + id)
        r = requests.get(str(config.dic['URL_AC_SERVICE_MNGMT']) + "/" + id,
                         verify=config.dic['VERIFY_SSL'])
        LOG.debug("[lifecycle.connectors.mf2c.service_manager] [qos_providing] response: " + str(r) + ", " + str(r.json()))

        json_data = json.loads(r.text)
        LOG.debug("[lifecycle.connectors.mf2c.service_manager] [qos_providing] json_data=" + str(json_data) + ", status=" + str(json_data['status']))

        if json_data['status'] == 200:
            return json_data["service-instance"]

        LOG.error("[lifecycle.connectors.mf2c.service_manager] [qos_providing] status: " + str(json_data['status']) + "; Returning None ...")
    except:
        LOG.exception("[lifecycle.connectors.mf2c.service_manager] [qos_providing] Exception; Returning None ...")
    return None
