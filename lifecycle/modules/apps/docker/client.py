"""
Docker client. Used by other files: adapters from docker, swarm, compss...
This is being developed for the MF2C Project: http://www.mf2c-project.eu/

Copyright: Atos Research and Innovation, 2017.

This code is licensed under an Apache 2.0 license. Please, refer to the LICENSE.TXT file for more information

Created on 09 feb. 2018

@author: Roi Sucasas - ATOS
"""

import docker, uuid
from lifecycle.modules.apps import ports_mngr as pmngr
import config
from lifecycle.logs import LOG
from lifecycle.data import data_adapter as data_adapter


# docker socket connection
DOCKER_SOCKET = config.dic['DOCKER_SOCKET'] # Example: "unix://var/run/docker.sock"

# client
client = None


# get_client_agent_docker: Get docker api client
# connect to docker api: Examples: base_url='tcp://192.168.252.42:2375'; base_url='unix://var/run/docker.sock'
def get_client_agent_docker():
    global client
    LOG.debug("[lifecycle.modules.apps.docker.client] [get_client_agent_docker] Connecting to DOCKER API [" + DOCKER_SOCKET + "], "
              "[client=" + str(client) + "]...")
    try:
        try:
            if client is not None:
                client.version()
                LOG.debug("[lifecycle.modules.apps.docker.client] [get_client_agent_docker] Returning existing client [" + str(client) + "] ...")
                return client
        except:
            LOG.error("[lifecycle.modules.apps.docker.client] [get_client_agent_docker] docker client gave an error. Trying to reconnect to docker...")

        client = docker.APIClient(base_url=DOCKER_SOCKET)
        LOG.debug("[lifecycle.modules.apps.docker.client] [get_client_agent_docker] Connected to DOCKER in [" + DOCKER_SOCKET + "]; version: " + str(client.version()))
        return client
    except:
        LOG.exception("[lifecycle.modules.apps.docker.client] [get_client_agent_docker] Error when connecting to DOCKER API: " + DOCKER_SOCKET)
        return None


# download_docker_image: check if image is already downloaded, and if not, tries to download the image
def download_docker_image(lclient, service_image, service_image_tag=None):
    # check if image already exists in agent
    l_images = lclient.images(name=service_image)
    # if not, download image
    if not l_images or len(l_images) == 0:
        LOG.debug("[lifecycle.modules.apps.docker.client] [download_docker_image] call to 'import_image' [" + service_image + "] ...")
        if service_image_tag is not None:
            lclient.import_image(tag=service_image_tag, image=service_image) # (tag="latest", image="ubuntu")
        else:
            lclient.import_image(image=service_image)  # (image="ubuntu")


# create_docker_container
def create_docker_container(service_image, service_name, service_command, prts):
    LOG.debug("[lifecycle.modules.apps.docker.client] [create_docker_container] [service_name=" + service_name + "], "
              "[service_command=" + service_command + "], [service_image=" + service_image + "], "
              "[ports=" + str(prts) + "]")
    # connect to docker api
    lclient = get_client_agent_docker()
    try:
        if lclient:
            # check if image already exists in agent or download image
            download_docker_image(lclient, service_image)

            LOG.debug("[lifecycle.modules.apps.docker.client] [create_docker_container] Creating container ...")

            prts_list = list(prts)
            ports_dict = pmngr.create_ports_dict(prts)
            LOG.debug("[lifecycle.modules.apps.docker.client] [create_docker_container] ports_dict: " + str(ports_dict))
            LOG.debug("[lifecycle.modules.apps.docker.client] [create_docker_container] prts: " + str(prts))
            LOG.debug("[lifecycle.modules.apps.docker.client] [create_docker_container] prts_list: " + str(prts_list))

            # create a new container: 'docker run'
            container = lclient.create_container(service_image,  # command=service_command,
                                                 name=service_name,
                                                 tty=True,
                                                 ports=prts_list,
                                                 host_config=lclient.create_host_config(port_bindings=ports_dict))
            return container
        else:
            LOG.error("[lifecycle.modules.apps.docker.client] [create_docker_container] Could not connect to DOCKER API")
            return None
    except:
        LOG.exception("[lifecycle.modules.apps.docker.client] [create_docker_container] Exception")
        return None


