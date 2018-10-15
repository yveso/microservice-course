# microservices-course

Following the [Microservices with Docker, Flask, and React Course](https://testdriven.io/).

## Chapter 1

* Build container: `docker-compose -f docker-compose-dev.yml build`
* Run container: `docker-compose -f docker-compose-dev.yml up -d`
* Update container: `docker-compose -f docker-compose-dev.yml up -d --build`
* View logs: `docker-compose -f docker-compose-dev.yml logs`
* Run Tests: `docker-compose -f docker-compose-dev.yml run users python manage.py test`
