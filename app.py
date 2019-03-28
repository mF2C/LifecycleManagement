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
                /lm/agent-config
                        GET:    get agent's lifecycle configuration: docker, docker-swarm, kubernetes, ...        
                                get agent's current user-profile and sharing-model (from 'local' User Management module)

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
                       description='mF2C - (micro)Lifecycle Management REST API - version ' + config.dic['VERSION'],
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
        'app': "(micro)Lifecycle Management REST API", 'status': "Running", 'api_doc_json': "http://" + config.dic['HOST_IP'] + ":" + str(config.dic['SERVER_PORT']) + config.dic['API_DOC_URL'],
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


########################################################################################################################
# MAIN
def main():
    LOG.info("LIFECYCLE: Starting (micro)Lifecycle Management application [version=" + str(config.dic['VERSION']) + "] ...")
    LOG.info("LIFECYCLE: Swagger running on http://" + config.dic['HOST_IP'] + ":" + str(config.dic['SERVER_PORT']) + config.dic['API_DOC_URL'] + ".html")
    LOG.info("LIFECYCLE: REST API running on http://" + config.dic['HOST_IP'] + ":" + str(config.dic['SERVER_PORT']) + config.dic['API_DOC_URL'])
    # START (SSL) SERVER
    # context = (config.dic['CERT_CRT'], config.dic['CERT_KEY'])
    # app.run(host='0.0.0.0', port=config.dic['SERVER_PORT'], ssl_context=context, threaded=True, debug=False)

    # START SERVER
    app.run(host='0.0.0.0', port=config.dic['SERVER_PORT'], threaded=True, debug=False)


if __name__ == "__main__":
    main()