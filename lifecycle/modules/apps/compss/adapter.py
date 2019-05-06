"""
MF2C / COMPSs adapter
This is being developed for the MF2C Project: http://www.mf2c-project.eu/

Copyright: Atos Research and Innovation, 2017.

This code is licensed under an Apache 2.0 license. Please, refer to the LICENSE.TXT file for more information

Created on 09 feb. 2018

@author: Roi Sucasas - ATOS
"""

import requests
from common.logs import LOG
from common.common import STATUS_STARTED
import lifecycle.data.db as db
import lifecycle.data.data_adapter as data_adapter
import lifecycle.data.service_instance as data_service_instance


'''
Lifecycle & COMPSs (IT-2):

<startApplication>
    <ceiClass>es.bsc.compss.agent.test.TestItf</ceiClass>
    <className>es.bsc.compss.agent.test.Test</className>
    <hasResult>false</hasResult>
    <methodName>main</methodName>
    <parameters>
        <params paramId="0">
            <direction>IN</direction>
            <stream>UNSPECIFIED</stream>
            <type>OBJECT_T</type>
            <array paramId="0">
                <componentClassname>java.lang.String</componentClassname>
                <values>
                    <element paramId="0">
                        <className>java.lang.String</className>
                        <value xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xs="http://www.w3.org/2001/XMLSchema" xsi:type="xs:string">20</value>
                    </element>
                </values>
            </array>
        </params>
    </parameters>
    <resources>
        <externalResource>
            <adaptor>es.bsc.compss.agent.rest.master.Adaptor</adaptor>
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
                    <name>MainProcessor</name>
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
            <name>172.18.0.7</name>
            <resourceConf xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:type="ResourcesExternalAdaptorProperties">
                <Property>
                    <Name>Port</Name>
                    <Value>46100</Value>
                </Property>
            </resourceConf>
        </externalResource>
        <externalResource>
            <adaptor>es.bsc.compss.agent.rest.master.Adaptor</adaptor>
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
                    <name>MainProcessor</name>
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
            <name>172.18.0.5</name>
            <resourceConf xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:type="ResourcesExternalAdaptorProperties">
                <Property>
                    <Name>Port</Name>
                    <Value>46101</Value>
                </Property>
            </resourceConf>
        </externalResource>
        <externalResource>
            <adaptor>es.bsc.compss.agent.rest.master.Adaptor</adaptor>
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
                    <name>MainProcessor</name>
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
            <name>172.18.0.6</name>
            <resourceConf xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:type="ResourcesExternalAdaptorProperties">
                <Property>
                    <Name>Port</Name>
                    <Value>46102</Value>
                </Property>
            </resourceConf>
        </externalResource>
    </resources>
</startApplication>
'''


# gen_resource:
def gen_resource(url, ports):
    try:
        if url == data_adapter.get_my_ip(): #common.get_ip_address():
            LOG.debug("LIFECYCLE: COMPSs adapter: gen_resource: (local) get_COMPSs_port_DB_DOCKER_PORTS ...")
            compss_port = db.get_COMPSs_port_DB_DOCKER_PORTS(ports)
        else:
            LOG.debug("LIFECYCLE: COMPSs adapter: gen_resource: (remote agent) first element from list ...")
            compss_port = ports[0]
        LOG.debug("LIFECYCLE: COMPSs adapter: gen_resource: compss_port: " + str(compss_port))

        xml = "<externalResource>" \
              "     <adaptor>es.bsc.compss.agent.rest.master.Adaptor</adaptor>" \
              "     <description>" \
              "         <memorySize>4.0</memorySize>" \
              "         <memoryType>[unassigned]</memoryType>" \
              "         <operatingSystemDistribution>[unassigned]</operatingSystemDistribution>" \
              "         <operatingSystemType>[unassigned]</operatingSystemType>" \
              "         <operatingSystemVersion>[unassigned]</operatingSystemVersion>" \
              "         <pricePerUnit>-1.0</pricePerUnit>" \
              "         <priceTimeUnit>-1</priceTimeUnit>" \
              "         <processors>" \
              "             <architecture>[unassigned]</architecture>" \
              "             <computingUnits>2</computingUnits>" \
              "             <internalMemory>-1.0</internalMemory>" \
              "             <name>MainProcessor</name>" \
              "             <propName>[unassigned]</propName>" \
              "             <propValue>[unassigned]</propValue>" \
              "             <speed>-1.0</speed>" \
              "             <type>CPU</type>" \
              "         </processors>" \
              "         <storageSize>-1.0</storageSize>" \
              "         <storageType>[unassigned]</storageType>" \
              "         <value>0.0</value>" \
              "         <wallClockLimit>-1</wallClockLimit>" \
              "     </description>" \
              "     <name>" + url + "</name>" \
              "     <resourceConf xmlns:xsi=\"http://www.w3.org/2001/XMLSchema-instance\" xsi:type=\"ResourcesExternalAdaptorProperties\">" \
              "         <Property>" \
              "             <Name>Port</Name>" \
              "             <Value>" + str(compss_port) + "</Value>" \
              "         </Property>" \
              "     </resourceConf>" \
              "</externalResource>"
        return xml
    except:
        LOG.exception('LIFECYCLE: COMPSs adapter: gen_resource: Exception')
        return False


