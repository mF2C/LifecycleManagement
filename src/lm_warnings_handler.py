'''
Warnings handler
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
def thr(warning):
    try:
        logs.info(">> UM warnings handler >> executing ...")
        logs.info(">> " + str(warning))
        # TODO

        time.sleep(10)
        logs.info(">> done.")
    except:
        logs.error('>> Error (0): Warnings_Handler: thread: Exception')


# Handle UM warnings
def handleWarning(warning):
    try:
        logs.info("Warnings_Handler: handleWarning: " + str(warning))

        # handle notification
        t = threading.Thread(target=thr, args=(warning,))
        t.start()
    except:
        logs.error('Error (0): SLA_Handler: handleWarning: Exception')
