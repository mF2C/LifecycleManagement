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
import common.common as common
import lifecycle.mF2C.data as data
import lifecycle.mF2C.mf2c as mf2c
from common.logs import LOG
from common.common import OPERATION_START, OPERATION_STOP, OPERATION_RESTART, OPERATION_TERMINATE, \
    OPERATION_START_JOB, STATUS_ERROR, STATUS_NOT_DEPLOYED, STATUS_WAITING, STATUS_STARTED, STATUS_STOPPED, \
    STATUS_TERMINATED, STATUS_UNKNOWN


'''
 Data managed by this component:
 SERVICE:
       {
           "name": "hello-world",
           "description": "Hello World Service",
           "resourceURI": "/hello-world",
           "exec": "hello-world",
           "exec_type": "docker",
           "exec_ports": ["8080", "8081"],
           "category": {
               "cpu": "low",
               "memory": "low",
               "storage": "low",
               "inclinometer": false,
               "temperature": false,
               "jammer": false,
               "location": false
           }
       }
       
       "exec_type": "docker" ........... "exec" = docker image (docker hub)
                    "compss" ........... "exec" = docker image based on COMPSs (docker hub)
                    "docker-compose" ... "exec" = docker-compose.yml location
-----------------------------------------------------------------------------------------------
 SERVICE INSTANCE:
   {
       ...
       "id": "",
       "user": "testuser",
       "service": "",
       "agreement": "",
       "status": "waiting",
       "agents": [
           {"agent": resource-link, "url": "192.168.1.31", "ports": [8081], "container_id": "10asd673f", "status": "waiting",
               "num_cpus": 3, "allow": true, "master_compss": true},
           {"agent": resource-link, "url": "192.168.1.34", "ports": [8081], "container_id": "99asd673f", "status": "waiting",
               "num_cpus": 2, "allow": true, "master_compss": false}
      ]
   }
   
    Agent example: {"agent": resource-link, "url": "192.168.1.31", "ports": [8081], "container_id": "10asd673f", 
                    "status": "waiting", "num_cpus": 3, "allow": true, "master_compss": false}
-----------------------------------------------------------------------------------------------
 AGENTS_LIST:
    agents_list: [{"agent_ip": "192.168.252.41", "master_compss": true, "num_cpus": 4}, 
                  {"agent_ip": "192.168.252.42", "master_compss": false, "num_cpus": 2},
                  {"agent_ip": "192.168.252.43", "master_compss": false, "num_cpus": 2}]
   
'''


# check_service_content:
def check_service_content(service):
    if 'category' not in service or 'exec_type' not in service or 'exec' not in service:
        LOG.debug("Lifecycle-Management: Lifecycle: check_service_content: fields category/exec/exec_type not found")
        return False
    return True


###############################################################################
# DEPLOYMENT / SUBMIT:

