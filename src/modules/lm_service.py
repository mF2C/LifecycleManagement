"""
Service
This is being developed for the MF2C Project: http://www.mf2c-project.eu/

Copyright: Roi Sucasas Font, Atos Research and Innovation, 2017.

This code is licensed under an Apache 2.0 license. Please, refer to the LICENSE.TXT file for more information

Created on 27 sept. 2017

@author: Roi Sucasas - ATOS
"""


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
        # TODO

        # 1. RECOMMENDER -> RECIPE = GET_RECIPE (SERVICE)
        # The Lifecycle Management module calls the Recommender in order to get the optimal deployment configuration
        # to run the service

        # 2. LANDSCAPER -> RESOURCES = GET_RESOURCES (RECIPE)
        # Based on this optimal configuration returned by the Recommender, the Lifecycle module asks the Landscaper
        # for a list of resources that match this recommendation.
        #       2.a. If no resources were found, then the Lifecycle Management forwards the request (submit a service) upwards
        #       2.b. If there are available resources ...

        # 3. QoS PROVIDING -> RESOURCES = XXX (RESOURCES)

        # 4. USER MANAGEMENT -> RESOURCES = XXX (RESOURCES)

        # 5. process information and decide where to allocate resources

        # 6. DISTRIBUTED EXECUTION RUNTIME / COMPSS -> ALLOCATE (RESOURCES, SERVICE)
        # Call to COMPSs in order to allocate resources (Iteration 1)
        # Call to the Service Management in order to allocate resources (Iteration 2)

        # 7. SLA MANAGER -> INITIALIZES_SLA (SERVICE, RESOURCES)
        # The Lifecycle calls the SLA Management to initialize all the SLA processes.

        # 8. DISTRIBUTED EXECUTION RUNTIME / COMPSS -> EXECUTE (SERVICE)
        # The Lifecycle calls the Distributed Execution Runtime in order to start the execution of the service.

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
