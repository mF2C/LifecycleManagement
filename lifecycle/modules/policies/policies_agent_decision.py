"""
Agent decision policies
This is being developed for the MF2C Project: http://www.mf2c-project.eu/

Copyright: Atos Research and Innovation, 2017.

This code is licensed under an Apache 2.0 license. Please, refer to the LICENSE.TXT file for more information

Created on 04 dic. 2018

@author: Roi Sucasas - ATOS
"""

import lifecycle.data.mF2C.mf2c as mf2c
import config as config
import common.common as common
from common.logs import LOG
from common.common import SERVICE_DOCKER, SERVICE_DOCKER_COMPOSE, SERVICE_COMPSS, SERVICE_KUBERNETES, SERVICE_DOCKER_SWARM


# select_agents_from_list
def select_agents_from_list(agents_list, service_type):
    list_of_agents = []

    # SERVICE_COMPSS
    if service_type == SERVICE_COMPSS:
        LOG.debug("LIFECYCLE: policies: select_agents_from_list: [SERVICE_COMPSS] service will be deployed in all selected agents")
        list_of_agents = agents_list
    # OTHERS
    elif service_type == SERVICE_DOCKER_COMPOSE or service_type == SERVICE_DOCKER or service_type == SERVICE_DOCKER_SWARM or service_type == SERVICE_KUBERNETES:
        list_of_agents.append(agents_list[0])
        LOG.debug("LIFECYCLE: policies: select_agents_from_list: [" + service_type + "] service will be deployed in first agent: " + str(list_of_agents))

    LOG.debug("LIFECYCLE: policies: select_agents_from_list: agents final list: " + str(list_of_agents))
    return list_of_agents
