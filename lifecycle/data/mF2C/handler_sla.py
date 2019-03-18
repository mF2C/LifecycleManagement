"""
SLAs' notifications handler
This is being developed for the MF2C Project: http://www.mf2c-project.eu/

Copyright: Roi Sucasas Font, Atos Research and Innovation, 2017.

This code is licensed under an Apache 2.0 license. Please, refer to the LICENSE.TXT file for more information

Created on 27 sept. 2017

@author: Roi Sucasas - ATOS
"""


from common.logs import LOG
import common.common as common
import threading
import time


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
        LOG.debug("LIFECYCLE: SLA Notifications Handler module: thr: Handling SLA violations [" + str(notification) + "] ...")

        # TODO
        #...

        time.sleep(10)

        LOG.debug("LIFECYCLE: SLA Notifications Handler module: thr: SLA violations handled")
    except:
        LOG.error('LIFECYCLE: SLA Notifications Handler module: thr: Exception')


# Handle SLA violations
def handle_sla_notification(notification):
    try:
        LOG.info("LIFECYCLE: SLA Notifications Handler module: handle_sla_notification: service_instance_id: notification: " + str(notification))

        # handle notification
        t = threading.Thread(target=thr, args=(notification,))
        t.start()

        return common.gen_response_ok('SLA Notification has been processed', 'notification', str(notification))
    except:
        LOG.error('LIFECYCLE: SLA Notifications Handler module: handle_sla_notification: Exception')
        return common.gen_response(500, 'Exception', 'notification', str(notification))