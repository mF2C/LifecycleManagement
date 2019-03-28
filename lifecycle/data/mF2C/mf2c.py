"""
Interactions with other mF2C components
This is being developed for the MF2C Project: http://www.mf2c-project.eu/

Copyright: Roi Sucasas Font, Atos Research and Innovation, 2017.

This code is licensed under an Apache 2.0 license. Please, refer to the LICENSE.TXT file for more information

Created on 09 feb. 2018

@author: Roi Sucasas - ATOS
"""

import requests
import json, ast
import config
from common.logs import LOG


###############################################################################
# USER MANAGEMENT
#   Calls to local User Management
###############################################################################


# SET UM INFORMATION
# set_lifecycle_um_properties: call to lifceycle from other agent in order to update user management properties
def user_management_set_um_properties(apps=0):
    LOG.debug("LIFECYCLE: MF2C: user_management_set_um_properties: localhost - local UM ")
    try:
        LOG.debug("LIFECYCLE: MF2C: user_management_set_um_properties: Updating UM properties ...")
        LOG.info("LIFECYCLE: MF2C: user_management_set_um_properties: HTTP PUT: " + str(config.dic['URL_AC_USER_MANAGEMENT']) + "/user-profile")
        r = requests.put(str(config.dic['URL_AC_USER_MANAGEMENT']) + "/user-profile",
                         json={"apps_running": apps},
                         verify=config.dic['VERIFY_SSL'])

        json_data = json.loads(r.text)
        LOG.debug("LIFECYCLE: MF2C: user_management_set_um_properties: response: " + str(r) + ", json_data: " + str(json_data))

        if r.status_code == 200:
            LOG.debug('LIFECYCLE: MF2C: user_management_set_um_properties: status_code=' + str(r.status_code))
            return json_data

        LOG.error('LIFECYCLE: MF2C: user_management_set_um_properties: Error: status_code=' + str(r.status_code))
    except:
        LOG.exception('LIFECYCLE: MF2C: user_management_set_um_properties: Exception')
        return None

