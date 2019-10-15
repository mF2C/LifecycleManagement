"""
Docker adapter
This is being developed for the MF2C Project: http://www.mf2c-project.eu/

Copyright: Atos Research and Innovation, 2017.

This code is licensed under an Apache 2.0 license. Please, refer to the LICENSE.TXT file for more information

Created on 09 feb. 2018

@author: Roi Sucasas - ATOS
"""

from lifecycle.modules.apps.docker import client as docker_client
from lifecycle import common as common
from lifecycle.data import data_adapter as data_adapter
import uuid, os, time
import urllib.request as urequest
from lifecycle.data.common import db as db #import SERVICE_INSTANCES_LIST
from lifecycle.logs import LOG
import config
from lifecycle.common import OPERATION_START, OPERATION_STOP, OPERATION_TERMINATE, \
    STATUS_ERROR, STATUS_WAITING, STATUS_STARTED, STATUS_STOPPED, STATUS_ERROR_STARTING, STATUS_ERROR_STOPPING, \
    STATUS_TERMINATED, STATUS_UNKNOWN, SERVICE_DOCKER, SERVICE_DOCKER_COMPOSE, SERVICE_COMPSS


'''
 Data managed by this component:
-----------------------------------------------------------------------------------------------
 SERVICE INSTANCE:
   {
       ...
       "id": "",
       "user_id": "testuser",
       "service_id": "",
       "agreement_id": "",
       "status": "waiting",
       "agents": [
           {"agent": resource-link, "url": "192.168.1.31", "ports": [8081], "container_id": "10asd673f", "status": "waiting",
               "num_cpus": 3, "allow": true, "master_compss": false},
           {"agent": resource-link, "url": "192.168.1.34", "ports": [8081], "container_id": "99asd673f", "status": "waiting",
               "num_cpus": 2, "allow": true, "master_compss": false}
      ]
   }
   
    Agent example: {"agent": resource-link, "url": "192.168.1.31", "ports": {8081}, "container_id": "10asd673f", 
                    "status": "waiting", "num_cpus": 3, "allow": true, "master_compss": false}
'''


###############################################################################
# DEPLOYMENT:

# deploy_docker_image:
def __deploy_docker_image(service, agent):
    LOG.debug("[lifecycle.modules.apps.docker.adapter] [__deploy_docker_image] " + str(service) + ", " + str(agent))
    try:
        # service image / location. Examples: "yeasy/simple-web"
        service_image = service['exec']
        # service_name examples: "simple-web-test"
        service_name = service['name'] + "-" + str(uuid.uuid4())
        # command. Docker examples: "/bin/sh -c 'python index.py'"
        service_command = ""
        # port(s)
        ports = agent['ports']

        container1 = docker_client.create_docker_container(service_image, service_name, service_command, ports)
        if container1 is not None:
            db.SERVICE_INSTANCES_LIST.append({
                "type": SERVICE_DOCKER,
                "container_main": container1['Id'],
                "container_2": "-"
            })
            LOG.debug("[lifecycle.modules.apps.docker.adapter] [__deploy_docker_image] container: " + str(container1))

            # update agent properties
            agent['container_id'] = container1['Id']
            agent['agent_param'] = "-"
            agent['status'] = STATUS_WAITING
            return common.gen_response_ok('Deploy service in agent', 'agent', str(agent), 'service', str(service))
        else:
            LOG.error("[lifecycle.modules.apps.docker.adapter] [__deploy_docker_image] Could not connect to DOCKER API")
            agent['status'] = STATUS_ERROR
            return common.gen_response(500, 'Error when connecting to DOCKER API', 'agent', str(agent), 'service', str(service))
    except:
        LOG.exception('[lifecycle.modules.apps.docker.adapter] [__deploy_docker_image] Exception')
        return common.gen_response(500, 'Exception: __deploy_docker_image()', 'agent', str(agent), 'service', str(service))


