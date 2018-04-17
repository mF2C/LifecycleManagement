"""
Allocation adapter
This is being developed for the MF2C Project: http://www.mf2c-project.eu/

Copyright: Atos Research and Innovation, 2017.

This code is licensed under an Apache 2.0 license. Please, refer to the LICENSE.TXT file for more information

Created on 09 feb. 2018

@author: Roi Sucasas - ATOS
"""

import lifecycle.modules.adapters.lf_adapter as lf_adapter


# allocates service in agents
# IN:
#   Service instance (example):
#   {
#       ...
#       "id": "",
#       "service_id": "",
#       "agreement_id": "",
#       "status": "waiting",
#       "agents": [
#           {"agent": resource-link, "url": "192.168.1.31", "port": 8081, "container_id": "10asd673f", "status": "waiting",
#               "num_cpus": 3, "allow": true},
#           {"agent": resource-link, "url": "192.168.1.34", "port": 8081, "container_id": "99asd673f", "status": "waiting",
#               "num_cpus": 2, "allow": true}
#      ]
#   }
def allocate(service_instance):
    # TODO
    # DISTRIBUTED EXECUTION RUNTIME / COMPSS -> ALLOCATE(RESOURCES, SERVICE)
    # Call to COMPSs in order to allocate resources (Iteration 1)
    # Call to the Service Management in order to allocate resources (Iteration 2)
    # return dependencies.allocate(service, agents_list)
    return lf_adapter.deploy(service_instance)


# Deploy service in an agent
# IN:
#   Service example:
#       {
#           "name": "hello-world",
#           "description": "Hello World Service",
#           "resourceURI": "/hello-world",
#           "exec": "hello-world",
#           "exec_type": "docker",
#           "exec_ports": ["8080", "8081"]
#           "category": {
#               "cpu": "low",
#               "memory": "low",
#               "storage": "low",
#               "inclinometer": false,
#               "temperature": false,
#               "jammer": false,
#               "location": false
#           }
#       }
#   Agent example:
#    {"agent": resource-link, "url": "192.168.1.31", "port": 8081, "container_id": "10asd673f", "status": "waiting",
#     "num_cpus": 3, "allow": true}
#
# OUT: status value
def allocate_service_agent(service, agent):
    return lf_adapter.deploy_service_agent(service, agent)