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
                /api/v2/lm/agent-config
                        GET:    get agent's lifecycle configuration: docker, docker-swarm, kubernetes, ...         
                /api/v2/lm/agent-info
                        GET:    get agent's lifecycle information: service_instances, ...
                /lm/service-instance/<string:service_instance_id>
                        GET:    get service instance / all service instances (from cimi)
                        POST:   SLA / UM notifications
                        PUT:    Starts / stops / restarts a service instance  //  starts a job in COMPSs
                        DELETE: terminates a service instance; deletes service instance (from cimi)
                /lm/service
                        POST:   Submits a service and gets a service instance (new version)
                /lm/service1 (deprecated)
                        POST:   Submits a service and gets a service instance (deprecated version)
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
                       description='mF2C - Lifecycle Management REST API',
                       basePath='http://localhost:' + str(config.dic['SERVER_PORT']),
                       resourcePath='/')
except ValueError:
    LOG.error('Lifecycle-Management: app: Exception: Error while initializing app / api')


'''
 API 'home' Route

    '/api/v2/'
    
        GET:    get rest api service status
'''
@app.route('/api/v2/', methods=['GET'])
def default_route():
    data = {
        'app': "Lifecycle Management REST API",
        'status': "Running",
        'api_doc_json': "http://" + config.dic['HOST_IP'] + ":" + str(config.dic['SERVER_PORT']) + config.dic['API_DOC_URL'],
        'api_doc_html': "http://" + config.dic['HOST_IP'] + ":" + str(config.dic['SERVER_PORT']) + config.dic['API_DOC_URL'] + ".html#!/spec"
    }
    resp = Response(json.dumps(data), status=200, mimetype='application/json')
    return resp


########################################################################################################################
### LIFECYCLE MANAGER
########################################################################################################################
'''
 Service instance route: status, service events handler

    '/api/v2/lm/agent-config'

        GET:    get agent's lifecycle configuration: docker, docker-swarm, kubernetes, ...
'''
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


'''
 Service instance route: status, service events handler

    '/api/v2/lm/agent-info'

        GET:    get agent's lifecycle information: service_instances, ...
'''
class InstanceInfo(Resource):
    # GET /api/v2/lm/agent-info
    @swagger.operation(
        summary="get agent's lifecycle information: service_instances, ...",
        notes="get agent's lifecycle information: service_instances, ...",
        produces=["application/json"],
        authorizations=[],
        parameters=[],
        responseMessages=[{
            "code": 500,
            "message": "Exception processing request"
        }])
    def get(self):
        return lm.getAgentInfo()

api.add_resource(InstanceInfo, '/api/v2/lm/agent-info')


'''
 Service instance route: status, service events handler

    '/api/v2/lm/service-instances/<string:service_instance_id>'
    
        GET:    get service instance / all service instances
        POST:   SLA / UM notifications
        PUT:    Starts / stops / restarts a service instance  //  starts a job in COMPSs
        DELETE: Terminate service, Deallocate service's resources
'''
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


    # POST: process warnings and notifications
    # POST /api/v2/lm/service-instance/<string:service_instance_id>
    @swagger.operation(
        summary="Process warnings and notifications",
        notes="Process warnings and notifications from other components.",
        produces=["application/json"],
        authorizations=[],
        parameters=[{
            "name": "service_instance_id",
            "description": "Service instance ID",
            "required": True,
            "paramType": "path",
            "type": "string"
            }, {
            "name": "body",
            "description": "Parameters in JSON format.<br/>Example: <br/>"
                           "{\"type\":\"sla_notification/um_warning\", <br/>\"data\":{}}",
            "required": True,
            "paramType": "body",
            "type": "string"
        }],
        responseMessages=[{
            "code": 406,
            "message": "'type' / 'data' parameter not found"
        }, {
            "code": 500,
            "message": "Exception processing request"
        }, {
            "code": 501,
            "message": "Operation not defined / implemented"
        }])
    def post(self, service_instance_id):
        return lm.postServiceInstanceEvent(request, service_instance_id)


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
            "description": "Parameters in JSON format.<br/>Example: <br/>"
                           "{<font color='blue'>\"service_instance_id\":</font>\"617f823c-43f6-4c1a-b482-5ca5cfd4ec93\",<br/>"
                           "<font color='blue'>\"operation\":</font>\"start/restart/stop\",<br/>"
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



