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
from lifecycle.utils.logs import LOG


'''
Lifecycle & COMPSs:

<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
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
        <resource name="COMPSsWorker01:8080">
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
        <resource name="COMPSsWorker02:1200">
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
</startApplication>
'''


# start_job: Start app in COMPSs container
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
def start_job(agent, parameters):
    LOG.debug("Lifecycle-Management: COMPSs adapter: start_job: [agent=" + str(agent) + "], [parameters=" + parameters + "]")
    try:
        xml = "<?xml version='1.0' encoding='utf-8'?>" \
              "<startApplication>" + parameters + "<resources>" \
              "   <resource name=\"localhost:8080\">" \
              "      <description>" \
              "        <memorySize>4.0</memorySize>" \
              "        <memoryType>[unassigned]</memoryType>" \
              "        <operatingSystemDistribution>[unassigned]</operatingSystemDistribution>" \
              "        <operatingSystemType>[unassigned]</operatingSystemType>" \
              "        <operatingSystemVersion>[unassigned]</operatingSystemVersion>" \
              "        <pricePerUnit>-1.0</pricePerUnit>" \
              "        <priceTimeUnit>-1</priceTimeUnit>" \
              "        <processors>" \
              "          <architecture>[unassigned]</architecture>" \
              "          <computingUnits>2</computingUnits>" \
              "          <internalMemory>-1.0</internalMemory>" \
              "          <name>[unassigned]</name>" \
              "          <propName>[unassigned]</propName>" \
              "          <propValue>[unassigned]</propValue>" \
              "          <speed>-1.0</speed>" \
              "          <type>CPU</type>" \
              "        </processors>" \
              "        <storageSize>-1.0</storageSize>" \
              "        <storageType>[unassigned]</storageType>" \
              "        <value>0.0</value>" \
              "        <wallClockLimit>-1</wallClockLimit>" \
              "      </description>" \
              "    </resource>" \
              "  </resources>" \
              "</startApplication>"
        LOG.debug("Lifecycle-Management: COMPSs adapter: start_job: [xml=" + xml + "]")

        res = requests.put("http://" + agent['url'] + ":" + str(agent['port']) + "/COMPSs/startApplication",
                           data=xml,
                           headers={'Content-Type': 'application/xml'})
        LOG.debug("Lifecycle-Management: COMPSs adapter: start_job: [res=" + str(res) + "]")

        return True
    except:
        traceback.print_exc(file=sys.stdout)
        LOG.error('Lifecycle-Management: COMPSs adapter: start_job: Exception')
        return False


# start_job_in_agents: Start app in COMPSs container (more than one agent involved in the execution of this job)
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
def start_job_in_agents(service_instance, parameters):
    LOG.debug("Lifecycle-Management: COMPSs adapter: start_job_in_agents: [service_instance=" + str(service_instance) + "], "
              "[parameters=" + parameters + "]")
    try:
        xml = "<?xml version='1.0' encoding='utf-8'?>" \
              "<startApplication>" + parameters + "<resources>" \
              "   <resource name=\"" + service_instance['agents'][0]['url'] + ":8080\">" \
              "      <description>" \
              "        <memorySize>4.0</memorySize>" \
              "        <memoryType>[unassigned]</memoryType>" \
              "        <operatingSystemDistribution>[unassigned]</operatingSystemDistribution>" \
              "        <operatingSystemType>[unassigned]</operatingSystemType>" \
              "        <operatingSystemVersion>[unassigned]</operatingSystemVersion>" \
              "        <pricePerUnit>-1.0</pricePerUnit>" \
              "        <priceTimeUnit>-1</priceTimeUnit>" \
              "        <processors>" \
              "          <architecture>[unassigned]</architecture>" \
              "          <computingUnits>1</computingUnits>" \
              "          <internalMemory>-1.0</internalMemory>" \
              "          <name>[unassigned]</name>" \
              "          <propName>[unassigned]</propName>" \
              "          <propValue>[unassigned]</propValue>" \
              "          <speed>-1.0</speed>" \
              "          <type>CPU</type>" \
              "        </processors>" \
              "        <storageSize>-1.0</storageSize>" \
              "        <storageType>[unassigned]</storageType>" \
              "        <value>0.0</value>" \
              "        <wallClockLimit>-1</wallClockLimit>" \
              "      </description>" \
              "    </resource>" \
              "   <resource name=\"" + service_instance['agents'][1]['url'] + ":8080\">" \
              "      <description>" \
              "        <memorySize>4.0</memorySize>" \
              "        <memoryType>[unassigned]</memoryType>" \
              "        <operatingSystemDistribution>[unassigned]</operatingSystemDistribution>" \
              "        <operatingSystemType>[unassigned]</operatingSystemType>" \
              "        <operatingSystemVersion>[unassigned]</operatingSystemVersion>" \
              "        <pricePerUnit>-1.0</pricePerUnit>" \
              "        <priceTimeUnit>-1</priceTimeUnit>" \
              "        <processors>" \
              "          <architecture>[unassigned]</architecture>" \
              "          <computingUnits>1</computingUnits>" \
              "          <internalMemory>-1.0</internalMemory>" \
              "          <name>[unassigned]</name>" \
              "          <propName>[unassigned]</propName>" \
              "          <propValue>[unassigned]</propValue>" \
              "          <speed>-1.0</speed>" \
              "          <type>CPU</type>" \
              "        </processors>" \
              "        <storageSize>-1.0</storageSize>" \
              "        <storageType>[unassigned]</storageType>" \
              "        <value>0.0</value>" \
              "        <wallClockLimit>-1</wallClockLimit>" \
              "      </description>" \
              "    </resource>" \
              "  </resources>" \
              "</startApplication>"
        LOG.debug("Lifecycle-Management: COMPSs adapter: start_job_in_agents: [xml=" + xml + "]")

        res = requests.put("http://" + service_instance['agents'][0]['url'] + ":" +
                                       str(service_instance['agents'][0]['port']) + "/COMPSs/startApplication",
                           data=xml,
                           headers={'Content-Type': 'application/xml'})
        LOG.debug("Lifecycle-Management: COMPSs adapter: start_job_in_agents: [res=" + str(res) + "]")

        return True
    except:
        traceback.print_exc(file=sys.stdout)
        LOG.error('Lifecycle-Management: COMPSs adapter: start_job_in_agents: Exception')
        return False