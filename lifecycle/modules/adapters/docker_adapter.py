"""
Docker adapter
This is being developed for the MF2C Project: http://www.mf2c-project.eu/

Copyright: Atos Research and Innovation, 2017.

This code is licensed under an Apache 2.0 license. Please, refer to the LICENSE.TXT file for more information

Created on 09 feb. 2018

@author: Roi Sucasas - ATOS
"""


import docker
from lifecycle.utils.logs import LOG


# Get docker api client
def get_client_agent_docker(url):
    try:
        # connect to docker api
        client = docker.APIClient(base_url=url)
        LOG.info("Connected to docker in [" + url + "]; version: " + str(client.version()) +
                 ", api_version: " + str(client.api_version))
        return client
    except:
        LOG.error('Lifecycle-Management: Docker adapter: get_client_agent_docker: Exception: ' + str(url))
        return None


# Deploy / allocate service
# IN:
#   Service instance (example):
#       {
#           "service_instance_id": "service_id",
#           "service_id": service['service_id'],
#           "list_of_agents": [{"url": "192.168.252.7" "container_id": ""}, ...],
#           "status": "",
#           ("service": service)
#       }
def deploy(service_instance):
    LOG.info("Lifecycle-Management: Docker adapter: deploy: " + str(service_instance))

    try:
        # get service image / location
        service_image = "yeasy/simple-web"
        service_name = "simple-web-test"
        service_command = "/bin/sh -c 'python index.py'"

        for agent_ip in service_instance["list_of_agents"]:
            LOG.info("Lifecycle-Management: Docker adapter: deploy: agent_ip: " + str(agent_ip))

            # get url
            url = agent_ip['url']

            # connect to docker api
            client = get_client_agent_docker('tcp://' + url + ':2375') # TODO

            # check if image already exists in agent
            l_images = client.images(name=service_image) # TODO not tested
            if not l_images or len(l_images) == 0:
                client.import_image(tag="latest", image=service_image)
                # client.import_image(tag="latest", image="ubuntu")

            # create a new container
            container = client.create_container(service_image, service_command,
                                                name=service_name,
                                                ports = [80],
                                                host_config = client.create_host_config(port_bindings={80: 81})) #{80: 80, 8080: None}))
            # container = client.create_container("yeasy/simple-web",
            #                                   "/bin/sh -c 'python index.py'",
            #                                   name="simple-web-test",
            #                                   #detach=True,
            #                                   ports = [80],
            #                                   host_config = client.create_host_config(port_bindings={80: 81})) #{80: 80, 8080: None}))

            agent_ip['container_id'] = container['Id']

        service_instance['status'] = "Deployed"
        return True
    except:
        LOG.error('Lifecycle-Management: Docker adapter: deploy: Exception')
        return False


# Terminate service
# IN:
#   Service instance (example):
#       {
#           "service_instance_id": "service_id",
#           "service_id": service['service_id'],
#           "list_of_agents": [{"url": "192.168.252.7" "container_id": ""}, ...],
#           "status": "",
#           ("service": service)
#       }
def terminate_service(service_instance):
    LOG.info("Lifecycle-Management: Docker adapter: terminate_service: " + str(service_instance))
    LOG.warn("Lifecycle-Management: Docker adapter: terminate_service not implemented ")

    # TODO remove service_instance

    return "Terminated"


# Terminate service
# IN:
#   Service instance (example):
#       {
#           "service_instance_id": "service_id",
#           "service_id": service['service_id'],
#           "list_of_agents": [{"url": "192.168.252.7" "container_id": ""}, ...],
#           "status": "",
#           ("service": service)
#       }
def get_status(service_instance):
    LOG.info("Lifecycle-Management: Docker adapter: get_status: " + str(service_instance))
    return service_instance['status']


# Terminate service
# IN:
#   Service instance (example):
#       {
#           "service_instance_id": "service_id",
#           "service_id": service['service_id'],
#           "list_of_agents": [{"url": "192.168.252.7" "container_id": ""}, ...],
#           "status": "",
#           ("service": service)
#       }
def stop(service_instance):
    LOG.info("Lifecycle-Management: Docker adapter: stop: " + str(service_instance))

    for agent_ip in service_instance["list_of_agents"]:
        LOG.info("Lifecycle-Management: Docker adapter: stop: agent_ip: " + str(agent_ip))
        # get url
        url = agent_ip['url']
        # connect to docker api
        client = get_client_agent_docker('tcp://' + url + ':2375')  # TODO
        # start container
        client.stop(agent_ip['container_id'])

    service_instance['status'] = "Stopped"

    return "Stopped"


# Terminate service
# IN:
#   Service instance (example):
#       {
#           "service_instance_id": "service_id",
#           "service_id": service['service_id'],
#           "list_of_agents": [{"url": "192.168.252.7" "container_id": ""}, ...],
#           "status": "",
#           ("service": service)
#       }
def start(service_instance):
    LOG.info("Lifecycle-Management: Docker adapter: start: " + str(service_instance))

    for agent_ip in service_instance["list_of_agents"]:
        LOG.info("Lifecycle-Management: Docker adapter: start: agent_ip: " + str(agent_ip))
        # get url
        url = agent_ip['url']
        # connect to docker api
        client = get_client_agent_docker('tcp://' + url + ':2375')  # TODO
        # start container
        client.start(agent_ip['container_id'])

    service_instance['status'] = "Running"

    return "Started"


# Terminate service
# IN:
#   Service instance (example):
#       {
#           "service_instance_id": "service_id",
#           "service_id": service['service_id'],
#           "list_of_agents": [{"url": "192.168.252.7" "container_id": ""}, ...],
#           "status": "",
#           ("service": service)
#       }
def restart(service_instance):
    LOG.info("Lifecycle-Management: Docker adapter: restart: " + str(service_instance))

    for agent_ip in service_instance["list_of_agents"]:
        LOG.info("Lifecycle-Management: Docker adapter: restart: agent_ip: " + str(agent_ip))
        # get url
        url = agent_ip['url']
        # connect to docker api
        client = get_client_agent_docker('tcp://' + url + ':2375')  # TODO
        # start container
        client.restart(agent_ip['container_id'])

    service_instance['status'] = "Running"

    return "Restarted"