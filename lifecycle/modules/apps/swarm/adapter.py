"""
Docker Swarm adapter
This is being developed for the MF2C Project: http://www.mf2c-project.eu/

Copyright: Atos Research and Innovation, 2017.

This code is licensed under an Apache 2.0 license. Please, refer to the LICENSE.TXT file for more information

Created on 18 oct. 2018

@author: Roi Sucasas - ATOS
"""

import docker, uuid
import config
from lifecycle import common as common
from lifecycle.modules.apps import ports_mngr as pmngr
from flask import json
from lifecycle.modules.apps.docker import client as docker_client
from lifecycle.logs import LOG
from lifecycle.common import OPERATION_START, OPERATION_STOP, OPERATION_TERMINATE, \
    STATUS_ERROR, STATUS_WAITING, STATUS_TERMINATED, STATUS_UNKNOWN


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
        LOG.debug("[lifecycle.modules.apps.swarm.adapter] [create_ports_dict] Configuring ports [" + str(ports) + "]...")
        l_ports = []
        for p in ports:
            LOG.debug("[lifecycle.modules.apps.swarm.adapter] [create_ports_dict] port [" + str(p) + "]...")
            if pmngr.is_port_free(p):
                l_ports.append({'Protocol': 'tcp', 'PublishedPort': p, 'TargetPort': p})
                pmngr.take_port(p, p)
                LOG.debug("[lifecycle.modules.apps.swarm.adapter] [create_ports_dict] port free")
            else:
                np = pmngr.assign_new_port()
                # original port : new port (exposed to host)
                l_ports.append({'Protocol': 'tcp', 'PublishedPort': np, 'TargetPort': p}) # dict_ports.update({p: np})
                pmngr.take_port(np, p)
                replace_in_list(ports, p, np)
                LOG.debug("[lifecycle.modules.apps.swarm.adapter] [create_ports_dict] port not free: redirected to " + str(np))

        return l_ports
    except:
        LOG.exception("[lifecycle.modules.apps.swarm.adapter] [create_ports_dict] Error during the ports dict creation: " + str(ports))
        return {ports[0]:ports[0]}


# get_client_agent_docker: Get docker api client
# connect to docker api: Examples: base_url='tcp://192.168.252.42:2375'; base_url='unix://var/run/docker.sock'
def get_client_agent_docker():
    global client
    LOG.debug("[lifecycle.modules.apps.swarm.adapter] [get_client_agent_docker] Connecting to DOCKER API [" + DOCKER_SOCKET + "], "
              "[SWARM MASTER? " + str(False) + "] [client=" + str(client) + "],...")
    try:
        try:
            if client is not None:
                client.version()
                LOG.debug("[lifecycle.modules.apps.swarm.adapter] [get_client_agent_docker] Returning existing client [" + json.dumps(client) + "] ...")
                return client
        except:
            LOG.exception("[lifecycle.modules.apps.swarm.adapter] [get_client_agent_docker] docker client gave an error. Trying to reconnect to docker...")

        client = docker.APIClient(base_url=DOCKER_SOCKET)
        LOG.debug("[lifecycle.modules.apps.swarm.adapter] [get_client_agent_docker] Connected to DOCKER in [" + DOCKER_SOCKET + "]; version: " + json.dumps(client.version()))
        return client
    except:
        LOG.exception("[lifecycle.modules.apps.swarm.adapter] [get_client_agent_docker] Error when connecting to DOCKER API: " + DOCKER_SOCKET)
        return None


# create_docker_service
def create_docker_service(service_image, service_name, service_command, prts, replicas, service, agent):
    LOG.debug("[lifecycle.modules.apps.swarm.adapter] [create_docker_service] [service_name=" + service_name + "], "
              "[service_command=" + service_command + "], [service_image=" + service_image + "], [ports=" + str(prts) + "]")

    # connect to docker api
    lclient = get_client_agent_docker()
    try:
        if lclient:
            # check if image already exists in agent
            l_images = lclient.images(name=service_image)
            # if not, download image
            if not l_images or len(l_images) == 0:
                LOG.debug("[lifecycle.modules.apps.swarm.adapter] [create_docker_service] call to 'import_image' [" + service_image + "] ...")
                lclient.import_image(image=service_image)  # (tag="latest", image="ubuntu") # (tag="latest", image="ubuntu")

            LOG.debug("[lifecycle.modules.apps.swarm.adapter] [create_docker_service] Creating service ...")

            prts_list = list(prts)
            ports_list = create_ports_dict(prts)
            LOG.debug("[lifecycle.modules.apps.swarm.adapter] [create_docker_service] ports_list: " + str(ports_list))
            LOG.debug("[lifecycle.modules.apps.swarm.adapter] [create_docker_service] prts: " + str(prts))
            LOG.debug("[lifecycle.modules.apps.swarm.adapter] [create_docker_service] prts_list: " + str(prts_list))

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

            LOG.debug("[lifecycle.modules.apps.swarm.adapter] [create_docker_service] container_spec: " + str(container_spec))

            # TaskTemplate:
            # (self, container_spec, resources=None, restart_policy=None,
            #   placement=None, log_driver=None, networks=None,
            #   force_update=None)
            task_tmpl = docker.types.TaskTemplate(container_spec, restart_policy=None)

            LOG.debug("[lifecycle.modules.apps.swarm.adapter] [create_docker_service] task_tmpl: " + str(task_tmpl))

            # ServiceMode:
            #   (self, mode, replicas=None)
            serv_mode = docker.types.ServiceMode(mode="replicated", replicas=replicas)

            LOG.debug("[lifecycle.modules.apps.swarm.adapter] [create_docker_service] serv_mode: " + str(serv_mode))

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

            LOG.debug("[lifecycle.modules.apps.swarm.adapter] [create_docker_service] res: " + str(res))

            # update agent properties
            # service ID is stored in 'container_id' field
            agent['container_id'] = res['ID'] #container1['Id']
            agent['status'] = STATUS_WAITING
            return common.gen_response_ok('Deploy service in agent (Docker Swarm)', 'agent', str(agent), 'service', str(service))
        else:
            LOG.error("[lifecycle.modules.apps.swarm.adapter] [create_docker_service] Could not connect to DOCKER API")
            agent['status'] = STATUS_ERROR
            return common.gen_response(500, 'Error when connecting to DOCKER API', 'agent', str(agent), 'service', str(service))
    except:
        LOG.exception('[lifecycle.modules.apps.swarm.adapter] [create_docker_service] Exception')
        return common.gen_response(500, 'Exception: deploy_docker_image()', 'agent', str(agent), 'service', str(service))


