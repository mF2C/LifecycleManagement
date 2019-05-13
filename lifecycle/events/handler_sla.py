"""
SLAs' notifications handler
This is being developed for the MF2C Project: http://www.mf2c-project.eu/

Copyright: Roi Sucasas Font, Atos Research and Innovation, 2017.

This code is licensed under an Apache 2.0 license. Please, refer to the LICENSE.TXT file for more information

Created on 27 sept. 2017

@author: Roi Sucasas - ATOS
"""

import threading, time
from lifecycle.logs import LOG
from lifecycle import common as common


###############################################################################
# SLA Notifications: handles warnings coming from User Management Assessment
#   {
#       "type": "sla_notification",
#       "data"
#           {
#               "user_id": "",
#               "device_id": "",
#               "service_instance_id": "",
#               "warning_id": "",
#               "warning_txt": ""
#           }
#   }


# thread
def thr(notification):
    try:
        LOG.debug("[lifecycle.events.handler_sla] [thr] Handling SLA violations [" + str(notification) + "] ...")

        # TODO
        #...

        time.sleep(10)

        LOG.debug("[lifecycle.events.handler_sla] [thr] SLA violations handled")
    except:
        LOG.error('[lifecycle.events.handler_sla] [thr] Exception')


# Handle SLA violations
def handle_sla_notification(notification):
    try:
        LOG.info("[lifecycle.events.handler_sla] [handle_sla_notification] service_instance_id: notification: " + str(notification))

        # handle notification
        t = threading.Thread(target=thr, args=(notification,))
        t.start()

        return common.gen_response_ok('SLA Notification has been processed', 'notification', str(notification))
    except:
        LOG.error('[lifecycle.events.handler_sla] [handle_sla_notification] Exception')
        return common.gen_response(500, 'Exception', 'notification', str(notification))