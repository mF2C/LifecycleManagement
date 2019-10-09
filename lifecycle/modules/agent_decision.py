"""
Agent decision
This is being developed for the MF2C Project: http://www.mf2c-project.eu/

Copyright: Atos Research and Innovation, 2017.

This code is licensed under an Apache 2.0 license. Please, refer to the LICENSE.TXT file for more information

Created on 09 feb. 2018

@author: Roi Sucasas - ATOS
"""

from lifecycle.connectors import connector as connector
from lifecycle.data import data_adapter as data_adapter
from lifecycle import common as common
from lifecycle.logs import LOG
from lifecycle.common import SERVICE_DOCKER, SERVICE_DOCKER_COMPOSE, SERVICE_COMPSS, SERVICE_KUBERNETES, SERVICE_DOCKER_SWARM


###############################################################################
# ANALYTICS ENGINE functions

# FUNCTION:  get_available_agents_list: Gets a list of available agents ordered by X
#   OUT: resources
#       { ... "list_of_agents": ["192.168.252.7", "192.168.252.8", "192.168.252.9" ...] }
#
#   OUTPUT FROM LANDSCAPER/RECOMMENDER:
#       "list of hosts ordered by ‘max optimization’ descending (at the moment optimizing by cpu usage)"
#       [
#           {'compute saturation': 0.0, 'network saturation': 0.0, 'memory saturation': 0.0, 'memory utilization': 0.0,
#           'network utilization': 0.0, 'type': 'machine', 'disk saturation': 0.0, 'node_name': 'machine-A',
#           'compute utilization': 0.0, 'disk utilization': 0.0},
#           ...
#       ]
# ==> [{"agent_ip": "192.168.252.41"}, {"agent_ip": "192.168.252.42"}]
def get_available_agents_resources(service):
    try:
        LOG.info("######## GET AVAILABLE AGENTS: ANALYTICS ENGINE / RECOMMENDER ################# (1) ###########")
        LOG.info("[lifecycle.modules.agent_decision] [get_available_agents_resources] Gets a list of available agents in the current cluster ...")

        if common.is_standalone_mode():
            LOG.warning("[lifecycle.modules.agent_decision] [get_available_agents_resources] STANDALONE_MODE enabled; returning None ...")
            return None
        else:
            # Call to ANALYTICS ENGINE (RECOMMENDER & LANDSCAPER)
            # The Lifecycle Management module calls the Recommender in order to get the optimal deployment configuration to run the service.
            # Based on this optimal configuration returned by the Recommender, the Lifecycle module asks the Landscaper for a list of resources that match this recommendation.
            resources = connector.get_available_devices(service)

            # TODO release version - uncomment
            # if not resources:
            #     LOG.debug("LIFECYCLE: agent_decision: get_available_agents_list: total=None")
            # else:
            #     LOG.debug("LIFECYCLE: agent_decision: get_available_agents_list: total=" + str(len(resources)))
            # return resources

            # TODO temporal version - until analytics engine works - remove
            # If no resources were found, then the Lifecycle Management forwards the request (submit a service) upwards
            if not resources or len(resources) == 0:
                LOG.warning("[lifecycle.modules.agent_decision] [get_available_agents_resources] temporal fix")
                LOG.warning("[lifecycle.modules.agent_decision] [get_available_agents_resources] returning localhost")
                return [{"agent_ip": data_adapter.get_host_ip()}]
            else:
                LOG.debug("[lifecycle.modules.agent_decision] [get_available_agents_resources] total=" + str(len(resources)))
                return resources
    except:
        LOG.exception('[lifecycle.modules.agent_decision] [get_available_agents_resources] Exception')
        return None


###############################################################################
# USER MANAGEMENT functions
#
#  SERVICE INSTANCE:
#    {
#        ...
#        "agents": [
#            {"agent": resource-link, "url": "192.168.1.31", "ports": [8081], "container_id": "10asd673f", "status": "waiting",
#                "num_cpus": 3, "allow": true, "master_compss": true, "app_type": "swarm"}, ...
#       ]
#    }
#

