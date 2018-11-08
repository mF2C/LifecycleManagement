"""
Lifecycle operations (deployment, execution, start, stop ...)
This is being developed for the MF2C Project: http://www.mf2c-project.eu/

Copyright: Atos Research and Innovation, 2017.

This code is licensed under an Apache 2.0 license. Please, refer to the LICENSE.TXT file for more information

Created on 09 feb. 2018

@author: Roi Sucasas - ATOS
"""

import lifecycle.modules.allocation_adapter as allocation_adapter
import lifecycle.modules.adapters.lf_adapter as lf_adapter
import common.common as common
from common.logs import LOG


# Deploy service in an agent
# IN: - Service
#    - Agent
def deploy(service, agent):
    LOG.debug("Lifecycle-Management: Operations: deploy: " + str(service) + ", agent: " + str(agent))
    return allocation_adapter.allocate_service_agent(service, agent)


# Service Operation: start
def start(agent):
    LOG.info("Lifecycle-Management: Operations: start service: " + str(agent))
    try:
        status = lf_adapter.start_service_agent(None, agent)
        return common.gen_response_ok('Start service', 'agent', str(agent), 'status', status)
    except:
        LOG.error('Lifecycle-Management: Operations: start: Exception')
        return common.gen_response(500, 'Exception', 'agent', str(agent))


# Service Operation: stop
def stop(agent):
    LOG.info("Lifecycle-Management: Operations: stop: " + str(agent))
    try:
        status = lf_adapter.stop_service_agent(None, agent)
        return common.gen_response_ok('Stop service', 'agent', str(agent), 'status', status)
    except:
        LOG.error('Lifecycle-Management: Operations: stop: Exception')
        return common.gen_response(500, 'Exception', 'agent', str(agent))


# Service Operation: terminate
def terminate(agent):
    LOG.info("Lifecycle-Management: Operations: terminate: " + str(agent))
    try:
        status = lf_adapter.terminate_service_agent(None, agent)
        return common.gen_response_ok('Terminate service', 'agent', str(agent), 'status', status)
    except:
        LOG.error('Lifecycle-Management: Operations: terminate: Exception')
        return common.gen_response(500, 'Exception', 'agent', str(agent))
