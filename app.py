#!/usr/bin/python3

"""
REST API
This is being developed for the MF2C Project: http://www.mf2c-project.eu/

Copyright: Roi Sucasas Font, Atos Research and Innovation, 2017.

This code is licensed under an Apache 2.0 license. Please, refer to the LICENSE.TXT file for more information

Created on 09 feb. 2018

@author: Roi Sucasas - ATOS
"""

import lifecycle.lifecycle as lifecycle
import lifecycle.operations as operations
import lifecycle.mF2C.handler_um as handler_um
import lifecycle.mF2C.handler_sla as handler_sla
import lifecycle.utils.init_config as init_config
import lifecycle.mF2C.mf2c as mf2c
import lifecycle.utils.common as common
import lifecycle.utils.auth as auth
from lifecycle import config
from lifecycle.utils.common import OPERATION_START, OPERATION_STOP, OPERATION_RESTART, OPERATION_TERMINATE, OPERATION_START_JOB
from lifecycle.utils.logs import LOG
from flask_cors import CORS
from flask import Flask, request, Response, json
from flask_restful import Resource, Api
from flask_restful_swagger import swagger


'''
REST API
    Routes:
    
        /api/v1/
            GET:    get rest api service status
        
        /api/v1/lifecycle/service-instance/<string:service_instance_id>
            GET:    get service instance / all service instances (from cimi)
            POST:   SLA / UM notifications
            
        /api/v1/lifecycle
            POST:   Submits a service; gets a service instance
            PUT:    starts / stops ... a service instance; start-job ... starts a job in COMPSs
            DELETE: terminates a service instance; deletes service instance (from cimi)

        /api/v1/lifecycle/service-instance-operations (agent operations)
            POST:   Submits a service in a mF2C agent
            PUT:    starts / stops ... a service in a mF2C agent; start-job
            DELETE: deletes a service in a mF2C agent
'''


try:
    init_config.init()

    # APP
    app = Flask(__name__)
    CORS(app)

    # API DOC
    api = swagger.docs(Api(app),
                       apiVersion='1.0.1',
                       api_spec_url=config.dic['API_DOC_URL'],
                       produces=["application/json", "text/html"],
                       swaggerVersion="1.2",
                       description='Lifecycle Management component REST API - mF2C',
                       basePath='http://localhost:' + str(config.dic['SERVER_PORT']),
                       resourcePath='/')
except ValueError:
    LOG.error('Lifecycle-Management: app: Exception: Error while initializing app / api')


'''
 API 'home' Route

    '/api/v1/'
    
        GET:    get rest api service status
'''
@app.route('/api/v1/', methods=['GET'])
# @auth.requires_auth # test basic auth
def default_route():
    data = {
        'app': 'Lifecycle Management Module REST API',
        'status': 'Running',
        'api_doc_json': 'https://localhost:' + str(config.dic['SERVER_PORT']) + config.dic['API_DOC_URL'],
        'api_doc_html': 'https://localhost:' + str(config.dic['SERVER_PORT']) + config.dic['API_DOC_URL'] + '.html#!/spec'
    }
    resp = Response(json.dumps(data), status=200, mimetype='application/json')
    return resp


'''
 Service route: status, service events handler

    '/api/v1/lifecycle/service-instance/<string:service_instance_id>'
    
        GET:    get service instance / all service instances (from cimi)
        POST:   SLA / UM notifications
'''
class Service(Resource):
    # GET: get service instance
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
        if service_instance_id == "all":
            return lifecycle.get_all()
        else:
            return lifecycle.get(service_instance_id)

    # POST: process warnings and notifications
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
        body = request.get_json()
        LOG.info('body: ' + str(body))
        if not body or 'type' not in body or 'data' not in body:
            LOG.error('Lifecycle-Management: REST API: post: Exception - parameter not found: type / data')
            return Response(json.dumps({'error': True, 'message': 'parameter not found: type / data'}),
                            status=406, content_type='application/json')
        else:
            if body['type'] == "sla_notification":
                return handler_sla.handle_sla_notification(service_instance_id, body['data'])
            elif body['type'] == "um_warning":
                return handler_um.handle_warning(service_instance_id, body['data'])
        LOG.error("Lifecycle-Management: REST API: post: type [" + body['type'] + "] not defined / implemented")
        return Response(json.dumps({'error': True, 'message': 'type not defined / implemented'}),
                        status=501, content_type='application/json')


