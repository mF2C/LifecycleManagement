"""
Lifecycle Operations: start/stop/terminate operations in 'parallel' mode
This is being developed for the MF2C Project: http://www.mf2c-project.eu/

Copyright: Atos Research and Innovation, 2017.

This code is licensed under an Apache 2.0 license. Please, refer to the LICENSE.TXT file for more information

Created on 04 dic. 2018

@author: Roi Sucasas - ATOS
"""

import threading
from lifecycle.connectors import connector as connector
from lifecycle.modules import applications_adapter as apps_adapter
from lifecycle import common as common
from lifecycle.data import data_adapter as data_adapter
from lifecycle.logs import LOG
from lifecycle.common import OPERATION_START, OPERATION_STOP, OPERATION_TERMINATE, STATUS_ERROR, STATUS_STARTED, STATUS_STOPPED, \
    STATUS_TERMINATED, STATUS_UNKNOWN, STATUS_STARTING, STATUS_STOPPING, STATUS_TERMINATING, OPERATION_STOP_TERMINATE


# thr_operation_service_local: operation_service localhost
def thr_operation_service_local(operation, service, agent):
    try:
        LOG.debug("[lifecycle.operations] [thr_operation_service_local] service operation: " + operation + " (localhost)")

        if operation == OPERATION_START:
            LOG.debug("[lifecycle.operations] [thr_operation_service_local] start service locally: " + str(service) + ", agent: " + str(agent))
            apps_adapter.start_service_agent(service, agent)

        elif operation == OPERATION_STOP:
            LOG.debug("[lifecycle.operations] [thr_operation_service_local] stop service locally: " + str(service) + ", agent: " + str(agent))
            apps_adapter.stop_service_agent(service, agent)

        elif operation == OPERATION_TERMINATE:
            LOG.debug("[lifecycle.operations] [thr_operation_service_local] terminate service locally: " + str(service) + ", agent: " + str(agent))
            apps_adapter.terminate_service_agent(service, agent)

    except:
        LOG.exception("[lifecycle.operations] [thr_operation_service_local] Exception")


# thr_operation_service_remote: operation_service remote
def thr_operation_service_remote(operation, service, agent):
    try:
        LOG.debug("[lifecycle.operations] [thr_operation_service_remote] service operation: " + operation + " (remote)")

        if operation == OPERATION_START:
            LOG.debug("[lifecycle.operations] [thr_operation_service_remote] start service in remote agent")
            resp_start = connector.lifecycle_operation(service, agent, OPERATION_START)
            if resp_start is not None:
                agent['status'] = resp_start['status']
                LOG.debug("[lifecycle.operations] [thr_operation_service_remote] result (start service): [agent=" + str(agent) + "]")
            else:
                agent['status'] = STATUS_UNKNOWN
                LOG.error("[lifecycle.operations] [thr_operation_service_remote] result (start service): ERROR")

        elif operation == OPERATION_STOP:
            LOG.debug("[lifecycle.operations] [thr_operation_service_remote] stop service in remote agent")
            resp_stop = connector.lifecycle_operation(service, agent, OPERATION_STOP)
            if resp_stop is not None:
                agent['status'] = resp_stop['status']
                LOG.debug("[lifecycle.operations] [thr_operation_service_remote] result (stop service): [agent=" + str(agent) + "]")
            else:
                agent['status'] = STATUS_UNKNOWN
                LOG.error("[lifecycle.operations] [thr_operation_service_remote] result (stop service): ERROR")

        elif operation == OPERATION_TERMINATE:
            LOG.debug("[lifecycle.operations] [thr_operation_service_remote] terminate service in remote agent")
            resp_terminate = connector.lifecycle_operation(service, agent, OPERATION_TERMINATE)
            if resp_terminate is not None:
                agent['status'] = resp_terminate['status']
                LOG.debug("[lifecycle.operations] [thr_operation_service_remote] result (terminate service): [agent=" + str(agent) + "]")
            else:
                agent['status'] = STATUS_UNKNOWN
                LOG.error("[lifecycle.operations] [thr_operation_service_remote] result (terminate service): ERROR")

    except:
        LOG.exception("[lifecycle.operations] [thr_operation_service_remote]  Exception")


