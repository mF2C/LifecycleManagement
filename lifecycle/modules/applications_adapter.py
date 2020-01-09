"""
Common adapter: Applications' allocation, deployment and exectution adapter
This is being developed for the MF2C Project: http://www.mf2c-project.eu/

Copyright: Atos Research and Innovation, 2017.

This code is licensed under an Apache 2.0 license. Please, refer to the LICENSE.TXT file for more information

Created on 09 feb. 2018

@author: Roi Sucasas - ATOS
"""

from lifecycle.connectors import connector as connector
from lifecycle.modules.apps.docker import adapter as docker_adpt
from lifecycle.modules.apps.swarm import adapter as swarm_adpt
from lifecycle.modules.apps.swarm.compose import adapter as swarm_compose_adpt
from lifecycle.modules.apps.kubernetes import adapter as k8s_adpt
from lifecycle.modules.apps.compss import adapter as compss_adpt
from lifecycle.common import SERVICE_KUBERNETES, SERVICE_DOCKER_SWARM, SERVICE_DOCKER_COMPOSE_SWARM, STATUS_ERROR


# Deploy / allocate service
# TODO k8s, swarm
def deploy_service_agent(service, service_instance, agent):
    if service['exec_type'] == SERVICE_KUBERNETES:
        return k8s_adpt.deploy_service(service, agent)
    elif service['exec_type'] == SERVICE_DOCKER_SWARM:
        return swarm_adpt.deploy_service_agent(service, agent)
    elif service['exec_type'] == SERVICE_DOCKER_COMPOSE_SWARM:
        return swarm_compose_adpt.deploy_service_agent(service, agent)
    else: # SERVICE_DOCKER, SERVICE_DOCKER_COMPOSE, SERVICE_COMPSS
        return docker_adpt.deploy_service_agent(service, service_instance, agent)


# Stop service in agent
# TODO k8s, swarm
def stop_service_agent(service, agent):
    if service['exec_type'] == SERVICE_KUBERNETES:
        return docker_adpt.stop_service_agent(agent)
    elif service['exec_type'] == SERVICE_DOCKER_SWARM:
        return swarm_adpt.stop_service_agent(agent)
    elif service['exec_type'] == SERVICE_DOCKER_COMPOSE_SWARM:
        return swarm_compose_adpt.stop_service_agent(service, agent)
    else: # SERVICE_DOCKER, SERVICE_DOCKER_COMPOSE, SERVICE_COMPSS
        if docker_adpt.stop_service_agent(agent) != STATUS_ERROR:
            connector.user_management_set_um_properties(apps=-1)


# Start service in agent
# TODO k8s, swarm
def start_service_agent(service, agent):
    if service['exec_type'] == SERVICE_KUBERNETES:
        return docker_adpt.start_service_agent(agent)
    elif service['exec_type'] == SERVICE_DOCKER_SWARM or service['exec_type'] == SERVICE_DOCKER_COMPOSE_SWARM:
        return swarm_adpt.start_service_agent(agent)
    else: # SERVICE_DOCKER, SERVICE_DOCKER_COMPOSE, SERVICE_COMPSS
        if docker_adpt.start_service_agent(agent) != STATUS_ERROR:
            connector.user_management_set_um_properties(apps=1)


# terminate service in agent
# TODO k8s, swarm
def terminate_service_agent(service, agent):
    if service['exec_type'] == SERVICE_KUBERNETES:
        return docker_adpt.terminate_service_agent(agent)
    elif service['exec_type'] == SERVICE_DOCKER_COMPOSE_SWARM:
        return swarm_compose_adpt.terminate_service_agent(service, agent)
    elif service['exec_type'] == SERVICE_DOCKER_SWARM:
        return swarm_adpt.terminate_service_agent(agent)
    else: # SERVICE_DOCKER, SERVICE_DOCKER_COMPOSE, SERVICE_COMPSS
        return docker_adpt.terminate_service_agent(agent)


# start_job_compss: Starts job in one agent
def start_job_compss(service_instance, body):
    return compss_adpt.start_job(service_instance, body)


# start_job_compss_multiple_agents: Starts job in multiple agents
def start_job_compss_multiple_agents(service_instance, body):
    return compss_adpt.start_job_in_agents(service_instance, body)