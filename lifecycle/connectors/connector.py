"""
Interactions with other mF2C components
This is being developed for the MF2C Project: http://www.mf2c-project.eu/

Copyright: Roi Sucasas Font, Atos Research and Innovation, 2017.

This code is licensed under an Apache 2.0 license. Please, refer to the LICENSE.TXT file for more information

Created on 10 may. 2019

@author: Roi Sucasas - ATOS
"""

from lifecycle.connectors import mf2c_connector as mf2c_connector
from lifecycle.connectors import standalone_connector as standalone_connector
from lifecycle.logs import LOG


# data adapterr
conn = None


# set adapter
def init(lm_mode):
    global conn

    LOG.info('[lifecycle.connectors.connector] [init] Setting connector...')
    if lm_mode == "DEFAULT" or lm_mode == "MF2C":
        LOG.info('[lifecycle.connectors.connector] [init] LM_MODE = MF2C')
        conn = mf2c_connector.Mf2cConnector()
    else:
        LOG.info('[lifecycle.connectors.connector] [init] LM_MODE = STANDALONE')
        conn = standalone_connector.StandaloneConnector()


# SLA MANAGER #
# create_sla_agreement: create SLA agreement
def create_sla_agreement(template_id, user_id, service):
    return conn.create_sla_agreement(template_id, user_id, service)


# start_sla_agreement: start SLA agreement
def sla_start_agreement(agreement_id):
    return conn.sla_start_agreement(agreement_id)


# sla_stop_agreement
def sla_stop_agreement(agreement_id):
    return conn.sla_stop_agreement(agreement_id)


# sla_terminate_agreement
def sla_terminate_agreement(agreement_id):
    return conn.sla_terminate_agreement(agreement_id)


# USER MANAGEMENT
# user_management_check_avialability: call to local UM to check if it's possible to deploy a service
def user_management_check_avialability():
    return conn.user_management_check_avialability()


# user_management_get_current: call to local UM to get current values (user, device)
def user_management_get_current(val):
    return conn.user_management_get_current(val)


# user_management_set_um_properties: call to lifceycle from other agent in order to update user management properties
def user_management_set_um_properties(apps=0):
    return conn.user_management_set_um_properties(apps)


# LIFECYCLE
# lifecycle_parent_deploy: call to parent's lifceycle; forwards a "submit service" request
def lifecycle_parent_deploy(leader_ip, service_id, user_id, sla_template_id, service_instance_id):
    return conn.lifecycle_parent_deploy(leader_ip, service_id, user_id, sla_template_id, service_instance_id)


# lifecycle_deploy: call to lifceycle from other agent in order to deploy a service
def lifecycle_deploy(service, service_instance, agent):
    return conn.lifecycle_deploy(service, service_instance, agent)


# lifecycle_operation: call to lifceycle from other agent in order to start/stop... a service
def lifecycle_operation(service, agent, operation):
    return conn.lifecycle_operation(service, agent, operation)


# lifecycle_um_info: call to lifceycle from other agent in order to get sharing model and user profile
def lifecycle_um_check_avialability(agent):
    return conn.lifecycle_um_check_avialability(agent)


# lifecycle_um_info: call to lifceycle from other agent in order to get sharing model and user profile
def lifecycle_check_agent_swarm(agent):
    return conn.lifecycle_check_agent_swarm(agent)


# LANDSCAPER / RECOMMENDER
# get_available_devices: Get available devices
def get_available_devices(service):
    return conn.get_available_devices(service)


# SERVICE MANAGER
# qos_providing
def qos_providing(service_instance):
    return conn.qos_providing(service_instance)