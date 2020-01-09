"""
Docker-Compose Swarm adapter
This is being developed for the MF2C Project: http://www.mf2c-project.eu/

Copyright: Atos Research and Innovation, 2017.

This code is licensed under an Apache 2.0 license. Please, refer to the LICENSE.TXT file for more information

Created on 12 dec. 2019

@author: Roi Sucasas - ATOS
"""

import os
import config
import shutil
import urllib.request as urequest
from lifecycle.logs import LOG
from lifecycle import common as common
from lifecycle.data.common import db as db
from lifecycle.common import STATUS_ERROR, STATUS_WAITING, SERVICE_DOCKER_COMPOSE_SWARM, STATUS_STOPPING


'''
These functions require the following in the docker-compose or docker files:
    -v /usr/bin/docker:/usr/bin/docker
'''

# deploy_service_agent:
#   Command:  docker stack deploy -c <DOCKER_COMPOSE_FILE_PATH> <STACK_NAME>
#
#               -v /home/atos/mF2C/compose_examples:/home/atos/mF2C/compose_examples
def deploy_service_agent(service, agent):
    LOG.debug("[lifecycle.modules.apps.swarm.compose.adapter] [deploy_service_agent] " + str(service) + ", " + str(agent))
    try:
        # 1. Download docker-compose.yml file
        location = service['exec']
        LOG.debug("[lifecycle.modules.apps.swarm.compose.adapter] [deploy_service_agent] Getting docker-compose.yml from " + location + " ...")

        # remove previous files
        LOG.debug("[lifecycle.modules.apps.swarm.compose.adapter] [deploy_service_agent] Cleaning folder [" + config.dic['WORKING_DIR_VOLUME'] + "] ...")
        try:
            LOG.debug("[lifecycle.modules.apps.swarm.compose.adapter] [deploy_service_agent] Checking files from [" + config.dic['WORKING_DIR_VOLUME'] + "] ...")
            if os.path.exists(config.dic['WORKING_DIR_VOLUME'] + "/docker-compose.yml"):
                os.remove(config.dic['WORKING_DIR_VOLUME'] + "/docker-compose.yml")
                LOG.debug("[lifecycle.modules.apps.swarm.compose.adapter] [deploy_service_agent] 'docker-compose.yml' file removed!")
            else:
                LOG.debug("[lifecycle.modules.apps.swarm.compose.adapter] [deploy_service_agent] Folder has no 'docker-compose.yml' file")
        except:
            LOG.warning("[lifecycle.modules.apps.docker.adapter] [__deploy_docker_compose] Error when removing file: " + config.dic['WORKING_DIR_VOLUME'] + "/docker-compose.yml")

        # copy / download docker-compose.yml
        LOG.debug("[lifecycle.modules.apps.swarm.compose.adapter] [deploy_service_agent] Copying [deployment] 'docker-compose.yml' to [" + config.dic['WORKING_DIR_VOLUME'] + "] ...")
        try:
            res, _ = urequest.urlretrieve(location, config.dic['WORKING_DIR_VOLUME'] + "/docker-compose.yml")
            LOG.debug("[lifecycle.modules.apps.swarm.compose.adapter] [deploy_service_agent] res: " + str(res))
        except:
            LOG.exception("[lifecycle.modules.apps.swarm.compose.adapter] [deploy_service_agent] Error when copying file to: " + config.dic['WORKING_DIR_VOLUME'] + "/docker-compose.yml")
            return common.gen_response(500,
                                       "Exception: deploy_docker_compose(): Error when copying file to WORKING_DIR_VOLUME",
                                       "agent", str(agent),
                                       "WORKING_DIR_VOLUME", config.dic['WORKING_DIR_VOLUME'])

        # 2. Deploy container: docker stack deploy -c <DOCKER_COMPOSE_FILE_PATH> <STACK_NAME>
        stack_id = service['name'].strip().lower() # + str(uuid.uuid4())

        LOG.debug("[lifecycle.modules.apps.swarm.compose.adapter] [deploy_service_agent] 'cd " + config.dic['WORKING_DIR_VOLUME'] + "'")
        resOs = os.system("cd " + config.dic['WORKING_DIR_VOLUME'])
        LOG.debug("[lifecycle.modules.apps.swarm.compose.adapter] [deploy_service_agent] resOs: " + str(resOs))

        LOG.debug("[lifecycle.modules.apps.swarm.compose.adapter] [deploy_service_agent] 'docker stack deploy -c " + config.dic['WORKING_DIR_VOLUME'] + "/docker-compose.yml  " + stack_id + "'")
        resOs = os.system("docker stack deploy -c " + config.dic['WORKING_DIR_VOLUME'] + "/docker-compose.yml " + stack_id)
        LOG.debug("[lifecycle.modules.apps.swarm.compose.adapter] [deploy_service_agent] resOs: " + str(resOs))

        # 3.
        if service['name'].strip().lower() is not None:
            db.SERVICE_INSTANCES_LIST.append({
                "type": SERVICE_DOCKER_COMPOSE_SWARM,
                "container_main": stack_id,
                "container_2": "-"
            })
            LOG.debug("[lifecycle.modules.apps.swarm.compose.adapter] [deploy_service_agent] container: " + stack_id)

            # update agent properties
            agent['container_id'] = stack_id
            agent['agent_param'] = "-"
            agent['status'] = STATUS_WAITING
            return common.gen_response_ok('Deploy docker-compose-swarm service in agent', 'agent', str(agent), 'service', str(service))
        else:
            LOG.error("[lifecycle.modules.apps.swarm.compose.adapter] [deploy_service_agent] Could not connect to DOCKER API")
            agent['status'] = STATUS_ERROR
            return common.gen_response(500, 'Error when connecting to DOCKER API', 'agent', str(agent), 'service',
                                       str(service))
    except:
        LOG.exception('[lifecycle.modules.apps.swarm.compose.adapter] [deploy_service_agent] Exception')
        return common.gen_response(500, 'Exception: deploy_docker_compose()', 'agent', str(agent), 'service', str(service))


