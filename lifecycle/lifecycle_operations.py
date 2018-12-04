"""
Lifecycle Operations: start/stop/terminate operations in 'parallel' mode
This is being developed for the MF2C Project: http://www.mf2c-project.eu/

Copyright: Atos Research and Innovation, 2017.

This code is licensed under an Apache 2.0 license. Please, refer to the LICENSE.TXT file for more information

Created on 04 dic. 2018

@author: Roi Sucasas - ATOS
"""

import sys, traceback
import threading
import lifecycle.modules.applications_adapter as apps_adapter
import lifecycle.modules.sla_adapter as sla_adapter
import common.common as common
import lifecycle.data.data_adapter as data_adapter
import lifecycle.data.mF2C.mf2c as mf2c
from common.logs import LOG
from common.common import OPERATION_START, OPERATION_STOP, OPERATION_TERMINATE, STATUS_ERROR, STATUS_STARTED, STATUS_STOPPED, \
    STATUS_TERMINATED, STATUS_UNKNOWN, STATUS_STARTING, STATUS_STOPPING, STATUS_TERMINATING


'''
 Data managed by this component:
 SERVICE:
    new version:
         {
            "name": "hello-world",
            "description": "Hello World Service",
            "exec": "hello-world",
            "exec_type": "docker",
            "exec_ports": [8080],
            "agent_type": "cloud",
            "num_agents": 1,
            "cpu_arch": "x86-64",
            "os": "linux", 
            "memory_min": 1000,
            "storage_min": 100, 
            "disk": 100, 
            "req_resource": ["Location", "Sentinel", "Ambulance"],
            "opt_resource": ["SenseHat", "GP-20U7"],
            "category": 3 
        }
        
    old version:
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
                    "docker-swarm" ..... "exec" =
                    "K8s" .............. "exec" =
-----------------------------------------------------------------------------------------------
 SERVICE INSTANCE:
   {
       ...
       "id": "",
       "user": "testuser",
       "service": "",
       "agreement": "",
       "status": "waiting",
       "service_type": "docker-swarm",
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
 AGENTS_LIST: (STANDALONE MODE)
    agents_list: [{"agent_ip": "192.168.252.41", "master_compss": true, "num_cpus": 4}, 
                  {"agent_ip": "192.168.252.42", "master_compss": false, "num_cpus": 2},
                  {"agent_ip": "192.168.252.43", "master_compss": false, "num_cpus": 2}]

 AGENTS_LIST: (landscaper/recommender)                
    available_agents_list: [{"agent_ip": "192.168.252.41"}, {"agent_ip": "192.168.252.42"}]

'''


# thr_operation_service_local: operation_service localhost
def thr_operation_service_local(operation, service, agent):
    try:
        LOG.debug("LIFECYCLE: Lifecycle_Operations: thr_operation_service_local: service operation: " + operation + " (localhost)")

        if operation == OPERATION_START:
            LOG.debug("LIFECYCLE: Lifecycle_Operations: thr_operation_service_local: start service locally: " + str(service) + ", agent: " + str(agent))
            apps_adapter.start_service_agent(service, agent)

        elif operation == OPERATION_STOP:
            LOG.debug("LIFECYCLE: Lifecycle_Operations: thr_operation_service_local: stop service locally: " + str(service) + ", agent: " + str(agent))
            apps_adapter.stop_service_agent(service, agent)

        elif operation == OPERATION_TERMINATE:
            LOG.debug("LIFECYCLE: Lifecycle_Operations: thr_operation_service_local: terminate service locally: " + str(service) + ", agent: " + str(agent))
            apps_adapter.terminate_service_agent(service, agent)

    except:
        LOG.error("LIFECYCLE: Lifecycle_Operations: thr_operation_service_local: thr: Exception")


