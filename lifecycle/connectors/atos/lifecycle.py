"""
Interactions with other mF2C components
This is being developed for the MF2C Project: http://www.mf2c-project.eu/

Copyright: Roi Sucasas Font, Atos Research and Innovation, 2017.

This code is licensed under an Apache 2.0 license. Please, refer to the LICENSE.TXT file for more information

Created on 09 may. 2019

@author: Roi Sucasas - ATOS
"""

import requests, json, ast
import config
from lifecycle.logs import LOG


# FORWARD REQUEST TO LEADER
# parent_deploy: call to parent's lifceycle; forwards a "submit service" request
def parent_deploy(leader_ip, service_id, user_id, sla_template_id, service_instance_id):
    LOG.debug("[lifecycle.connectors.atos.lifecycle] [parent_deploy] forward request to leader: " + leader_ip + ", service_id: " + str(service_id) +
              ", user_id: " + str(user_id) + ", sla_template_id: " + sla_template_id + ", service_instance_id: " + service_instance_id)
    try:
        LOG.info("[lifecycle.connectors.atos.lifecycle] [parent_deploy] HTTP POST: http://" + leader_ip + ":" + str(config.dic['SERVER_PORT']) + "/api/v2/lm/service")

        r = requests.post("http://" + leader_ip + ":" + str(config.dic['SERVER_PORT']) + "/api/v2/lm/service",
                          json={"service_id": service_id,
                                "user_id": user_id,
                                "sla_template": sla_template_id,
                                "service_instance_id": service_instance_id},
                          verify=config.dic['VERIFY_SSL'])
        LOG.debug("[lifecycle.connectors.atos.lifecycle] [parent_deploy] response: " + str(r) + ", " + str(r.json()))

        if r.status_code >= 200 and r.status_code <= 204:
            return True

        LOG.error("[lifecycle.connectors.atos.lifecycle] [parent_deploy] Error: status_code=" + str(r.status_code) + "; Returning None ...")
    except:
        LOG.exception("[lifecycle.connectors.atos.lifecycle] [parent_deploy] Exception; Returning False ...")
    return False


# DEPLOY A SERVICE
# deploy: call to lifceycle from other agent in order to deploy a service
def deploy(service, service_instance, agent):
    LOG.debug("[lifecycle.connectors.atos.lifecycle] [deploy] deploy service in agent: " + str(service) + ", " + str(service_instance) + ", " + str(agent))
    try:
        LOG.info("[lifecycle.connectors.atos.lifecycle] [deploy] HTTP POST: http://" + agent['url'] + ":" + str(config.dic['SERVER_PORT']) + "/api/v2/lm/service-instance-int")
        r = requests.post("http://" + agent['url'] + ":" + str(config.dic['SERVER_PORT']) + "/api/v2/lm/service-instance-int",
                          json={"service": service,
                                "service_instance": service_instance,
                                "agent": agent},
                          verify=config.dic['VERIFY_SSL'])
        LOG.debug("[lifecycle.connectors.atos.lifecycle] [deploy] response: " + str(r) + ", " + str(r.json()))

        if r.status_code == 200:
            json_data = json.loads(r.text)
            agent = json_data['agent']
            LOG.debug("[lifecycle.connectors.atos.lifecycle] [deploy] result: agent: " + str(agent))
            return ast.literal_eval(agent)

        LOG.error("[lifecycle.connectors.atos.lifecycle] [deploy] Error: status_code=" + str(r.status_code) + "; Returning None ...")
    except:
        LOG.exception("[lifecycle.connectors.atos.lifecycle] [deploy] Exception; Returning None ...")
    return None