# start_job: Start app in COMPSs container
def start_job(service_instance_id, body, agent): #service_instance_id, agent, parameters):
    ceiClass = body['ceiClass']
    className = body['className']
    hasResult = body['hasResult']
    methodName = body['methodName']
    parameters = body['parameters']
    LOG.debug("LIFECYCLE: COMPSs adapter: start_job: [agent=" + str(agent) + "], [body=" + str(body) + "]")
    try:
        # create (1) resource xml
        xml_resource = gen_resource(agent['url'], agent['ports'])

        # create xml
        # TODO ??? "  <serviceInstanceId>" + service_instance_id + "</serviceInstanceId>" \   ????
        xml = "<?xml version='1.0' encoding='utf-8'?>" \
              "<startApplication>" \
              "<ceiClass>" + ceiClass + "</ceiClass>" \
              "<className>" + className + "</className>" \
              "<hasResult>" + str(hasResult) + "</hasResult>" \
              "<methodName>" + methodName + "</methodName>" \
              "<parameters>" + parameters + "</parameters>" \
              "<resources>" + xml_resource + "</resources>" \
              "</startApplication>"
        LOG.debug("LIFECYCLE: COMPSs adapter: start_job: [xml=" + xml + "]")

        compss_port = db.get_COMPSs_port_DB_DOCKER_PORTS(agent['ports'])
        LOG.debug("LIFECYCLE: COMPSs adapter: start_job: PUT http://" + agent['url'] + ":" + str(compss_port) + "/COMPSs/startApplication")

        res = requests.put("http://" + agent['url'] + ":" + str(compss_port) + "/COMPSs/startApplication",
                           data=xml,
                           headers={'Content-Type': 'application/xml'})
        LOG.debug("LIFECYCLE: COMPSs adapter: start_job: [res=" + str(res) + "]")
        return True
    except:
        LOG.exception('LIFECYCLE: COMPSs adapter: start_job: Exception')
        return False


# start_job_in_agents: Start app in multiple COMPSs containers
def start_job_in_agents(service_instance, body):
    ceiClass = body['ceiClass']
    className = body['className']
    hasResult = body['hasResult']
    methodName = body['methodName']
    parameters = body['parameters']
    LOG.debug("LIFECYCLE: COMPSs adapter: start_job_in_agents: [service_instance=" + str(service_instance) + "], [parameters=" + str(parameters) + "]")
    try:
        # create resource xml
        xml_resources_content = ""
        for agent in service_instance['agents']:
            if agent['status'] == STATUS_STARTED:
                xml_resources_content += gen_resource(agent['url'], agent['ports'])

        if not xml_resources_content:
            LOG.error('LIFECYCLE: COMPSs adapter: start_job_in_agents: xml_resources_content is empty: agents status != STATUS_STARTED')
            return False

        # TODO ??? "  <serviceInstanceId>" + service_instance_id + "</serviceInstanceId>" \   ????
        xml = "<?xml version='1.0' encoding='utf-8'?>" \
              "<startApplication>" \
              "  <ceiClass>" + ceiClass + "</ceiClass>" \
              "  <className>" + className + "</className>" \
              "  <hasResult>" + str(hasResult) + "</hasResult>" \
              "  <methodName>" + methodName + "</methodName>" \
              "  <parameters>" + parameters + "</parameters>" \
              "  <resources>" + xml_resources_content + "</resources>" \
              "</startApplication>"
        LOG.debug("LIFECYCLE: COMPSs adapter: start_job: [xml=" + xml + "]")

        master_agent = data_service_instance.find_master(service_instance)
        compss_port = db.get_COMPSs_port_DB_DOCKER_PORTS(master_agent['ports'])

        res = requests.put("http://" + master_agent['url'] + ":" + str(compss_port) + "/COMPSs/startApplication",
                           data=xml,
                           headers={'Content-Type': 'application/xml'})
        LOG.debug("LIFECYCLE: COMPSs: adapter: start_job_in_agents: response: " + str(res) + ", " + str(res.json()))

        # TODO store operation ID
        appId = "12312422312"
        data_service_instance.store_appid_in_master(service_instance, appId)

        return True
    except:
        LOG.exception('LIFECYCLE: COMPSs adapter: start_job_in_agents: Exception')
        return False