# thr_operation_service_remote: operation_service remote
def thr_operation_service_remote(operation, service, agent):
    try:
        LOG.debug("LIFECYCLE: Lifecycle_Operations: thr_operation_service_remote: service operation: " + operation + " (remote)")

        if operation == OPERATION_START:
            LOG.debug("LIFECYCLE: Lifecycle_Operations: thr_operation_service_remote: start service in remote agent")
            resp_start = mf2c.lifecycle_operation(agent, OPERATION_START)
            if resp_start is not None:
                agent['status'] = resp_start['status']
                LOG.debug("LIFECYCLE: Lifecycle_Operations: thr_operation_service_remote: result (start service): [agent=" + str(agent) + "]")
            else:
                agent['status'] = STATUS_UNKNOWN
                LOG.error("LIFECYCLE: Lifecycle_Operations: thr_operation_service_remote: result (start service): ERROR")

        elif operation == OPERATION_STOP:
            LOG.debug("LIFECYCLE: Lifecycle_Operations: thr_operation_service_remote: stop service in remote agent")
            resp_stop = mf2c.lifecycle_operation(agent, OPERATION_STOP)
            if resp_stop is not None:
                agent['status'] = resp_stop['status']
                LOG.debug("LIFECYCLE: Lifecycle_Operations: thr_operation_service_remote: result (stop service): [agent=" + str(agent) + "]")
            else:
                agent['status'] = STATUS_UNKNOWN
                LOG.error("LIFECYCLE: Lifecycle_Operations: thr_operation_service_remote: result (stop service): ERROR")

        elif operation == OPERATION_TERMINATE:
            LOG.debug("LIFECYCLE: Lifecycle_Operations: thr_operation_service_remote: terminate service in remote agent")
            resp_terminate = mf2c.lifecycle_operation(agent, OPERATION_TERMINATE)
            if resp_terminate is not None:
                agent['status'] = resp_terminate['status']
                LOG.debug("LIFECYCLE: Lifecycle_Operations: thr_operation_service_remote: result (terminate service): [agent=" + str(agent) + "]")
            else:
                agent['status'] = STATUS_UNKNOWN
                LOG.error("LIFECYCLE: Lifecycle_Operations: thr_operation_service_remote: result (terminate service): ERROR")

    except:
        LOG.error("LIFECYCLE: Lifecycle_Operations: thr_operation_service_remote: thr: Exception")


# thr_operation_service: start/stop/terminate service instance in agents
def thr_operation_service(service_instance, operation):
    LOG.debug("LIFECYCLE: Lifecycle_Operations: thr_operation_service: [" + operation + "]: " + service_instance['id'])
    try:
        # 1. get service
        service = data_adapter.get_service(service_instance['service'])
        LOG.debug("LIFECYCLE: Lifecycle_Operations: thr_operation_service: service: " + str(service))

        # 2. stop/start/terminate service in all agents
        thrs = []  # 1 thread per agent
        for agent in service_instance["agents"]:
            LOG.info("LIFECYCLE:>>> AGENT >>> " + agent['url'] + " <<<")
            # LOCAL
            if agent['url'] == common.get_local_ip():
                thrs.append(threading.Thread(target=thr_operation_service_local, args=(operation, service, agent,)))
            # REMOTE AGENT (call lifecycle from agent)
            elif common.check_ip(agent['url']):
                thrs.append(threading.Thread(target=thr_operation_service_remote, args=(operation, service, agent,)))
            # NOT FOUND / NOT CONNECTED
            else:
                agent['status'] = STATUS_ERROR
                LOG.error("LIFECYCLE: Lifecycle_Operations: thr_operation_service: agent [" + agent['url'] + "] cannot be reached")

        # start threads
        for x in thrs:
            x.start()

        # join / wait for threads before executing next tags
        for x in thrs:
            x.join()

        # 3. save / update / terminate service_instance
        LOG.debug("LIFECYCLE: Lifecycle_Operations: thr_operation_service: UPDATING service_instance [" + operation + "]: " + str(service_instance))
        if operation == OPERATION_START:
            service_instance['status'] = STATUS_STARTED
            data_adapter.update_service_instance(service_instance['id'], service_instance)          # cimi / db
            sla_adapter.initializes_sla(service_instance, service_instance['agreement'])            # sla

        elif operation == OPERATION_STOP:
            service_instance['status'] = STATUS_STOPPED
            data_adapter.update_service_instance(service_instance['id'], service_instance)          # cimi / db
            sla_adapter.stop_sla_agreement(service_instance, service_instance['agreement'])         # sla

        elif operation == OPERATION_TERMINATE:
            service_instance['status'] = STATUS_TERMINATED
            data_adapter.del_service_instance(service_instance['id'])                               # cimi / db
            sla_adapter.terminate_sla_agreement(service_instance, service_instance['agreement'])    # sla
    except:
        traceback.print_exc(file=sys.stdout)
        LOG.error('LIFECYCLE: Lifecycle_Operations: thr_operation_service: thr: Exception')


