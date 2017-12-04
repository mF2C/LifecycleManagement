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

...

-----------------------

### Installation Guide

##### 1. Requirements

1. Docker
2. Docker-Compose
3. Python 2.7.9 - 2.7.14

#### Launch with Docker

- Build application:

```bash
sudo docker build -t lm-app .
```

- Run application:

```bash
sudo docker run -p 5002:5000 lm-app
```

#### Launch with Docker-Compose

...

-----------------------

### Usage Guide

...

-----------------------

### Relation to other mF2C components

...