# submit_service_in_agents: Submits a service (no access to external docker APIs; calls to other agent's lifecycle components)
# IN: service, user_id, agreement_id, agents_list
# OUT: service_instance
def submit_service_in_agents(service, user_id, agreement_id, agents_list, check_service=False):
    LOG.debug("Lifecycle-Management: Lifecycle: submit_service_in_agents: " + str(service) + ", user_id: " + user_id)
    try:
        # 1. check parameters content
        if check_service and not check_service_content(service):
            return common.gen_response(500, 'field(s) category/exec/exec_type not found', 'service', str(service))

        # 2. create new service instance
        LOG.debug("Lifecycle-Management: Lifecycle: submit_service_in_agents: agents_list" + str(agents_list))

        service_instance = data.create_service_instance(service, agents_list, user_id, agreement_id)
        if not service_instance:
            LOG.error("Lifecycle-Management: Lifecycle: submit_service_in_agents: error creating service_instance")
            return common.gen_response(500, 'error creating service_instance', 'service', str(service))

        # 3. select from agents list
        r = agent_decision.select_agents(service['exec_type'], service_instance)
        if not r is None:
            service_instance = r

        LOG.debug("Lifecycle-Management: Lifecycle: submit_service_in_agents: service_instance: " + str(service_instance))

        # 3. allocate service / call remote container
        for agent in service_instance["agents"]:
            LOG.info(">>> AGENT >>> " + agent['url'] + " <<<")
            # LOCAL
            if agent['url'] == common.get_local_ip():
                LOG.debug("Lifecycle-Management: Lifecycle: submit_service_in_agents: allocate service locally")
                # agent.update({"master_compss": True})
                resp_deploy = allocation_adapter.allocate_service_agent(service, agent)
                LOG.debug("Lifecycle-Management: Lifecycle: submit_service_in_agents: allocate service locally: "
                          "[resp_deploy=" + str(resp_deploy) + "]")
                if agent['status'] == "waiting":
                    LOG.debug("Lifecycle-Management: Lifecycle: submit_service_in_agents: execute service locally")
                    # executes service
                    execution_adapter.execute_service_agent(service, agent)
                else:
                    LOG.error("Lifecycle-Management: Lifecycle: submit_service_in_agents: allocate service locally: NOT DEPLOYED")
                    agent['status'] = "not-deployed"
                # agent.pop("master_compss", None)

            # 'REMOTE' AGENT: calls to lifecycle from remote agent
            elif common.check_ip(agent['url']):
                LOG.debug("Lifecycle-Management: Lifecycle: submit_service_in_agents: allocate service in remote agent [" + agent['url'] + "]")
                resp_deploy = mf2c.lifecycle_deploy(service, agent)
                if resp_deploy is not None:
                    agent['status'] = resp_deploy['status']
                    agent['container_id'] = resp_deploy['container_id']
                    agent['ports'] = resp_deploy['ports']
                    LOG.debug("Lifecycle-Management: Lifecycle: submit_service_in_agents: allocate service in remote agent: "
                              "[agent=" + str(agent) + "]")
                    # executes / starts service
                    resp_start = mf2c.lifecycle_operation(agent, "start")
                    if resp_start is not None:
                        agent['status'] = resp_start['status']
                        LOG.debug("Lifecycle-Management: Lifecycle: submit_service_in_agents: execute service in remote agent: "
                            "[agent=" + str(agent) + "]")
                else:
                    LOG.error("Lifecycle-Management: Lifecycle: submit_service_in_agents: allocate service in remote agent: NOT DEPLOYED")
                    agent['status'] = "not-deployed"

            # NOT FOUND / NOT CONNECTED
            else:
                agent['status'] = "error"
                LOG.error("Lifecycle-Management: Lifecycle: submit_service_in_agents: agent [" + agent['url'] + "] cannot be reached")

        # 4. initializes SLA
        if sla_adapter.initializes_sla(service_instance, agreement_id):
            LOG.debug("Lifecycle-Management: Lifecycle: submit_service_in_agents: sla agreement started")
        else:
            LOG.error("Lifecycle-Management: Lifecycle: submit_service_in_agents: sla agreement NOT started")

        # 5. save / update service_instance
        LOG.debug("Lifecycle-Management: Lifecycle: submit_service_in_agents: UPDATING service_instance: " + str(service_instance))
        service_instance['status'] = STATUS_STARTED
        data.update_service_instance(service_instance['id'], service_instance)

        return common.gen_response_ok('Deploy service', 'service_instance', service_instance)
    except:
        LOG.error('Lifecycle-Management: Lifecycle: submit_service_in_agents: Exception')
        return common.gen_response(500, 'Exception', 'service', str(service))


# submit: Submits a service (gets list of agents from mF2C components - recommender, landscaper - or from config)
# IN: service, user_id, agreement_id
# OUT: service_instance
def submit(service, user_id, agreement_id):
    LOG.debug("Lifecycle-Management: Lifecycle: submit_v2: " + str(service) + ", user_id: " + user_id)
    try:
        # 1. check parameters content
        if not check_service_content(service):
            return common.gen_response(500, 'field(s) category/exec/exec_type not found', 'service', str(service))

        # 2. get list of available agents / resources / VMs. Example:
        #   [{"agent_ip": "192.168.252.41", "num_cpus": 4, "master_compss": false}, {...}]
        # Call to landscaper/reommender
        available_agents_list = agent_decision.get_available_agents_resources(service)
        if not available_agents_list:
            # TODO forward to parent

            # error
            LOG.error("Lifecycle-Management: Lifecycle: submit_v2: available_agents_list is None")
            return common.gen_response(500, 'available_agents_list is None', 'service', str(service))
        elif len(available_agents_list) == 0:
            # TODO forward to parent

            # no resurces / agents found
            LOG.error("Lifecycle-Management: Lifecycle: submit_v2: available_agents_list is empty")
            return common.gen_response(500, 'available_agents_list is empty', 'service', str(service))
        else:
            # 3. Create new service instance & allocate service / call other agents when needed
            return submit_service_in_agents(service, user_id, agreement_id, available_agents_list)
    except:
        LOG.error('Lifecycle-Management: Lifecycle: submit_v2: Exception')
        return common.gen_response(500, 'Exception', 'service', str(service))


