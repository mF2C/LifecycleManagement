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
from lifecycle import config
from lifecycle.utils.logs import LOG


# ACL
acl = {"owner":
           {"principal": config.dic['CIMI_USER'], #"ADMIN",
            "type": "ROLE"},
       "rules": [{"principal": config.dic['CIMI_USER'], #"ADMIN",
                  "type": "ROLE",
                  "right": "ALL"},
                 {"principal": "ANON",
                  "type": "ROLE",
                  "right": "ALL"}
                 ]}


# common_new_map_fields: generates a map with time and acl values
def common_new_map_fields():
    now = datetime.datetime.now()
    default_map = {
        "created": now.strftime('%Y-%m-%dT%H:%M:%S.%fZ'),
        "updated": now.strftime('%Y-%m-%dT%H:%M:%S.%fZ'),
        "resourceURI": {"href": "service-instance/1234579abcdef"},
        "acl": acl
    }
    return default_map


# common_update_map_fields: generates a map with time and acl values
def common_update_map_fields():
    now = datetime.datetime.now()
    default_map = {
        "updated": now.strftime('%Y-%m-%dT%H:%M:%S.%fZ'),
        "acl": acl
    }
    return default_map


###############################################################################


# get_service_instance_by_id: get service instance by id
def get_service_instance_by_id(id, obj_response_cimi=None):
    try:
        res = requests.get(config.dic['CIMI_URL'] + '/service-instance/' + id,
                           headers={'slipstream-authn-info': 'super ADMIN'},
                           verify=False)

        if res.status_code == 200:
            return res.json()

        LOG.error("Request failed: " + res.status_code)
        LOG.error("Response: " + str(res.json()))
        return None
    except:
        traceback.print_exc(file=sys.stdout)
        LOG.error('Exception')
        return None


# get_all_service_instances: get all service instances
def get_all_service_instances(obj_response_cimi=None):
    try:
        res = requests.get(config.dic['CIMI_URL'] + '/service-instance',
                           headers={'slipstream-authn-info': 'super ADMIN'},
                           verify=False)

        if res.status_code == 200:
            return res.json()['serviceInstances']

        LOG.error("Request failed: " + res.status_code)
        LOG.error("Response: " + str(res.json()))
        return None
    except:
        traceback.print_exc(file=sys.stdout)
        LOG.error('Exception')
        return None


# del_service_instance_by_id: delete service instance
def del_service_instance_by_id(id, obj_response_cimi=None):
    try:
        res = requests.delete(config.dic['CIMI_URL'] + '/service-instance/' + id,
                              headers={'slipstream-authn-info': 'super ADMIN'},
                              verify=False)

        if res.status_code == 200:
            return res.json()
        return None
    except:
        traceback.print_exc(file=sys.stdout)
        LOG.error('Exception')
        return None


# FUNCTION: add_service_instance: add resource to cimi
# RETURNS: resource
def add_service_instance(resource_name, content):
    try:
        LOG.debug("Adding new resource to [" + resource_name + "] ... ")

        # complete map and update resource
        content.update(common_new_map_fields())

        res = requests.post(config.dic['CIMI_URL'] + '/service-instance',
                            headers={'slipstream-authn-info': 'super ADMIN'},
                            verify=False,
                            json=content)

        if res.status_code == 201:
            id = res.json()['resource-id'].replace('service-instance/', '')
            return get_service_instance_by_id(id)

        LOG.error("Request failed: " + res.status_code)
        LOG.error("Response: " + str(res.json()))
        return None
    except:
        traceback.print_exc(file=sys.stdout)
        LOG.error('Exception')
        return None


# update_service_instance: updates a service_instance
def update_service_instance(resource_id, content):
    try:
        LOG.info("Updating resource [" + resource_id + "] ... ")
        resource_id = resource_id.replace('service-instance/', '')

        # complete map and update resource
        content.update(common_update_map_fields())

        res = requests.put(config.dic['CIMI_URL']  + '/service-instance/' + resource_id,
                            headers={'slipstream-authn-info': 'super ADMIN'},
                            verify=False,
                            json=content)

        if res.status_code == 200:
            return get_service_instance_by_id(resource_id)

        LOG.error("Request failed: " + res.status_code)
        LOG.error("Response: " + str(res.json()))
        return None
    except:
        traceback.print_exc(file=sys.stdout)
        LOG.error('Exception')
        return None



