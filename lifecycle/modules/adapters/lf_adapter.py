"""
Common adapter
This is being developed for the MF2C Project: http://www.mf2c-project.eu/

Copyright: Atos Research and Innovation, 2017.

This code is licensed under an Apache 2.0 license. Please, refer to the LICENSE.TXT file for more information

Created on 09 feb. 2018

@author: Roi Sucasas - ATOS
"""


import lifecycle.modules.adapters.docker_adapter as adpt
import lifecycle.modules.adapters.mf2c_compss_adapter as compss_adpt
import lifecycle.mF2C.data as data


# Deploy / allocate service
def deploy(service_instance):
    return adpt.deploy(service_instance)


# Deploy / allocate service
def deploy_service_agent(service, agent):
    return adpt.deploy_service_agent(service, agent)


# Terminate service
def terminate_service(service_instance_id):
    return adpt.terminate_service(data.get_service_instance(service_instance_id))


# Get service status
def get_status(service_instance_id):
    return adpt.get_status(data.get_service_instance(service_instance_id))


# Stop service
def stop(service_instance_id):
    return adpt.stop(data.get_service_instance(service_instance_id))


# Stop service in agent
def stop_service_agent(service, agent):
    return adpt.stop_service_agent(agent)


# Start service
def start(service_instance_id):
    return adpt.start(data.get_service_instance(service_instance_id))


# Start service in agent
def start_service_agent(service, agent):
    return adpt.start_service_agent(agent)


# Execute service
def execute(service_instance):
    return adpt.start(service_instance)


# Execute service in agent
def execute_service_agent(service, agent):
    return adpt.start_service_agent(agent)


# Restart service
def restart(service_instance_id):
    return adpt.restart(data.get_service_instance(service_instance_id))


# Restart service in agent
def restart_service_agent(service, agent):
    return adpt.restart_service_agent(agent)