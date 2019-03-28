# LifecycleManagement - COMPSs application

Deployment and lifecycle management of an application based on **COMPSs** (docker image that includes COMPSs and the appication)

Service definition:

```json
{
		"id": "service/9fbfd7cd-4154-450e-aeab-7a6b84153206",
		"name": "compss-test",
		"description": "compss app",
		"exec_type": "compss",
		"exec_ports": [
			46100,
			46101,
			46102,
			46103
		],
		"num_agents": 2,
		"os": "linux",
		"disk": 100,
		"category": 0,
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
sudo docker pull mf2c/compss-test:latest
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

When working with other components of the mF2C platform, the request body should look like that:

```json
{
	"service_id": "service/6d1ba52b-4ce7-4333-914f-e434ddeeb591",
	"user_id": "user/testuser1",
	"agreement_id": "agreement/a7a30e2b-2ba1-4370-a1d4-af85c30d8713",
	"agents_list": [{
			"agent_ip": "192.168.252.41"
		}
	]
}
```

If the `service id` is not included in the request body, then this body requires a `service` object. Apart from that, the `user` (user_id) that launches this service, and the `agreement_id` are also needed. As an alternative you can specify the list of `agents` (agents_list) where this service will be deployed. For COMPSs applications the service definition has to include the following properties:

  - `exec` _mf2c/compss-agent:latest_ or any other docker COMPSs image from a public docker hub
  - `exec_type`_compss_

Or

```json
{
	"service": {
		"name": "compss-test",
		"description": "compss app",
		"exec_type": "compss",
		"exec_ports": [
			46100,
			46101,
			46102,
			46103
		],
		"num_agents": 2,
		"os": "linux",
		"disk": 100,
		"category": 0,
		"agent_type": "normal",
		"cpu_arch": "x86-64",
		"memory_min": 1000,
		"storage_min": 100,
		"req_resource": [],
		"opt_resource": []
	},
	"user_id": "user/testuser1",
	"agreement_id": "agreement/a7a30e2b-2ba1-4370-a1d4-af85c30d8713",
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
PUT /api/v2/service-instance/2f6da0d0-e1e9-44fb-b03f-4259ce55a8f7
```

REQUEST BODY:

```json
{
	"operation":"start-job",
	"parameters":"<ceiClass>es.bsc.compss.test.TestItf</ceiClass><className>es.bsc.compss.test.Test</className><methodName>main</methodName><parameters><params paramId='0'><direction>IN</direction><type>OBJECT_T</type><array paramId='0'><componentClassname>java.lang.String</componentClassname><values><element paramId='0'><className>java.lang.String</className><value xmlns:xsi='http://www.w3.org/2001/XMLSchema-instance' xmlns:xs='http://www.w3.org/2001/XMLSchema' xsi:type='xs:string'>3</value></element></values></array></params></parameters>"
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

The logs of the docker COMPSs containers should contain the following:

**MASTER**:

```bash
[(1246547)    API]  -  Creating task from method load in es.bsc.compss.agent.loader.Loader
[(1246547)    API]  -  There are 7 parameters
[(1246547)    API]  -    Parameter 1 has type OBJECT_T
[(1246547)    API]  -    Parameter 2 has type OBJECT_T
[(1246547)    API]  -    Parameter 3 has type STRING_T
[(1246547)    API]  -    Parameter 4 has type LONG_T
[(1246548)    API]  -    Parameter 5 has type STRING_T
[(1246548)    API]  -    Parameter 6 has type STRING_T
[(1246548)    API]  -    Parameter 7 has type OBJECT_T
[(1246684)    API]  -  Starting COMPSs Runtime v2.2.rc1803 (build 20180504-1041.r93a44b963732a109ae56e0957e448cd1d3dc8749)
[(1246684)    API]  -  Initializing es.bsc.compss.test.TestItf
Variables set
Types:  [class [Ljava.lang.String;]
Params: [[Ljava.lang.String;@7fbc386b]
Received a service invocation creating 3 tasks.
[(1246700)    API]  -  Creating task from method test in es.bsc.compss.test.Test
[(1246700)    API]  -  There is 1 parameter
[(1246700)    API]  -    Parameter 1 has type INT_T
[(1246700)    API]  -  Creating task from method test in es.bsc.compss.test.Test
[(1246701)    API]  -  There is 1 parameter
[(1246701)    API]  -    Parameter 1 has type INT_T
[(1246701)    API]  -  Creating task from method test in es.bsc.compss.test.Test
[(1246701)    API]  -  There is 1 parameter
[(1246701)    API]  -    Parameter 1 has type INT_T
[(1246701)    API]  -  No more tasks for app 1357508865803972598
[(1254378)    API]  -  Getting Result Files 1357508865803972598
Execution lasted 7837
Publishing result of an operation execution:
{"serviceInstance":{"href":"service-instance/null"},"operation":"main","execution_time":7837.0,"acl":{"owner":{"principal":"ADMIN","type":"ROLE"},"rules":[{"principal":"USER","right":"MODIFY","type":"ROLE"},{"principal":"ADMIN","right":"ALL","type":"ROLE"}]}}
```

**WORKER**:

```bash
2018-05-08 10:01:00.880:INFO:oejsh.ContextHandler:APPLICATION: Started o.e.j.s.ServletContextHandler@34cdeda2{/,null,AVAILABLE}
2018-05-08 10:01:00.898:INFO:oejs.ServerConnector:APPLICATION: Started ServerConnector@5311b9f6{HTTP/1.1}{0.0.0.0:46100}
2018-05-08 10:01:00.898:INFO:oejs.Server:APPLICATION: Started @2040ms
Running Task 4466134303511434428
[(1228603)    API]  -  Registering CoreElement test(OBJECT_T)
[(1228604)    API]  -    - Implementation: test(OBJECT_T)es.bsc.compss.test.Test
[(1228604)    API]  -    - Constraints   :
[(1228605)    API]  -    - Type          : METHOD
[(1228605)    API]  -    - ImplTypeArgs  :
[(1228605)    API]  -            Arg: es.bsc.compss.test.Test
[(1228606)    API]  -            Arg: test
[(1228613)    API]  -  Creating task from method test in es.bsc.compss.test.Test
[(1228613)    API]  -  There is 1 parameter
[(1228614)    API]  -    Parameter 1 has type OBJECT_T
Executing task 1 which lasts 1000 ms.
Running Task 4382260945185475773
[(1229824)    API]  -  Registering CoreElement test(OBJECT_T)
[(1229824)    API]  -    - Implementation: test(OBJECT_T)es.bsc.compss.test.Test
[(1229824)    API]  -    - Constraints   :
[(1229824)    API]  -    - Type          : METHOD
[(1229825)    API]  -    - ImplTypeArgs  :
[(1229825)    API]  -            Arg: es.bsc.compss.test.Test
[(1229825)    API]  -            Arg: test
[(1229828)    API]  -  Creating task from method test in es.bsc.compss.test.Test
[(1229828)    API]  -  There is 1 parameter
[(1229828)    API]  -    Parameter 1 has type OBJECT_T
Executing task 2 which lasts 2000 ms.
Running Task 2580548301657135571
[(1231868)    API]  -  Registering CoreElement test(OBJECT_T)
[(1231869)    API]  -    - Implementation: test(OBJECT_T)es.bsc.compss.test.Test
[(1231869)    API]  -    - Constraints   :
[(1231869)    API]  -    - Type          : METHOD
[(1231869)    API]  -    - ImplTypeArgs  :
[(1231869)    API]  -            Arg: es.bsc.compss.test.Test
[(1231869)    API]  -            Arg: test
[(1231874)    API]  -  Creating task from method test in es.bsc.compss.test.Test
[(1231874)    API]  -  There is 1 parameter
[(1231874)    API]  -    Parameter 1 has type OBJECT_T
Executing task 3 which lasts 3000 ms.
```


--------------------------------------------------------------------------

### 4. Stop the service

The following method stops the service.

REQUEST:

```
PUT /api/v2/service-instance/2f6da0d0-e1e9-44fb-b03f-4259ce55a8f7
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
DELETE /api/v2/service-instance/2f6da0d0-e1e9-44fb-b03f-4259ce55a8f7
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
GET /api/v2/service-instance/all
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
