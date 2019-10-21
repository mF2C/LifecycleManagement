"""
SLAs' notifications handler
This is being developed for the MF2C Project: http://www.mf2c-project.eu/

Copyright: Roi Sucasas Font, Atos Research and Innovation, 2017.

This code is licensed under an Apache 2.0 license. Please, refer to the LICENSE.TXT file for more information

Created on 27 sept. 2017

@author: Roi Sucasas - ATOS
"""

import threading, time
from lifecycle.logs import LOG
from lifecycle import common as common
from lifecycle.modules import agent_decision as agent_decision
from lifecycle.data import data_adapter as data_adapter
from lifecycle.modules.apps.compss import adapter as compss_adpt
from lifecycle.connectors import connector as connector
from lifecycle.common import STATUS_CREATED_NOT_INITIALIZED


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


# List of service instances being processed
QoS_SERVICE_INSTANCES_LIST = []


# __deploy_COMPSs_in_agent
def __deploy_COMPSs_in_agent(service, service_instance, agent_ip):
    LOG.debug("[lifecycle.events.handler_qos] [__deploy_COMPSs_in_agent] Deploying COMPSs service [" + service_instance['id'] + "] in new agent  [" + agent_ip + "] ...")
    try:
        # 1. create NEW AGENT
        LOG.debug("[lifecycle.events.handler_qos] [__deploy_COMPSs_in_agent] Creating new service instance agent [" + agent_ip + "]")
        new_agent = {"device_id":     "-",
                     "app_type":      service['exec_type'],
                     "ports":         service['exec_ports'],
                     "url":           agent_ip,
                     "status":        STATUS_CREATED_NOT_INITIALIZED,
                     "compss_app_id": "-",
                     "allow":         True,
                     "container_id":  "-",
                     "master_compss": False,
                     "agent_param":   "not-defined"}

        # 2. DEPLOY COMPSs in NEW AGENT
        LOG.debug("[lifecycle.events.handler_qos] [__deploy_COMPSs_in_agent] allocate service in remote agent [" + new_agent['url'] + "]")
        resp_deploy = connector.lifecycle_deploy(service, service_instance, new_agent)
        if resp_deploy is not None:
            new_agent['status'] = resp_deploy['status']
            new_agent['container_id'] = resp_deploy['container_id']
            new_agent['ports'] = resp_deploy['ports']
            LOG.debug("[lifecycle.events.handler_qos] [__deploy_COMPSs_in_agent] allocate service in remote agent: [agent=" + str(new_agent) + "]")
            # executes / starts service
            resp_start = connector.lifecycle_operation(service, new_agent, "start")
            if resp_start is not None:
                new_agent['status'] = resp_start['status']
                LOG.debug("[lifecycle.events.handler_qos] [__deploy_COMPSs_in_agent] execute service in remote agent: [agent=" + str(new_agent) + "]")
                return True
        else:
            LOG.error("[lifecycle.events.handler_qos] [__deploy_COMPSs_in_agent] allocate service in remote agent: NOT DEPLOYED")
            new_agent['status'] = "not-deployed"
    except:
        LOG.exception("[lifecycle.events.handler_qos] [__deploy_COMPSs_in_agent] Exception. Returning False ...")
    return False