# deploy_docker_compss:
def __deploy_docker_compss(service, service_instance, agent):
    LOG.debug("[lifecycle.modules.apps.docker.adapter] [__deploy_docker_compss] " + str(service) + ", " + str(agent))
    try:
        # service image / location. Examples: "mf2c/compss-agent:latest", "mf2c/compss-mf2c:1.0"
        service_image = service['exec']
        # port(s); COMPSs exposes port 8080
        ports = agent['ports']
        # ip
        ip = agent['url']
        # ip_leader
        ip_leader = service_instance['device_ip'] # TODO create a 'exec_device_ip'

        container1 = docker_client.create_docker_compss_container(service_image, ip, ports, ip_leader)
        if container1 is not None:
            db.SERVICE_INSTANCES_LIST.append({
                "type": SERVICE_COMPSS,
                "container_main": container1['Id'],
                "container_2": "-"
            })
            LOG.debug("[lifecycle.modules.apps.docker.adapter] [__deploy_docker_compss] container: " + str(container1))

            # update agent properties
            agent['container_id'] = container1['Id']
            agent['agent_param'] = "-"
            agent['status'] = STATUS_WAITING
            return common.gen_response_ok('Deploy service in agent', 'agent', str(agent), 'service', str(service))
        else:
            LOG.error("[lifecycle.modules.apps.docker.adapter] [__deploy_docker_compss] Could not connect to DOCKER API")
            agent['status'] = STATUS_ERROR
            return common.gen_response(500, 'Error when connecting to DOCKER API', 'agent', str(agent), 'service', str(service))
    except:
        LOG.exception('[lifecycle.modules.apps.docker.adapter] [__deploy_docker_compss] Exception')
        return common.gen_response(500, 'Exception: __deploy_docker_compss()', 'agent', str(agent), 'service', str(service))


# deploy_docker_compose:
#   Command:  sudo docker run -v /var/run/docker.sock:/var/run/docker.sock
#               -v /home/atos/mF2C/compose_examples:/home/atos/mF2C/compose_examples
#               -w="/home/atos/mF2C/compose_examples" docker/compose:1.21.0 up
def __deploy_docker_compose(service, agent):
    LOG.debug("[lifecycle.modules.apps.docker.adapter] [__deploy_docker_compose] " + str(service) + ", " + str(agent))
    try:
        # 1. Download docker-compose.yml file
        location = service['exec']
        LOG.debug("[lifecycle.modules.apps.docker.adapter] [__deploy_docker_compose] Getting docker-compose.yml from " + location + " ...")
        # remove previous files
        try:
            os.remove(config.dic['WORKING_DIR_VOLUME'] + "/docker-compose.yml")
        except:
            LOG.warning("[lifecycle.modules.apps.docker.adapter] [__deploy_docker_compose] Error when removing file: " + config.dic['WORKING_DIR_VOLUME'] + "/docker-compose.yml")
        # download docker-compose.yml
        try:
            res, _ = urequest.urlretrieve(location, config.dic['WORKING_DIR_VOLUME'] + "/docker-compose.yml")
            LOG.debug("[lifecycle.modules.apps.docker.adapter] [__deploy_docker_compose] > download result: " + str(res))
        except:
            LOG.exception("[lifecycle.modules.apps.docker.adapter] [__deploy_docker_compose] Error when downloading file to: " + config.dic['WORKING_DIR_VOLUME'] + "/docker-compose.yml")
            return common.gen_response(500, "Exception: deploy_docker_compose(): Error when downloading file to WORKING_DIR_VOLUME",
                                       "agent", str(agent),
                                       "WORKING_DIR_VOLUME", config.dic['WORKING_DIR_VOLUME'])

        # 2. Deploy container
        service_name = service['name'] + "-" + str(uuid.uuid4()) # service_name
        service_command = "up" # command

        # container 1 => command 'up'
        container1 = docker_client.create_docker_compose_container(service_name, service_command)
        if container1 is not None:
            LOG.debug("[lifecycle.modules.apps.docker.adapter] [__deploy_docker_compose] container1: " + str(container1))
            # container 2 => command 'down'
            container2 = docker_client.create_docker_compose_container(service_name + "-" + str(uuid.uuid4()), "down")
            if container2 is not None:
                db.SERVICE_INSTANCES_LIST.append({
                    "type": SERVICE_DOCKER_COMPOSE,
                    "container_main": container1['Id'],
                    "container_2": container2['Id']
                })
                LOG.debug("[lifecycle.modules.apps.docker.adapter] [__deploy_docker_compose] container2: " + str(container2))
                LOG.debug("[lifecycle.modules.apps.docker.adapter] [__deploy_docker_compose] container '1' & '2' created")
                agent['agent_param'] = container2['Id']
            else:
                db.SERVICE_INSTANCES_LIST.append({
                    "type": SERVICE_DOCKER_COMPOSE,
                    "container_main": container1['Id'],
                    "container_2": 'error'
                })
                LOG.error("[lifecycle.modules.apps.docker.adapter] [__deploy_docker_compose] container '2' not created")
                agent['agent_param'] = "-"

            # update agent properties
            agent['container_id'] = container1['Id']
            agent['status'] = STATUS_WAITING
            return common.gen_response_ok('Deploy service in agent', 'agent', str(agent), 'service', str(service))
        else:
            LOG.error("[lifecycle.modules.apps.docker.adapter] [__deploy_docker_compose] Could not connect to DOCKER API")
            agent['status'] = STATUS_ERROR
            return common.gen_response(500, 'Error when connecting to DOCKER API', 'agent', str(agent), 'service',
                                       str(service))
    except:
        LOG.exception('[lifecycle.modules.apps.docker.adapter] [__deploy_docker_compose] Exception')
        return common.gen_response(500, 'Exception: __deploy_docker_compose()', 'agent', str(agent), 'service', str(service))


