"""
Agent decision
This is being developed for the MF2C Project: http://www.mf2c-project.eu/

Copyright: Atos Research and Innovation, 2017.

This code is licensed under an Apache 2.0 license. Please, refer to the LICENSE.TXT file for more information

Created on 09 feb. 2018

@author: Roi Sucasas - ATOS
"""

import lifecycle.data.mF2C.mf2c as mf2c
import config as config
import common.common as common
from common.logs import LOG
from common.common import SERVICE_DOCKER, SERVICE_DOCKER_COMPOSE, SERVICE_COMPSS, SERVICE_KUBERNETES, SERVICE_DOCKER_SWARM


'''
OUTPUT FROM LANDSCAPER/RECOMMENDER:
"list of hosts ordered by ‘max optimization’ descending (at the moment optimizing by cpu usage)"
 [
  {'compute saturation': 0.0, 'network saturation': 0.0, 'memory saturation': 0.0, 'memory utilization': 0.0,
   'network utilization': 0.0, 'type': 'machine', 'disk saturation': 0.0, 'node_name': 'machine-A',
   'compute utilization': 0.0, 'disk utilization': 0.0},
  {'compute saturation': 0.0, 'network saturation': 0.0, 'memory saturation': 0.0, 'memory utilization': 0.0,
   'network utilization': 0.0, 'type': 'machine', 'disk saturation': 0.0, 'node_name': 'machine-B',
   'compute utilization': 0.0, 'disk utilization': 0.0},
  {'compute saturation': 0.0, 'network saturation': 0.0, 'memory saturation': 0.0, 'memory utilization': 0.0,
   'network utilization': 0.0, 'type': 'machine', 'disk saturation': 0.0, 'node_name': '192.168.252.41',
   'compute utilization': 0.0, 'disk utilization': 0.0},
  {'compute saturation': 0.0, 'network saturation': 0.0, 'memory saturation': 0.0, 'memory utilization': 0.0,
   'network utilization': 0.0, 'type': 'machine', 'disk saturation': 0.0, 'node_name': 'tango-docker',
   'compute utilization': 0.0, 'disk utilization': 0.0}
 ]
    
 ==> [{"agent_ip": "192.168.252.41"}, {"agent_ip": "192.168.252.42"}]
'''


# get_available_agents_list: Gets a list of available agents
# IN: service
# OUT: resources TODO!!
#   resources example:
#       {
#           "list_of_agents": ["192.168.252.7", "192.168.252.8", "192.168.252.9" ...],   // list urls / docker apis
#           ...
#       }
def get_available_agents_resources(service):
    try:
        LOG.debug("LIFECYCLE: agent_decision: get_available_agents_list ################")
        LOG.debug("LIFECYCLE: agent_decision: get_available_agents_list: " + str(service))

        if common.is_standalone_mode():
            LOG.warning("LIFECYCLE: agent_decision: get_available_agents_list: STANDALONE_MODE enabled")
            LOG.error("LIFECYCLE: agent_decision: get_available_agents_list: returning None...")
            return None
        else:
            # Call to ANALYTICS ENGINE (RECOMMENDER & LANDSCAPER)
            # The Lifecycle Management module calls the Recommender in order to get the optimal deployment configuration
            #   to run the service.
            # Based on this optimal configuration returned by the Recommender, the Lifecycle module asks the Landscaper
            #   for a list of resources that match this recommendation.
            resources = mf2c.recommender_get_optimal_resources(service)

            # If no resources were found, then the Lifecycle Management forwards the request (submit a service) upwards
            if not resources or len(resources) == 0:
                # forwards the request upwards
                # TODO: not implemented
                LOG.warning("LIFECYCLE: agent_decision: get_available_agents_list: forwards the request upwards: not implemented")

                # TODO remove
                LOG.warning("LIFECYCLE: agent_decision: get_available_agents_list: returning localhost")
                return [{"agent_ip": config.dic['HOST_IP']}]

            else:
                LOG.debug("LIFECYCLE: agent_decision: get_available_agents_list: total=" + str(len(resources)))
                return resources
    except:
        LOG.error('LIFECYCLE: agent_decision: get_available_agents_list: Exception')
        return None


