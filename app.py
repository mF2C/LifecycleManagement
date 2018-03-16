"""
REST API
This is being developed for the MF2C Project: http://www.mf2c-project.eu/

Copyright: Roi Sucasas Font, Atos Research and Innovation, 2017.

This code is licensed under an Apache 2.0 license. Please, refer to the LICENSE.TXT file for more information

Created on 27 sept. 2017

@author: Roi Sucasas - ATOS
"""

#!/usr/bin/python3

import lifecycle.lifecycle as lifecycle
import lifecycle.mF2C.handler_um as handler_um
import lifecycle.mF2C.handler_sla as handler_sla
import lifecycle.utils.auth as auth
import os
from lifecycle import config
from lifecycle.utils.logs import LOG
from flask_cors import CORS
from flask import Flask, request, Response, json
from flask_restful import Resource, Api
from flask_restful_swagger import swagger


try:
    # CONFIGURATION values
    LOG.info('[SERVER_PORT=' + str(config.dic['SERVER_PORT']) + ']')
    LOG.info('[API_DOC_URL=' + config.dic['API_DOC_URL'] + ']')
    LOG.info('[CERT_CRT=' + config.dic['CERT_CRT'] + ']')
    LOG.info('[CERT_KEY=' + config.dic['CERT_KEY'] + ']')
    LOG.info('[DEBUG=' + str(config.dic['DEBUG']) + ']')
    # CIMI
    LOG.info('[CIMI_URL=' + config.dic['CIMI_URL'] + ']')
    LOG.info('[CIMI_COOKIES_PATH=' + config.dic['CIMI_COOKIES_PATH'] + ']')
    LOG.info('[CIMI_USER=' + config.dic['CIMI_USER'] + ']')
    LOG.info('[CIMI_PASSWORD=' + config.dic['CIMI_PASSWORD'] + ']')

    # get CIMI from environment values:
    LOG.info('Reading values from ENVIRONMENT...')

    env_cimi_url = os.getenv('CIMI_URL', default='not-defined')
    LOG.info('[CIMI_URL=' + env_cimi_url + ']')
    if env_cimi_url != 'not-defined':
        config.dic['CIMI_URL'] = env_cimi_url

    env_cimi_cookies_path = os.getenv('CIMI_COOKIES_PATH', default='not-defined')
    LOG.info('[CIMI_COOKIES_PATH=' + env_cimi_cookies_path + ']')
    if env_cimi_cookies_path != 'not-defined':
        config.dic['CIMI_COOKIES_PATH'] = env_cimi_cookies_path

    env_cimi_user = os.getenv('CIMI_USER', default='not-defined')
    LOG.info('[CIMI_USER=' + env_cimi_user + ']')
    if env_cimi_user != 'not-defined':
        config.dic['CIMI_USER'] = env_cimi_user

    env_cimi_password = os.getenv('CIMI_PASSWORD', default='not-defined')
    LOG.info('[CIMI_PASSWORD=' + env_cimi_password + ']')
    if env_cimi_password != 'not-defined':
        config.dic['CIMI_PASSWORD'] = env_cimi_password

    # CIMI
    LOG.info('Checking CIMI configuration...')

    LOG.info('[CIMI_URL=' + config.dic['CIMI_URL'] + ']')
    LOG.info('[CIMI_COOKIES_PATH=' + config.dic['CIMI_COOKIES_PATH'] + ']')
    LOG.info('[CIMI_USER=' + config.dic['CIMI_USER'] + ']')
    LOG.info('[CIMI_PASSWORD=' + config.dic['CIMI_PASSWORD'] + ']')

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
    LOG.error('ERROR')


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
#               "service_instance_id": "",
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
#               "service_instance_id": "",
#               "warning_id": "",
#               "warning_txt": ""
#           }
#   }
class Service(Resource):
    # GET: get service status
    @swagger.operation(
        summary="Get service instance",
        notes="Gets the service instance",
        produces=["application/json"],
        authorizations=[],
        parameters=[{
                "name": "service_instance_id",
                "description": "Service instance ID",
                "required": True,
                "paramType": "path",
                "type": "string"
            }],
        responseMessages=[{
                "code": 500,
                "message": "Exception processing request"
            }])
    def get(self, service_instance_id):
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
    def post(self, service_instance_id):
        body = request.get_json()
        LOG.info('body: ' + str(body))
        if not body or 'type' not in body or 'data' not in body:
            LOG.error('Lifecycle-Management: Service: post: Exception - parameter not found: type / data')
            return Response(json.dumps({'error': True, 'message': 'parameter not found: type / data'}),
                            status=406, content_type='application/json')
        else:
            if body['type'] == "sla_notification":
                return handler_sla.handle_sla_notification(service_instance_id, body['data'])
            elif body['type'] == "um_warning":
                return handler_um.handle_warning(service_instance_id, body['data'])
        LOG.error("Lifecycle-Management: Service: post: type [" + body['type'] + "] not defined / implemented")
        return Response(json.dumps({'error': True, 'message': 'type not defined / implemented'}),
                        status=501, content_type='application/json')


