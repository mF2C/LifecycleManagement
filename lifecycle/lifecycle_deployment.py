"""
Lifecycle Deployment: deployment in 'parallel' mode
This is being developed for the MF2C Project: http://www.mf2c-project.eu/

Copyright: Atos Research and Innovation, 2017.

This code is licensed under an Apache 2.0 license. Please, refer to the LICENSE.TXT file for more information

Created on 09 feb. 2018

@author: Roi Sucasas - ATOS
"""

import sys, traceback
import threading
import lifecycle.modules.agent_decision as agent_decision
import lifecycle.modules.applications_adapter as apps_adapter
import lifecycle.modules.sla_adapter as sla_adapter
import common.common as common
import lifecycle.data.data_adapter as data_adapter
import lifecycle.data.mF2C.mf2c as mf2c
from common.logs import LOG
from common.common import STATUS_STARTED, STATUS_DEPLOYING


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


# check_service_content:
def check_service_content(service):
    if 'category' not in service or 'exec_type' not in service or 'exec' not in service:
        LOG.debug("LIFECYCLE: Lifecycle_Deployment: check_service_content: fields category/exec/exec_type not found")
        return False
    return True


###############################################################################
# DEPLOYMENT / SUBMIT:


# thr_submit_local: deploy locally
def thr_submit_local(service, agent):
    try:
        LOG.debug("LIFECYCLE: Lifecycle_Deployment: thr_submit_local: allocate service locally")

        resp_deploy = apps_adapter.deploy_service_agent(service, agent)
        LOG.debug("LIFECYCLE: Lifecycle_Deployment: thr_submit_local: allocate service locally: "
                  "[resp_deploy=" + str(resp_deploy) + "]")
        if agent['status'] == "waiting":
            LOG.debug("LIFECYCLE: Lifecycle_Deployment: thr_submit_local: execute service locally")
            # executes service
            apps_adapter.start_service_agent(service, agent)
        else:
            LOG.error("LIFECYCLE: Lifecycle_Deployment: thr_submit_local: allocate service locally: NOT DEPLOYED")
            agent['status'] = "not-deployed"

    except:
        LOG.error("LIFECYCLE: Lifecycle_Deployment: thr_submit_local: thr: Exception")


# thr_submit_remote: deploy in a remote agent
def thr_submit_remote(service, agent):
    try:
        LOG.debug("LIFECYCLE: Lifecycle_Deployment: thr_submit_remote: allocate service in remote agent [" + agent['url'] + "]")
        resp_deploy = mf2c.lifecycle_deploy(service, agent)
        if resp_deploy is not None:
            agent['status'] = resp_deploy['status']
            agent['container_id'] = resp_deploy['container_id']
            agent['ports'] = resp_deploy['ports']
            LOG.debug("LIFECYCLE: Lifecycle_Deployment: thr_submit_remote: allocate service in remote agent: "
                      "[agent=" + str(agent) + "]")
            # executes / starts service
            resp_start = mf2c.lifecycle_operation(agent, "start")
            if resp_start is not None:
                agent['status'] = resp_start['status']
                LOG.debug("LIFECYCLE: Lifecycle_Deployment: thr_submit_remote: execute service in remote agent: "
                          "[agent=" + str(agent) + "]")
        else:
            LOG.error("LIFECYCLE: Lifecycle_Deployment: thr_submit_remote: allocate service in remote agent: NOT DEPLOYED")
            agent['status'] = "not-deployed"

    except:
        LOG.error("LIFECYCLE: Lifecycle_Deployment: thr_submit_remote: thr: Exception")


