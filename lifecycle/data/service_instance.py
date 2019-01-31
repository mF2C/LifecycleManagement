"""
Service instance - Data management
This is being developed for the MF2C Project: http://www.mf2c-project.eu/

Copyright: Atos Research and Innovation, 2017.

This code is licensed under an Apache 2.0 license. Please, refer to the LICENSE.TXT file for more information

Created on 28 feb. 2019

@author: Roi Sucasas - ATOS
"""

from common.logs import LOG
from common.common import STATUS_CREATED_NOT_INITIALIZED


# new_service_instance: Creates a new service instance object
#   IN: 1. service
#       2. [{"agent_ip": "192.168.252.41", "num_cpus": 4, "master_compss": false},
#           {"agent_ip": "192.168.252.43", "num_cpus": 2, "master_compss": true}] TODO: IPs list until landscaper is ready
#       3. user_id
#       4. agreement_id
#   OUT: service_instance dict
def new_service_instance(service, agents_list, user_id, agreement_id):
    LOG.debug("LIFECYCLE: Data: Service Instance: new_service_instance: " + str(service) + ", " + str(agents_list) + ", " + str(user_id) + ", " + str(agreement_id))

    # create list of agents
    list_of_agents = []

    # ports:
    ports_l = []
    try:
        ports_l = service['exec_ports']
    except:
        LOG.warning("LIFECYCLE: Data: Service Instance: new_service_instance: No ports values found in service definition")

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
                               "master_compss": master_compss,  # TODO master_compss is not needed anymore
                               "agent_param":   "not-defined"})
        i += 1

    # SERVICE_INSTANCE:
    new_service_instance = {"service":          service['id'],
                            "agreement":        agreement_id,
                            "user":             user_id,
                            "device_id":        "not-defined",
                            "device_ip":        "not-defined",
                            "parent_device_id": "not-defined",
                            "parent_device_ip": "not-defined",
                            "agents":           list_of_agents,
                            "service_type":     service['exec_type'],
                            "status":           STATUS_CREATED_NOT_INITIALIZED}

    LOG.debug("LIFECYCLE: Data: Service Instance: new_service_instance: create_service_instance: adding service_intance to CIMI ...")
    LOG.debug("LIFECYCLE: Data: Service Instance: new_service_instance: create_service_instance: " + str(new_service_instance))

    return new_service_instance


def new_service_instance_old(service, agents_list, user_id, agreement_id):
    LOG.debug("LIFECYCLE: Data: Service Instance: new_service_instance: " + str(service) + ", " + str(agents_list) + ", " + str(user_id) + ", " + str(agreement_id))

    # create list of agents
    list_of_agents = []

    # ports:
    ports_l = []
    try:
        ports_l = service['exec_ports']
    except:
        LOG.warning("LIFECYCLE: Data: Service Instance: new_service_instance: No ports values found in service definition")

    # AGENTs:
    i = 0
    for agent in agents_list:
        if len(agents_list) == 1 or i == 0:
            master_compss = True
        else:
            master_compss = False
        # Add new AGENT to list
        list_of_agents.append({"agent":         {"href": "agent/default-value"},
                               "ports":         ports_l,
                               "url":           agent['agent_ip'],
                               "status":        STATUS_CREATED_NOT_INITIALIZED,
                               "num_cpus":      1,
                               "allow":         True,
                               "container_id":  "-",
                               "master_compss": master_compss,  # TODO master_compss is not needed anymore
                               "agent_param":   "not-defined"})
        i += 1

    # SERVICE_INSTANCE:
    new_service_instance = {"service":          service['id'],
                            "agreement":        agreement_id,
                            "user":             user_id,
                            "agents":           list_of_agents,
                            "status":           STATUS_CREATED_NOT_INITIALIZED}

    LOG.debug("LIFECYCLE: Data: Service Instance: new_service_instance: create_service_instance: adding service_intance to CIMI ...")
    LOG.debug("LIFECYCLE: Data: Service Instance: new_service_instance: create_service_instance: " + str(new_service_instance))

    return new_service_instance