# TODO
def is_swarm_node():
    try:
        # connect to docker api
        lclient = get_client_agent_docker()
        if lclient:
            l = lclient.services()
            return common.gen_response_ok('docker swarm supported', 'is_swarm_node', True)
        return common.gen_response_ok('docker client error', 'is_swarm_node', False)
    except:
        return common.gen_response_ok('docker swarm not supported', 'is_swarm_node', False)


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

    replicas = 1
    try:
        if not service is None and not service['num_agents'] is None:
            replicas = service['num_agents']
    except:
        LOG.exception('[lifecycle.modules.apps.swarm.adapter] [deploy_service_agent] Exception: replicas set to 1')
        replicas = 1

    create_docker_service(service_image, service_name, service_command, ports, replicas, service, agent)


# update_docker_service
def update_docker_service(service_id, service_image, service_name, replicas, version):
    LOG.debug("[lifecycle.modules.apps.swarm.adapter] [update_docker_service] [service_id=" + service_id + "], [service_name=" + service_name + "], "
              "[service_image=" + service_image + "], [version=" + str(version) + "]")

    # connect to docker api
    lclient = get_client_agent_docker()
    try:
        if lclient:
            LOG.debug("[lifecycle.modules.apps.swarm.adapter] [update_docker_service] Updating service ...")

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
                LOG.info("[lifecycle.modules.apps.swarm.adapter] [update_docker_service] Service '" + service_name + "' removed")
                return True
            else:
                LOG.error("[lifecycle.modules.apps.swarm.adapter] [update_docker_service] Error updating service '" + service_name + "'")
                return False
        else:
            LOG.error("[lifecycle.modules.apps.swarm.adapter] [update_docker_service] Could not connect to DOCKER API")
            return None
    except:
        LOG.exception("[lifecycle.modules.apps.swarm.adapter] [update_docker_service] Exception. Returning None ...")
        return None


# delete_docker_service
def delete_docker_service(service_id):
    LOG.debug("[lifecycle.modules.apps.swarm.adapter] [delete_docker_service] [service_name=" + service_id + "]")

    # connect to docker api
    lclient = get_client_agent_docker()
    try:
        if lclient:
            if lclient.remove_service(service_id):
                LOG.info("[lifecycle.modules.apps.swarm.adapter] [delete_docker_service] Service '" + service_id + "' removed")
                return True
            else:
                LOG.error("[lifecycle.modules.apps.swarm.adapter] [delete_docker_service] Error removing service '" + service_id + "'")
                return False
        else:
            LOG.error("[lifecycle.modules.apps.swarm.adapter] [delete_docker_service] Could not connect to DOCKER API")
            return None
    except:
        LOG.exception("[lifecycle.modules.apps.swarm.adapter] [delete_docker_service] Exception")
        return None


###############################################################################
# OPERATIONS:

# operation_service_agent: service operation (start, stop...)
def operation_service_agent(agent, operation):
    LOG.debug("LIFECYCLE: Docker Swarm: operation_service_agent [" + operation + "]: " + str(agent))
    try:
        # connect to docker api / check existing connection
        if docker_client.get_client_agent_docker() is not None:
            if operation == OPERATION_STOP or operation == OPERATION_TERMINATE:
                # service ID is stored in 'container_id' field
                delete_docker_service(agent['container_id'])
                agent['status'] = STATUS_TERMINATED
            else:
                LOG.warning("[lifecycle.modules.apps.swarm.adapter] [operation_service_agent] [" + operation + "]: " + str(agent) + ": operation not supported")
        # if error when connecting to agent...
        else:
            LOG.error("[lifecycle.modules.apps.swarm.adapter] [operation_service_agent] Could not connect to DOCKER API")
            agent['status'] = STATUS_UNKNOWN
        # return status
        return agent['status']
    except:
        agent['status'] = STATUS_ERROR
        LOG.exception('[lifecycle.modules.apps.swarm.adapter] [operation_service_agent] Exception. Returning STATUS_ERROR ...')
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
