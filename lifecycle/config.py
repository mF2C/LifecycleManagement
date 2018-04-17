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
        "DEBUG":                        False,
        # VERIFY_SSL controls whether we verify the server's TLS certificate or not
        "VERIFY_SSL":                   False,
        # CIMI RESOURCES
        "CIMI_USERS":                   "users",
        "CIMI_SERVICES":                "services",
        "CIMI_SERVICE":                 "service",
        "CIMI_SERVICE_INSTANCES":       "serviceInstances",
        "CIMI_SERVICE_INSTANCE":        "service-instance",
        # URLs from other mF2C components:
        # CIMI:  https://dashboard.mf2c-project.eu/api/cloud-entry-point
        "CIMI_URL":                     "https://dashboard.mf2c-project.eu",    # "https://192.168.252.41",
        "CIMI_COOKIES_PATH":            "~./cookies",
        "CIMI_USER":                    "rsucasas",
        "CIMI_PASSWORD":                "password",
        # URLs from other mF2C components:
        #       PM-RECOMMENDER get recipe: api/v1/recommender/recipe/...
        "URL_PM_RECOMMENDER":           "https://localhost:5004/api/v1/recommender/recipe/....",
        #       PM-LANDSCAPER get resources (recipe): api/v1/landscape/...
        "URL_PM_LANDSCAPER":            "https://localhost:5003/api/v1/landscape/....",
        #       AC-QoS PROVIDING
        "URL_AC_QoS_PROVIDING":         "https://localhost:5003/api/v1/landscape/....",
        #       AC-USER MANAGEMENT
        "URL_AC_USER_MANAGEMENT":       "https://localhost:5003/api/v1/landscape/....",
        #       PM-COMPSS-RUNTIME allocate
        "URL_PM_COMPSS_RUNTIME_ALLOC":  "https://localhost:5003/api/v1/landscape/....",
        #       PM-COMPSS-RUNTIME execute
        "URL_PM_COMPSS_RUNTIME_EXEC":   "https://localhost:5003/api/v1/landscape/....",
        #       PM-SLA MANAGER
        "URL_PM_SLA_MANAGER":           "https://localhost:5003/api/v1/landscape/....",
        # TESTS
        #"AVAILABLE_AGENTS": ["192.168.252.41", "192.168.252.42", "192.168.252.43"]
        "AVAILABLE_AGENTS": [{"agent_ip": "192.168.252.41", "num_cpus": 4},
                             {"agent_ip": "192.168.252.42", "num_cpus": 2},
                             {"agent_ip": "192.168.252.43", "num_cpus": 2}]}
