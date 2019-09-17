"""
CIMI - Data management
This is being developed for the MF2C Project: http://www.mf2c-project.eu/

Copyright: Atos Research and Innovation, 2017.

This code is licensed under an Apache 2.0 license. Please, refer to the LICENSE.TXT file for more information

Created on 03 june 2019

@author: Roi Sucasas - ATOS
"""

from lifecycle.data.standalone import lm_db as lm_db
from lifecycle.data.standalone import service_instance as service_instance
from lifecycle.logs import LOG
import uuid


###############################################################################
# SERVICE INSTANCE
# get_service_instance: Get service instance
def get_service_instance(service_instance_id):
    LOG.debug("[lifecycle.data.standalone.data_interface] [get_service_instance] get_service_instance: " + service_instance_id)
    return lm_db.db_si_get(service_instance_id)


# get_service_instance: Get service instance
def get_service_instance_report(service_instance_id):
    LOG.debug("[lifecycle.data.standalone.data_interface] [get_service_instance_report] not implemented")
    return None


# get_all_service_instances: Get all service instances
def get_all_service_instances():
    LOG.debug("[lifecycle.data.standalone.data_interface] [get_all_service_instances] get_all_service_instances")
    return lm_db.db_si_getall()


# del_service_instance: Delete service instance
def del_service_instance(service_instance_id):
    LOG.debug("[lifecycle.data.standalone.data_interface] [del_service_instance] del_service_instance: " + service_instance_id)
    return lm_db.db_si_del(service_instance_id)


# create_service_instance: Creates a new service instance
def create_service_instance(service, agents_list, user_id, agreement_id):
    LOG.debug("[lifecycle.data.standalone.data_interface] [create_service_instance] Adding new resource to service instances [" +
              service['name'] + ", " + str(agents_list) + ", " + str(user_id) + ", " + str(agreement_id) + "] ...")

    new_service_instance = service_instance.new_service_instance(service, agents_list, user_id, agreement_id)

    LOG.debug("[lifecycle.data.mf2c.data_interface] [create_service_instance] adding service_intance to CIMI ...")
    id = service['name'].replace(" ", "") + "_" + str(uuid.uuid4())
    new_service_instance['id'] = id
    res = lm_db.db_si_save(id, new_service_instance)

    if not res:
        LOG.error("[lifecycle.data.standalone.data_interface] [create_service_instance] Error during the creation of the service_instance object")
        return new_service_instance
    return res


