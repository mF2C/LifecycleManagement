"""
CIMI - Data management
This is being developed for the MF2C Project: http://www.mf2c-project.eu/

Copyright: Atos Research and Innovation, 2017.

This code is licensed under an Apache 2.0 license. Please, refer to the LICENSE.TXT file for more information

Created on 09 feb. 2018

@author: Roi Sucasas - ATOS
"""


import lifecycle.data.mF2C.data as data_mf2c
#import lifecycle.data.mF2C.mf2c as mf2c
#import lifecycle.data.standalone.data as data_standalone


'''
 Data managed by this component:
 SERVICE:
       {
           "name": "hello-world",
           "description": "Hello World Service",
           "resourceURI": "/hello-world",
           "exec": "hello-world",
           "exec_type": "docker",
           "exec_ports": ["8080", "8081"],
           "category": {
               "cpu": "low",
               "memory": "low",
               "storage": "low",
               "inclinometer": false,
               "temperature": false,
               "jammer": false,
               "location": false
           }
       }

 SERVICE INSTANCE:
   {
       ...
       "id": "",
       "user": "testuser",
       "service": "",
       "agreement": "",
       "status": "waiting",
       "agents": [
           {"agent": resource-link, "url": "192.168.1.31", "ports": [8081], "container_id": "10asd673f", "status": "waiting",
               "num_cpus": 3, "allow": true, "master_compss": true},
           {"agent": resource-link, "url": "192.168.1.34", "ports": [8081], "container_id": "99asd673f", "status": "waiting",
               "num_cpus": 2, "allow": true, "master_compss": false}
      ]
   }
'''


###############################################################################
# COMMON

# exist_user: check if 'user id' exists
def exist_user(user_id):
    return data_mf2c.exist_user(user_id)


# exist_device: check if 'device id' exists
def exist_device(device_id):
    return data_mf2c.exist_device(device_id)


###############################################################################
# USER MANAGEMENT
# get_um_profile: Get um_profile
def get_um_profile():
    return data_mf2c.get_um_profile()


# get_um_sharing_model: Get sharing_model
def get_um_sharing_model():
    return data_mf2c.get_um_sharing_model()


# set_um_profile:
# def set_um_profile(apps=0):
#     return data_mf2c.get_um_profile()

###############################################################################
# get_leader_ip: Get IP address from Leader
def get_leader_ip():
    return data_mf2c.get_leader_ip()


###############################################################################
# get_power: Get battery level
def get_power():
    return data_mf2c.get_power()


###############################################################################
# SERVICE
# get_service: Get service
def get_service(service_id):
    return data_mf2c.get_service(service_id)


###############################################################################
# SERVICE INSTANCE
# get_service_instance: Gets the service instance
def get_service_instance(service_instance_id, obj_response_cimi=None):
    return data_mf2c.get_service_instance(service_instance_id, obj_response_cimi)


# get_service_instance_report: Gets the service instance report
def get_service_instance_report(service_instance_id):
    return data_mf2c.get_service_instance_report(service_instance_id)


# get_all_service_instances: Gets all service instances
def get_all_service_instances(obj_response_cimi=None):
    return data_mf2c.get_all_service_instances(obj_response_cimi)


# del_service_instance: Deletes service instance
def del_service_instance(service_instance_id, obj_response_cimi=None):
    return data_mf2c.del_service_instance(service_instance_id, obj_response_cimi)


# del_all_service_instances: Deletes all service instances
def del_all_service_instances(obj_response_cimi=None):
    return data_mf2c.del_all_service_instances(obj_response_cimi)


# create_service_instance: Creates a new service instance
def create_service_instance(service, agents_list, user_id, agreement_id):
    return data_mf2c.create_service_instance(service, agents_list, user_id, agreement_id)


# update_service_instance: Updates a service instance
def update_service_instance(service_instance_id, service_instance):
    return data_mf2c.update_service_instance(service_instance_id, service_instance)