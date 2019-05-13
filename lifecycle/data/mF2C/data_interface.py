"""
CIMI - Data management
This is being developed for the MF2C Project: http://www.mf2c-project.eu/

Copyright: Atos Research and Innovation, 2017.

This code is licensed under an Apache 2.0 license. Please, refer to the LICENSE.TXT file for more information

Created on 09 feb. 2018

@author: Roi Sucasas - ATOS
"""

import lifecycle.data.mF2C.cimi as cimi
import lifecycle.data.app.service_instance as service_instance
from lifecycle.logs import LOG


###############################################################################
# COMMON

# FUNCTION: get_current_device_id
def __get_current_device_id():
    LOG.info("[lifecycle.data.mf2c.data_interface] [__get_current_device_id] Getting 'my' device ID ...")

    agent = cimi.get_agent_info()
    LOG.debug("[lifecycle.data.mf2c.data_interface] [__get_current_device_id] agent=" + str(agent))

    if not agent is None and agent != -1:
        LOG.info("[lifecycle.data.mf2c.data_interface] [__get_current_device_id] Returning 'my' device ID = " + agent['device_id'] + " ...")
        return agent['device_id']
    else:
        return -1


# FUNCTION: get_agent
def __get_agent():
    LOG.info("[lifecycle.data.mf2c.data_interface] [__get_agent] Getting 'my' device ID ...")

    agent = cimi.get_agent_info()
    LOG.debug("[lifecycle.data.mf2c.data_interface] [__get_agent] agent=" + str(agent))

    if not agent is None and agent != -1:
        return agent
    else:
        return None


# FUNCTION: get_my_ip: Get 'my' ip address
def get_my_ip():
    agent = __get_agent()
    if agent is not None:
        LOG.info("[lifecycle.data.mf2c.data_interface] [get_my_ip] IP from current agent = " + agent['device_ip'])
        return agent['device_ip']
    else:
        LOG.error("[lifecycle.data.mf2c.data_interface] [get_my_ip] Error retrieving IP from agent. Returning None ...")
        return None


# FUNCTION: get_leader_ip: Get leader ip address
def get_leader_ip():
    agent = __get_agent()
    if agent is not None:
        LOG.info("[lifecycle.data.mf2c.data_interface] [get_leader_ip] LEADER IP from current agent = " + agent['leader_ip'])
        return agent['leader_ip']
    else:
        LOG.error("[lifecycle.data.mf2c.data_interface] [get_leader_ip] Error retrieving LEADER IP from agent. Returning None ...")
        return None


# FUNCTION: get_agent
def get_agent():
    return cimi.get_agent()


###############################################################################
# USER MANAGEMENT

# get_um_profile: Get um_profile
def get_um_profile():
    LOG.debug("[lifecycle.data.mf2c.data_interface] [get_um_profile] Getting information about current user and device...")
    # get 'my' device_id
    device_id = __get_current_device_id()
    if device_id == -1:
        return None
    else:
        return cimi.get_user_profile_by_device(device_id)


# get_um_sharing_model: Get sharing_model
def get_um_sharing_model():
    LOG.debug("[lifecycle.data.mf2c.data_interface] [get_um_sharing_model] Getting information about current user and device...")
    # get 'my' device_id
    device_id = __get_current_device_id()
    if device_id == -1:
        return None
    else:
        return cimi.get_sharing_model_by_device(device_id)


###############################################################################
# SERVICE
# get_service_instance: Get service
def get_service(service_id):
    LOG.debug("[lifecycle.data.mf2c.data_interface] [get_service] get_service: " + service_id)
    return cimi.get_service_by_id(service_id)


###############################################################################
# SERVICE INSTANCE
# get_service_instance: Get service instance
def get_service_instance(service_instance_id, obj_response_cimi=None):
    LOG.debug("[lifecycle.data.mf2c.data_interface] [get_service_instance] get_service_instance: " + service_instance_id)
    return cimi.get_service_instance_by_id(service_instance_id)


# get_service_instance: Get service instance
def get_service_instance_report(service_instance_id):
    LOG.debug("[lifecycle.data.mf2c.data_interface] [get_service_instance_report] " + service_instance_id)
    return cimi.get_service_instance_report(service_instance_id)


# get_all_service_instances: Get all service instances
def get_all_service_instances(obj_response_cimi=None):
    LOG.debug("[lifecycle.data.mf2c.data_interface] [get_all_service_instances] get_all_service_instances")
    return cimi.get_all_service_instances()


# del_service_instance: Delete service instance
def del_service_instance(service_instance_id, obj_response_cimi=None):
    LOG.debug("[lifecycle.data.mf2c.data_interface] [del_service_instance] del_service_instance: " + service_instance_id)
    return cimi.del_service_instance_by_id(service_instance_id)


# del_all_service_instances: Delete all service instances
def del_all_service_instances():
    LOG.debug("[lifecycle.data.mf2c.data_interface] [del_all_service_instances] Deleting all  service instances ... ")
    return cimi.del_all_service_instances()


# create_service_instance: Creates a new service instance
#   IN: 1. service
#       2. [{"agent_ip": "192.168.252.41", "num_cpus": 4, "master_compss": false},
#           {"agent_ip": "192.168.252.43", "num_cpus": 2, "master_compss": true}] TODO: IPs list until landscaper is ready
#       3. user_id
#       4. agreement_id
#   OUT: service_instance dict
def create_service_instance(service, agents_list, user_id, agreement_id):
    LOG.debug("[lifecycle.data.mf2c.data_interface] [create_service_instance] Adding new resource to service instances [" +
              service['name'] + ", " + str(agents_list) + ", " + str(user_id) + ", " + str(agreement_id) + "] ...")

    if len(agents_list) == 0:
        new_service_instance = service_instance.new_empty_service_instance(service, user_id, agreement_id)
    else:
        new_service_instance = service_instance.new_service_instance(service, agents_list, user_id, agreement_id)

    LOG.debug("[lifecycle.data.mf2c.data_interface] [create_service_instance] adding service_intance to CIMI ...")
    res = cimi.add_service_instance(new_service_instance, user_id)

    if not res:
        LOG.error("[lifecycle.data.mf2c.data_interface] [create_service_instance] Error during the creation of the service_instance object")
        return new_service_instance
    return res


# update_service_instance: Updates a service instance
#       service_instance_id = "service-instance/250af452-959f-4ac6-9b06-54f757b46bf0"
def update_service_instance(service_instance_id, service_instance):
    LOG.debug("[lifecycle.data.mf2c.data_interface] [update_service_instance] Updating resource ... (" + service_instance_id + ", " + str(service_instance) + ")")
    res = cimi.update_service_instance(service_instance_id, service_instance)
    if not res:
        LOG.error("[lifecycle.data.mf2c.data_interface] [update_service_instance] Error during the edition of the service_instance object")
        return None
    return res