# add_resources_to_job
def add_resources_to_job(service_instance, appId, workerIP):
    # <?xml version="1.0" encoding="UTF-8" standalone="yes"?>
    # <newResource>
    #    <appId>1357211900655995414</appId>
    #    <externalResource>
    #        <adaptor>es.bsc.compss.agent.rest.master.Adaptor</adaptor>
    #        <description>
    #            <memorySize>4.0</memorySize>
    #            <memoryType>[unassigned]</memoryType>
    #            <operatingSystemDistribution>[unassigned]</operatingSystemDistribution>
    #            <operatingSystemType>[unassigned]</operatingSystemType>
    #            <operatingSystemVersion>[unassigned]</operatingSystemVersion>
    #            <pricePerUnit>-1.0</pricePerUnit>
    #            <priceTimeUnit>-1</priceTimeUnit>
    #            <processors>
    #                <architecture>[unassigned]</architecture>
    #                <computingUnits>1</computingUnits>
    #                <internalMemory>-1.0</internalMemory>
    #                <name>MainProcessor</name>
    #                <propName>[unassigned]</propName>
    #                <propValue>[unassigned]</propValue>
    #                <speed>-1.0</speed>
    #                <type>CPU</type>
    #            </processors>
    #            <storageSize>-1.0</storageSize>
    #            <storageType>[unassigned]</storageType>
    #            <value>0.0</value>
    #            <wallClockLimit>-1</wallClockLimit>
    #        </description>
    #        <name>172.18.0.6</name>
    #        <resourceConf xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:type="ResourcesExternalAdaptorProperties">
    #            <Property>
    #                <Name>Port</Name>
    #                <Value>46102</Value>
    #            </Property>
    #        </resourceConf>
    #    </externalResource>
    # </newResource>
    LOG.debug("LIFECYCLE: COMPSs adapter: add_resources_to_job: ")
    try:
        # TODO get new port for new resource ==> 46102
        xml = "<newResource>" \
              "     <appId>" + appId + "</appId>" \
              "     <externalResource>" \
              "         <adaptor>es.bsc.compss.agent.rest.master.Adaptor</adaptor>" \
              "         <description>" \
              "             <memorySize>4.0</memorySize>" \
              "             <memoryType>[unassigned]</memoryType>" \
              "             <operatingSystemDistribution>[unassigned]</operatingSystemDistribution>" \
              "             <operatingSystemType>[unassigned]</operatingSystemType>" \
              "             <operatingSystemVersion>[unassigned]</operatingSystemVersion>" \
              "             <pricePerUnit>-1.0</pricePerUnit>" \
              "             <priceTimeUnit>-1</priceTimeUnit>" \
              "             <processors>" \
              "                 <architecture>[unassigned]</architecture>" \
              "                 <computingUnits>2</computingUnits>" \
              "                 <internalMemory>-1.0</internalMemory>" \
              "                 <name>MainProcessor</name>" \
              "                 <propName>[unassigned]</propName>" \
              "                 <propValue>[unassigned]</propValue>" \
              "                 <speed>-1.0</speed>" \
              "                 <type>CPU</type>" \
              "             </processors>" \
              "             <storageSize>-1.0</storageSize>" \
              "             <storageType>[unassigned]</storageType>" \
              "             <value>0.0</value>" \
              "             <wallClockLimit>-1</wallClockLimit>" \
              "         </description>" \
              "         <name>" + workerIP + "</name>" \
              "         <resourceConf xmlns:xsi=\"http://www.w3.org/2001/XMLSchema-instance\" xsi:type=\"ResourcesExternalAdaptorProperties\">" \
              "             <Property>" \
              "                 <Name>Port</Name>" \
              "                 <Value>46102</Value>" \
              "             </Property>" \
              "         </resourceConf>" \
              "     </externalResource>" \
              "</newResource>"

        master_agent = data_service_instance.find_master(service_instance)
        compss_port = db.get_COMPSs_port_DB_DOCKER_PORTS(master_agent['ports'])

        res = requests.put("http://" + master_agent['url'] + ":" + str(compss_port) + "/COMPSs/newResource",
                           data=xml,
                           headers={'Content-Type': 'application/xml'})
        LOG.debug("LIFECYCLE: COMPSs: adapter: add_resources_to_job: response: " + str(res) + ", " + str(res.json()))

        return True
    except:
        LOG.exception('LIFECYCLE: COMPSs adapter: add_resources_to_job: Exception')
        return False


