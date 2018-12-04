"""
Internal Lifecycle operations (deployment, execution, start, stop ...). Internal calls between Lifecycles from different agents.
This is being developed for the MF2C Project: http://www.mf2c-project.eu/

Copyright: Atos Research and Innovation, 2017.

This code is licensed under an Apache 2.0 license. Please, refer to the LICENSE.TXT file for more information

Created on 09 feb. 2018

@author: Roi Sucasas - ATOS
"""

import lifecycle.modules.applications_adapter as apps_adapter
import common.common as common
from common.logs import LOG


# Deploy service in an agent
# IN: - Service
#    - Agent
def deploy(service, agent):
    LOG.debug("LIFECYCLE: Operations: deploy: " + str(service) + ", agent: " + str(agent))
    return apps_adapter.deploy_service_agent(service, agent)


# Service Operation: start
def start(agent):
    LOG.info("LIFECYCLE: Operations: start service: " + str(agent))
    try:
        status = apps_adapter.start_service_agent(None, agent)
        return common.gen_response_ok('Start service', 'agent', str(agent), 'status', status)
    except:
        LOG.error('LIFECYCLE: Operations: start: Exception')
        return common.gen_response(500, 'Exception', 'agent', str(agent))


# Service Operation: stop
def stop(agent):
    LOG.info("LIFECYCLE: Operations: stop: " + str(agent))
    try:
        status = apps_adapter.stop_service_agent(None, agent)
        return common.gen_response_ok('Stop service', 'agent', str(agent), 'status', status)
    except:
        LOG.error('LIFECYCLE: Operations: stop: Exception')
        return common.gen_response(500, 'Exception', 'agent', str(agent))


# Service Operation: terminate
def terminate(agent):
    LOG.info("LIFECYCLE: Operations: terminate: " + str(agent))
    try:
        status = apps_adapter.terminate_service_agent(None, agent)
        return common.gen_response_ok('Terminate service', 'agent', str(agent), 'status', status)
    except:
        LOG.error('LIFECYCLE: Operations: terminate: Exception')
        return common.gen_response(500, 'Exception', 'agent', str(agent))
