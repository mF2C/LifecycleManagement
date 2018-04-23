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
import lifecycle.mF2C.mf2c as mf2c
from lifecycle.utils.logs import LOG


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

 SERVICE INSTANCE:
   {
       ...
       "id": "",
       "user": "testuser",
       "service": "",
       "agreement": "",
       "status": "waiting",
       "agents": [
           {"agent": resource-link, "url": "192.168.1.31", "port": 8081, "container_id": "10asd673f", "status": "waiting",
               "num_cpus": 3, "allow": true, "master_compss": true},
           {"agent": resource-link, "url": "192.168.1.34", "port": 8081, "container_id": "99asd673f", "status": "waiting",
               "num_cpus": 2, "allow": true, "master_compss": false}
      ]
   }
'''


# check_service_content:
def check_service_content(service):
    if 'category' not in service or 'exec_type' not in service or 'exec' not in service:
        LOG.debug("Lifecycle-Management: Lifecycle: check_service_content: fields category/exec/exec_type not found")
        return False
    return True


# submit_service_in_agents: Submits a service (no access to external docker APIs; calls to other agent's lifecycle components)
#   agents_list:    [{"agent_ip": "192.168.252.41", "num_cpus": 4},
#                    {"agent_ip": "192.168.252.42", "num_cpus": 2},
#                    {"agent_ip": "192.168.252.43", "num_cpus": 2}]
# IN: service, user_id, agreement_id, agents_list
# OUT: service_instance
def submit_service_in_agents(service, user_id, agreement_id, agents_list, check_service=False):
    LOG.debug("Lifecycle-Management: Lifecycle: submit_v2: " + str(service) + ", user_id: " + user_id)
    try:
        # 1. check parameters content
        if check_service and not check_service_content(service):
            return common.gen_response(500, 'field(s) category/exec/exec_type not found', 'service', str(service))

        # 2. create new service instance
        LOG.debug("Lifecycle-Management: Lifecycle: submit_v2: agents_list" + str(agents_list))

        service_instance = data.create_service_instance(service, agents_list, user_id, agreement_id)
        if not service_instance:
            LOG.error("Lifecycle-Management: Lifecycle: submit_service_in_agents: error creating service_instance")
            return common.gen_response(500, 'error creating service_instance', 'service', str(service))

        # 3. select from agents list
        r = agent_decision.select_agents(service_instance)
        if not r is None:
            service_instance = r

        LOG.debug("Lifecycle-Management: Lifecycle: submit_service_in_agents: service_instance: " + str(service_instance))

        # 3. allocate service / call remote container
        # allocate
        #   Agent example:
        #    {"agent": resource-link, "url": "192.168.1.31", "port": 8081, "container_id": "10asd673f", "status": "waiting",
        #     "num_cpus": 3, "allow": true}
        for agent in service_instance["agents"]:
            LOG.info(">>> AGENT >>> " + agent['url'])
            # LOCAL
            if agent['url'] == common.get_ip():
                LOG.debug("Lifecycle-Management: Lifecycle: submit_service_in_agents: allocate service locally")
                if allocation_adapter.allocate_service_agent(service, agent) == "waiting":
                    LOG.debug("Lifecycle-Management: Lifecycle: submit_service_in_agents: SLA & service exec")
                    # initializes SLA
                    sla_adapter.initializes_sla(service_instance, agreement_id)
                    # executes service
                    execution_adapter.execute_service_agent(service, agent)
            # OTHER AGENT
            elif common.check_ip(agent['url']):
                LOG.debug("Lifecycle-Management: Lifecycle: submit_service_in_agents: allocate service in other agent [" + agent['url'] + "]")
                #  call lifecycle from x
                mf2c.lifecycle_deploy(service, agent)
            # NOT FOUND / NOT CONNECTED
            else:
                agent['status'] = "error"
                LOG.error("Lifecycle-Management: Lifecycle: submit_service_in_agents: agent [" + agent['url'] + "] cannot be reached")

        # 4. save / update service_instance
        LOG.debug("Lifecycle-Management: Lifecycle: submit_service_in_agents: UPDATING service_instance: " + str(service_instance))
        data.update_service_instance(service_instance['id'], service_instance)

        return common.gen_response_ok('Deploy service', 'service_instance', service_instance)
    except:
        LOG.error('Lifecycle-Management: Lifecycle: submit_service_in_agents: Exception')
        return common.gen_response(500, 'Exception', 'service', str(service))


# submit: Submits a service (no access to external docker APIs; calls to other agent's lifecycle components)
# IN: service, user_id, agreement_id
# OUT: service_instance
def submit(service, user_id, agreement_id):
    LOG.debug("Lifecycle-Management: Lifecycle: submit_v2: " + str(service) + ", user_id: " + user_id)
    try:
        # 1. check parameters content
        if not check_service_content(service):
            return common.gen_response(500, 'field(s) category/exec/exec_type not found', 'service', str(service))

        # 2. get list of available agents / resources / VMs. Example: TODO!!!
        #   [{"agent_ip": "192.168.252.41", "num_cpus": 4},
        #    {"agent_ip": "192.168.252.42", "num_cpus": 2},
        #    {"agent_ip": "192.168.252.43", "num_cpus": 2}]
        available_agents_list = agent_decision.get_available_agents_list(service)   # TODO call to landscaper/reommender
        if not available_agents_list:
            # error
            LOG.error("Lifecycle-Management: Lifecycle: submit_v2: available_agents_list is None")
            return common.gen_response(500, 'available_agents_list is None', 'service', str(service))
        elif len(available_agents_list) == 0:
            # no resurces / agents found
            LOG.error("Lifecycle-Management: Lifecycle: submit_v2: available_agents_list is empty")
            return common.gen_response(500, 'available_agents_list is empty', 'service', str(service))
        else:
            # 3. Create new service instance & allocate service / call other agents when needed
            return submit_service_in_agents(service, user_id, agreement_id, available_agents_list)
    except:
        LOG.error('Lifecycle-Management: Lifecycle: submit_v2: Exception')
        return common.gen_response(500, 'Exception', 'service', str(service))


# Service Operation: start (version 2: no access to external docker APIs / calls to other agent's lifecycle components)
def start(service_instance_id):
    LOG.debug("Lifecycle-Management: Lifecycle: start_v2: " + service_instance_id)
    try:
        # 1. get service_instance object
        service_instance = data.get_service_instance(service_instance_id)
        if not service_instance:
            return common.gen_response(500, 'Error getting service instance object', 'service_instance_id', service_instance_id)

        # 2. start service in all agents
        for agent in service_instance["agents"]:
            LOG.info(">>> AGENT >>> " + agent['url'])
            # LOCAL
            if agent['url'] == common.get_ip():
                LOG.debug("Lifecycle-Management: Lifecycle: start_v2: start service locally")
                lf_adapter.start_service_agent(None, agent)
            # OTHER AGENT
            elif common.check_ip(agent['url']):
                LOG.debug("Lifecycle-Management: Lifecycle: start_v2: start service in other agent")
                #  call lifecycle from x
                mf2c.lifecycle_operation(agent, "start")
            # NOT FOUND / NOT CONNECTED
            else:
                agent['status'] = "error"
                LOG.error("Lifecycle-Management: Lifecycle: start_v2: agent [" + agent['url'] + "] cannot be reached")

        return common.gen_response_ok('Start service', 'service_instance_id', service_instance_id,
                                      'service_instance', str(service_instance))
    except:
        LOG.error('Lifecycle-Management: Lifecycle: start_v2: Exception')
        return common.gen_response(500, 'Exception', 'service_instance_id', service_instance_id)


# Service Operation: restart (version 2: no access to external docker APIs / calls to other agent's lifecycle components)
def restart(service_instance_id):
    LOG.debug("Lifecycle-Management: Lifecycle: restart_v2: " + service_instance_id)
    try:
        # 1. get service_instance object
        service_instance = data.get_service_instance(service_instance_id)
        if not service_instance:
            return common.gen_response(500, 'Error getting service instance object', 'service_instance_id', service_instance_id)

        # 2. restart service in all agents
        for agent in service_instance["agents"]:
            LOG.info(">>> AGENT >>> " + agent['url'])
            # LOCAL
            if agent['url'] == common.get_ip():
                LOG.debug("Lifecycle-Management: Lifecycle: restart_v2: start service locally")
                lf_adapter.restart_service_agent(None, agent)
            # OTHER AGENT
            elif common.check_ip(agent['url']):
                LOG.debug("Lifecycle-Management: Lifecycle: restart_v2: start service in other agent")
                #  call lifecycle from x
                mf2c.lifecycle_operation(agent, "restart")
            # NOT FOUND / NOT CONNECTED
            else:
                agent['status'] = "error"
                LOG.error("Lifecycle-Management: Lifecycle: restart_v2: agent [" + agent['url'] + "] cannot be reached")

        return common.gen_response_ok('Restart service', 'service_instance_id', service_instance_id,
                                      'service_instance', str(service_instance))
    except:
        LOG.error('Lifecycle-Management: Lifecycle: restart_v2: Exception')
        return common.gen_response(500, 'Exception', 'service_instance_id', service_instance_id)


# Service Operation: stop (version 2: no access to external docker APIs / calls to other agent's lifecycle components)
def stop(service_instance_id):
    LOG.info("Lifecycle-Management: Lifecycle: stop_v2: " + service_instance_id)
    try:
        # 1. get service_instance object
        service_instance = data.get_service_instance(service_instance_id)
        if not service_instance:
            return common.gen_response(500, 'Error getting service instance object', 'service_instance_id', service_instance_id)

        # 2. stop service in all agents
        for agent in service_instance["agents"]:
            LOG.info(">>> AGENT >>> " + agent['url'])
            # LOCAL
            if agent['url'] == common.get_ip():
                LOG.debug("Lifecycle-Management: Lifecycle: stop_v2: start service locally")
                lf_adapter.stop_service_agent(None, agent)
            # OTHER AGENT
            elif common.check_ip(agent['url']):
                LOG.debug("Lifecycle-Management: Lifecycle: stop_v2: start service in other agent")
                #  call lifecycle from x
                mf2c.lifecycle_operation(agent, "stop")
            # NOT FOUND / NOT CONNECTED
            else:
                agent['status'] = "error"
                LOG.error("Lifecycle-Management: Lifecycle: stop_v2: agent [" + agent['url'] + "] cannot be reached")

        # 3. deletes service_instance from cimi
        obj_response_cimi = common.ResponseCIMI()
        resp = data.del_service_instance(service_instance_id, obj_response_cimi)
        if not resp is None and resp != -1:
            LOG.debug('Service instance deleted from CIMI')
        else:
            LOG.error("Error: Service instance NOT deleted from CIMI")

        return common.gen_response_ok('Stop service', 'service_instance_id', service_instance_id,
                                      'service_instance', str(service_instance))
    except:
        LOG.error('Lifecycle-Management: Lifecycle: stop_v2: Exception')
        return common.gen_response(500, 'Exception', 'service_instance_id', service_instance_id)


# Service Instance Operation: starts a job / app
# TODO get agent with compss master
def start_job(data):
    LOG.debug("Lifecycle-Management: Lifecycle: start_job: " + str(data))
    try:
        service_instance = data.get_service_instance(data['service_instance_id'])
        agent = service_instance['agents'][0]
        LOG.debug("Lifecycle-Management: Lifecycle: start_job: Starting job in agent [" + str(agent) + "] ...")

        res = lf_adapter.start_job(agent, data['parameters'])
        return common.gen_response_ok('Start job', 'service_id', data['service_instance_id'], 'res', res)
    except:
        LOG.error('Lifecycle-Management: Lifecycle: start_job: Exception')
        return common.gen_response(500, 'Exception', 'data', str(data))


# Terminate service, Deallocate service's resources
def terminate(service_id):
    LOG.debug("Lifecycle-Management: Lifecycle: terminate: " + service_id)
    try:
        status = lf_adapter.terminate_service(service_id)
        return common.gen_response_ok('Terminate service', 'service_id', service_id, 'status', status)
    except:
        LOG.error('Lifecycle-Management: Lifecycle: terminate: Exception')
        return common.gen_response(500, 'Exception', 'service_id', service_id)


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


# Delete service instance from CIMI
def delete(service_instance_id):
    LOG.debug("Lifecycle-Management: Lifecycle: delete: " + service_instance_id)
    try:
        obj_response_cimi = common.ResponseCIMI()
        resp = data.del_service_instance(service_instance_id, obj_response_cimi)

        if not resp is None:
            return common.gen_response_ok('Service instance content', 'service_instance_id', service_instance_id,
                                          'Response', resp['message'])
        else:
            return common.gen_response(500, "Error in 'delete' function",
                                       "service_instance_id", service_instance_id,
                                       "Error_Msg", obj_response_cimi.msj)
    except:
        LOG.error('Lifecycle-Management: Lifecycle: delete: Exception')
        return common.gen_response(500, 'Exception', 'service_instance_id', service_instance_id)