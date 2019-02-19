"""
SLA adapter
This is being developed for the MF2C Project: http://www.mf2c-project.eu/

Copyright: Atos Research and Innovation, 2017.

This code is licensed under an Apache 2.0 license. Please, refer to the LICENSE.TXT file for more information

Created on 09 feb. 2018

@author: Roi Sucasas - ATOS
"""

import lifecycle.data.mF2C.mf2c as mf2c
from common.logs import LOG
import config


# initialize all the SLA processes
# IN:
#   - Service instance
#   - agreement id
def initializes_sla(service_instance, agreement_id):
    try:
        LOG.debug("LIFECYCLE: sla_adapter: initializes_sla #############################")
        LOG.debug("LIFECYCLE: sla_adapter: initializes_sla: " + str(service_instance) + ", " + str(agreement_id))

        if config.dic['STANDALONE_MODE'] == 'True' or config.dic['STANDALONE_MODE'] is None:
            LOG.warning("LIFECYCLE: sla_adapter: initializes_sla: STANDALONE_MODE enabled")
            return None

        else:
            return mf2c.sla_start_agreement(agreement_id)
    except:
        LOG.error('LIFECYCLE: sla_adapter: initializes_sla: Exception')
        return None


# stops_sla_agreement
# IN:
#   - Service instance
#   - agreement id
def stop_sla_agreement(service_instance, agreement_id):
    try:
        LOG.debug("LIFECYCLE: sla_adapter: stops_sla_agreement #############################")
        LOG.debug("LIFECYCLE: sla_adapter: stops_sla_agreement: " + str(service_instance) + ", " + str(agreement_id))

        if config.dic['STANDALONE_MODE'] == 'True' or config.dic['STANDALONE_MODE'] is None:
            LOG.warning("LIFECYCLE: sla_adapter: stop_sla_agreement: STANDALONE_MODE enabled")
            return None

        else:
            return mf2c.sla_stop_agreement(agreement_id)
    except:
        LOG.error('LIFECYCLE: sla_adapter: stops_sla_agreement: Exception')
        return None


# terminates_sla_agreement
# IN:
#   - Service instance
#   - agreement id
def terminate_sla_agreement(service_instance, agreement_id):
    try:
        LOG.debug("LIFECYCLE: sla_adapter: terminate_sla_agreement #############################")
        LOG.debug("LIFECYCLE: sla_adapter: terminate_sla_agreement: " + str(service_instance) + ", " + str(agreement_id))

        if config.dic['STANDALONE_MODE'] == 'True' or config.dic['STANDALONE_MODE'] is None:
            LOG.warning("LIFECYCLE: agent_decision: terminate_sla_agreement: STANDALONE_MODE enabled")
            return None

        else:
            # TODO terminate function is not ready (sla)
            return mf2c.sla_terminate_agreement(agreement_id)
    except:
        LOG.error('LIFECYCLE: sla_adapter: terminate_sla_agreement: Exception')
        return None
