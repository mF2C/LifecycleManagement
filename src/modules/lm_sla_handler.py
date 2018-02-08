"""
SLAs' notifications handler
This is being developed for the MF2C Project: http://www.mf2c-project.eu/

Copyright: Roi Sucasas Font, Atos Research and Innovation, 2017.

This code is licensed under an Apache 2.0 license. Please, refer to the LICENSE.TXT file for more information

Created on 27 sept. 2017

@author: Roi Sucasas - ATOS
"""


from src.utils.logs import LOG
import src.utils.common as common
import threading
import time


# thread
def thr(service_id, notification):
    try:
        LOG.debug("Lifecycle-Management: SLA Notifications Handler module: thr: service_id: " + service_id + " ...")

        # TODO
        #...

        time.sleep(10)

        # TEST
        LOG.debug("Lifecycle-Management: SLA Notifications Handler module: thr: " + service_id +
                   " notification: " + str(notification) + " DONE!")
    except:
        LOG.error('Lifecycle-Management: SLA Notifications Handler module: thr: Exception')


# Handle SLA violations
def handle_sla_notification(service_id, notification):
    try:
        LOG.info("Lifecycle-Management: SLA Notifications Handler module: handle_sla_notification: service_id: " +
                  service_id + ", notification: " + str(notification))

        # handle notification
        t = threading.Thread(target=thr, args=(service_id, notification,))
        t.start()

        return common.gen_response_ok('SLA Notification has been processed', 'service_id', service_id, 'notification', notification)
    except:
        LOG.error('Lifecycle-Management: SLA Notifications Handler module: handle_sla_notification: Exception')
        return common.gen_response(500, 'Exception', 'service_id', service_id, 'notification', notification)