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


# FUNCTION: create_sla_agreement: creates the SLA agreement
def create_sla_agreement(sla_template_id, user_id, service):
    if config.dic['STANDALONE_MODE'] == 'True' or config.dic['STANDALONE_MODE'] is None:
        LOG.warning("LIFECYCLE: sla_adapter: create_sla_agreement: STANDALONE_MODE enabled; Returning None ...")
        return None
    else:
        LOG.debug("LIFECYCLE: sla_adapter: create_sla_agreement: Creating a new SLA template [" + sla_template_id + ", " + user_id + "] " + " for service '" + service['name'] + "' ...")
        return mf2c.create_sla_agreement(sla_template_id, user_id, service)


# FUNCTION: start_sla_agreement: initialize all the SLA processes
def start_sla_agreement(service_instance, agreement_id):
    if config.dic['STANDALONE_MODE'] == 'True' or config.dic['STANDALONE_MODE'] is None:
        LOG.warning("LIFECYCLE: sla_adapter: start_sla_agreement: STANDALONE_MODE enabled; Returning None ...")
        return None
    else:
        LOG.debug("LIFECYCLE: sla_adapter: start_sla_agreement: Starting SLA (" + str(service_instance) + ", " + agreement_id + ") ...")
        return mf2c.sla_start_agreement(agreement_id)


# stops_sla_agreement
# IN:
#   - Service instance
#   - agreement id
def stop_sla_agreement(service_instance, agreement_id):
    if config.dic['STANDALONE_MODE'] == 'True' or config.dic['STANDALONE_MODE'] is None:
        LOG.warning("LIFECYCLE: sla_adapter: stop_sla_agreement: STANDALONE_MODE enabled; Returning None ...")
        return None
    else:
        LOG.debug("LIFECYCLE: sla_adapter: sla_stop_agreement: Stopping SLA (" + str(service_instance) + ", " + agreement_id + ") ...")
        return mf2c.sla_stop_agreement(agreement_id)


# terminates_sla_agreement
# IN:
#   - Service instance
#   - agreement id
def terminate_sla_agreement(service_instance, agreement_id):
    if config.dic['STANDALONE_MODE'] == 'True' or config.dic['STANDALONE_MODE'] is None:
        LOG.warning("LIFECYCLE: agent_decision: sla_terminate_agreement: STANDALONE_MODE enabled; Returning None ...")
        return None
    else:
        LOG.debug("LIFECYCLE: sla_adapter: sla_terminate_agreement: Terminating SLA (" + str(service_instance) + ", " + agreement_id + ") ...")
        return mf2c.sla_terminate_agreement(agreement_id)
