# LifecycleManagement
Platform Controller - Lifecycle Management module

[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)

&copy; Atos Spain S.A. 2017

The Lifecycle Management module is a component of the European Project mF2C.

-----------------------

[Description](#description)

[Component architecture](#component-architecture)

[Installation Guide](#installation-guide)

[Usage Guide](#usage-guide)

[Relation to other mF2C components](#relation-to-other-mf2c-components)

-----------------------

### Description

The Lifecycle Management component is responsible for managing the lifecycle of the applications to be executed by the mF2C infrastructure.
This includes the initialization, the submission and the termination of these applications, among other operations.

-----------------------

### Component architecture

This component is part of the Platform Manager's Service Orchestration module:

![Platform Manager](docresources/pm.png)

-----------------------

### Installation Guide

#### 1. Requirements

1. [Docker](https://docs.docker.com/install/)
2. [mF2C CIMI server](https://github.com/mF2C/cimi)

Dockerfile content:

```
FROM python:3.4-alpine
ADD . /code
WORKDIR /code
RUN pip install -r requirements.txt
EXPOSE 46000
CMD ["python", "app.py"]
```

#### 2. Install & Launch with Docker

1. [Install and launch the CIMI server](https://github.com/mF2C/cimi/tree/master/_demo)

2. Clone / download repository

```bash
git clone https://github.com/mF2C/LifecycleManagement.git
```

3. Go to LifecycleManagement folder

```bash
cd LifecycleManagement
```

4. Build application:

```bash
sudo docker build -t lm-app .
```

5. Run application:

```bash
sudo docker run -p 46000:46000 lm-app
```

-----------------------

### Usage Guide

1. Create one or more users in CIMI

2. Start the Lifecycle Management module with access to the docker socket ('-v /var/run/docker.sock:/var/run/docker.sock')

```bash
sudo docker run --env CIMI_URL=https://cimi_rest_api --env CIMISER="user" --env CIMI_PASSWORD="password"  --env CIMI_COOKIES_PATH="~./cookies" --env HOST_IP="host_ip" -v /var/run/docker.sock:/var/run/docker.sock -p 46000:46000 lm-app
```

3. After launching the Lifecycle Management module, the REST API services can be accessed at port 46000:

     - List of services (json): _https://localhost:46000/api/v1/lifecycle_

     - List of services (swagger ui): _https://localhost:46000/api/v1/lifecycle.html_

-----------------------

### Relation to other mF2C components

The Lifecycle Management module is connected with the following mF2C components:

- Is called by the following modules / components:
    - User Management: it receives warnings from the User Management when the mF2C applications use more resources than allowed by the users

- Makes calls to the following modules / components:
    - User Management:
    - QoS:
    - Landscaper:
    - Recommender:
    - Distributed Execution Runtime:
    - SLA Manager:
    - Service Management:
