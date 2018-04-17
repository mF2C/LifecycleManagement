"""
Docker adapter
This is being developed for the MF2C Project: http://www.mf2c-project.eu/

Copyright: Atos Research and Innovation, 2017.

This code is licensed under an Apache 2.0 license. Please, refer to the LICENSE.TXT file for more information

Created on 09 feb. 2018

@author: Roi Sucasas - ATOS
"""

import lifecycle.utils.common as common
import docker
import requests
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
'''


# get_client_agent_docker: Get docker api client
# connect to docker api: Examples: base_url='tcp://192.168.252.42:2375'; base_url='unix://var/run/docker.sock'
def get_client_agent_docker():
    LOG.info("Connecting to DOCKER API [unix://var/run/docker.sock]...")
    try:
        client = docker.APIClient(base_url='unix://var/run/docker.sock')
        LOG.info("Connected to DOCKER in [unix://var/run/docker.sock]; version: " + str(client.version()))
        return client
    except:
        LOG.error('Lifecycle-Management: Docker adapter: get_client_agent_docker: Error when connecting to DOCKER API: '
                  'unix://var/run/docker.sock')
        return None


# deploy: Deploy / allocate service
# IN: service_instance
def deploy(service_instance):
    LOG.info("Lifecycle-Management: Docker adapter: deploy: " + str(service_instance))

    try:
        # get service image / location
        service_image = "mf2c/compss-mf2c:1.0"      #""yeasy/simple-web"
        service_name = "app-compss"                 #""simple-web-test"
        #service_command = "/bin/sh -c 'python index.py'"

        for agent in service_instance["agents"]:
            LOG.info("Lifecycle-Management: Docker adapter: deploy: agent: " + str(agent))
            # connect to docker api
            client = get_client_agent_docker() # TODO

            if client:
                # check if image already exists in agent
                l_images = client.images(name=service_image) # TODO not tested
                if not l_images or len(l_images) == 0:
                    LOG.info("Lifecycle-Management: Docker adapter: deploy: call to 'import_image' [" + service_image + "] ...")
                    client.import_image(tag="latest", image=service_image) # (tag="latest", image="ubuntu")

                # create a new container: 'docker run'
                container = client.create_container(service_image, #command=service_command,
                                                    name=service_name,
                                                    tty=True,
                                                    ports=[8080],
                                                    host_config=client.create_host_config(port_bindings={8080: 8080}))
                # update agent properties
                agent['container_id'] = container['Id']
                agent['status'] = "waiting"
            else:
                LOG.error("Lifecycle-Management: Docker adapter: deploy: Could not connect to DOCKER API")
                agent['status'] = "error"

        service_instance['status'] = "Deployed"
        return True
    except:
        traceback.print_exc(file=sys.stdout)
        LOG.error('Lifecycle-Management: Docker adapter: deploy: Exception')
        return False


# deploy_service_agent: Deploy service in an agent
# IN: service
#    {"agent": resource-link, "url": "192.168.1.31", "port": 8081, "container_id": "10asd673f", "status": "waiting",
#     "num_cpus": 3, "allow": true}
# OUT: status value
def deploy_service_agent(service, agent):
    LOG.info("Lifecycle-Management: Docker adapter: deploy_service_agent: " + str(service) + ", " + str(agent))

    try:
        # get service image / location
        service_image = service['exec'] # "mf2c/compss-mf2c:1.0"      #""yeasy/simple-web"
        service_name = service['name'] # "app-compss"                 #""simple-web-test"
        #service_command = "/bin/sh -c 'python index.py'"

        # get url / port
        port = agent['port']    # TODO check/improve ports
        # connect to docker api
        client = get_client_agent_docker()

        if client:
            # check if image already exists in agent
            l_images = client.images(name=service_image)
            # if not, download image
            if not l_images or len(l_images) == 0:
                LOG.info("Lifecycle-Management: Docker adapter: deploy: call to 'import_image' [" + service_image + "] ...")
                client.import_image(image=service_image)  # (tag="latest", image="ubuntu") # (tag="latest", image="ubuntu")

            LOG.info("Lifecycle-Management: Docker adapter: deploy_service_agent: " + service_image + ", " + service_name + " ...")
            # create a new container: 'docker run'
            container = client.create_container(service_image, #command=service_command,
                                                name=service_name,
                                                tty=True,
                                                ports=[port],
                                                host_config=client.create_host_config(port_bindings={port: port}))
            # update agent properties
            agent['container_id'] = container['Id']
            agent['status'] = "waiting"
            return common.gen_response_ok('Deploy service in agent', 'agent', str(agent), 'service', str(service))
        else:
            LOG.error("Lifecycle-Management: Docker adapter: deploy_service_agent: Could not connect to DOCKER API")
            agent['status'] = "error"
            return common.gen_response(500, 'Error when connecting to DOCKER API', 'agent', str(agent), 'service', str(service))
    except:
        traceback.print_exc(file=sys.stdout)
        LOG.error('Lifecycle-Management: Docker adapter: deploy_service_agent: Exception')
        return common.gen_response(500, 'Exception: deploy_service_agent()', 'agent', str(agent), 'service', str(service))


# Return service's status
def get_status(service_instance):
    LOG.info("Lifecycle-Management: Docker adapter: get_status: " + str(service_instance))
    return service_instance['status']


# Start app inside container
def start_compss_app(service_instance, agent):
    LOG.info("Lifecycle-Management: Docker adapter: start_app")

    try:
        xml = "<?xml version='1.0' encoding='utf-8'?>" \
              "<startApplication>" \
              "  <ceiClass>es.bsc.compss.test.TestItf</ceiClass>" \
              "  <className>es.bsc.compss.test.Test</className>" \
              "  <methodName>main</methodName>" \
              "  <parameters>" \
              "    <array paramId=\"0\">" \
              "      <componentClassname>java.lang.String</componentClassname>" \
              "      <values>" \
              "        <element paramId=\"0\">" \
              "          <className>java.lang.String</className>" \
              "          <value xmlns:xsi=\"http://www.w3.org/2001/XMLSchema-instance\" " \
              "             xmlns:xs=\"http://www.w3.org/2001/XMLSchema\" xsi:type=\"xs:string\">3</value>" \
              "        </element>" \
              "      </values>" \
              "    </array>" \
              "  </parameters>" \
              "  <resources>" \
              "    <resource name=\"localhost:8080\">" \
              "      <description>" \
              "        <memorySize>4.0</memorySize>" \
              "        <memoryType>[unassigned]</memoryType>" \
              "        <operatingSystemDistribution>[unassigned]</operatingSystemDistribution>" \
              "        <operatingSystemType>[unassigned]</operatingSystemType>" \
              "        <operatingSystemVersion>[unassigned]</operatingSystemVersion>" \
              "        <pricePerUnit>-1.0</pricePerUnit>" \
              "        <priceTimeUnit>-1</priceTimeUnit>" \
              "        <processors>" \
              "          <architecture>[unassigned]</architecture>" \
              "          <computingUnits>2</computingUnits>" \
              "          <internalMemory>-1.0</internalMemory>" \
              "          <name>[unassigned]</name>" \
              "          <propName>[unassigned]</propName>" \
              "          <propValue>[unassigned]</propValue>" \
              "          <speed>-1.0</speed>" \
              "          <type>CPU</type>" \
              "        </processors>" \
              "        <storageSize>-1.0</storageSize>" \
              "        <storageType>[unassigned]</storageType>" \
              "        <value>0.0</value>" \
              "        <wallClockLimit>-1</wallClockLimit>" \
              "      </description>" \
              "    </resource>" \
              "  </resources>" \
              "</startApplication>"

        requests.put("http://127.0.0.1:8080/COMPSs/startApplication",
                     data=xml,
                     headers={'Content-Type': 'application/xml'})

        return True
    except:
        traceback.print_exc(file=sys.stdout)
        LOG.error('Lifecycle-Management: Docker adapter: start_app: Exception')
        return False


# start_service_agent: Start service in agent
def start_service_agent(agent):
    LOG.info("Lifecycle-Management: Docker adapter: start_service_agent: " + str(agent))

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
    LOG.info("Lifecycle-Management: Docker adapter: start: " + str(service_instance))

    for agent in service_instance["agents"]:
        start_service_agent(agent)

    service_instance['status'] = "Running"

    return "Started"


# restart_service_agent: Restart service in agent
def restart_service_agent(agent):
    LOG.info("Lifecycle-Management: Docker adapter: restart_service_agent: " + str(agent))

    # connect to docker api
    client = get_client_agent_docker()

    if client:
        # start container
        client.restart(agent['container_id'])
        agent['status'] = "Running"
    else:
        LOG.error("Lifecycle-Management: Docker adapter: restart_service_agent: Could not connect to DOCKER API")
        agent['status'] = "??"

    return "Restarted"


# restart: Restart service
def restart(service_instance):
    LOG.info("Lifecycle-Management: Docker adapter: restart: " + str(service_instance))

    for agent in service_instance["agents"]:
        restart_service_agent(agent)

    service_instance['status'] = "Running"

    return "Restarted"


# stop_service_agent: Stop service / stop container
def stop_service_agent(agent):
    LOG.info("Lifecycle-Management: Docker adapter: stop_service_agent: " + str(agent))

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
    LOG.info("Lifecycle-Management: Docker adapter: stop: " + str(service_instance))

    for agent in service_instance["agents"]:
        stop_service_agent(agent)

    service_instance['status'] = "Stopped"
    return "Stopped"


# Terminate service
def terminate_service(service_instance):
    LOG.info("Lifecycle-Management: Docker adapter: terminate_service: " + str(service_instance))
    LOG.warn("Lifecycle-Management: Docker adapter: terminate_service not implemented ")

    # TODO remove service_instance

    return "Terminated"