'''
 Service route (deprecated): submits a service ==> service instance is created
 
    '/api/v2/lm/service1'
    
        POST:       Submits a service; gets a service instance

class Service(Resource):
    # POST: Submits a service
    # POST /api/v2/lm/service1
    @swagger.operation(
        summary="Submits a <b>service</b> (deployment phase) (deprecated)",
        notes="Submits a service and returns a json with the content of a service instance:<br/>"
              "<b>'exec_type'</b>='docker' ... deploy a docker image<br/>"
              "<b>'exec_type'</b>='docker-compose' ... deploy a docker compose service<br/>"
              "<b>'exec_type'</b>='compss' ... deploy a docker COMPSs image<br/>",
        produces=["application/json"],
        authorizations=[],
        parameters=[{
            "name": "body",
            "description": "Parameters in JSON format.<br/>Service example: <br/>"
                            "{\"service\": {<br/>"
                                 "\"id\": \"120f1ae12ca\",<br/>"
                                 "\"name\": \"compss-mf2c\",<br/>"
                                 "\"description\": \"Hello World Service\",<br/>"
                                 "\"resourceURI\": \"/hello-world\",<br/>"
                                 "\"exec\": \"mf2c/compss-mf2c:1.0\",<br/>"
                                 "\"exec_type\": \"compss\",<br/>"
                                 "\"category\": {<br/>"
                                     "\"cpu\": \"low\",<br/>"
                                     "\"memory\": \"low\",<br/>"
                                     "\"storage\": \"low\",<br/>"
                                     "\"inclinometer\": false,<br/>"
                                     "\"temperature\": false,<br/>"
                                     "\"jammer\": false,<br/>"
                                     "\"location\": false<br/>"
                                 "}},<br/>"
                            "\"service_id\": \"120f1ae12ca\",<br/>"
                            "\"user_id\": \"rsucasas\",<br/>"
                            "\"agreement_id\": \"sla_agreement/12932af0ef123\",<br/>"
                            "\"agents_list\": [{\"agent_ip\": \"192.168.252.41\", \"num_cpus\": 4, \"master_compss\": false},<br/>"
                                              "{\"agent_ip\": \"192.168.252.42\", \"num_cpus\": 2, \"master_compss\": true}] }",
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
        return lm.postService1(request)

api.add_resource(Service, '/api/v2/lm/service1')
'''

