"""
MF2C / COMPSs adapter
This is being developed for the MF2C Project: http://www.mf2c-project.eu/

Copyright: Atos Research and Innovation, 2017.

This code is licensed under an Apache 2.0 license. Please, refer to the LICENSE.TXT file for more information

Created on 09 feb. 2018

@author: Roi Sucasas - ATOS
"""


from lifecycle.utils.logs import LOG


# Deploy / allocate service
# IN:
#   Service instance (example):
#       {
#           "service_instance_id": "service_id",
#           "service_id": service['service_id'],
#           "list_of_agents": ["tcp://192.168.252.7:2375", "tcp://192.168.252.8:2375", "tcp://192.168.252.9:2375" ...],
#           "status": "",
#           ("service": service)
#       }
def deploy(service_instance):
    LOG.info("Lifecycle-Management: Docker adapter: deploy: " + str(service_instance))

    for agent in service_instance["list_of_agents"]:
        LOG.info("Lifecycle-Management: Docker adapter: deploy: agent: " + agent)
        #client = docker.APIClient(base_url='tcp://192.168.252.42:2375')

        #LOG.info("---------------------")
        #LOG.info("version: " + str(client.version()))
        #LOG.info("api_version: " + str(client.api_version))
        #LOG.info("containers: " + str(client.containers()))
        #LOG.info("---------------------")

        #LOG.info("- Start container from image (already downloaded in server)")
        #container = client.create_container("yeasy/simple-web",
        #                                   "/bin/sh -c 'python index.py'",
        #                                   name="simple-web-test",
        #                                   #detach=True,
        #                                   ports = [80],
        #                                   host_config = client.create_host_config(port_bindings={80: 81})) #{80: 80, 8080: None}))
        #LOG.info(str(container))
        #LOG.info(container['Id'])
        #client.start(container['Id'])

        LOG.info("---------------------")

        #client.import_image(tag="latest", image="ubuntu")

    return True


# Terminate service
# IN:
#   Service instance (example):
#       {
#           "service_instance_id": "service_id",
#           "service_id": service['service_id'],
#           "list_of_agents": ["tcp://192.168.252.7:2375", "tcp://192.168.252.8:2375", "tcp://192.168.252.9:2375" ...],
#           "status": "",
#           ("service": service)
#       }
def terminate_service(service_instance):
    LOG.info("Lifecycle-Management: Docker adapter: terminate_service: " + str(service_instance))
    LOG.warn("Lifecycle-Management: Docker adapter: terminate_service not implemented ")
    return "Terminated"


# Terminate service
# IN:
#   Service instance (example):
#       {
#           "service_instance_id": "service_id",
#           "service_id": service['service_id'],
#           "list_of_agents": ["tcp://192.168.252.7:2375", "tcp://192.168.252.8:2375", "tcp://192.168.252.9:2375" ...],
#           "status": "",
#           ("service": service)
#       }
def get_status(service_instance):
    LOG.info("Lifecycle-Management: Docker adapter: get_status: " + str(service_instance))
    LOG.warn("Lifecycle-Management: Docker adapter: get_status not implemented ")
    return "Running"


# Terminate service
# IN:
#   Service instance (example):
#       {
#           "service_instance_id": "service_id",
#           "service_id": service['service_id'],
#           "list_of_agents": ["tcp://192.168.252.7:2375", "tcp://192.168.252.8:2375", "tcp://192.168.252.9:2375" ...],
#           "status": "",
#           ("service": service)
#       }
def stop(service_instance):
    LOG.info("Lifecycle-Management: Docker adapter: stop: " + str(service_instance))
    LOG.warn("Lifecycle-Management: Docker adapter: stop not implemented ")
    return "Stopped"


# Terminate service
# IN:
#   Service instance (example):
#       {
#           "service_instance_id": "service_id",
#           "service_id": service['service_id'],
#           "list_of_agents": ["tcp://192.168.252.7:2375", "tcp://192.168.252.8:2375", "tcp://192.168.252.9:2375" ...],
#           "status": "",
#           ("service": service)
#       }
def start(service_instance):
    LOG.info("Lifecycle-Management: Docker adapter: start: " + str(service_instance))
    LOG.warn("Lifecycle-Management: Docker adapter: start not implemented ")
    return "Started"


# Terminate service
# IN:
#   Service instance (example):
#       {
#           "service_instance_id": "service_id",
#           "service_id": service['service_id'],
#           "list_of_agents": ["tcp://192.168.252.7:2375", "tcp://192.168.252.8:2375", "tcp://192.168.252.9:2375" ...],
#           "status": "",
#           ("service": service)
#       }
def restart(service_instance):
    LOG.info("Lifecycle-Management: Docker adapter: restart: " + str(service_instance))
    LOG.warn("Lifecycle-Management: Docker adapter: restart not implemented ")
    return "Restarted"