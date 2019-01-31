"""
MF2C / COMPSs adapter
This is being developed for the MF2C Project: http://www.mf2c-project.eu/

Copyright: Atos Research and Innovation, 2017.

This code is licensed under an Apache 2.0 license. Please, refer to the LICENSE.TXT file for more information

Created on 09 feb. 2018

@author: Roi Sucasas - ATOS
"""

import requests
import sys, traceback
from common.logs import LOG
import common
from common.common import STATUS_STARTED
import lifecycle.data.db as db


'''
Lifecycle & COMPSs:

<startApplication>
    <ceiClass>es.bsc.compss.test.TestItf</ceiClass>
    <className>es.bsc.compss.test.Test</className>
    <methodName>main</methodName>
    <parameters>
        <params paramId="0">
            <direction>IN</direction>
            <type>OBJECT_T</type>
            <array paramId="0">
                <componentClassname>java.lang.String</componentClassname>
                <values>
                    <element paramId="0">
                        <className>java.lang.String</className>
                        <value xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xs="http://www.w3.org/2001/XMLSchema" xsi:type="xs:string">3</value>
                    </element>
                </values>
            </array>
        </params>
    </parameters>
    <resources>
        <resource name="172.17.0.3:46100">
            <description>
                <memorySize>4.0</memorySize>
                <memoryType>[unassigned]</memoryType>
                <operatingSystemDistribution>[unassigned]</operatingSystemDistribution>
                <operatingSystemType>[unassigned]</operatingSystemType>
                <operatingSystemVersion>[unassigned]</operatingSystemVersion>
                <pricePerUnit>-1.0</pricePerUnit>
                <priceTimeUnit>-1</priceTimeUnit>
                <processors>
                    <architecture>[unassigned]</architecture>
                    <computingUnits>1</computingUnits>
                    <internalMemory>-1.0</internalMemory>
                    <name>[unassigned]</name>
                    <propName>[unassigned]</propName>
                    <propValue>[unassigned]</propValue>
                    <speed>-1.0</speed>
                    <type>CPU</type>
                </processors>
                <storageSize>-1.0</storageSize>
                <storageType>[unassigned]</storageType>
                <value>0.0</value>
                <wallClockLimit>-1</wallClockLimit>
            </description>
        </resource>
        <resource name="172.17.0.2:46100">
            <description>
                <memorySize>4.0</memorySize>
                <memoryType>[unassigned]</memoryType>
                <operatingSystemDistribution>[unassigned]</operatingSystemDistribution>
                <operatingSystemType>[unassigned]</operatingSystemType>
                <operatingSystemVersion>[unassigned]</operatingSystemVersion>
                <pricePerUnit>-1.0</pricePerUnit>
                <priceTimeUnit>-1</priceTimeUnit>
                <processors>
                    <architecture>[unassigned]</architecture>
                    <computingUnits>1</computingUnits>
                    <internalMemory>-1.0</internalMemory>
                    <name>[unassigned]</name>
                    <propName>[unassigned]</propName>
                    <propValue>[unassigned]</propValue>
                    <speed>-1.0</speed>
                    <type>CPU</type>
                </processors>
                <storageSize>-1.0</storageSize>
                <storageType>[unassigned]</storageType>
                <value>0.0</value>
                <wallClockLimit>-1</wallClockLimit>
            </description>
        </resource>
    </resources>
    <serviceInstanceId>e47b5928-98c5-417e-9dd5-1593fc6dca5b</serviceInstanceId>
</startApplication>

# parameters:
#   "  <ceiClass>es.bsc.compss.test.TestItf</ceiClass>" \
#   "  <className>es.bsc.compss.test.Test</className>" \
#   "  <methodName>main</methodName>" \
#   "  <parameters>" \
#   "    <array paramId=\"0\">" \
#   "      <componentClassname>java.lang.String</componentClassname>" \
#   "      <values>" \
#   "        <element paramId=\"0\">" \
#   "          <className>java.lang.String</className>" \
#   "          <value xmlns:xsi=\"http://www.w3.org/2001/XMLSchema-instance\" " \
#   "             xmlns:xs=\"http://www.w3.org/2001/XMLSchema\" xsi:type=\"xs:string\">3</value>" \
#   "        </element>" \
#   "      </values>" \
#   "    </array>" \
#   "  </parameters>" \
'''


# find_master:
def find_master(service_instance):
    try:
        LOG.debug("Lifecycle-Management: common: find_master: Check if local agent has COMPSs and is included in the service instance ...")
        for agent in service_instance['agents']:
            if agent['status'] == STATUS_STARTED and agent['url'] == common.get_local_ip():
                LOG.debug("Lifecycle-Management: common: find_master: Local agent has COMPSs, status=STARTED and is included in the service instance!")
                LOG.debug("Lifecycle-Management: common: find_master: agent: " + str(agent))
                return agent

        LOG.debug("Lifecycle-Management: common: find_master: Check agents included in the service instance and status=STARTED ...")
        for agent in service_instance['agents']:
            if agent['status'] == STATUS_STARTED:
                LOG.debug("Lifecycle-Management: common: find_master: agent: " + str(agent))
                return agent
    except:
        LOG.error("Lifecycle-Management: common: find_master: Exception")

    LOG.warning("Lifecycle-Management: common: find_master: return service_instance['agents'][0]: " + str(service_instance['agents'][0]))
    return service_instance['agents'][0]


