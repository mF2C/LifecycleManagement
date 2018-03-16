"""
CIMI - Data management
This is being developed for the MF2C Project: http://www.mf2c-project.eu/

Copyright: Atos Research and Innovation, 2017.

This code is licensed under an Apache 2.0 license. Please, refer to the LICENSE.TXT file for more information

Created on 09 feb. 2018

@author: Roi Sucasas - ATOS
"""

import lifecycle.mF2C.cimi as cimi
from lifecycle.utils.logs import LOG


###############################################################################
# USER

# Get user
def get_user_by_id(user_id):
    LOG.info("User-Management: Data: get_user: " + str(user_id))
    return cimi.get_user_by_id(user_id)


###############################################################################
# SERVICE INSTANCE
#
# {
#        "user_id": "user/testuser",
#        "id": "",
#        "name": "",
#        "description": "profiling ...",
#        "resourceURI": "",
#        "service_id": {"href": ""},
#        "agreement_id": {"href": ""},
#        "status": "",
#        "agents": [
#            {"agent_id": {"href": ""}, "port": int, "container_id": "", "status": "", "num_cpus": int}
#       ]
#    }

# Get service instance
# OUT: Service instance (dict)
def get_service_instance(service_instance_id):
    LOG.info("Lifecycle-Management: Data: get_service_instance: " + service_instance_id)
    return cimi.get_service_instance_by_id(service_instance_id)


# Creates a new service instance
# OUT: Service instance (dict)
def create_service_instance(service, agents_list):
    LOG.info("Lifecycle-Management: Data: create_service_instance: " + str(service) + ", " + str(agents_list))

    # list of agents
    list_of_agents = []
    for agent_ip in agents_list:
        list_of_agents.append({"url": agent_ip, "container_id": ""})

    data = {"service_instance_id": "service_instance_id",
            "service_id": service['service_id'],
            "list_of_agents": list_of_agents,
            "status": "",
            "service": service}
    return cimi.add_resource("serviceinstances", data)