# FUNCTION: __user_management: call to USER MANAGEMENT -> profiling and sharing model
# If any error is found when calling USER MANAGEMENT module, then the Lifecycle does not filter the list of agents
def __user_management(service_instance):
    try:
        LOG.info("[lifecycle.modules.agent_decision] [__user_management] Checking user-profile and sharing-model in selected agents " +
                 str(service_instance["agents"]) + " ...")

        l_filtered_agents = []
        for agent in service_instance["agents"]:
            LOG.debug("[lifecycle.modules.agent_decision] [__user_management] Getting user-profile and sharing-model policies result from " + agent['url'] + " ...")
            res = None

            # LOCAL
            if agent['url'] == data_adapter.get_my_ip(): #common.get_local_ip():
                LOG.debug("[lifecycle.modules.agent_decision] [__user_management] Getting LOCAL user-profile and sharing-model policies ...")
                res = connector.user_management_check_avialability() #data_adapter.get_check_um()
            # 'REMOTE' AGENT
            elif common.check_ip(agent['url']):
                LOG.debug("[lifecycle.modules.agent_decision] [__user_management] Getting REMOTE user-profile and sharing-model policies ...")
                res = connector.lifecycle_um_check_avialability(agent)
            else:
                LOG.warning("[lifecycle.modules.agent_decision] [__user_management] Could not get user-profile and sharing-model policies")

            LOG.debug("[lifecycle.modules.agent_decision] [__user_management] res=" + str(res))

            # mantain agent in list if no user_profiling or user_sharing_model
            if res is None:
                LOG.warning("[lifecycle.modules.agent_decision] [__user_management] user-profile or sharing-model result is None")
                l_filtered_agents.append(agent)
            # check content
            else:
                LOG.debug("[lifecycle.modules.agent_decision] [__user_management] Checking agents information ...")
                if 'result' in res and not res['result']:
                    LOG.debug("[lifecycle.modules.agent_decision] [__user_management] agent not allowed: " + str(agent))
                else:
                    if not res['sharing_model'] or not res['sharing_model']['device_id']:
                        l_filtered_agents.append(agent)
                    else:
                        agent['device_id'] = res['sharing_model']['device_id']
                        l_filtered_agents.append(agent)

        service_instance['agents'] = l_filtered_agents

        return service_instance
    except:
        LOG.exception('[lifecycle.modules.agent_decision] [__user_management] Exception')
        return None


###############################################################################
## QOS PROVIDING functions
#
#  SERVICE INSTANCE:
#    { ...
#      "agents": [{"agent": resource-link, "url": "192.168.1.31", "ports": [8081], "container_id": "10asd673f", "status": "waiting",
#                "num_cpus": 3, "allow": true, "master_compss": true, "app_type": "swarm"}, ...] }
#
# OUTPUT FROM QoS PROVIDING:
#   { ... "agents": [{'allow': False, 'url': '192.168.252.41'}, ...] }

# FUNCTION: __check_qos:
def __check_qos(agent_resp):
    if 'allow' not in agent_resp: #if not agent_resp['allow']:
        return True # TODO return False
    return agent_resp['allow'] #True


# FUNCTION: __qos_providing: call to QoS PROVIDING
# If any error is found when calling QoS provider, then the Lifecycle does not filter the list of agents
def __qos_providing(service_instance):
    try:
        LOG.debug("[lifecycle.modules.agent_decision] [__qos_providing] Checking QoS of service instance [" + str(service_instance) + "] ...")

        service_instance_resp = connector.qos_providing(service_instance)
        LOG.debug("[lifecycle.modules.agent_decision] [__qos_providing] service_instance_resp: " + str(service_instance_resp))

        if service_instance_resp is not None:
            l_filtered_agents = []
            try:
                LOG.debug("[lifecycle.modules.agent_decision] [__qos_providing] processing response...")
                for agent_resp in service_instance_resp["agents"]:
                    for agent in service_instance["agents"]:
                        if agent['device_id'] == agent_resp['device_id'] and __check_qos(agent_resp):
                            l_filtered_agents.append(agent)
            except:
                LOG.exception('[lifecycle.modules.agent_decision] [__qos_providing] Exception while processing response')
                return None
            service_instance['agents'] = l_filtered_agents
        else:
            LOG.error("[lifecycle.modules.agent_decision] [__qos_providing] mf2c.service_management_qos(service_instance) returned NONE")

        LOG.debug("[lifecycle.modules.agent_decision] [__qos_providing] service_instance=" + str(service_instance))
        return service_instance
    except:
        LOG.exception('[lifecycle.modules.agent_decision] [__qos_providing] Exception')
        return None


###############################################################################
## SWARM SERVICE functions

# FUNCTION: __check_swarm:
def __check_swarm(agent):
    result = connector.lifecycle_check_agent_swarm(agent)
    if not result is None:
        return result['result']
    return False


