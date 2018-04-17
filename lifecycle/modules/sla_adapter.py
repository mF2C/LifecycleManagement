"""
SLA adapter
This is being developed for the MF2C Project: http://www.mf2c-project.eu/

Copyright: Atos Research and Innovation, 2017.

This code is licensed under an Apache 2.0 license. Please, refer to the LICENSE.TXT file for more information

Created on 09 feb. 2018

@author: Roi Sucasas - ATOS
"""

import lifecycle.mF2C.mf2c as mf2c
from lifecycle.utils.logs import LOG


# initialize all the SLA processes
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
#
#   SLA
#   {
#     "id": "a02",
#     "name": "Agreement 02",
#     "state": "stopped",
#     "text":{
#         "id": "a02",
#         "type": "agreement",
#         "name": "Agreement 02",
#         "provider": { "id": "mf2c", "name": "mF2C Platform" },
#         "client": { "id": "c02", "name": "A client" },  <== del service instance
#         "creation": "2018-01-16T17:09:45Z",
#         "expiration": "2019-01-17T17:09:45Z",
#         "guarantees": [
#             {
#                 "name": "TestGuarantee",
#                 "constraints": "[test_value] < 10"
#             }
#         ]
#     }
#   }
def initializes_sla(service_instance):
    try:
        LOG.info("Lifecycle-Management: sla_adapter: initializes_sla: " + str(service_instance))
        LOG.warn("Lifecycle-Management: sla_adapter: initializes_sla not implemented ")

        # 1. SLA MANAGER -> INITIALIZES_SLA(SERVICE, RESOURCES)
        # The Lifecycle calls the SLA Management to initialize all the SLA processes.
        service_instance['agreement_id'] = "sla_agreement_id_test_001" # TODO mf2c.initializes_sla(service_instance)

        return service_instance
    except:
        LOG.error('Lifecycle-Management: sla_adapter: initializes_sla: Exception')
        return None