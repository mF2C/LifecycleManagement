"""
SLA adapter
This is being developed for the MF2C Project: http://www.mf2c-project.eu/

Copyright: Atos Research and Innovation, 2017.

This code is licensed under an Apache 2.0 license. Please, refer to the LICENSE.TXT file for more information

Created on 09 feb. 2018

@author: Roi Sucasas - ATOS
"""

import lifecycle.mF2C.mf2c as mf2c
from lifecycle.utils.logs import LOG
from lifecycle import config


# initialize all the SLA processes
# IN:
#   - Service instance
#   - agreement id
def initializes_sla(service_instance, agreement_id):
    try:
        LOG.debug("Lifecycle-Management: sla_adapter: initializes_sla #############################")
        LOG.debug("Lifecycle-Management: sla_adapter: initializes_sla: " + str(service_instance) + ", " + str(agreement_id))

        if config.dic['STANDALONE_MODE'] or config.dic['STANDALONE_MODE'] == 'True':
            LOG.warning("Lifecycle-Management: agent_decision: select_agents: STANDALONE_MODE enabled")
            return None

        else:
            return mf2c.start_sla_agreement(agreement_id)
    except:
        LOG.error('Lifecycle-Management: sla_adapter: initializes_sla: Exception')
        return None


# stops_sla_agreement
# IN:
#   - Service instance
#   - agreement id
def stop_sla_agreement(service_instance, agreement_id):
    try:
        LOG.debug("Lifecycle-Management: sla_adapter: stops_sla_agreement #############################")
        LOG.warning("Lifecycle-Management: sla_adapter: stops_sla_agreement not implemented: " + str(service_instance) + ", " + str(agreement_id))

        return None
    except:
        LOG.error('Lifecycle-Management: sla_adapter: stops_sla_agreement: Exception')
        return None


# terminates_sla_agreement
# IN:
#   - Service instance
#   - agreement id
def terminate_sla_agreement(service_instance, agreement_id):
    try:
        LOG.debug("Lifecycle-Management: sla_adapter: terminates_sla_agreement #############################")
        LOG.warning("Lifecycle-Management: sla_adapter: terminates_sla_agreement not implemented: " + str(service_instance) + ", " + str(agreement_id))

        return None
    except:
        LOG.error('Lifecycle-Management: sla_adapter: terminates_sla_agreement: Exception')
        return None
