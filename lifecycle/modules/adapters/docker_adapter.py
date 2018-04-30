"""
Docker adapter
This is being developed for the MF2C Project: http://www.mf2c-project.eu/

Copyright: Atos Research and Innovation, 2017.

This code is licensed under an Apache 2.0 license. Please, refer to the LICENSE.TXT file for more information

Created on 09 feb. 2018

@author: Roi Sucasas - ATOS
"""

import lifecycle.utils.common as common
import docker, wget
import sys, traceback
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
       
       "exec_type": "docker" ........... "exec" = docker image (docker hub)
                    "docker-compose" ... "exec" = docker-compose.yml location
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
           {"agent": resource-link, "url": "192.168.1.31", "port": 8081, "container_id": "10asd673f", "status": "waiting",
               "num_cpus": 3, "allow": true},
           {"agent": resource-link, "url": "192.168.1.34", "port": 8081, "container_id": "99asd673f", "status": "waiting",
               "num_cpus": 2, "allow": true}
      ]
   }
   
    Agent example: {"agent": resource-link, "url": "192.168.1.31", "port": 8081, "container_id": "10asd673f", 
                    "status": "waiting", "num_cpus": 3, "allow": true}
'''


# working dir for docker compose applications / services
WORKING_DIR_VOLUME = "/home/atos/mF2C/compose_examples"
# docker compose image: needed to deploy docker compose based services
DOCKER_COMPOSE_IMAGE = "docker/compose:1.21.0"
# docker socket volume
DOCKER_SOCKET_VOLUME = "/var/run/docker.sock"
# docker socket connection
DOCKER_SOCKET = "unix://var/run/docker.sock"


# get_client_agent_docker: Get docker api client
# connect to docker api: Examples: base_url='tcp://192.168.252.42:2375'; base_url='unix://var/run/docker.sock'
def get_client_agent_docker():
    LOG.debug("Connecting to DOCKER API [" + DOCKER_SOCKET + "]...")
    try:
        client = docker.APIClient(base_url=DOCKER_SOCKET)
        LOG.debug("Connected to DOCKER in [" + DOCKER_SOCKET + "]; version: " + str(client.version()))
        return client
    except:
        LOG.error("Lifecycle-Management: Docker adapter: get_client_agent_docker: " 
                  "Error when connecting to DOCKER API: " + DOCKER_SOCKET)
        return None


# deploy_docker_image:
def deploy_docker_image(service, agent):
    LOG.debug("Lifecycle-Management: Docker adapter: (1) deploy_docker_image: " + str(service) + ", " + str(agent))
    try:
        # service image / location. Examples: "mf2c/compss-mf2c:1.0", "yeasy/simple-web"
        service_image = service['exec']
        # service_name examples: "app-compss", "simple-web-test"
        service_name = service['name']
        # command. Docker examples: "/bin/sh -c 'python index.py'"
        service_command = ""

        # get url / port
        port = agent['port']  # TODO check/improve ports

        # connect to docker api
        client = get_client_agent_docker()

        if client:
            # check if image already exists in agent
            l_images = client.images(name=service_image)
            # if not, download image
            if not l_images or len(l_images) == 0:
                LOG.debug("Lifecycle-Management: Docker adapter: (2) deploy_docker_image: call to 'import_image' [" + service_image + "] ...")
                client.import_image(image=service_image)  # (tag="latest", image="ubuntu") # (tag="latest", image="ubuntu")

            LOG.debug("Lifecycle-Management: Docker adapter: (3) deploy_docker_image: [service_image=" + service_image
                      + "], [service_name=" + service_name + "],  [port=" + str(port) + "]...")

            # create a new container: 'docker run'
            container = client.create_container(service_image,  # command=service_command,
                                                name=service_name,
                                                tty=True,
                                                ports=[port],
                                                host_config=client.create_host_config(port_bindings={port: port}))

            LOG.debug("Lifecycle-Management: Docker adapter: (4) deploy_docker_image: container: " + str(container))

            # update agent properties
            agent['container_id'] = container['Id']
            agent['status'] = "waiting"
            return common.gen_response_ok('Deploy service in agent', 'agent', str(agent), 'service', str(service))
        else:
            LOG.error("Lifecycle-Management: Docker adapter: deploy_docker_image: Could not connect to DOCKER API")
            agent['status'] = "error"
            return common.gen_response(500, 'Error when connecting to DOCKER API', 'agent', str(agent), 'service', str(service))
    except:
        traceback.print_exc(file=sys.stdout)
        LOG.error('Lifecycle-Management: Docker adapter: deploy_docker_image: Exception')
        return common.gen_response(500, 'Exception: deploy_docker_image()', 'agent', str(agent), 'service', str(service))


# deploy_docker_compose:
#   Command:  sudo docker run -v /var/run/docker.sock:/var/run/docker.sock
#               -v /home/atos/mF2C/compose_examples:/home/atos/mF2C/compose_examples
#               -w="/home/atos/mF2C/compose_examples" docker/compose:1.21.0 up
def deploy_docker_compose(service, agent):
    LOG.debug("Lifecycle-Management: Docker adapter: (1) deploy_docker_compose: " + str(service) + ", " + str(agent))
    try:
        # 1. Download docker-compose.yml file
        location = service['exec']
        LOG.debug("Lifecycle-Management: Docker adapter: (2) deploy_docker_compose: Getting docker-compose.yml from "
                  + location + " ...")
        # url = 'https://raw.githubusercontent.com/mF2C/mF2C/master/docker-compose/docker-compose.yml'
        res = wget.download(location, WORKING_DIR_VOLUME + "/docker-compose.yml") #'C://TMP/docker_files/docker-compose.yml')
        LOG.debug("Lifecycle-Management: Docker adapter: (3) deploy_docker_compose: res: " + str(res))

        # 2. Deploy container
        # service_name
        service_name = service['name']
        # command
        service_command = "up"

        # connect to docker api
        client = get_client_agent_docker()

        if client:
            # check if image already exists in agent
            l_images = client.images(name=DOCKER_COMPOSE_IMAGE)  # TODO not tested
            if not l_images or len(l_images) == 0:
                LOG.debug("Lifecycle-Management: Docker adapter: (4) deploy_docker_compose: call to 'import_image' [" + DOCKER_COMPOSE_IMAGE + "] ...")
                client.import_image(tag="1.21.0", image=DOCKER_COMPOSE_IMAGE)

            LOG.debug("Lifecycle-Management: Docker adapter: (5) deploy_docker_compose: [service_image=" + DOCKER_COMPOSE_IMAGE
                      + "], [service_name=" + service_name + "]...")

            # create a new container: 'docker run'
            container = client.create_container(DOCKER_COMPOSE_IMAGE,
                                                command=service_command,
                                                name=service_name,
                                                tty=True,
                                                volumes=[WORKING_DIR_VOLUME, DOCKER_SOCKET_VOLUME],
                                                host_config=client.create_host_config(
                                                    binds={
                                                        WORKING_DIR_VOLUME: {
                                                            'bind': WORKING_DIR_VOLUME,
                                                            'mode': 'rw',
                                                        },
                                                        '/var/run/docker.sock': {
                                                            'bind': DOCKER_SOCKET_VOLUME,
                                                            'mode': 'rw',
                                                        }
                                                    }
                                                ),
                                                working_dir=WORKING_DIR_VOLUME)

            LOG.debug("Lifecycle-Management: Docker adapter: (6) deploy_docker_compose: container: " + str(container))

            # update agent properties
            agent['container_id'] = container['Id']
            agent['status'] = "waiting"
            return common.gen_response_ok('Deploy service in agent', 'agent', str(agent), 'service', str(service))
        else:
            LOG.error("Lifecycle-Management: Docker adapter: deploy_docker_compose: Could not connect to DOCKER API")
            agent['status'] = "error"
            return common.gen_response(500, 'Error when connecting to DOCKER API', 'agent', str(agent), 'service',
                                       str(service))
    except:
        traceback.print_exc(file=sys.stdout)
        LOG.error('Lifecycle-Management: Docker adapter: deploy_docker_compose: Exception')
        return common.gen_response(500, 'Exception: deploy_docker_compose()', 'agent', str(agent), 'service', str(service))


# deploy_service_agent: Deploy service in an agent
# IN: service, agent
# OUT: status value
def deploy_service_agent(service, agent):
    LOG.debug("Lifecycle-Management: Docker adapter: (1) deploy_service_agent: " + str(service) + ", " + str(agent))
    try:
        # docker-compose
        if service['exec_type'] == 'docker-compose':
            return deploy_docker_compose(service, agent)
        # docker
        elif service['exec_type'] == 'docker':
            return deploy_docker_image(service, agent)
        # not defined
        else:
            LOG.warning("Lifecycle-Management: Docker adapter: deploy_service_agent: [" + service['exec_type'] + "] not defined")
            return common.gen_response(500, 'Exception: type not defined: deploy_service_agent()', 'agent', str(agent),
                                       'service', str(service))
    except:
        traceback.print_exc(file=sys.stdout)
        LOG.error('Lifecycle-Management: Docker adapter: deploy_service_agent: Exception')
        return common.gen_response(500, 'Exception: deploy_service_agent()', 'agent', str(agent), 'service', str(service))


# start_service_agent: Start service in agent
def start_service_agent(agent):
    LOG.debug("Lifecycle-Management: Docker adapter: start_service_agent: " + str(agent))

    # connect to docker api
    client = get_client_agent_docker()

    if client:
        # start container
        client.start(agent['container_id'])
        agent['status'] = "Running"
    else:
        LOG.error("Lifecycle-Management: Docker adapter: start_service_agent: Could not connect to DOCKER API")
        agent['status'] = "??"

    return "Started"


# start: Start service
def start(service_instance):
    LOG.debug("Lifecycle-Management: Docker adapter: start: " + str(service_instance))

    for agent in service_instance["agents"]:
        start_service_agent(agent)

    service_instance['status'] = "Running"

    return "Started"


# stop_service_agent: Stop service / stop container
def stop_service_agent(agent):
    LOG.debug("Lifecycle-Management: Docker adapter: stop_service_agent: " + str(agent))

    # connect to docker api
    client = get_client_agent_docker()

    if client:
        # stop container
        client.stop(agent['container_id'])
        client.remove_container(agent['container_id'], force=True)
        agent['status'] = "Stopped"
    else:
        LOG.error("Lifecycle-Management: Docker adapter: stop_service_agent: Could not connect to DOCKER API")
        agent['status'] = "??"

    return "Stopped"


# stop: Stop service / stop container
def stop(service_instance):
    LOG.debug("Lifecycle-Management: Docker adapter: stop: " + str(service_instance))

    for agent in service_instance["agents"]:
        stop_service_agent(agent)

    service_instance['status'] = "Stopped"
    return "Stopped"


# Terminate service
def terminate_service(service_instance):
    LOG.debug("Lifecycle-Management: Docker adapter: terminate_service: " + str(service_instance))
    LOG.warn("Lifecycle-Management: Docker adapter: terminate_service not implemented ")

    # TODO remove service_instance

    return "Terminated"
