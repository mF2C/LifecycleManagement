"""
CONFIGURATION FILE
This is being developed for the MF2C Project: http://www.mf2c-project.eu/

Copyright: Roi Sucasas Font, Atos Research and Innovation, 2017.

This code is licensed under an Apache 2.0 license. Please, refer to the LICENSE.TXT file for more information

Created on 18 oct. 2018

@author: Roi Sucasas - ATOS
"""

#!/usr/bin/python

dic = { "VERSION":                      "1.2.3",

        "LM_MODE":                      "MF2C", # "DEFAULT"  "MF2C"  "STANDALONE"

        # SERVER - REST API:
        "SERVER_PORT":                  46000,
        "HOST_IP":                      "localhost",
        "API_DOC_URL":                  "/api/v2/lm",
        "STANDALONE_MODE":              False,

        # working dir
        "LM_WORKING_DIR_VOLUME":        "/tmp/lm/", #"C://TMP/store/", # "/tmp/lm/", #

        # DOCKER / SWARM / K8s:
        "DOCKER_SOCKET":                "unix://var/run/docker.sock",
        "DOCKER_SWARM":                 False,
        "K8S_MASTER":                   False,
        "K8S_PROXY":                    "http://127.0.0.1:8001",
        "K8S_NAMESPACE":                "default",

        # VERIFY_SSL controls whether we verify the server's TLS certificate or not
        "VERIFY_SSL":                   False,

        # CIMI:
        "CIMI_URL":                     "http://cimi:8201/api",
        "CIMI_USER":                    "rsucasas",   # TODO remove

        # docker:
        # working dir for docker compose applications / services
        "WORKING_DIR_VOLUME":           "/home/atos/mF2C/compose_examples",
        # docker compose image: needed to deploy docker compose based services
        "DOCKER_COMPOSE_IMAGE":         "docker/compose:1.23.1", #1.21.0",
        "DOCKER_COMPOSE_IMAGE_TAG":     "1.23.1", #"1.21.0",
        # docker socket volume
        "DOCKER_SOCKET_VOLUME":         "/var/run/docker.sock",
        # ports db
        "DB_DOCKER_PORTS":              "docker_ports_db", #"./docker_ports_db",

        # URLs / ports from other mF2C components:
        # PM-SLA MANAGER
        "URL_PM_SLA_MANAGER":           "http://slalite:46030",
        # AC-QoS PROVIDING
        "URL_AC_SERVICE_MNGMT":         "http://service-manager:46200/api/service-management",
        # TIMEOUT ANALYTICS ENGINE
        "TIMEOUT_ANALYTICSENGINE":      25,
        # PORT_COMPSs
        "PORT_COMPSs":                  46100,
        # NETWORK_COMPSs
        "NETWORK_COMPSs":               "not-defined",
        # COMPSs - dataclay
        "DATACLAY_EP":                  "dataclay",
        # URL_PM_RECOM_LANDSCAPER:
        "URL_PM_RECOM_LANDSCAPER":      "http://analytics_engine:46020/mf2c",

        # TODO fix/remove dependencies
        # PM-Lifecycle: /api/v1/lifecycle/<string:service_id>
        "URL_PM_LIFECYCLE":             "http://lm-um:46000/api/v2/lm",
        # AC-USER MANAGEMENT
        "URL_AC_USER_MANAGEMENT":       "http://lm-um:46300/api/v2/um"
}
