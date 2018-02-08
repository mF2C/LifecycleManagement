"""
Warnings handler
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
def thr(service_id, warning):
    try:
        LOG.debug("Lifecycle-Management: Warnings Handler module: thr: service_id: " + service_id + " ...")

        # TODO
        #...

        time.sleep(5)

        # TEST
        LOG.debug("Lifecycle-Management: Warnings Handler module: thr: " + service_id +
                   " warning: " + str(warning) + " DONE!")
    except:
        LOG.error('Lifecycle-Management: Warnings Handler module: thr: Exception')


# Handle UM warnings
def handle_warning(service_id, warning):
    try:
        LOG.info("Lifecycle-Management: Warnings Handler module: handle_warning: service_id: " +
                  service_id + ", warning: " + str(warning))

        # handle notification
        t = threading.Thread(target=thr, args=(service_id, warning,))
        t.start()

        return common.gen_response_ok('SLA Warning is being processed...', 'service_id', service_id, 'warning', warning)
    except:
        LOG.error('Lifecycle-Management: Warnings Handler module: handle_warning: Exception')
        return common.gen_response(500, 'Exception', 'service_id', service_id, 'warning', warning)
