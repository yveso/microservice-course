# microservices-course

[![Build Status](https://travis-ci.com/yveso/microservice-course.svg?branch=master)](https://travis-ci.com/yveso/microservice-course)

Following the [Microservices with Docker, Flask, and React Course](https://testdriven.io/) course.

## Chapter 1

* Build container: `docker-compose -f docker-compose-dev.yml build`
* Run container: `docker-compose -f docker-compose-dev.yml up -d`
* Update container: `docker-compose -f docker-compose-dev.yml up -d --build`
* View logs: `docker-compose -f docker-compose-dev.yml logs`
* Run Tests: `docker-compose -f docker-compose-dev.yml run users python manage.py test`
* Start Shell: `docker-compose -f docker-compose-dev.yml run users flask shell`
* Recreate DB: `docker-compose -f docker-compose-dev.yml run users python manage.py recreate-db`
* Run Postgres: `docker-compose -f docker-compose-dev.yml exec users-db psql -U postgres`
```
postgres=# \c users_dev
You are now connected to database "users_dev" as user "postgres".
users_dev=# \dt
         List of relations
 Schema | Name  | Type  |  Owner
--------+-------+-------+----------
 public | users | table | postgres
(1 row)

users_dev=# \q
```
* Seed DB: `docker-compose -f docker-compose-dev.yml run users python manage.py seed-db`
* Run Tests with coverage: `docker-compose -f docker-compose-dev.yml run users python manage.py cov`
* Run flake8: `docker-compose -f docker-compose-dev.yml run users flake8 project`

### Deployment

* `docker-machine create --driver digitalocean --digitalocean-access-token=??? microservice-tut`
* `docker-machine env microservice-tut`
    * bash: `eval $(docker-machine env microservice-tut)`
    * cmd: `@FOR /f "tokens=*" %i IN ('docker-machine env microservice-tut') DO @%i`
    * PowerShell: `docker-machine.exe" env microservice-tut | Invoke-Expression`
* `docker-machine ls`
* `docker-compose -f docker-compose-prod.yml up -d --build`
* `docker-compose -f docker-compose-prod.yml run users python manage.py recreate-db`
* `docker-compose -f docker-compose-prod.yml run users python manage.py seed-db`
* `docker-compose -f docker-compose-prod.yml run users python manage.py test`
* `docker-machine ip microservice-tut`
* `docker-compose -f docker-compose-prod.yml run users env`
* `docker-compose -f docker-compose-prod.yml up -d`
* `docker-compose -f docker-compose-prod.yml up -d --build nginx`
* Unset (back to local) `docker-machine env -u`
* `docker-compose -f docker-compose-dev.yml up -d --build nginx`
