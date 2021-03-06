"""
StandaloneConnector: Interactions with other X components
This is being developed for the MF2C Project: http://www.mf2c-project.eu/

Copyright: Roi Sucasas Font, Atos Research and Innovation, 2017.

This code is licensed under an Apache 2.0 license. Please, refer to the LICENSE.TXT file for more information

Created on 10 may. 2019

@author: Roi Sucasas - ATOS
"""

from lifecycle.connectors.atos import sla_manager as sla_manager
from lifecycle.connectors.atos import user_manager as user_manager
from lifecycle.connectors.atos import lifecycle as lifecycle
from lifecycle.logs import LOG


# Components connector class
class StandaloneConnector:

    # SLA MANAGER #
    # create_sla_agreement: create SLA agreement
    def create_sla_agreement(self, template_id, user_id, service):
        return sla_manager.create_sla_agreement(template_id, user_id, service)


    # start_sla_agreement: start SLA agreement
    def sla_start_agreement(self, agreement_id):
        return sla_manager.start_agreement(agreement_id)


    # sla_stop_agreement
    def sla_stop_agreement(self, agreement_id):
        return sla_manager.stop_agreement(agreement_id)


    # sla_terminate_agreement
    def sla_terminate_agreement(self, agreement_id):
        return sla_manager.terminate_agreement(agreement_id)


    # USER MANAGEMENT
    # user_management_check_avialability: call to local UM to check if it's possible to deploy a service
    def user_management_check_avialability(self):
        return user_manager.check_avialability()


    # user_management_get_current: call to local UM to get current values (user, device)
    def user_management_get_current(self, val):
        return user_manager.get_current(val)


    # user_management_set_um_properties: call to lifceycle from other agent in order to update user management properties
    def user_management_set_um_properties(self, apps=0):
        return user_manager.set_um_properties(apps)


    # LIFECYCLE
    # lifecycle_parent_deploy: call to parent's lifceycle; forwards a "submit service" request
    def lifecycle_parent_deploy(self, leader_ip, service_id, user_id, sla_template_id, service_instance_id):
        return lifecycle.parent_deploy(leader_ip, service_id, user_id, sla_template_id, service_instance_id)


    # lifecycle_deploy: call to lifceycle from other agent in order to deploy a service
    def lifecycle_deploy(self, service, service_instance, agent):
        return lifecycle.deploy(service, service_instance, agent)


    # lifecycle_operation: call to lifceycle from other agent in order to start/stop... a service
    def lifecycle_operation(self, service, agent, operation):
        return lifecycle.operation(service, agent, operation)


    # lifecycle_um_info: call to lifceycle from other agent in order to get sharing model and user profile
    def lifecycle_um_check_avialability(self, agent):
        return lifecycle.um_check_avialability(agent)


    # lifecycle_um_info: call to lifceycle from other agent in order to get sharing model and user profile
    def lifecycle_check_agent_swarm(self, agent):
        return lifecycle.check_agent_swarm(agent)


    # LANDSCAPER / RECOMMENDER
    # get_available_devices: Get available devices
    def get_available_devices(self, service):
        LOG.warning("[lifecycle.connectors.standalone_connector] [get_available_devices] not implemented")
        return None


    # SERVICE MANAGER
    # qos_providing
    def qos_providing(self, service_instance):
        LOG.warning("[lifecycle.connectors.standalone_connector] [qos_providing] not implemented")
        return None