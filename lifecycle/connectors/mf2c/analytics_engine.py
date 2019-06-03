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
from urllib3.exceptions import NewConnectionError


# CALL TO LANDSCAPER & RECOMMENDER: get service's recipe / get available resources for a recipe
#   =>  POST 'http://localhost:46020/mf2c/optimal'
# 	    BODY: service json
def get_optimal_resources():
    LOG.debug("[lifecycle.connectors.mf2c.analytics_engine] [get_optimal_resources] Getting list of devices ...")
    try:
        LOG.info("[lifecycle.connectors.mf2c.analytics_engine] [get_optimal_resources] HTTP POST: " + str(config.dic['URL_PM_RECOM_LANDSCAPER']) + "/optimal")
        r = requests.post(str(config.dic['URL_PM_RECOM_LANDSCAPER']) + "/optimal",
                          json={"sort_order": ["cpu", "memory"],
                                "name":"test"},
                          headers={"Accept": "text/json", "Content-Type": "application/json"},
                          verify=config.dic['VERIFY_SSL'],
                          timeout=config.dic['TIMEOUT_ANALYTICSENGINE'])
        LOG.debug("[lifecycle.connectors.mf2c.analytics_engine] [get_optimal_resources] response: " + str(r) + ", " + str(r.text)) # str(r.json()))

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
            LOG.debug("[lifecycle.connectors.mf2c.analytics_engine] [get_optimal_resources] json_data=" + str(json_data))

            # create list of agents
            list_of_agents = []
            for elem in json_data:
                list_of_agents.append({"agent_ip": elem['ipaddress']})

            LOG.debug("[lifecycle.connectors.mf2c.analytics_engine] [get_optimal_resources] list_of_agents=" + str(list_of_agents))
            return list_of_agents

        LOG.error("[lifecycle.connectors.mf2c.analytics_engine] [get_optimal_resources] Error: status_code=" +  str(r.status_code) + "; Returning None ...")
    except NewConnectionError:
        LOG.error("[lifecycle.connectors.mf2c.analytics_engine] [get_optimal_resources] New Connection Error. Returning None ...")
    except:
        LOG.exception("[lifecycle.connectors.mf2c.analytics_engine] [get_optimal_resources] Exception; Returning None ...")
    return None