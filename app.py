"""
REST API
This is being developed for the MF2C Project: http://www.mf2c-project.eu/

Copyright: Roi Sucasas Font, Atos Research and Innovation, 2017.

This code is licensed under an Apache 2.0 license. Please, refer to the LICENSE.TXT file for more information

Created on 27 sept. 2017

@author: Roi Sucasas - ATOS
"""

#!/usr/bin/python3

import src.modules.lm_service_operations as lm_service_operations
import src.modules.lm_service as lm_service
import src.modules.lm_warnings_handler as lm_warnings_handler
import src.modules.lm_sla_handler as lm_sla_handler
import src.utils.logs as logs
import src.utils.auth as auth
import config
from flask_cors import CORS
from flask import Flask, request, Response, json
from flask_restful import Resource, Api
from flask_restful_swagger import swagger


try:
    # CONFIGURATION values
    logs.info('[SERVER_PORT=' + str(config.dic['SERVER_PORT']) + ']')
    logs.info('[API_DOC_URL=' + config.dic['API_DOC_URL'] + ']')
    logs.info('[CERT_CRT=' + config.dic['CERT_CRT'] + ']')
    logs.info('[CERT_KEY=' + config.dic['CERT_KEY'] + ']')
    logs.info('[DEBUG=' + str(config.dic['DEBUG']) + ']')

    # CIMI URL
    CIMI_API_ENV_NAME = "CIMI_API"
    CIMI_API_ENV_VALUE = "http://...."

    # APP
    app = Flask(__name__)
    CORS(app)

    # API DOC
    api = swagger.docs(Api(app),
                       apiVersion='1.0',
                       api_spec_url=config.dic['API_DOC_URL'],
                       produces=["application/json", "text/html"],
                       swaggerVersion="1.2",
                       description='Lifecycle Management component REST API - mF2C',
                       basePath='http://localhost:' + str(config.dic['SERVER_PORT']),
                       resourcePath='/')
except ValueError:
    logs.error('ERROR')


###############################################################################
## API Route
###############################################################################
@app.route('/api/v1/', methods=['GET'])
@auth.requires_auth # test basic auth
def default_route():
    data = {
        'app': 'Lifecycle Management Module REST API',
        'status': 'Running',
        'api_doc_json': 'https://localhost:' + str(config.dic['SERVER_PORT']) + config.dic['API_DOC_URL'],
        'api_doc_html': 'https://localhost:' + str(config.dic['SERVER_PORT']) + config.dic['API_DOC_URL'] + '.html#!/spec'
    }
    resp = Response(json.dumps(data), status=200, mimetype='application/json')
    return resp