# qos_providing: call to QoS PROVIDING
def qos_providing(service_instance):
    try:
        LOG.debug("LIFECYCLE: agent_decision: qos_providing ############################")
        LOG.debug("LIFECYCLE: agent_decision: qos_providing: " + str(service_instance))

        service_instance_1 = mf2c.service_management_qos(service_instance)
        LOG.debug("LIFECYCLE: agent_decision: qos_providing: service_instance_1: " + str(service_instance_1))
        if service_instance_1 is not None:
            try:
                LOG.debug("LIFECYCLE: agent_decision: qos_providing: processing response...")
                for agent1 in service_instance_1["agents"]:
                    LOG.debug("LIFECYCLE: agent_decision: qos_providing: [agent1=" + str(agent1) + "]")
                    if not agent1['allow']:
                        LOG.debug("LIFECYCLE: agent_decision: qos_providing: [agent1.allow=FALSE]")
                        for agent0 in service_instance["agents"]:
                            if agent0['url'] == agent1['url']:
                                agent0['allow'] = False
                                LOG.debug("LIFECYCLE: agent_decision: qos_providing: [agent0=" + str(agent0) + "]")
                    else:
                        LOG.debug("LIFECYCLE: agent_decision: qos_providing: [agent1.allow=TRUE]")

            except:
                LOG.error('LIFECYCLE: agent_decision: qos_providing: Exception while processing response')

        return True
    except:
        LOG.error('LIFECYCLE: agent_decision: qos_providing: Exception')
        return False


'''
 SERVICE INSTANCE:
   {
       ...
       "id": "",
       "user": "testuser",
       "device_id": "",
	   "device_ip": "",
	   "parent_device_id": "",
	   "parent_device_ip": "",
       "service": "",
       "agreement": "",
       "status": "waiting",
       "service_type": "swarm",
       "agents": [
           {"agent": resource-link, "url": "192.168.1.31", "ports": [8081], "container_id": "10asd673f", "status": "waiting",
               "num_cpus": 3, "allow": true, "master_compss": true, "app_type": "swarm"},
           {"agent": resource-link, "url": "192.168.1.34", "ports": [8081], "container_id": "99asd673f", "status": "waiting",
               "num_cpus": 2, "allow": true, "master_compss": false, "app_type": "swarm"}
      ]
   }
'''


# check_user_profile:
def check_user_profile(user_profiling):
    return True


# check_user_sharing_model:
def check_user_sharing_model(user_sharing_model):
    return True


# user_management: call to USER MANAGEMENT -> profiling and sharing model
def user_management(service_instance):
    try:
        LOG.debug("LIFECYCLE: agent_decision: user_management ############################")
        LOG.debug("LIFECYCLE: agent_decision: user_management: " + str(service_instance))

        l_filtered_agents = []
        for agent in service_instance["agents"]:
            LOG.debug("LIFECYCLE: agent_decision: user_management: Getting user_profiling and user_sharing_model from " + agent['url'] + " ...")
            user_profiling = None
            user_sharing_model = None

            # LOCAL
            if agent['url'] == common.get_local_ip():
                LOG.debug("LIFECYCLE: agent_decision: user_management: LOCAL user_profiling and user_sharing_model")
                user_profiling = mf2c.user_management_profiling()
                user_sharing_model = mf2c.user_management_sharing_model()
            # 'REMOTE' AGENT
            elif common.check_ip(agent['url']):
                LOG.debug("LIFECYCLE: agent_decision: user_management: REMOTE user_profiling and user_sharing_model")
                user_profiling = mf2c.user_management_profiling(agent['url'])
                user_sharing_model = mf2c.user_management_sharing_model(agent['url'])
            else:
                LOG.warning("LIFECYCLE: agent_decision: user_management: Could not get user_profiling and user_sharing_model")

            LOG.debug("LIFECYCLE: agent_decision: user_management: user_profiling: " + str(user_profiling))
            LOG.debug("LIFECYCLE: agent_decision: user_management: user_sharing_model: " + str(user_sharing_model))

            # mantain agent in list if no user_profiling or user_sharing_model
            if user_profiling is None or user_sharing_model is None:
                LOG.warning("LIFECYCLE: agent_decision: user_management: user_profiling or user_sharing_model is None")
                l_filtered_agents.append(agent)
            # check content
            else:
                LOG.debug("LIFECYCLE: agent_decision: user_management: Checking user information ...")
                allowed = True
                if not check_user_profile(user_profiling):
                    allowed = False
                    LOG.debug("LIFECYCLE: agent_decision: user_management: agent not allowed: " + str(agent))
                if not check_user_sharing_model(user_sharing_model):
                    allowed = False
                    LOG.debug("LIFECYCLE: agent_decision: user_management: agent not allowed: " + str(agent))

                if allowed:
                    l_filtered_agents.append(agent)
        service_instance['agents'] = l_filtered_agents

        return service_instance
    except:
        LOG.error('LIFECYCLE: agent_decision: user_management: Exception')
        return None


