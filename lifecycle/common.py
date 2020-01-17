"""
Common functions
This is being developed for the MF2C Project: http://www.mf2c-project.eu/

Copyright: Roi Sucasas Font, Atos Research and Innovation, 2017.

This code is licensed under an Apache 2.0 license. Please, refer to the LICENSE.TXT file for more information

Created on 09 feb. 2018

@author: Roi Sucasas - ATOS
"""


import os
import config
from flask import Response, json
from lifecycle.logs import LOG


###############################################################################
# GLOBAL VARS:

# LOGS
TRACE = 5

# Service Type
SERVICE_DOCKER = "docker"
SERVICE_DOCKER_COMPOSE = "docker-compose" #"docker-compose"
SERVICE_COMPSS = "compss"
SERVICE_DOCKER_SWARM =  "docker-swarm" #"swarm" #""docker-swarm"
SERVICE_KUBERNETES = "K8s"
SERVICE_DOCKER_COMPOSE_SWARM = "docker-compose-swarm" #"docker-compose-swarm

# Operations:
OPERATION_START = "start"
OPERATION_STOP = "stop"
OPERATION_RESTART = "restart"
OPERATION_TERMINATE = "terminate"
OPERATION_START_JOB = "start-job"
OPERATION_STOP_TERMINATE = "stop-and-terminate"

# service instance / agent status
STATUS_ERROR = "error"
STATUS_ERROR_STARTING = "error-starting"
STATUS_ERROR_STOPPING = "error-stopping"
STATUS_UNKNOWN = "??"
STATUS_NOT_DEPLOYED = "not-deployed"
STATUS_WAITING = "waiting"
STATUS_STARTED = "started"
STATUS_STOPPED = "stopped"
STATUS_TERMINATED = "terminated"
STATUS_CREATED_NOT_INITIALIZED = "created-not-initialized"
STATUS_DEPLOYING = "deploying"
STATUS_STARTING = "starting"
STATUS_STOPPING = "stopping"
STATUS_TERMINATING = "terminating"


###############################################################################
# STAND_ALONE_MODE:

# is_standalone_mode
def is_standalone_mode():
    if config.dic['LM_MODE'] is not None and config.dic['LM_MODE'] == 'STANDALONE':
        return True
    return False


###############################################################################
# RESPONSEs:

# CLASS ResponseCIMI
class ResponseCIMI():
    msj = ""


# Generate response 200
def gen_response_ok(message, key, value, key2=None, value2=None):
    dict = {'error': False, 'message': message}
    dict[key] = value
    if not (key2 is None) and not (value2 is None):
        dict[key2] = value2
    LOG.log(TRACE, "[lifecycle.common.common] [gen_response_ok] Generate response OK; dict=" + str(dict))
    return dict


# Generate response ERROR
def gen_response(status, message, key, value, key2=None, value2=None):
    dict = {'error': True, 'message': message}
    dict[key] = value
    if not (key2 is None) and not (value2 is None):
        dict[key2] = value2
    LOG.log(TRACE, '[lifecycle.common.common] [gen_response] Generate response ' + str(status) + "; dict=" + str(dict))
    return Response(json.dumps(dict), status=status, content_type='application/json')


# Generate response 200
def gen_response_ko(message, key, value, key2=None, value2=None):
    dict = {'error': True, 'message': message}
    dict[key] = value
    if not (key2 is None) and not (value2 is None):
        dict[key2] = value2
    LOG.log(TRACE, "[lifecycle.common.common] [gen_response] Generate response KO; dict=" + str(dict))
    return dict


###############################################################################
# IPs:
# check_ip: Check if IP is alive
def check_ip(ip_adress):
    try:
        # '-c 1' ==> linux
        # '-n 1' ==> windows
        response = os.system("ping -c 1 " + ip_adress)
        if response == 0:
            return True
    except:
        LOG.error('[lifecycle.common.common] [check_ip] Exception')
    return True


###############################################################################
# ENV:
# set_value_env: set value (in config dict) from environment
def set_value_env(env_name):
    res = os.getenv(env_name, default='not-defined')
    #LOG.debug('LIFECYCLE: [' + env_name + '=' + res + ']')
    if res != 'not-defined':
        config.dic[env_name] = res
