"""
User Management Warnings handler
This is being developed for the MF2C Project: http://www.mf2c-project.eu/

Copyright: Roi Sucasas Font, Atos Research and Innovation, 2017.

This code is licensed under an Apache 2.0 license. Please, refer to the LICENSE.TXT file for more information

Created on 27 sept. 2017

@author: Roi Sucasas - ATOS
"""

import threading, time
from lifecycle.logs import LOG
from lifecycle import common as common
from lifecycle.modules.apps.compss import adapter as compss_adpt


###############################################################################
#  Dinamicity Handler: reconfigure / redeploy service instances when a device leaves the cluster
#   ==> Event System


# thread
# warning = body['data']
def thr(notification):
    try:
        LOG.debug("[lifecycle.events.handler_dinamicity] [thr] Handling event / notification [" + str(notification) + "] ...")

        # TODO
        # Get agent information

        # Get service instances running in lost agent
        # ...

        # Iterate resulting service instances
        # 1. if service_instance is running COMPSs ...
        compss_adpt.notify_job_resource_lost(None)

        # 2. if service_instance is running other app ...
        # redeploy

        time.sleep(10)

        LOG.debug("[lifecycle.events.handler_dinamicity] [thr] Event / notification handled")
    except:
        LOG.exception('[lifecycle.events.handler_dinamicity] [thr] Exception')


# Handle Dinamicity notifications
def handle_dinamicity(notification):
    try:
        LOG.info("[lifecycle.events.handler_dinamicity] [handle_dinamicity] notification: " + str(notification))

        # handle notification
        t = threading.Thread(target=thr, args=(notification,))
        t.start()

        return common.gen_response_ok('UM notification is being processed...', 'notification', str(notification))
    except:
        LOG.exception('[lifecycle.events.handler_dinamicity] [handle_dinamicity] Exception')
        return common.gen_response(500, 'Exception', 'notification', str(notification))
