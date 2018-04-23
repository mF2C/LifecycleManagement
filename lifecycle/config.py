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
        "HOST_IP":                      "192.168.252.41",                       # if possible, read from env values
        "API_DOC_URL":                  "/api/v1/lifecycle",
        "CERT_CRT":                     "cert/ia.crt",
        "CERT_KEY":                     "cert/ia.key",
        "DEBUG":                        False,
        "STANDALONE_MODE":              True,

        # VERIFY_SSL controls whether we verify the server's TLS certificate or not
        "VERIFY_SSL":                   False,

        # CIMI RESOURCES managed by this component
        "CIMI_USERS":                   "users",
        "CIMI_SERVICES":                "services",
        "CIMI_SERVICE":                 "service",
        "CIMI_SERVICE_INSTANCES":       "serviceInstances",
        "CIMI_SERVICE_INSTANCE":        "service-instance",

        # CIMI:  https://dashboard.mf2c-project.eu/api/cloud-entry-point
        "CIMI_URL":                     "https://dashboard.mf2c-project.eu/api",    # https://proxy
        "CIMI_COOKIES_PATH":            "~./cookies",
        "CIMI_USER":                    "rsucasas",
        "CIMI_PASSWORD":                "password",

        # URLs from other mF2C components:
        # PM-SLA MANAGER
        "URL_PM_SLA_MANAGER":           "https://127.0.0.1:46030",

        # AC-QoS PROVIDING
        "URL_AC_QoS_PROVIDING":         "https://127.0.0.1:46200/api/service-management",
        # AC-USER MANAGEMENT
        "URL_AC_USER_MANAGEMENT":       "https://127.0.0.1:46300/api/v1/user-management",

        # TODO!! PM-RECOMMENDER get recipe: api/v1/recommender/recipe/...
        "URL_PM_RECOMMENDER":           "https://localhost:46020/api/",
        # TODO!! PM-LANDSCAPER get resources (recipe): api/v1/landscape/...
        "URL_PM_LANDSCAPER":            "https://localhost:46010/api/",

        # TESTS
        #"AVAILABLE_AGENTS": ["192.168.252.41", "192.168.252.42", "192.168.252.43"]
        "AVAILABLE_AGENTS": [{"agent_ip": "192.168.252.41", "num_cpus": 4},
                             {"agent_ip": "192.168.252.42", "num_cpus": 2},
                             {"agent_ip": "192.168.252.43", "num_cpus": 2}]
}
