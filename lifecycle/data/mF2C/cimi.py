"""
CIMI interface
This is being developed for the MF2C Project: http://www.mf2c-project.eu/

Copyright: Roi Sucasas Font, Atos Research and Innovation, 2017.

This code is licensed under an Apache 2.0 license. Please, refer to the LICENSE.TXT file for more information

Created on 09 feb. 2018

@author: Roi Sucasas - ATOS
"""

import requests
import sys, traceback
import datetime
import config
from common.logs import LOG


# SERVICE_INSTANCE CIMI RESOURCE
RSRC_SERVICE_INSTANCE = "service-instance"
# SERVICE CIMI RESOURCE
RSRC_SERVICE = "service"

# ACL
ACL = {"owner":
           {"principal": config.dic['CIMI_USER'], #"ADMIN",
            "type": "ROLE"},
       "rules": [{"principal": config.dic['CIMI_USER'], #"ADMIN",
                  "type": "ROLE",
                  "right": "ALL"},
                 {"principal": "ANON",
                  "type": "ROLE",
                  "right": "ALL"}
                 ]}
# CIMI HEADER
CIMI_HEADER = {'slipstream-authn-info': 'super ADMIN'}


# TODO replace ACL
# Generates ACL for a specific user
def getACLforUser(user):
    ACL_USER = {"owner":
                   {"principal": user,
                    "type": "ROLE"},
               "rules": [{"principal": user,
                          "type": "ROLE",
                          "right": "ALL"},
                         {"principal": "ANON",
                          "type": "ROLE",
                          "right": "ALL"}
                         ]}
    return ACL_USER


# common_new_map_fields: generates a map with time and acl values
def common_new_map_fields():
    now = datetime.datetime.now()
    default_map = {
        "created": now.strftime('%Y-%m-%dT%H:%M:%S.%fZ'),
        "updated": now.strftime('%Y-%m-%dT%H:%M:%S.%fZ'),
        "resourceURI": {"href": "service-instance/1234579abcdef"},
        "acl": ACL
    }
    return default_map


# common_update_map_fields: generates a map with time and acl values
def common_update_map_fields():
    now = datetime.datetime.now()
    default_map = {
        "updated": now.strftime('%Y-%m-%dT%H:%M:%S.%fZ'),
        "acl": ACL
    }
    return default_map


# patch_update_map_fields: TODO remove after dataclay is updated
def patch_update_map_fields():
    now = datetime.datetime.now()
    default_map = {
        "device_id":        "not-defined",
        "device_ip":        "not-defined",
        "parent_device_id": "not-defined",
        "parent_device_ip": "not-defined",
        "service_type": "not-defined"
    }
    return default_map


###############################################################################
# COMMON

# TODO get this information from new RESOURCE: AGENT
# get_current_device_info
def get_current_device_info():
    try:
        res = requests.get(config.dic['CIMI_URL'] + "/device",
                           headers=CIMI_HEADER,
                           verify=False)

        LOG.info("LIFECYCLE: cimi: get_current_device_info: response: " + str(res.json()))

        if res.status_code == 200 and res.json()['count'] == 0:
            LOG.warning("LIFECYCLE: cimi: get_current_device_info: 'device' not found")
            return -1
        elif res.status_code == 200:
            return res.json()['devices'][0]

        LOG.warning("LIFECYCLE: cimi: get_current_device_info: 'device' not found")
        return -1
    except:
        LOG.exception('LIFECYCLE: cimi: get_current_device_info: Exception')
        return None


# exist_user: check if 'user id' exists
def exist_user(user_id):
    try:
        user_id = user_id.replace('user/', '')
        res = requests.get(config.dic['CIMI_URL'] + "/user/" + user_id,
                           headers=CIMI_HEADER,
                           verify=False)
        LOG.debug("LIFECYCLE: cimi: exist_user: Response: " + str(res.json()))

        if res.status_code == 200 and not res.json()['id'] is None:
            return True
    except:
        traceback.print_exc(file=sys.stdout)
        LOG.warning("LIFECYCLE: cimi: exist_user: controlled exception")
    LOG.warning("LIFECYCLE: cimi: exist_user: 'user' not found / error getting user")
    return False


# exist_device: check if 'device id' exists
def exist_device(device_id):
    try:
        device_id = device_id.replace('device/', '')
        res = requests.get(config.dic['CIMI_URL'] + "/device/" + device_id,
                           headers=CIMI_HEADER,
                           verify=False)
        LOG.debug("LIFECYCLE: cimi: exist_device: Response: " + str(res.json()))
        if res.status_code == 200 and not res.json()['id'] is None:
            return True
    except:
        traceback.print_exc(file=sys.stdout)
        LOG.warning("LIFECYCLE: cimi: exist_user: controlled exception")
    LOG.warning("LIFECYCLE: cimi: exist_device: 'device' not found / error getting device")
    return False