###############################################################################
# OPERATIONS:

# operation_service: start/stop/terminate service instance in agents
def operation_service(service_instance_id, operation):
    LOG.debug("Lifecycle-Management: Docker adapter: operation_service: [" + operation + "]: " + service_instance_id)
    try:
        # 1. get service_instance object
        service_instance = data.get_service_instance(service_instance_id)
        if not service_instance:
            return common.gen_response(500, 'Error getting service instance object', 'service_instance_id', service_instance_id)

        # 2. start service in all agents
        for agent in service_instance["agents"]:
            LOG.info(">>> AGENT >>> " + agent['url'] + " <<<")
            # LOCAL
            if agent['url'] == common.get_local_ip():
                if operation == OPERATION_START:
                    LOG.debug("Lifecycle-Management: Lifecycle: operation_service: start service locally")
                    lf_adapter.start_service_agent(None, agent)

                elif operation == OPERATION_STOP:
                    LOG.debug("Lifecycle-Management: Lifecycle: operation_service: stop service locally")
                    lf_adapter.stop_service_agent(None, agent)

                elif operation == OPERATION_TERMINATE:
                    LOG.debug("Lifecycle-Management: Lifecycle: operation_service: terminate service locally")
                    lf_adapter.terminate_service_agent(None, agent)

            # REMOTE AGENT (call lifecycle from agent)
            elif common.check_ip(agent['url']):
                if operation == OPERATION_START:
                    LOG.debug("Lifecycle-Management: Lifecycle: operation_service: start service in remote agent")
                    resp_start = mf2c.lifecycle_operation(agent, OPERATION_START)
                    if resp_start is not None:
                        agent['status'] = resp_start['status']
                        LOG.debug("Lifecycle-Management: Lifecycle: operation_service: result (start service): [agent=" + str(agent) + "]")
                    else:
                        agent['status'] = STATUS_UNKNOWN
                        LOG.error("Lifecycle-Management: Lifecycle: operation_service: result (start service): ERROR")

                elif operation == OPERATION_STOP:
                    LOG.debug("Lifecycle-Management: Lifecycle: operation_service: stop service in remote agent")
                    resp_stop = mf2c.lifecycle_operation(agent, OPERATION_STOP)
                    if resp_stop is not None:
                        agent['status'] = resp_stop['status']
                        LOG.debug("Lifecycle-Management: Lifecycle: operation_service: result (stop service): [agent=" + str(agent) + "]")
                    else:
                        agent['status'] = STATUS_UNKNOWN
                        LOG.error("Lifecycle-Management: Lifecycle: operation_service: result (stop service): ERROR")

                elif operation == OPERATION_TERMINATE:
                    LOG.debug("Lifecycle-Management: Lifecycle: operation_service: terminate service in remote agent")
                    resp_terminate = mf2c.lifecycle_operation(agent, OPERATION_TERMINATE)
                    if resp_terminate is not None:
                        agent['status'] = resp_terminate['status']
                        LOG.debug("Lifecycle-Management: Lifecycle: operation_service: result (terminate service): [agent=" + str(agent) + "]")
                    else:
                        agent['status'] = STATUS_UNKNOWN
                        LOG.error("Lifecycle-Management: Lifecycle: operation_service: result (terminate service): ERROR")

            # NOT FOUND / NOT CONNECTED
            else:
                agent['status'] = STATUS_ERROR
                LOG.error("Lifecycle-Management: Lifecycle: operation_service: agent [" + agent['url'] + "] cannot be reached")

        # 3. save / update / terminate service_instance
        LOG.debug("Lifecycle-Management: Lifecycle: operation_service: UPDATING service_instance [" + operation + "]: " + str(service_instance))
        if operation == OPERATION_START:
            service_instance['status'] = STATUS_STARTED
            data.update_service_instance(service_instance['id'], service_instance)                  # cimi
            sla_adapter.initializes_sla(service_instance, service_instance['agreement'])            # sla

        elif operation == OPERATION_STOP:
            service_instance['status'] = STATUS_STOPPED
            data.update_service_instance(service_instance['id'], service_instance)                  # cimi
            sla_adapter.stop_sla_agreement(service_instance, service_instance['agreement'])         # sla

        elif operation == OPERATION_TERMINATE:
            service_instance['status'] = STATUS_TERMINATED
            data.del_service_instance(service_instance['id'])                                       # cimi
            sla_adapter.terminate_sla_agreement(service_instance, service_instance['agreement'])    # sla

        # response
        return common.gen_response_ok(operation + " service", 'service_instance_id', service_instance_id,
                                      'service_instance', str(service_instance))
    except:
        LOG.error('Lifecycle-Management: Lifecycle: operation_service: Exception')
        return common.gen_response(500, 'Exception', 'service_instance_id', service_instance_id)