api.add_resource(Service, '/api/v1/lifecycle/<string:service_instance_id>')


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
                           "{\"service\":{ \"service_id\": \"service_id\", \"service_path\": \"yeasy/simple-web\"}}",
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
            LOG.error('Lifecycle-Management: ServiceLifecycle: post: Exception - parameter not found: service')
            return Response(json.dumps({'error': True, 'message': 'parameter not found: service'}),
                            status=406, content_type='application/json')
        return lifecycle.submit(data['service'])

    # PUT: Starts / stops / restarts ... a service and returns a JSON object with the result / status of the operation.
    @swagger.operation(
        summary="Starts / stops / restarts a service ",
        notes="Starts / stops / restarts a service.",
        produces=["application/json"],
        authorizations=[],
        parameters=[{
            "name": "body",
            "description": "Parameters in JSON format.<br/>Example: <br/>"
                           "{\"service_instance_id\":\"...\", \"operation\":\"start/restart/stop\"}",
            "required": True,
            "paramType": "body",
            "type": "string"
        }],
        responseMessages=[{
            "code": 406,
            "message": "'service_instance_id' / 'operation' parameter not found"
        }, {
            "code": 500,
            "message": "Exception processing request"
        }])
    def put(self):
        data = request.get_json()
        if 'service_instance_id' not in data or 'operation' not in data:
            LOG.error('Lifecycle-Management: ServiceLifecycle: put: Exception - parameter not found: service_instance_id / operation')
            return Response(json.dumps({'error': True, 'message': 'parameter not found: service_instance_id / operation'}),
                            status=406, content_type='application/json')
        # operations
        if data['operation'] == 'start':
            return lifecycle.start(data['service_instance_id'])
        elif data['operation'] == 'stop':
            return lifecycle.stop(data['service_instance_id'])
        elif data['operation'] == 'restart':
            return lifecycle.restart(data['service_instance_id'])
        else:
            LOG.error('Lifecycle-Management: ServiceLifecycle: put: operation not defined / implemented')
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
                           "{\"service_instance_id\":\"...\"}",
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
            LOG.error('Lifecycle-Management: ServiceLifecycle: delete: Exception - parameter not found: service_instance_id')
            return Response(json.dumps({'error': True, 'message': 'parameter not found: service_instance_id'}),
                            status=406, content_type='application/json')
        return lifecycle.terminate(data['service_instance_id'])


api.add_resource(ServiceLifecycle, '/api/v1/lifecycle')


###############################################################################

def main():
    # START SERVER
    context = (config.dic['CERT_CRT'], config.dic['CERT_KEY'])
    app.run(host='0.0.0.0', port=config.dic['SERVER_PORT'], ssl_context=context, threaded=True, debug=config.dic['DEBUG'])


if __name__ == "__main__":
    main()