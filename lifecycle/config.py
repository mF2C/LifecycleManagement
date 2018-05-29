"""
CONFIGURATION FILE
This is being developed for the MF2C Project: http://www.mf2c-project.eu/

Copyright: Roi Sucasas Font, Atos Research and Innovation, 2017.

This code is licensed under an Apache 2.0 license. Please, refer to the LICENSE.TXT file for more information

Created on 09 feb. 2018

@author: Roi Sucasas - ATOS
"""

#!/usr/bin/python

dic = { "SERVER_PORT":                  46000,
        "HOST_IP":                      "192.168.252.40",                       # if possible, read from env values
        "API_DOC_URL":                  "/api/v1/lifecycle",
        "CERT_CRT":                     "cert/ia.crt",
        "CERT_KEY":                     "cert/ia.key",
        "STANDALONE_MODE":              False,

        # VERIFY_SSL controls whether we verify the server's TLS certificate or not
        "VERIFY_SSL":                   False,

        # CIMI RESOURCES managed by this component
        "CIMI_SERVICE_INSTANCES":       "serviceInstances",

        # CIMI:  https://dashboard.mf2c-project.eu/api/cloud-entry-point
        "CIMI_URL":                     "",    # https://proxy
        "CIMI_COOKIES_PATH":            "~./cookies",
        "CIMI_USER":                    "",
        "CIMI_PASSWORD":                "",

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
        # AC-USER MANAGEMENT
        "URL_AC_USER_MANAGEMENT":       "https://user-management:46300/api/v1/user-management",
        # PORT_COMPSs
        "PORT_COMPSs":                  46100,
        # NETWORK_COMPSs
        "NETWORK_COMPSs":               "not-defined",
        # COMPSs - dataclay
        "DATACLAY_EP":                  "dataclay",
        # URL_PM_RECOM_LANDSCAPER:
        "URL_PM_RECOM_LANDSCAPER":      "http://192.168.252.41:46020/mf2c",
}