# thr_submit_service_in_agents: deploy agents (parallel process)
def thr_submit_service_in_agents(service, service_instance, user_id, agreement_id):
    try:
        LOG.debug("LIFECYCLE: Lifecycle_Deployment: thr_submit_service_in_agents: " + str(service) + ", user_id: " + user_id)

        # 3. select from agents list
        r = agent_decision.select_agents(service['exec_type'], service_instance)
        if not r is None:
            service_instance = r

        LOG.debug("LIFECYCLE: Lifecycle_Deployment: thr_submit_service_in_agents: service_instance: " + str(service_instance))

        # 4. allocate service / call remote container
        thrs = []   # 1 thread per agent
        for agent in service_instance["agents"]:
            LOG.info("LIFECYCLE:>>> AGENT >>> " + agent['url'] + " <<<")
            # LOCAL
            if agent['url'] == common.get_local_ip():
                thrs.append(threading.Thread(target=thr_submit_local, args=(service, agent,)))
            # 'REMOTE' AGENT: calls to lifecycle from remote agent
            elif common.check_ip(agent['url']):
                thrs.append(threading.Thread(target=thr_submit_remote, args=(service, agent,)))
            # NOT FOUND / NOT CONNECTED
            else:
                agent['status'] = "error"
                LOG.error("LIFECYCLE: Lifecycle_Deployment: thr_submit_service_in_agents: agent [" + agent['url'] + "] cannot be reached")

        # start threads
        for x in thrs:
            x.start()

        # join / wait for threads before executing next tags
        for x in thrs:
            x.join()

        # 5. initializes SLA
        if sla_adapter.initializes_sla(service_instance, agreement_id):
            LOG.debug("LIFECYCLE: Lifecycle_Deployment: thr_submit_service_in_agents: sla agreement started")
        else:
            LOG.error("LIFECYCLE: Lifecycle_Deployment: thr_submit_service_in_agents: sla agreement NOT started")

        # 6. save / update service_instance
        LOG.debug("LIFECYCLE: Lifecycle_Deployment: thr_submit_service_in_agents: UPDATING service_instance: " + str(service_instance))
        service_instance['status'] = STATUS_STARTED
        data_adapter.update_service_instance(service_instance['id'], service_instance)

        LOG.debug("LIFECYCLE: Lifecycle_Deployment: thr_submit_service_in_agents: service instance deployed: service_instance: " + str(service_instance))
    except:
        LOG.error("LIFECYCLE: Lifecycle_Deployment: thr_submit_service_in_agents: thr: Exception")


# submit_service_in_agents: Submits a service (no access to external docker APIs; calls to other agent's lifecycle components)
# IN: service, user_id, agreement_id, agents_list
# OUT: service_instance
def submit_service_in_agents(service, user_id, agreement_id, agents_list, check_service=False):
    LOG.debug("LIFECYCLE: Lifecycle_Deployment: submit_service_in_agents: " + str(service) + ", user_id: " + user_id)
    try:
        # 1. check parameters content
        if check_service and not check_service_content(service):
            return common.gen_response(500, 'field(s) category/exec/exec_type not found', 'service', str(service))

        # 2. create new service instance
        LOG.debug("LIFECYCLE: Lifecycle_Deployment: submit_service_in_agents: agents_list" + str(agents_list))

        service_instance = data_adapter.create_service_instance(service, agents_list, user_id, agreement_id)
        if not service_instance:
            LOG.error("LIFECYCLE: Lifecycle_Deployment: submit_service_in_agents: error creating service_instance")
            return common.gen_response(500, 'error creating service_instance', 'service', str(service))

        # 3. select from agents list
        r = agent_decision.select_agents(service['exec_type'], service_instance)
        if not r is None:
            service_instance = r

        LOG.debug("LIFECYCLE: Lifecycle_Deployment: submit_service_in_agents: service_instance: " + str(service_instance))

        # submit service thread
        service_instance['status'] = STATUS_DEPLOYING
        t = threading.Thread(target=thr_submit_service_in_agents, args=(service, service_instance, user_id, agreement_id,))
        t.start()

        return common.gen_response_ok('Service deployment operation is being processed...', 'service_instance', service_instance)
    except:
        traceback.print_exc(file=sys.stdout)
        LOG.error('LIFECYCLE: Lifecycle_Deployment: submit_service_in_agents: Exception')
        return common.gen_response(500, 'Exception', 'service', str(service))


# submit: Submits a service (gets list of agents from mF2C components - recommender, landscaper - or from config)
# IN: service, user_id, agreement_id
# OUT: service_instance
def submit(service, user_id, agreement_id):
    LOG.debug("LIFECYCLE: Lifecycle_Deployment: submit: " + str(service) + ", user_id: " + user_id)
    try:
        # 1. check parameters content
        if not check_service_content(service):
            return common.gen_response(500, 'field(s) category/exec/exec_type not found', 'service', str(service))

        # 2. get list of available agents / resources / VMs. Example:
        #   [{"agent_ip": "192.168.252.41", "num_cpus": 4, "master_compss": false}, {...}]
        # Call to landscaper/recommender
        available_agents_list = agent_decision.get_available_agents_resources(service)
        if not available_agents_list:
            # TODO forward to parent

            # error
            LOG.error("LIFECYCLE: Lifecycle_Deployment: submit: available_agents_list is None")
            return common.gen_response(500, 'available_agents_list is None', 'service', str(service))
        elif len(available_agents_list) == 0:
            # TODO forward to parent

            # no resurces / agents found
            LOG.error("LIFECYCLE: Lifecycle_Deployment: submit: available_agents_list is empty")
            return common.gen_response(500, 'available_agents_list is empty', 'service', str(service))
        else:
            # 3. Create new service instance & allocate service / call other agents when needed
            return submit_service_in_agents(service, user_id, agreement_id, available_agents_list)
    except:
        LOG.error('LIFECYCLE: Lifecycle_Deployment: submit: Exception')
        return common.gen_response(500, 'Exception', 'service', str(service))



