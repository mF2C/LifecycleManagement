# LifecycleManagement - COMPSs application
[![version](https://img.shields.io/badge/version-1.2.7-blue.svg)]()

Deployment and lifecycle management of an application based on **COMPSs** (docker image that includes COMPSs and the application)

Service definition:

```json
{
	"name": "compss-test-it2-1",
	"description": "compss-test IT-2-4 v2",
	"exec": "mf2c/compss-test:it2.4",
  "sla_templates": ["sla-template/083e1759-4b66-4295-b187-37997feec013"],
	"os": "linux",
	"disk": 100,
	"category": 0,
	"num_agents": 1,
	"exec_type": "compss",
	"exec_ports": [80],
	"agent_type": "normal",
	"cpu_arch": "x86-64",
	"memory_min": 1000,
	"storage_min": 100,
	"req_resource": [],
	"opt_resource": []
}
```

--------------------------------------------------------------------------

### Launch mF2C Agent in a device

```bash
sudo docker-compose -p mf2c up
```

Lifecycle URL: https://_HOST_:46000/api/v2/lm.html

The Lifecycle offers a Swagger UI that allows anyone to visualize and interact with the API’s resources without having any of the implementation logic in place.

### Download docker images

Download the docker images used in this example to save time:

```bash
sudo docker pull mf2c/compss-test:it2.4
```

### Previous tasks

Before deploying and launching the COMPSs application follow next steps:

##### 1. create a User
```bash
curl -XPOST -k -H 'content-type:application/json' https://localhost/api/user -d '''
{
    "userTemplate": {
        "href": "user-template/self-registration",
        "password": "testpassword",
        "passwordRepeat" : "testpassword",
        "emailAddress": "your_email@",
        "username": "user_name"
    }
}'''
```

##### 2. create a SLA template

Use the resulting template id when creating the service (next step) and also when launching a service in mF2C.

```bash
curl -H "slipstream-authn-info: super ADMIN" -H "Content-type: application/json" -d "{
	\"id\": \"template_01\",
    \"name\": \"Template 01\",
    \"state\": \"started\",
    \"details\":{
        \"id\": \"template_01\",
        \"type\": \"template\",
        \"name\": \"service_name\",
        \"provider\": { \"id\": \"mf2c\", \"name\": \"mF2C Platform\" },
        \"client\": { \"id\": \"{{.user}}\", \"name\": \"{{.user}}\" },
        \"creation\": \"2018-01-16T17:09:45.01Z\",
        \"expiration\": \"2021-01-16T17:09:45.01Z\",
        \"guarantees\": [
            {
                \"name\": \"es.bsc.compss.agent.test.Test.main\",
                \"constraint\": \"execution_time < 1000\"
            }
        ]
    }
}"  -X POST https://localhost/api/sla-template --insecure
```

##### 3. create the service

Use the resulting service id when launching a service in mF2C.

```bash
curl -H "slipstream-authn-info: super ADMIN" -H "Content-type: application/json" -d "{
	\"name\": \"compss-test-it2-1\",
	\"description\": \"compss-test IT-2-4 v2\",
	\"exec\": \"mf2c/compss-test:it2.4\",
  \"sla_templates\": [\"sla-template/083e1759-4b66-4295-b187-37997feec013\"],
	\"os\": \"linux\",
	\"disk\": 100,
	\"category\": 0,
	\"num_agents\": 1,
	\"exec_type\": \"compss\",
	\"exec_ports\": [80],
	\"agent_type\": \"normal\",
	\"cpu_arch\": \"x86-64\",
	\"memory_min\": 1000,
	\"storage_min\": 100,
	\"req_resource\": [],
	\"opt_resource\": []
}" -X POST https://localhost/api/service --insecure
```

--------------------------------------------------------------------------

## Example

This examples shows the lifecycle of a COMPSs application/service (`mf2c/compss-mf2c:1.0`) in mF2C. The Lifecycle Management module first deploys this COMPSs docker image in all selected agents (2 agents). Then, it starts a container (COMPSs) in each of these agents. Then, it launches a job in these two COMPSs containers. Finally, the Lifecycle Management module stops the service, and shutdowns the containers.

--------------------------------------------------------------------------

### 1. Get all service instances

This method returns all existing service instances.

REQUEST:

```
GET /api/v2/lm/service-instances/all
```

RESPONSE:

```json
{
  "error": false,
  "message": "Service instances content",
  "service_instances": [],
  "Msg": ""
}
```

--------------------------------------------------------------------------

### 2. Submit a service

In order to submit (and start) a service, use the following method:

REQUEST:

```
POST /api/v2/lm/service
```

REQUEST BODY:

Use the service and sla template identifiers obtained in the previuos steps. The request body should look like that:

```json
{
	"service_id": "service/e9bb729e-9249-4189-aa7d-e827fea8a419",
	"sla_template": "sla-template/083e1759-4b66-4295-b187-37997feec013"
}
```

If the `service id` is not included in the request body, then this body requires a `service` object. As an alternative you can specify the list of `agents` (agents_list) where this service will be deployed. For `COMPSs applications` the service definition has to include the following properties:

  - `exec` _mf2c/compss-test:it2.4_ or any other docker COMPSs image from a public docker hub
  - `exec_type`_compss_

Or

```json
{
	"service": {
		"name": "compss-test-it2-1",
		"description": "compss-test IT-2-4 v2",
		"exec": "mf2c/compss-test:it2.4",
	  "sla_templates": ["sla-template/083e1759-4b66-4295-b187-37997feec013"],
		"os": "linux",
		"disk": 100,
		"category": 0,
		"num_agents": 1,
		"exec_type": "compss",
		"exec_ports": [80],
		"agent_type": "normal",
		"cpu_arch": "x86-64",
		"memory_min": 1000,
		"storage_min": 100,
		"req_resource": [],
		"opt_resource": []
	},
	"sla_template": "sla-template/083e1759-4b66-4295-b187-37997feec013",
	"agents_list": [
		{"agent_ip": "192.168.252.41", "num_cpus": 4}, {"agent_ip": "192.168.252.42", "num_cpus": 4}]
}
```

RESPONSE:

If deployment was successful, the response includes the id of the new service instance, and for each of the agents, it includes the container identifiers.

```json
{
  "service_instance": {
    "updated": "2018-05-08T10:00:58.397607Z",
    "agents": [
      {
        "port": 46100,
        "allow": true,
        "container_id": "fc6ecf2060c1a648d9376dab995543434f7b344bfcae9c178e02bde90d213777",
        "status": "started",
        "agent": {
          "href": "agent/default-value"
        },
        "url": "192.168.252.41",
        "master_compss": true,
        "num_cpus": 7
      },
      {
        "port": 46100,
        "allow": true,
        "container_id": "7d7acb04e1389c3a7242db40c005555c54340c7fce6a96647664ae7dd4659087",
        "status": "started",
        "agent": {
          "href": "agent/default-value"
        },
        "url": "192.168.252.42",
        "num_cpus": 7
      }
    ],
    "user": "user",
    "resourceURI": "http://schemas.dmtf.org/cimi/2/ServiceInstance",
    "acl": {
      "owner": {
        "type": "ROLE",
        "principal": "user"
      },
      "rules": [
        {
          "type": "ROLE",
          "right": "ALL",
          "principal": "user"
        },
        {
          "type": "ROLE",
          "right": "ALL",
          "principal": "ANON"
        }
      ]
    },
    "id": "service-instance/2f6da0d0-e1e9-44fb-b03f-4259ce55a8f7",
    "agreement": "not-defined",
    "operations": [
      {
        "rel": "edit",
        "href": "service-instance/2f6da0d0-e1e9-44fb-b03f-4259ce55a8f7"
      },
      {
        "rel": "delete",
        "href": "service-instance/2f6da0d0-e1e9-44fb-b03f-4259ce55a8f7"
      }
    ],
    "status": "started",
    "created": "2018-05-08T10:00:34.387Z",
    "service": "app_compss_test_01"
  },
  "message": "Deploy service",
  "error": false
}
```

Service instance ID is needed for the following steps: `2f6da0d0-e1e9-44fb-b03f-4259ce55a8f7`

--------------------------------------------------------------------------

### 3. Start a job in COMPSs

To start a job in COMPSs (1 master, 1 worker)...

REQUEST:

```
PUT /api/v2/lm/service-instance/2f6da0d0-e1e9-44fb-b03f-4259ce55a8f7/compss
```

REQUEST BODY:

```json
{
	"operation":"start-job",
	"ceiClass":"es.bsc.compss.agent.test.TestItf",
	"className":"es.bsc.compss.agent.test.Test",
	"hasResult":false,
	"methodName":"main",
	"parameters":" <params paramId=\"0\"> <direction>IN</direction> <stream>UNSPECIFIED</stream> <type>OBJECT_T</type> <array paramId=\"0\"> <componentClassname>java.lang.String</componentClassname> <values> <element paramId=\"0\"> <className>java.lang.String</className> <value xmlns:xsi=\"http://www.w3.org/2001/XMLSchema-instance\" xmlns:xs=\"http://www.w3.org/2001/XMLSchema\" xsi:type=\"xs:string\">3</value> </element> </values> </array> </params>"
}
```

RESPONSE:

```json
{
  "error": false,
  "service_id": "2f6da0d0-e1e9-44fb-b03f-4259ce55a8f7",
  "message": "Start job",
  "res": true
}
```

The result of the job execution is stored in **cimi**, and can be obtained with the following call:

##### 3.1 Get Service instance report

```
GET /api/v2/lm/service-instances/2f6da0d0-e1e9-44fb-b03f-4259ce55a8f7/report
```

--------------------------------------------------------------------------

### 4. Stop the service

The following method stops the service.

REQUEST:

```
PUT /api/v2/lm/service-instance/2f6da0d0-e1e9-44fb-b03f-4259ce55a8f7
```

REQUEST BODY:

```json
{"operation":"stop"}
```

RESPONSE:

```json
{
  "error": false,
  "service_instance_id": "2f6da0d0-e1e9-44fb-b03f-4259ce55a8f7",
  "service_instance": "{'status': 'stopped', ..., 'id': 'service-instance/2f6da0d0-e1e9-44fb-b03f-4259ce55a8f7', 'user': 'user'}",
  "message": "stop service"
}
```

--------------------------------------------------------------------------

### 5. Terminate the service instance

After stopping the service, the service instance can be terminated and removed from `cimi`.

REQUEST:

```
DELETE /api/v2/lm/service-instance/2f6da0d0-e1e9-44fb-b03f-4259ce55a8f7
```

RESPONSE:

```json
{
  "error": false,
  "service_instance_id": "2f6da0d0-e1e9-44fb-b03f-4259ce55a8f7",
  "service_instance": "{....}",
  "message": "terminate service"
}
```

--------------------------------------------------------------------------

### 6. Get all service instances

After stopping the service, the service instance should be removed from `cimi`.

REQUEST:

```
GET /api/v2/lm/service-instance/all
```

RESPONSE:

```
{
  "error": false,
  "message": "Service instances content",
  "service_instances": [],
  "Msg": ""
}
```
