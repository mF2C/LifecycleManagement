"""
ports_mngr: docker ports management
This is being developed for the MF2C Project: http://www.mf2c-project.eu/

Copyright: Roi Sucasas Font, Atos Research and Innovation, 2017.

This code is licensed under an Apache 2.0 license. Please, refer to the LICENSE.TXT file for more information

Created on 09 feb. 2018

@author: Roi Sucasas - ATOS
"""

import socket
import lifecycle.utils.db as DB
from lifecycle.utils.logs import LOG


# is_port_free
def is_port_free(port):
    LOG.debug("Lifecycle-Management: Docker: ports_mngr: is_port_free? [" + str(port) + "] ...")
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        result = False
        try:
            sock.bind(("0.0.0.0", port))
            result = True
            LOG.debug("Lifecycle-Management: Docker: ports_mngr: is_port_free: [" + str(port) + "] is free")
        except:
            LOG.warning("Lifecycle-Management: Docker: ports_mngr: is_port_free: Port [" + str(port) + "] is in use")
        sock.close()
        return result
    except:
        LOG.error("Lifecycle-Management: Docker: ports_mngr: is_port_free [" + str(port) + "]: Exception")
        return False


# take_port
def take_port(port, mappedt_to):
    return DB.save_to_DB_DOCKER_PORTS(port, mappedt_to)


# release_port
def release_port(port):
    return DB.del_from_DB_DOCKER_PORTS(port)


# take_port
def assign_new_port(port):
    for i in range(1, 50):
        p = port + i
        if is_port_free(p):
            return p