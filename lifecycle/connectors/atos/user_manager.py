"""
Interactions with other mF2C components
This is being developed for the MF2C Project: http://www.mf2c-project.eu/

Copyright: Roi Sucasas Font, Atos Research and Innovation, 2017.

This code is licensed under an Apache 2.0 license. Please, refer to the LICENSE.TXT file for more information

Created on 09 may. 2019

@author: Roi Sucasas - ATOS
"""

import requests, json
import config
from lifecycle.logs import LOG


# SET UM INFORMATION
# set_um_properties: call to lifceycle from other agent in order to update user management properties
def set_um_properties(apps=0):
    LOG.debug("[lifecycle.connectors.atos.user_manager] [set_um_properties] localhost - local UM: Updating UM properties ...")
    try:
        LOG.info("[lifecycle.connectors.atos.user_manager] [set_um_properties] HTTP PUT: " + str(config.dic['URL_AC_USER_MANAGEMENT']) + "/sharing-model")
        r = requests.put(str(config.dic['URL_AC_USER_MANAGEMENT']) + "/sharing-model",
                         json={"apps_running": apps},
                         verify=config.dic['VERIFY_SSL'])
        LOG.debug("[lifecycle.connectors.atos.user_manager] [set_um_properties] response: " + str(r) + ", " + str(r.json()))

        if r.status_code == 200:
            json_data = json.loads(r.text)
            LOG.debug('[lifecycle.connectors.atos.user_manager] [set_um_properties] json_data=' + str(json_data))
            return json_data

        LOG.error("[lifecycle.connectors.atos.user_manager] [set_um_properties] Error: status_code=" + str(r.status_code) + "; Returning None ...")
    except:
        LOG.exception("[lifecycle.connectors.atos.user_manager] [set_um_properties] Exception; Returning None ...")
    return None


# CHECK AVIALABILITY
# check_avialability: call to local UM to check if it's possible to deploy a service
def check_avialability():
    LOG.debug("[lifecycle.connectors.atos.user_manager] [check_avialability] localhost - local UM: Checking avialability ...")
    try:
        LOG.info("[lifecycle.connectors.atos.user_manager] [check_avialability] HTTP GET: " + str(config.dic['URL_AC_USER_MANAGEMENT']) + "/check")
        r = requests.get(str(config.dic['URL_AC_USER_MANAGEMENT']) + "/check",
                         verify=config.dic['VERIFY_SSL'])
        LOG.debug("[lifecycle.connectors.atos.user_manager] [check_avialability] response: " + str(r) + ", " + str(r.json()))

        json_data = json.loads(r.text)
        LOG.debug("[lifecycle.connectors.atos.user_manager] [check_avialability] json_data=" + str(json_data))
        if r.status_code == 200 and not json_data['result'] is None:
            return json_data

        LOG.error("[lifecycle.connectors.atos.user_manager] [check_avialability] Error: status_code=" + str(r.status_code) + "; Returning None ...")
    except:
        LOG.exception("[lifecycle.connectors.atos.user_manager] [check_avialability] Exception; Returning None ...")
    return None


# GET CURRENT USER / DEVICE
# get_current: call to local UM to get current values (user, device)
def get_current(val):
    LOG.debug("[lifecycle.connectors.atos.user_manager] [get_current] Getting current " + val + " from localhost - UM: Checking avialability ...")
    try:
        LOG.info("[lifecycle.connectors.atos.user_manager] [get_current] HTTP GET: " + str(config.dic['URL_AC_USER_MANAGEMENT']) + "/current/" + val)
        r = requests.get(str(config.dic['URL_AC_USER_MANAGEMENT']) + "/current/" + val,
                         verify=config.dic['VERIFY_SSL'])
        LOG.debug("[lifecycle.connectors.atos.user_manager] [get_current] response: " + str(r) + ", " + str(r.json()))

        json_data = json.loads(r.text)
        LOG.debug("[lifecycle.connectors.atos.user_manager] [get_current] json_data=" + str(json_data))
        if r.status_code == 200:
            return json_data

        LOG.error("[lifecycle.connectors.atos.user_manager] [get_current] Error: status_code=" + str(r.status_code) + "; Returning None ...")
    except:
        LOG.exception("[lifecycle.connectors.atos.user_manager] [get_current] Exception; Returning None ...")
    return None