api.add_resource(Service, '/api/v1/lifecycle/service-instance/<string:service_instance_id>')


'''
 ServiceLifecycle route: submit, terminate, operations (start, stop, pause...)
 
    '/api/v1/lifecycle'
    
        POST:       Submits a service; gets a service instance
        PUT:        starts / stops ... a service instance; start-job ... starts a job in COMPSs
        DELETE:     terminates a service instance; deletes service instance (from cimi)
'''
class ServiceLifecycle(Resource):
    # POST: Submits a service
    #   'data' from request -POST- (body) - content:
    #   {
    #       "service": {...},
    #       "service_id": "",
    #       "user_id": "",
    #       "operation": "stop"
    #   }
    @swagger.operation(
        summary="Submits a <b>service</b> (deployment phase)",
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
        data = request.get_json()
        if 'user_id' not in data or 'agreement_id' not in data:
            LOG.error('Lifecycle-Management: REST API: post: Exception - parameter not found: user_id / agreement_id')
            return Response(json.dumps({'error': True, 'message': 'parameter not found: user_id / agreement_id'}),
                            status=406, content_type='application/json')
        elif 'service' not in data and 'service_id' not in data:
            LOG.error('Lifecycle-Management: REST API: post: Exception - parameter not found: service / service_id')
            return Response(json.dumps({'error': True, 'message': 'parameter not found: service /  service_id'}),
                            status=406, content_type='application/json')

        if 'service' in data:
            service = data['service']
        elif common.is_standalone_mode():
            LOG.error("Lifecycle-Management: REST API: post: Exception - STANDALONE_MODE enabled: parameters are not valid: ")
            return Response(json.dumps({'error': True, 'message': 'STANDALONE_MODE enabled: parameters are not valid'}),
                            status=500, content_type='application/json')
        else:
            service = mf2c.service_management_get_service(data['service_id'])
            if service is None:
                LOG.error("Lifecycle-Management: REST API: post: Exception - service not found!")
                return Response(json.dumps({"error": True, "message": "service not found; [id=" + data['service_id'] + "]"}),
                                status=500, content_type='application/json')

        # submit function returns a json with the content of the 'service_instance'
        if 'agents_list' in data:
            # using a predefined list of agents:
            return lifecycle.submit_service_in_agents(service, data['user_id'], data['agreement_id'],
                                                      data['agents_list'], check_service=True)
        else:
            # using agent_decision module (landscaper, recommender...):
            return lifecycle.submit(service, data['user_id'], data['agreement_id'])

    # PUT: Starts / stops / restarts ... a service and returns a JSON object with the result / status of the operation.
    @swagger.operation(
        summary="start, stop, restart a <b>service instance</b> // start a <b>job</b>",
        notes="Available operations:<br/>"
              "<b>'start / stop / restart'</b> ... service instance operations<br/>"
              "<b>'start-job'</b> ... starts a job<br/><br/>"
              "Field 'parameters' is used only for starting a job in an agent.",
        produces=["application/json"],
        authorizations=[],
        parameters=[{
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
    def put(self):
        data = request.get_json()
        if 'service_instance_id' not in data or 'operation' not in data:
            LOG.error('Lifecycle-Management: REST API: put: Parameter not found: service_instance_id / operation')
            return Response(json.dumps({'error': True, 'message': 'parameter not found: service_instance_id / operation'}),
                            status=406, content_type='application/json')
        # operations
        if data['operation'] == OPERATION_START:
            return lifecycle.start(data['service_instance_id'])
        elif data['operation'] == OPERATION_STOP:
            return lifecycle.stop(data['service_instance_id'])
        elif data['operation'] == OPERATION_RESTART:
            return lifecycle.start(data['service_instance_id'])
        elif data['operation'] == OPERATION_START_JOB:
            if 'parameters' not in data:
                LOG.error('Lifecycle-Management: REST API: put: Parameter not found: parameters')
                return Response(json.dumps({'error': True, 'message': 'parameter not found: parameters'}),
                                status=406, content_type='application/json')
            return lifecycle.start_job(data)
        else:
            LOG.error('Lifecycle-Management: REST API: put: operation not defined / implemented')
            return Response(json.dumps({'error': True, 'message': 'operation not defined / implemented'}),
                            status=501, content_type='application/json')

    # DELETE: Terminate service, Deallocate service's resources
    @swagger.operation(
        summary="Terminates a service instance and deallocates the service's resources",
        notes="Terminates a service instance, and deallocates all the resources.",
        produces=["application/json"],
        authorizations=[],
        parameters=[{
            "name": "body",
            "description": "Parameters in JSON format.<br/>Example: <br/>"
                           "{\"service_instance_id\":\"2122f75b-4dd5-49f1-ac30-dda18e2e1e00\"}",
            "required": True,
            "paramType": "body",
            "type": "string"
        }],
        responseMessages=[{
            "code": 406,
            "message": "'service_instance_id' parameter not found"
        }, {
            "code": 500,
            "message": "Exception processing request"
        }])
    def delete(self):
        data = request.get_json()
        if 'service_instance_id' not in data:
            LOG.error('Lifecycle-Management: REST API: delete: Parameter not found: service_instance_id')
            return Response(json.dumps({'error': True, 'message': 'parameter not found: service_instance_id'}),
                            status=406, content_type='application/json')
        return lifecycle.terminate(data['service_instance_id'])


api.add_resource(ServiceLifecycle, '/api/v1/lifecycle')


'''
 ServiceLifecycleOperations route: deploy a service, start, stop, ...
    /api/v1/lifecycle/service-instance-operations (agent operations)
    
        POST:   Submits a service in a mF2C agent
        PUT:    starts / stops ... a service in a mF2C agent
        DELETE: deletes a service in a mF2C agent
'''
class ServiceLifecycleOperations(Resource):
    # POST: Submits a service in an agent
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
    def post(self):
        data = request.get_json()
        if 'service' not in data or 'agent' not in data:
            LOG.error('Lifecycle-Management: REST API: post: Exception - parameter not found: service / agent')
            return Response(json.dumps({'error': True, 'message': 'parameter not found: service /  agent'}),
                            status=406, content_type='application/json')
        return operations.deploy(data['service'], data['agent'])

    # PUT: Starts / stops / restarts ... a service in an agent, and returns a JSON object with the result / status of
    # the operation.
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
    def put(self):
        data = request.get_json()
        if 'operation' not in data or 'agent' not in data:
            LOG.error('Lifecycle-Management: REST API: put: Exception - parameter not found: agent / operation')
            return Response(
                json.dumps({'error': True, 'message': 'parameter not found: agent / operation'}),
                status=406, content_type='application/json')
        # operations
        if data['operation'] == OPERATION_START:
            return operations.start(data['agent'])
        elif data['operation'] == OPERATION_STOP:
            return operations.stop(data['agent'])
        elif data['operation'] == OPERATION_RESTART:
            return operations.start(data['agent'])
        elif data['operation'] == OPERATION_TERMINATE:
            return operations.terminate(data['agent'])
        else:
            LOG.error('Lifecycle-Management: REST API: put: operation not defined / implemented')
            return Response(json.dumps({'error': True, 'message': 'operation not defined / implemented'}),
                            status=501, content_type='application/json')


api.add_resource(ServiceLifecycleOperations, '/api/v1/lifecycle/service-instance-operations')


###############################################################################


def main():
    # START SERVER
    context = (config.dic['CERT_CRT'], config.dic['CERT_KEY'])
    app.run(host='0.0.0.0', port=config.dic['SERVER_PORT'], ssl_context=context, threaded=True, debug=config.dic['DEBUG'])


if __name__ == "__main__":
    main()