###############################################################################
# Service route: status, service events handler
#
# Warnings Handler: handle warnings coming from User Management Assessment:
#   {
#       "type": "um_warning",
#       "data"
#           {
#               "user_id": "",
#               "device_id": "",
#               "service_id": "",
#               "warning_id": "",
#               "warning_txt": ""
#           }
#   }
#
# SLA Notifications: handle warnings coming from User Management Assessment
#   {
#       "type": "sla_notification",
#       "data"
#           {
#               "user_id": "",
#               "device_id": "",
#               "service_id": "",
#               "warning_id": "",
#               "warning_txt": ""
#           }
#   }
class Service(Resource):
    # GET: get service status
    @swagger.operation(
        summary="Get service status",
        notes="Gets the status of a service",
        produces=["application/json"],
        authorizations=[],
        parameters=[{
                "name": "service_id",
                "description": "Service ID",
                "required": True,
                "paramType": "path",
                "type": "string"
            }],
        responseMessages=[{
                "code": 500,
                "message": "Exception processing request"
            }])
    def get(self, service_id):
        return lm_service.get_status(service_id)

    # POST: process warnings and notifications
    @swagger.operation(
        summary="Process warnings and notifications",
        notes="Process warnings and notifications from other components.",
        produces=["application/json"],
        authorizations=[],
        parameters=[{
            "name": "service_id",
            "description": "Service ID",
            "required": True,
            "paramType": "path",
            "type": "string"
            }, {
            "name": "body",
            "description": "Parameters in JSON format.<br/>Example: <br/>"
                           "{\"type\":\"sla_notification/um_warning\", \"data\":{}}",
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
    def post(self, service_id):
        data = request.get_json()
        if 'type' not in data or 'data' not in data:
            logs.error('Lifecycle-Management: Service: post: Exception - parameter not found: type / data')
            return Response(json.dumps({'error': True, 'message': 'parameter not found: type / data'}),
                            status=406, content_type='application/json')
        else:
            if data['type'] == "sla_notification":
                return lm_sla_handler.handle_sla_notification(service_id, data['data'])
            elif data['type'] == "um_warning":
                return lm_warnings_handler.handle_warning(service_id, data['data'])
        logs.error('Lifecycle-Management: Service: post: type not defined / implemented')
        return Response(json.dumps({'error': True, 'message': 'type not defined / implemented'}),
                        status=501, content_type='application/json')


api.add_resource(Service, '/api/v1/lifecycle/<string:service_id>')


###############################################################################
# ServiceLifecycle route: submit, terminate, operations (start, stop, pause...)
# 'data' from request (body) - content:
#   {
#       "service": {},
#       "service_id": "",
#       "operation": "stop"
#   }
###############################################################################
class ServiceLifecycle(Resource):
    # POST: Submits a service
    @swagger.operation(
        summary="Submits a service ",
        notes="Submits a service.",
        produces=["application/json"],
        authorizations=[],
        parameters=[{
            "name": "body",
            "description": "Parameters in JSON format.<br/>Example: <br/>"
                           "{\"service\":{...}}",
            "required": True,
            "paramType": "body",
            "type": "string"
        }],
        responseMessages=[{
            "code": 406,
            "message": "'service' parameter not found"
        }, {
            "code": 500,
            "message": "Exception processing request"
        }])
    def post(self):
        data = request.get_json()
        if 'service' not in data:
            logs.error('Lifecycle-Management: ServiceLifecycle: post: Exception - parameter not found: service')
            return Response(json.dumps({'error': True, 'message': 'parameter not found: service'}),
                            status=406, content_type='application/json')
        return lm_service.submit(data['service'])

    # PUT: Starts / stops / restarts ... a service and returns a JSON object with the result / status of the operation.
    @swagger.operation(
        summary="Starts / stops / restarts a service ",
        notes="Starts / stops / restarts a service.",
        produces=["application/json"],
        authorizations=[],
        parameters=[{
            "name": "body",
            "description": "Parameters in JSON format.<br/>Example: <br/>"
                           "{\"service_id\":\"...\", \"operation\":\"start/restart/stop\"}",
            "required": True,
            "paramType": "body",
            "type": "string"
        }],
        responseMessages=[{
            "code": 406,
            "message": "'service_id' / 'operation' parameter not found"
        }, {
            "code": 500,
            "message": "Exception processing request"
        }])
    def put(self):
        data = request.get_json()
        if 'service_id' not in data or 'operation' not in data:
            logs.error('Lifecycle-Management: ServiceLifecycle: put: Exception - parameter not found: service_id / operation')
            return Response(json.dumps({'error': True, 'message': 'parameter not found: service_id / operation'}),
                            status=406, content_type='application/json')
        # operations
        if data['operation'] == 'start':
            return lm_service_operations.start(data['service_id'])
        elif data['operation'] == 'stop':
            return lm_service_operations.stop(data['service_id'])
        elif data['operation'] == 'restart':
            return lm_service_operations.restart(data['service_id'])
        else:
            logs.error('Lifecycle-Management: ServiceLifecycle: put: operation not defined / implemented')
            return Response(json.dumps({'error': True, 'message': 'operation not defined / implemented'}),
                            status=501, content_type='application/json')

    # DELETE: Terminate service, Deallocate service's resources
    @swagger.operation(
        summary="Terminates a service and deallocates the service's resources",
        notes="Terminate service, Deallocate service's resources.",
        produces=["application/json"],
        authorizations=[],
        parameters=[{
            "name": "body",
            "description": "Parameters in JSON format.<br/>Example: <br/>"
                           "{\"service_id\":\"...\"}",
            "required": True,
            "paramType": "body",
            "type": "string"
        }],
        responseMessages=[{
            "code": 406,
            "message": "'service_id' parameter not found"
        }, {
            "code": 500,
            "message": "Exception processing request"
        }])
    def delete(self):
        data = request.get_json()
        if 'service_id' not in data:
            logs.error('Lifecycle-Management: ServiceLifecycle: delete: Exception - parameter not found: service_id')
            return Response(json.dumps({'error': True, 'message': 'parameter not found: service_id'}),
                            status=406, content_type='application/json')
        return lm_service.terminate(data['service_id'])


api.add_resource(ServiceLifecycle, '/api/v1/lifecycle')


###############################################################################

def main():
    # get CIMI_API_ENV_VALUE from env
    # CIMI_API_ENV_VALUE = os.environ.get(CIMI_API_ENV_NAME, '...')
    # logs.info('[CIMI_API_ENV_VALUE=' + CIMI_API_ENV_VALUE + ']')
    # START SERVER
    context = (config.dic['CERT_CRT'], config.dic['CERT_KEY'])
    app.run(host='0.0.0.0', port=config.dic['SERVER_PORT'], ssl_context=context, threaded=True, debug=config.dic['DEBUG'])


if __name__ == "__main__":
    main()