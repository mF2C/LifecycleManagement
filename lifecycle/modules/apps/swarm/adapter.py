"""
Docker adapter
This is being developed for the MF2C Project: http://www.mf2c-project.eu/

Copyright: Atos Research and Innovation, 2017.

This code is licensed under an Apache 2.0 license. Please, refer to the LICENSE.TXT file for more information

Created on 18 oct. 2018

@author: Roi Sucasas - ATOS
"""

import docker, uuid, sys, traceback, time
import common.common as common
import lifecycle.modules.apps.docker.ports_mngr as pmngr
from flask import json
import lifecycle.modules.apps.docker.client as docker_client
import lifecycle.data.db as db
from common.logs import LOG
import config
from common.common import OPERATION_START, OPERATION_STOP, OPERATION_TERMINATE, \
    STATUS_ERROR, STATUS_WAITING, STATUS_STARTED, STATUS_STOPPED, \
    STATUS_TERMINATED, STATUS_UNKNOWN

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
-----------------------------------------------------------------------------------------------
 DOCKER SWARM SERVICE:
     {
        'Endpoint': {
            'Ports': [{
                    'TargetPort': 80,
                    'Protocol': 'tcp',
                    'PublishedPort': 8013,
                    'PublishMode': 'ingress'
                }
            ],
            'Spec': {
                'Ports': [{
                        'TargetPort': 80,
                        'Protocol': 'tcp',
                        'PublishedPort': 8013,
                        'PublishMode': 'ingress'
                    }
                ],
                'Mode': 'vip'
            },
            'VirtualIPs': [{
                    'NetworkID': '4y6asogm7yqlvp48rf44xxzlu',
                    'Addr': '10.255.0.4/16'
                }
            ]
        },
        'CreatedAt': '2018-11-27T15:31:11.391088745Z',
        'Version': {
            'Index': 187
        },
        'Spec': {
            'EndpointSpec': {
                'Ports': [{
                        'TargetPort': 80,
                        'Protocol': 'tcp',
                        'PublishedPort': 8013,
                        'PublishMode': 'ingress'
                    }
                ],
                'Mode': 'vip'
            },
            'Mode': {
                'Replicated': {
                    'Replicas': 1
                }
            },
            'TaskTemplate': {
                'ContainerSpec': {
                    'Image': 'nginx:latest@sha256:31b8e90a349d1fce7621f5a5a08e4fc519b634f7d3feb09d53fac9b12aa4d991',
                    'TTY': True
                },
                'ForceUpdate': 0
            },
            'Name': 'my_nginx_app',
            'Labels': {}
        },
        'UpdatedAt': '2018-11-27T15:31:11.39351795Z',
        'ID': 'qaxt11ejf36utnf3gy8gmrlzz'
    }
