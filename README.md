# LifecycleManagement
Platform Controller - Lifecycle Management module

[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)
[![version](https://img.shields.io/badge/version-1.2.7-blue.svg)]()

&copy; Atos Spain S.A. 2017

The Lifecycle Management module is a component of the European Project [mF2C](https://www.mf2c-project.eu/).

-----------------------

[Description](#description)

[Component architecture](#component-architecture)

[Installation Guide](#installation-guide)

[Usage Guide](#usage-guide)

[Relation to other mF2C components](#relation-to-other-mf2c-components)

[Resources managed by this component](#resources-managed-by-this-component)

[LICENSE](#license)

-----------------------

### Description

The Lifecycle Management component is responsible for managing the lifecycle of the applications to be executed by the mF2C infrastructure.
This includes the initialization, the submission and the termination of these applications, among other operations.

The Lifecycle Manager can deploy services in agents with Docker, Docker Swarm and Kubernetes. Services deployed in Docker engines can be normal docker images or _docker-compose_ files.

-----------------------

### Component architecture

This component is part of the Platform Manager's Service Orchestration module:

![Platform Manager](resources/pm.png)

-----------------------

### Installation Guide

#### 1. Requirements

1. Install [Docker](https://docs.docker.com/install/)


#### 2. Install and Run

This component can be installed as a standalone component, or as part of mF2C. To install it as a standalone component you just need the following:

- Clone repository

```bash
      git clone https://github.com/mF2C/LifecycleManagement.git
      cd LifecycleManagement
```

- Build the docker image:

```bash
      sudo docker build -t lifecycle .
```

The docker image can also be downloaded from docker hub (this image includes the [User Management module](https://github.com/mF2C/UserManagement)):

```bash
      sudo docker pull mf2c lifecycle-usermngt:latest
```

To install it as part of mF2C see **mF2C/mF2C** [repository](https://github.com/mF2C/mF2C)

Finally, to run the component without Docker, you will need **Python 3.4**.


###### 2.1. Launch the Lifecycle

Run application and expose port `46000`:

```bash
sudo docker run -p 46000:46000 lifecycle
```

To start the Lifecycle Management module with access to the docker socket ('-v /var/run/docker.sock:/var/run/docker.sock') run the following:

```bash
sudo docker run -v /var/run/docker.sock:/var/run/docker.sock -p 46000:46000 lifecycle
```

Available environment variables:
- **STANDALONE_MODE** `False` if working in an agent with other mF2C components; `True` if working without external dependencies (except docker)
- **CIMI_URL**
- **HOST_IP** Machine's IP address: needed by the lifecycle when deploying services in a set of agents (to see if an agent is in local host or if it is in another machine)
- **CIMI_USER** CIMI user
- **WORKING_DIR_VOLUME** _docker-compose.yml_ folder
- **URL_PM_SLA_MANAGER** URL of the Platform Manager - SLA Manager; e.g. https://192.168.192.192:46030
- **URL_AC_SERVICE_MNGMT** URL of the Agent Controller - QoS Providing; e.g. https://192.168.192.192:46200/api/service-management
- **URL_AC_USER_MANAGEMENT** URL of the Agent Controller - User Management; e.g. https://192.168.192.192:46300/api/v1/user-management
- **URL_PM_RECOM_LANDSCAPER** URL of the Platform Manager - Landscaper/Recommender; e.g. http://192.168.252.41:46020/mf2c
- **K8S_MASTER**
- **K8S_PROXY**
- **K8S_NAMESPACE**
- **DOCKER_SOCKET**
- **DOCKER_SWARM**

Example:

```bash
sudo docker run -v /var/run/docker.sock:/var/run/docker.sock --env HOST_IP=192.192.192.192 -p 46000:46000 mf2c/lifecycle
```

After launching the Lifecycle Management module, the REST API services can be accessed at port 46000:
- List of services (json): _https://localhost:46000/api/v2/lm_
- List of services (swagger ui): _https://localhost:46000/api/v2/lm.html_

-----------------------

### Usage Guide

The following methods are exposed by the Lifeycle REST API:

- **/api/v2**
  - GET _get rest api service status_

- **/api/v2/lm**
  - POST _SLA / User Management / QoS notifications_

- **/api/v2/lm/agent-config**
  - GET _get agent's lifecycle configuration: docker, docker-swarm, kubernetes, ..._

- **/api/v2/lm/check-agent-um**
  - GET _checks if device can run more apps - UP & SM policies (from 'local' User Management module)_

- **/api/v2/lm/check-agent-swarm**
  - GET _checks if device can run warm apps (from 'local' User Management module)_

- **/api/v2/lm/agent-um**

- **/api/v2/lm/service-instance/<string:service_instance_id>**
  - GET _get service instance / all service instances (from cimi)_
  - PUT _Starts / stops / restarts a service instance_
  - DELETE _terminates a service instance; deletes service instance (from cimi)_

- **/api/v2/lm/service-instance/<string:service_instance_id>/compss**
  - PUT _starts a job in COMPSs_

- **/api/v2/lm/service-instances/<string:service_instance_id>/report**
  - GET _get service instance report_

- **/api/v2/lm/service**
  - POST _Submits a service and gets a service instance_

- **/api/v2/lm/service-instance-int** (_internal calls between LMs from different agents_)
  - POST _Submits a service in a mF2C agent_
  - PUT _starts / stops ... a service in a mF2C agent; start-job_


View the following examples:
   - [COMPSs application](resources/LifecycleExample_01.md): Complete lifecycle of a service based on COMPSs
   - [NGINX server](resources/LifecycleExample_03.md): Deployment and lifecycle of a nginx server (single docker application)
   - [GitLab application](resources/LifecycleExample_02.md): Deployment of a service based on a docker-compose file

See also the user guide that can be found in _https://github.com/mF2C/Documentation/blob/master/documentation/user_guide/api.rst_

-----------------------

### Relation to other mF2C components

The **Lifecycle** Management module is connected with the following mF2C components:

- Is called by the following modules / components:
    - _User Management_: Lifecycle receives warnings from the User Management when the mF2C applications use more resources than allowed by the users
    - _QoS Enforcement_: The Lifecycles process the QoS Enforcement notifications to increase the number of agents executing a COMPSs job.

- Makes calls to the following modules / components:
    - _Analytics Engine_: The Lifecycle gets from this component the list of all available agents and resources where a service can be deployed
    - _Service Management_: The Lifecycle calls the Service Management module to know which of the agents from a list can be used to deploy a service
    - _User Management_: Lifecycle interacts with the User Management module to get the profile and sharing resources defined by the user in a device
    - _Distributed Execution Runtime / COMPSs_: The Lifecycle can launch COMPSs jobs
    - _SLA Manager_: Lifecycle calls the SLA Manager to start, stop and terminate the SLA agreement monitoring process


-----------------------

### Resources managed by this component

The Lifecycle creates and manages the service instances resource. These are the instances of the services that are deployed and launched in one or more mF2C agents. Each of the **Service Instance** resource contains the following properties:
- **user** : user that launches the service
- **device_id** : device that launches the service
- **device_ip** : device's IP address
- **parent_device_id** : leader / parent device
- **parent_device_ip** : parent's IP address
- **service** : service identifier (service running in the agents)
- **agreement** : agreement identifier
- **status** : status of the service
- **service_type** : type of service: docker, docker-compose, docker-swarm, kubernetes
- **agents**: (mF2C agents that are running this service)
  - **url** : agent IP address
  - **status** : status of the container or docker swarm service
  - **ports** : ports used / exposed by the container or docker swarm service
  - **container_id** : id from docker container or docker swarm service
  - **allow** : agent is allowed to deploy the container / service (set by the _service manager_ component)
  - **master_compss** : true if this agent is master (COMPSs)
  - **app_type** : type of service: docker, docker-compose, docker-swarm, kubernetes
  - **device_id** : device identifier
  - **compss_app_id** : COMPSs job id

-----------------------

### LICENSE

The Lifecycle application is licensed under [Apache License, version 2](LICENSE.TXT).
