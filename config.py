"""
CONFIGURATION FILE
This is being developed for the MF2C Project: http://www.mf2c-project.eu/

Copyright: Roi Sucasas Font, Atos Research and Innovation, 2017.

This code is licensed under an Apache 2.0 license. Please, refer to the LICENSE.TXT file for more information

Created on 18 oct. 2018

@author: Roi Sucasas - ATOS
"""

#!/usr/bin/python

dic = { "VERSION":                      "1.0.8-arm",

        # SERVER - REST API:
        "SERVER_PORT":                  46000,
        "HOST_IP":                      "localhost",
        "API_DOC_URL":                  "/api/v2/lm",
        "CERT_CRT":                     "cert/ia.crt",
        "CERT_KEY":                     "cert/ia.key",

        # DOCKER / SWARM / K8s:
        "DOCKER_SOCKET":                "unix://var/run/docker.sock",
        "DOCKER_SWARM":                 False,
        "K8S_MASTER":                   False,

        # VERIFY_SSL controls whether we verify the server's TLS certificate or not
        "VERIFY_SSL":                   False,

        # CIMI:
        "CIMI_URL":                     "http://cimi:8201/api",
        "CIMI_USER":                    "rsucasas",   # TODO remove

        # docker:
        # working dir for docker compose applications / services
        "WORKING_DIR_VOLUME":           "/tmp/mf2c/compose_files",
        # docker compose image: needed to deploy docker compose based services
        "DOCKER_COMPOSE_IMAGE":         "docker/compose:1.24.0",
        "DOCKER_COMPOSE_IMAGE_TAG":     "1.24.0",
        # docker socket volume
        "DOCKER_SOCKET_VOLUME":         "/var/run/docker.sock",
        # ports db
        "DB_DOCKER_PORTS":              "./docker_ports_db",

        # URLs / ports from other mF2C components:
        # TIMEOUT ANALYTICS ENGINE
        "TIMEOUT_ANALYTICSENGINE":      25,
        # PORT_COMPSs
        "PORT_COMPSs":                  46100,
        # NETWORK_COMPSs
        "NETWORK_COMPSs":               "not-defined",
        # COMPSs - dataclay
        "DATACLAY_EP":                  "dataclay",
}
