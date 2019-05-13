"""
Service instance - Data management
This is being developed for the MF2C Project: http://www.mf2c-project.eu/

Copyright: Atos Research and Innovation, 2017.

This code is licensed under an Apache 2.0 license. Please, refer to the LICENSE.TXT file for more information

Created on 28 feb. 2019

@author: Roi Sucasas - ATOS
"""

from lifecycle.logs import LOG
from lifecycle.common import STATUS_CREATED_NOT_INITIALIZED, STATUS_STARTED
from lifecycle.data import data_adapter as data_adapter


# new_service_instance: Creates a new service instance object
#   IN: 1. service
#       2. [{"agent_ip": "192.168.252.41", "num_cpus": 4, "master_compss": false},
#           {"agent_ip": "192.168.252.43", "num_cpus": 2, "master_compss": true}] TODO: IPs list until landscaper is ready
#       3. user_id
#       4. agreement_id
#   OUT: service_instance dict
def new_service_instance(service, agents_list, user_id, agreement_id):
    LOG.debug("[lifecycle.data.app.service_instance] [new_service_instance] " + service['name'] + ", " + str(agents_list) + ", " + str(user_id) + ", " + str(agreement_id))

    # create list of agents
    list_of_agents = []

    # ports:
    ports_l = []
    try:
        ports_l = service['exec_ports']
    except:
        LOG.warning("[lifecycle.data.app.service_instance] [new_service_instance] No ports values found in service definition")

    # AGENTs:
    i = 0
    for agent in agents_list:
        if len(agents_list) == 1 or i == 0:
            master_compss = True
        else:
            master_compss = False
        # Add new AGENT to list
        list_of_agents.append({"agent":         {"href": "agent/default-value"},
                               "app_type":      service['exec_type'],
                               "ports":         ports_l,
                               "url":           agent['agent_ip'],
                               "status":        STATUS_CREATED_NOT_INITIALIZED,
                               "num_cpus":      1,
                               "allow":         True,
                               "container_id":  "-",
                               "master_compss": master_compss,  # TODO master_compss... selected / final master
                               "agent_param":   "not-defined"}) # TODO agent_param... to store COMPSS operation ID
        i += 1

    # info from AGENT
    cimi_agent = data_adapter.get_agent()
    if cimi_agent is not None and cimi_agent != -1:
        if 'parent_device_id' not in cimi_agent:
            parent_device_id = "not-defined"
        else:
            parent_device_id = cimi_agent['parent_device_id']

        if 'parent_device_ip' not in cimi_agent:
            parent_device_ip = "not-defined"
        else:
            parent_device_ip = cimi_agent['parent_device_ip']

        # SERVICE_INSTANCE:
        new_service_instance = {
            "service": service['id'],
            "agreement": agreement_id,
            "user": user_id,
            "device_id": cimi_agent['device_id'],
            "device_ip": cimi_agent['device_ip'],
            "parent_device_id": parent_device_ip,
            "parent_device_ip": parent_device_id,
            "agents": list_of_agents,
            "service_type": service['exec_type'],
            "status": STATUS_CREATED_NOT_INITIALIZED
        }
    else:
        new_service_instance = {
            "service":          service['id'],
            "agreement":        agreement_id,
            "user":             user_id,
            "device_id":        "not-defined",
            "device_ip":        "not-defined",
            "parent_device_id": "not-defined",
            "parent_device_ip": "not-defined",
            "agents":           list_of_agents,
            "service_type":     service['exec_type'],
            "status":           STATUS_CREATED_NOT_INITIALIZED}

    LOG.debug("[lifecycle.data.app.service_instance] [new_service_instance] service_intance=" + str(new_service_instance))
    return new_service_instance


# new_empty_service_instance: Creates a new service instance object without agents
def new_empty_service_instance(service, user_id, agreement_id):
    LOG.debug("[lifecycle.data.app.service_instance] [new_empty_service_instance] " + service['name'] + ", " + str(user_id) + ", " + str(agreement_id))

    # SERVICE_INSTANCE:
    new_service_instance = {"service":          service['id'],
                            "agreement":        agreement_id,
                            "user":             user_id,
                            "device_id":        "not-defined",
                            "device_ip":        "not-defined",
                            "parent_device_id": "not-defined",
                            "parent_device_ip": "not-defined",
                            "agents":           [],
                            "service_type":     service['exec_type'],
                            "status":           STATUS_CREATED_NOT_INITIALIZED}

    LOG.debug("[lifecycle.data.app.service_instance] [new_empty_service_instance] new_service_instance=" + str(new_service_instance))
    return new_service_instance


