# microservices-course

Following the [Microservices with Docker, Flask, and React Course](https://testdriven.io/).

## Chapter 1

* Build container: `docker-compose -f docker-compose-dev.yml build`
* Run container: `docker-compose -f docker-compose-dev.yml up -d`
* Update container: `docker-compose -f docker-compose-dev.yml up -d --build`
* View logs: `docker-compose -f docker-compose-dev.yml logs`
* Run Tests: `docker-compose -f docker-compose-dev.yml run users python manage.py test`
* Start Shell: `docker-compose -f docker-compose-dev.yml run users flask shell`
* Recreate DB: `docker-compose -f docker-compose-dev.yml run users python manage.py recreate-db`
* Run Postgres `docker-compose -f docker-compose-dev.yml exec users-db psql -U postgres`
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
