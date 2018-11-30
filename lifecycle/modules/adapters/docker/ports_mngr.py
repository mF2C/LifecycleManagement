"""
ports_mngr: docker ports management
This is being developed for the MF2C Project: http://www.mf2c-project.eu/

Copyright: Roi Sucasas Font, Atos Research and Innovation, 2017.

This code is licensed under an Apache 2.0 license. Please, refer to the LICENSE.TXT file for more information

Created on 09 feb. 2018

@author: Roi Sucasas - ATOS
"""

import socket
import lifecycle.data.db as db
from common.logs import LOG


PORT_MIN = 46500
PORT_MAX = 46600
PORT_INDEX = 46500


def tryPort(port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    result = False
    try:
        sock.bind(("0.0.0.0", port))
        result = True
    except:
        print("LIFECYCLE: Port " + str(port) + " is in use")
    sock.close()
    return result


# is_port_free
def is_port_free(port):
    LOG.debug("LIFECYCLE: ports_mngr: is_port_free? [" + str(port) + "] ...")
    try:
        if port < 25000:
            LOG.warning("LIFECYCLE: ports_mngr: is_port_free: Port [" + str(port) + "] is < 25000")
            return False

        if db.get_from_DB_DOCKER_PORTS(port) is None:
            LOG.debug("LIFECYCLE: ports_mngr: is_port_free: [" + str(port) + "] is free")
            return True

        LOG.warning("LIFECYCLE: ports_mngr: is_port_free: Port [" + str(port) + "] is in use")
        return False
    except:
        LOG.error("LIFECYCLE: ports_mngr: is_port_free [" + str(port) + "]: Exception")
        return False


# take_port
def take_port(port, mappedt_to):
    return db.save_to_DB_DOCKER_PORTS(port, mappedt_to)


# release_port
def release_port(port):
    return db.del_from_DB_DOCKER_PORTS(port)


# take_port
def assign_new_port():
    global PORT_INDEX
    for i in range(PORT_MIN, PORT_MAX):
        LOG.debug("LIFECYCLE: ports_mngr: PORT_INDEX: [" + str(PORT_INDEX) + "]")
        PORT_INDEX = PORT_INDEX + 1
        #p = PORT_INDEX
        if is_port_free(PORT_INDEX):
            return PORT_INDEX