"""
Kubernetes adapter
This is being developed for the MF2C Project: http://www.mf2c-project.eu/

Copyright: Atos Research and Innovation, 2017.

This code is licensed under an Apache 2.0 license. Please, refer to the LICENSE.TXT file for more information

Created on 18 oct. 2018

@author: Roi Sucasas - ATOS
"""

import config
import common.common as common
import sys, traceback
from common.logs import LOG
from common.common import OPERATION_START, OPERATION_STOP, OPERATION_TERMINATE, STATUS_ERROR, STATUS_STARTED, STATUS_TERMINATED, STATUS_STOPPED
import requests


'''
 Data managed by this component:
-----------------------------------------------------------------------------------------------
 SERVICE INSTANCE:
   {
       ...
       "id": "",
       "user_id": "testuser",
       "service_id": "",
       "agreement_id": "",
       "status": "waiting",
       "agents": [
           {"agent": resource-link, "url": "192.168.1.31", "ports": [8081], "container_id": "10asd673f", "status": "waiting",
               "num_cpus": 3, "allow": true, "master_compss": false},
           {"agent": resource-link, "url": "192.168.1.34", "ports": [8081], "container_id": "99asd673f", "status": "waiting",
               "num_cpus": 2, "allow": true, "master_compss": false}
      ]
   }
   
    Agent example: {"agent": resource-link, "url": "192.168.1.31", "ports": {8081}, "container_id": "10asd673f", 
                    "status": "waiting", "num_cpus": 3, "allow": true, "master_compss": false}
-----------------------------------------------------------------------------------------------
'''


###############################################################################
# DEPLOYMENT:

# deploy_service:
# IN: service, agent
# OUT: status value
def deploy_service(service, agent):
    LOG.debug("Lifecycle-Management: K8s adapter: (1) deploy_service: " + str(service) + ", " + str(agent))
    try:

        '''
        :oauth-token (config/get-openshift-oauth-token) 
        :insecure? true
        :content-type :json
        :accept :json
        
        requests.post:
            :param auth: (optional) Auth tuple to enable Basic/Digest/Custom HTTP Auth.
            
            requests.get('https://api.github.com/user', auth=HTTPBasicAuth('user', 'pass'))
        '''
        headers = {'content-type': 'application/json'}
        # deployment
        r = requests.post(config.dic['K8S_PROXY'] + "/apis/apps/v1/namespaces/" + config.dic['K8S_NAMESPACE'] + "/deployments",
                          headers=headers,
                          json={},
                          verify=config.dic['VERIFY_SSL'])

        # service
        r = requests.post(config.dic['K8S_PROXY'] + "/api/v1/namespaces/" + config.dic['K8S_NAMESPACE'] + "/services",
                          headers=headers,
                          json={},
                          verify=config.dic['VERIFY_SSL'])

        agent['status'] = STATUS_STARTED

    except:
        traceback.print_exc(file=sys.stdout)
        LOG.error('Lifecycle-Management: K8s adapter: deploy_service: Exception')
        return common.gen_response(500, 'Exception: deploy_service()', 'agent', str(agent), 'service', str(service))


###############################################################################
# OPERATIONS:

# operation_service: service operation (start, stop...)
def operation_service(agent, operation):
    LOG.debug("Lifecycle-Management: K8s adapter: operation_service [" + operation + "]: " + str(agent))
    try:
        # load config
        #k8scfg.load_kube_config()

        if operation == OPERATION_START:
            # create deployment

            # create service

            agent['status'] = STATUS_STARTED

        elif operation == OPERATION_STOP:
            # create deployment

            # create service

            agent['status'] = STATUS_STOPPED

        elif operation == OPERATION_TERMINATE:
            # deployment
            r = requests.delete(config.dic['K8S_PROXY'] + "/apis/apps/v1/namespaces/" + config.dic['K8S_NAMESPACE'] + "/deployments/",
                              json={}, verify=config.dic['VERIFY_SSL'])

            # service
            r = requests.delete(config.dic['K8S_PROXY'] + "/api/v1/namespaces/" + config.dic['K8S_NAMESPACE'] + "/services/",
                              json={}, verify=config.dic['VERIFY_SSL'])

            agent['status'] = STATUS_TERMINATED

        # return status
        return agent['status']
    except:
        agent['status'] = STATUS_ERROR
        traceback.print_exc(file=sys.stdout)
        LOG.error('Lifecycle-Management: K8s adapter: operation_service: Exception')
        return STATUS_ERROR


# start_service_agent: Start service in agent
def start_service(agent):
    return operation_service(agent, OPERATION_START)


# stop_service_agent: Stop service / stop container
def stop_service(agent):
    return operation_service(agent, OPERATION_STOP)


# terminate_service_agent: Stop service / stop container
def terminate_service(agent):
    return operation_service(agent, OPERATION_TERMINATE)