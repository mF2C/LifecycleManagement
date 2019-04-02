#!/usr/bin/python3

"""
USER MANAGEMENT MODULE & LIFECYCLE MANAGER - REST API
This is being developed for the MF2C Project: http://www.mf2c-project.eu/

Copyright: Roi Sucasas Font, Atos Research and Innovation, 2017.

This code is licensed under an Apache 2.0 license. Please, refer to the LICENSE.TXT file for more information

Created on 18 oct. 2018

@author: Roi Sucasas - ATOS
"""

import config as config
import app_funcs as lm
# lm
import lifecycle.init_config as lm_init_config
# common
from common.logs import LOG
# ext
from flask_cors import CORS
from flask import Flask, request, Response, json
from flask_restful import Resource, Api
from flask_restful_swagger import swagger


'''
REST API
    Routes:
        Root:
            /api/v2
                        GET:    get rest api service status
            Lifecycle:
                /lm
                        POST:   SLA / UM / QoS notifications
                        
                /lm/agent-config
                        GET:    get agent's lifecycle configuration: docker, docker-swarm, kubernetes, ...  
                        
                /lm/check-agent-um
                        GET:    checks if device can run more apps - UP & SM policies (from 'local' User Management module)      
                         
                /lm/agent-um
                        GET:    get agent's current user-profile and sharing-model (from 'local' User Management module)
                        PUT:    updates user-profile current number of applications running
                        
                /lm/service-instance/<string:service_instance_id>
                        GET:    get service instance / all service instances (from cimi)
                        PUT:    Starts / stops / restarts a service instance  //  starts a job in COMPSs
                        DELETE: terminates a service instance; deletes service instance (from cimi)
                        
                /api/v2/lm/service-instances/<string:service_instance_id>/report
                        GET:    get service instance report
                        
                /lm/service
                        POST:   Submits a service and gets a service instance (new version)

                /lm/service-instance-int 
                        POST:   Submits a service in a mF2C agent
                        PUT:    starts / stops ... a service in a mF2C agent; start-job
'''
try:
    lm_init_config.init()

    # APP
    app = Flask(__name__)
    CORS(app)

    # API DOC
    api = swagger.docs(Api(app),
                       apiVersion='1.0.1',
                       api_spec_url=config.dic['API_DOC_URL'],
                       produces=["application/json", "text/html"],
                       swaggerVersion="1.2",
                       description='mF2C - Lifecycle Management REST API - version ' + config.dic['VERSION'],
                       basePath='http://localhost:' + str(config.dic['SERVER_PORT']),
                       resourcePath='/')
except ValueError:
    LOG.error('LIFECYCLE: app: Exception: Error while initializing app / api')


########################################################################################################################
### LIFECYCLE MANAGER
########################################################################################################################
#
# API 'home' Route
#
#    '/api/v2/'
#
#        GET:    get rest api service status
#
@app.route('/api/v2/', methods=['GET'])
def default_route():
    data = {
        'app': "Lifecycle Management REST API", 'status': "Running", 'api_doc_json': "http://" + config.dic['HOST_IP'] + ":" + str(config.dic['SERVER_PORT']) + config.dic['API_DOC_URL'],
        'api_doc_html': "http://" + config.dic['HOST_IP'] + ":" + str(config.dic['SERVER_PORT']) + config.dic['API_DOC_URL'] + ".html#!/spec"
    }
    resp = Response(json.dumps(data), status=200, mimetype='application/json')
    return resp


#
# Service instance route: status, service events handler
#
#    '/api/v2/lm/agent-config'
#
#       GET:    get agent's lifecycle configuration: docker, docker-swarm, kubernetes, ...
#
class InstanceConfig(Resource):
    # GET /api/v2/lm/agent-config
    @swagger.operation(
        summary="get agent's lifecycle configuration: docker, docker-swarm, kubernetes, ...",
        notes="get agent's lifecycle configuration: docker, docker-swarm, kubernetes, ...",
        produces=["application/json"],
        authorizations=[],
        parameters=[],
        responseMessages=[{
            "code": 500,
            "message": "Exception processing request"
        }])
    def get(self):
        return lm.getAgentConfig()

