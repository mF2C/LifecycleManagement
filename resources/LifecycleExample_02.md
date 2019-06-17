# LifecycleManagement - GitLab application
[![version](https://img.shields.io/badge/version-1.2.7-blue.svg)]()

Deployment of a [GitLab](https://github.com/sameersbn/docker-gitlab) application (docker compose) in a mF2C Agent. This is a service based on a **docker compose** file.

Service definition:

```json
{
	"name": "docker_compose_app_1",
	"description": "docker-compose application",
	"exec": "https://raw.githubusercontent.com/sameersbn/docker-gitlab/master/docker-compose.yml",
  "sla_templates": ["sla-template/083e1759-4b66-4295-b187-37997feec013"],
	"os": "linux",
	"disk": 100,
	"category": 0,
	"num_agents": 1,
	"exec_type": "docker-compose",
	"exec_ports": [80],
	"agent_type": "normal",
	"cpu_arch": "x86-64",
	"memory_min": 1000,
	"storage_min": 100,
	"req_resource": [],
	"opt_resource": []
}

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
sudo docker pull sameersbn/gitlab:11.11.2
sudo docker pull sameersbn/postgresql:10
sudo docker pull sameersbn/redis:4.0.9-1
sudo docker pull docker/compose:1.24.0
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
	\"name\": \"docker_compose_app_1\",
	\"description\": \"docker-compose application\",
	\"exec\": \"https://raw.githubusercontent.com/sameersbn/docker-gitlab/master/docker-compose.yml\",
  \"sla_templates\": [\"sla-template/461de863-75f4-453f-b60e-932be8df6e69\"],
	\"os\": \"linux\",
	\"disk\": 100,
	\"category\": 0,
	\"num_agents\": 1,
	\"exec_type\": \"docker-compose\",
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

This examples shows the deployment of a docker-compose application in mF2C. The docker compose yaml file is downloaded from the following URL:
https://raw.githubusercontent.com/sameersbn/docker-gitlab/master/docker-compose.yml

--------------------------------------------------------------------------

### 1. Submit the service (create a **service instance**)

In order to submit a service, use the following method:

REQUEST:

```
POST /api/v2/lm/service
```

REQUEST BODY:

Use the service and sla template identifiers obtained in the previuos steps. The request body should look like that:

```json
{
	"service_id": "service/21c66db9-49b5-45cc-8e3a-1230a30435a0",
	"sla_template": "sla-template/461de863-75f4-453f-b60e-932be8df6e69"
}
```

If the `service id` is not included in the request body, then this body requires a `service` object. As an alternative you can specify a list of `agents` (agents_list) where this service will be deployed. For `DOCKER-COMPOSE applications` the service definition has to include the following properties:

  - `exec` _YAML URL_ (URL of the Docker Compose file definition)
```json
{
	"service": {
		"name": "docker_compose_app_1",
		"description": "docker-compose application",
		"exec": "https://raw.githubusercontent.com/sameersbn/docker-gitlab/master/docker-compose.yml",
	  "sla_templates": ["sla-template/083e1759-4b66-4295-b187-37997feec013"],
		"os": "linux",
		"disk": 100,
		"category": 0,
		"num_agents": 1,
		"exec_type": "docker-compose",
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

If deployment was successful, the response includes the id of the new **service instance**, and for each of the agents, it also includes the container identifiers.

```json
{
  "error": false,
  "service_instance": {
    "status": "started",
    "updated": "2018-05-07T12:21:46.556964Z",
    "created": "2018-05-07T12:21:44.981Z",
    "agreement": "not-defined",
    "service": "docker_compose_app_1",
    "acl": {
      "rules": [
        {
          "right": "ALL",
          "principal": "user",
          "type": "ROLE"
        },
        {
          "right": "ALL",
          "principal": "ANON",
          "type": "ROLE"
        }
      ],
      "owner": {
        "principal": "user",
        "type": "ROLE"
      }
    },
    "operations": [
      {
        "href": "service-instance/f1bcf627-99cb-4138-a429-b44c5645e6a6",
        "rel": "edit"
      },
      {
        "href": "service-instance/f1bcf627-99cb-4138-a429-b44c5645e6a6",
        "rel": "delete"
      }
    ],
    "agents": [
      {
        "agent": {
          "href": "agent/default-value"
        },
        "allow": true,
        "status": "started",
        "port": 9876,
        "url": "192.168.111.111",
        "num_cpus": 4,
        "container_id": "8259ec5ce1c97c0ce0e12e671f532b6fe44c015ee422ec10320df180a0e6da38"
      }
    ],
    "resourceURI": "http://schemas.dmtf.org/cimi/2/ServiceInstance",
    "id": "service-instance/f1bcf627-99cb-4138-a429-b44c5645e6a6",
    "user": "user"
  },
  "message": "Deploy service"
}
```

Check the values of the agents: the `status` of the containers should be 'started', and the content of `container_id` should be something like '8259ec5ce1c97c0ce0e12e671f532b6fe44c015ee422ec10320df180a0e6da38'.

Service instance ID is needed for the following steps: `f1bcf627-99cb-4138-a429-b44c5645e6a6`

--------------------------------------------------------------------------

### 2. Start the service -GitLab-

1. Check that GitLab can be accessed from http://192.168.111.111:10080/

2. `sudo docker ps` should show something like the following:

```bash
CONTAINER ID        IMAGE                        COMMAND                  CREATED             STATUS              PORTS                                                   NAMES
2da8f57e5185        sameersbn/gitlab:10.7.2      "/sbin/entrypoint...."   4 minutes ago       Up 4 minutes        443/tcp, 0.0.0.0:10022->22/tcp, 0.0.0.0:10080->80/tcp   compose_examples_gitlab_1
d977725144de        sameersbn/postgresql:9.6-2   "/sbin/entrypoint.sh"    4 minutes ago       Up 4 minutes        5432/tcp                                                compose_examples_postgresql_1
cfb6ff199979        sameersbn/redis:latest       "/sbin/entrypoint...."   4 minutes ago       Up 4 minutes        6379/tcp                                                compose_examples_redis_1
8259ec5ce1c9        docker/compose:1.21.0        "docker-compose up"      4 minutes ago       Up 4 minutes                                                                docker_compose_app-b0aad05e-4f70-4977-bce2-c280d76c874c
b2128b5b977f        lm-app           
```

--------------------------------------------------------------------------

### 3. Stop the service instance

The following method stops the service instance.

REQUEST:

```
PUT /api/v1/lifecycle
```

REQUEST BODY:

```json
{"service_instance_id":"f1bcf627-99cb-4138-a429-b44c5645e6a6",
"operation":"stop"}
```

RESPONSE:

```json
{
  "error": false,
  "service_instance_id": "f1bcf627-99cb-4138-a429-b44c5645e6a6",
  "service_instance": "{'status': 'stopped', 'updated': '2018-05-07T12:32:21.401937Z', 'created': '2018-05-07T12:21:44.981Z', 'agreement': 'not-defined', 'service': 'docker_compose_app_2', 'acl': {'rules': [{'right': 'ALL', 'principal': 'user', 'type': 'ROLE'}, {'right': 'ALL', 'principal': 'ANON', 'type': 'ROLE'}], 'owner': {'principal': 'user', 'type': 'ROLE'}}, 'operations': [{'href': 'service-instance/f1bcf627-99cb-4138-a429-b44c5645e6a6', 'rel': 'edit'}, {'href': 'service-instance/f1bcf627-99cb-4138-a429-b44c5645e6a6', 'rel': 'delete'}], 'agents': [{'agent': {'href': 'agent/default-value'}, 'allow': True, 'status': 'stopped', 'url': '192.168.111.111', 'port': 9876, 'num_cpus': 4, 'container_id': '8259ec5ce1c97c0ce0e12e671f532b6fe44c015ee422ec10320df180a0e6da38'}], 'resourceURI': 'http://schemas.dmtf.org/cimi/2/ServiceInstance', 'id': 'service-instance/f1bcf627-99cb-4138-a429-b44c5645e6a6', 'user': 'user'}",
  "message": "stop service"
}
```

--------------------------------------------------------------------------

### 4. Terminate the service instance

After stopping the service, the service instance can be terminated and removed from `cimi`.

REQUEST:

```
DELETE /api/v1/lifecycle
```

REQUEST BODY:

```json
{"service_instance_id":"f1bcf627-99cb-4138-a429-b44c5645e6a6"}

RESPONSE:

```json
{
  "error": false,
  "service_instance_id": "f1bcf627-99cb-4138-a429-b44c5645e6a6",
  "service_instance": "{'service': 'docker_compose_app_2', 'agents': [{'agent': {'href': 'agent/default-value'}, 'allow': True, 'status': 'terminated', 'url': '192.168.111.111', 'port': 9876, 'num_cpus': 4, 'container_id': '8259ec5ce1c97c0ce0e12e671f532b6fe44c015ee422ec10320df180a0e6da38'}], 'status': 'terminated', 'operations': [{'href': 'service-instance/f1bcf627-99cb-4138-a429-b44c5645e6a6', 'rel': 'edit'}, {'href': 'service-instance/f1bcf627-99cb-4138-a429-b44c5645e6a6', 'rel': 'delete'}], 'updated': '2018-05-07T12:39:58.682Z', 'user': 'user', 'acl': {'rules': [{'right': 'ALL', 'principal': 'user', 'type': 'ROLE'}, {'right': 'ALL', 'principal': 'ANON', 'type': 'ROLE'}, {'right': 'ALL', 'principal': 'ADMIN', 'type': 'ROLE'}], 'owner': {'principal': 'user', 'type': 'ROLE'}}, 'resourceURI': 'http://schemas.dmtf.org/cimi/2/ServiceInstance', 'id': 'service-instance/f1bcf627-99cb-4138-a429-b44c5645e6a6', 'created': '2018-05-07T12:21:44.981Z', 'agreement': 'not-defined'}",
  "message": "terminate service"
}
```
