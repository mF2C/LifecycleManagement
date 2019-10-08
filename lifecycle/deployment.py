"""
Lifecycle Deployment: deployment in 'parallel' mode
This is being developed for the MF2C Project: http://www.mf2c-project.eu/

Copyright: Atos Research and Innovation, 2017.

This code is licensed under an Apache 2.0 license. Please, refer to the LICENSE.TXT file for more information

Created on 09 feb. 2018

@author: Roi Sucasas - ATOS
"""

import threading
from lifecycle.connectors import connector as connector
from lifecycle.modules import agent_decision as agent_decision
from lifecycle.modules import applications_adapter as apps_adapter
from lifecycle import common as common
from lifecycle.data import data_adapter as data_adapter
from lifecycle.logs import LOG
from lifecycle.common import STATUS_STARTED, STATUS_DEPLOYING
from lifecycle import operations as operations


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
        LOG.debug("[lifecycle.deployment] [check_service_content] fields category/exec/exec_type not found")
        return False
    return True


###############################################################################
# DEPLOYMENT / SUBMIT:


# thr_submit_local: deploy locally
def thr_submit_local(service, service_instance, agent):
    try:
        LOG.debug("[lifecycle.deployment] [thr_submit_local] allocate service locally")

        resp_deploy = apps_adapter.deploy_service_agent(service, service_instance, agent)
        LOG.debug("[lifecycle.deployment] [thr_submit_local] allocate service locally: "
                  "[resp_deploy=" + str(resp_deploy) + "]")
        if agent['status'] == "waiting":
            LOG.debug("[lifecycle.deployment] [thr_submit_local] execute service locally")
            # executes service
            apps_adapter.start_service_agent(service, agent)
        else:
            LOG.error("[lifecycle.deployment] [thr_submit_local] allocate service locally: NOT DEPLOYED")
            agent['status'] = "not-deployed"

    except:
        LOG.exception("[lifecycle.deployment] [thr_submit_local] Exception")


# thr_submit_remote: deploy in a remote agent
def thr_submit_remote(service, service_instance, agent):
    try:
        LOG.debug("[lifecycle.deployment] [thr_submit_remote] allocate service in remote agent [" + agent['url'] + "]")
        resp_deploy = connector.lifecycle_deploy(service, service_instance, agent)
        if resp_deploy is not None:
            agent['status'] = resp_deploy['status']
            agent['container_id'] = resp_deploy['container_id']
            agent['ports'] = resp_deploy['ports']
            LOG.debug("[lifecycle.deployment] [thr_submit_remote] allocate service in remote agent: "
                      "[agent=" + str(agent) + "]")
            # executes / starts service
            resp_start = connector.lifecycle_operation(service, agent, "start")
            if resp_start is not None:
                agent['status'] = resp_start['status']
                LOG.debug("[lifecycle.deployment] [thr_submit_remote] execute service in remote agent: "
                          "[agent=" + str(agent) + "]")
        else:
            LOG.error("[lifecycle.deployment] [thr_submit_remote] allocate service in remote agent: NOT DEPLOYED")
            agent['status'] = "not-deployed"

    except:
        LOG.exception("[lifecycle.deployment] [thr_submit_remote] Exception")


# thr_submit_service_in_agents: deploy agents (parallel process)
def thr_submit_service_in_agents(service, service_instance, sla_template_id, user_id):
    try:
        LOG.debug("[lifecycle.deployment] [thr_submit_service_in_agents] Executing thread ...")

        # 4. allocate service / call remote container
        thrs = []   # 1 thread per agent
        for agent in service_instance["agents"]:
            LOG.debug("[lifecycle.deployment] [thr_submit_service_in_agents] >>> AGENT >>> " + agent['url'] + " <<<")
            # LOCAL
            if agent['url'] == data_adapter.get_my_ip(): #common.get_local_ip():
                thrs.append(threading.Thread(target=thr_submit_local, args=(service, service_instance, agent,)))
            # 'REMOTE' AGENT: calls to lifecycle from remote agent
            elif common.check_ip(agent['url']):
                thrs.append(threading.Thread(target=thr_submit_remote, args=(service, service_instance, agent,)))
            # NOT FOUND / NOT CONNECTED
            else:
                agent['status'] = "error"
                LOG.error("[lifecycle.deployment] [thr_submit_service_in_agents] agent [" + agent['url'] + "] cannot be reached")

        # start threads
        for x in thrs:
            x.start()

        # join / wait for threads before executing next tags
        for x in thrs:
            x.join()

        # 5.1 creates SLA template
        id_agreement = connector.create_sla_agreement(sla_template_id, user_id, service)
        if id_agreement is not None:
            service_instance['agreement'] = id_agreement
            # 5.2 initializes SLA
            if connector.sla_start_agreement(id_agreement):
                LOG.debug("[lifecycle.deployment] [thr_submit_service_in_agents] sla agreement started")
            else:
                LOG.error("[lifecycle.deployment] [thr_submit_service_in_agents] sla agreement NOT started")

        # 6. save / update service_instance
        LOG.debug("[lifecycle.deployment] [thr_submit_service_in_agents] Updating service_instance: " + str(service_instance))
        service_instance['status'] = STATUS_STARTED
        data_adapter.update_service_instance(service_instance['id'], service_instance)

        LOG.debug("[lifecycle.deployment] [thr_submit_service_in_agents] service instance deployed: service_instance: " + str(service_instance))
    except:
        LOG.exception("[lifecycle.deployment] [thr_submit_service_in_agents] Exception")


