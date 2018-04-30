"""
Allocation adapter
This is being developed for the MF2C Project: http://www.mf2c-project.eu/

Copyright: Atos Research and Innovation, 2017.

This code is licensed under an Apache 2.0 license. Please, refer to the LICENSE.TXT file for more information

Created on 09 feb. 2018

@author: Roi Sucasas - ATOS
"""

import lifecycle.modules.adapters.lf_adapter as lf_adapter


# allocate_service_agent: Deploy service in an agent
# IN: Service, Agent
# OUT: status value
def allocate_service_agent(service, agent):
    return lf_adapter.deploy_service_agent(service, agent)