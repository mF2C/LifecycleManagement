"""
db: pydblite (https://pydblite.readthedocs.io)
This is being developed for the MF2C Project: http://www.mf2c-project.eu/

Copyright: Roi Sucasas Font, Atos Research and Innovation, 2017.

This code is licensed under an Apache 2.0 license. Please, refer to the LICENSE.TXT file for more information

Created on 09 feb. 2018

@author: Roi Sucasas - ATOS
"""

from common.logs import LOG
from pydblite.pydblite import Base
import config


'''
SERVICE_INSTANCES_LIST = {
    {
        "type": "docker-compose", 
        "container_main": "",
        "container_2": ""
    }
}
'''


try:
    # SERVICE_INSTANCES_LIST
    # "MEMORY DB"
    LOG.info('LIFECYCLE: db: Initializing SERVICE_INSTANCES_LIST ...')
    SERVICE_INSTANCES_LIST = []

    # DB_DOCKER_PORTS: PORTS DATABASE for each of the Lifecycles / agents
    # "PHYSICAL DB"
    LOG.info('LIFECYCLE: db: Initializing DB_DOCKER_PORTS ...')
    DB_DOCKER_PORTS = Base(config.dic['DB_DOCKER_PORTS'])
    # create new base with field names
    if not DB_DOCKER_PORTS.exists():
        DB_DOCKER_PORTS.create('port', 'mapped_to')
    else:
        DB_DOCKER_PORTS.open()
        records = DB_DOCKER_PORTS()
except:
    LOG.error('LIFECYCLE: db: Exception: Error while initializing db components')


# get_elem_from_list:
def get_elem_from_list(container_main_id):
    for obj in SERVICE_INSTANCES_LIST:
        if obj['container_main'] == container_main_id:
            return obj
    return None


# print_records
def print_records(db):
    LOG.debug('LIFECYCLE: db: print_records: Retrieving records from db...')
    records = db()
    for r in records:
        LOG.debug("> " + str(r))


# save_to_DB_DOCKER_PORTS
def save_to_DB_DOCKER_PORTS(port, mapped_to):
    LOG.debug('LIFECYCLE: db: save_to_DB_DOCKER_PORTS: Saving record ...')
    try:
        record = get_from_DB_DOCKER_PORTS(port)
        if record is None:
            DB_DOCKER_PORTS.insert(port=port, mapped_to=mapped_to)
            # save changes on disk
            DB_DOCKER_PORTS.commit()

            # debug DB
            print_records(DB_DOCKER_PORTS)
            return True
        else:
            LOG.warning('LIFECYCLE: db: save_to_DB_DOCKER_PORTS: Port already added to DB')
            return False
    except:
        LOG.error('LIFECYCLE: db: save_to_DB_DOCKER_PORTS: Exception')
        return False


# get_from_DB_DOCKER_PORTS
def get_from_DB_DOCKER_PORTS(port):
    LOG.debug('LIFECYCLE: db: get_from_DB_DOCKER_PORTS: Getting record ...')
    try:
        # debug DB
        print_records(DB_DOCKER_PORTS)

        records = [r for r in DB_DOCKER_PORTS if r['port'] == port]
        LOG.debug("LIFECYCLE: db: get_from_DB_DOCKER_PORTS: records: " + str(records))

        #records = DB_DOCKER_PORTS(port=port)
        if len(records) >= 1:
            return records[0]
        else:
            LOG.warning('LIFECYCLE: db: get_from_DB_DOCKER_PORTS: No records found')
    except:
        LOG.error('LIFECYCLE: db: get_from_DB_DOCKER_PORTS: Exception')
    return None


# get_from_DB_DOCKER_PORTS
def get_COMPSs_port_DB_DOCKER_PORTS(lports):
    LOG.debug('LIFECYCLE: db: get_from_DB_DOCKER_PORTS: Getting record ...')
    try:
        # debug DB
        print_records(DB_DOCKER_PORTS)

        for p in lports:
            records = [r for r in DB_DOCKER_PORTS if r['port'] == p]
            LOG.debug("LIFECYCLE: db: get_COMPSs_port_DB_DOCKER_PORTS: records: " + str(records))

            if len(records) >= 1:
                if records[0]['mapped_to'] == config.dic['PORT_COMPSs']:
                    LOG.debug('LIFECYCLE: db: get_COMPSs_port_DB_DOCKER_PORTS: PORT_COMPSs: ' + str(records[0]['port']))
                    return records[0]['port']
    except:
        LOG.error('LIFECYCLE: db: get_COMPSs_port_DB_DOCKER_PORTS: Exception')

    LOG.error('LIFECYCLE: db: get_COMPSs_port_DB_DOCKER_PORTS: No COMPSs ports found in DB!')
    return config.dic['PORT_COMPSs']


# del_from_DB_DOCKER_PORTS
def del_from_DB_DOCKER_PORTS(port):
    LOG.debug('LIFECYCLE: db: get_from_DB_DOCKER_PORTS: Deleting record ...')
    try:
        record = get_from_DB_DOCKER_PORTS(port)
        if record is not None:
            LOG.debug("LIFECYCLE: db: del_from_DB_DOCKER_PORTS: deleted records: " + str(DB_DOCKER_PORTS.delete(record)))
            # save changes on disk
            DB_DOCKER_PORTS.commit()
            return True
        else:
            LOG.warning('LIFECYCLE: db: save_to_DB_DOCKER_PORTS: Port was not found in DB')
            return False
    except:
        LOG.error('LIFECYCLE: db: del_from_DB_DOCKER_PORTS: Exception')
        return False