# __forward_submit_request_to_leader
def __forward_submit_request_to_leader(service, user_id, sla_template_id, service_instance_id):
    LOG.debug("[lifecycle.deployment] [forward_submit_request_to_leader] Forwarding service [" + service['name'] + "] deployment to leader" +
              " (user_id: " + user_id + ", sla_template_id: " + sla_template_id + ", service_instance_id: " + service_instance_id + ") ...")
    # leader IP and current agent IP
    leader_ip = data_adapter.get_leader_ip()
    my_ip = data_adapter.get_my_ip()

    # check if leader_ip =/= current agent IP
    if  leader_ip is not None and my_ip is not None and my_ip == leader_ip:
        LOG.warning("[lifecycle.deployment] [forward_submit_request_to_leader] LM cannot forward request to leader. Reason: 'my_ip' == 'leader_ip'")
        # delete service_instance
        if service_instance_id is not None:
            LOG.debug("[lifecycle.deployment] [forward_submit_request_to_leader] Deleting service instance [" + service_instance_id + "] ...")
            service_instance_id = id.replace('service-instance/', '')
            operations.terminate(service_instance_id)
        # send error
        return common.gen_response(500,
                                   "Not enough resources found in current cluster => Error when forwarding request to Leader: my_ip == leader_ip !",
                                   "service_instance_id", service_instance_id,
                                   "actions", "1) Service instance deleted, 2) Request not completed")

    # if leader_ip =/= current agent IP, forward request to leader
    elif leader_ip is not None and connector.lifecycle_parent_deploy(leader_ip, service['id'], user_id, sla_template_id, service_instance_id):
        LOG.debug("[lifecycle.deployment] [forward_submit_request_to_leader] Checking service_instance before forwarding request to leader...")
        # check if service instance was created
        service_instance = None
        if not service_instance_id:
            service_instance = data_adapter.create_service_instance(service, [], user_id, "")
            service_instance_id = service_instance['id']

        LOG.debug("[lifecycle.deployment] [forward_submit_request_to_leader] Request forwarded to leader.")
        return common.gen_response_ok("Not enough resources found in current cluster => Request forwarded to Leader. Service deployment operation is being processed...",
                                      "service_instance_id", service_instance_id,
                                      "service_instance", service_instance)

    # error
    else:
        LOG.error("[lifecycle.deployment] [forward_submit_request_to_leader] LM could not forward request to leader: 'leader_ip' is None / error connecting to leader agent")
        # delete service_instance
        if service_instance_id is not None:
            LOG.debug("[lifecycle.deployment] [forward_submit_request_to_leader] Deleting service instance [" + service_instance_id + "] ...")
            service_instance_id = id.replace('service-instance/', '')
            operations.terminate(service_instance_id)
        # send error
        return common.gen_response(500,
                                   "Not enough resources found in current cluster => Error when forwarding request to Leader!",
                                   "service_instance_id", service_instance_id,
                                   "actions", "1) Service instance deleted, 2) Request not completed")


