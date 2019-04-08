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
       "device_id": "",
	   "device_ip": "",
	   "parent_device_id": "",
	   "parent_device_ip": "",
       "service": "",
       "agreement": "",
       "status": "waiting",
       "service_type": "swarm",
       "agents": [
           {"agent": resource-link, "url": "192.168.1.31", "ports": [8081], "container_id": "10asd673f", "status": "waiting",
               "num_cpus": 3, "allow": true, "master_compss": true, "app_type": "swarm"},
           {"agent": resource-link, "url": "192.168.1.34", "ports": [8081], "container_id": "99asd673f", "status": "waiting",
               "num_cpus": 2, "allow": true, "master_compss": false, "app_type": "swarm"}
      ]
   }
'''


###############################################################################
# COMMON

# TODO get this information from new RESOURCE: AGENT
# get_current_device_id
def get_current_device_id():
    LOG.info("LIFECYCLE: Data: get_device_id: Getting 'my' device ID ...")

    device = cimi.get_current_device_info()
    LOG.debug("LIFECYCLE: Data: get_device_id: device = " + str(device))

    if not device is None and device != -1:
        LOG.info("LIFECYCLE: Data: get_device_id: Returning 'my' device ID = " + str(device['id']))
        return device['id']
    else:
        return -1


# Get 'my' ip address
def get_my_ip():
    my_device = get_current_device_id()
    if my_device is not None and my_device != -1:
        LOG.info("LIFECYCLE: Data: get_my_ip: IP from current device = " + my_device['ethernetAddress'])
        return my_device['ethernetAddress']
    else:
        LOG.error("LIFECYCLE: Data: get_my_ip: Error retrieving IP from device ...")
        return None


# exist_user: check if 'user id' exists
def exist_user(user_id):
    return cimi.exist_user(user_id)


# exist_device: check if 'device id' exists
def exist_device(device_id):
    return cimi.exist_device(device_id)



###############################################################################
# USER MANAGEMENT
# get_um_profile: Get um_profile
def get_um_profile():
    LOG.debug("LIFECYCLE: Data: get_current_user_profile: Getting information about current user and device...")
    # get 'my' device_id
    device_id = get_current_device_id()
    if device_id == -1:
        return None
    else:
        return cimi.get_user_profile_by_device(device_id)


# get_um_sharing_model: Get sharing_model
def get_um_sharing_model():
    LOG.debug("LIFECYCLE: Data: get_current_sharing_model: Getting information about current user and device...")
    # get 'my' device_id
    device_id = get_current_device_id()
    if device_id == -1:
        return None
    else:
        return cimi.get_sharing_model_by_device(device_id)


###############################################################################
# SERVICE
# get_service_instance: Get service
def get_service(service_id):
    LOG.debug("LIFECYCLE: Data: get_service: " + service_id)
    return cimi.get_service_by_id(service_id)


###############################################################################
# SERVICE INSTANCE
# get_service_instance: Get service instance
def get_service_instance(service_instance_id, obj_response_cimi=None):
    LOG.debug("LIFECYCLE: Data: get_service_instance: " + service_instance_id)
    return cimi.get_service_instance_by_id(service_instance_id, obj_response_cimi)


# get_service_instance: Get service instance
def get_service_instance_report(service_instance_id):
    LOG.debug("LIFECYCLE: Data: get_service_instance_report_by_id: " + service_instance_id)
    return cimi.get_service_instance_report(service_instance_id)


# get_all_service_instances: Get all service instances
def get_all_service_instances(obj_response_cimi=None):
    LOG.debug("LIFECYCLE: Data: get_all_service_instances")
    return cimi.get_all_service_instances(obj_response_cimi)


# del_service_instance: Delete service instance
def del_service_instance(service_instance_id, obj_response_cimi=None):
    LOG.debug("LIFECYCLE: Data: del_service_instance: " + service_instance_id)
    return cimi.del_service_instance_by_id(service_instance_id, obj_response_cimi)


# del_all_service_instances: Delete all service instances
def del_all_service_instances(obj_response_cimi=None):
    LOG.debug("LIFECYCLE: Data: del_all_service_instances")
    return cimi.del_all_service_instances(obj_response_cimi)


# create_service_instance: Creates a new service instance
#   IN: 1. service
#       2. [{"agent_ip": "192.168.252.41", "num_cpus": 4, "master_compss": false},
#           {"agent_ip": "192.168.252.43", "num_cpus": 2, "master_compss": true}] TODO: IPs list until landscaper is ready
#       3. user_id
#       4. agreement_id
#   OUT: service_instance dict
def create_service_instance(service, agents_list, user_id, agreement_id):
    LOG.debug("LIFECYCLE: Data: create_service_instance: " + str(service) + ", " + str(agents_list) + ", " + str(user_id) + ", " + str(agreement_id))

    if len(agents_list) == 0:
        new_service_instance = service_instance.new_empty_service_instance(service, user_id, agreement_id)
    else:
        new_service_instance = service_instance.new_service_instance(service, agents_list, user_id, agreement_id)

    res = cimi.add_service_instance(new_service_instance)

    if not res:
        LOG.error("LIFECYCLE: Data: create_service_instance: Error during the creation of the service_instance object")
        return new_service_instance
    return res


# update_service_instance: Updates a service instance
#       service_instance_id = "service-instance/250af452-959f-4ac6-9b06-54f757b46bf0"
def update_service_instance(service_instance_id, service_instance):
    LOG.debug("LIFECYCLE: Data: (1) update_service_instance: " + service_instance_id + ", " + str(service_instance))
    res = cimi.update_service_instance(service_instance_id, service_instance)
    LOG.debug("LIFECYCLE: Data: (2) update_service_instance: " + str(res))
    if not res:
        LOG.error("LIFECYCLE: Data: update_service_instance: Error during the edition of the service_instance object")
        return None
    return res


###############################################################################


# Get battery level
def get_power():
    # get 'my' device_id
    device_id = get_current_device_id()
    LOG.info("LIFECYCLE: Data: get_power: Getting power status from device [" + device_id + "] ...")
    return cimi.get_power(device_id)


# Get parent
def get_parent():
    # get 'my' device_id
    device_id = get_current_device_id()
    LOG.info("LIFECYCLE: Data: get_parent: Getting LEADER ID from device [" + device_id + "] ...")
    return cimi.get_parent(device_id)


# Get leader ip address
def get_leader_ip():
    parent = get_parent()
    if parent is not None and parent != -1:
        LOG.info("LIFECYCLE: Data: get_parent: LEADER IP from current device = " + parent['ethernetAddress'])
        return parent['ethernetAddress']
    else:
        LOG.error("LIFECYCLE: Data: get_parent: Error retrieving LEADER IP from device ...")
        return None