# deploy_service_agent: Deploy service in an agent
# IN: service, agent
# OUT: status value
def deploy_service_agent(service, service_instance, agent):
    LOG.debug("[lifecycle.modules.apps.docker.adapter] [deploy_service_agent] " + str(service) + ", " + str(agent))
    try:
        # docker-compose
        if service['exec_type'] == SERVICE_DOCKER_COMPOSE:
            return __deploy_docker_compose(service, agent)
        # docker
        elif service['exec_type'] == SERVICE_DOCKER:
            return __deploy_docker_image(service, agent)
        # compss (docker)
        elif service['exec_type'] == SERVICE_COMPSS:
            return __deploy_docker_compss(service, service_instance, agent)
        # not defined
        else:
            LOG.warning("[lifecycle.modules.apps.docker.adapter] [deploy_service_agent] [" + service['exec_type'] + "] not defined")
            return common.gen_response(500, 'Exception: type not defined: deploy_service_agent()', 'agent', str(agent),
                                       'service', str(service))
    except:
        LOG.exception('[lifecycle.modules.apps.docker.adapter] [deploy_service_agent] Exception')
        return common.gen_response(500, 'Exception: deploy_service_agent()', 'agent', str(agent), 'service', str(service))


###############################################################################
# OPERATIONS:

