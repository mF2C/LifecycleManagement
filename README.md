# (micro)LifecycleManagement
Platform Controller - Lifecycle Management module (microagent version)

[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)

&copy; Atos Spain S.A. 2017

The Lifecycle Management module is a component of the European Project mF2C.

-----------------------

[Description](#description)

[Component architecture](#component-architecture)

[Installation Guide](#installation-guide)

[Usage Guide](#usage-guide)

[Relation to other mF2C components](#relation-to-other-mf2c-components)

[LICENSE](#license)

-----------------------

### Description

The Lifecycle Management component is responsible for managing the lifecycle of the applications to be executed by the mF2C infrastructure.
This includes the initialization, the submission and the termination of these applications, among other operations.

The Lifecycle Manager can deploy services in agents with Docker, Docker Swarm and Kubernetes. Services deployed in Docker engines can be normal docker images or _docker-compose_ files.

This version is specific for mF2C microagents, and some of the funcionalities of the LM have been removed or disabled.

-----------------------

### Component architecture

This component is part of the Platform Manager's Service Orchestration module:

![Platform Manager](resources/pm.png)

-----------------------

### Installation Guide

#### 1. Requirements

This component can be installed as a standalone component, or as part of mF2C. To install it as a standalone component you just need the following:

1. [Docker](https://docs.docker.com/install/)

**Dockerfile** content:

```
FROM armhf/python:3.4-alpine

ADD ./Lifecycle/ /code
WORKDIR /code
RUN pip install -r requirements.txt
EXPOSE 46000
CMD ["python", "app.py"]

```

To install as part of mF2C see **mF2C/mF2C** [repository](https://github.com/mF2C/mF2C)

To run the component without Docker, you will need the following:

1. Python 3.4

#### 2. Install

###### 2.1. Get Docker image from **Docker Hub**

1. Pull image:

```bash
docker pull mf2c/lifecycle
```

2. Run application and expose port `46000`:

```bash
sudo docker run -p 46000:46000 mf2c/lifecycle
```

Read [Usage Guide](#usage-guide) section to see how to properly start the component.

###### 2.2. Get repository

1. Clone / download repository

```bash
git clone https://github.com/mF2C/LifecycleManagement.git
```

2. Go to LifecycleManagement folder

```bash
cd LifecycleManagement
```

3. Build application:

```bash
sudo docker build -t lm-arm .
```

4. Run application and expose port `46000`:

```bash
sudo docker run -p 46000:46000 lm-arm
```

<p style="color:red; font-weight: bold">NOTE: Read next section to see how to properly start the component.</p>

-----------------------

### Usage Guide

1. Start the Lifecycle Management module with access to the docker socket ('-v /var/run/docker.sock:/var/run/docker.sock')

```bash
sudo docker run -v /var/run/docker.sock:/var/run/docker.sock -p 46000:46000 lm-arm
```
  - Available environment variables:
    - **STANDALONE_MODE** `False` if working in an agent with other mF2C components; `True` if working without external dependencies (except docker)
    - **CIMI_URL**
    - **HOST_IP** Machine's IP address: needed by the lifecycle when deploying services in a set of agents (to see if an agent is in local host or if it is in another machine)
    - **CIMI_USER** CIMI user
    - **WORKING_DIR_VOLUME** _docker-compose.yml_ folder

  Example:

  ```bash
  sudo docker run -v /var/run/docker.sock:/var/run/docker.sock --env HOST_IP=192.192.192.192 -p 46000:46000 mf2c/lifecycle
  ```

  2. Methods exposed by the REST API

  - List of methods:
    - **/api/v2**
      - GET _get rest api service status_
    - **/api/v2/lm/agent-config**
      - GET _get agent's lifecycle configuration: docker, docker-swarm, kubernetes, ..._
    - **/api/v2/lm/service-instance-int** (_internal calls_)
      - POST _Submits a service in a mF2C agent_
        - PUT _starts / stops ... a service in a mF2C agent; start-job_

3. After launching the Lifecycle Management module, the REST API services can be accessed at port 46000:
    - List of services (json): _https://localhost:46000/api/v2/lm_
    - List of services (swagger ui): _https://localhost:46000/api/v2/lm.html_

-----------------------

### Relation to other mF2C components

The (micro)**Lifecycle** Management module is connected with the following mF2C components:

- Is called by the following modules / components:
    - _Lifecycle_: Lifecycle from a leader agent may contact this (micro)Lifecycle to deploy and manage services

-----------------------

### LICENSE

The Lifecycle application is licensed under [Apache License, version 2](LICENSE.TXT).