# add_agents_to_empty_service_instance: Adds a list of agents to the service instance
def add_agents_to_empty_service_instance(service, user_id, agreement_id, agents_list):
    LOG.debug("[lifecycle.data.app.service_instance] [add_agents_to_empty_service_instance] " + service['name'] + ", " + str(user_id) + ", " + str(agreement_id))

    # SERVICE_INSTANCE:
    new_service_instance = {"service":          service['id'],
                            "agreement":        agreement_id,
                            "user":             user_id,
                            "device_id":        "not-defined",
                            "device_ip":        "not-defined",
                            "parent_device_id": "not-defined",
                            "parent_device_ip": "not-defined",
                            "agents":           [],
                            "service_type":     service['exec_type'],
                            "status":           STATUS_CREATED_NOT_INITIALIZED}

    LOG.debug("[lifecycle.data.app.service_instance] [add_agents_to_empty_service_instance] adding service_intance to CIMI ...")
    LOG.debug("[lifecycle.data.app.service_instance] [add_agents_to_empty_service_instance] new_service_instance=" + str(new_service_instance))

    return new_service_instance


# is_agent_in_service_instance: check if an agent (url) is being used in a service_instance
def is_agent_in_service_instance(service_instance, agent_url):
    LOG.debug("[lifecycle.data.app.service_instance] [is_agent_in_service_instance] " + service_instance['id'] + ", " + str(agent_url))
    for agent in service_instance['agents']:
        if agent['url'] == agent_url:
            return True
    return False


# set_master:
def __set_master(service_instance):
    try:
        LOG.debug("[lifecycle.data.app.service_instance] [__set_master] Update service instance: set master (COMPSs)")
        data_adapter.update_service_instance(service_instance['id'], service_instance)
    except:
        LOG.exception("[lifecycle.data.app.service_instance] [__set_master] Exception")


# find_master:
def find_master(service_instance):
    try:
        LOG.debug("[lifecycle.data.app.service_instance] [find_master] Check if local agent has COMPSs and is included in the service instance ...")

        for agent in service_instance['agents']:
            if agent['master_compss'] and agent['status'] == STATUS_STARTED:
                LOG.debug("[lifecycle.data.app.service_instance] [find_master] Agent is master, status=STARTED: " + str(agent))
                return agent

        for agent in service_instance['agents']:
            if agent['status'] == STATUS_STARTED and agent['url'] == data_adapter.get_my_ip(): #common.get_local_ip():
                LOG.debug("[lifecycle.data.app.service_instance] [find_master] Local agent has COMPSs, status=STARTED and is included in the service instance!")
                LOG.debug("[lifecycle.data.app.service_instance] [find_master] agent: " + str(agent))
                agent['master_compss'] = True
                __set_master(service_instance)
                return agent

        LOG.debug("[lifecycle.data.app.service_instance] [find_master] Check agents included in the service instance and status=STARTED ...")
        for agent in service_instance['agents']:
            if agent['status'] == STATUS_STARTED:
                LOG.debug("[lifecycle.data.app.service_instance] [find_master] agent: " + str(agent))
                agent['master_compss'] = True
                __set_master(service_instance)
                return agent
    except:
        LOG.exception("[lifecycle.data.app.service_instance] [find_master] Exception")

    LOG.warning("[lifecycle.data.app.service_instance] [find_master] return service_instance['agents'][0]: " + str(service_instance['agents'][0]))
    return service_instance['agents'][0]


# is_master:
def is_master(agent):
    if agent['master_compss']:
        return True
    return False


# store_appid_in_master:
def store_appid_in_master(service_instance, appId):
    try:
        LOG.debug("[lifecycle.data.app.service_instance] [store_appid_in_master] Storing appId [" + str(appId) + "] in the service instance ...")

        for agent in service_instance['agents']:
            if agent['master_compss']:
                LOG.debug("[lifecycle.data.app.service_instance] [store_appid_in_master] Agent is master: " + str(agent))
                agent['agent_param'] = str(appId)
                res = data_adapter.update_service_instance(service_instance['id'], service_instance)
                LOG.debug("[lifecycle.data.app.service_instance] [store_appid_in_master] res=" + res + ", agent=" + str(agent))
                return True
    except:
        LOG.exception("[lifecycle.data.app.service_instance] [store_appid_in_master] Exception")
    return False


# get_appid_from_master:
def get_appid_from_master(service_instance):
    try:
        LOG.debug("[lifecycle.data.app.service_instance] [get_appid_from_master] Getting (COMPSs) appId from the service instance ...")

        for agent in service_instance['agents']:
            if agent['master_compss']:
                LOG.debug("[lifecycle.data.app.service_instance] [get_appid_from_master] Agent is master: " + str(agent))
                return agent['agent_param']
    except:
        LOG.exception("[lifecycle.data.app.service_instance] [get_appid_from_master] Exception. Returning None ...")
    return None