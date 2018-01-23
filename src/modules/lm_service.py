"""
Service
This is being developed for the MF2C Project: http://www.mf2c-project.eu/

Copyright: Roi Sucasas Font, Atos Research and Innovation, 2017.

This code is licensed under an Apache 2.0 license. Please, refer to the LICENSE.TXT file for more information

Created on 27 sept. 2017

@author: Roi Sucasas - ATOS
"""


import config
import requests
from src.utils import logs
from flask import Response, json, jsonify


# requests
# r = requests.get('https://api.github.com/user', auth=('user', 'pass'))
# if r.status_code == 200:
#    logs.info('1')
# else:
#    logs.error('Error (1): Service: submit: call to Recommender: status_code != 200')


# Submit a service
def submit(service):
    try:
        logs.info("Lifecycle-Management: Service module: Submit service: " + service)

        # TODO define SERVICE content

        # 1. RECOMMENDER -> RECIPE = GET_RECIPE (SERVICE)
        # The Lifecycle Management module calls the Recommender in order to get the optimal deployment configuration
        # to run the service
        # TODO: RECIPE = GET_RECIPE(SERVICE)
        r = requests.get(config.dic['URL_PM_RECOMMENDER'], verify=config.dic['VERIFY_SSL'])
        if r.status_code == 200:
            logs.debug('Lifecycle-Management: Service module: Submit service (1): status_code=' + r.status_code +
                       '; response: ' + r.text)
        else:
            logs.error('Lifecycle-Management: Service module: Submit service (1): Error: status_code=' + r.status_code)

        # 2. LANDSCAPER -> RESOURCES = GET_RESOURCES (RECIPE)
        # Based on this optimal configuration returned by the Recommender, the Lifecycle module asks the Landscaper
        # for a list of resources that match this recommendation.
        #       2.a. If no resources were found, then the Lifecycle Management forwards the request (submit a service) upwards
        #       2.b. If there are available resources ...
        # TODO: RESOURCES = GET_RESOURCES(RECIPE)
        r = requests.get(config.dic['URL_PM_LANDSCAPER'], verify=config.dic['VERIFY_SSL'])
        if r.status_code == 200:
            logs.debug('Lifecycle-Management: Service module: Submit service (2): status_code=' + r.status_code +
                       '; response: ' + r.text)
        else:
            logs.error('Lifecycle-Management: Service module: Submit service (2): Error: status_code=' + r.status_code)

        # 3. QoS PROVIDING -> RESOURCES = XXX (RESOURCES)
        # TODO: RESOURCES = GET_RESOURCES(RESOURCES)
        r = requests.get(config.dic['URL_AC_QoS_PROVIDING'], verify=config.dic['VERIFY_SSL'])

        # 4. USER MANAGEMENT -> RESOURCES = XXX (RESOURCES)
        # TODO: RESOURCES = GET_RESOURCES(RESOURCES)
        r = requests.get(config.dic['URL_AC_USER_MANAGEMENT'], verify=config.dic['VERIFY_SSL'])

        # 5. process information and decide where to allocate resources
        # TODO: APPLY ONE OF THE FOLLOWING POLICIES
        #   1. Recommender = empty
        #   2. There are no resources available
        #   3. There are only some resources available

        # 6. DISTRIBUTED EXECUTION RUNTIME / COMPSS -> ALLOCATE (RESOURCES, SERVICE)
        # Call to COMPSs in order to allocate resources (Iteration 1)
        # Call to the Service Management in order to allocate resources (Iteration 2)
        # TODO: ALLOCATE(RESOURCES, SERVICE)
        r = requests.get(config.dic['URL_PM_COMPSS_RUNTIME_ALLOC'], verify=config.dic['VERIFY_SSL'])

        # 7. SLA MANAGER -> INITIALIZES_SLA (SERVICE, RESOURCES)
        # The Lifecycle calls the SLA Management to initialize all the SLA processes.
        # TODO: INITIALIZES_SLA(SERVICE, RESOURCES)
        r = requests.get(config.dic['URL_PM_SLA_MANAGER'], verify=config.dic['VERIFY_SSL'])

        # 8. DISTRIBUTED EXECUTION RUNTIME / COMPSS -> EXECUTE (SERVICE)
        # The Lifecycle calls the Distributed Execution Runtime in order to start the execution of the service.
        # TODO: EXECUTE(SERVICE)
        r = requests.get(config.dic['URL_PM_COMPSS_RUNTIME_EXEC'], verify=config.dic['VERIFY_SSL'])

        # return
        return Response(jsonify({'Service': 'submit', 'service': service}), status=200, content_type='application/json')
    except:
        logs.error('Lifecycle-Management: Service module: submit: Exception')
        return Response(json.dumps({'error': True, 'message': 'Exception', 'service': service}),
                        status=500, content_type='application/json')


# Terminate service, Deallocate service's resources
def terminate(service_id):
    try:
        logs.info("Lifecycle-Management: Service module: Terminate service: " + service_id)

        # TODO
        #...

        # TEST
        return {'error': False, 'message': 'Service terminated', 'service_id': service_id}
    except:
        logs.error('Lifecycle-Management: Service module: terminate: Exception')
        return Response(json.dumps({'error': True, 'message': 'Exception', 'service_id': ''}),
                        status=500, content_type='application/json')


# Get service status
def get_status(service_id):
    try:
        logs.info("Lifecycle-Management: Service module: Get service status: " + service_id)

        # TODO
        #...

        # TEST
        return {'error': False, 'message': 'Service status', 'service_id': service_id, 'status':'Running'}
    except:
        logs.error('Lifecycle-Management: Service module: get_status: Exception')
        return Response(json.dumps({'error': True, 'message': 'Exception', 'service_id': ''}),
                        status=500, content_type='application/json')
