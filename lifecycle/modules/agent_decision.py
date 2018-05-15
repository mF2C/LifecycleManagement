"""
Agent decision
This is being developed for the MF2C Project: http://www.mf2c-project.eu/

Copyright: Atos Research and Innovation, 2017.

This code is licensed under an Apache 2.0 license. Please, refer to the LICENSE.TXT file for more information

Created on 09 feb. 2018

@author: Roi Sucasas - ATOS
"""

import lifecycle.mF2C.mf2c as mf2c
import lifecycle.utils.common as common
from lifecycle.utils.logs import LOG
from lifecycle import config


'''
OUTPUT FROM LANDSCAPER/RECOMMENDER:
"list of hosts ordered by ‘max optimization’ descending (at the moment optimizing by cpu usage)"
    {
        "node_name": {
            "0": "machine-A",
            "1": "machine-B"
        },
        "type": {
            "0": "machine",
            "1": "machine"
        },
        "compute utilization": {
            "0": 0.0,
            "1": 0.0
        },
        "compute saturation": {
            "0": 0.0,
            "1": 0.0
        },
        "memory utilization": {
            "0": 0.0,
            "1": 0.0
        },
        "memory saturation": {
            "0": 0.0,
            "1": 0.0
        },
        "network utilization": {
            "0": 0.0,
            "1": 0.0
        },
        "network saturation": {
            "0": 0.0,
            "1": 0.0
        },
        "disk utilization": {
            "0": 0.0,
            "1": 0.0
        },
        "disk saturation": {
            "0": 0.0,
            "1": 0.0
        }
    }
    
    ==>
    
    "agents_list": [{
			"agent_ip": "192.168.252.41",
			"num_cpus": 7,
			"master_compss": true
		}
	]
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
        LOG.debug("Lifecycle-Management: agent_decision: get_available_agents_list ################")
        LOG.debug("Lifecycle-Management: agent_decision: get_available_agents_list: " + str(service))

        if common.is_standalone_mode():
            LOG.warning("Lifecycle-Management: agent_decision: get_available_agents_list: STANDALONE_MODE enabled")
            LOG.warning("Lifecycle-Management: agent_decision: get_available_agents_list: agents from config: " + str(config.dic['AVAILABLE_AGENTS']))
            return config.dic['AVAILABLE_AGENTS']
        else:
            # Call to ANALYTICS ENGINE (RECOMMENDER & LANDSCAPER)
            # The Lifecycle Management module calls the Recommender in order to get the optimal deployment configuration
            #   to run the service.
            # Based on this optimal configuration returned by the Recommender, the Lifecycle module asks the Landscaper
            #   for a list of resources that match this recommendation.
            resources = mf2c.get_optimal_resources(service)

            # If no resources were found, then the Lifecycle Management forwards the request (submit a service) upwards
            if not resources or len(resources) == 0:
                # forwards the request upwards
                # TODO: not implemented
                LOG.warning("Lifecycle-Management: agent_decision: get_available_agents_list: forwards the request upwards: not implemented")
                return None

            else:
                # process response: resources
                LOG.debug("Lifecycle-Management: agent_decision: get_available_agents_list: processing resources: " + str(resources) + " ...")
                total_res = len(resources['node_name'])
                LOG.debug("Lifecycle-Management: agent_decision: get_available_agents_list: total=" + str(total_res))

                # TODO hostname <-> IP mapping

                return config.dic['AVAILABLE_AGENTS']
    except:
        LOG.error('Lifecycle-Management: agent_decision: get_available_agents_list: Exception')
        return None


# select_agents_list: Select from list of available agents
# 1. QoS PROVIDING -> RESOURCES = XXX (RESOURCES) -> RESOURCES = GET_RESOURCES(RESOURCES)
#       resources = mf2c.get_qos_resources(resources) # TODO
# 2. USER MANAGEMENT -> RESOURCES = GET_RESOURCES(RESOURCES)
#       resources = mf2c.get_um_resources(resources) # TODO
# 3. Select agents
def select_agents(service_instance):
    try:
        LOG.debug("Lifecycle-Management: agent_decision: select_agents ############################")
        LOG.debug("Lifecycle-Management: agent_decision: select_agents: " + str(service_instance))

        if common.is_standalone_mode():
            LOG.warning("Lifecycle-Management: agent_decision: select_agents: STANDALONE_MODE enabled")
            return service_instance
        else:
            # 1. QoS PROVIDING
            service_instance_1 = mf2c.service_management_qos(service_instance)
            LOG.debug("Lifecycle-Management: agent_decision: select_agents: service_instance_1: " + str(service_instance_1))
            if service_instance_1 is not None:
                try:
                    LOG.debug("Lifecycle-Management: agent_decision: select_agents: processing response...")
                    for agent1 in service_instance_1["agents"]:
                        LOG.debug("Lifecycle-Management: agent_decision: select_agents: [agent1=" + str(agent1) + "]")
                        if not agent1['allow']:
                            LOG.debug("Lifecycle-Management: agent_decision: select_agents: [agent1.allow=FALSE]")
                            for agent0 in service_instance["agents"]:
                                if agent0['url'] == agent1['url']:
                                    agent0['allow'] = False
                                    LOG.debug("Lifecycle-Management: agent_decision: select_agents: [agent0=" + str(agent0) + "]")
                        else:
                            LOG.debug("Lifecycle-Management: agent_decision: select_agents: [agent1.allow=TRUE]")

                except:
                    LOG.error('Lifecycle-Management: agent_decision: select_agents: Exception while processing response')

            # 2. USER MANAGEMENT -> profiling and sharing model
            # TODO information from User Management module not used
            for agent in service_instance["agents"]:
                LOG.info(">>> AGENT >>> " + agent['url'] + " <<<")
                # LOCAL
                if agent['url'] == common.get_local_ip():
                    LOG.debug("Lifecycle-Management: agent_decision: select_agents: local user_profiling and user_sharing_model")

                    user_profiling = mf2c.user_management_profiling(service_instance['user'])
                    LOG.debug("Lifecycle-Management: agent_decision: select_agents: user_profiling: " + str(user_profiling))

                    user_sharing_model = mf2c.user_management_sharing_model(service_instance['user'])
                    LOG.debug("Lifecycle-Management: agent_decision: select_agents: user_sharing_model: " + str(user_sharing_model))

                # 'REMOTE' AGENT
                elif common.check_ip(agent['url']):
                    LOG.debug("Lifecycle-Management: agent_decision: select_agents: remote user_profiling and user_sharing_model")

                    user_profiling = mf2c.user_management_profiling(service_instance['user'])
                    LOG.debug("Lifecycle-Management: agent_decision: select_agents: user_profiling: " + str(user_profiling))

                    user_sharing_model = mf2c.user_management_sharing_model(service_instance['user'])
                    LOG.debug("Lifecycle-Management: agent_decision: select_agents: user_sharing_model: " + str(user_sharing_model))

            # 3. TODO PROCESS INFORMATION AND SELECT BEST CANDIDATES
            LOG.debug("Lifecycle-Management: agent_decision: select_agents: not implemented")

            if not service_instance_1:
                LOG.error("Lifecycle-Management: agent_decision: select_agents: Error calling QoS Providing component")
                return service_instance
            return service_instance_1
    except:
        LOG.error('Lifecycle-Management: agent_decision: select_agents: Exception')
        return None