# FUNCTION: __filter_by_swarm: check if agents support swarm
def __filter_by_swarm(service_instance):
    try:
        LOG.debug("[lifecycle.modules.agent_decision] [filter_by_swarm] Checking if agents support Docker Swarm ...")

        l_filtered_agents = []
        try:
            for agent in service_instance["agents"]:
                if __check_swarm(agent):
                    LOG.debug("[lifecycle.modules.agent_decision] [filter_by_swarm] Docker Swarm supported by agent: " + str(agent))
                    l_filtered_agents.append(agent)
        except:
            LOG.exception('[lifecycle.modules.agent_decision] [filter_by_swarm] Exception while processing response')
            return None
        service_instance['agents'] = l_filtered_agents

        LOG.debug("[lifecycle.modules.agent_decision] [filter_by_swarm] service_instance=" + str(service_instance))
        return service_instance
    except:
        LOG.exception('[lifecycle.modules.agent_decision] [filter_by_swarm] Exception')
        return None



###############################################################################

# FUNCTION: __service_compss: deploy COMPSs application ==> all available agents / num_agents
# if the service is a COMPSs service, the LM will select all agents or a total of 'num_agents'
# in the case this variable ('num_agents') is defined and grater than 1
def __select_agents_service_compss(service_instance, num_agents):
    # compss ==> deploy in all agents
    if len(service_instance['agents']) > 0 and num_agents == -1:
        LOG.debug("[lifecycle.modules.agent_decision] [__select_agents_service_compss] [SERVICE_COMPSS] service will be deployed in all selected agents")

    # compss ==> deploy in 'num_agents'
    elif len(service_instance['agents']) > 0:
        if len(service_instance['agents']) >= num_agents:
            LOG.debug("[lifecycle.modules.agent_decision] [__select_agents_service_compss] [SERVICE_COMPSS] service will be deployed in " + str(num_agents) + " agents")
            list_of_agents = []
            i = 0
            while i < num_agents: #len(service_instance['agents']):
                list_of_agents.append(service_instance['agents'][i])
                i += 1
            service_instance['agents'] = list_of_agents

        else:
            LOG.warning("[lifecycle.modules.agent_decision] [__select_agents_service_compss] [SERVICE_COMPSS] service should be deployed in " + str(num_agents) +
                        " agents, but only " + str(len(service_instance['agents'])) + " are available")
            return service_instance, "not-enough-resources-found"

    # compss: not-enough-resources-found
    else:
        return service_instance, "not-enough-resources-found"

    LOG.debug("[lifecycle.modules.agent_decision] [__select_agents_service_compss] agents FINAL list: " + str(service_instance['agents']))
    return service_instance, "ok"


# __service_docker_swarm: deploy DOCKER SWARM application ==> first available docker swarm agent
def __select_agents_service_docker_swarm(service_instance):
    # docker swarm ==> deploy in first available agent
    if len(service_instance['agents']) > 0:
        list_of_agents = [service_instance['agents'][0]]
        LOG.debug("[lifecycle.modules.agent_decision] [__select_agents_service_docker_swarm] first agent: " + str(list_of_agents))
        service_instance['agents'] = list_of_agents

    # docker swarm: not-enough-resources-found
    else:
        return service_instance, "not-enough-resources-found"

    LOG.debug("[lifecycle.modules.agent_decision] [__select_agents_service_docker_swarm] agents FINAL list: " + str(service_instance['agents']))
    return service_instance, "ok"


# FUNCTION: __service_default: deploy DEFAULT application ==> first available agent
# by default the LM will select the first available option. This means, the service will
# be deployed in only one mF2C agent
def __select_agents_service_default(service_instance):
    # docker swarm ==> deploy in first available agent
    if len(service_instance['agents']) > 0:
        list_of_agents = [service_instance['agents'][0]]
        LOG.debug("[lifecycle.modules.agent_decision] [__select_agents_service_default] first agent: " + str(list_of_agents))
        service_instance['agents'] = list_of_agents

    # docker swarm: not-enough-resources-found
    else:
        return service_instance, "not-enough-resources-found"

    LOG.debug("[lifecycle.modules.agent_decision] [__select_agents_service_default] agents FINAL list: " + str(service_instance['agents']))
    return service_instance, "ok"


