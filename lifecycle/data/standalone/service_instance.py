"""
Service instance - Data management
This is being developed for the MF2C Project: http://www.mf2c-project.eu/

Copyright: Atos Research and Innovation, 2017.

This code is licensed under an Apache 2.0 license. Please, refer to the LICENSE.TXT file for more information

Created on 28 feb. 2019

@author: Roi Sucasas - ATOS
"""

from lifecycle.logs import LOG
from lifecycle.common import STATUS_CREATED_NOT_INITIALIZED


# new_service_instance: Creates a new service instance object
#   IN: 1. service
#       2. [{"agent_ip": "192.168.252.41"}, {"agent_ip": "192.168.252.43"}]
#       3. user_id
#       4. agreement_id
#   OUT: service_instance dict
def new_service_instance(service, agents_list, user_id, agreement_id):
    LOG.debug("[lifecycle.data.standalone.service_instance] [new_service_instance] " + service['name'] + ", " + str(agents_list) + ", " + str(user_id) + ", " + str(agreement_id))

    # create list of agents
    list_of_agents = []

    # ports:
    ports_l = []
    try:
        ports_l = service['exec_ports']
    except:
        LOG.warning("[lifecycle.data.standalone.service_instance] [new_service_instance] No ports values found in service definition")

    # AGENTs:
    i = 0
    if len(agents_list) > 0:
        for agent in agents_list:
            if len(agents_list) == 1 or i == 0:
                master_compss = True
            else:
                master_compss = False
            # Add new AGENT to list
            list_of_agents.append({"device_id":     "-",
                                   "app_type":      service['exec_type'],
                                   "ports":         ports_l,
                                   "url":           agent['agent_ip'],
                                   "status":        STATUS_CREATED_NOT_INITIALIZED,
                                   "compss_app_id": "-",
                                   "allow":         True,
                                   "container_id":  "-",
                                   "master_compss": master_compss,  # master_compss... selected / final master
                                   "agent_param":   "not-defined"})
            i += 1

    # service instance
    new_service_instance = {
        "service": service,
        "agreement": agreement_id,
        "user": user_id,
        "device_id": "not-defined",
        "device_ip": "not-defined",
        "parent_device_id": "not-defined",
        "parent_device_ip": "not-defined",
        "agents": list_of_agents,
        "service_type": service['exec_type'],
        "status": STATUS_CREATED_NOT_INITIALIZED
    }

    LOG.debug("[lifecycle.data.standalone.service_instance] [new_service_instance] service_intance=" + str(new_service_instance))
    return new_service_instance


