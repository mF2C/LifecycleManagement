"""
Initial configuration
This is being developed for the MF2C Project: http://www.mf2c-project.eu/

Copyright: Atos Research and Innovation, 2017.

This code is licensed under an Apache 2.0 license. Please, refer to the LICENSE.TXT file for more information

Created on 02 may 2018

@author: Roi Sucasas - ATOS
"""


import lifecycle.utils.common as common
from lifecycle.utils.logs import LOG
from lifecycle import config


'''
ENV VARIABLES (mF2C):
    CIMI_USER=
    CIMI_PASSWORD=
    CIMI_API_KEY=
    CIMI_API_SECRET=
    CIMI_SSL_INSECURE=
    
    CIMI URL = https://proxy
    
ENV VARIABLES (lifecycle):
    HOST_IP
    STANDALONE_MODE
    CIMI_COOKIES_PATH
    
    URL_PM_SLA_MANAGER
    URL_AC_QoS_PROVIDING
    URL_AC_USER_MANAGEMENT
    
    WORKING_DIR_VOLUME = "/home/atos/mF2C/compose_examples"
    DOCKER_COMPOSE_IMAGE = "docker/compose:1.21.0"
    DOCKER_SOCKET_VOLUME = "/var/run/docker.sock"
'''


def init():
    try:
        # CONFIGURATION / ENVIRONMENT VALUES
        LOG.info('Reading values from ENVIRONMENT...')
        # STANDALONE_MODE
        common.set_value_env('STANDALONE_MODE')
        # docker
        common.set_value_env('WORKING_DIR_VOLUME')
        common.set_value_env('DOCKER_COMPOSE_IMAGE')
        common.set_value_env('DOCKER_SOCKET_VOLUME')
        # HOST IP from environment values:
        common.set_value_env('HOST_IP')
        # CIMI environment values:
        common.set_value_env('CIMI_URL')
        common.set_value_env('CIMI_COOKIES_PATH')
        common.set_value_env('CIMI_USER')
        common.set_value_env('CIMI_PASSWORD')
        # mF2C components: env variables
        common.set_value_env('URL_PM_SLA_MANAGER')
        common.set_value_env('URL_AC_QoS_PROVIDING')
        common.set_value_env('URL_AC_USER_MANAGEMENT')

        LOG.info('Checking configuration...')
        LOG.info('[SERVER_PORT=' + str(config.dic['SERVER_PORT']) + ']')
        LOG.info('[API_DOC_URL=' + config.dic['API_DOC_URL'] + ']')
        LOG.info('[CERT_CRT=' + config.dic['CERT_CRT'] + ']')
        LOG.info('[CERT_KEY=' + config.dic['CERT_KEY'] + ']')
        LOG.info('[DEBUG=' + str(config.dic['DEBUG']) + ']')
        LOG.info('[STANDALONE_MODE=' + str(config.dic['STANDALONE_MODE']) + ']')
        LOG.info('[WORKING_DIR_VOLUME=' + config.dic['WORKING_DIR_VOLUME'] + ']')
        LOG.info('[DOCKER_COMPOSE_IMAGE=' + config.dic['DOCKER_COMPOSE_IMAGE'] + ']')
        LOG.info('[DOCKER_SOCKET_VOLUME=' + config.dic['DOCKER_SOCKET_VOLUME'] + ']')
        LOG.info('[HOST_IP=' + config.dic['HOST_IP'] + ']')
        LOG.info('[CIMI_URL=' + config.dic['CIMI_URL'] + ']')
        LOG.info('[CIMI_COOKIES_PATH=' + config.dic['CIMI_COOKIES_PATH'] + ']')
        LOG.info('[CIMI_USER=' + config.dic['CIMI_USER'] + ']')
        LOG.info('[CIMI_PASSWORD=' + config.dic['CIMI_PASSWORD'] + ']')
        LOG.info('[URL_PM_SLA_MANAGER=' + config.dic['URL_PM_SLA_MANAGER'] + ']')
        LOG.info('[URL_AC_QoS_PROVIDING=' + config.dic['URL_AC_QoS_PROVIDING'] + ']')
        LOG.info('[URL_AC_USER_MANAGEMENT=' + config.dic['URL_AC_USER_MANAGEMENT'] + ']')

        if config.dic['STANDALONE_MODE'] == 'True' or config.dic['STANDALONE_MODE']:
            LOG.warning("STANDALONE_MODE enabled")
        else:
            LOG.info("STANDALONE_MODE not enabled")
    except:
        LOG.error('Lifecycle-Management: init_config: Exception: Error while initializing application')