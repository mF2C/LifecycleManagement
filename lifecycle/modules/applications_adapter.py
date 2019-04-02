"""
Common adapter: Applications' allocation, deployment and exectution adapter
This is being developed for the MF2C Project: http://www.mf2c-project.eu/

Copyright: Atos Research and Innovation, 2017.

This code is licensed under an Apache 2.0 license. Please, refer to the LICENSE.TXT file for more information

Created on 09 feb. 2018

@author: Roi Sucasas - ATOS
"""


import lifecycle.modules.apps.docker.adapter as docker_adpt
import lifecycle.modules.apps.swarm.adapter as swarm_adpt
import lifecycle.modules.apps.kubernetes.adapter as k8s_adpt
import lifecycle.modules.apps.compss.adapter as compss_adpt
from common.common import SERVICE_DOCKER, SERVICE_DOCKER_COMPOSE, SERVICE_COMPSS, SERVICE_KUBERNETES, SERVICE_DOCKER_SWARM, STATUS_ERROR
import lifecycle.data.mF2C.mf2c as mf2c


# Deploy / allocate service
# TODO k8s, swarm
def deploy_service_agent(service, agent):
    if service['exec_type'] == SERVICE_KUBERNETES:
        return k8s_adpt.deploy_service(service, agent)
    elif service['exec_type'] == SERVICE_DOCKER_SWARM:
        return swarm_adpt.deploy_service_agent(service, agent)
    else: # SERVICE_DOCKER, SERVICE_DOCKER_COMPOSE, SERVICE_COMPSS
        return docker_adpt.deploy_service_agent(service, agent)


# Stop service in agent
# TODO k8s, swarm
def stop_service_agent(service, agent):
    if service['exec_type'] == SERVICE_KUBERNETES:
        return docker_adpt.stop_service_agent(agent)
    elif service['exec_type'] == SERVICE_DOCKER_SWARM:
        return swarm_adpt.stop_service_agent(agent)
    else: # SERVICE_DOCKER, SERVICE_DOCKER_COMPOSE, SERVICE_COMPSS
        if docker_adpt.stop_service_agent(agent) != STATUS_ERROR:
            mf2c.user_management_set_um_properties(apps=-1)


# Start service in agent
# TODO k8s, swarm
def start_service_agent(service, agent):
    if service['exec_type'] == SERVICE_KUBERNETES:
        return docker_adpt.start_service_agent(agent)
    elif service['exec_type'] == SERVICE_DOCKER_SWARM:
        return swarm_adpt.start_service_agent(agent)
    else: # SERVICE_DOCKER, SERVICE_DOCKER_COMPOSE, SERVICE_COMPSS
        if docker_adpt.start_service_agent(agent) != STATUS_ERROR:
            mf2c.user_management_set_um_properties(apps=1)


# terminate service in agent
# TODO k8s, swarm
def terminate_service_agent(service, agent):
    if service['exec_type'] == SERVICE_KUBERNETES:
        return docker_adpt.terminate_service_agent(agent)
    elif service['exec_type'] == SERVICE_DOCKER_SWARM:
        return swarm_adpt.terminate_service_agent(agent)
    else: # SERVICE_DOCKER, SERVICE_DOCKER_COMPOSE, SERVICE_COMPSS
        return docker_adpt.terminate_service_agent(agent)


# start_job_compss: Starts job in one agent
def start_job_compss_OLD(service_instance_id, agent, parameters):
    return compss_adpt.start_job(service_instance_id, agent, parameters)


# start_job_compss: Starts job in one agent
def start_job_compss(service_instance_id, body, agent):
    return compss_adpt.start_job(service_instance_id, body, agent)


# start_job_compss_multiple_agents: Starts job in multiple agents
def start_job_compss_multiple_agents_OLD(service_instance, parameters):
    return compss_adpt.start_job_in_agents(service_instance, parameters)


# start_job_compss_multiple_agents: Starts job in multiple agents
def start_job_compss_multiple_agents(service_instance, body):
    return compss_adpt.start_job_in_agents(service_instance, body)