"""
Warnings handler
This is being developed for the MF2C Project: http://www.mf2c-project.eu/

Copyright: Roi Sucasas Font, Atos Research and Innovation, 2017.

This code is licensed under an Apache 2.0 license. Please, refer to the LICENSE.TXT file for more information

Created on 27 sept. 2017

@author: Roi Sucasas - ATOS
"""


from src.utils import logs
from flask import Response, json
import threading
import time


# thread
def thr(service_id, warning):
    try:
        logs.debug("Lifecycle-Management: Warnings Handler module: thr: service_id: " + service_id + " ...")

        # TODO
        #...

        time.sleep(5)

        # TEST
        logs.debug("Lifecycle-Management: Warnings Handler module: thr: " + service_id +
                   " warning: " + str(warning) + " DONE!")
    except:
        logs.error('Lifecycle-Management: Warnings Handler module: thr: Exception')


# Handle UM warnings
def handle_warning(service_id, warning):
    try:
        logs.info("Lifecycle-Management: Warnings Handler module: handle_warning: service_id: " +
                  service_id + ", warning: " + str(warning))

        # handle notification
        t = threading.Thread(target=thr, args=(service_id, warning,))
        t.start()

        return {'error': False, 'message': 'Warning is being processed...', 'service_id': service_id, 'warning': warning}
    except:
        logs.error('Lifecycle-Management: Warnings Handler module: handle_warning: Exception')
        return Response(json.dumps({'error': True, 'message': 'Exception', 'warning': ''}),
                        status=500, content_type='application/json')
