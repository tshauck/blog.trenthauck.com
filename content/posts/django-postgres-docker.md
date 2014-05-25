title: Django + Postgres + Docker = :)
slug: django-postgres-docker
date: 2014-05-24
Summary: Life is much better with containers.
Category: Development
Tags: Python, Ops

# Background

Early today I fucked-up a server of mine on accident, and I spent hours and
hours setting everything backup.  It sucked.

Most of that is a lie.  I deleted a Docker image on accident, it was hosting a
web reporting tool I had build for a client, which still kinda sucks, but isn't
nearly as bad as it could of been, because I had the site back up in about 10
minutes.  Here's why:

# Docker Containers

The idea of Docker is mostly compared to containers in a shipyard.  I like to
envision myself walking down a grocery store isle, and checking things of a
list:

1. Database - needs to be relational... [postgres][postgres], duh.
2. Web App - django since I like python.  I just built my own here.

## Postgres Container

There are a few things to consider here:

* Have postgres's data directory persist ouside the container.  This way, if
  you're dumb like me and the container shuts down, the data isn't lost.
* [Linking][linking] containers is easy when running the parent container (here
  the Web App).  The parent gets access to the child's env variables.  For
  example, in my `settings.py` file to setup the connection to postgres I simply
  `os.environ("DB_PORT_5432_TCP_PORT")` and I have the port.

There are more things to consider, but since a database for a simple web app is
really a commodity, I just need to worry about getting a few things right.

## The Web App

Since I wrote this part.  It's really as simple creating a DockerFile in the
repository then scripting out everything.  Django is covered plenty of other
places, but my DockeFile looks something like:

```
M ubuntu:14.04

MAINTAINER trent@trenthauck.com

RUN apt-get -y update && \
    apt-get -y install python-pip && \
    apt-get -y install python-dev && \
    apt-get -y install libpq-dev

RUN pip install pandas django psycopg2 django_pandas
```

Plus some other things which I'd rather not share.  And we're back, easy peasy.


[postgres]: https://github.com/Painted-Fox/docker-postgresql
[linking]: http://docs.docker.io/use/working_with_links_names/
