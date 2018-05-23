"""
db: pydblite (https://pydblite.readthedocs.io)
This is being developed for the MF2C Project: http://www.mf2c-project.eu/

Copyright: Roi Sucasas Font, Atos Research and Innovation, 2017.

This code is licensed under an Apache 2.0 license. Please, refer to the LICENSE.TXT file for more information

Created on 09 feb. 2018

@author: Roi Sucasas - ATOS
"""

from lifecycle.utils.logs import LOG
from pydblite.pydblite import Base


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
    SERVICE_INSTANCES_LIST = []

    # SERVICE_INSTANCES DB
    # DB_SERVICE_INSTANCES = Base('SERVICE_INSTANCES', save_to_file=False)
    # create new base with field names
    # DB_SERVICE_INSTANCES.create('type', 'container_main', 'container_2')

except ValueError:
    LOG.error('Lifecycle-Management: db: Exception: Error while initializing db')


# get_elem_from_list:
def get_elem_from_list(container_main_id):
    for obj in SERVICE_INSTANCES_LIST:
        if obj['container_main'] == container_main_id:
            return obj
    return None


'''
# save_to_DB_SERVICE_INSTANCES
def save_to_DB_SERVICE_INSTANCES(type, container_main, container_2):
    DB_SERVICE_INSTANCES.insert(type=type, container_main=container_main, container_2=container_2)




# pydblite:
def pydblite():
    from pydblite.pydblite import Base
    db = Base('dummy', path="C://TMP/db_data") #save_to_file=False
    # create new base with field names
    db.create('name', 'age', 'size')
    # insert new record
    db.insert(name='homer', age=23, size=1.84)
    # records are dictionaries with a unique integer key __id__
    # simple selection by field value
    records = db(name="homer")
    # complex selection by list comprehension
    res = [r for r in db if 30 > r['age'] >= 18 and r['size'] < 2]
    print("res:", res)
    # delete a record or a list of records
    r = records[0]
    db.delete(r)

    list_of_records = []
    r = db.insert(name='homer', age=23, size=1.84)
    list_of_records.append(db[r])
    r = db.insert(name='marge', age=36, size=1.94)
    list_of_records.append(db[r])

    # or generator expression
    for r in (r for r in db if r['name'] in ('homer', 'marge')):
        # print "record:", r
        pass

    db.delete(list_of_records)

    rec_id = db.insert(name='Bart', age=15, size=1.34)
    record = db[rec_id]  # the record such that record['__id__'] == rec_id

    # delete a record by its id
    del db[rec_id]

    # create an index on a field
    db.create_index('age')
    # update
    rec_id = db.insert(name='Lisa', age=13, size=1.24)

    # direct access by id
    record = db[rec_id]

    db.update(record, age=24)
    # add and drop fields
    db.add_field('new_field', default=0)
    db.drop_field('name')
    # save changes on disk
    db.commit()
'''


'''
def main():
    pydblite()


if __name__ == "__main__":
    main()
'''