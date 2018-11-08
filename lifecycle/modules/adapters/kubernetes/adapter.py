"""
Docker adapter
This is being developed for the MF2C Project: http://www.mf2c-project.eu/

Copyright: Atos Research and Innovation, 2017.

This code is licensed under an Apache 2.0 license. Please, refer to the LICENSE.TXT file for more information

Created on 18 oct. 2018

@author: Roi Sucasas - ATOS
"""

import common.common as common
import sys, traceback
from common.logs import LOG
from common.common import OPERATION_START, OPERATION_STOP, OPERATION_TERMINATE, STATUS_ERROR, STATUS_STARTED, STATUS_TERMINATED
from kubernetes import config as k8scfg
from kubernetes import client as k8sclient

# https://kubernetes.io/docs/tasks/access-application-cluster/configure-access-multiple-clusters/

'''
 Data managed by this component:
 SERVICE:
       {
           "name": "hello-world",
           "description": "Hello World Service",
           "resourceURI": "/hello-world",
           "exec": "hello-world",
           "exec_type": "kubernetes",
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
                    "kubernetes" ....... "exec" = docker image (docker hub)
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

# deploy_service:
# IN: service, agent
# OUT: status value
def deploy_service(service, agent):
    LOG.debug("Lifecycle-Management: K8s adapter: (1) deploy_service: " + str(service) + ", " + str(agent))
    try:
        # load config
        k8scfg.load_kube_config()
        # create deployment
        k8sclient.AppsV1Api().create_namespaced_deployment(namespace="default",
                                                           body={})
        # create service
        k8sclient.CoreV1Api().create_namespaced_service(namespace="default",
                                                        body={})

        agent['status'] = STATUS_STARTED

        # v1 = k8sclient.CoreV1Api()
        # print("Listing pods with their IPs:")
        # ret = v1.list_pod_for_all_namespaces(watch=False)

        '''
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
            SERVICE_INSTANCES_LIST.append({
                "type": "docker",
                "container_main": container1['Id'],
                "container_2": "-"
            })
            LOG.debug("  > container: " + str(container1))

            # update agent properties
            agent['container_id'] = container1['Id']
            agent['status'] = STATUS_WAITING
            return common.gen_response_ok('Deploy service in agent', 'agent', str(agent), 'service', str(service))
        else:
            LOG.error("Lifecycle-Management: K8s adapter: deploy_docker_image: Could not connect to K8s API")
            agent['status'] = STATUS_ERROR
            return common.gen_response(500, 'Error when connecting to K8s API', 'agent', str(agent), 'service', str(service))
        '''
    except:
        traceback.print_exc(file=sys.stdout)
        LOG.error('Lifecycle-Management: K8s adapter: deploy_service: Exception')
        return common.gen_response(500, 'Exception: deploy_service()', 'agent', str(agent), 'service', str(service))


###############################################################################
# OPERATIONS:

# operation_service: service operation (start, stop...)
def operation_service(agent, operation):
    LOG.debug("Lifecycle-Management: K8s adapter: operation_service [" + operation + "]: " + str(agent))
    try:
        # load config
        k8scfg.load_kube_config()

        if operation == OPERATION_START:
            '''
            # create deployment
            k8sclient.AppsV1Api().create_namespaced_deployment(namespace="default",
                                                               body={})
            # create service
            k8sclient.CoreV1Api().create_namespaced_service(namespace="default",
                                                            body={})

            agent['status'] = STATUS_STARTED
            '''

        elif operation == OPERATION_STOP:
            '''
            # create deployment
            k8sclient.AppsV1Api().create_namespaced_deployment(namespace="default",
                                                               body={})
            # create service
            k8sclient.CoreV1Api().create_namespaced_service(namespace="default",
                                                            body={})
            agent['status'] = STATUS_STOPPED
            '''

        elif operation == OPERATION_TERMINATE:
            # delete deployment
            k8sclient.AppsV1Api().delete_namespaced_deployment(name="",
                                                               namespace="default")
            # delete service
            k8sclient.CoreV1Api().delete_namespaced_service(name="",
                                                            namespace="default")
            agent['status'] = STATUS_TERMINATED

        # return status
        return agent['status']
    except:
        agent['status'] = STATUS_ERROR
        traceback.print_exc(file=sys.stdout)
        LOG.error('Lifecycle-Management: K8s adapter: operation_service: Exception')
        return STATUS_ERROR


# start_service_agent: Start service in agent
def start_service(agent):
    return operation_service(agent, OPERATION_START)


# stop_service_agent: Stop service / stop container
def stop_service(agent):
    return operation_service(agent, OPERATION_STOP)


# terminate_service_agent: Stop service / stop container
def terminate_service(agent):
    return operation_service(agent, OPERATION_TERMINATE)
