"""
Docker client
This is being developed for the MF2C Project: http://www.mf2c-project.eu/

Copyright: Atos Research and Innovation, 2017.

This code is licensed under an Apache 2.0 license. Please, refer to the LICENSE.TXT file for more information

Created on 09 feb. 2018

@author: Roi Sucasas - ATOS
"""


import docker
from lifecycle.utils.logs import LOG
from lifecycle import config


# docker socket connection
DOCKER_SOCKET = "unix://var/run/docker.sock"


# get_client_agent_docker: Get docker api client
# connect to docker api: Examples: base_url='tcp://192.168.252.42:2375'; base_url='unix://var/run/docker.sock'
def get_client_agent_docker():
    LOG.debug("Lifecycle-Management: Docker client: Connecting to DOCKER API [" + DOCKER_SOCKET + "]...")
    try:
        client = docker.APIClient(base_url=DOCKER_SOCKET)
        LOG.debug("Lifecycle-Management: Docker client: Connected to DOCKER in [" + DOCKER_SOCKET + "]; version: " + str(client.version()))
        return client
    except:
        LOG.error("Lifecycle-Management: Docker client: get_client_agent_docker: Error when connecting to DOCKER API: " + DOCKER_SOCKET)
        return None


# create_docker_compose_container
def create_docker_container(service_image, service_name, service_command, port):
    LOG.debug("Lifecycle-Management: Docker client: create_docker_container: [service_name=" + service_name + "], "
              "[service_command=" + service_command + "], [service_image=" + service_image + "], "
              "[port=" + str(port) + "]")
    # connect to docker api
    client = get_client_agent_docker()
    try:
        if client:
            # check if image already exists in agent
            l_images = client.images(name=service_image)
            # if not, download image
            if not l_images or len(l_images) == 0:
                LOG.debug("Lifecycle-Management: Docker client: create_docker_container: call to 'import_image' [" + service_image + "] ...")
                client.import_image(image=service_image)  # (tag="latest", image="ubuntu") # (tag="latest", image="ubuntu")

            LOG.debug("Lifecycle-Management: Docker client: create_docker_container: [service_image=" + service_image
                      + "], [service_name=" + service_name + "],  [port=" + str(port) + "]...")

            # create a new container: 'docker run'
            container = client.create_container(service_image,  # command=service_command,
                                                name=service_name,
                                                tty=True,
                                                ports=[port],
                                                host_config=client.create_host_config(port_bindings={port: port}))
            return container
        else:
            LOG.error("Lifecycle-Management: Docker adapter: create_docker_container: Could not connect to DOCKER API")
            return None
    except:
        LOG.error("Lifecycle-Management: Docker client: create_docker_container: Exception")
        return None


# create_docker_compose_container
def create_docker_compose_container(service_name, service_command):
    LOG.debug("Lifecycle-Management: Docker client: create_docker_compose_container: [service_name=" + service_name +"], "
              "[service_command=" + service_command + "]")
    try:
        # connect to docker api
        client = get_client_agent_docker()
        if client:
            # check if image already exists in agent
            l_images = client.images(name=config.dic['DOCKER_COMPOSE_IMAGE'])
            if not l_images or len(l_images) == 0:
                LOG.debug("Lifecycle-Management: Docker client: create_docker_compose_container: call to 'import_image' [" +
                          config.dic['DOCKER_COMPOSE_IMAGE'] + "] ...")
                client.import_image(tag=config.dic['DOCKER_COMPOSE_IMAGE_TAG'], image=config.dic['DOCKER_COMPOSE_IMAGE'])

            # create a new container: 'docker run'
            container = client.create_container(config.dic['DOCKER_COMPOSE_IMAGE'],
                                                command=service_command,
                                                name=service_name,
                                                tty=True,
                                                volumes=[config.dic['WORKING_DIR_VOLUME'], config.dic['DOCKER_SOCKET_VOLUME']],
                                                host_config=client.create_host_config(
                                                    binds={
                                                        config.dic['WORKING_DIR_VOLUME']: {
                                                            'bind': config.dic['WORKING_DIR_VOLUME'],
                                                            'mode': 'rw',
                                                        },
                                                        '/var/run/docker.sock': {
                                                            'bind': config.dic['DOCKER_SOCKET_VOLUME'],
                                                            'mode': 'rw',
                                                        }
                                                    }
                                                ),
                                                working_dir=config.dic['WORKING_DIR_VOLUME'])
            return container
        else:
            LOG.error("Lifecycle-Management: Docker client: deploy_docker_compose: Could not connect to DOCKER API")
            return None
    except:
        LOG.error("Lifecycle-Management: Docker client: deploy_docker_compose: Exception")
        return None