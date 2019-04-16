"""
CIMI - Data management
This is being developed for the MF2C Project: http://www.mf2c-project.eu/

Copyright: Atos Research and Innovation, 2017.

This code is licensed under an Apache 2.0 license. Please, refer to the LICENSE.TXT file for more information

Created on 09 feb. 2018

@author: Roi Sucasas - ATOS
"""

import lifecycle.data.mF2C.cimi as cimi
import lifecycle.data.service_instance as service_instance
from common.logs import LOG


'''
 Data managed by this component:
 SERVICE:
       {
           "name": "hello-world",
           "description": "Hello World Service",
           "resourceURI": "/hello-world",
           "exec": "hello-world",
           "exec_type": "docker",
           "exec_ports": ["8080", "8081"],
           "category": {
               "cpu": "low",
               "memory": "low",
               "storage": "low",
               "inclinometer": false,
               "temperature": false,
               "jammer": false,
               "location": false
           }
       }

 SERVICE INSTANCE:
   {
       ...
       "id": "",
       "user": "testuser",
       "service": "",
       "agreement": "",
       "status": "waiting",
       "agents": [
           {"agent": resource-link, "url": "192.168.1.31", "ports": [8081], "container_id": "10asd673f", "status": "waiting",
               "num_cpus": 3, "allow": true, "master_compss": true},
           {"agent": resource-link, "url": "192.168.1.34", "ports": [8081], "container_id": "99asd673f", "status": "waiting",
               "num_cpus": 2, "allow": true, "master_compss": false}
      ]
   }
'''


###############################################################################
# SERVICE INSTANCE
# get_service_instance: Get service instance
def get_service_instance(service_instance_id, obj_response_cimi=None):
    LOG.debug("Lifecycle-Management: Data: get_service_instance: " + service_instance_id)
    return cimi.get_service_instance_by_id(service_instance_id)


# get_all_service_instances: Get all service instances
def get_all_service_instances(obj_response_cimi=None):
    LOG.debug("Lifecycle-Management: Data: get_all_service_instances")
    return cimi.get_all_service_instances(obj_response_cimi)


# del_service_instance: Delete service instance
def del_service_instance(service_instance_id, obj_response_cimi=None):
    LOG.debug("Lifecycle-Management: Data: del_service_instance: " + service_instance_id)
    return cimi.del_service_instance_by_id(service_instance_id, obj_response_cimi)


# del_all_service_instances: Delete all service instances
def del_all_service_instances(obj_response_cimi=None):
    LOG.debug("Lifecycle-Management: Data: del_all_service_instances")
    return cimi.del_all_service_instances(obj_response_cimi)


# create_service_instance: Creates a new service instance
#   IN: 1. service
#       2. [{"agent_ip": "192.168.252.41", "num_cpus": 4, "master_compss": false},
#           {"agent_ip": "192.168.252.43", "num_cpus": 2, "master_compss": true}] TODO: IPs list until landscaper is ready
#       3. user_id
#       4. agreement_id
#   OUT: service_instance dict
def create_service_instance(service, agents_list, user_id, agreement_id):
    LOG.debug("Lifecycle-Management: Data: create_service_instance: " + str(service) + ", " + str(agents_list))

    new_service_instance = service_instance.new_service_instance(service, agents_list, user_id, agreement_id)

    res = cimi.add_service_instance(new_service_instance)
    if not res:
        LOG.error("Lifecycle-Management: Data: create_service_instance: Error during the creation of the service_instance object")
        return new_service_instance
    return res


# update_service_instance: Updates a service instance
#       service_instance_id = "service-instance/250af452-959f-4ac6-9b06-54f757b46bf0"
def update_service_instance(service_instance_id, service_instance):
    LOG.debug("Lifecycle-Management: Data: (1) update_service_instance: " + service_instance_id + ", " + str(service_instance))
    res = cimi.update_service_instance(service_instance_id, service_instance)
    LOG.debug("Lifecycle-Management: Data: (2) update_service_instance: " + str(res))
    if not res:
        LOG.error("Lifecycle-Management: Data: update_service_instance: Error during the edition of the service_instance object")
        return None
    return res