# __service_docker: deploy DOCKER application ==> first available agent / num_agents
def __select_agents_service_docker(service_instance, num_agents):
    # docker ==> deploy in only 1 agent
    if len(service_instance['agents']) > 0 and num_agents == -1:
        list_of_agents = [service_instance['agents'][0]]
        LOG.debug("[lifecycle.modules.agent_decision] [__select_agents_service_docker] first agent: " + str(list_of_agents))
        service_instance['agents'] = list_of_agents

    # docker ==> deploy in 'num_agents'
    elif len(service_instance['agents']) > 0:
        if len(service_instance['agents']) >= num_agents:
            LOG.debug("[lifecycle.modules.agent_decision] [__select_agents_service_docker] [DOCKER] service will be deployed in " + str(num_agents) + " agents")
            list_of_agents = []
            i = 0
            while i < num_agents: # len(service_instance['agents']):
                list_of_agents.append(service_instance['agents'][i])
                i += 1
            service_instance['agents'] = list_of_agents

        else:
            LOG.warning("[lifecycle.modules.agent_decision] [__select_agents_service_compss] [DOCKER] service should be deployed in " + str(num_agents) +
                        " agents, but only " + str(len(service_instance['agents'])) + " are available")
            return service_instance, "not-enough-resources-found"

    # compss: not-enough-resources-found
    else:
        return service_instance, "not-enough-resources-found"

    LOG.debug("[lifecycle.modules.agent_decision] [__select_agents_service_docker] agents FINAL list: " + str(service_instance['agents']))
    return service_instance, "ok"


# select_agents_list: Select from list of available agents
#   the initial list of agents can be found in 'service_instance' object
def select_agents(service_type, num_agents, service_instance):
    try:
        LOG.debug("[lifecycle.modules.agent_decision] [select_agents] [service_type=" + service_type + "], [agents=" + str(service_instance) + "]")

        # STANDALONE MODE ################################
        if common.is_standalone_mode():
            LOG.warning("[lifecycle.modules.agent_decision] [select_agents] STANDALONE_MODE enabled")
            return service_instance, "ok"

        # MF2C MODE ######################################
        else:
            LOG.debug("[lifecycle.modules.agent_decision] [select_agents] agents INITIAL list: " + str(service_instance['agents']))
            # 1. FILTER LIST ###############

            # 1.1. USER MANAGEMENT -> profiling and sharing model
            LOG.info("######## SELECT AGENTS: USER MANAGEMENT ####################################### (2) ###########")
            service_instance_res = __user_management(service_instance)
            if not service_instance_res is None:
                service_instance = service_instance_res
                # save service instance in cimi
                data_adapter.update_service_instance(service_instance['id'], service_instance)

            # 1.2. QoS PROVIDING
            LOG.info("######## SELECT AGENTS: SERVICE MANAGEMENT (QoS) ############################## (3) ###########")
            service_instance_res = __qos_providing(service_instance)
            if not service_instance_res is None:
                service_instance = service_instance_res

            # 1.3. check if service is a SWARM service and filter
            if service_type == SERVICE_DOCKER_SWARM:
                LOG.info("######## SELECT AGENTS: SWARM SERVICE ######################################### (4) ###########")
                service_instance_res = __filter_by_swarm(service_instance)
                if not service_instance_res is None:
                    service_instance = service_instance_res

            LOG.debug("[lifecycle.modules.agent_decision] [select_agents] agents FILTERED list: " + str(service_instance['agents']))

            # 2. SELECT AGENTS FROM LIST ###
            LOG.info("######## SELECT AGENTS: SELECT AGENTS FROM FILTERED LIST ######################################")
            # 2.1. COMPSs
            if service_type == SERVICE_COMPSS:
                return __select_agents_service_compss(service_instance, num_agents)
            # 2.2. DOCKER_SWARM
            elif service_type == SERVICE_DOCKER_SWARM:
                return __select_agents_service_docker_swarm(service_instance)
            # 2.3. DOCKER_COMPOSE
            elif service_type == SERVICE_DOCKER_COMPOSE:
                return __select_agents_service_default(service_instance)
            # 2.4 KUBERNETES
            elif service_type == SERVICE_KUBERNETES:
                LOG.error('[lifecycle.modules.agent_decision] [select_agents] Service type not implemented') # TODO
                return None, "error"
            # 2.5 DOCKER
            elif service_type == SERVICE_DOCKER:
                return __select_agents_service_docker(service_instance, num_agents)
            else:
                LOG.error('[lifecycle.modules.agent_decision] [select_agents] Service type not defined / unknown')
                return None, "error"
    except:
        LOG.exception('[lifecycle.modules.agent_decision] [select_agents] Exception')
        return None, "error"