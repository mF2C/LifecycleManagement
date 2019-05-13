"""
Kubernetes adapter
This is being developed for the MF2C Project: http://www.mf2c-project.eu/

Copyright: Atos Research and Innovation, 2017.

This code is licensed under an Apache 2.0 license. Please, refer to the LICENSE.TXT file for more information

Created on 18 oct. 2018

@author: Roi Sucasas - ATOS
"""

import config
from lifecycle import common as common
from lifecycle.modules.apps.kubernetes import schemas as shemas
from lifecycle.logs import LOG
from lifecycle.common import OPERATION_START, OPERATION_STOP, OPERATION_TERMINATE, STATUS_ERROR, STATUS_WAITING, STATUS_TERMINATED
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
    LOG.debug("[lifecycle.modules.apps.kubernetes.adapter] [deploy_service] " + str(service) + ", " + str(agent))
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
                          json=shemas.genDeploymentDict(service['name']),
                          verify=config.dic['VERIFY_SSL'])

        # service
        r = requests.post(config.dic['K8S_PROXY'] + "/api/v1/namespaces/" + config.dic['K8S_NAMESPACE'] + "/services",
                          headers=headers,
                          json=shemas.genServiceDict(service['name']),
                          verify=config.dic['VERIFY_SSL'])

        # app name is stored in 'container_id' field
        agent['container_id'] = service['name']
        agent['status'] = STATUS_WAITING

    except:
        LOG.exception('[lifecycle.modules.apps.kubernetes.adapter] [deploy_service] Exception')
        return common.gen_response(500, 'Exception: deploy_service()', 'agent', str(agent), 'service', str(service))


###############################################################################
# OPERATIONS:

# operation_service: service operation (start, stop...)
def operation_service(agent, operation):
    LOG.debug("[lifecycle.modules.apps.kubernetes.adapter] [operation_service] [" + operation + "]: " + str(agent))
    try:
        if operation == OPERATION_TERMINATE or operation == OPERATION_STOP:
            # app name is stored in 'container_id' field
            # deployment
            r = requests.delete(config.dic['K8S_PROXY'] + "/apis/apps/v1/namespaces/" + config.dic['K8S_NAMESPACE'] + "/deployments/" + agent['container_id'],
                                json={},
                                verify=config.dic['VERIFY_SSL'])

            # service
            r = requests.delete(config.dic['K8S_PROXY'] + "/api/v1/namespaces/" + config.dic['K8S_NAMESPACE'] + "/services/serv_" + agent['container_id'],
                                json={},
                                verify=config.dic['VERIFY_SSL'])

            agent['status'] = STATUS_TERMINATED

        else:
            LOG.warning("[lifecycle.modules.apps.kubernetes.adapter] [operation_service] [" + operation + "]: " + str(agent) + ": operation not supported")

        # return status
        return agent['status']
    except:
        agent['status'] = STATUS_ERROR
        LOG.exception('[lifecycle.modules.apps.kubernetes.adapter] [operation_service] Exception. Returning STATUS_ERROR ...')
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
