"""
ports_mngr: docker ports management
This is being developed for the MF2C Project: http://www.mf2c-project.eu/

Copyright: Roi Sucasas Font, Atos Research and Innovation, 2017.

This code is licensed under an Apache 2.0 license. Please, refer to the LICENSE.TXT file for more information

Created on 09 feb. 2018

@author: Roi Sucasas - ATOS
"""

import socket
from lifecycle.data import data_adapter as data_adapter
from lifecycle.logs import LOG


PORT_MIN = 20001
PORT_MAX = 55000
PORT_INDEX = 20001


# tryPort
def tryPort(port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    result = False
    try:
        sock.bind(("0.0.0.0", port))
        #sock.connect_ex(('127.0.0.1', 80))
        result = True
    except:
        LOG.warning("[lifecycle.modules.apps.ports_mngr] [tryPort] Port (" + str(port) + ") is in use")
    sock.close()
    return result


# is_port_free
def is_port_free(port):
    try:
        if port < 10000:
            LOG.warning("[lifecycle.modules.apps.ports_mngr] [is_port_free] Ports (" + str(port) + ") under 10000 are nor allowed")
            return False

        if data_adapter.db_get_port_mapped(port) is None and tryPort(port):
            LOG.debug("[lifecycle.modules.apps.ports_mngr] [is_port_free] Port (" + str(port) + ") is free")
            return True
    except:
        LOG.exception("[lifecycle.modules.apps.ports_mngr] [is_port_free] [" + str(port) + "]: Exception")
    return False


# take_port
def take_port(port, mappedt_to):
    return data_adapter.db_save_port_mapped(port, mappedt_to)


# release_port
def release_port(port):
    return data_adapter.db_delete_port(port)


# take_port
def assign_new_port():
    global PORT_INDEX
    for i in range(PORT_MIN, PORT_MAX):
        if is_port_free(PORT_INDEX):
            return PORT_INDEX
        PORT_INDEX = PORT_INDEX + 1


# replace_in_list: replace element in list
def replace_in_list(l, xvalue, newxvalue):
    for n, i in enumerate(l):
        if i == xvalue:
            l[n] = newxvalue
    return l


# create_ports_dict:
def create_ports_dict(ports, isCompss=False):
    try:
        LOG.debug("[lifecycle.modules.apps.ports_mngr] [create_ports_dict] Checking and configuring service instance ports [" + str(ports) + "] ...")
        dict_ports = {}
        for p in ports:
            if is_port_free(p):
                dict_ports.update({p:p})
                take_port(p, p)
                LOG.debug("[lifecycle.modules.apps.ports_mngr] [create_ports_dict] port [ " + str(p) + " ] is free")
            else:
                np = assign_new_port()
                # original port : new port (exposed to host)
                if not isCompss:
                    dict_ports.update({p: np})
                    take_port(np, p)
                    replace_in_list(ports, p, np)
                    LOG.debug("[lifecycle.modules.apps.ports_mngr] [create_ports_dict] Port [ " + str(p) + " ] not free: redirected to " + str(np))
                else:
                    dict_ports.update({np: np})
                    take_port(np, np)
                    replace_in_list(ports, np, np)
                    LOG.debug("[lifecycle.modules.apps.ports_mngr] [create_ports_dict] Compss service using port: " + str(np))

        return dict_ports
    except:
        LOG.exception("[lifecycle.modules.apps.ports_mngr] [create_ports_dict] Error during the ports dict creation: " + str(ports))
        return {ports[0]:ports[0]}
