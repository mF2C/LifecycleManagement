"""
CIMI - Data management
This is being developed for the MF2C Project: http://www.mf2c-project.eu/

Copyright: Atos Research and Innovation, 2017.

This code is licensed under an Apache 2.0 license. Please, refer to the LICENSE.TXT file for more information

Created on 09 feb. 2018

@author: Roi Sucasas - ATOS
"""

from lifecycle.utils.logs import LOG


#   Service instance (example):
#       {
#           "service_instance_id": "service_id",
#           "service_id": service['service_id'],
#           "list_of_agents": [{"url": "tcp://192.168.252.7:2375"} {"url": "tcp://192.168.252.8:2375"}],
#           "status": "",
#           ("service": service)
#       }


# Get service instance
# OUT:
#   Service instance (example):
#       {
#           "service_instance_id": "service_id",
#           "service_id": service['service_id'],
#           "list_of_agents": [{"url": "192.168.252.7" "container_id": ""} ...]
#           "status": "",
#           ("service": service)
#       }
def get_service_instance(service_instance_id):
    LOG.info("Lifecycle-Management: Data: get_service_instance: " + service_instance_id)

    # TODO Get from CIMI

    # return service instance
    return {"service_instance_id": "service_instance_id",
            "service_id": "service_id",
            "list_of_agents": [{"url": "192.168.252.7", "container_id": ""}, {"url": "192.168.252.7", "container_id": ""}],
            "status": "",
            "service": {}}


# Creates a new service instance
# OUT:
#   Service instance (example):
#       {
#           "service_instance_id": "service_id",
#           "service_id": service['service_id'],
#           "list_of_agents": [{"url": "192.168.252.7", "container_id": ""} ...]
#           "list_of_agents": [{"url": "192.168.252.7", "container_id": ""} ...]
#           "status": "",
#           ("service": service)
#       }
def create_service_instance(service, agents_list):
    LOG.info("Lifecycle-Management: Data: create_service_instance: " + str(service) + ", " + str(agents_list))

    list_of_agents = []
    for agent_ip in agents_list:
        list_of_agents.append({"url": agent_ip, "container_id": ""})

    # TODO Save to CIMI

    # return service instance
    return {"service_instance_id": "service_instance_id",
            "service_id": service['service_id'],
            "list_of_agents": list_of_agents,
            "status": "",
            "service": service}