# create_docker_compss_container
def create_docker_compss_container(service_image, ip, prts, ip_leader):
    LOG.debug("[lifecycle.modules.apps.docker.client] [create_docker_compss_container] Creating COMPSs container [service_image=" +
              service_image + "], [ports=" + str(prts) + "], [ip=" + ip + "] [ip_leader=" + ip_leader + "] ...")
    # connect to docker api
    lclient = get_client_agent_docker()
    try:
        if lclient:
            # check if image already exists in agent or download image
            download_docker_image(lclient, service_image)

            # create a new container: 'docker run'
            # check ports for COMPSs container:
            if config.dic['PORT_COMPSs'] not in prts:
                prts.insert(0, config.dic['PORT_COMPSs'])
            else:
                prts.remove(config.dic['PORT_COMPSs'])
                prts.insert(0, config.dic['PORT_COMPSs'])

            LOG.debug("[lifecycle.modules.apps.docker.client] [create_docker_compss_container] prts: " + str(prts))

            prts_list = list(prts)
            ports_dict = pmngr.create_ports_dict(prts)
            LOG.debug("[lifecycle.modules.apps.docker.client] [create_docker_compss_container] ports_dict: " + str(ports_dict))
            LOG.debug("[lifecycle.modules.apps.docker.client] [create_docker_compss_container] prts_list: " + str(prts_list))

            LOG.debug("[lifecycle.modules.apps.docker.client] [create_docker_compss_container] AGENT_HOST: " + data_adapter.get_host_ip())
            LOG.debug("[lifecycle.modules.apps.docker.client] [create_docker_compss_container] AGENT_PORT: " + str(data_adapter.db_get_compss_port(prts)))
            LOG.debug("[lifecycle.modules.apps.docker.client] [create_docker_compss_container] DATACLAY_EP: " + ip_leader + config.dic['DATACLAY_EP'])
            LOG.debug("[lifecycle.modules.apps.docker.client] [create_docker_compss_container] REPORT_ADDRESS: " + config.dic['CIMI_URL']) #"http://" +  data_adapter.get_host_ip() + "/api") #config.dic['CIMI_URL'])

            # "docker run --rm -it --env MF2C_HOST=172.17.0.3 -p46100:46100 --env DEBUG=debug --name compss3123 mf2c/compss-test:latest"
            container = lclient.create_container(service_image,
                                                 name="compss-" + str(uuid.uuid4()),
                                                 environment={"MF2C_HOST": ip,
                                                              "DEBUG": "debug",
                                                              "AGENT_HOST": data_adapter.get_host_ip(),
                                                              "AGENT_PORT": data_adapter.db_get_compss_port(prts),
                                                              "DATACLAY_EP": ip_leader + config.dic['DATACLAY_EP'],
                                                              "REPORT_ADDRESS": config.dic['CIMI_URL']}, #"http://" +  data_adapter.get_host_ip() + "/api"}, #config.dic['CIMI_URL']},
                                                 tty=True,
                                                 ports=prts_list,
                                                 networking_config=None,
                                                 host_config=lclient.create_host_config(port_bindings=ports_dict,
                                                                                        auto_remove=False))

            networks = lclient.networks(names=["mf2c_default"])
            LOG.debug("[lifecycle.modules.apps.docker.client] [create_docker_compss_container] networks: " + str(networks))
            if not networks is None and len(networks) > 0:
                LOG.debug("[lifecycle.modules.apps.docker.client] [create_docker_compss_container] networks[0]=" + str(networks[0]))
                id_network = networks[0]['id']
                LOG.debug("[lifecycle.modules.apps.docker.client] [create_docker_compss_container] Connecting to network ...")
                lclient.connect_container_to_network(container['Id'], id_network)

            else:
                LOG.debug("[lifecycle.modules.apps.docker.client] [create_docker_compss_container] networks is empty / None")

            return container
        else:
            LOG.error("[lifecycle.modules.apps.docker.client] [create_docker_compss_container] Could not connect to DOCKER API")
            return None
    except:
        LOG.exception("[lifecycle.modules.apps.docker.client] [create_docker_compss_container] Exception")
        return None


# create_docker_compose_container
def create_docker_compose_container(service_name, service_command):
    LOG.debug("[lifecycle.modules.apps.docker.client] [create_docker_compose_container] Creating docker-compose containers [service_name=" +
              service_name +"], [service_command=" + service_command + "] ...")
    try:
        # connect to docker api
        lclient = get_client_agent_docker()
        if lclient:
            # check if image already exists in agent or download image
            download_docker_image(lclient, config.dic['DOCKER_COMPOSE_IMAGE'], config.dic['DOCKER_COMPOSE_IMAGE_TAG'])

            # create a new container: 'docker run'
            container = lclient.create_container(config.dic['DOCKER_COMPOSE_IMAGE'],
                                                 command=service_command,
                                                 name=service_name,
                                                 tty=True,
                                                 volumes=[config.dic['WORKING_DIR_VOLUME'], config.dic['DOCKER_SOCKET_VOLUME']],
                                                 host_config=lclient.create_host_config(
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
            LOG.error("[lifecycle.modules.apps.docker.client] [create_docker_compose_container] Could not connect to DOCKER API")
            return None
    except:
        LOG.exception("[lifecycle.modules.apps.docker.client] [create_docker_compose_container] Exception")
        return None


# stop_container
def stop_container(id):
    try:
        lclient = get_client_agent_docker()
        lclient.stop(id)
        return True
    except:
        LOG.exception("[lifecycle.modules.apps.docker.client] [stop_container] [" + id + "]: Exception")
        return False


# start_container
def start_container(id):
    try:
        lclient = get_client_agent_docker()
        lclient.start(id)
        return True
    except:
        LOG.exception("[lifecycle.modules.apps.docker.client] [start_container] [" + id + "]: Exception")
        return False


# remove_container_by_id
def remove_container_by_id(id):
    try:
        lclient = get_client_agent_docker()
        lclient.remove_container(id, force=True)
    except:
        LOG.exception("[lifecycle.modules.apps.docker.client] [remove_container_by_id] [" + id + "]: Exception")
        return False


# remove_container
def remove_container(agent):
    try:
        lclient = get_client_agent_docker()
        lclient.remove_container(agent['container_id'], force=True)

        for p in agent['ports']:
            pmngr.release_port(p)
    except:
        LOG.exception("[lifecycle.modules.apps.docker.client] [remove_container] [" + str(agent) + "]: Exception")
        return False


# start_container
def add_container_to_network(id):
    try:
        LOG.debug("[lifecycle.modules.apps.docker.client] [add_container_to_network] "
                  "[NETWORK_COMPSs=" + config.dic['NETWORK_COMPSs'] + "], [id=" + id + "]")
        lclient = get_client_agent_docker()
        LOG.debug("[lifecycle.modules.apps.docker.client] [add_container_to_network] resp: " +
                  str(lclient.connect_container_to_network(id, config.dic['NETWORK_COMPSs'])))
    except:
        LOG.exception("[lifecycle.modules.apps.docker.client] [add_container_to_network] [" + id + "]: Exception")
        return False
