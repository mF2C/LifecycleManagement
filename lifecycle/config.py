"""
CONFIGURATION FILE
This is being developed for the MF2C Project: http://www.mf2c-project.eu/

Copyright: Roi Sucasas Font, Atos Research and Innovation, 2017.

This code is licensed under an Apache 2.0 license. Please, refer to the LICENSE.TXT file for more information

Created on 27 sept. 2017

@author: Roi Sucasas - ATOS
"""

#!/usr/bin/python

dic = { "SERVER_PORT":                  46000,
        "API_DOC_URL":                  "/api/v1/lifecycle",
        "CERT_CRT":                     "cert/ia.crt",
        "CERT_KEY":                     "cert/ia.key",
        "DEBUG":                        False,
        # VERIFY_SSL controls whether we verify the server's TLS certificate or not
        "VERIFY_SSL":                   False,
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
        "AVAILABLE_AGENTS": ["192.168.252.7", "192.168.252.8", "192.168.252.9", "192.168.252.42"]}