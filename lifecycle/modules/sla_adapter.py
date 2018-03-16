"""
SLA adapter
This is being developed for the MF2C Project: http://www.mf2c-project.eu/

Copyright: Atos Research and Innovation, 2017.

This code is licensed under an Apache 2.0 license. Please, refer to the LICENSE.TXT file for more information

Created on 09 feb. 2018

@author: Roi Sucasas - ATOS
"""


import lifecycle.mF2C.mf2c as cimi
from lifecycle.utils.logs import LOG


# initialize all the SLA processes
# IN:
#   Service instance (example):
#       {
#           "service_instance_id": "service_id",
#           "service_id": service['service_id'],
#           "list_of_agents": [{"url": "192.168.252.7" "container_id": ""} ...],
#           "status": "",
#           ("service": service)
#       }
def initializes_sla(service_instance):
    try:
        LOG.info("Lifecycle-Management: sla_adapter: initializes_sla: " + str(service_instance))

        # 1. SLA MANAGER -> INITIALIZES_SLA(SERVICE, RESOURCES)
        # The Lifecycle calls the SLA Management to initialize all the SLA processes.
        return cimi.initializes_sla(service_instance)
    except:
        LOG.error('Lifecycle-Management: sla_adapter: initializes_sla: Exception')
        return None