"""
Allocation adapter
This is being developed for the MF2C Project: http://www.mf2c-project.eu/

Copyright: Atos Research and Innovation, 2017.

This code is licensed under an Apache 2.0 license. Please, refer to the LICENSE.TXT file for more information

Created on 09 feb. 2018

@author: Roi Sucasas - ATOS
"""


import lifecycle.modules.adapters.lf_adapter as lf_adapter
from lifecycle.utils.logs import LOG


# allocates service in agents
# IN:
#   Service instance (example):
#       {
#           "service_instance_id": "service_id",
#           "service_id": service['service_id'],
#           "list_of_agents": [{"url": "192.168.252.7" "container_id": ""} ...],
#           "status": "",
#           ("service": service)
#       }
def allocate(service_instance):
    try:
        LOG.info("Lifecycle-Management: allocation_adapter: allocate: " + str(service_instance))

        # TODO
        # DISTRIBUTED EXECUTION RUNTIME / COMPSS -> ALLOCATE(RESOURCES, SERVICE)
        # Call to COMPSs in order to allocate resources (Iteration 1)
        # Call to the Service Management in order to allocate resources (Iteration 2)
        #return dependencies.allocate(service, agents_list)

        return lf_adapter.deploy(service_instance)
    except:
        LOG.error('Lifecycle-Management: allocation_adapter: allocate: Exception')
        return None