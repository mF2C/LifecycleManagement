"""
CIMI interface
This is being developed for the MF2C Project: http://www.mf2c-project.eu/

Copyright: Roi Sucasas Font, Atos Research and Innovation, 2017.

This code is licensed under an Apache 2.0 license. Please, refer to the LICENSE.TXT file for more information

Created on 27 sept. 2017

@author: Roi Sucasas - ATOS
"""


import sys, traceback
import requests
from lifecycle import config
from lifecycle.utils.logs import LOG
from slipstream.api import Api


# CIMI initialization
# API
api = None

# ACL
acl = {"owner":
           {"principal": "ADMIN",
            "type": "ROLE"},
       "rules": [{"principal": "ADMIN",
                  "type": "ROLE",
                  "right": "ALL"},
                 {"principal": "ANON",
                  "type": "ROLE",
                  "right": "ALL"}
                 ]}


# connect_to_cimi: CIMI initialization / api creation
def connect_to_cimi():
    global api
    try:
        # API
        LOG.info('Connecting UM to ' + config.dic['CIMI_URL'] + " ...")

        api = Api(config.dic['CIMI_URL'],
                  insecure=True,
                  cookie_file=config.dic['CIMI_COOKIES_PATH'],
                  login_creds={'username': config.dic['CIMI_USER'],
                               'password': config.dic['CIMI_PASSWORD']})

        LOG.info(str(api))

        # Login with username & password
        LOG.info(str(api.login({"href": "session-template/internal",
                                "username": config.dic['CIMI_USER'],
                                "password": config.dic['CIMI_PASSWORD']})))

        # test api
        resp = api.cimi_search('users')
        LOG.info('UM connected to ' + config.dic['CIMI_URL'] + ": total users: " + str(resp.count))
        return str(resp.count)

    except ValueError:
        traceback.print_exc(file=sys.stdout)
        LOG.error('ERROR')
        return -1


# common_map_fields: generates a map with time and acl values
def common_map_fields():
    default_map = {
        "created": "1964-08-25T10:00:00.0Z",
        "updated": "1964-08-25T10:00:00.0Z",
        "acl": acl
    }
    return default_map


# check if api object is initialized
def get_api():
    if api is None:
        connect_to_cimi()
    return api


###############################################################################


# get_user_by_id: get user by id
def get_user_by_id(user_id):
    try:
        resp = get_api().cimi_search("users", filter="id='" + user_id + "'")
        if resp.count == 1:
            return resp.json['users'][0] # dict
        else:
            LOG.warning("User not found [user_id=" + user_id + "]")
            return None
    except:
        traceback.print_exc(file=sys.stdout)
        LOG.error('Exception')
        return None


# get_service_instance_by_id: get service instance by id
def get_service_instance_by_id(id):
    try:
        resp = get_api().cimi_search("serviceinstances", filter="id='" + id + "'")
        if resp.count == 1:
            return resp.json['serviceinstances'][0] # dict
        else:
            LOG.warning("User not found [id=" + id + "]")
            return None
    except:
        traceback.print_exc(file=sys.stdout)
        LOG.error('Exception')
        return None


# get_all: get all resources
def get_all(resource_type):
    try:
        return get_api().cimi_search(resource_type)
    except:
        traceback.print_exc(file=sys.stdout)
        LOG.error('Exception')
        return None


# get_resource_by_id: get resource by id
def get_resource_by_id(resource_id):
    try:
        return get_api().cimi_get(resource_id)
    except:
        traceback.print_exc(file=sys.stdout)
        LOG.error('Exception')
        return None


# delete_resource: delete resource by id
def delete_resource(resource_id):
    try:
        return get_api().cimi_delete(resource_id)
    except:
        traceback.print_exc(file=sys.stdout)
        LOG.error('Exception')
        return None


# FUNCTION: add_resource: add resource to cimi
# RETURNS: resource
def add_resource(resource_name, content):
    try:
        LOG.debug("Adding new resource to [" + resource_name + "] ... ")

        # complete map and update resource
        content.update(common_map_fields())

        resp = get_api().cimi_add(resource_name, content)
        LOG.debug("resp:        " + str(resp.message))
        LOG.debug("resource-id: " + str(resp.json['resource-id']))

        return get_resource_by_id(resp.json['resource-id'])
    except:
        traceback.print_exc(file=sys.stdout)
        LOG.error('Exception')
        return None


# add_resource: add resource to cimi
def update_resource(resource_id, content):
    try:
        LOG.debug("Adding new resource to [" + resource_id + "] ... ")

        # complete map and update resource
        content.update(common_map_fields())

        resp = get_api().cimi_edit(resource_id, content)
        LOG.debug("resp: " + str(resp))
        LOG.debug("id: " + str(resp.id))

        return get_resource_by_id(resp.id)
    except:
        traceback.print_exc(file=sys.stdout)
        LOG.error('Exception')
        return None

