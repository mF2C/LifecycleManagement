"""
SLAs' notifications handler
This is being developed for the MF2C Project: http://www.mf2c-project.eu/

Copyright: Roi Sucasas Font, Atos Research and Innovation, 2017.

This code is licensed under an Apache 2.0 license. Please, refer to the LICENSE.TXT file for more information

Created on 27 sept. 2017

@author: Roi Sucasas - ATOS
"""


from common.logs import LOG
import common.common as common
import threading
import time
import lifecycle.modules.agent_decision as agent_decision
import lifecycle.data.mF2C.data as data_mf2c
import lifecycle.modules.apps.compss.adapter as compss_adpt


###############################################################################
# QoS Notifications: handles qos enforcement notifications
#   {
#       "type": "qos_enforcement",
#       "data"
#           {
#               "user_id": "",
#               "device_id": "",
#               "service_instance_id": "",
#               "message": "",
#               "num_agents": ""
#           }
#   }


# thread
# notification = body['data']
def thr(notification):
    try:
        LOG.debug("LIFECYCLE: QoS Notifications Handler module: thr: Handling QoS notifications [" + str(notification) + "] ...")

        # TODO
        # get notification values
        service_instance_id = notification['service_instance_id']
        service_instance = data_mf2c.get_service_instance(service_instance_id)
        service = data_mf2c.get_service(service_instance['id'])
        new_num_agents = notification['num_agents']

        # ADD NEW RESOURCES TO COMPSs MASTER
        if new_num_agents > len(service_instance['agents']):
            LOG.debug("LIFECYCLE: QoS Notifications Handler module: thr: Reconfiguring service instance. Adding more resources to service instance (COMPSs) ...")

            # Call to landscaper/recommender
            available_agents_list = agent_decision.get_available_agents_resources(service)
            if len(available_agents_list) > 0:
                LOG.debug("LIFECYCLE: QoS Notifications Handler module: thr: Reconfiguring service instance. Checking available resources ...")
                # TODO
                # ...
                compss_adpt.add_resources_to_job(service_instance)
            else:
                LOG.error("LIFECYCLE: QoS Notifications Handler module: thr: Handling QoS notifications: available_agents_list is None or is empty ")

        # REMOVE RESOURCES FROM COMPSs MASTER
        elif new_num_agents < len(service_instance['agents']):
            LOG.debug("LIFECYCLE: QoS Notifications Handler module: thr: Reconfiguring service instance. Removing resources from service instance (COMPSs) ...")
            # TODO
            # ...
            compss_adpt.rem_resources_from_job(service_instance)

        LOG.debug("LIFECYCLE: QoS Notifications Handler module: thr: QoS notifications handled")
    except:
        LOG.exception('LIFECYCLE: QoS Notifications Handler module: thr: Exception')


# Handle QoS violations
def handle_qos_notification(notification):
    try:
        LOG.info("LIFECYCLE: QoS Notifications Handler module: handle_qos_notification: service_instance_id: notification: " + str(notification))

        # handle notification
        t = threading.Thread(target=thr, args=(notification,))
        t.start()

        return common.gen_response_ok('QoS Notification has been processed', 'notification', str(notification))
    except:
        LOG.exception('LIFECYCLE: QoS Notifications Handler module: handle_qos_notification: Exception')
        return common.gen_response(500, 'Exception', 'notification', str(notification))