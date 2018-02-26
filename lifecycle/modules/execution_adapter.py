"""
Execution adapter
This is being developed for the MF2C Project: http://www.mf2c-project.eu/

Copyright: Atos Research and Innovation, 2017.

This code is licensed under an Apache 2.0 license. Please, refer to the LICENSE.TXT file for more information

Created on 09 feb. 2018

@author: Roi Sucasas - ATOS
"""


import lifecycle.modules.adapters.lf_adapter as lf_adapter
from lifecycle.utils.logs import LOG


# executes service in agents
# IN:
#   Service instance (example):
#       {
#           "service_instance_id": "service_id",
#           "service_id": service['service_id'],
#           "list_of_agents": [{"url": "192.168.252.7" "container_id": ""} ...],
#           "status": "",
#           ("service": service)
#       }
def execute(service_instance):
    try:
        LOG.info("Lifecycle-Management: execution_adapter: execute: " + str(service_instance))

        # TODO
        # DISTRIBUTED EXECUTION RUNTIME / COMPSS -> EXECUTE(SERVICE)
        # The Lifecycle calls the Distributed Execution Runtime in order to start the execution of the service.
        #return dependencies.execute(service, agents_list)

        return lf_adapter.execute(service_instance)
    except:
        LOG.error('Lifecycle-Management: execution_adapter: execute: Exception')
        return None