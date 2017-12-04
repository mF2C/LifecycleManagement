'''
REST API
This is being developed for the MF2C Project: http://www.mf2c-project.eu/

Copyright: Roi Sucasas Font, Atos Research and Innovation, 2017.

This code is licensed under an Apache 2.0 license. Please, refer to the LICENSE.TXT file for more information

Created on 27 sept. 2017

@author: Roi Sucasas - ATOS
'''

#!/usr/bin/python3

# rest_api.py
import src.lm_service_operations as lm_service_operations
import src.lm_service as lm_service
import src.lm_warnings_handler as lm_warnings_handler
import src.lm_sla_handler as lm_sla_handler
import os
import logs
from flask import Flask, request, Response, json
from flask_restful import Resource, Api


CIMI_API_ENV_NAME = "CIMI_API"
CIMI_API_ENV_VALUE = "http://...."

app = Flask(__name__)
api = Api(app)


# 'home' route
@app.route('/api/v1/', methods=['GET'])
def default_route():
    data = {
        'app': 'Lifecycle Management Module REST API',
        'status': 'Running'
    }
    resp = Response(json.dumps(data), status=200, mimetype='application/json')
    return resp



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
    def get(self, service_id):
        return lm_service.getStatus(service_id)

    # POST: process warnings and notifications
    def post(self, service_id):
        data = request.get_json()
        if 'type' not in data or 'data' not in data:
            logs.error('Error (rest_api.py - Service) : POST : type / data  not found')
            return Response(json.dumps({'error': 'type not found'}), status=406, content_type='application/json')
        else:
            if 'type' == "sla_notification":
                return lm_sla_handler.handleSLANotifications(data['data'])
            elif 'type' == "um_warning":
                return lm_warnings_handler.handleWarning(data['data'])
        return Response(json.dumps({'error': 'type not defined / implemented'}), status=501, content_type='application/json')

api.add_resource(Service, '/api/v1/lifecycle/service_id')


# ServiceLifecycle route: submit, terminate, operations (start, stop, restart, pause...)
# 'data' from request (body) - content:
#   {
#       "service": {},
#       "service_id": "",
#       "operation": "stop"
#   }
class ServiceLifecycle(Resource):

    # POST: submit a new service
    def post(self):
        data = request.get_json()
        if 'service' not in data:
            logs.error('Error (rest_api.py - ServiceLifecycle) : POST : service not found')
            return Response(json.dumps({'error': 'service not found'}), status=406, content_type='application/json')
        return lm_service.submit(data['service'])

    # PUT: service operations
    def put(self):
        data = request.get_json()
        if 'service_id' not in data or 'operation' not in data:
            logs.error('Error (rest_api.py - ServiceLifecycle) : PUT : service_id / operation not found')
            return Response(json.dumps({'error': 'service_id / operation not found'}), status=406, content_type='application/json')
        # operations
        if data['operation'] == 'start':
            return lm_service_operations.start(data['service_id'])
        elif data['operation'] == 'stop':
            return lm_service_operations.stop(data['service_id'])
        elif data['operation'] == 'restart':
            return lm_service_operations.restart(data['service_id'])
        else:
            logs.error('Error (rest_api.py - ServiceLifecycle) : PUT : operation not defined / implemented')
            return Response(json.dumps({'error': 'operation not defined / implemented'}), status=501, content_type='application/json')

    # DELETE: terminate service
    def delete(self):
        data = request.get_json()
        if 'service_id' not in data:
            logs.error('Error (rest_api.py - ServiceLifecycle) : DELETE : service_id not found')
            return Response(json.dumps({'error': 'service_id not found'}), status=406, content_type='application/json')
        return lm_service.terminate(data['service_id'])

api.add_resource(ServiceLifecycle, '/api/v1/lifecycle')



def main():
    # get CIMI_API_ENV_VALUE from env
    CIMI_API_ENV_VALUE = os.environ.get(CIMI_API_ENV_NAME, '...')
    logs.info('[CIMI_API_ENV_VALUE=' + CIMI_API_ENV_VALUE + ']')
    # start server
    app.run(host='0.0.0.0', debug=True)


if __name__ == "__main__":
    main()