###############################################################################
# UM

# TODO get this information from new RESOURCE: AGENT
# get_user_profile_by_device: get profile from device
def get_user_profile_by_device(device_id):
    try:
        device_id = device_id.replace('device/', '')

        res = requests.get(config.dic['CIMI_URL'] + "/user-profile?$filter=device_id=\"device/" + device_id + "\"",
                           headers=CIMI_HEADER,
                           verify=False)

        LOG.debug("LIFECYCLE: cimi: get_user_profile_by_device: response: " + str(res))
        LOG.debug("LIFECYCLE: cimi: get_user_profile_by_device: response: " + str(res.json()))

        if res.status_code == 200 and len(res.json()['userProfiles']) > 0:
            return res.json()['userProfiles'][0]
        else:
            LOG.warning("LIFECYCLE: cimi: get_user_profile_by_device: User's profile not found [device_id=" + device_id + "]")
            return -1
    except:
        LOG.exception('LIFECYCLE: cimi: get_user_profile_by_device: Exception')
        return None


# TODO get this information from new RESOURCE: AGENT
# get_sharing_model_by_device: get sharing model from device
def get_sharing_model_by_device(device_id):
    try:
        device_id = device_id.replace('device/', '')

        res = requests.get(config.dic['CIMI_URL'] + "/sharing-model?$filter=device_id=\"device/" + device_id + "\"",
                           headers=CIMI_HEADER,
                           verify=False)

        LOG.debug("LIFECYCLE: cimi: get_sharing_model_by_device: response: " + str(res))
        LOG.debug("LIFECYCLE: cimi: get_sharing_model_by_device: response: " + str(res.json()))

        if res.status_code == 200 and len(res.json()['sharingModels']) > 0:
            return res.json()['sharingModels'][0]
        else:
            LOG.warning("LIFECYCLE: cimi: get_sharing_model_by_device: Sharing-model not found [device_id=" + device_id + "]")
            return -1
    except:
        LOG.exception('LIFECYCLE: cimi: get_sharing_model_by_device: Exception')
        return None


###############################################################################


# get_service_by_id: get service by id
def get_service_by_id(id):
    try:
        resource_id = id.replace(RSRC_SERVICE + '/', '')
        LOG.debug("LIFECYCLE: cimi: get_service_by_id: Getting service instance [" + resource_id + "] ... ")

        res = requests.get(config.dic['CIMI_URL'] + '/' + RSRC_SERVICE + '/' + resource_id, headers=CIMI_HEADER, verify=False)
        if res.status_code == 200:
            return res.json()

        LOG.error("LIFECYCLE: cimi: get_service_by_id: Request failed: " + res.status_code)
        LOG.error("LIFECYCLE: cimi: get_service_by_id: Response: " + str(res.json()))
        return None
    except:
        traceback.print_exc(file=sys.stdout)
        LOG.error('LIFECYCLE: cimi: get_service_by_id: Exception')
        return None


# get_service_instance_by_id: get service instance by id
def get_service_instance_by_id(id, obj_response_cimi=None):
    try:
        LOG.debug("LIFECYCLE: cimi: get_service_instance_by_id: Getting service instance [" + id + "] ... ")

        res = requests.get(config.dic['CIMI_URL'] + '/' + RSRC_SERVICE_INSTANCE + '/' + id, headers=CIMI_HEADER, verify=False)
        if res.status_code == 200:
            return res.json()

        LOG.error("LIFECYCLE: cimi: get_service_instance_by_id: Request failed: " + res.status_code)
        LOG.error("LIFECYCLE: cimi: get_service_instance_by_id: Response: " + str(res.json()))
        return None
    except:
        traceback.print_exc(file=sys.stdout)
        LOG.error('LIFECYCLE: cimi: get_service_instance_by_id: Exception')
        return None


# get_all_service_instances: get all service instances
def get_all_service_instances(obj_response_cimi=None):
    try:
        LOG.debug("LIFECYCLE: cimi: get_all_service_instances: Getting all service instances ... ")

        res = requests.get(config.dic['CIMI_URL'] + '/' + RSRC_SERVICE_INSTANCE, headers=CIMI_HEADER, verify=False)
        if res.status_code == 200:
            return res.json()['serviceInstances']

        LOG.error("LIFECYCLE: cimi: get_all_service_instances: Request failed: " + res.status_code)
        LOG.error("LIFECYCLE: cimi: get_all_service_instances: Response: " + str(res.json()))
        return None
    except:
        traceback.print_exc(file=sys.stdout)
        LOG.error('LIFECYCLE: cimi: get_all_service_instances: Exception')
        return None


