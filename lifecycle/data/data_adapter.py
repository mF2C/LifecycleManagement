"""
CIMI - Data management
This is being developed for the MF2C Project: http://www.mf2c-project.eu/

Copyright: Atos Research and Innovation, 2017.

This code is licensed under an Apache 2.0 license. Please, refer to the LICENSE.TXT file for more information

Created on 09 feb. 2018

@author: Roi Sucasas - ATOS
"""

from lifecycle.data import mf2c_data_adapter as mf2c_data_adapter
from lifecycle.data import standalone_data_adapter as standalone_data_adapter
from lifecycle.logs import LOG


# data adapterr
adapter = None


# set adapter
def init(lm_mode):
    global adapter

    LOG.info('[lifecycle.data.data_adapter] [init] Setting data adapter...')
    if lm_mode == "DEFAULT" or lm_mode == "MF2C":
        LOG.info('[lifecycle.data.data_adapter] [init] LM_MODE = MF2C')
        adapter = mf2c_data_adapter.Mf2cDataAdapter()
    else:
        LOG.info('[lifecycle.data.data_adapter] [init] LM_MODE = STANDALONE')
        adapter = standalone_data_adapter.StandaloneDataAdapter()


###############################################################################
# COMMON

# get_my_ip: Get IP address from local
def get_my_ip():
    return adapter.get_my_ip()


# get_leader_ip: Get IP address from Leader
def get_leader_ip():
    return adapter.get_leader_ip()


# get_agent:
def get_agent():
    return adapter.get_agent()


###############################################################################
# USER MANAGEMENT

# get_um_profile: Get um_profile
def get_um_profile():
    return adapter.get_um_profile()


# get_um_sharing_model: Get sharing_model
def get_um_sharing_model():
    return adapter.get_um_sharing_model()


# get_check_swarm: checks if device can run swarm apps
def get_check_swarm():
    return adapter.get_check_swarm()


###############################################################################
# SERVICE

# get_service: Get service
def get_service(service_id):
    return adapter.get_service(service_id)


###############################################################################
# SERVICE INSTANCE

# get_service_instance: Gets the service instance
def get_service_instance(service_instance_id, obj_response_cimi=None):
    return adapter.get_service_instance(service_instance_id, obj_response_cimi)


# get_service_instance_report: Gets the service instance report
def get_service_instance_report(service_instance_id):
    return adapter.get_service_instance_report(service_instance_id)


# get_all_service_instances: Gets all service instances
def get_all_service_instances(obj_response_cimi=None):
    return adapter.get_all_service_instances(obj_response_cimi)


# del_service_instance: Deletes service instance
def del_service_instance(service_instance_id, obj_response_cimi=None):
    return adapter.del_service_instance(service_instance_id, obj_response_cimi)


# del_all_service_instances: Deletes all service instances
def del_all_service_instances():
    return adapter.del_all_service_instances()


# create_service_instance: Creates a new service instance
def create_service_instance(service, agents_list, user_id, agreement_id):
    return adapter.create_service_instance(service, agents_list, user_id, agreement_id)


# update_service_instance: Updates a service instance
def update_service_instance(service_instance_id, service_instance):
    return adapter.update_service_instance(service_instance_id, service_instance)


# serv_instance_get_appid_from_master:
def serv_instance_get_appid_from_master(service_instance):
    return adapter.serv_instance_get_appid_from_master(service_instance)


# serv_instance_store_appid_in_master:
def serv_instance_store_appid_in_master(service_instance, appId):
    return adapter.serv_instance_store_appid_in_master(service_instance, appId)


# serv_instance_is_master:
def serv_instance_is_master(agent):
    return adapter.serv_instance_is_master(agent)


# serv_instance_find_master:
def serv_instance_find_master(service_instance):
    return adapter.serv_instance_find_master(service_instance)


# serv_instance_is_agent_in_service_instance:
def serv_instance_is_agent_in_service_instance(service_instance, agent_url):
    return adapter.serv_instance_is_agent_in_service_instance(service_instance, agent_url)


# serv_instance_add_agents_to_empty_service_instance:
def serv_instance_add_agents_to_empty_service_instance(service, user_id, agreement_id, agents_list):
    return adapter.serv_instance_add_agents_to_empty_service_instance(service, user_id, agreement_id, agents_list)


# serv_instance_add_agents_to_empty_service_instance:
def serv_instance_new_empty_service_instance(service, user_id, agreement_id):
    return adapter.serv_instance_new_empty_service_instance(service, user_id, agreement_id)


###############################################################################

# db_init: initialize elements
def db_init():
    return adapter.db_init()


# db_get_elem_from_list:
def db_get_elem_from_list(container_main_id):
    return adapter.db_get_elem_from_list(container_main_id)


# db_save_port
def db_save_port_mapped(port, mapped_to):
    return adapter.db_save_port_mapped(port, mapped_to)


# db_get_port_mapped
def db_get_port_mapped(port):
    return adapter.db_get_port_mapped(port)


# db_get_compss_port
def db_get_compss_port(lports):
    return adapter.db_get_compss_port(lports)


# db_delete_port
def db_delete_port(port):
    return adapter.db_delete_port(port)