"""
Generic data adapter
This is being developed for the MF2C Project: http://www.mf2c-project.eu/

Copyright: Atos Research and Innovation, 2017.

This code is licensed under an Apache 2.0 license. Please, refer to the LICENSE.TXT file for more information

Created on 10 mayo 2019

@author: Roi Sucasas - ATOS
"""

import config
from lifecycle.logs import LOG
from lifecycle.data.common import db as db
from lifecycle.data.standalone import data_interface as data_standalone
from lifecycle.data.standalone import lm_db as lm_db
from lifecycle.connectors.atos import user_manager as user_manager


# Data adapter class
class StandaloneDataAdapter:

    ###############################################################################
    # COMMON

    # get_my_ip: Get IP address from local
    def get_my_ip(self):
        LOG.warning("[lifecycle.data.standalone_data_adapter] [get_my_ip] not implemented. Returning value of 'HOST_IP' ...")
        return config.dic['HOST_IP']


    # get_host_ip: Get IP address from local
    def get_host_ip(self):
        return config.dic['HOST_IP']


    # get_leader_ip: Get IP address from Leader
    def get_leader_ip(self):
        LOG.warning("[lifecycle.data.standalone_data_adapter] [get_leader_ip] not implemented")
        return None


    # get_agent
    def get_agent(self):
        LOG.warning("[lifecycle.data.standalone_data_adapter] [get_agent] not implemented")
        return None


    ###############################################################################
    # USER MANAGEMENT

    # get_um_profile: Get um_profile
    def get_um_profile(self):
        um_res = user_manager.get_user_profile()
        if um_res is not None:
            return um_res['user_profile']
        else:
            return None


    # get_um_sharing_model: Get sharing_model
    def get_um_sharing_model(self):
        um_res = user_manager.get_sharing_model()
        if um_res is not None:
            return um_res['sharing_model']
        else:
            return None


    # get_check_swarm: checks if device can run swarm apps
    def get_check_swarm(self):
        LOG.warning("[lifecycle.data.standalone_data_adapter] [get_check_swarm] not implemented")
        return None


    ###############################################################################
    # SERVICE

    # get_service: Get service
    def get_service(self, service_id):
        LOG.warning("[lifecycle.data.standalone_data_adapter] [get_service] not implemented")
        return None


    ###############################################################################
    # SERVICE INSTANCE

    # get_service_instance: Gets the service instance
    def get_service_instance(self, service_instance_id, obj_response_cimi=None):
        return data_standalone.get_service_instance(service_instance_id)


    # get_service_instance_report: Gets the service instance report
    def get_service_instance_report(self, service_instance_id):
        LOG.warning("[lifecycle.data.standalone_data_adapter] [get_service_instance_report] not implemented")
        return None


    # get_all_service_instances: Gets all service instances
    def get_all_service_instances(self, obj_response_cimi=None):
        return data_standalone.get_all_service_instances()


    # del_service_instance: Deletes service instance
    def del_service_instance(self, service_instance_id, obj_response_cimi=None):
        return data_standalone.del_service_instance(service_instance_id)


    # del_all_service_instances: Deletes all service instances
    def del_all_service_instances(self):
        LOG.warning("[lifecycle.data.standalone_data_adapter] [del_all_service_instances] not implemented")
        return None


    # create_service_instance: Creates a new service instance
    def create_service_instance(self, service, agents_list, user_id, agreement_id):
        return data_standalone.create_service_instance(service, agents_list, user_id, agreement_id)


    # update_service_instance: Updates a service instance
    def update_service_instance(self, service_instance_id, service_instance):
        LOG.warning("[lifecycle.data.standalone_data_adapter] [update_service_instance] not implemented")
        return None


    # serv_instance_get_appid_from_master:
    def serv_instance_get_appid_from_master(self, service_instance):
        LOG.warning("[lifecycle.data.standalone_data_adapter] [serv_instance_get_appid_from_master] not implemented")
        return None


    # serv_instance_store_appid_in_master:
    def serv_instance_store_appid_in_master(self, service_instance, appId):
        LOG.warning("[lifecycle.data.standalone_data_adapter] [serv_instance_store_appid_in_master] not implemented")
        return None


    # serv_instance_is_master:
    def serv_instance_is_master(self, agent):
        LOG.warning("[lifecycle.data.standalone_data_adapter] [serv_instance_is_master] not implemented")
        return None


    # serv_instance_find_master:
    def serv_instance_find_master(self, service_instance):
        LOG.warning("[lifecycle.data.standalone_data_adapter] [serv_instance_find_master] not implemented")
        return None


    # serv_instance_is_agent_in_service_instance:
    def serv_instance_is_agent_in_service_instance(self, service_instance, agent_url):
        LOG.warning("[lifecycle.data.standalone_data_adapter] [serv_instance_is_agent_in_service_instance] not implemented")
        return None


    # serv_instance_replace_service_instance_agents:
    def serv_instance_replace_service_instance_agents(self, service_instance, service, user_id, sla_template_id, agents_list):
        LOG.warning("[lifecycle.data.standalone_data_adapter] [serv_instance_replace_service_instance_agents] not implemented")
        return None


    ###############################################################################

    # db_init: initialize elements
    def db_init(self):
        lm_db.init()
        db.init()


    # db_get_elem_from_list:
    def db_get_elem_from_list(self, container_main_id):
        return db.get_elem_from_list(container_main_id)


    # db_save_port
    def db_save_port_mapped(self, port, mapped_to):
        return db.save_to_DB_DOCKER_PORTS(port, mapped_to)


    # db_get_port_mapped
    def db_get_port_mapped(self, port):
        return db.get_from_DB_DOCKER_PORTS(port)


    # db_get_compss_port
    def db_get_compss_port(self, lports):
        return db.get_COMPSs_port_DB_DOCKER_PORTS(lports)


    # db_delete_port
    def db_delete_port(self, port):
        return db.del_from_DB_DOCKER_PORTS(port)