# START / STOP SERVICE INSTANCE
# operation: call to lifceycle from other agent in order to start/stop... a service
def operation(service, agent, operation):
    LOG.debug("[lifecycle.connectors.atos.lifecycle] [operation] " + str(service) + ", " + str(agent) + ", " + operation)
    try:
        LOG.info("[lifecycle.connectors.atos.lifecycle] [operation] HTTP PUT: http://" + agent['url'] + ":" + str(config.dic['SERVER_PORT']) + "/api/v2/lm/service-instance-int")
        r = requests.put("http://" + agent['url'] + ":" + str(config.dic['SERVER_PORT']) + "/api/v2/lm/service-instance-int",
                         json={"service": service,
                               "operation": operation,
                               "agent": agent},
                         verify=config.dic['VERIFY_SSL'])
        LOG.debug("[lifecycle.connectors.atos.lifecycle] [operation] response: " + str(r) + ", " + str(r.json()))

        if r.status_code == 200:
            json_data = json.loads(r.text)
            agent = json_data['agent']
            LOG.debug("[connectors.atos.lifecycle] [operation] agent: " + str(agent))
            return ast.literal_eval(agent)

        LOG.error("[lifecycle.connectors.atos.lifecycle] [operation] Error: status_code=" +  str(r.status_code) + "; Returning None ...")
    except:
        LOG.exception("[lifecycle.connectors.atos.lifecycle] [operation] Exception; Returning None ...")
    return None


# um_check_avialability: call to lifceycle from other agent in order to get sharing model and user profile
def um_check_avialability(agent):
    LOG.debug("[lifecycle.connectors.atos.lifecycle] [um_check_avialability] " + str(agent))
    try:
        LOG.info("[lifecycle.connectors.atos.lifecycle] [um_check_avialability] HTTP GET: http://" + agent['url'] + ":" + str(config.dic['SERVER_PORT']) + "/api/v2/lm/check-agent-um")
        r = requests.get("http://" + agent['url'] + ":" + str(config.dic['SERVER_PORT']) + "/api/v2/lm/check-agent-um",
                         verify=config.dic['VERIFY_SSL'])
        LOG.debug("[lifecycle.connectors.atos.lifecycle] [um_check_avialability] response: " + str(r) + ", " + str(r.json()))

        if r.status_code == 200:
            json_data = json.loads(r.text)
            LOG.debug("[lifecycle.connectors.atos.lifecycle] [um_check_avialability] json_data=" + str(json_data))
            return json_data

        LOG.error("[lifecycle.connectors.atos.lifecycle] [um_check_avialability] Error: status_code=" +  str(r.status_code) + "; Returning None ...")
    except:
        LOG.exception("[lifecycle.connectors.atos.lifecycle] [um_check_avialability] Exception; Returning None ...")
    return None


# check_agent_swarm: call to lifceycle from other agent to check if docker swarm is supported
def check_agent_swarm(agent):
    LOG.debug("[lifecycle.connectors.atos.lifecycle] [check_agent_swarm] " + str(agent))
    try:
        LOG.info("[lifecycle.connectors.atos.lifecycle] [check_agent_swarm] HTTP GET: http://" + agent['url'] + ":" + str(config.dic['SERVER_PORT']) + "/api/v2/lm/check-agent-swarm")
        r = requests.get("http://" + agent['url'] + ":" + str(config.dic['SERVER_PORT']) + "/api/v2/lm/check-agent-swarm",
                         verify=config.dic['VERIFY_SSL'])
        LOG.debug("[lifecycle.connectors.atos.lifecycle] [check_agent_swarm] response: " + str(r) + ", " + str(r.json()))

        if r.status_code == 200:
            json_data = json.loads(r.text)
            LOG.debug("[lifecycle.connectors.atos.lifecycle] [check_agent_swarm] json_data=" + str(json_data))
            return json_data

        LOG.error("[lifecycle.connectors.atos.lifecycle] [check_agent_swarm] Error: status_code=" +  str(r.status_code) + "; Returning None ...")
    except:
        LOG.exception("[lifecycle.connectors.atos.lifecycle] [check_agent_swarm] Exception; Returning None ...")
    return None