# LifecycleManagement - GitLab application

Deployment of a [GitLab](https://github.com/sameersbn/docker-gitlab) application (docker compose) in a mF2C Agent. This is a service based on a docker compose file.

Service definition:

```json
{
	"id": "docker_compose_app_1",
	"name": "docker_compose_app",
	"description": "docker_compose Service",
	"resourceURI": "/docker_compose_app",
	"exec": "https://raw.githubusercontent.com/sameersbn/docker-gitlab/master/docker-compose.yml",
	"exec_type": "docker-compose",
	"exec_ports": [],
	"category": {
		"cpu": "low",
		"memory": "low",
		"storage": "low",
		"inclinometer": false,
		"temperature": false,
		"jammer": false,
		"location": false
	}
}
```

--------------------------------------------------------------------------

### Launch Lifecycle Management module (STANDALONE MODE)

```bash
sudo docker run --env CIMI_URL=https://cimi_url/api --env STANDALONE_MODE=True --env CIMI_USER="user" --env CIMI_PASSWORD="password" --env HOST_IP="192.168.111.111" -v /var/run/docker.sock:/var/run/docker.sock -v /home/user/mF2C/compose_examples:/home/user/mF2C/compose_examples -p 46000:46000 mf2c/lifecycle
```

Application URL: https://192.168.111.111:46000/api/v1/lifecycle.html

The lifecycle offers a Swagger UI that allows anyone to visualize and interact with the API’s resources without having any of the implementation logic in place.

--------------------------------------------------------------------------

## Example 1

This examples shows the deployment of a docker-compose application in mF2C. The docker compose yaml file is downloaded from the following URL:
https://raw.githubusercontent.com/sameersbn/docker-gitlab/master/docker-compose.yml

--------------------------------------------------------------------------

### 1. Submit the service (create a **service instance**)

In order to submit a service, use the following method:

REQUEST:

```
POST /api/v1/lifecycle
```

REQUEST BODY:

The body of this request requires a `service` object, the `user` (user_id) that launches this service, and the list of `agents` (agents_list) where this service will be deployed.

  - `exec` URL of the _docker-compose.yml_ file  
  - `exec_type`_docker-compose_

```json
{
	"service": {
		"id": "docker_compose_app_1",
		"name": "docker_compose_app",
		"description": "docker_compose Service",
		"resourceURI": "/docker_compose_app",
		"exec": "https://raw.githubusercontent.com/sameersbn/docker-gitlab/master/docker-compose.yml",
		"exec_type": "docker-compose",
		"exec_ports": [],
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
	"service_id": "docker_compose_app_1",
	"user_id": "user",
	"agreement_id": "not-defined",
	"operation": "not-defined",
	"agents_list": [{"agent_ip": "192.168.111.111", "num_cpus": 4}]
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

Check the values of the agents: the `status` of the containers should be 'started', and the content of `container_id``should be something like '8259ec5ce1c97c0ce0e12e671f532b6fe44c015ee422ec10320df180a0e6da38'.

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
