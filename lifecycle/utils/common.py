"""
Common functions
This is being developed for the MF2C Project: http://www.mf2c-project.eu/

Copyright: Roi Sucasas Font, Atos Research and Innovation, 2017.

This code is licensed under an Apache 2.0 license. Please, refer to the LICENSE.TXT file for more information

Created on 09 feb. 2018

@author: Roi Sucasas - ATOS
"""


import socket, os
from lifecycle import config
from flask import Response, json
from lifecycle.utils.logs import LOG


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





# check_ip: Check if IP is alive
def check_ip(ip_adress):
    try:
        # '-c 1' ==> linux
        # '-n 1' ==> windows
        response = os.system("ping -n 1 " + ip_adress)
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
            LOG.error('Lifecycle-Management: Lifecycle: check_ip: Exception')

    return ipaddr


# Get IP
def get_ip():
    return get_ip_address() #config.dic['HOST_IP']
