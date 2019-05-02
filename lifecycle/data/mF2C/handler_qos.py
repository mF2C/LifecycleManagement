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
import lifecycle.modules.agent_decision as agent_decision
import lifecycle.data.mF2C.data as data_mf2c
import lifecycle.data.service_instance as data_service_instance
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

        if not 'num_agents' in notification and not 'service_instance_id' in notification:
            LOG.error("LIFECYCLE: QoS Notifications Handler module: thr: Service instance reconfiguration: 'num_agents' / 'service_instance_id' parameters not found in notification!")
        else:
            # get notification values
            service_instance_id = notification['service_instance_id']
            service_instance = data_mf2c.get_service_instance(service_instance_id)
            service = data_mf2c.get_service(service_instance['id'])
            current_num_agents = len(service_instance['agents']) #service['num_agents']
            new_num_agents = notification['num_agents']
            appId = data_service_instance.get_appid_from_master(service_instance)

            if not appId:
                LOG.error("LIFECYCLE: QoS Notifications Handler module: thr: Service instance reconfiguration: 'appId' not found in service_instance!")
                LOG.error("LIFECYCLE: QoS Notifications Handler module: thr: service_instance=" + str(service_instance))
            else:
                # ADD NEW RESOURCES TO COMPSs MASTER
                if new_num_agents > current_num_agents:
                    LOG.debug("LIFECYCLE: QoS Notifications Handler module: thr: Reconfiguring service instance: Adding more nodes to service instance (COMPSs) ...")
                    # Call to landscaper/recommender
                    available_agents_list = agent_decision.get_available_agents_resources(service) # ==> [{"agent_ip": "192.168.252.41"}, ...]
                    if len(available_agents_list) > 0:
                        LOG.debug("LIFECYCLE: QoS Notifications Handler module: thr: Reconfiguring service instance: Checking available resources ...")
                        for agent in available_agents_list:
                            # add new resources to master if agent does not belong to current execution
                            if not data_service_instance.is_agent_in_service_instance(service_instance, agent["agent_ip"]) and new_num_agents > current_num_agents:
                                if compss_adpt.add_resources_to_job(service_instance, appId, agent["agent_ip"]):
                                    current_num_agents = current_num_agents + 1
                                else:
                                    LOG.error("LIFECYCLE: QoS Notifications Handler module: thr: Reconfiguring service instance: Error adding new resources / 'appId' not found in service_instance!")
                    else:
                        LOG.error("LIFECYCLE: QoS Notifications Handler module: thr: Handling QoS notifications: available_agents_list is None or is empty ")

                # REMOVE RESOURCES FROM COMPSs MASTER
                elif new_num_agents < current_num_agents:
                    LOG.debug("LIFECYCLE: QoS Notifications Handler module: thr: Reconfiguring service instance: Removing nodes from service instance (COMPSs) ...")
                    for agent in service_instance['agents']:
                        # if agent is not the master, it can be removed
                        if not data_service_instance.is_master(agent) and new_num_agents < current_num_agents:
                            if compss_adpt.rem_resources_from_job(service_instance, appId, agent["agent_ip"]):
                                current_num_agents = current_num_agents - 1

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