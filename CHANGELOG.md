# Changelog (Lifecycle Manager)
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.3.9] - 2019-10-08
### Changed
- Service deployment - Agent selection: workflow updated; the LM calls the UM before calling the QoS Provider
- Service instance is updated before calling QoS Provider

### Fixed
- create agreement path was fixed

## [1.3.7] - 2019-09-17
### Added
- new service added to check health of components: UM and LM

## [1.3.6] - 2019-08-08
### Added
- GUI to manage the Lifecycle and User Management modules

### Changed
- logs and exceptions updated
- errors handling improved
- paths names changed:
  - Before: PUT /api/v2/lm/service-instances/{service_instance_id}/compss
  - Now: PUT /api/v2/lm/service-instances/{service_instance_id}/der

### Fixed
- error when assigning ports with COMPSs applications

## [1.2.7] - 2019-06-17
### Changed
- docker-compose base image updated
- docker-compose example updated
- use of service's category field when calling analytics engine


## [1.2.6] - 2019-06-04
### Added
- new database for standalone mode

### Changed
- logs and exceptions updated
- Analytics Engine and Service Manager connection
- documentation and examples updated

### Fixed
- service instance errors

## [1.2.4] - 2019-05-15
### Added
- Changelog file added to project :)

### Changed
- logs improved
- packages structure updated
- Creation of COMPSs containers updated
- Get host IP address from `agent` resource before trying with environment variables
- Parameter 'service_instance' is passed to remote Lifecycle Managers during deployment phase (internal calls)

### Removed
- certs files and references

### Fixed
- ...
