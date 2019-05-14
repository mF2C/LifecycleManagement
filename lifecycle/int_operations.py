"""
Internal Lifecycle operations (deployment, execution, start, stop ...). Internal calls between Lifecycles from different agents.
This is being developed for the MF2C Project: http://www.mf2c-project.eu/

Copyright: Atos Research and Innovation, 2017.

This code is licensed under an Apache 2.0 license. Please, refer to the LICENSE.TXT file for more information

Created on 09 feb. 2018

@author: Roi Sucasas - ATOS
"""

from lifecycle.modules import applications_adapter as apps_adapter
from lifecycle import common as common
from lifecycle.logs import LOG


# Deploy service in an agent
# IN: - Service
#    - Agent
def deploy(service, service_instance, agent):
    LOG.debug("[lifecycle.int_operations] [deploy] " + str(service) + ", service_instance: " + str(service_instance) + ", agent: " + str(agent))
    return apps_adapter.deploy_service_agent(service, service_instance, agent)


# Service Operation: start
def start(service, agent):
    LOG.info("[lifecycle.int_operations] [start] " + str(service) + ", agent: " + str(agent))
    try:
        status = apps_adapter.start_service_agent(service, agent)
        return common.gen_response_ok('Start service', 'agent', str(agent), 'status', status)
    except:
        LOG.exception('[lifecycle.int_operations] [start] Exception')
        return common.gen_response(500, 'Exception', 'agent', str(agent))


# Service Operation: stop
def stop(service, agent):
    LOG.info("[lifecycle.int_operations] [stop] " + str(service) + ", agent: " + str(agent))
    try:
        status = apps_adapter.stop_service_agent(service, agent)
        return common.gen_response_ok('Stop service', 'agent', str(agent), 'status', status)
    except:
        LOG.exception('[lifecycle.int_operations] [stop] Exception')
        return common.gen_response(500, 'Exception', 'agent', str(agent))


# Service Operation: terminate
def terminate(service, agent):
    LOG.info("[lifecycle.int_operations] [terminate] " + str(service) + ", agent: " + str(agent))
    try:
        status = apps_adapter.terminate_service_agent(service, agent)
        return common.gen_response_ok('Terminate service', 'agent', str(agent), 'status', status)
    except:
        LOG.exception('[lifecycle.int_operations] [terminate] Exception')
        return common.gen_response(500, 'Exception', 'agent', str(agent))
