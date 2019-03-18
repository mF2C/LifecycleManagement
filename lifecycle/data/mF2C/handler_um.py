"""
User Management Warnings handler
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
#  Warnings Handler: handles warnings coming from User Management Assessment:
#   {
#       "type": "um_warning",
#       "data"
#           {
#               "user_id": "",
#               "device_id": "",
#               "user_profile": {},
#               "sharing_model": {},
#               "result": {'battery_limit_violation': true, 'max_apps_violation': true, 'resource_contributor_violation': true}
#           }
#   }


# thread
# warning = body['data']
def thr(warning):
    try:
        LOG.debug("LIFECYCLE: UM Warnings Handler module: thr: Handling UM notifications [" + str(warning) + "] ...")

        # battery_limit_violation
        if warning['result']['battery_limit_violation']:
            LOG.warning("LIFECYCLE: UM Warnings Handler module: thr: battery_limit_violation")
            # TODO

        # resource_contributor_violation
        elif warning['result']['resource_contributor_violation']:
            LOG.warning("LIFECYCLE: UM Warnings Handler module: thr: resource_contributor_violation")
            # TODO

        # max_apps_violation
        elif warning['result']['max_apps_violation']:
            LOG.warning("LIFECYCLE: UM Warnings Handler module: thr: max_apps_violation")
            # TODO

        LOG.debug("LIFECYCLE: UM Warnings Handler module: thr: UM Notification handled")
    except:
        LOG.exception('LIFECYCLE: UM Warnings Handler module: thr: Exception')


# Handle UM warnings
def handle_warning(warning):
    try:
        LOG.info("LIFECYCLE: UM Warnings Handler module: handle_warning: warning: " + str(warning))

        # handle notification
        t = threading.Thread(target=thr, args=(warning,))
        t.start()

        return common.gen_response_ok('UM Warning is being processed...', 'warning', str(warning))
    except:
        LOG.exception('LIFECYCLE: UM Warnings Handler module: handle_warning: Exception')
        return common.gen_response(500, 'Exception', 'warning', str(warning))
