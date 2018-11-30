"""
Initial configuration
This is being developed for the MF2C Project: http://www.mf2c-project.eu/

Copyright: Atos Research and Innovation, 2017.

This code is licensed under an Apache 2.0 license. Please, refer to the LICENSE.TXT file for more information

Created on 02 may 2018

@author: Roi Sucasas - ATOS
"""


import config
import common.common as common
from common.logs import LOG


'''
ENV VARIABLES (mF2C):
    CIMI_USER=
    CIMI_API_KEY=
    CIMI_API_SECRET=
    CIMI_SSL_INSECURE=
    
    CIMI URL = https://proxy
    
ENV VARIABLES (lifecycle):
    HOST_IP
    STANDALONE_MODE
    
    URL_PM_SLA_MANAGER
    URL_AC_SERVICE_MNGMT
    URL_AC_USER_MANAGEMENT
    URL_PM_RECOM_LANDSCAPER
    
    WORKING_DIR_VOLUME = "/home/atos/mF2C/compose_examples"
    DOCKER_COMPOSE_IMAGE = "docker/compose:1.21.0"
    DOCKER_SOCKET_VOLUME = "/var/run/docker.sock"
'''


def init():
    try:
        # CONFIGURATION / ENVIRONMENT VALUES
        LOG.info('> LIFECYCLE: Reading values from ENVIRONMENT...')
        # STANDALONE_MODE
        common.set_value_env('STANDALONE_MODE')
        # docker
        common.set_value_env('WORKING_DIR_VOLUME')
        common.set_value_env('DOCKER_COMPOSE_IMAGE')
        common.set_value_env('DOCKER_SOCKET_VOLUME')
        common.set_value_env('DB_DOCKER_PORTS')
        # HOST IP from environment values:
        common.set_value_env('HOST_IP')
        # K8S_MASTER
        common.set_value_env('K8S_MASTER')
        # DOCKER_SOCKET
        common.set_value_env('DOCKER_SOCKET')
        # DOCKER_SWARM
        common.set_value_env('DOCKER_SWARM')
        # CIMI environment values:
        common.set_value_env('CIMI_USER')
        # mF2C components: env variables
        common.set_value_env('TIMEOUT_ANALYTICSENGINE')
        common.set_value_env('PORT_COMPSs')
        common.set_value_env('NETWORK_COMPSs')
        common.set_value_env('DATACLAY_EP')
        common.set_value_env('URL_PM_SLA_MANAGER')
        common.set_value_env('URL_AC_SERVICE_MNGMT')
        common.set_value_env('URL_AC_USER_MANAGEMENT')
        common.set_value_env('URL_PM_RECOM_LANDSCAPER')
        # CIMI URL
        common.set_value_env('CIMI_URL')
        LOG.debug('LIFECYCLE: [CIMI_URL=' + config.dic['CIMI_URL'] + ']')
        if "/api" not in config.dic['CIMI_URL'] and not config.dic['CIMI_URL'].endswith("/api"):
            LOG.debug("LIFECYCLE: Adding '/api' to CIMI_URL ...")
            if config.dic['CIMI_URL'].endswith("/"):
                config.dic['CIMI_URL'] = config.dic['CIMI_URL'] + "api"
            else:
                config.dic['CIMI_URL'] = config.dic['CIMI_URL'] + "/api"
            LOG.debug('LIFECYCLE: [CIMI_URL=' + config.dic['CIMI_URL'] + ']')
        else:
            LOG.debug("LIFECYCLE: CIMI_URL ... " + config.dic['CIMI_URL'])

        LOG.info('> LIFECYCLE: Checking configuration...')
        LOG.info('LIFECYCLE: [SERVER_PORT=' + str(config.dic['SERVER_PORT']) + ']')
        LOG.info('LIFECYCLE: [DOCKER_SOCKET=' + config.dic['DOCKER_SOCKET'] + ']')
        LOG.info('LIFECYCLE: [DOCKER_SWARM_=' + str(config.dic['DOCKER_SWARM']) + ']')
        LOG.info('LIFECYCLE: [K8S_MASTER=' + str(config.dic['K8S_MASTER']) + ']')
        LOG.info('LIFECYCLE: [API_DOC_URL=' + config.dic['API_DOC_URL'] + ']')
        LOG.info('LIFECYCLE: [CERT_CRT=' + config.dic['CERT_CRT'] + ']')
        LOG.info('LIFECYCLE: [CERT_KEY=' + config.dic['CERT_KEY'] + ']')
        LOG.info('LIFECYCLE: [STANDALONE_MODE=' + str(config.dic['STANDALONE_MODE']) + ']')
        LOG.info('LIFECYCLE: [VERIFY_SSL=' + str(config.dic['VERIFY_SSL']) + ']')
        LOG.info('LIFECYCLE: [CIMI_URL=' + config.dic['CIMI_URL'] + ']')
        LOG.info('LIFECYCLE: [CIMI_USER=' + config.dic['CIMI_USER'] + ']')
        LOG.info('LIFECYCLE: [WORKING_DIR_VOLUME=' + config.dic['WORKING_DIR_VOLUME'] + ']')
        LOG.info('LIFECYCLE: [DOCKER_COMPOSE_IMAGE=' + config.dic['DOCKER_COMPOSE_IMAGE'] + ']')
        LOG.info('LIFECYCLE: [DOCKER_COMPOSE_IMAGE_TAG=' + config.dic['DOCKER_COMPOSE_IMAGE_TAG'] + ']')
        LOG.info('LIFECYCLE: [DOCKER_SOCKET_VOLUME=' + config.dic['DOCKER_SOCKET_VOLUME'] + ']')
        LOG.info('LIFECYCLE: [DB_DOCKER_PORTS=' + config.dic['DB_DOCKER_PORTS'] + ']')
        LOG.info('LIFECYCLE: [URL_PM_SLA_MANAGER=' + config.dic['URL_PM_SLA_MANAGER'] + ']')
        LOG.info('LIFECYCLE: [URL_AC_SERVICE_MNGMT=' + config.dic['URL_AC_SERVICE_MNGMT'] + ']')
        LOG.info('LIFECYCLE: [URL_AC_USER_MANAGEMENT=' + config.dic['URL_AC_USER_MANAGEMENT'] + ']')
        LOG.info('LIFECYCLE: [URL_PM_RECOM_LANDSCAPER=' + config.dic['URL_PM_RECOM_LANDSCAPER'] + ']')
        LOG.info('LIFECYCLE: [TIMEOUT_ANALYTICSENGINE=' + str(config.dic['TIMEOUT_ANALYTICSENGINE']) + ']')
        LOG.info('LIFECYCLE: [PORT_COMPSs=' + str(config.dic['PORT_COMPSs']) + ']')
        LOG.info('LIFECYCLE: [NETWORK_COMPSs=' + config.dic['NETWORK_COMPSs'] + ']')
        LOG.info('LIFECYCLE: [DATACLAY_EP=' + config.dic['DATACLAY_EP'] + ']')

        if config.dic['STANDALONE_MODE'] == 'True' or config.dic['STANDALONE_MODE'] is None:
            LOG.warning("LIFECYCLE: STANDALONE_MODE enabled")
        else:
            LOG.info("LIFECYCLE: STANDALONE_MODE not enabled")
    except:
        LOG.error('LIFECYCLE: init_config: Exception: Error while initializing application')