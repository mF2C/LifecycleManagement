"""
Service
This is being developed for the MF2C Project: http://www.mf2c-project.eu/

Copyright: Roi Sucasas Font, Atos Research and Innovation, 2017.

This code is licensed under an Apache 2.0 license. Please, refer to the LICENSE.TXT file for more information

Created on 27 sept. 2017

@author: Roi Sucasas - ATOS
"""


import src.utils.common as common
import src.modules.dependencies as dependencies
from src.utils.logs import LOG


# Submit a service
def submit(service):
    LOG.info("Lifecycle-Management: Service module: Submit service: " + str(service))
    try:
        # TODO define SERVICE content
        # 1. get Service REQUEST - TODO: process data / content

        # 2. RECOMMENDER -> TODO: RECIPE = GET_RECIPE(SERVICE)
        # The Lifecycle Management module calls the Recommender in order to get the optimal deployment configuration
        # to run the service
        recipe = dependencies.get_recipe(service)

        # 3. LANDSCAPER -> TODO: RESOURCES = GET_RESOURCES(RECIPE)
        # Based on this optimal configuration returned by the Recommender, the Lifecycle module asks the Landscaper
        # for a list of resources that match this recommendation.
        resources = dependencies.get_resources(recipe)

        # If no resources were found, then the Lifecycle Management forwards the request (submit a service) upwards
        if not resources or len(resources) == 0:
            # TODO: forwards the request upwards
            LOG.info("Lifecycle-Management: Service module: Submit service: forwards the request upwards" + service)
        # If there are available resources ...
        else:
            # 4. QoS PROVIDING -> RESOURCES = XXX (RESOURCES) TODO: RESOURCES = GET_RESOURCES(RESOURCES)
            resources = dependencies.get_qos_resources(resources)

            # 5. USER MANAGEMENT -> TODO: RESOURCES = GET_RESOURCES(RESOURCES)
            resources = dependencies.get_um_resources(resources)

            # 6. process information and decide where to allocate resources
            # TODO: APPLY ONE OF THE FOLLOWING POLICIES
            #   1. Recommender = empty
            #   2. There are no resources available
            #   3. There are only some resources available

            # 7. DISTRIBUTED EXECUTION RUNTIME / COMPSS -> TODO: ALLOCATE(RESOURCES, SERVICE)
            # Call to COMPSs in order to allocate resources (Iteration 1)
            # Call to the Service Management in order to allocate resources (Iteration 2)
            res = dependencies.allocate(service, resources)

            # 8. SLA MANAGER -> TODO: INITIALIZES_SLA(SERVICE, RESOURCES)
            # The Lifecycle calls the SLA Management to initialize all the SLA processes.
            res = dependencies.initializes_sla(service, resources)

            # 9. DISTRIBUTED EXECUTION RUNTIME / COMPSS -> TODO: EXECUTE(SERVICE)
            # The Lifecycle calls the Distributed Execution Runtime in order to start the execution of the service.
            res = dependencies.execute(service, resources)

            # return
            return common.gen_response_ok('Service submitted', 'service', service)
    except:
        LOG.error('Lifecycle-Management: Service module: Submit service: Exception')
        return common.gen_response(500, 'Exception', 'service', service)


# Terminate service, Deallocate service's resources
def terminate(service_id):
    try:
        LOG.info("Lifecycle-Management: Service module: Terminate service: " + service_id)

        # TODO
        #...

        return common.gen_response_ok('Service terminated', 'service_id', service_id)
    except:
        LOG.error('Lifecycle-Management: Service module: terminate: Exception')
        return common.gen_response(500, 'Exception', 'service_id', service_id)


# Get service status
def get_status(service_id):
    try:
        LOG.info("Lifecycle-Management: Service module: Get service status: " + service_id)

        # TODO
        #...

        return common.gen_response_ok('Service status', 'service_id', service_id, 'status', 'Running')
    except:
        LOG.error('Lifecycle-Management: Service module: get_status: Exception')
        return common.gen_response(500, 'Exception', 'service_id', service_id)