'''
 Service route (v2): submits a service ==> service instance is created
 
    '/api/v2/lm/service'
    
        POST:       Submits a service; gets a service instance
'''
class Service(Resource):
    # POST: Submits a service
    # POST /api/v2/lm/service
    @swagger.operation(
        summary="Submits a <b>service</b> (deployment phase) / <b>version 2</b>",
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
                           "\"service_id\": \"120f1ae12ca\",<br/>"
                           "\"user_id\": \"rsucasas\",<br/>"
                           "\"agreement_id\": \"sla_agreement/12932af0ef123\",<br/>"
                           "\"agents_list\": [{\"agent_ip\": \"192.168.252.41\", \"num_cpus\": 4, \"master_compss\": false}]<br/>}",
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


'''
 Service instance (only calls between LMs - LMs internal communication) route: deploy a service, start, stop, ...
 
    '/api/v2/lm/service-instance-int'
    
        POST:   Submits a service in a mF2C agent
        PUT:    starts / stops ... a service in a mF2C agent
'''
class ServiceInstanceInt(Resource):
    # POST: Submits a service in an agent
    # POST /api/v2/lm/service-instance-int
    '''
    @swagger.operation(
        summary="Submits a service in a mF2C agent",
        notes="Submits a service in a mF2C agent.",
        produces=["application/json"],
        authorizations=[],
        parameters=[{
            "name": "body",
            "description": "Parameters in JSON format.<br/>Service example: <br/>"
                            "{\"service\": {"
                                 "\"name\": \"app-compss\","
                                 "\"description\": \"app-compss Service\","
                                 "\"resourceURI\": \"/app-compss\","
                                 "\"exec\": \"mf2c/compss-mf2c:1.0\","
                                 "\"exec_type\": \"compss\","
                                 "\"category\": {"
                                     "\"cpu\": \"low\","
                                     "\"memory\": \"low\","
                                     "\"storage\": \"low\","
                                     "\"inclinometer\": false,"
                                     "\"temperature\": false,"
                                     "\"jammer\": false,"
                                     "\"location\": false"
                                 "}},"
                            "\"agent\": {"
                                "\"agent\": {\"href\": \"agent/asdasd\"},"
                                "\"url\": \"192.168.252.41\","
                                "\"ports\": [8080]," 
                                "\"container_id\": \"-\","
                                "\"status\": \"waiting\"," 
                                "\"num_cpus\": 1," 
                                "\"allow\": true,"
                                "\"master_compss\": false}"
                            "}",
            "required": True,
            "paramType": "body",
            "type": "string"
        }],
        responseMessages=[{
            "code": 406,
            "message": "'service' / 'agent' parameter not found"
        }, {
            "code": 500,
            "message": "Exception processing request"
        }])
    '''
    def post(self):
        return lm.postServiceInt(request)


    # PUT: Starts / stops / restarts ... a service in an agent, and returns a JSON object with the result / status of the operation.
    # PUT /api/v2/lm/service-instance-int
    '''
    @swagger.operation(
        summary="Starts / stops / restarts a <b>service instance</b> in a mF2C agent",
        notes="Available operations:<br/>"
              "<b>'start / stop / restart / terminate'</b> ... service instance operations<br/>",
        produces=["application/json"],
        authorizations=[],
        parameters=[{
            "name": "body",
            "description": "Parameters in JSON format.<br/>Service example: <br/>"
                           "{"
                               "<font color='blue'>\"operation\":</font> \"start\" ,<br/>"
                               "<font color='blue'>\"agent\":</font> {"
                                    "\"agent\": {\"href\": \"agent/asdasd\"},"
                                    "\"url\": \"192.168.252.41\","
                                    "\"ports\": [8080]," 
                                    "\"container_id\": \"-\","
                                    "\"status\": \"waiting\"," 
                                    "\"num_cpus\": 1," 
                                    "\"allow\": true,"
                                    "\"master_compss\": false}}",
            "required": True,
            "paramType": "body",
            "type": "string"
        }],
        responseMessages=[{
            "code": 406,
            "message": "('agent' / 'operation' / 'parameters') Parameter not found"
        }, {
            "code": 500,
            "message": "Exception processing request"
        }])
    '''
    def put(self):
        return lm.putServiceInt(request)

api.add_resource(ServiceInstanceInt, '/api/v2/lm/service-instance-int')


########################################################################################################################
# MAIN
def main():
    LOG.info("LIFECYCLE: Starting Lifecycle Management application [version=" + str(config.dic['VERSION']) + "] ...")
    LOG.info("LIFECYCLE: Swagger running on http://" + config.dic['HOST_IP'] + ":" + str(config.dic['SERVER_PORT']) + config.dic['API_DOC_URL'] + ".html")
    LOG.info("LIFECYCLE: REST API running on http://" + config.dic['HOST_IP'] + ":" + str(config.dic['SERVER_PORT']) + config.dic['API_DOC_URL'])
    # START (SSL) SERVER
    # context = (config.dic['CERT_CRT'], config.dic['CERT_KEY'])
    # app.run(host='0.0.0.0', port=config.dic['SERVER_PORT'], ssl_context=context, threaded=True, debug=False)

    #LOG.info("Checking User Management component ...")
    #lm.checkUserManagementComponent()

    # START SERVER
    app.run(host='0.0.0.0', port=config.dic['SERVER_PORT'], threaded=True, debug=False)


if __name__ == "__main__":
    main()