# thread
# notification = body['data']
def thr(notification):
    try:
        global QoS_SERVICE_INSTANCES_LIST

        LOG.debug("[lifecycle.events.handler_qos] [thr] Handling QoS notifications [" + str(notification) + "] ...")

        # get notification values
        service_instance_id = notification['service_instance_id']
        service_instance = data_adapter.get_service_instance(service_instance_id)
        service = data_adapter.get_service(service_instance['service'])
        current_num_agents = len(service_instance['agents']) #service['num_agents']
        new_num_agents = notification['num_agents']
        appId = data_adapter.serv_instance_get_appid_from_master(service_instance)

        if not appId:
            LOG.error("[lifecycle.events.handler_qos] [thr] Service instance reconfiguration: 'appId' not found in service_instance!")
            LOG.error("[lifecycle.events.handler_qos] [thr] service_instance=" + str(service_instance))
        else:
            # ADD NEW RESOURCES TO COMPSs MASTER
            if new_num_agents > current_num_agents:
                LOG.debug("[lifecycle.events.handler_qos] [thr] Reconfiguring service instance: Adding more nodes to service instance (COMPSs) ...")
                # Call to landscaper/recommender
                LOG.debug("[lifecycle.events.handler_qos] [thr] Getting list of available agents ...")
                available_agents_list = agent_decision.get_available_agents_resources(service) # ==> [{"agent_ip": "192.168.252.41"}, ...]
                LOG.debug("[lifecycle.events.handler_qos] [thr] List of available agents: " + str(available_agents_list))
                if len(available_agents_list) > 0:
                    LOG.debug("[lifecycle.events.handler_qos] [thr] Reconfiguring service instance: Checking available resources ...")
                    for agent in available_agents_list:
                        LOG.debug("[lifecycle.events.handler_qos] [thr]  - checking agent [" + str(agent) + "]")
                        # add new resources to master if agent does not belong to current execution
                        if not data_adapter.serv_instance_is_agent_in_service_instance(service_instance, agent["agent_ip"]) and new_num_agents > current_num_agents:
                            # DEPLOY
                            LOG.debug("[lifecycle.events.handler_qos] [thr] Deploying COMPSs in agent [" + str(agent) + "] ...")
                            if __deploy_COMPSs_in_agent(service, service_instance, agent["agent_ip"]):
                                # ADD TO COMPSs
                                LOG.debug("[lifecycle.events.handler_qos] [thr] Adding to COMPSs execution ...")
                                if compss_adpt.add_resources_to_job(service_instance, appId, agent["agent_ip"]):
                                    current_num_agents = current_num_agents + 1
                                else:
                                    LOG.error("[lifecycle.events.handler_qos] [thr] Reconfiguring service instance: Error adding new resources / 'appId' not found in service_instance!")
                else:
                    LOG.error("[lifecycle.events.handler_qos] [thr] Handling QoS notifications: available_agents_list is None or is empty ")

            # REMOVE RESOURCES FROM COMPSs MASTER
            elif new_num_agents < current_num_agents:
                LOG.debug("[lifecycle.events.handler_qos] [thr] Reconfiguring service instance: Removing nodes from service instance (COMPSs) ...")
                for agent in service_instance['agents']:
                    # if agent is not the master, it can be removed
                    if not data_adapter.serv_instance_is_master(agent) and new_num_agents < current_num_agents:
                        if compss_adpt.rem_resources_from_job(service_instance, appId, agent["agent_ip"]):
                            current_num_agents = current_num_agents - 1

        LOG.debug("[lifecycle.events.handler_qos] [thr] Waiting 60s to terminate process ...")
        time.sleep(60)

        LOG.debug("[lifecycle.events.handler_qos] [thr] Removing service instance id from QoS_SERVICE_INSTANCES_LIST ...")
        QoS_SERVICE_INSTANCES_LIST.remove(notification['service_instance_id'])

        LOG.debug("[lifecycle.events.handler_qos] [thr] QoS notifications handled")
    except:
        LOG.exception('[lifecycle.events.handler_qos] [thr] Exception')
        QoS_SERVICE_INSTANCES_LIST.remove(notification['service_instance_id'])


# __check_service_instance_id: check if service instance is still being processed
def __check_service_instance_id(service_instance_id):
    for sid in QoS_SERVICE_INSTANCES_LIST:
        if sid == service_instance_id:
            LOG.warning("[lifecycle.events.handler_qos] [__check_notification] service instance [" + service_instance_id + "] is being processed")
            return False
    LOG.debug("[lifecycle.events.handler_qos] [__check_notification] service instance [" + sid + "] is NOT being processed")
    return True


# Handle QoS violations
def handle_qos_notification(notification):
    try:
        global QoS_SERVICE_INSTANCES_LIST

        LOG.info("[lifecycle.events.handler_qos] [handle_qos_notification] service_instance_id: notification: " + str(notification))

        if not 'num_agents' in notification and not 'service_instance_id' in notification:
            LOG.error("[lifecycle.events.handler_qos] [handle_qos_notification] 'num_agents' / 'service_instance_id' parameters not found in notification!")
            return common.gen_response(406, 'Error', 'parameter num_agents / service_instance_id not found in qos notification', str(notification))

        # handle notification
        if __check_service_instance_id(notification['service_instance_id']):
            QoS_SERVICE_INSTANCES_LIST.append(notification['service_instance_id'])
            t = threading.Thread(target=thr, args=(notification,))
            t.start()
            return common.gen_response_ok('QoS Notification is being processed...', 'notification', str(notification))

        return common.gen_response_ok("QoS Notification was not processed: List of current service instances being processed: " + str(SERVICE_INSTANCES_LIST),
                                      "notification",
                                      str(notification))
    except:
        LOG.exception('[lifecycle.events.handler_qos] [handle_qos_notification] Exception')
        return common.gen_response(500, 'Exception', 'notification', str(notification))