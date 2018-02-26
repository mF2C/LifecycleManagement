"""
Agent decision
This is being developed for the MF2C Project: http://www.mf2c-project.eu/

Copyright: Atos Research and Innovation, 2017.

This code is licensed under an Apache 2.0 license. Please, refer to the LICENSE.TXT file for more information

Created on 09 feb. 2018

@author: Roi Sucasas - ATOS
"""


import lifecycle.mF2C.cimi as cimi
from lifecycle.utils.logs import LOG


# Get list of available agents
# IN:
#   Service example:
#       {
#           "service_path": "yeasy/simple-web"
#           ...
#       }
# OUT:
#   resources example:
#       {
#           "list_of_agents": ["192.168.252.7", "192.168.252.8", "192.168.252.9" ...],   // list urls / docker apis
#           ...
#       }
def get_available_agents_list(service):
    try:
        LOG.info("Lifecycle-Management: agent_decision: get_available_agents_list: " + str(service))

        # 1. RECOMMENDER -> RECIPE = GET_RECIPE(SERVICE)
        # The Lifecycle Management module calls the Recommender in order to get the optimal deployment configuration
        # to run the service
        recipe = cimi.get_recipe(service)

        # 2. LANDSCAPER -> RESOURCES = GET_RESOURCES(RECIPE)
        # Based on this optimal configuration returned by the Recommender, the Lifecycle module asks the Landscaper
        # for a list of resources that match this recommendation.
        resources = cimi.get_resources(recipe) # TODO resources = config.dic['AVAILABLE_AGENTS']

        # If no resources were found, then the Lifecycle Management forwards the request (submit a service) upwards
        if not resources or len(resources) == 0:
            # forwards the request upwards
            LOG.info("Lifecycle-Management: agent_decision: get_available_agents_list: forwards the request upwards" + service)
            return []
        # If there are available resources ...
        else:
            # 3. QoS PROVIDING -> RESOURCES = XXX (RESOURCES) -> RESOURCES = GET_RESOURCES(RESOURCES)
            resources = cimi.get_qos_resources(resources)

            # 4. USER MANAGEMENT -> RESOURCES = GET_RESOURCES(RESOURCES)
            resources = cimi.get_um_resources(resources)
            return resources
    except:
        LOG.error('Lifecycle-Management: agent_decision: get_available_agents_list: Exception')
        return None


# Select from list of available agents
# IN:
#   resources example:
#       {
#           "list_of_agents": ["192.168.252.7", "192.168.252.8", "192.168.252.9" ...],
#           ...
#       }
# OUT:
#   resources example:
#       {
#           "list_of_agents": ["192.168.252.7", "192.168.252.8", "192.168.252.9" ...],   // list urls / docker apis
#           ...
#       }
def select_agents_list(available_agents_list):
    try:
        LOG.info("Lifecycle-Management: agent_decision: select_agents_list: " + str(available_agents_list))
        LOG.warn("Lifecycle-Management: agent_decision: select_agents_list not implemented ")

        return available_agents_list
    except:
        LOG.error('Lifecycle-Management: agent_decision: select_agents_list: Exception')
        return None