"""
lm_db: pydblite (https://pydblite.readthedocs.io)
This is being developed for the MF2C Project: http://www.mf2c-project.eu/

Copyright: Roi Sucasas Font, Atos Research and Innovation, 2017.

This code is licensed under an Apache 2.0 license. Please, refer to the LICENSE.TXT file for more information

Created on 03 june 2019

@author: Roi Sucasas - ATOS
"""

import config
from lifecycle.logs import LOG
from pydblite.pydblite import Base


DB_LM_SERVICE_INSTANCES = None


# init: initialize elements
def init():
    global DB_LM_SERVICE_INSTANCES
    try:
        # DB_LM: LM DATABASE ("PHYSICAL DB")
        LOG.info('[lifecycle.data.app.lm_db] [init] Initializing DB_LM ...')
        DB_LM_SERVICE_INSTANCES = Base(config.dic['LM_WORKING_DIR_VOLUME'] + config.dic['DB_STANDALONE_MODE'] + "_service_instances")
        # create new base with field names
        if not DB_LM_SERVICE_INSTANCES.exists():
            DB_LM_SERVICE_INSTANCES.create('id', 'service_instance')
        else:
            DB_LM_SERVICE_INSTANCES.open()
    except:
        LOG.exception('[lifecycle.data.app.lm_db] [init] Exception: Error while initializing db components')


# print_records
def __print_records(db):
    LOG.debug('[lifecycle.data.app.lm_db] [__print_records] Retrieving records from db...')
    records = db()
    for r in records:
        LOG.debug("lm_db> " + str(r))


# save to DB_LM_SERVICE_INSTANCES
def db_si_save(id, service_instance):
    LOG.debug("[lifecycle.data.app.lm_db] [db_si_save] Saving record [" + id + "] ...")
    try:
        record = db_si_get(id)
        if record is None:
            DB_LM_SERVICE_INSTANCES.insert(id=id, service_instance=service_instance)
            # save changes on disk
            DB_LM_SERVICE_INSTANCES.commit()

            # debug DB
            __print_records(DB_LM_SERVICE_INSTANCES)
            return True
        else:
            LOG.warning('[lifecycle.data.app.lm_db] [db_si_save] Service Instance already added to DB')
            return False
    except:
        LOG.exception('[lifecycle.data.app.lm_db] [db_si_save] Exception')
        return False


# uopdate to DB_LM_SERVICE_INSTANCES
def db_si_update(id, service_instance):
    LOG.debug("[lifecycle.data.app.lm_db] [db_si_update] Updating record [" + id + "] ...")
    try:
        record = db_si_get(id)
        if record is not None:
            DB_LM_SERVICE_INSTANCES.insert(id=id, service_instance=service_instance)
            # save changes on disk
            DB_LM_SERVICE_INSTANCES.commit()

            # debug DB
            __print_records(DB_LM_SERVICE_INSTANCES)
            return True
        else:
            LOG.warning('[lifecycle.data.app.lm_db] [db_si_update] Service Instance not found')
            return False
    except:
        LOG.exception('[lifecycle.data.app.lm_db] [db_si_update] Exception')
        return False


# get from DB_LM_SERVICE_INSTANCES
def db_si_get(id):
    try:
        records = [r for r in DB_LM_SERVICE_INSTANCES if r['id'] == id]
        LOG.debug("[lifecycle.data.app.lm_db] [db_si_get] records: " + str(records))

        if len(records) >= 1:
            return records[0]['service_instance']
        else:
            LOG.warning('[lifecycle.data.app.lm_db] [db_si_get] No records found')
    except:
        LOG.exception('[lifecycle.data.app.lm_db] [db_si_get] Exception')
    return None


# get from DB_LM_SERVICE_INSTANCES
def db_si_getrecord(id):
    try:
        records = [r for r in DB_LM_SERVICE_INSTANCES if r['id'] == id]
        LOG.debug("[lifecycle.data.app.lm_db] [db_si_get] records: " + str(records))

        if len(records) >= 1:
            return records[0]
        else:
            LOG.warning('[lifecycle.data.app.lm_db] [db_si_get] No records found')
    except:
        LOG.exception('[lifecycle.data.app.lm_db] [db_si_get] Exception')
    return None


# get all from DB_LM_SERVICE_INSTANCES
def db_si_getall():
    try:
        records = DB_LM_SERVICE_INSTANCES()
        LOG.debug("[lifecycle.data.app.lm_db] [db_si_getall] Getting all records ... total=" + str(len(records)))

        if len(records) >= 1:
            list_of_records = []
            for r in records:
                list_of_records.append(r['service_instance'])
            return list_of_records
        else:
            LOG.warning('[lifecycle.data.app.lm_db] [db_si_getall] No records found')
    except:
        LOG.exception('[lifecycle.data.app.lm_db] [db_si_getall] Exception')
    return None


# del from DB_LM_SERVICE_INSTANCES
def db_si_del(id):
    try:
        record = db_si_getrecord(id)
        if record is not None:
            LOG.debug("[lifecycle.data.app.lm_db] [db_si_del] deleted records: " + str(DB_LM_SERVICE_INSTANCES.delete(record)))
            # save changes on disk
            DB_LM_SERVICE_INSTANCES.commit()
            return True
        else:
            LOG.warning('[lifecycle.data.app.lm_db] [db_si_del] Service Instance was not found in DB')
            return False
    except:
        LOG.exception('[lifecycle.data.app.lm_db] [db_si_del] Exception')
        return False