# FUNCTION: submit_service_in_agents: Submits a service in a set of agents / devices
#  (no access to external docker APIs; calls to other agent's lifecycle components)
def submit_service_in_agents(service, user_id, service_instance_id, sla_template_id, agents_list, check_service=False):
    LOG.debug("[lifecycle.deployment] [submit_service_in_agents] Deploying service [name=" + service['name'] + ", "
              ", user_id=" + user_id + ", sla_template_id=" + sla_template_id + ", agents_list=" + str(agents_list) + "] in agents ...")
    try:
        # 1. check parameters content
        if check_service and not check_service_content(service):
            return common.gen_response(500, 'field(s) category/exec/exec_type not found', 'service', str(service))

        # 2. create new service instance
        if service_instance_id is not None and service_instance_id != "":
            service_instance = data_adapter.get_service_instance(service_instance_id)
        else:
            LOG.debug("[lifecycle.deployment] [submit_service_in_agents] Creating service instance ... ")
            service_instance = data_adapter.create_service_instance(service, agents_list, user_id, "DEFAULT-VALUE")
            if not service_instance or 'id' not in service_instance:
                LOG.error("[lifecycle.deployment] [submit_service_in_agents] error creating service_instance")
                return common.gen_response(500, 'error creating service_instance', 'service', str(service))

        # 3. select from agents list
        if 'num_agents' not in service or service['num_agents'] == 0:
            num_agents = -1
        else:
            num_agents = service['num_agents']

        LOG.info("[lifecycle.deployment] [submit_service_in_agents] Total agents needed to run the service ['num_agents']: " + str(num_agents))
        LOG.info("[lifecycle.deployment] [submit_service_in_agents] Selecting agents ... ")

        r, m = agent_decision.select_agents(service['exec_type'], num_agents, service_instance)

        if m == "error" or r is None:
            LOG.error("[lifecycle.deployment] [submit_service_in_agents] error when selecting agents. Forwarding to Leader...")
            # forward to parent
            return __forward_submit_request_to_leader(service, user_id, sla_template_id, service_instance['id'])

        elif m == "not-enough-resources-found" or len(r['agents']) == 0:
            LOG.warning("[lifecycle.deployment] [submit_service_in_agents] Not enough resources (number of agents) found. Forwarding to Leader...")
            # forward to parent
            return __forward_submit_request_to_leader(service, user_id, sla_template_id, service_instance['id'])

        else:
            LOG.info("######## DEPLOYMENT ###############################################################")
            service_instance = r
            LOG.debug("[lifecycle.deployment] [submit_service_in_agents] service_instance: " + str(service_instance))

            # submit service thread
            service_instance['status'] = STATUS_DEPLOYING
            t = threading.Thread(target=thr_submit_service_in_agents, args=(service, service_instance, sla_template_id, user_id,))
            t.start()

            return common.gen_response_ok("Service deployment operation is being processed [" + service_instance['id'] + "]...",
                                          "service_instance", service_instance)
    except:
        LOG.exception('[lifecycle.deployment] [submit_service_in_agents] Exception')
        return common.gen_response(500, 'Exception', 'service', str(service))


# FUNCTION: submit: Submits a service in mF2C
# (gets list of agents from mF2C components - recommender, landscaper - or from config)
def submit(service, user_id, service_instance_id, sla_template_id):
    LOG.debug("[lifecycle.deployment] [submit] Deploying service [" + service['name'] + "] in mF2C ...")
    try:
        # 1. check parameters content
        if not check_service_content(service):
            return common.gen_response(500, 'field(s) category/exec/exec_type not found', 'service', str(service))

        # 2. get list of available agents / resources / VMs. Example: [{"agent_ip": "192.168.252.41"}, {...}]
        # Call to landscaper / recommender
        available_agents_list = agent_decision.get_available_agents_resources(service)
        if not available_agents_list:
            # warning
            LOG.error("[lifecycle.deployment] [submit] available_agents_list is None. Forwarding to Leader...")
            # forward to parent
            return __forward_submit_request_to_leader(service, user_id, sla_template_id, "")

        elif len(available_agents_list) == 0:
            # no resources / agents found
            LOG.warning("[lifecycle.deployment] [submit] available_agents_list is empty. Forwarding to Leader...")
            # forward to parent
            return __forward_submit_request_to_leader(service, user_id, sla_template_id, "")

        else:
            LOG.info("######## DEPLOYMENT ###############################################################")
            # 3. Create new service instance & allocate service / call other agents when needed
            return submit_service_in_agents(service, user_id, service_instance_id, sla_template_id, available_agents_list)
    except:
        LOG.exception('[lifecycle.deployment] [submit] Exception')
        return common.gen_response(500, 'Exception', 'service', str(service))