# gen_resource:
def gen_resource(url, ports):
    try:
        if url == common.get_local_ip():
            LOG.debug("Lifecycle-Management: COMPSs adapter: gen_resource: (local) get_COMPSs_port_DB_DOCKER_PORTS ...")
            compss_port = db.get_COMPSs_port_DB_DOCKER_PORTS(ports)
        else:
            LOG.debug("Lifecycle-Management: COMPSs adapter: gen_resource: (remote agent) first element from list ...")
            compss_port = ports[0]
        LOG.debug("Lifecycle-Management: COMPSs adapter: gen_resource: compss_port: " + str(compss_port))

        xml = "<resource name=\"" + url + ":" + str(compss_port) + "\">" \
              "  <description>" \
              "    <memorySize>4.0</memorySize>" \
              "    <memoryType>[unassigned]</memoryType>" \
              "    <operatingSystemDistribution>[unassigned]</operatingSystemDistribution>" \
              "    <operatingSystemType>[unassigned]</operatingSystemType>" \
              "    <operatingSystemVersion>[unassigned]</operatingSystemVersion>" \
              "    <pricePerUnit>-1.0</pricePerUnit>" \
              "    <priceTimeUnit>-1</priceTimeUnit>" \
              "    <processors>" \
              "      <architecture>[unassigned]</architecture>" \
              "      <computingUnits>2</computingUnits>" \
              "      <internalMemory>-1.0</internalMemory>" \
              "      <name>[unassigned]</name>" \
              "      <propName>[unassigned]</propName>" \
              "      <propValue>[unassigned]</propValue>" \
              "      <speed>-1.0</speed>" \
              "      <type>CPU</type>" \
              "    </processors>" \
              "    <storageSize>-1.0</storageSize>" \
              "    <storageType>[unassigned]</storageType>" \
              "    <value>0.0</value>" \
              "    <wallClockLimit>-1</wallClockLimit>" \
              "  </description>" \
              "</resource>"
        return xml
    except:
        LOG.error('Lifecycle-Management: COMPSs adapter: gen_resource: Exception')
        return False


# start_job: Start app in COMPSs container
def start_job(service_instance_id, agent, parameters):
    LOG.debug("Lifecycle-Management: COMPSs adapter: start_job: [agent=" + str(agent) + "], [parameters=" + str(parameters) + "]")
    try:
        # create (1) resource xml
        xml_resource = gen_resource(agent['url'], agent['ports'])

        # create xml
        xml = "<?xml version='1.0' encoding='utf-8'?>" \
              "<startApplication>" + parameters + \
              "  <resources>" + xml_resource + "  </resources>" \
              "  <serviceInstanceId>" + service_instance_id + "</serviceInstanceId>" \
              "</startApplication>"
        LOG.debug("Lifecycle-Management: COMPSs adapter: start_job: [xml=" + xml + "]")

        compss_port = db.get_COMPSs_port_DB_DOCKER_PORTS(agent['ports'])
        res = requests.put("http://" + agent['url'] + ":" + str(compss_port) + "/COMPSs/startApplication",
                           data=xml,
                           headers={'Content-Type': 'application/xml'})
        LOG.debug("Lifecycle-Management: COMPSs adapter: start_job: [res=" + str(res) + "]")
        return True
    except:
        traceback.print_exc(file=sys.stdout)
        LOG.error('Lifecycle-Management: COMPSs adapter: start_job: Exception')
        return False


# start_job_in_agents: Start app in multiple COMPSs containers
def start_job_in_agents(service_instance, parameters):
    LOG.debug("Lifecycle-Management: COMPSs adapter: start_job_in_agents: [service_instance=" + str(service_instance) + "], "
              "[parameters=" + str(parameters) + "]")
    try:
        # create resource xml
        xml_resources_content = ""
        for agent in service_instance['agents']:
            if agent['status'] == STATUS_STARTED:
                xml_resources_content += gen_resource(agent['url'], agent['ports'])

        if not xml_resources_content:
            LOG.error('Lifecycle-Management: COMPSs adapter: start_job_in_agents: xml_resources_content is empty: agents status != STATUS_STARTED')
            return False

        xml = "<?xml version='1.0' encoding='utf-8'?>" \
              "<startApplication>" + parameters + \
              "  <resources>" + xml_resources_content + "</resources>" \
              "  <serviceInstanceId>" + service_instance['id'].replace('service-instance/', '') + "</serviceInstanceId>" \
              "</startApplication>"
        LOG.debug("Lifecycle-Management: COMPSs adapter: start_job_in_agents: [xml=" + xml + "]")

        master_agent = find_master(service_instance)
        compss_port = db.get_COMPSs_port_DB_DOCKER_PORTS(master_agent['ports'])

        res = requests.put("http://" + master_agent['url'] + ":" + str(compss_port) + "/COMPSs/startApplication",
                           data=xml,
                           headers={'Content-Type': 'application/xml'})
        LOG.debug("Lifecycle-Management: COMPSs adapter: start_job_in_agents: [res=" + str(res) + "]")
        return True
    except:
        traceback.print_exc(file=sys.stdout)
        LOG.error('Lifecycle-Management: COMPSs adapter: start_job_in_agents: Exception')
        return False