# service_manager_qos_providing: call to QoS PROVIDING
def service_manager_qos_providing(service_instance):
    try:
        LOG.debug("LIFECYCLE: agent_decision: service_manager_qos_providing ############################")
        LOG.debug("LIFECYCLE: agent_decision: service_manager_qos_providing: " + str(service_instance))

        service_instance_res = mf2c.service_management_qos(service_instance)
        LOG.debug("LIFECYCLE: agent_decision: service_manager_qos_providing: service_instance_res: " + str(service_instance_res))
        if service_instance_res is not None:
            LOG.debug("LIFECYCLE: agent_decision: service_manager_qos_providing: processing response...")

            service_instance['agents'] = []

            for agent_res in service_instance_res["agents"]:
                if agent_res['allow']:
                    service_instance['agents'].append(agent_res)
    except:
        LOG.error('LIFECYCLE: agent_decision: service_manager_qos_providing: Exception')
    return service_instance


# select_agents_list: Select from list of available agents
def select_agents(service_type, service_instance):
    try:
        LOG.debug("LIFECYCLE: agent_decision: select_agents: [service_type=" + service_type + "], [agents=" + str(service_instance) + "]")

        if common.is_standalone_mode():
            LOG.warning("LIFECYCLE: agent_decision: select_agents: STANDALONE_MODE enabled")
            return service_instance
        else:
            LOG.debug("LIFECYCLE: agent_decision: select_agents: agents INITIAL list: " + str(service_instance['agents']))

            # 1. QoS PROVIDING
            qos_providing(service_instance)

            # 2. USER MANAGEMENT -> profiling and sharing model
            service_instance_res = user_management(service_instance)
            if not service_instance_res is None:
                service_instance = service_instance_res

            LOG.debug("LIFECYCLE: agent_decision: select_agents: agents FILTERED list: " + str(service_instance['agents']))

            # compss (docker)
            if service_type == SERVICE_COMPSS:
                LOG.debug("LIFECYCLE: agent_decision: select_agents: [SERVICE_COMPSS] service will be deployed in all selected agents")
            else:
                list_of_agents = []
                list_of_agents.append(service_instance['agents'][0])
                LOG.debug("LIFECYCLE: agent_decision: select_agents: [" + service_type + "] first agent: " + str(list_of_agents))

                # docker-compose, docker, swarm, k8s
                if service_type == SERVICE_DOCKER_COMPOSE or service_type == SERVICE_DOCKER \
                        or service_type == SERVICE_DOCKER_SWARM or service_type == SERVICE_KUBERNETES:
                    service_instance['agents'] = list_of_agents
                # not defined
                else:
                    LOG.warning("LIFECYCLE: agent_decision: select_agents: [" + service_type + "] not defined")

            LOG.debug("LIFECYCLE: agent_decision: select_agents: agents FINAL list: " + str(service_instance['agents']))

            return service_instance
    except:
        LOG.error('LIFECYCLE: agent_decision: select_agents: Exception')
        return None