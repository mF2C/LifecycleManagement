"""
Service operations
This is being developed for the MF2C Project: http://www.mf2c-project.eu/

Copyright: Roi Sucasas Font, Atos Research and Innovation, 2017.

This code is licensed under an Apache 2.0 license. Please, refer to the LICENSE.TXT file for more information

Created on 27 sept. 2017

@author: Roi Sucasas - ATOS
"""


from src.utils.logs import LOG
import src.utils.common as common


# Service Operation: start
def start(service_id):
    try:
        LOG.info("Lifecycle-Management: Service Operations module: start service: " + service_id)

        # TODO
        # ...

        return common.gen_response_ok('Service started', 'service_id', service_id)
    except:
        LOG.error('Lifecycle-Management: Service Operations module: start: Exception')
        return common.gen_response(500, 'Exception', 'service_id', service_id, 'service_id', service_id)


# Service Operation: restart
def restart(service_id):
    try:
        LOG.info("Lifecycle-Management: Service Operations module: restart service: " + service_id)

        # TODO
        # ...

        return common.gen_response_ok('Service restarted', 'service_id', service_id)
    except:
        LOG.error('Lifecycle-Management: Service Operations module: restart: Exception')
        return common.gen_response(500, 'Exception', 'service_id', service_id, 'service_id', service_id)


# Service Operation: stop
def stop(service_id):
    try:
        LOG.info("Lifecycle-Management: Service Operations module: stop service: " + service_id)

        # TODO
        # ...

        return common.gen_response_ok('Service stopped', 'service_id', service_id)
    except:
        LOG.error('Lifecycle-Management: Service Operations module: stop: Exception')
        return common.gen_response(500, 'Exception', 'service_id', service_id, 'service_id', service_id)