api.add_resource(InstanceConfig, '/api/v2/lm/agent-config')


#
# Service instance route: status, service events handler
#
#    '/api/v2/lm/check-agent-um'
#
#         GET:    checks if device can run more apps - UP & SM policies (from 'local' User Management module)
#
class CheckAgentUM(Resource):
    # GET /api/v2/lm/check-agent-um
    @swagger.operation(
        summary="checks if device can run more apps - UP & SM policies (from 'local' User Management module)",
        notes="checks if device can run more apps - UP & SM policies (from 'local' User Management module)",
        produces=["application/json"],
        authorizations=[],
        parameters=[],
        responseMessages=[{
            "code": 500,
            "message": "Exception processing request"
        }])
    def get(self):
        return lm.getCheckAgentUMInfo()

api.add_resource(CheckAgentUM, '/api/v2/lm/check-agent-um')


#
# Service instance route: status, service events handler
#
#    '/api/v2/lm/agent-um'
#
#        GET:    get agent's current user-profile and sharing-model (from 'local' User Management module)
#        PUT:    updates user-profile current number of applications running
#
class AgentUM(Resource):
    # GET /api/v2/lm/agent-um
    @swagger.operation(
        summary="get agent's current user-profile and sharing-model (from 'local' User Management module)",
        notes="get agent's current user-profile and sharing-model (from 'local' User Management module)",
        produces=["application/json"],
        authorizations=[],
        parameters=[],
        responseMessages=[{
            "code": 500,
            "message": "Exception processing request"
        }])
    def get(self):
        return lm.getAgentUMInfo()


    # PUT /api/v2/lm/agent-um
    @swagger.operation(
        summary="updates user-profile current number of applications running",
        notes="updates user-profile current number of applications running",
        produces=["application/json"],
        authorizations=[],
        parameters=[{
            "name": "body",
            "description": "Parameters in JSON format.<br/>Example: <br/>"
                "{\"apps\":1}",
            "required": True,
            "paramType": "body",
            "type": "string"
        }],
        responseMessages=[{
            "code": 500, "message": "Exception processing request"
        }])
    def put(self):
        return lm.putAgentUMInfo(request)

api.add_resource(AgentUM, '/api/v2/lm/agent-um')


