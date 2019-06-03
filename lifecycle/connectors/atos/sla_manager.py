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


# create_sla_agreement: create SLA agreement
# curl -k -X POST -d @resources/samples/create-agreement.json https://localhost:8090/mf2c/create-agreement
# {"template_id":"t01","agreement_id":"9be511e8-347f-4a40-b784-e80789e4c65b","parameters":{"user":"a-user-id"}}
def create_sla_agreement(template_id, user_id, service):
    LOG.debug("[lifecycle.connectors.atos.sla_manager] [create_sla_agreement] template_id=" + template_id + ", user_id=" + user_id + ", service=" + service['name'])
    try:
        LOG.info("[lifecycle.connectors.atos.sla_manager] [create_sla_agreement] HTTP POST: " + str(config.dic['URL_PM_SLA_MANAGER']) + "/mf2c/create-agreement")
        body = {"template_id": template_id,
                "parameters": {"user":user_id}}
        r = requests.post(str(config.dic['URL_PM_SLA_MANAGER']) + "/mf2c/create-agreement",
                          json=body,
                          verify=config.dic['VERIFY_SSL'])
        LOG.debug("[lifecycle.connectors.atos.sla_manager] [create_sla_agreement] response: " + str(r) + ", " + str(r.json()))

        if r.status_code >= 200 and r.status_code <= 204:
            json_data = json.loads(r.text)
            LOG.debug("[lifecycle.connectors.atos.sla_manager] [create_sla_agreement] json_data=" + str(json_data))
            return json_data['agreement_id']

        LOG.error("[lifecycle.connectors.atos.sla_manager] [create_sla_agreement] Error: status_code=" +  str(r.status_code) + "; Returning None ...")
    except:
        LOG.exception("[lifecycle.connectors.atos.sla_manager] [create_sla_agreement] Exception; Returning None ...")
    return None


# start_agreement: start SLA agreement
# PUT /agreements/<id>/start   (stop)
def start_agreement(agreement_id):
    agreement_id = agreement_id.replace('agreement/', '')
    LOG.debug("[lifecycle.connectors.atos.sla_manager] [start_agreement] agreement_id: " + agreement_id)
    try:
        LOG.info("[lifecycle.connectors.atos.sla_manager] [start_agreement] HTTP PUT: " + str(config.dic['URL_PM_SLA_MANAGER']) + "/agreements/" + agreement_id + "/start")
        r = requests.put(str(config.dic['URL_PM_SLA_MANAGER']) + "/agreements/" + agreement_id + "/start",
                         verify=config.dic['VERIFY_SSL'])
        LOG.debug("[lifecycle.connectors.atos.sla_manager] [start_agreement] response: " + str(r) + ", " + str(r.text))

        if r.status_code >= 200 and r.status_code <= 204:
            return True

        LOG.error("[lifecycle.connectors.atos.sla_manager] [start_agreement] Error: status_code=" +  str(r.status_code) + "; Returning False ...")
    except:
        LOG.exception("[lifecycle.connectors.atos.sla_manager] [start_agreement] Exception; Returning False ...")
    return False


# stop_agreement:
# PUT /agreements/<id>/stop
def stop_agreement(agreement_id):
    agreement_id = agreement_id.replace('agreement/', '')
    LOG.debug("[lifecycle.connectors.atos.sla_manager] [stop_agreement] agreement_id: " + agreement_id)
    try:
        LOG.info("[lifecycle.connectors.atos.sla_manager] [stop_agreement] HTTP PUT: " + str(config.dic['URL_PM_SLA_MANAGER']) + "/agreements/" + agreement_id + "/stop")
        r = requests.put(str(config.dic['URL_PM_SLA_MANAGER']) + "/agreements/" + agreement_id + "/stop",
                         verify=config.dic['VERIFY_SSL'])
        LOG.debug("[lifecycle.connectors.atos.sla_manager] [stop_agreement] response: " + str(r)) # + ", " + str(r.json()))

        if r.status_code >= 200 and r.status_code <= 204:
            return True

        LOG.error("[lifecycle.connectors.atos.sla_manager] [stop_agreement] rror: status_code=" +  str(r.status_code) + "; Returning False ...")
    except:
        LOG.exception("[lifecycle.connectors.atos.sla_manager] [stop_agreement] Exception; Returning False ...")
    return False


# terminate_agreement:
# PUT /agreements/<id>/stop
def terminate_agreement(agreement_id):
    agreement_id = agreement_id.replace('agreement/', '')
    LOG.debug("[lifecycle.connectors.atos.sla_manager] [terminate_agreement] agreement_id: " + agreement_id)
    try:
        LOG.info("[lifecycle.connectors.atos.sla_manager] [terminate_agreement] HTTP PUT: " + str(config.dic['URL_PM_SLA_MANAGER']) + "/agreements/" + agreement_id + "/stop")
        r = requests.put(str(config.dic['URL_PM_SLA_MANAGER']) + "/agreements/" + agreement_id + "/terminate",
                         verify=config.dic['VERIFY_SSL'])
        LOG.debug("[lifecycle.connectors.atos.sla_manager] [terminate_agreement] response: " + str(r)) # + ", " + str(r.json()))

        if r.status_code >= 200 and r.status_code <= 204:
            return True

        LOG.error("[lifecycle.connectors.atos.sla_manager] [terminate_agreement] Error: status_code=" +  str(r.status_code) + "; Returning False ...")
    except:
        LOG.exception("[lifecycle.connectors.atos.sla_manager] [terminate_agreement] Exception; Returning False ...")
    return False