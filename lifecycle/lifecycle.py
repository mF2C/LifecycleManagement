"""
Lifecycle processes, including all service operations (submission, execution, start, stop ...)
This is being developed for the MF2C Project: http://www.mf2c-project.eu/

Copyright: Atos Research and Innovation, 2017.

This code is licensed under an Apache 2.0 license. Please, refer to the LICENSE.TXT file for more information

Created on 09 feb. 2018

@author: Roi Sucasas - ATOS
"""

import lifecycle.modules.agent_decision as agent_decision
import lifecycle.modules.allocation_adapter as allocation_adapter
import lifecycle.modules.execution_adapter as execution_adapter
import lifecycle.modules.sla_adapter as sla_adapter
import lifecycle.modules.adapters.lf_adapter as lf_adapter
import lifecycle.utils.common as common
import lifecycle.mF2C.data as data
from lifecycle.utils.logs import LOG


# Submits a service
# IN:
#   Service example:
#       {
#           "service_id": "service_id",
#           "service_path": "yeasy/simple-web"
#           ...
#       }
# OUT:
#   Service instance (example):
#       {
#           "service_instance_id": "service_id",
#           "service_id": service['service_id'],
#           "list_of_agents": agents_list,
#           "status": "",
#           ("service": service)
#       }
def submit(service):
    try:
        LOG.debug("Lifecycle-Management: Lifecycle: submit: " + str(service))

        # 1. get container path (service)
        if 'service_path' not in service:
            # error
            LOG.debug("Lifecycle-Management: Lifecycle: submit: (container) service_path not found")

        # 2. get list of available agents / resources / VMs
        available_agents_list = agent_decision.get_available_agents_list(service)
        if not available_agents_list:
            # error
            LOG.debug("Lifecycle-Management: Lifecycle: submit: available_agents_list is None")

        elif len(available_agents_list) == 0:
            # no resurces / agents found
            LOG.debug("Lifecycle-Management: Lifecycle: submit: available_agents_list is empty")

        else:
            # 3. select from agents list and Create new service instance
            agents_list = agent_decision.select_agents_list(available_agents_list)
            LOG.debug("Lifecycle-Management: Lifecycle: submit: available_agents_list" + str(available_agents_list))

            service_instance = data.create_service_instance(service, agents_list)
            LOG.debug("Lifecycle-Management: Lifecycle: submit: service_instance" + str(service_instance))

            # 3. allocate service / call remote container
            # allocate
            if allocation_adapter.allocate(service_instance):
                # initializes SLA
                sla_adapter.initializes_sla(service_instance)
                # executes service
                execution_adapter.execute(service_instance)

        return service_instance
    except:
        LOG.error('Lifecycle-Management: Lifecycle: submit: Exception')
        return common.gen_response(500, 'Exception', 'service', str(service))



# Service Operation: start
def start(service_instance_id):
    try:
        LOG.info("Lifecycle-Management: Operations: start service: " + service_instance_id)

        status = lf_adapter.start(service_instance_id)
        return common.gen_response_ok('Start service', 'service_instance_id', service_instance_id, 'status', status)
    except:
        LOG.error('Lifecycle-Management: Operations: start: Exception')
        return common.gen_response(500, 'Exception', 'service_instance_id', service_instance_id)


# Service Operation: restart
def restart(service_instance_id):
    try:
        LOG.info("Lifecycle-Management: Operations: restart: " + service_instance_id)

        status = lf_adapter.restart(service_instance_id)
        return common.gen_response_ok('Restart service', 'service_instance_id', service_instance_id, 'status', status)
    except:
        LOG.error('Lifecycle-Management: Operations: restart: Exception')
        return common.gen_response(500, 'Exception', 'service_instance_id', service_instance_id)


# Service Operation: stop
def stop(service_instance_id):
    try:
        LOG.info("Lifecycle-Management: Operations: stop: " + service_instance_id)

        status = lf_adapter.stop(service_instance_id)
        return common.gen_response_ok('Stop service', 'service_instance_id', service_instance_id, 'status', status)
    except:
        LOG.error('Lifecycle-Management: Operations: stop: Exception')
        return common.gen_response(500, 'Exception', 'service_instance_id', service_instance_id)


# Terminate service, Deallocate service's resources
def terminate(service_instance_id):
    try:
        LOG.info("Lifecycle-Management: Operations: terminate: " + service_instance_id)

        status = lf_adapter.terminate_service(service_instance_id)
        return common.gen_response_ok('Terminate service', 'service_instance_id', service_instance_id, 'status', status)
    except:
        LOG.error('Lifecycle-Management: Operations: terminate: Exception')
        return common.gen_response(500, 'Exception', 'service_instance_id', service_instance_id)


# Get service status
def get(service_instance_id):
    try:
        LOG.info("Lifecycle-Management: Operations: get: " + service_instance_id)

        return common.gen_response_ok('Service instance content', 'service_instance_id', service_instance_id,
                                      'service_instance', data.get_service_instance(service_instance_id))
    except:
        LOG.error('Lifecycle-Management: Operations: get: Exception')
        return common.gen_response(500, 'Exception', 'service_instance_id', service_instance_id)