# del_service_instance_by_id: delete service instance
def del_service_instance_by_id(resource_id, obj_response_cimi=None):
    try:
        LOG.debug("LIFECYCLE: cimi: del_service_instance_by_id: Deleting resource [" + resource_id + "] ... ")
        resource_id = resource_id.replace(RSRC_SERVICE_INSTANCE + '/', '')

        res = requests.delete(config.dic['CIMI_URL'] + '/' + RSRC_SERVICE_INSTANCE + '/' + resource_id, headers=CIMI_HEADER, verify=False)
        if res.status_code == 200:
            return res.json()

        return None
    except:
        traceback.print_exc(file=sys.stdout)
        LOG.error('LIFECYCLE: cimi: del_service_instance_by_id: Exception')
        return None


# del_all_service_instances: delete all service instances
def del_all_service_instances(obj_response_cimi=None):
    try:
        LOG.debug("LIFECYCLE: cimi: del_all_service_instances: Deleting all  service instances ... ")

        service_instances = get_all_service_instances()
        for si in service_instances:
            LOG.info("LIFECYCLE: cimi: del_all_service_instances: Deleting " + si['id'] + " ... ")
            resource_id = si['id'].replace(RSRC_SERVICE_INSTANCE + '/', '')
            requests.delete(config.dic['CIMI_URL'] + '/' + RSRC_SERVICE_INSTANCE + '/' + resource_id, headers=CIMI_HEADER, verify=False)
        return True
    except:
        traceback.print_exc(file=sys.stdout)
        LOG.error('LIFECYCLE: cimi: del_all_service_instances: Exception')
        return False


# FUNCTION: add_service_instance: add resource to cimi
# RETURNS: resource
def add_service_instance(content):
    try:
        LOG.debug("LIFECYCLE: cimi: add_service_instance: Adding new resource to service instances ... ")

        # complete map and update resource
        content.update(common_new_map_fields())

        LOG.debug("LIFECYCLE: cimi: add_service_instance: [content=" + str(content) + "] ... ")

        res = requests.post(config.dic['CIMI_URL'] + '/' + RSRC_SERVICE_INSTANCE,
                            headers=CIMI_HEADER,
                            verify=False,
                            json=content)

        LOG.debug("LIFECYCLE: cimi: add_service_instance: res: " + str(res))

        if res.status_code == 201:
            id = res.json()['resource-id'].replace(RSRC_SERVICE_INSTANCE + '/', '')
            return get_service_instance_by_id(id)

        LOG.error("LIFECYCLE: cimi: add_service_instance: Request failed: " + res.status_code)
        LOG.error("LIFECYCLE: cimi: add_service_instance: Response: " + str(res.json()))
        return None
    except:
        traceback.print_exc(file=sys.stdout)
        LOG.error('LIFECYCLE: cimi: add_service_instance: Exception while adding new resource to service instances!')
        return None


# update_service_instance: updates a service_instance
def update_service_instance(resource_id, content):
    try:
        LOG.debug("LIFECYCLE: cimi: update_service_instance: Updating resource [" + resource_id + "] ... ")
        resource_id = resource_id.replace(RSRC_SERVICE_INSTANCE + '/', '')

        # complete map and update resource
        content.update(common_update_map_fields())

        content.update(patch_update_map_fields())

        LOG.debug("LIFECYCLE: cimi: update_service_instance: [content=" + str(content) + "] ... ")

        res = requests.put(config.dic['CIMI_URL']  + '/' + RSRC_SERVICE_INSTANCE + '/' + resource_id,
                           headers=CIMI_HEADER,
                           verify=False,
                           json=content)

        LOG.debug("LIFECYCLE: cimi: update_service_instance: [res=" + str(res) + "]")

        if res.status_code == 200:
            return get_service_instance_by_id(resource_id)

        LOG.error("LIFECYCLE: cimi: update_service_instance: Request failed: " + res.status_code)
        LOG.error("LIFECYCLE: cimi: update_service_instance: Response: " + str(res.json()))
        return None
    except:
        traceback.print_exc(file=sys.stdout)
        LOG.error('LIFECYCLE: cimi: update_service_instance: Exception')
        return None