#
# Service instance route:
#
#     '/api/v2/lm/service-instances/<string:service_instance_id>'
#
#        GET:    get service instance / all service instances
#        PUT:    Starts / stops / restarts a service instance  //  starts a job in COMPSs
#        DELETE: Terminate service, Deallocate service's resources
#
class ServiceInstance(Resource):
    # GET: get service instance
    # GET /api/v2/lm/service-instance/<string:service_instance_id>
    @swagger.operation(
        summary="Get service instance",
        notes="Gets a (all) service instance(s)",
        produces=["application/json"],
        authorizations=[],
        parameters=[{
                "name": "service_instance_id",
                "description": "Service instance ID or 'all'.<br/>Example: <br/>b08ee389-36c0-45f0-8684-61baf6e03da8",
                "required": True,
                "paramType": "path",
                "type": "string"
            }],
        responseMessages=[{
                "code": 500,
                "message": "Exception processing request"
            }])
    def get(self, service_instance_id):
        return lm.getServiceInstance(service_instance_id)


    # PUT: Starts / stops / restarts ... a service and returns a JSON object with the result / status of the operation.
    #      start-job ... starts a job in COMPSs
    # PUT /api/v2/lm/service-instance/<string:service_instance_id>
    @swagger.operation(
        summary="start, stop, restart a <b>service instance</b> // start a <b>job</b>",
        notes="Available operations:<br/>"
              "<b>'start / stop / restart'</b> ... service instance operations<br/>"
              "<b>'start-job'</b> ... starts a job<br/><br/>"
              "Field 'parameters' is used only for starting a job in an agent.",
        produces=["application/json"],
        authorizations=[],
        parameters=[{
                "name": "service_instance_id",
                "description": "Service instance ID or 'all'.<br/>Example: <br/>b08ee389-36c0-45f0-8684-61baf6e03da8",
                "required": True,
                "paramType": "path",
                "type": "string"
            }, {
            "name": "body",
            "description": "Parameters in JSON format.<br/>Example 1: <br/>"
                           "{<br/><font color='blue'>\"operation\":</font>\"start/restart/stop\"<br/>}"
                           "<br/><br/>Example 2: <br/>"
                           "{<br/><font color='blue'>\"operation\":</font>\"start-job\",<br/>"
                           "<font color='blue'>\"parameters\":</font>\"&lt;ceiClass&gt;es.bsc.compss.test.TestItf&lt;/ceiClass&gt; "
                           "  &lt;className&gt;es.bsc.compss.test.Test&lt;/className&gt;"
                           "  &lt;methodName&gt;main&lt;/methodName&gt;"
                           "  &lt;parameters&gt;"
                           "    &lt;array paramId=\"0\"&gt;"
                           "      &lt;componentClassname&gt;java.lang.String&lt;/componentClassname&gt;"
                           "      &lt;values&gt;"
                           "        &lt;element paramId=\"0\"&gt;"
                           "          &lt;className&gt;java.lang.String&lt;/className&gt;"
                           "          &lt;value xmlns:xsi=\"http://www.w3.org/2001/XMLSchema-instance\" "
                           "             xmlns:xs=\"http://www.w3.org/2001/XMLSchema\" xsi:type=\"xs:string\"&gt;3&lt;/value&gt;"
                           "        &lt;/element&gt;"
                           "      &lt;/values&gt;"
                           "    &lt;/array&gt;"
                           "  &lt;/parameters&gt;\" <br/>}",
            "required": True,
            "paramType": "body",
            "type": "string"
        }],
        responseMessages=[{
            "code": 406,
            "message": "('service_instance_id' / 'operation' / 'parameters') Parameter not found"
        }, {
            "code": 500,
            "message": "Exception processing request"
        }])
    def put(self, service_instance_id):
        return lm.putServiceInstance(request, service_instance_id)


    # DELETE: Terminate service, Deallocate service's resources
    # DELETE /api/v2/lm/service-instance/<string:service_instance_id>
    @swagger.operation(
        summary="Terminates a service instance and deallocates the service's resources",
        notes="Terminates a service instance, and deallocates all the resources.",
        produces=["application/json"],
        authorizations=[],
        parameters=[{
                "name": "service_instance_id",
                "description": "Service instance ID or 'all'.<br/>Example: <br/>b08ee389-36c0-45f0-8684-61baf6e03da8",
                "required": True,
                "paramType": "path",
                "type": "string"
            }],
        responseMessages=[{
            "code": 406,
            "message": "'service_instance_id' parameter not found"
        }, {
            "code": 500,
            "message": "Exception processing request"
        }])
    def delete(self, service_instance_id):
        return lm.deleteServiceInstance(service_instance_id)

api.add_resource(ServiceInstance, '/api/v2/lm/service-instances/<string:service_instance_id>')


#
# Service instance route:
#
#     '/api/v2/lm/service-instances/<string:service_instance_id>/report'
#
#        GET:    get service instance report
#
class ServiceInstanceReport(Resource):
    # GET: get service instance report
    # GET /api/v2/lm/service-instance/<string:service_instance_id>/report
    @swagger.operation(
        summary="Returns the service instance operation report",
        notes="Gets the service instance operation report",
        produces=["application/json"],
        authorizations=[],
        parameters=[{
                "name": "service_instance_id",
                "description": "Service instance ID or 'all'.<br/>Example: <br/>b08ee389-36c0-45f0-8684-61baf6e03da8",
                "required": True,
                "paramType": "path",
                "type": "string"
            }],
        responseMessages=[{
                "code": 500,
                "message": "Exception processing request"
            }])
    def get(self, service_instance_id):
        return lm.getServiceInstanceReport(service_instance_id)

api.add_resource(ServiceInstanceReport, '/api/v2/lm/service-instances/<string:service_instance_id>/report')