# thr_operation_service: start/stop/terminate service instance in agents
def __thr_operation_service(service_instance, operation):
    LOG.info("########################################################################################")
    LOG.info("######## OPERATION: " + operation + " SERVICE INSTANCE")
    LOG.debug("[lifecycle.operations] [__thr_operation_service] operation=" + operation + ", service_instance_id=" + service_instance['id'])
    try:
        # 1. get service
        service = data_adapter.get_service(service_instance['service'])
        LOG.debug("[lifecycle.operations] [__thr_operation_service] service: " + str(service))

        # 2. stop/start/terminate service in all agents
        thrs = []  # 1 thread per agent
        for agent in service_instance["agents"]:
            LOG.info("[lifecycle.operations] [__thr_operation_service] >>> AGENT >>> " + agent['url'] + " <<<")
            # LOCAL
            if agent['url'] == data_adapter.get_my_ip(): #common.get_local_ip():
                thrs.append(threading.Thread(target=thr_operation_service_local, args=(operation, service, agent,)))
            # REMOTE AGENT (call lifecycle from agent)
            elif common.check_ip(agent['url']):
                thrs.append(threading.Thread(target=thr_operation_service_remote, args=(operation, service, agent,)))
            # NOT FOUND / NOT CONNECTED
            else:
                agent['status'] = STATUS_ERROR
                LOG.error("[lifecycle.operations] [__thr_operation_service] agent [" + agent['url'] + "] cannot be reached")

        # start threads
        for x in thrs:
            x.start()

        # join / wait for threads before executing next tags
        for x in thrs:
            x.join()

        # 3. save / update / terminate service_instance
        LOG.debug("[lifecycle.operations] [__thr_operation_service] Updating service_instance [" + operation + "]: " + str(service_instance))
        if operation == OPERATION_START:
            service_instance['status'] = STATUS_STARTED
            data_adapter.update_service_instance(service_instance['id'], service_instance)          # cimi / db
            connector.sla_start_agreement(service_instance['agreement'])                            # sla

        elif operation == OPERATION_STOP:
            service_instance['status'] = STATUS_STOPPED
            data_adapter.update_service_instance(service_instance['id'], service_instance)          # cimi / db
            connector.sla_stop_agreement(service_instance['agreement'])                             # sla

        elif operation == OPERATION_TERMINATE:
            service_instance['status'] = STATUS_TERMINATED
            data_adapter.del_service_instance(service_instance['id'])                               # cimi / db
            connector.sla_terminate_agreement(service_instance['agreement'])                        # sla
    except:
        LOG.exception('[lifecycle.operations] [__thr_operation_service] Exception')


# __thr_stop_terminate_service: stop and terminate service instance in agents
def __thr_stop_terminate_service(service_instance):
    LOG.info("########################################################################################")
    LOG.info("######## OPERATION: STOP & TERMINATE SERVICE INSTANCE")
    LOG.debug("[lifecycle.operations] [__thr_stop_terminate_service] service_instance_id=" + service_instance['id'])
    try:
        # 1. get service
        service = data_adapter.get_service(service_instance['service'])
        LOG.debug("[lifecycle.operations] [__thr_stop_terminate_service] service: " + str(service))

        # 2. stop service in all agents
        LOG.debug("[lifecycle.operations] [__thr_stop_terminate_service] Stopping service instance ...")
        thrs = []  # 1 thread per agent
        for agent in service_instance["agents"]:
            LOG.info("[lifecycle.operations] [__thr_stop_terminate_service] >>> AGENT >>> " + agent['url'] + " <<<")
            # LOCAL
            if agent['url'] == data_adapter.get_my_ip(): #common.get_local_ip():
                thrs.append(threading.Thread(target=thr_operation_service_local, args=(OPERATION_STOP, service, agent,)))
            # REMOTE AGENT (call lifecycle from agent)
            elif common.check_ip(agent['url']):
                thrs.append(threading.Thread(target=thr_operation_service_remote, args=(OPERATION_STOP, service, agent,)))
            # NOT FOUND / NOT CONNECTED
            else:
                agent['status'] = STATUS_ERROR
                LOG.error("[lifecycle.operations] [__thr_stop_terminate_service] agent [" + agent['url'] + "] cannot be reached")

        # start threads
        for x in thrs:
            x.start()

        # join / wait for threads before executing next tags
        for x in thrs:
            x.join()

        # 3. terminate service in all agents
        LOG.debug("[lifecycle.operations] [__thr_stop_terminate_service] Terminating service instance ...")
        thrs = []  # 1 thread per agent
        for agent in service_instance["agents"]:
            LOG.info("[lifecycle.operations] [__thr_stop_terminate_service] >>> AGENT >>> " + agent['url'] + " <<<")
            # LOCAL
            if agent['url'] == data_adapter.get_my_ip():  # common.get_local_ip():
                thrs.append(threading.Thread(target=thr_operation_service_local, args=(OPERATION_TERMINATE, service, agent,)))
            # REMOTE AGENT (call lifecycle from agent)
            elif common.check_ip(agent['url']):
                thrs.append(
                    threading.Thread(target=thr_operation_service_remote, args=(OPERATION_TERMINATE, service, agent,)))
            # NOT FOUND / NOT CONNECTED
            else:
                agent['status'] = STATUS_ERROR
                LOG.error("[lifecycle.operations] [__thr_stop_terminate_service] agent [" + agent[
                    'url'] + "] cannot be reached")

        # start threads
        for x in thrs:
            x.start()

        # join / wait for threads before executing next tags
        for x in thrs:
            x.join()

        # 4. save / update / terminate service_instance
        LOG.debug("[lifecycle.operations] [__thr_stop_terminate_service] Updating service_instance [" + OPERATION_STOP_TERMINATE + "]: " + str(service_instance))
        service_instance['status'] = STATUS_TERMINATED
        data_adapter.del_service_instance(service_instance['id'])                               # cimi / db
        connector.sla_terminate_agreement(service_instance['agreement'])                        # sla
    except:
        LOG.exception('[lifecycle.operations] [__thr_stop_terminate_service] Exception')


