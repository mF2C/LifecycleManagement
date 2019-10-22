"""
Data adapter for MF2C project
This is being developed for the MF2C Project: http://www.mf2c-project.eu/

Copyright: Atos Research and Innovation, 2017.

This code is licensed under an Apache 2.0 license. Please, refer to the LICENSE.TXT file for more information

Created on 10 mayo 2019

@author: Roi Sucasas - ATOS
"""

from lifecycle.data.mF2C import data_interface as data_mf2c, service_instance as si
from lifecycle.modules.apps.swarm import adapter as swarm_adapter
from lifecycle.data.common import db as db


# Data adapter class
class Mf2cDataAdapter:

    ###############################################################################
    # COMMON

    # get_my_ip: Get IP address from local
    def get_my_ip(self):
        return data_mf2c.get_my_ip()


    # get_host_ip: Get IP address from local
    def get_host_ip(self):
        return data_mf2c.get_my_ip()


    # get_leader_ip: Get IP address from Leader
    def get_leader_ip(self):
        return data_mf2c.get_leader_ip()


    # get_agent:
    def get_agent(self):
        return data_mf2c.get_agent()


    ###############################################################################
    # USER MANAGEMENT

    # get_um_profile: Get um_profile
    def get_um_profile(self):
        return data_mf2c.get_um_profile()


    # get_um_sharing_model: Get sharing_model
    def get_um_sharing_model(self):
        return data_mf2c.get_um_sharing_model()


    # get_check_swarm: checks if device can run swarm apps
    def get_check_swarm(self):
        return swarm_adapter.is_swarm_node()


    ###############################################################################
    # SERVICE

    # get_service: Get service
    def get_service(self, service_id):
        return data_mf2c.get_service(service_id)


    ###############################################################################
    # SERVICE INSTANCE

    # get_service_instance: Gets the service instance
    def get_service_instance(self, service_instance_id, obj_response_cimi=None):
        return data_mf2c.get_service_instance(service_instance_id, obj_response_cimi)


    # get_service_instance_report: Gets the service instance report
    def get_service_instance_report(self, service_instance_id):
        service_instance = self.get_service_instance(service_instance_id)
        if service_instance is not None:
            appId = self.serv_instance_get_appid_from_master(service_instance)
            if appId is not None:
                return data_mf2c.get_service_instance_report(appId)
        return None


    # get_all_service_instances: Gets all service instances
    def get_all_service_instances(self, obj_response_cimi=None):
        return data_mf2c.get_all_service_instances(obj_response_cimi)


    # del_service_instance: Deletes service instance
    def del_service_instance(self, service_instance_id, obj_response_cimi=None):
        return data_mf2c.del_service_instance(service_instance_id, obj_response_cimi)


    # del_all_service_instances: Deletes all service instances
    def del_all_service_instances(self):
        return data_mf2c.del_all_service_instances()


    # create_service_instance: Creates a new service instance
    def create_service_instance(self, service, agents_list, user_id, agreement_id):
        return data_mf2c.create_service_instance(service, agents_list, user_id, agreement_id)


    # update_service_instance: Updates a service instance
    def update_service_instance(self, service_instance_id, service_instance):
        return data_mf2c.update_service_instance(service_instance_id, service_instance)


    # serv_instance_get_appid_from_master:
    def serv_instance_get_appid_from_master(self, service_instance):
        return si.get_appid_from_master(service_instance)


    # serv_instance_store_appid_in_master:
    def serv_instance_store_appid_in_master(self, service_instance, appId):
        return si.store_appid_in_master(service_instance, appId)


    # serv_instance_is_master:
    def serv_instance_is_master(self, agent):
        return si.is_master(agent)


    # serv_instance_find_master:
    def serv_instance_find_master(self, service_instance):
        return si.find_master(service_instance)


    # serv_instance_is_agent_in_service_instance:
    def serv_instance_is_agent_in_service_instance(self, service_instance, agent_url):
        return si.is_agent_in_service_instance(service_instance, agent_url)


    # serv_instance_replace_service_instance_agents:
    def serv_instance_replace_service_instance_agents(self, service_instance, service, user_id, sla_template_id, agents_list):
        return si.replace_service_instance_agents(service_instance, service, user_id, sla_template_id, agents_list)


    ###############################################################################

    # db_init: initialize elements
    def db_init(self):
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