"""
Common adapter
This is being developed for the MF2C Project: http://www.mf2c-project.eu/

Copyright: Atos Research and Innovation, 2017.

This code is licensed under an Apache 2.0 license. Please, refer to the LICENSE.TXT file for more information

Created on 09 feb. 2018

@author: Roi Sucasas - ATOS
"""


import lifecycle.modules.adapters.docker.adapter as docker_adpt
import lifecycle.modules.adapters.compss.adapter as compss_adpt


# Deploy / allocate service
def deploy_service_agent(service, agent):
    return docker_adpt.deploy_service_agent(service, agent)


# Stop service in agent
def stop_service_agent(service, agent):
    return docker_adpt.stop_service_agent(agent)


# Start service in agent
def start_service_agent(service, agent):
    return docker_adpt.start_service_agent(agent)


# terminate service in agent
def terminate_service_agent(service, agent):
    return docker_adpt.terminate_service_agent(agent)


# start_job_compss: Starts job in one agent
def start_job_compss(service_instance_id, agent, parameters):
    return compss_adpt.start_job(service_instance_id, agent, parameters)


# start_job_compss_multiple_agents: Starts job in multiple agents
def start_job_compss_multiple_agents(service_instance, parameters):
    return compss_adpt.start_job_in_agents(service_instance, parameters)