"""
Common functions
This is being developed for the MF2C Project: http://www.mf2c-project.eu/

Copyright: Roi Sucasas Font, Atos Research and Innovation, 2017.

This code is licensed under an Apache 2.0 license. Please, refer to the LICENSE.TXT file for more information

Created on 09 feb. 2018

@author: Roi Sucasas - ATOS
"""


import socket, os
import config
from flask import Response, json
from common.logs import LOG


###############################################################################
# GLOBAL VARS:

# Service Type
SERVICE_DOCKER = "docker"
SERVICE_DOCKER_COMPOSE = "docker-compose"
SERVICE_COMPSS = "compss"
SERVICE_DOCKER_SWARM = "docker-swarm"
SERVICE_KUBERNETES = "K8s"

# Operations:
OPERATION_START = "start"
OPERATION_STOP = "stop"
OPERATION_RESTART = "restart"
OPERATION_TERMINATE = "terminate"
OPERATION_START_JOB = "start-job"

# service instance / agent status
STATUS_ERROR = "error"
STATUS_UNKNOWN = "??"
STATUS_NOT_DEPLOYED = "not-deployed"
STATUS_WAITING = "waiting"
STATUS_STARTED = "started"
STATUS_STOPPED = "stopped"
STATUS_TERMINATED = "terminated"
STATUS_CREATED_NOT_INITIALIZED = "created-not-initialized"


###############################################################################
# STAND_ALONE_MODE:

# is_standalone_mode
def is_standalone_mode():
    if config.dic['STANDALONE_MODE'] == 'True' or config.dic['STANDALONE_MODE'] is None:
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
    LOG.debug("Generate response OK; dict=" + str(dict))
    return dict


# Generate response ERROR
def gen_response(status, message, key, value, key2=None, value2=None):
    dict = {'error': True, 'message': message}
    dict[key] = value
    if not (key2 is None) and not (value2 is None):
        dict[key2] = value2
    LOG.debug('Generate response ' + str(status) + "; dict=" + str(dict))
    return Response(json.dumps(dict), status=status, content_type='application/json')


'''
# Generate response 200
def gen_response_ok(message, key, value, key2=None, value2=None):
    dict = {'error': False, 'message': message}
    dict[key] = value
    if not (key2 is None) and not (value2 is None):
        dict[key2] = value2
    LOG.debug("Generate response OK; dict=" + str(dict))
    return dict
'''

# Generate response 200
def gen_response_ko(message, key, value, key2=None, value2=None):
    dict = {'error': True, 'message': message}
    dict[key] = value
    if not (key2 is None) and not (value2 is None):
        dict[key2] = value2
    LOG.debug("Generate response KO; dict=" + str(dict))
    return dict

'''
# Generate response ERROR
def gen_response(status, message, key, value, key2=None, value2=None):
    dict = {'error': True, 'message': message}
    dict[key] = value
    if not (key2 is None) and not (value2 is None):
        dict[key2] = value2
    LOG.debug('Generate response ' + str(status) + "; dict=" + str(dict))
    return Response(json.dumps(dict), status=status, content_type='application/json')
'''

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
        LOG.error('Lifecycle-Management: Lifecycle: check_ip: Exception')
    return False


# get_ip_address: get IP
def get_ip_address():
    ipaddr = ''
    try:
        # 1: Use outside connection
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(('google.com', 0))
        ipaddr = s.getsockname()[0]
    except:
        try:
            # 2: Use the gethostname method
            ipaddr = socket.gethostbyname(socket.gethostname())
        except:
            LOG.error('Lifecycle-Management: common: check_ip: Exception')

    LOG.info('Lifecycle-Management: common: ipaddr: ' + ipaddr)
    return ipaddr


# get_local_ip: Get local / host IP
def get_local_ip():
    return config.dic['HOST_IP'] #get_ip_address() #config.dic['HOST_IP']


###############################################################################
# ENV:
# set_value_env: set value (in config dict) from environment
def set_value_env(env_name):
    res = os.getenv(env_name, default='not-defined')
    LOG.debug('[' + env_name + '=' + res + ']')
    if res != 'not-defined':
        config.dic[env_name] = res
