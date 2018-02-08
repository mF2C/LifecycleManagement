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

![Platform Manager](resources/pm.png)

-----------------------

### Installation Guide

#### 1. Requirements

1. [Docker](https://docs.docker.com/install/)
2. [Docker-Compose](https://docs.docker.com/compose/install/) (for integration with other components)

Dockerfile content:

```
FROM python:3.4-alpine
ADD . /code
WORKDIR /code
RUN pip install -r requirements.txt
EXPOSE 46000
CMD ["python", "app.py"]
```

#### 2. Install

###### 2.1 Launch with Docker

How to install the Lifecycle Management module:

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
sudo docker build -t lm-app .
```

4. Run application:

```bash
sudo docker run -p 46000:46000 lm-app
```

5. REST API can be accessed at port 46000:

     - List of services (json): _https://localhost:46000/api/v1/lifecycle_

     - List of services (swagger ui): _https://localhost:46000/api/v1/lifecycle.html_


###### 2.2. Launch with Docker-Compose

How to install the Lifecycle Management module and other components:

_-not ready-_

-----------------------

### Usage Guide

After installing the Lifecycle Management module, the REST API services can be accessed at port 46000:

     - List of services (json): _https://localhost:46300/api/v1/lifecycle_

     - List of services (swagger ui): _https://localhost:46300/api/v1/lifecycle.html_

#### Test component

_-not ready-_

-----------------------

### Relation to other mF2C components

The Lifecycle Management module is connected with the following mF2C components:

- Is called by the following modules / components:
    - User Management: it receives warnings from the User Management when the mF2C applications use more resources than allowed by the users
    - ...
- Makes calls to the following modules / components:
    - User Management:
    - QoS:
    - Landscaper:
    - Recommender:
    - Distributed Execution Runtime:
    - SLA Manager:
    - Service Management:
    - ...