'''

# docker socket connection
DOCKER_SOCKET = config.dic['DOCKER_SOCKET'] #"unix://var/run/docker.sock"
# client
client = None


# replace_in_list: replace element in list
def replace_in_list(l, xvalue, newxvalue):
    for n, i in enumerate(l):
        if i == xvalue:
            l[n] = newxvalue
    return l


# create_ports_dict:
def create_ports_dict(ports):
    try:
        LOG.debug("LIFECYCLE: Docker Swarm: create_ports_dict: Configuring ports [" + str(ports) + "]...")
        l_ports = []
        for p in ports:
            LOG.debug("LIFECYCLE: Docker Swarm: create_ports_dict: port [" + str(p) + "]...")
            if pmngr.is_port_free(p):
                l_ports.append({'Protocol': 'tcp', 'PublishedPort': p, 'TargetPort': p})
                pmngr.take_port(p, p)
                LOG.debug("LIFECYCLE: Docker Swarm: create_ports_dict: port free")
            else:
                np = pmngr.assign_new_port()
                # original port : new port (exposed to host)
                l_ports.append({'Protocol': 'tcp', 'PublishedPort': np, 'TargetPort': p}) # dict_ports.update({p: np})
                pmngr.take_port(np, p)
                replace_in_list(ports, p, np)
                LOG.debug("LIFECYCLE: Docker Swarm: create_ports_dict: port not free: redirected to " + str(np))

        return l_ports
    except:
        LOG.error("LIFECYCLE: Docker Swarm: create_ports_dict: Error during the ports dict creation: " + str(ports))
        return {ports[0]:ports[0]}


# get_client_agent_docker: Get docker api client
# connect to docker api: Examples: base_url='tcp://192.168.252.42:2375'; base_url='unix://var/run/docker.sock'
def get_client_agent_docker():
    global client
    LOG.debug("LIFECYCLE: Docker Swarm: Connecting to DOCKER API [" + DOCKER_SOCKET + "], "
              "[SWARM MASTER? " + str(False) + "] [client=" + str(client) + "],...")
    try:
        try:
            if client is not None:
                client.version()
                LOG.debug("LIFECYCLE: Docker Swarm: Returning existing client [" + json.dumps(client) + "] ...")
                return client
        except:
            LOG.error("LIFECYCLE: Docker Swarm: docker client gave an error. Trying to reconnect to docker...")

        client = docker.APIClient(base_url=DOCKER_SOCKET)
        LOG.debug("LIFECYCLE: Docker Swarm: Connected to DOCKER in [" + DOCKER_SOCKET + "]; version: " + json.dumps(client.version()))
        return client
    except:
        traceback.print_exc(file=sys.stdout)
        LOG.error("LIFECYCLE: Docker Swarm: get_client_agent_docker: Error when connecting to DOCKER API: " + DOCKER_SOCKET)
        return None


# create_docker_service
def create_docker_service(service_image, service_name, service_command, prts, replicas, service, agent):
    LOG.debug("LIFECYCLE: Docker Swarm: create_docker_service: [service_name=" + service_name + "], "
              "[service_command=" + service_command + "], [service_image=" + service_image + "], [ports=" + str(prts) + "]")

    # connect to docker api
    lclient = get_client_agent_docker()
    try:
        if lclient:
            # check if image already exists in agent
            l_images = lclient.images(name=service_image)
            # if not, download image
            if not l_images or len(l_images) == 0:
                LOG.debug("LIFECYCLE: Docker Swarm: create_docker_service: call to 'import_image' [" + service_image + "] ...")
                lclient.import_image(image=service_image)  # (tag="latest", image="ubuntu") # (tag="latest", image="ubuntu")

            LOG.debug("LIFECYCLE: Docker Swarm: create_docker_service: Creating service ...")

            prts_list = list(prts)
            ports_list = create_ports_dict(prts)
            LOG.debug("LIFECYCLE: Docker Swarm: create_docker_service: ports_list: " + str(ports_list))
            LOG.debug("LIFECYCLE: Docker Swarm: create_docker_service: prts: " + str(prts))
            LOG.debug("LIFECYCLE: Docker Swarm: create_docker_service: prts_list: " + str(prts_list))

            # ContainerSpec:
            # (self, image, command=None, args=None, hostname=None, env=None,
            #   workdir=None, user=None, labels=None, mounts=None,
            #   stop_grace_period=None, secrets=None, tty=None, groups=None,
            #   open_stdin=None, read_only=None, stop_signal=None,
            #   healthcheck=None, hosts=None, dns_config=None, configs=None,
            #   privileges=None, isolation=None)
            container_spec = docker.types.ContainerSpec(image=service_image,
                                                        tty=True,
                                                        command=service_command)

            # TaskTemplate:
            # (self, container_spec, resources=None, restart_policy=None,
            #   placement=None, log_driver=None, networks=None,
            #   force_update=None)
            task_tmpl = docker.types.TaskTemplate(container_spec)

            # ServiceMode:
            #   (self, mode, replicas=None)
            serv_mode = docker.types.ServiceMode(mode="replicated", replicas=replicas)

            # create a new service (DOCKER SWARM):
            # create_service(task_template, name=None, labels=None, mode=None, update_config=None, networks=None,
            #                endpoint_config=None, endpoint_spec=None, rollback_config=None)
            res = lclient.create_service(task_tmpl,
                                         name=service_name,
                                         mode=serv_mode,
                                         endpoint_spec={
                                             'Ports': ports_list
                                                #[{'Protocol': 'tcp', 'PublishedPort': 8013, 'TargetPort': 80}]
                                         }) # published_port: target_port

            #SERVICE_INSTANCES_LIST.append({
            #    "type": "docker",
            #    "container_main": container1['Id'],
            #    "container_2": "-"
            #})
            #LOG.debug("  > container: " + str(container1))

            # update agent properties
            agent['container_id'] = res['ID'] #container1['Id']
            agent['status'] = STATUS_WAITING
            return common.gen_response_ok('Deploy service in agent (Docker Swarm)', 'agent', str(agent), 'service', str(service))
            #LOG.debug("LIFECYCLE: Docker Swarm: create_docker_service: create_service: " + str(res))
            #return res
        else:
            LOG.error("LIFECYCLE: Docker Swarm: create_docker_service: Could not connect to DOCKER API")
            agent['status'] = STATUS_ERROR
            return common.gen_response(500, 'Error when connecting to DOCKER API', 'agent', str(agent), 'service', str(service))
    except:
        traceback.print_exc(file=sys.stdout)
        LOG.error('LIFECYCLE: Docker Swarm: create_docker_service: Exception')
        return common.gen_response(500, 'Exception: deploy_docker_image()', 'agent', str(agent), 'service', str(service))


# deploy_service_agent
# TODO
def deploy_service_agent(service, agent):
    # Example: create_docker_service("nginx:latest", "my_nginx_app", "", [80], 1)
    # service image / location.
    service_image = service['exec']
    # service_name examples: "simple-web-test"
    service_name = service['name'] + "-" + str(uuid.uuid4())
    # command. Docker examples: "/bin/sh -c 'python index.py'"
    service_command = ""
    # port(s)
    ports = agent['ports']

    create_docker_service(service_image, service_name, service_command, ports, 1, service, agent)


# update_docker_service
def update_docker_service(service_id, service_image, service_name, replicas, version):
    LOG.debug("LIFECYCLE: Docker Swarm: update_docker_service: [service_id=" + service_id + "], [service_name=" + service_name + "], "
              "[service_image=" + service_image + "], [version=" + str(version) + "]")

    # connect to docker api
    lclient = get_client_agent_docker()
    try:
        if lclient:
            LOG.debug("LIFECYCLE: Docker Swarm: update_docker_service: Updating service ...")

            # ContainerSpec:
            # (self, image, command=None, args=None, hostname=None, env=None,
            #   workdir=None, user=None, labels=None, mounts=None,
            #   stop_grace_period=None, secrets=None, tty=None, groups=None,
            #   open_stdin=None, read_only=None, stop_signal=None,
            #   healthcheck=None, hosts=None, dns_config=None, configs=None,
            #   privileges=None, isolation=None)
            container_spec = docker.types.ContainerSpec(image=service_image,
                                                        tty=True)

            # TaskTemplate:
            # (self, container_spec, resources=None, restart_policy=None,
            #   placement=None, log_driver=None, networks=None,
            #   force_update=None)
            task_tmpl = docker.types.TaskTemplate(container_spec)

            # ServiceMode:
            #   (self, mode, replicas=None)
            serv_mode = docker.types.ServiceMode(mode="replicated", replicas=replicas)

            # updates a service (DOCKER SWARM):
            # update_service(self, service, version, task_template=None, name=None,
            #            labels=None, mode=None, update_config=None,
            #            networks=None, endpoint_config=None,
            #            endpoint_spec=None, fetch_current_spec=False)
            if lclient.update_service(service_id, version, name=service_name, task_template=task_tmpl, mode=serv_mode):
                LOG.info("LIFECYCLE: Docker Swarm: update_docker_service: Service '" + service_name + "' removed")
                return True
            else:
                LOG.error("LIFECYCLE: Docker Swarm: update_docker_service: Error updating service '" + service_name + "'")
                return False
        else:
            LOG.error("LIFECYCLE: Docker Swarm: update_docker_service: Could not connect to DOCKER API")
            return None
    except:
        traceback.print_exc(file=sys.stdout)
        LOG.error("LIFECYCLE: Docker Swarm: update_docker_service: Exception")
        return None


# delete_docker_service
def delete_docker_service(service_name):
    LOG.debug("LIFECYCLE: Docker Swarm: delete_docker_service: [service_name=" + service_name + "]")

    # connect to docker api
    lclient = get_client_agent_docker()
    try:
        if lclient:
            if lclient.remove_service(service_name):
                LOG.info("LIFECYCLE: Docker Swarm: delete_docker_service: Service '" + service_name + "' removed")
                return True
            else:
                LOG.error("LIFECYCLE: Docker Swarm: delete_docker_service: Error removing service '" + service_name + "'")
                return False
        else:
            LOG.error("LIFECYCLE: Docker Swarm: delete_docker_service: Could not connect to DOCKER API")
            return None
    except:
        traceback.print_exc(file=sys.stdout)
        LOG.error("LIFECYCLE: Docker Swarm: delete_docker_service: Exception")
        return None


# get_docker_service
def get_docker_service(service_name):
    LOG.debug("LIFECYCLE: Docker Swarm: get_docker_service: [service_name=" + service_name + "]")

    # connect to docker api
    lclient = get_client_agent_docker()
    try:
        if lclient:
            res = lclient.inspect_service(service_name)
            LOG.debug("LIFECYCLE: Docker Swarm: create_docker_service: get_docker_service: " + str(res))

            if res:
                LOG.info("LIFECYCLE: Docker Swarm: get_docker_service: Service '" + service_name + "' info retrieved")
                return res
            else:
                LOG.error("LIFECYCLE: Docker Swarm: get_docker_service: Error getting service '" + service_name + "'")
                return False
        else:
            LOG.error("LIFECYCLE: Docker Swarm: get_docker_service: Could not connect to DOCKER API")
            return None
    except:
        traceback.print_exc(file=sys.stdout)
        LOG.error("LIFECYCLE: Docker Swarm: get_docker_service: Exception")
        return None


###############################################################################
# OPERATIONS:

# operation_service_agent: service operation (start, stop...)
def operation_service_agent(agent, operation):
    LOG.debug("LIFECYCLE: Docker adapter: operation_service_agent [" + operation + "]: " + str(agent))
    try:
        # connect to docker api / check existing connection
        if docker_client.get_client_agent_docker() is not None:
            if operation == OPERATION_START:
                docker_client.start_container(agent['container_id'])
                agent['status'] = STATUS_STARTED

                if config.dic['NETWORK_COMPSs'] != "not-defined":
                    docker_client.add_container_to_network(agent['container_id'])

            elif operation == OPERATION_STOP:
                l_elem = db.get_elem_from_list(agent['container_id'])
                LOG.debug("  > docker-compose? [l_elem=" + str(l_elem) + "]")

                # docker-compose
                if l_elem is not None and l_elem['type'] == "docker-compose":
                    LOG.debug("  >> Docker-compose down [" + l_elem['container_2'] + "] ...")
                    docker_client.start_container(l_elem['container_2'])
                    LOG.debug("  >> Docker-compose down: waiting 60 seconds...")
                    time.sleep(60)
                    LOG.debug("  >> Stop container 1 [" + agent['container_id'] + "] ...")
                    docker_client.stop_container(agent['container_id'])
                    LOG.debug("  >> Stop container 2 [" + l_elem['container_2'] + "] ...")
                    docker_client.stop_container(l_elem['container_2'])
                # 'normal' container
                else:
                    LOG.debug("  >> Stop container: " + agent['container_id'])
                    docker_client.stop_container(agent['container_id'])
                agent['status'] = STATUS_STOPPED

            elif operation == OPERATION_TERMINATE:
                l_elem = db.get_elem_from_list(agent['container_id'])
                LOG.debug("  > docker-compose? [l_elem=" + str(l_elem) + "]")

                # docker-compose
                if l_elem is not None and l_elem['type'] == "docker-compose":
                    LOG.debug("  >> Remove container 1 [" + agent['container_id'] + "] ...")
                    docker_client.remove_container(agent)
                    LOG.debug("  >> Remove container 2 [" + l_elem['container_2'] + "] ...")
                    docker_client.remove_container_by_id(l_elem['container_2'])
                # 'normal' container
                else:
                    LOG.debug("  >> Remove container: " + agent['container_id'])
                    docker_client.remove_container(agent)
                agent['status'] = STATUS_TERMINATED

        # if error when connecting to agent...
        else:
            LOG.error("LIFECYCLE: Docker adapter: operation_service_agent: Could not connect to DOCKER API")
            agent['status'] = STATUS_UNKNOWN
        # return status
        return agent['status']
    except:
        agent['status'] = STATUS_ERROR
        traceback.print_exc(file=sys.stdout)
        LOG.error('LIFECYCLE: Docker adapter: operation_service_agent: Exception')
        return STATUS_ERROR


# start_service_agent: Start service in agent
def start_service_agent(agent):
    return operation_service_agent(agent, OPERATION_START)


# stop_service_agent: Stop service / stop container
def stop_service_agent(agent):
    return operation_service_agent(agent, OPERATION_STOP)


# terminate_service_agent: Stop service / stop container
def terminate_service_agent(agent):
    return operation_service_agent(agent, OPERATION_TERMINATE)