#
#  Service route (v2): submits a service ==> service instance is created
#
#    '/api/v2/lm/service'
#
#        POST:       Submits a service; gets a service instance
#
class Service(Resource):
    # POST: Submits a service
    # POST /api/v2/lm/service
    @swagger.operation(
        summary="Submits a <b>service</b> (deployment phase)</b>",
        notes="Submits a service and returns a json with the content of a service instance:<br/>"
              "<b>'exec_type'</b>='docker' ... deploy a docker image<br/>"
              "<b>'exec_type'</b>='docker-compose' ... deploy a docker compose service<br/>"
              "<b>'exec_type'</b>='compss' ... deploy a docker COMPSs image<br/>",
        produces=["application/json"],
        authorizations=[],
        parameters=[{
            "name": "body",
            "description": "Parameters in JSON format.<br/>Service example: <br/>"
                           "{<br/>"
                           "\"service_id\": \"service/74dd7176-111e-412a-98ce-a6409d58b3ca\",<br/>"
                           "\"user_id\": \"user/testuser\",<br/>"
                           "\"agreement_id\": \"sla_agreement/12932af0ef123\"<br/>}",
            "required": True,
            "paramType": "body",
            "type": "string"
        }],
        responseMessages=[{
            "code": 406,
            "message": "'service_id' / 'service' / 'user_id' / agreement_id parameter not found"
        }, {
            "code": 500,
            "message": "Error processing request"
        }])
    def post(self):
        return lm.postService(request)

api.add_resource(Service, '/api/v2/lm/service')


#
#  Service instance (only calls between LMs - LMs internal communication) route: deploy a service, start, stop, ...
#
#     '/api/v2/lm/service-instance-int'
#
#        POST:   Submits a service in a mF2C agent
#        PUT:    starts / stops ... a service in a mF2C agent
#
class ServiceInstanceInt(Resource):
    # POST: Submits a service in an agent
    # POST /api/v2/lm/service-instance-int
    def post(self):
        return lm.postServiceInt(request)

    # PUT: Starts / stops / restarts ... a service in an agent, and returns a JSON object with the result / status of the operation.
    # PUT /api/v2/lm/service-instance-int
    def put(self):
        return lm.putServiceInt(request)

api.add_resource(ServiceInstanceInt, '/api/v2/lm/service-instance-int')


#
#  Service instance route: service events handler
#
#    '/api/v2/lm'
#
#        POST:   SLA / UM notifications
#
class LmEvents(Resource):
    # POST: process warnings and notifications
    # POST /api/v2/lm
    @swagger.operation(
        summary="Process warnings and notifications",
        notes="Process warnings and notifications from other components.",
        produces=["application/json"],
        authorizations=[],
        parameters=[{
            "name": "body",
            "description": "Parameters in JSON format.<br/>Example: <br/>"
                "{\"type\":\"sla_notification / um_warning / qos_enforcement\", <br/>\"data\":{}}",
            "required": True,
            "paramType": "body",
            "type": "string"
        }], responseMessages=[{
            "code": 406, "message": "'type' / 'data' parameter not found"
        }, {
            "code": 500, "message": "Exception processing request"
        }, {
            "code": 501, "message": "Operation not defined / implemented"
        }])
    def post(self):
        return lm.postServiceInstanceEvent(request)


api.add_resource(LmEvents, '/api/v2/lm')


########################################################################################################################
# MAIN
def main():
    LOG.info("LIFECYCLE: Starting Lifecycle Management application [version=" + str(config.dic['VERSION']) + "] ...")
    LOG.info("LIFECYCLE: Swagger running on http://" + config.dic['HOST_IP'] + ":" + str(config.dic['SERVER_PORT']) + config.dic['API_DOC_URL'] + ".html")
    LOG.info("LIFECYCLE: REST API running on http://" + config.dic['HOST_IP'] + ":" + str(config.dic['SERVER_PORT']) + config.dic['API_DOC_URL'])
    # START (SSL) SERVER
    # context = (config.dic['CERT_CRT'], config.dic['CERT_KEY'])
    # app.run(host='0.0.0.0', port=config.dic['SERVER_PORT'], ssl_context=context, threaded=True, debug=False)

    # START SERVER
    app.run(host='0.0.0.0', port=config.dic['SERVER_PORT'], threaded=True, debug=False)


if __name__ == "__main__":
    main()