# operation_service: start/stop/terminate service instance in agents
def operation_service(service_instance_id, operation):
    LOG.debug("LIFECYCLE: Lifecycle_Operations: operation_service: [" + operation + "]: " + service_instance_id)
    try:
        # 1. get service_instance object
        service_instance = data_adapter.get_service_instance(service_instance_id)
        if not service_instance:
            return common.gen_response(500, 'Error getting service instance object', 'service_instance_id', service_instance_id)

        # submit operation thread
        if operation == OPERATION_START:
            service_instance['status'] = STATUS_STARTING
        elif operation == OPERATION_STOP:
            service_instance['status'] = STATUS_STOPPING
        elif operation == OPERATION_TERMINATE:
            service_instance['status'] = STATUS_TERMINATING

        t = threading.Thread(target=thr_operation_service, args=(service_instance, operation,))
        t.start()

        # response
        return common.gen_response_ok("Service " + operation + " operation is being processed ...", "service_instance", service_instance)
    except:
        traceback.print_exc(file=sys.stdout)
        LOG.error('LIFECYCLE: Lifecycle_Operations: operation_service: Exception')
        return common.gen_response(500, 'Exception', 'service_instance_id', service_instance_id)


# Service Operation: start (version 2: no access to external docker APIs / calls to other agent's lifecycle components)
def start(service_instance_id):
    return operation_service(service_instance_id, OPERATION_START)


# Service Operation: stop (version 2: no access to external docker APIs / calls to other agent's lifecycle components)
def stop(service_instance_id):
    return operation_service(service_instance_id, OPERATION_STOP)


# Terminate service, Deallocate service's resources
def terminate(service_instance_id):
    LOG.debug("LIFECYCLE: Lifecycle: terminate: " + service_instance_id)
    try:
        # 1. get service_instance object
        service_instance = data_adapter.get_service_instance(service_instance_id)
        if not service_instance:
            return common.gen_response(500, 'Error getting service instance object', 'service_instance_id', service_instance_id)

        # 2. service instance status = Stopped
        if service_instance['status'] != "Stopped":
            stop(service_instance_id)

        # 3. terminate
        return operation_service(service_instance_id, OPERATION_TERMINATE)
    except:
        LOG.error('LIFECYCLE: Lifecycle: terminate: Exception')
        return common.gen_response(500, 'Exception', 'service_instance_id', service_instance_id)


# terminate_all
def terminate_all():
    if data_adapter.del_all_service_instances():
        return common.gen_response_ok('Terminate all services', 'result', 'True')
    else:
        return common.gen_response(500, 'Exception', 'result', 'False')


# Service Instance Operation: starts a job / app
def start_job(body, service_instance_id):
    LOG.debug("LIFECYCLE: Lifecycle: start_job: " + str(body))
    LOG.debug("LIFECYCLE: Lifecycle: start_job: [service_instance_id=" + service_instance_id + "]")
    try:
        # service instance
        service_instance = data_adapter.get_service_instance(service_instance_id)
        LOG.debug("LIFECYCLE: Lifecycle: start_job: service_instance: " + str(service_instance))

        # start job in agent(s)
        if len(service_instance['agents']) == 1:
            res = apps_adapter.start_job_compss(body['service_instance_id'], service_instance['agents'][0], body['parameters'])
        elif len(service_instance['agents']) >= 2:
            res = apps_adapter.start_job_compss_multiple_agents(service_instance, body['parameters'])
        else:
            LOG.warning("LIFECYCLE: Lifecycle: start_job: Execution supported in only 1 or more agents! agents size=" + str(len(service_instance['agents'])))
            res = None

        if res:
            return common.gen_response_ok('Start job', 'service_id', body['service_instance_id'], 'res', res)
        else:
            return common.gen_response(500, 'Error when starting job', 'service_instance', str(service_instance))
    except:
        LOG.error('LIFECYCLE: Lifecycle: start_job: Exception')
        return common.gen_response(500, 'Exception', 'data', str(body))