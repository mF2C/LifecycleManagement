'''
SLAs' notifications handler
This is being developed for the MF2C Project: http://www.mf2c-project.eu/

Copyright: Roi Sucasas Font, Atos Research and Innovation, 2017.

This code is licensed under an Apache 2.0 license. Please, refer to the LICENSE.TXT file for more information

Created on 27 sept. 2017

@author: Roi Sucasas - ATOS
'''

#!/usr/bin/python3

import threading
import logs
import time


# thread
def thr(notification):
    try:
        logs.info(">> sla notifications handler >> executing ...")
        logs.info(">> " + str(notification))
        # TODO

        time.sleep(10)
        logs.info(">> done.")
    except:
        logs.error('>> Error (0): SLA_Handler: thread: Exception')


# Handle SLA violations
def handleSLANotifications(notification):
    try:
        logs.info("SLA_Handler: handleSLANotifications: " + str(notification))

        # handle notification
        t = threading.Thread(target=thr, args=(notification,))
        t.start()
    except:
        logs.error('Error (0): SLA_Handler: handleSLANotifications: Exception')