# stop_service_agent:
#   Command:  docker stack deploy -c <DOCKER_COMPOSE_FILE_PATH> <STACK_NAME>
#
#               -v /home/atos/mF2C/compose_examples:/home/atos/mF2C/compose_examples
def stop_service_agent(service, agent):
    LOG.debug("[lifecycle.modules.apps.swarm.compose.adapter] [stop_service_agent] " + str(service) + ", " + str(agent))
    try:
        # 1. Remove stack: docker stack rm <STACK_NAME>
        stack_id = service['name'].strip().lower()  # + str(uuid.uuid4())

        LOG.debug("[lifecycle.modules.apps.swarm.compose.adapter] [stop_service_agent] 'cd " + config.dic['WORKING_DIR_VOLUME'] + "'")
        resOs = os.system("cd " + config.dic['WORKING_DIR_VOLUME'])
        LOG.debug("[lifecycle.modules.apps.swarm.compose.adapter] [stop_service_agent] resOs: " + str(resOs))

        LOG.debug("[lifecycle.modules.apps.swarm.compose.adapter] [stop_service_agent] 'docker stack rm " + stack_id + "'")
        resOs = os.system("docker stack rm " + stack_id)
        LOG.debug("[lifecycle.modules.apps.swarm.compose.adapter] [stop_service_agent] resOs: " + str(resOs))

        # 3.
        if service['name'].strip().lower() is not None:
            db.SERVICE_INSTANCES_LIST.append({
                "type": SERVICE_DOCKER_COMPOSE_SWARM,
                "container_main": stack_id,
                "container_2": "-"
            })
            LOG.debug("[lifecycle.modules.apps.swarm.compose.adapter] [stop_service_agent] container: " + stack_id)

            # update agent properties
            agent['container_id'] = stack_id
            agent['agent_param'] = "-"
            agent['status'] = STATUS_STOPPING
            return common.gen_response_ok('Deploy docker-compose-swarm service in agent', 'agent', str(agent),
                                          'service', str(service))
        else:
            LOG.error("[lifecycle.modules.apps.swarm.compose.adapter] [stop_service_agent] Could not connect to DOCKER API")
            agent['status'] = STATUS_ERROR
            return common.gen_response(500, 'Error when connecting to DOCKER API', 'agent', str(agent), 'service',
                                       str(service))

    except:
        LOG.exception('[lifecycle.modules.apps.swarm.compose.adapter] [stop_service_agent] Exception')
        return common.gen_response(500, 'Exception: deploy_docker_compose()', 'agent', str(agent), 'service',
                                   str(service))


# terminate_service_agent: Terminate service / stop container
def terminate_service_agent(service, agent):
    LOG.debug("[lifecycle.modules.apps.swarm.compose.adapter] [terminate_service_agent] " + str(service) + ", " + str(agent))