# Service Operation: start (version 2: no access to external docker APIs / calls to other agent's lifecycle components)
def start(service_instance_id):
    return operation_service(service_instance_id, OPERATION_START)


# Service Operation: stop (version 2: no access to external docker APIs / calls to other agent's lifecycle components)
def stop(service_instance_id):
    return operation_service(service_instance_id, OPERATION_STOP)


# Terminate service, Deallocate service's resources
def terminate(service_instance_id):
    LOG.debug("Lifecycle-Management: Lifecycle: terminate: " + service_instance_id)
    try:
        # 1. get service_instance object
        service_instance = data.get_service_instance(service_instance_id)
        if not service_instance:
            return common.gen_response(500, 'Error getting service instance object', 'service_instance_id', service_instance_id)

        # 2. service instance status = Stopped
        if service_instance['status'] != "Stopped":
            stop(service_instance_id)

        # 3. terminate
        return operation_service(service_instance_id, OPERATION_TERMINATE)
    except:
        LOG.error('Lifecycle-Management: Lifecycle: terminate: Exception')
        return common.gen_response(500, 'Exception', 'service_instance_id', service_instance_id)


# terminate_all
def terminate_all():
    if data.del_all_service_instances():
        return common.gen_response_ok('Terminate all services', 'result', 'True')
    else:
        return common.gen_response(500, 'Exception', 'result', 'False')


# Service Instance Operation: starts a job / app
def start_job(body, service_instance_id):
    LOG.debug("Lifecycle-Management: Lifecycle: start_job: " + str(body))
    LOG.debug("Lifecycle-Management: Lifecycle: start_job: [service_instance_id=" + service_instance_id + "]")
    try:
        # service instance
        service_instance = data.get_service_instance(service_instance_id)
        LOG.debug("Lifecycle-Management: Lifecycle: start_job: service_instance: " + str(service_instance))

        # start job in agent(s)
        if len(service_instance['agents']) == 1:
            res = lf_adapter.start_job_compss(body['service_instance_id'], service_instance['agents'][0], body['parameters'])
        elif len(service_instance['agents']) >= 2:
            res = lf_adapter.start_job_compss_multiple_agents(service_instance, body['parameters'])
        else:
            LOG.warning("Lifecycle-Management: Lifecycle: start_job: Execution supported in only 1 or more agents! agents size="
                        + str(len(service_instance['agents'])))
            res = None

        if res:
            return common.gen_response_ok('Start job', 'service_id', body['service_instance_id'], 'res', res)
        else:
            return common.gen_response(500, 'Error when starting job', 'service_instance', str(service_instance))
    except:
        LOG.error('Lifecycle-Management: Lifecycle: start_job: Exception')
        return common.gen_response(500, 'Exception', 'data', str(body))


# Get service instance
def get(service_instance_id):
    LOG.debug("Lifecycle-Management: Lifecycle: get: " + service_instance_id)
    try:
        obj_response_cimi = common.ResponseCIMI()
        service_instance = data.get_service_instance(service_instance_id, obj_response_cimi)

        if not service_instance is None and service_instance != -1:
            return common.gen_response_ok('Service instance content', 'service_instance_id', service_instance_id,
                                          'service_instance', service_instance)
        else:
            return common.gen_response(500, "Error in 'get' function",
                                       "service_instance_id", service_instance_id,
                                       "Error_Msg", obj_response_cimi.msj)
    except:
        LOG.error('Lifecycle-Management: Lifecycle: get: Exception')
        return common.gen_response(500, 'Exception', 'service_instance_id', service_instance_id)


# Get all service instances
def get_all():
    LOG.debug("Lifecycle-Management: Lifecycle: get_all ")
    try:
        obj_response_cimi = common.ResponseCIMI()
        service_instances = data.get_all_service_instances(obj_response_cimi)

        if not service_instances is None:
            return common.gen_response_ok('Service instances content', 'service_instances', service_instances,
                                          "Msg", obj_response_cimi.msj)
        else:
            return common.gen_response(500, "Error in 'get_all' function", "Error_Msg", obj_response_cimi.msj)
    except:
        LOG.error('Lifecycle-Management: Lifecycle: get_all: Exception')
        return common.gen_response(500, 'Exception', 'get_all', "-")

