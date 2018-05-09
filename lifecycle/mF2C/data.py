"""
CIMI - Data management
This is being developed for the MF2C Project: http://www.mf2c-project.eu/

Copyright: Atos Research and Innovation, 2017.

This code is licensed under an Apache 2.0 license. Please, refer to the LICENSE.TXT file for more information

Created on 09 feb. 2018

@author: Roi Sucasas - ATOS
"""

import lifecycle.mF2C.cimi as cimi
from lifecycle.utils.logs import LOG
from lifecycle import config


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
       "service": "",
       "agreement": "",
       "status": "waiting",
       "agents": [
           {"agent": resource-link, "url": "192.168.1.31", "ports": [8081], "container_id": "10asd673f", "status": "waiting",
               "num_cpus": 3, "allow": true, "master_compss": true},
           {"agent": resource-link, "url": "192.168.1.34", "ports": [8081], "container_id": "99asd673f", "status": "waiting",
               "num_cpus": 2, "allow": true, "master_compss": false}
      ]
   }
'''


###############################################################################
# SERVICE INSTANCE
# get_service_instance: Get service instance
def get_service_instance(service_instance_id, obj_response_cimi=None):
    LOG.info("Lifecycle-Management: Data: get_service_instance: " + service_instance_id)
    return cimi.get_service_instance_by_id(service_instance_id, obj_response_cimi)


# get_all_service_instances: Get all service instances
def get_all_service_instances(obj_response_cimi=None):
    LOG.info("Lifecycle-Management: Data: get_all_service_instances: ")
    return cimi.get_all_service_instances(obj_response_cimi)


# del_service_instance: Delete service instance
def del_service_instance(service_instance_id, obj_response_cimi=None):
    LOG.info("Lifecycle-Management: Data: del_service_instance: " + service_instance_id)
    return cimi.del_service_instance_by_id(service_instance_id, obj_response_cimi)


# create_service_instance: Creates a new service instance
#   IN: 1. service
#       2. [{"agent_ip": "192.168.252.41", "num_cpus": 4, "master_compss": false},
#           {"agent_ip": "192.168.252.43", "num_cpus": 2, "master_compss": true}] TODO: IPs list until landscaper is ready
#       3. user_id
#       4. agreement_id
#   OUT: service_instance dict
def create_service_instance(service, agents_list, user_id, agreement_id):
    LOG.debug("Lifecycle-Management: Data: create_service_instance: " + str(service) + ", " + str(agents_list))

    # create list of agents
    list_of_agents = []

    # ports:
    ports_l = []
    try:
        ports_l = service['exec_ports'] #[0]
    except:
        LOG.warning("Lifecycle-Management: Data: No ports values found in service definition")

    # AGENTs:
    for agent in agents_list:
        if len(agents_list) == 1:
            master_compss = True
        elif 'master_compss' not in agent:
            master_compss = False
        else:
            master_compss = agent['master_compss']
        # Add new AGENT to list
        list_of_agents.append({"agent":         {"href": "agent/default-value"},
                               "ports":         ports_l,
                               "url":           agent['agent_ip'],
                               "status":        "not-defined",
                               "num_cpus":      agent['num_cpus'],
                               "allow":         True,
                               "container_id":  "-",
                               "master_compss": master_compss,
                               "agent_param":   "not-defined"})

    # SERVICE_INSTANCE:
    new_service_instance = {"service":          service['id'],
                            "agreement":        agreement_id,
                            "user":             user_id,
                            "agents":           list_of_agents,
                            "status":           "not-defined"}

    LOG.debug("Lifecycle-Management: Data: create_service_instance: adding service_intance to CIMI ...")
    LOG.debug("Lifecycle-Management: Data: create_service_instance: " + str(new_service_instance))

    res = cimi.add_service_instance(new_service_instance)
    if not res:
        LOG.error("Lifecycle-Management: Data: create_service_instance: Error during the creation of the service_instance object")
        return new_service_instance
    return res


# update_service_instance: Updates a service instance
#       service_instance_id = "service-instance/250af452-959f-4ac6-9b06-54f757b46bf0"
def update_service_instance(service_instance_id, service_instance):
    LOG.debug("Lifecycle-Management: Data: (1) update_service_instance: " + service_instance_id + ", " + str(service_instance))
    res = cimi.update_service_instance(service_instance_id, service_instance)
    LOG.debug("Lifecycle-Management: Data: (2) update_service_instance: " + str(res))
    if not res:
        LOG.error("Lifecycle-Management: Data: update_service_instance: Error during the edition of the service_instance object")
        return None
    return res