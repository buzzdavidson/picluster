[![pipeline status](https://gitlab.com/nicosingh/rabbitmq-cluster-swarm/badges/master/pipeline.svg)](https://gitlab.com/nicosingh/rabbitmq-cluster-swarm/commits/master) [![Docker Pulls](https://img.shields.io/docker/pulls/nicosingh/rabbitmq-cluster-swarm.svg)](https://hub.docker.com/r/nicosingh/rabbitmq-cluster-swarm/)

# What is included?

* RabbitMQ master and slaves, with one vhost (`/`)
* RabbitMQ metrics exporter
* Prometheus server
* Grafana

# How to run this image?

Since this image is prepared to run in Docker Swarm, the first step is to initialize the swarm:

`$ docker swarm init`

Then, add all the slaves into this Swarm using `$ docker swarm join` command. The image is prepared to include all Swarm workers as Rabbit slaves, and all Swarm managers as Rabbit masters. It also supports zero slaves (just one Rabbit master node).

Once the swarm is ready, we should create the **docker-cloud.yml** with RabbitMQ services definition. You can take an example from this [image's repo](https://gitlab.com/nicosingh/rabbitmq-cluster-swarm/blob/master/docker-cloud.yml).

Finally, we start the docker swarm rabbit cluster:

`$ docker stack deploy -c docker-cloud.yml rabbitcluster`

Where `rabbitcluster` is the name of the swarm service.