# rem_resources_from_job
def rem_resources_from_job(service_instance, appId, workerIP):
    # OPTION 1
    # <?xml version="1.0" encoding="UTF-8" standalone="yes"?>
    # <removeNode>
    #    <appId>8408755967528372176</appId>
    #    <workerName>172.18.0.5</workerName>
    # </removeNode>
    #
    # OPTION 2
    # <?xml version="1.0" encoding="UTF-8" standalone="yes"?>
    # <reduceNode>
    #    <appId>8234957497504047381</appId>
    #    <resources>
    #        <memorySize>4.0</memorySize>
    #        <memoryType>[unassigned]</memoryType>
    #        <operatingSystemDistribution>[unassigned]</operatingSystemDistribution>
    #        <operatingSystemType>[unassigned]</operatingSystemType>
    #        <operatingSystemVersion>[unassigned]</operatingSystemVersion>
    #        <pricePerUnit>-1.0</pricePerUnit>
    #        <priceTimeUnit>-1</priceTimeUnit>
    #        <processors>
    #            <architecture>[unassigned]</architecture>
    #            <computingUnits>1</computingUnits>
    #            <internalMemory>-1.0</internalMemory>
    #            <name>MainProcessor</name>
    #            <propName>[unassigned]</propName>
    #            <propValue>[unassigned]</propValue>
    #            <speed>-1.0</speed>
    #            <type>CPU</type>
    #        </processors>
    #        <storageSize>-1.0</storageSize>
    #        <storageType>[unassigned]</storageType>
    #        <value>0.0</value>
    #        <wallClockLimit>-1</wallClockLimit>
    #    </resources>
    #    <workerName>172.18.0.5</workerName>
    # </reduceNode>
    LOG.debug("LIFECYCLE: COMPSs adapter: rem_resources_from_job: ")
    try:
        xml = "<removeNode>" \
              "     <appId>" + appId + "</appId>" \
              "     <workerName>" + workerIP + "</workerName>" \
              "</removeNode>"

        master_agent = data_service_instance.find_master(service_instance)
        compss_port = db.get_COMPSs_port_DB_DOCKER_PORTS(master_agent['ports'])

        res = requests.put("http://" + master_agent['url'] + ":" + str(compss_port) + "/COMPSs/removeNode",
                           data=xml,
                           headers={'Content-Type': 'application/xml'})
        LOG.debug("LIFECYCLE: COMPSs: adapter: rem_resources_from_job: response: " + str(res) + ", " + str(res.json()))

        return True
    except:
        LOG.exception('LIFECYCLE: COMPSs adapter: rem_resources_from_job: Exception')
        return False


# notify_job_resource_lost
def notify_job_resource_lost(service_instance, appId, workerIP):
    # <?xml version="1.0" encoding="UTF-8" standalone="yes"?>
    # <lostNode>
    #    <appId>1357211900655995414</appId>
    #    <workerName>172.18.0.5</workerName>
    # </lostNode>
    LOG.debug("LLIFECYCLE: COMPSs adapter: notify_job_resource_lost: ")
    try:
        xml = "<lostNode>" \
              "     <appId>" + appId + "</appId>" \
              "     <workerName>" + workerIP + "</workerName>" \
              "</lostNode>"

        master_agent = data_service_instance.find_master(service_instance)
        compss_port = db.get_COMPSs_port_DB_DOCKER_PORTS(master_agent['ports'])

        res = requests.put("http://" + master_agent['url'] + ":" + str(compss_port) + "/COMPSs/lostNode",
                           data=xml,
                           headers={'Content-Type': 'application/xml'})
        LOG.debug("LIFECYCLE: COMPSs: adapter: notify_job_resource_lost: response: " + str(res) + ", " + str(res.json()))

        return True
    except:
        LOG.exception('LIFECYCLE: COMPSs adapter: notify_job_resource_lost: Exception')
        return False