# operation_service: start/stop/terminate service instance in agents
def operation_service(service_instance_id, operation):
    LOG.debug("[lifecycle.operations] [operation_service] operation=" + operation + ", service_instance_id=" + service_instance_id)
    try:
        # 1. get service_instance object
        service_instance = data_adapter.get_service_instance(service_instance_id)
        if service_instance is None or service_instance == -1:
            return common.gen_response(500, 'Error getting service instance object', 'service_instance_id', service_instance_id)

        if operation == OPERATION_STOP_TERMINATE:
            service_instance['status'] = STATUS_TERMINATING
            # execute thread
            t = threading.Thread(target=__thr_stop_terminate_service, args=(service_instance,))
            t.start()
        else:
            # submit operation thread
            if operation == OPERATION_START:
                service_instance['status'] = STATUS_STARTING
            elif operation == OPERATION_STOP:
                service_instance['status'] = STATUS_STOPPING
            elif operation == OPERATION_TERMINATE:
                service_instance['status'] = STATUS_TERMINATING
            # execute thread
            t = threading.Thread(target=__thr_operation_service, args=(service_instance, operation,))
            t.start()

        # response
        return common.gen_response_ok("Service " + operation + " operation is being processed ...", "service_instance", service_instance)
    except:
        LOG.exception('[lifecycle.operations] [operation_service] Exception')
        return common.gen_response(500, 'Exception', 'service_instance_id', service_instance_id)


# Service Operation: start (version 2: no access to external docker APIs / calls to other agent's lifecycle components)
def start(service_instance_id):
    return operation_service(service_instance_id, OPERATION_START)


# Service Operation: stop (version 2: no access to external docker APIs / calls to other agent's lifecycle components)
def stop(service_instance_id):
    return operation_service(service_instance_id, OPERATION_STOP)


# Terminate service, Deallocate service's resources
def terminate(service_instance_id):
    LOG.debug("[lifecycle.operations] [terminate] service_instance_id=" + service_instance_id)
    try:
        # 1. get service_instance object
        service_instance = data_adapter.get_service_instance(service_instance_id)
        if service_instance is None or service_instance == -1:
            return common.gen_response(500, 'Error getting service instance object', 'service_instance_id', service_instance_id)

        # 2. updates service instance status
        service_instance['status'] = STATUS_TERMINATING
        data_adapter.update_service_instance(service_instance_id, service_instance)

        # 3.1 service instance status = Stopped => stop and terminate
        if service_instance['status'] != "Stopped":
            return operation_service(service_instance_id, OPERATION_STOP_TERMINATE)
        # 3.2 terminate
        else:
            return operation_service(service_instance_id, OPERATION_TERMINATE)
    except:
        LOG.exception('[lifecycle.operations] [terminate] Exception')
        return common.gen_response(500, 'Exception', 'service_instance_id', service_instance_id)


# terminate_all
def terminate_all():
    if data_adapter.del_all_service_instances():
        # TODO stop and terminate containers
        return common.gen_response_ok('Terminate all services', 'result', 'True')
    else:
        return common.gen_response(500, 'Exception', 'result', 'False')


# Service Instance Operation: starts a job / app
def start_job(body, service_instance_id):
    LOG.info("########################################################################################")
    LOG.info("######## JOBS: START JOB")
    LOG.debug("[lifecycle.operations] [start_job] body=" + str(body))
    LOG.debug("[lifecycle.operations] [start_job] service_instance_id=" + service_instance_id)
    try:
        # service instance
        service_instance = data_adapter.get_service_instance(service_instance_id)
        if service_instance is None or service_instance == -1:
            return common.gen_response(500, 'Error getting service instance object', 'service_instance_id', service_instance_id)

        LOG.debug("[lifecycle.operations] [start_job] service_instance=" + str(service_instance))

        # start job in agent(s)
        if len(service_instance['agents']) == 1:
            res = apps_adapter.start_job_compss(service_instance, body)
        elif len(service_instance['agents']) >= 2:
            res = apps_adapter.start_job_compss_multiple_agents(service_instance, body)
        else:
            LOG.warning("[lifecycle.operations] [start_job] Execution supported in only 1 or more agents! agents size=" + str(len(service_instance['agents'])))
            res = None

        if res:
            return common.gen_response_ok('Start job', 'service_id', service_instance_id, 'res', res)
        else:
            return common.gen_response(500, 'Error when starting job', 'service_instance', str(service_instance))
    except:
        LOG.exception('[lifecycle.operations] [start_job] Exception')
        return common.gen_response(500, 'Exception', 'data', str(body))