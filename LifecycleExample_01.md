# LifecycleManagement - Examples

### Launch Lifecycle Management module (STANDALONE MODE)

```bash
sudo docker run --env CIMI_URL=https://cimi_url/api --env STANDALONE_MODE=True --env CIMI_USER="user" --env CIMI_PASSWORD="password" --env HOST_IP="192.168.111.111" -v /var/run/docker.sock:/var/run/docker.sock -v /home/user/mF2C/compose_examples:/home/user/mF2C/compose_examples -p 46000:46000 mf2c/lifecycle
```

Application URL: https://192.168.192.192:46000/api/v1/lifecycle.html

The lifecycle offers a Swagger UI that allows anyone to visualize and interact with the API’s resources without having any of the implementation logic in place.

--------------------------------------------------------

## Example 1

This examples shows the lifecycle of a COMPSs application/service (`mf2c/compss-mf2c:1.0`) in mF2C. The Lifecycle Management module first deploys this COMPSs docker image in all selected agents. Then, it starts a container (COMPSs) in each of these agents. And then it launches a job in these COMPSs containers. Finally, the Lifecycle Management module stops the service, and shutdowns the containers.

### 1. Get all service instances

This method returns all existing service instances.

REQUEST:

```
GET /api/v1/lifecycle/service-instance/all
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

### 2. Submit a service

In order to submit a service, use the following method:

REQUEST:

```
POST /api/v1/lifecycle
```

REQUEST BODY:

The body of this request requires a `service` object, the `user` (user_id) that launches this service, and the list of `agents` (agents_list) where this service will be deployed.

```json
{
	"service": {
		"id": "service_v2_test_01",
		"name": "app-compss",
		"description": "app-compss Service",
		"resourceURI": "/app-compss",
		"exec": "mf2c/compss-mf2c:1.0",
		"exec_type": "docker",
		"exec_ports": [8080, 8081],
		"category": {
			"cpu": "low",
			"memory": "low",
			"storage": "low",
			"inclinometer": false,
			"temperature": false,
			"jammer": false,
			"location": false
		}
	},
	"service_id": "service_v2_test_01",
	"user_id": "user",
	"agreement_id": "not-defined",
	"operation": "stop",
	"agents_list": [
		{"agent_ip": "192.168.192.192", "num_cpus": 4}]
}
```

RESPONSE:

If deployment was successful, the response includes the id of the new service instance, and for each of the agents, it includes the container identifiers.

```json
  "service_instance": {
    "created": "2018-04-23T12:53:35.575Z",
    "resourceURI": "http://schemas.dmtf.org/cimi/2/ServiceInstance",
    "service": "service_v2_test_01",
    "updated": "2018-04-23T12:53:36.198791Z",
    "agents": [
      {
        "status": "waiting",
        "num_cpus": 4,
        "url": "192.168.192.192",
        "port": 8080,
        "allow": true,
        "agent": {
          "href": "agent/default-value"
        },
        "container_id": "57c39fbe9adc8525b09d5074b0e197126fb836bbf525986d9dc46df3583f6511"
      }
    ],
    "user": "user",
    "agreement": "not-defined",
    "status": "not-defined",
    "id": "service-instance/3a1faff6-59dd-47eb-a052-9a773856a706",
    "acl": {
      "owner": {
        "type": "ROLE",
        "principal": "user"
      },
      "rules": [
        {
          "right": "ALL",
          "type": "ROLE",
          "principal": "user"
        },
        {
          "right": "ALL",
          "type": "ROLE",
          "principal": "ANON"
        }
      ]
    },
    "operations": [
      {
        "href": "service-instance/3a1faff6-59dd-47eb-a052-9a773856a706",
        "rel": "edit"
      },
      {
        "href": "service-instance/3a1faff6-59dd-47eb-a052-9a773856a706",
        "rel": "delete"
      }
    ]
  },
  "message": "Deploy service",
  "error": false
}
```

### 3. Start a service

To start a service...

REQUEST:

```
PUT /api/v1/lifecycle
```

REQUEST BODY:

```json
{"service_instance_id":"3a1faff6-59dd-47eb-a052-9a773856a706",
"operation":"start"}
```

RESPONSE:

```
...
```

### 4. Start a job

REQUEST:

```
GET /api/v1/lifecycle/service-instance/all
```

REQUEST BODY:

The body requires the part of the `XML` needed by the COMPSs service. This part should be included in the `parameters` field.

```json
{
  "service_instance_id":"3a1faff6-59dd-47eb-a052-9a773856a706",
  "operation":"start-job",
  "parameters":"<ceiClass>es.bsc.compss.test.TestItf</ceiClass><className>es.bsc.compss.test.Test</className><methodName>main</methodName><parameters><array paramId='0'><componentClassname>java.lang.String</componentClassname><values><element paramId='0'><className>java.lang.String</className><value xmlns:xsi='http://www.w3.org/2001/XMLSchema-instance' xmlns:xs='http://www.w3.org/2001/XMLSchema' xsi:type='xs:string'>3</value></element></values></array></parameters>"
}
```

RESPONSE:

```
...
```

### 5. Get all service instances / service information

REQUEST:

```
GET /api/v1/lifecycle/service-instance/all
```

RESPONSE:

```json
{
  "error": false,
  "message": "Service instances content",
  "service_instances": [
    {
      "service": "service_v2_test_01",
      "updated": "2018-04-23T12:02:27.353Z",
      "agreement": "agreement_temp_id",
      "created": "2018-04-23T12:02:27.353Z",
      "status": "not-defined",
      "id": "service-instance/3a1faff6-59dd-47eb-a052-9a773856a706",
      "acl": {
        "owner": {
          "principal": "user",
          "type": "ROLE"
        },
        "rules": [
          {
            "principal": "user",
            "type": "ROLE",
            "right": "ALL"
          },
          {
            "principal": "ANON",
            "type": "ROLE",
            "right": "ALL"
          },
          {
            "type": "ROLE",
            "principal": "ADMIN",
            "right": "ALL"
          }
        ]
      },
      "operations": [
        {
          "rel": "edit",
          "href": "service-instance/3a1faff6-59dd-47eb-a052-9a773856a706"
        },
        {
          "rel": "delete",
          "href": "service-instance/3a1faff6-59dd-47eb-a052-9a773856a706"
        }
      ],
      "resourceURI": "http://schemas.dmtf.org/cimi/2/ServiceInstance",
      "agents": [
        {
          "agent": {
            "href": "agent/default-value"
          },
          "port": 8080,
          "url": "192.168.252.41",
          "status": "not-defined",
          "num_cpus": 4,
          "allow": true,
          "container_id": "-"
        }],
      "user": "rsucasas"
    }
  ],
  "Msg": ""
}
```

### 6. Stop a service

The following method stops the service, stops and removes the containers, and finally, deletes the service instance from `cimi`.

REQUEST:

```
PUT /api/v1/lifecycle
```

REQUEST BODY:

```json
{"service_instance_id":"11c9994d-1913-4213-9cb4-41ff0f9e46fe",
"operation":"stop"}
```

RESPONSE:

```json
{
  "service_instance": "{'status': 'not-defined', 'created': '2018-04-23T12:53:35.575Z', 'resourceURI': 'http://schemas.dmtf.org/cimi/2/ServiceInstance', 'user': 'user', 'id': 'service-instance/3a1faff6-59dd-47eb-a052-9a773856a706', 'updated': '2018-04-23T12:53:36.494Z', 'operations': [{'href': 'service-instance/3a1faff6-59dd-47eb-a052-9a773856a706', 'rel': 'edit'}, {'href': 'service-instance/3a1faff6-59dd-47eb-a052-9a773856a706', 'rel': 'delete'}], 'agents': [{'status': 'Stopped', 'num_cpus': 4, 'url': '192.168.252.41', 'port': 8080, 'allow': True, 'agent': {'href': 'agent/default-value'}, 'container_id': '57c39fbe9adc8525b09d5074b0e197126fb836bbf525986d9dc46df3583f6511'}], 'service': 'service_v2_test_01', 'acl': {'owner': {'type': 'ROLE', 'principal': 'user'}, 'rules': [{'right': 'ALL', 'type': 'ROLE', 'principal': 'user'}, {'right': 'ALL', 'type': 'ROLE', 'principal': 'ANON'}, {'right': 'ALL', 'type': 'ROLE', 'principal': 'ADMIN'}]}, 'agreement': 'not-defined'}",
  "message": "Stop service",
  "service_instance_id": "3a1faff6-59dd-47eb-a052-9a773856a706",
  "error": false
}
```

### 7. Get all service instances

After stopping the service, the service instance should be removed from `cimi`.

REQUEST:

```
GET /api/v1/lifecycle/service-instance/all
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
