"""
CONFIGURATION FILE
This is being developed for the MF2C Project: http://www.mf2c-project.eu/

Copyright: Roi Sucasas Font, Atos Research and Innovation, 2017.

This code is licensed under an Apache 2.0 license. Please, refer to the LICENSE.TXT file for more information

Created on 18 oct. 2018

@author: Roi Sucasas - ATOS
"""

#!/usr/bin/python

dic = { "VERSION":                      "0.1",

        # SERVER - REST API
        "SERVER_PORT":                  46000,
        "HOST_IP":                      "192.168.252.40",                       # if possible, read from env values
        "API_DOC_URL":                  "/api/v2/lm",
        "CERT_CRT":                     "cert/ia.crt",
        "CERT_KEY":                     "cert/ia.key",
        "STANDALONE_MODE":              False,

        # VERIFY_SSL controls whether we verify the server's TLS certificate or not
        "VERIFY_SSL":                   False,

        # for testing the interaction with the lifecycle management
        "ENABLE_ASSESSMENT_TESTS":      True,

        # CIMI RESOURCES managed by this component
        "CIMI_SERVICE_INSTANCES": "serviceInstances",
        "CIMI_USERS": "users",
        "CIMI_PROFILES": "user-profile",  # "userProfiles",
        "CIMI_SHARING_MODELS": "sharing-model",  # "sharingModels",

        # CIMI
        "CIMI_URL":                     "http://cimi:8201/api",         # https://dashboard.mf2c-project.eu/api
        "CIMI_COOKIES_PATH":            "~./cookies",
        "CIMI_USER":                    "rsucasas",
        "CIMI_PASSWORD":                "password",

        # docker:
        # working dir for docker compose applications / services
        "WORKING_DIR_VOLUME":           "/home/atos/mF2C/compose_examples",
        # docker compose image: needed to deploy docker compose based services
        "DOCKER_COMPOSE_IMAGE":         "docker/compose:1.21.0",
        "DOCKER_COMPOSE_IMAGE_TAG":     "1.21.0",
        # docker socket volume
        "DOCKER_SOCKET_VOLUME":         "/var/run/docker.sock",
        # ports db
        "DB_DOCKER_PORTS":              "./docker_ports_db",

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
        "URL_PM_LIFECYCLE":             "https://lifecycle:46000/api/v1/lifecycle/",
        # AC-USER MANAGEMENT
        "URL_AC_USER_MANAGEMENT": "https://user-management:46300/api/v1/user-management"
}
