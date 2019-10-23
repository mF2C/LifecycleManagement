"""
MF2C / COMPSs adapter
This is being developed for the MF2C Project: http://www.mf2c-project.eu/

Copyright: Atos Research and Innovation, 2017.

This code is licensed under an Apache 2.0 license. Please, refer to the LICENSE.TXT file for more information

Created on 09 feb. 2018

@author: Roi Sucasas - ATOS
"""

import requests
from lifecycle.logs import LOG
from lifecycle.common import STATUS_STARTED
from lifecycle.data import data_adapter as data_adapter


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
            ...
        </externalResource>
    </resources>
</startApplication>
'''


# gen_resource:
def gen_resource(url, ports):
    try:
        LOG.debug("[lifecycle.modules.apps.compss.adapter] [gen_resource] Getting first element from list (compss_port) ...")
        compss_port = ports[0]
        LOG.debug("[lifecycle.modules.apps.compss.adapter] [gen_resource] compss_port: " + str(compss_port))

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
        LOG.exception('[lifecycle.modules.apps.compss.adapter] [gen_resource] Exception')
        return False


# start_job: Start app in COMPSs container
def start_job(service_instance, body):
    ceiClass = body['ceiClass']
    className = body['className']
    hasResult = body['hasResult']
    methodName = body['methodName']
    parameters = body['parameters']

    service_instance_id = service_instance['id']
    agent = service_instance['agents'][0]

    LOG.debug("[lifecycle.modules.apps.compss.adapter] [start_job] service_instance_id=" + service_instance_id + ", agent=" + str(agent) + ", body=" + str(body))
    try:
        # create resource xml
        xml_resource = gen_resource(agent['url'], agent['ports'])

        # create xml
        xml = "<?xml version='1.0' encoding='utf-8'?>" \
              "<startApplication>" \
              "  <ceiClass>" + ceiClass + "</ceiClass>" \
              "  <className>" + className + "</className>" \
              "  <hasResult>" + str(hasResult) + "</hasResult>" \
              "  <methodName>" + methodName + "</methodName>" \
              "  <parameters>" + parameters + "</parameters>" \
              "  <resources>" + xml_resource + "</resources>" \
              "  <serviceInstanceId>" + service_instance['id'].replace("service-instance/", "") + "</serviceInstanceId>" \
              "</startApplication>"
        LOG.debug("[lifecycle.modules.apps.compss.adapter] [start_job] [xml=" + xml + "]")

        master_agent = data_adapter.serv_instance_find_master(service_instance)
        compss_port = agent['ports'][0]
        LOG.debug("[lifecycle.modules.apps.compss.adapter] [start_job] PUT http://" + agent['url'] + ":" + str(compss_port) + "/COMPSs/startApplication")

        res = requests.put("http://" + agent['url'] + ":" + str(compss_port) + "/COMPSs/startApplication",
                           data=xml,
                           headers={'Content-Type': 'application/xml'})
        if res.ok:
            LOG.debug("[lifecycle.modules.apps.compss.adapter] [start_job] response (json): " + str(res) + ", " + str(res.json()) + ", " + str(res.text))
            data_adapter.serv_instance_store_appid_in_master(service_instance, str(res.json()))
            return True
        else:
            LOG.error("[lifecycle.modules.apps.compss.adapter] [start_job] Response from COMPSs: " + str(res))
    except:
        LOG.exception('[lifecycsle.modules.apps.compss.adapter] [start_job] Exception')
    return False


# start_job_in_agents: Start app in multiple COMPSs containers
def start_job_in_agents(service_instance, body):
    ceiClass = body['ceiClass']
    className = body['className']
    hasResult = body['hasResult']
    methodName = body['methodName']
    parameters = body['parameters']
    LOG.debug("[lifecycle.modules.apps.compss.adapter] [start_job_in_agents] [service_instance=" + str(service_instance) + "], [parameters=" + str(parameters) + "]")
    try:
        # create resource xml
        xml_resources_content = ""
        for agent in service_instance['agents']:
            if agent['status'] == STATUS_STARTED:
                xml_resources_content += gen_resource(agent['url'], agent['ports'])

        if not xml_resources_content:
            LOG.error('[lifecycle.modules.apps.compss.adapter] [start_job_in_agents] xml_resources_content is empty: agents status != STATUS_STARTED')
            return False

        xml = "<?xml version='1.0' encoding='utf-8'?>" \
              "<startApplication>" \
              "  <ceiClass>" + ceiClass + "</ceiClass>" \
              "  <className>" + className + "</className>" \
              "  <hasResult>" + str(hasResult) + "</hasResult>" \
              "  <methodName>" + methodName + "</methodName>" \
              "  <parameters>" + parameters + "</parameters>" \
              "  <resources>" + xml_resources_content + "</resources>" \
              "  <serviceInstanceId>" + service_instance['id'].replace("service-instance/", "") + "</serviceInstanceId>" \
              "</startApplication>"
        LOG.debug("[lifecycle.modules.apps.compss.adapter] [start_job_in_agents] [xml=" + xml + "]")

        master_agent = data_adapter.serv_instance_find_master(service_instance)
        compss_port = master_agent['ports'][0]

        res = requests.put("http://" + master_agent['url'] + ":" + str(compss_port) + "/COMPSs/startApplication",
                           data=xml,
                           headers={'Content-Type': 'application/xml'})
        LOG.debug("[lifecycle.modules.apps.compss.adapter] [start_job_in_agents] response: " + str(res) + ", " + str(res.json()))

        if res.ok:
            LOG.debug("[lifecycle.modules.apps.compss.adapter] [start_job_in_agents] res.text: " + str(res.text))
            data_adapter.serv_instance_store_appid_in_master(service_instance, str(res.json()))
            return True
    except:
        LOG.exception('[lifecycle.modules.apps.compss.adapter] [start_job_in_agents] Exception')
    return False


# add_resources_to_job
def add_resources_to_job(service_instance, appId, workerIP, workerPorts):
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
    LOG.debug("[lifecycle.modules.apps.compss.adapter] [add_resources_to_job] Adding new worker to execution: workerIP=" + workerIP + ", workerPort=" + str(workerPort) + " ...")
    try:
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
              "                 <Name>" + str(workerPorts[0]) + "</Name>" \
              "                 <Value>46102</Value>" \
              "             </Property>" \
              "         </resourceConf>" \
              "     </externalResource>" \
              "</newResource>"

        master_agent = data_adapter.serv_instance_find_master(service_instance)
        compss_port = master_agent['ports'][0]

        res = requests.put("http://" + master_agent['url'] + ":" + str(compss_port) + "/COMPSs/newResource",
                           data=xml,
                           headers={'Content-Type': 'application/xml'})
        LOG.debug("[lifecycle.modules.apps.compss.adapter] [add_resources_to_job] response: " + str(res) + ", " + str(res.json()))

        return True
    except:
        LOG.exception('[lifecycle.modules.apps.compss.adapter] [add_resources_to_job] Exception')
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
    LOG.debug("[lifecycle.modules.apps.compss.adapter] [rem_resources_from_job] ...")
    try:
        xml = "<removeNode>" \
              "     <appId>" + appId + "</appId>" \
              "     <workerName>" + workerIP + "</workerName>" \
              "</removeNode>"

        master_agent = data_adapter.serv_instance_find_master(service_instance)
        compss_port = data_adapter.db_get_compss_port(master_agent['ports'])

        res = requests.put("http://" + master_agent['url'] + ":" + str(compss_port) + "/COMPSs/removeNode",
                           data=xml,
                           headers={'Content-Type': 'application/xml'})
        LOG.debug("[lifecycle.modules.apps.compss.adapter] [rem_resources_from_job] response: " + str(res) + ", " + str(res.json()))

        return True
    except:
        LOG.exception('[lifecycle.modules.apps.compss.adapter] [rem_resources_from_job] Exception')
        return False


# notify_job_resource_lost
def notify_job_resource_lost(service_instance, appId, workerIP):
    # <?xml version="1.0" encoding="UTF-8" standalone="yes"?>
    # <lostNode>
    #    <appId>1357211900655995414</appId>
    #    <workerName>172.18.0.5</workerName>
    # </lostNode>
    LOG.debug("[lifecycle.modules.apps.compss.adapter] [notify_job_resource_lost] ...")
    try:
        xml = "<lostNode>" \
              "     <appId>" + appId + "</appId>" \
              "     <workerName>" + workerIP + "</workerName>" \
              "</lostNode>"

        master_agent = data_adapter.serv_instance_find_master(service_instance)
        compss_port = data_adapter.db_get_compss_port(master_agent['ports'])

        res = requests.put("http://" + master_agent['url'] + ":" + str(compss_port) + "/COMPSs/lostNode",
                           data=xml,
                           headers={'Content-Type': 'application/xml'})
        LOG.debug("[lifecycle.modules.apps.compss.adapter] [notify_job_resource_lost] response: " + str(res) + ", " + str(res.json()))

        return True
    except:
        LOG.exception('[lifecycle.modules.apps.compss.adapter] [notify_job_resource_lost] Exception')
        return False