# operation_service_agent: service operation (start, stop...)
def __operation_service_agent(agent, operation):
    LOG.debug("[lifecycle.modules.apps.docker.adapter] [__operation_service_agent] [" + operation + "]: " + str(agent))
    try:
        # connect to docker api / check existing connection
        if docker_client.get_client_agent_docker() is not None:
            if operation == OPERATION_START:
                if docker_client.start_container(agent['container_id']):
                    agent['status'] = STATUS_STARTED
                else:
                    agent['status'] = STATUS_ERROR_STARTING

                if config.dic['NETWORK_COMPSs'] != "not-defined":
                    docker_client.add_container_to_network(agent['container_id'])

            elif operation == OPERATION_STOP:
                l_elem = data_adapter.db_get_elem_from_list(agent['container_id'])
                LOG.debug("[lifecycle.modules.apps.docker.adapter] [__operation_service_agent] docker-compose? [l_elem=" + str(l_elem) + "]")

                # docker-compose
                if l_elem is not None and l_elem['type'] == SERVICE_DOCKER_COMPOSE:
                    LOG.debug("[lifecycle.modules.apps.docker.adapter] [__operation_service_agent] 'Docker-compose down' container [" + l_elem['container_2'] + "] launched ...")
                    docker_client.start_container(l_elem['container_2'])
                    LOG.debug("[lifecycle.modules.apps.docker.adapter] [__operation_service_agent] Executing 'docker-compose down' ...")

                    for i in range(6):
                        time.sleep(20)
                        res = docker_client.inspect_container(l_elem['container_2'])
                        if res is not None and res['State']['Status'] is not None and res['State']['Status'] == 'exited':
                            break
                        LOG.debug("[lifecycle.modules.apps.docker.adapter] [__operation_service_agent] Waiting for 'docker-compose down' execution (20s) ...")

                    LOG.debug("[lifecycle.modules.apps.docker.adapter] [__operation_service_agent] Stopping 'Docker-compose up' container [" + agent['container_id'] + "] ...")
                    docker_client.stop_container(agent['container_id'])
                    LOG.debug("[lifecycle.modules.apps.docker.adapter] [__operation_service_agent] Stopping 'Docker-compose down' container [" + l_elem['container_2'] + "] ...")
                    docker_client.stop_container(l_elem['container_2'])
                    agent['status'] = STATUS_STOPPED
                # 'normal' container
                else:
                    LOG.debug("[lifecycle.modules.apps.docker.adapter] [__operation_service_agent] Stop container: " + agent['container_id'])
                    if docker_client.stop_container(agent['container_id']):
                        agent['status'] = STATUS_STOPPED
                    else:
                        agent['status'] = STATUS_ERROR_STOPPING

            elif operation == OPERATION_TERMINATE:
                l_elem = data_adapter.db_get_elem_from_list(agent['container_id'])
                LOG.debug("[lifecycle.modules.apps.docker.adapter] [__operation_service_agent] docker-compose? [l_elem=" + str(l_elem) + "]")

                # docker-compose
                if l_elem is not None and l_elem['type'] == SERVICE_DOCKER_COMPOSE:
                    LOG.debug("[lifecycle.modules.apps.docker.adapter] [__operation_service_agent] Remove container 1 [" + agent['container_id'] + "] ...")
                    docker_client.remove_container(agent)
                    LOG.debug("[lifecycle.modules.apps.docker.adapter] [__operation_service_agent] Remove container 2 [" + l_elem['container_2'] + "] ...")
                    docker_client.remove_container_by_id(l_elem['container_2'])
                # 'normal' container
                else:
                    LOG.debug("[lifecycle.modules.apps.docker.adapter] [__operation_service_agent] Remove container: " + agent['container_id'])
                    docker_client.remove_container(agent)
                agent['status'] = STATUS_TERMINATED

        # if error when connecting to agent...
        else:
            LOG.error("[lifecycle.modules.apps.docker.adapter] [__operation_service_agent] Could not connect to DOCKER API")
            agent['status'] = STATUS_UNKNOWN
        # return status
        return agent['status']
    except:
        agent['status'] = STATUS_ERROR
        LOG.exception('[lifecycle.modules.apps.docker.adapter] [__operation_service_agent] Exception')
        return STATUS_ERROR


# start_service_agent: Start service in agent
def start_service_agent(agent):
    return __operation_service_agent(agent, OPERATION_START)


# stop_service_agent: Stop service / stop container
def stop_service_agent(agent):
    return __operation_service_agent(agent, OPERATION_STOP)


# terminate_service_agent: Stop service / stop container
def terminate_service_agent(agent):
    return __operation_service_agent(agent, OPERATION_TERMINATE)
