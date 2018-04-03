"""
Docker adapter
This is being developed for the MF2C Project: http://www.mf2c-project.eu/

Copyright: Atos Research and Innovation, 2017.

This code is licensed under an Apache 2.0 license. Please, refer to the LICENSE.TXT file for more information

Created on 09 feb. 2018

@author: Roi Sucasas - ATOS
"""


import docker
import requests
import sys, traceback
from lifecycle.utils.logs import LOG


# Get docker api client
def get_client_agent_docker(url):
    try:
        # connect to docker api
        # client = docker.APIClient(base_url='unix://var/run/docker.sock')
        client = docker.APIClient(base_url=url) #'tcp://192.168.252.42:2375') #172.17.0.1:2375')

        try:
            LOG.info(">> " + str(client))
            LOG.info(">> " + str(client.version()))
            LOG.info("Connected to docker in [" + url + "]; version: " + str(client.version()))
        except:
            LOG.error("Error when connecting to DOCKER API")

        return client
    except:
        LOG.error('Lifecycle-Management: Docker adapter: get_client_agent_docker: Exception: ' + str(url))
        return None


# Deploy / allocate service
# IN:
#   Service instance (example):
#    {
#    	"id": URI,
#    	"name": string,
#    	"description": "profiling ...",
#    	"created": dateTime,
#    	"updated": dateTime,
#    	"resourceURI": URI,
#    	"service_id": string,
#       "agreement_id": string,
#    	"status": string,
#    	"agents": [
#        {"agent": resource-link, "url": "192.168.1.31", "port": int, "container_id": string, "status": string, "num_cpus": int}
#      ]
#    }
def deploy(service_instance):
    LOG.info("Lifecycle-Management: Docker adapter: deploy: " + str(service_instance))

    try:
        # get service image / location
        service_image = "mf2c/compss-mf2c:1.0"      #""yeasy/simple-web"
        service_name = "app-compss"                 #""simple-web-test"
        #service_command = "/bin/sh -c 'python index.py'"

        for agent in service_instance["agents"]:
            LOG.info("Lifecycle-Management: Docker adapter: deploy: agent: " + str(agent))
            # get url
            url = agent['url']
            # connect to docker api
            client = get_client_agent_docker('tcp://' + url + ':2375') # TODO
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
            agent['container_id'] = container['Id']

        service_instance['status'] = "Deployed"
        return True
    except:
        traceback.print_exc(file=sys.stdout)
        LOG.error('Lifecycle-Management: Docker adapter: deploy: Exception')
        return False


# Terminate service
def terminate_service(service_instance):
    LOG.info("Lifecycle-Management: Docker adapter: terminate_service: " + str(service_instance))
    LOG.warn("Lifecycle-Management: Docker adapter: terminate_service not implemented ")

    # TODO remove service_instance

    return "Terminated"


# Return service's status
def get_status(service_instance):
    LOG.info("Lifecycle-Management: Docker adapter: get_status: " + str(service_instance))
    return service_instance['status']


# Stop service / stop container
def stop(service_instance):
    LOG.info("Lifecycle-Management: Docker adapter: stop: " + str(service_instance))

    for agent in service_instance["agents"]:
        LOG.info("Lifecycle-Management: Docker adapter: stop: agent: " + str(agent))
        # get url
        url = agent['url']
        # connect to docker api
        client = get_client_agent_docker('tcp://' + url + ':2375')  # TODO
        # stop container
        client.stop(agent['container_id'])
        client.remove_container(agent['container_id'], force=True)

    service_instance['status'] = "Stopped"
    return "Stopped"


# Start app inside container
def start_compss_app(service_instance):
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

        requests.put('http://192.168.252.41:8080/COMPSs/startApplication',
                     data=xml,
                     headers={'Content-Type': 'application/xml'})

        return True
    except:
        traceback.print_exc(file=sys.stdout)
        LOG.error('Lifecycle-Management: Docker adapter: start_app: Exception')
        return False


# Start service
def start(service_instance):
    LOG.info("Lifecycle-Management: Docker adapter: start: " + str(service_instance))

    for agent in service_instance["agents"]:
        LOG.info("Lifecycle-Management: Docker adapter: start: agent_ip: " + str(agent))
        # get url
        url = agent['url']
        # connect to docker api
        client = get_client_agent_docker('tcp://' + url + ':2375')  # TODO
        # start container
        client.start(agent['container_id'])

    service_instance['status'] = "Running"

    return "Started"


# Restart service
def restart(service_instance):
    LOG.info("Lifecycle-Management: Docker adapter: restart: " + str(service_instance))

    for agent in service_instance["agents"]:
        LOG.info("Lifecycle-Management: Docker adapter: restart: agent_ip: " + str(agent))
        # get url
        url = agent['url']
        # connect to docker api
        client = get_client_agent_docker('tcp://' + url + ':2375')  # TODO
        # start container
        client.restart(agent['container_id'])

    service_instance['status'] = "Running"

    return "Restarted"



###############################################################################

def main():
    # '''
    LOG.info("-------------------------------")
    service_instance = {
        	"id": "id....",
        	"name": "name....",
        	"description": "profiling ...",
        	#"created": dateTime,
        	#"updated": dateTime,
        	#"resourceURI": URI,
        	"service_id": "service_id....",
            "agreement_id": "agreement_id....",
        	"status": "none",
        	"agents": [
            {"agent": "", "url": "192.168.252.41", "port": 8080, "container_id": "", "status": "none", "num_cpus": 0}
          ]
        }
    deploy(service_instance)

    LOG.info("-------------------------------")
    start(service_instance)     # start container

    LOG.info("-------------------------------")
    start_compss_app(service_instance) # start app (in container)

    LOG.info("-------------------------------")
    stop(service_instance)

    LOG.info("-------------------------------")
    # '''


if __name__ == "__main__":
    main()