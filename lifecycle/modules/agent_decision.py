"""
Agent decision
This is being developed for the MF2C Project: http://www.mf2c-project.eu/

Copyright: Atos Research and Innovation, 2017.

This code is licensed under an Apache 2.0 license. Please, refer to the LICENSE.TXT file for more information

Created on 09 feb. 2018

@author: Roi Sucasas - ATOS
"""

import lifecycle.data.mF2C.mf2c as mf2c
import lifecycle.data.data_adapter as data_adapter
import config as config
import common.common as common
from common.logs import LOG
from common.common import SERVICE_DOCKER, SERVICE_DOCKER_COMPOSE, SERVICE_COMPSS, SERVICE_KUBERNETES, SERVICE_DOCKER_SWARM


###############################################################################
# LANDSCAPER / RECOMMENDER
# get_available_agents_list: Gets a list of available agents
# IN: service
# OUT: resources TODO!!
#   resources example:
#       {
#           "list_of_agents": ["192.168.252.7", "192.168.252.8", "192.168.252.9" ...],   // list urls / docker apis
#           ...
#       }
#
# OUTPUT FROM LANDSCAPER/RECOMMENDER:
#
# "list of hosts ordered by ‘max optimization’ descending (at the moment optimizing by cpu usage)"
#  [
#   {'compute saturation': 0.0, 'network saturation': 0.0, 'memory saturation': 0.0, 'memory utilization': 0.0,
#    'network utilization': 0.0, 'type': 'machine', 'disk saturation': 0.0, 'node_name': 'machine-A',
#    'compute utilization': 0.0, 'disk utilization': 0.0},
#   {'compute saturation': 0.0, 'network saturation': 0.0, 'memory saturation': 0.0, 'memory utilization': 0.0,
#    'network utilization': 0.0, 'type': 'machine', 'disk saturation': 0.0, 'node_name': 'machine-B',
#    'compute utilization': 0.0, 'disk utilization': 0.0},
#   {'compute saturation': 0.0, 'network saturation': 0.0, 'memory saturation': 0.0, 'memory utilization': 0.0,
#    'network utilization': 0.0, 'type': 'machine', 'disk saturation': 0.0, 'node_name': '192.168.252.41',
#    'compute utilization': 0.0, 'disk utilization': 0.0},
#   {'compute saturation': 0.0, 'network saturation': 0.0, 'memory saturation': 0.0, 'memory utilization': 0.0,
#    'network utilization': 0.0, 'type': 'machine', 'disk saturation': 0.0, 'node_name': 'tango-docker',
#    'compute utilization': 0.0, 'disk utilization': 0.0}
#  ]
#
# ==> [{"agent_ip": "192.168.252.41"}, {"agent_ip": "192.168.252.42"}]
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
        LOG.exception('LIFECYCLE: agent_decision: get_available_agents_list: Exception')
        return None


###############################################################################
# USER MANAGEMENT
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


# check_user_profile:
def check_user_profile(user_profiling):
    if not user_profiling['resource_contributor']:
        LOG.debug("LIFECYCLE: agent_decision: check_user_profile: agent not allowed (1): resource_contributor is set to False")
        return False
    elif user_profiling['apps_running'] >= user_profiling['max_apps']:
        LOG.debug("LIFECYCLE: agent_decision: check_user_profile: agent not allowed (2): apps_running >= max_apps")
        return False
    return True


# check_user_sharing_model:
def check_user_sharing_model(user_sharing_model):
    power = data_adapter.get_power()
    if power is None or power == -1 or power > user_sharing_model['battery_limit']:
        return True
    LOG.debug("LIFECYCLE: agent_decision: check_user_sharing_model: agent not allowed (1): battery_limit >= current battery level")
    return False


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
                user_profiling = data_adapter.get_um_profile()
                user_sharing_model = data_adapter.get_um_sharing_model()
            # 'REMOTE' AGENT
            elif common.check_ip(agent['url']):
                LOG.debug("LIFECYCLE: agent_decision: user_management: REMOTE user_profiling and user_sharing_model")
                agent_um = mf2c.lifecycle_um_info(agent)
                if not agent_um:
                    user_profiling = agent_um['user-profile']
                    user_sharing_model = agent_um['sharing-model']
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
                if allowed and not check_user_sharing_model(user_sharing_model):
                    allowed = False
                    LOG.debug("LIFECYCLE: agent_decision: user_management: agent not allowed: " + str(agent))

                if allowed:
                    l_filtered_agents.append(agent)
        service_instance['agents'] = l_filtered_agents

        return service_instance
    except:
        LOG.exception('LIFECYCLE: agent_decision: user_management: Exception')
        return None


###############################################################################
## QOS PROVIDING
#
#  SERVICE INSTANCE:
#    {
#        ...
#        "agents": [{"agent": resource-link, "url": "192.168.1.31", "ports": [8081], "container_id": "10asd673f", "status": "waiting",
#                "num_cpus": 3, "allow": true, "master_compss": true, "app_type": "swarm"}, ...]
#    }
#
# OUTPUT FROM LQoS PROVIDING:
#   {
#       ...
#       "agents": [{'allow': False, 'url': '192.168.252.41'}, ...]
#   }


# check_qos:
def check_qos(agent_resp):
    if not agent_resp['allow']:
        return True # TODO return False
    return True


# qos_providing: call to QoS PROVIDING
def qos_providing(service_instance):
    try:
        LOG.debug("LIFECYCLE: agent_decision: qos_providing ############################")
        LOG.debug("LIFECYCLE: agent_decision: qos_providing: (1): " + str(service_instance))

        service_instance_resp = mf2c.service_management_qos(service_instance)
        LOG.debug("LIFECYCLE: agent_decision: qos_providing: service_instance_resp: " + str(service_instance_resp))

        if service_instance_resp is not None:
            try:
                l_filtered_agents = []
                LOG.debug("LIFECYCLE: agent_decision: qos_providing: processing response...")
                for agent_resp in service_instance_resp["agents"]:
                    for agent in service_instance["agents"]:
                        if agent['url'] == agent_resp['url'] and check_qos(agent_resp):
                            l_filtered_agents.append(agent)
            except:
                LOG.exception('LIFECYCLE: agent_decision: qos_providing: Exception while processing response')
                return None
            service_instance['agents'] = l_filtered_agents

        LOG.debug("LIFECYCLE: agent_decision: qos_providing: (2): " + str(service_instance))
        return service_instance
    except:
        LOG.exception('LIFECYCLE: agent_decision: qos_providing: Exception')
        return None


###############################################################################


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
            service_instance_res = qos_providing(service_instance)
            if not service_instance_res is None:
                service_instance = service_instance_res

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
        LOG.exception('LIFECYCLE: agent_decision: select_agents: Exception')
        return None