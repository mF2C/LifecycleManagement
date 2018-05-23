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
# CIMI HEADER
cimi_header = {'slipstream-authn-info': 'super ADMIN'}


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
        LOG.debug("cimi: get_service_instance_by_id: Getting service instance [" + id + "] ... ")

        res = requests.get(config.dic['CIMI_URL'] + '/service-instance/' + id, headers=cimi_header, verify=False)
        if res.status_code == 200:
            return res.json()

        LOG.error("cimi: get_service_instance_by_id: Request failed: " + res.status_code)
        LOG.error("cimi: get_service_instance_by_id: Response: " + str(res.json()))
        return None
    except:
        traceback.print_exc(file=sys.stdout)
        LOG.error('cimi: get_service_instance_by_id: Exception')
        return None


# get_all_service_instances: get all service instances
def get_all_service_instances(obj_response_cimi=None):
    try:
        LOG.debug("cimi: get_all_service_instances: Getting all service instances ... ")

        res = requests.get(config.dic['CIMI_URL'] + '/service-instance', headers=cimi_header, verify=False)
        if res.status_code == 200:
            return res.json()['serviceInstances']

        LOG.error("cimi: get_all_service_instances: Request failed: " + res.status_code)
        LOG.error("cimi: get_all_service_instances: Response: " + str(res.json()))
        return None
    except:
        traceback.print_exc(file=sys.stdout)
        LOG.error('cimi: get_all_service_instances: Exception')
        return None


# del_service_instance_by_id: delete service instance
def del_service_instance_by_id(resource_id, obj_response_cimi=None):
    try:
        LOG.debug("cimi: del_service_instance_by_id: Deleting resource [" + resource_id + "] ... ")
        resource_id = resource_id.replace('service-instance/', '')

        res = requests.delete(config.dic['CIMI_URL'] + '/service-instance/' + resource_id, headers=cimi_header, verify=False)
        if res.status_code == 200:
            return res.json()

        return None
    except:
        traceback.print_exc(file=sys.stdout)
        LOG.error('cimi: del_service_instance_by_id: Exception')
        return None


# del_all_service_instances: delete all service instances
def del_all_service_instances(obj_response_cimi=None):
    try:
        LOG.debug("cimi: del_all_service_instances: Deleting all  service instances ... ")

        service_instances = get_all_service_instances()
        for si in service_instances:
            LOG.info("cimi: del_all_service_instances: Deleting " + si['id'] + " ... ")
            resource_id = si['id'].replace('service-instance/', '')
            requests.delete(config.dic['CIMI_URL'] + '/service-instance/' + resource_id, headers=cimi_header, verify=False)
        return True
    except:
        traceback.print_exc(file=sys.stdout)
        LOG.error('cimi: del_all_service_instances: Exception')
        return False


# FUNCTION: add_service_instance: add resource to cimi
# RETURNS: resource
def add_service_instance(content):
    try:
        LOG.debug("cimi: add_service_instance: Adding new resource to service instances ... ")

        # complete map and update resource
        content.update(common_new_map_fields())

        res = requests.post(config.dic['CIMI_URL'] + '/service-instance', headers=cimi_header, verify=False, json=content)
        LOG.debug("res: " + str(res))
        if res.status_code == 201:
            id = res.json()['resource-id'].replace('service-instance/', '')
            return get_service_instance_by_id(id)

        LOG.error("cimi: add_service_instance: Request failed: " + res.status_code)
        LOG.error("cimi: add_service_instance: Response: " + str(res.json()))
        return None
    except:
        traceback.print_exc(file=sys.stdout)
        LOG.error('cimi: add_service_instance: Exception while adding new resource to service instances!')
        return None


# update_service_instance: updates a service_instance
def update_service_instance(resource_id, content):
    try:
        LOG.debug("cimi: update_service_instance: Updating resource [" + resource_id + "] ... ")
        resource_id = resource_id.replace('service-instance/', '')

        # complete map and update resource
        content.update(common_update_map_fields())

        res = requests.put(config.dic['CIMI_URL']  + '/service-instance/' + resource_id, headers=cimi_header, verify=False, json=content)
        if res.status_code == 200:
            return get_service_instance_by_id(resource_id)

        LOG.error("cimi: update_service_instance: Request failed: " + res.status_code)
        LOG.error("cimi: update_service_instance: Response: " + str(res.json()))
        return None
    except:
        traceback.print_exc(file=sys.stdout)
        LOG.error('cimi: update_service_instance: Exception')
        return None



