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
from lifecycle import config


###############################################################################
# USER

# Get user
def get_user_by_id(user_id):
    LOG.info("User-Management: Data: get_user: " + str(user_id))
    return cimi.get_user_by_id(user_id)


###############################################################################
# SERVICE
#
# {
#        "id": "",
#        "name": "",
#        "description": "profiling ...",
#        "resourceURI": "",
#        ## service
#        "category": {
#        "cpu": "low",
#        "memory": "low",
#        "storage": "low",
#        "inclinometer": false,
#        "temperature": false,
#        "jammer": false,
#        "location": false
#        }
#  }
###############################################################################
# SERVICE INSTANCE
#
# {
#        "id": "",
#        "name": "",
#        "description": "profiling ...",
#        "resourceURI": "",
#        ## service instance
#        "service_id": {"href": "blaat"},
#        "agreement_id": {"href": "blaat"},
#        "status": "waiting",
#        "agents": [
#            {"agent_id": {"href": "blaat"}, "port": 8987, "container_id": "123daf231230f", "status": "waiting", "num_cpus": 2, "allow": true}
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
    # {"agent_id": {"href": "blaat"}, "port": 8987, "container_id": "123daf231230f", "status": "waiting", "num_cpus": 2, "allow": true}
    for agent_ip in agents_list:
        list_of_agents.append({"agent":         {"href": "agent/1230958abdef2"},
                               "port":          8987,
                               "url":           agent_ip,
                               "status":        "waiting",
                               "num_cpus":      2,
                               "allow":         True,
                               "container_id":  "-"})

    data = {"service_id":       {"href": "service/" + service['id']},
            "agreement_id":     {"href": "blaat"},
            "agents":           list_of_agents,
            "status":           "waiting"}              #"service":          service}
    return cimi.add_resource(config.dic['CIMI_SERVICE_INSTANCES'], data)
