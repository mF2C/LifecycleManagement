"""
Kubernetes schemas
This is being developed for the MF2C Project: http://www.mf2c-project.eu/

Copyright: Atos Research and Innovation, 2017.

This code is licensed under an Apache 2.0 license. Please, refer to the LICENSE.TXT file for more information

Created on 04 dic. 2018

@author: Roi Sucasas - ATOS
"""


from common.logs import LOG


# genDeploymentDict
def genDeploymentDict(appname):
    try:
        dictDeployment = {
            "apiVersion": "apps/v1",
            "kind": "Deployment",
            "metadata": {
                "name": appname
            },
            "spec": {
                "replicas": 1,
                "revisionHistoryLimit": 10,
                "selector": {
                    "matchLabels": {
                        "app": appname
                    }
                },
                "template": {
                    "metadata": {
                        "labels": {
                            "app": appname
                        }
                    },
                    "spec": {
                        "containers": [
                            {
                                "image": "",
                                "name": "",
                                "imagePullPolicy": "",
                                "ports": [
                                    {"containerPort": 80}
                                ],
                                "volumeMounts": [
                                    {"name": "", "mountPath": ""}
                                ],
                                "env": [
                                    {"name": "", "value": ""}
                                ]
                            }
                        ]
                    }
                }
            }
        }

        return dictDeployment
    except:
        LOG.error("LIFECYCLE: Kubernetes schemas: genDeploymentDict: Error during the creation of the deployment dict")


# genServiceDict
def genServiceDict(appname):
    try:
        dictService = {
            "apiVersion": "v1",
            "kind": "Service",
            "metadata": {
                "name": "serv_" + appname
            },
            "spec": {
                "selector": {
                    "app": appname
                },
                "ports": [
                    {
                        "name": "", "port": 50090, "protocol": "TCP", "targetPort": 80
                    }
                ]
            }
        }

        return dictService
    except:
        LOG.error("LIFECYCLE: Kubernetes schemas: genDeploymentDict: Error during the creation of the deployment dict")
