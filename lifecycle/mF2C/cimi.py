"""
Interactions with other mF2C components
This is being developed for the MF2C Project: http://www.mf2c-project.eu/

Copyright: Roi Sucasas Font, Atos Research and Innovation, 2017.

This code is licensed under an Apache 2.0 license. Please, refer to the LICENSE.TXT file for more information

Created on 27 sept. 2017

@author: Roi Sucasas - ATOS
"""

from lifecycle import config
from lifecycle.utils.logs import LOG


# TODO CALL TO RECOMMENDER: get service's recipe
def get_recipe(service):
    try:
        LOG.info("Lifecycle-Management: Dependencies: get_recipe: " + str(service))
        LOG.warn("Lifecycle-Management: Dependencies: get_recipe not implemented ")
        """
        r = requests.get(config.dic['URL_PM_RECOMMENDER'], verify=config.dic['VERIFY_SSL'])
        if r.status_code == 200:
            LOG.debug('Lifecycle-Management: Dependencies: get_recipe: status_code=' + r.status_code + '; response: ' + r.text)
        else:
            LOG.error('Lifecycle-Management: Dependencies: get_recipe: Error: status_code=' + r.status_code)
        """
        return {}
    except:
        LOG.error('Lifecycle-Management: Dependencies: get_recipe: Exception')
        return {}


# TODO CALL TO LANDSCAPER: get available resources for a recipe
def get_resources(recipe):
    try:
        LOG.info("User-Management: Dependencies: get_resources: " + str(recipe))
        LOG.warn("Lifecycle-Management: Dependencies: get_resources not implemented ")
        """
        r = requests.get(config.dic['URL_PM_LANDSCAPER'], verify=config.dic['VERIFY_SSL'])
        if r.status_code == 200:
            LOG.debug('Lifecycle-Management: Dependencies: get_resources: status_code=' + r.status_code + '; response: ' + r.text)
        else:
            LOG.error('Lifecycle-Management: Dependencies: get_resources: Error: status_code=' + r.status_code)
        """
        return config.dic['AVAILABLE_AGENTS']
    except:
        LOG.error('Lifecycle-Management: Dependencies: get_resources: Exception')
        return {}


# TODO CALL TO QoS PROVIDING: get resources
def get_qos_resources(resources):
    try:
        LOG.info("User-Management: Dependencies: get_qos_resources: " + str(resources))
        LOG.warn("Lifecycle-Management: Dependencies: get_qos_resources not implemented ")
        """
        r = requests.get(config.dic['URL_AC_QoS_PROVIDING'], verify=config.dic['VERIFY_SSL'])
        if r.status_code == 200:
            LOG.debug('Lifecycle-Management: Dependencies: get_qos_resources: status_code=' + r.status_code + '; response: ' + r.text)
        else:
            LOG.error('Lifecycle-Management: Dependencies: get_qos_resources: Error: status_code=' + r.status_code)
        """
        return resources
    except:
        LOG.error('Lifecycle-Management: Dependencies: get_qos_resources: Exception')
        return {}


# TODO CALL TO User Management: get resources
def get_um_resources(resources):
    try:
        LOG.info("User-Management: Dependencies: get_um_resources: " + str(resources))
        LOG.warn("Lifecycle-Management: Dependencies: get_um_resources not implemented ")
        """
        r = requests.get(config.dic['URL_AC_USER_MANAGEMENT'], verify=config.dic['VERIFY_SSL'])
        if r.status_code == 200:
            LOG.debug('Lifecycle-Management: Dependencies: get_um_resources: status_code=' + r.status_code + '; response: ' + r.text)
        else:
            LOG.error('Lifecycle-Management: Dependencies: get_um_resources: Error: status_code=' + r.status_code)
        """
        return resources
    except:
        LOG.error('Lifecycle-Management: Dependencies: get_um_resources: Exception')
        return {}


# TODO CALL TO DISTRIBUTED EXECUTION RUNTIME / COMPSS: allocate
def allocate(service_instance, resources):
    try:
        LOG.info("User-Management: Dependencies: allocate: " + str(resources) + ", " + str(service_instance))
        LOG.warn("Lifecycle-Management: Dependencies: allocate not implemented ")
        """
        r = requests.get(config.dic['URL_PM_COMPSS_RUNTIME_ALLOC'], verify=config.dic['VERIFY_SSL'])
        if r.status_code == 200:
            LOG.debug('Lifecycle-Management: Dependencies: allocate: status_code=' + r.status_code + '; response: ' + r.text)
        else:
            LOG.error('Lifecycle-Management: Dependencies: allocate: Error: status_code=' + r.status_code)
        """
        return {}
    except:
        LOG.error('Lifecycle-Management: Dependencies: allocate: Exception')
        return {}


# TODO CALL TO SLA:
def initializes_sla(service_instance):
    try:
        LOG.info("User-Management: Dependencies: initializes_sla: " + str(service_instance))
        LOG.warn("Lifecycle-Management: Dependencies: initializes_sla not implemented ")
        """
        r = requests.get(config.dic['URL_PM_SLA_MANAGER'], verify=config.dic['VERIFY_SSL'])
        if r.status_code == 200:
            LOG.debug('Lifecycle-Management: Dependencies: initializes_sla: status_code=' + r.status_code + '; response: ' + r.text)
        else:
            LOG.error('Lifecycle-Management: Dependencies: initializes_sla: Error: status_code=' + r.status_code)
        """
        return True
    except:
        LOG.error('Lifecycle-Management: Dependencies: initializes_sla: Exception')
        return False


# TODO CALL TO DISTRIBUTED EXECUTION RUNTIME / COMPSS: execute
def execute(service, resources):
    try:
        LOG.info("User-Management: Dependencies: execute: " + str(resources) + ", " + str(service))
        LOG.warn("Lifecycle-Management: Dependencies: execute not implemented ")
        """
        r = requests.get(config.dic['URL_PM_COMPSS_RUNTIME_EXEC'], verify=config.dic['VERIFY_SSL'])
        if r.status_code == 200:
            LOG.debug('Lifecycle-Management: Dependencies: execute: status_code=' + r.status_code + '; response: ' + r.text)
        else:
            LOG.error('Lifecycle-Management: Dependencies: execute: Error: status_code=' + r.status_code)
        """
        return {}
    except:
        LOG.error('Lifecycle-Management: Dependencies: execute: Exception')
        return {}