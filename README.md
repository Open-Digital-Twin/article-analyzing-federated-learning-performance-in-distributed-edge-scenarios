# Federated Learning

This repository contains the architectural block implementations along Dockerfiles to be used for distributed federated learning experiments using containers. The `docker-compose` file in the root is an example to deploy the application, containing the expected environment variables, and running on an infrastructure with 3 worker VMs and one manager.

This code has been used for the Analyzing Federated Learning in Distributed Edge Scenarios paper, which will be available here when published.

# Running the Application

## Fully Running in a Dockerized Environment

To run the main application in a fully dockerized environment, run:

```
docker stack deploy --compose-file docker-compose.yaml STACK_NAME
```

Note that, to successfully run this without any tweaks, the environment I used for the experiments has to be replicated. This means that the VMs names declared in the containers have to be the same, and it requires a Docker Swarm with 3 worker VMs and one Manager.

To run in a different environment, the names will have to be tweaked in the `docker-compose` file, and likewise in the observer module which has the node names.

## Running in a Local Environment


Running locally without Docker requires installing the dependencies. For the server and client run:

```
pip3 install numpy torch flwr vision 
```

Running the server and clients is simple. After adding the data to the clients (refer to the client section below), go to the server module and run the following:

```
SERVER_IP=0.0.0.0:8080 FRACTION_FIT=0.1 MIN_FIT_CLIENTS=2 MIN_AVAILABLE_CLIENTS=2 NUM_ROUNDS=10 python3 server.py
```

This should open the server application expecting two clients. Then, navigate to the client and run:

```
SERVER_IP=0.0.0.0:8080 KERNEL_SQUARE_CONVOLUTION=5 FIRST_FULLY_CONNECTED_LAYER=120 SECOND_FULLY_CONNECTED_LAYER=84 EPOCHS=10 python3 client.py
```

This will run the first client. The server will expect another one, so you can either navigate to a different client with different data and run the same command, or simply run the command again in the same client.

After the clients are connected, they will train their models, upload and receive updated parameters. This will repeat for 10 rounds as specified when running the server.

The observer can only observe Docker containers, so it is not possible to be run locally without a Swarm.

# Components

## Server

The server is responsible for starting the gRPC connection with the clients, and averaging the models that are uploaded for a certain number of server rounds (i.e., repetitions). Currently, the server uses a simple average strategy.

The server is powered by the [Flower Framework](https://flower.dev/) and works by implementing the required server interfaces.

## Client

The client is responsible for connecting to the gRPC connection opened by the server, training a local model with a number of epochs, and uploading the model to the server.

In this repository there is one client example, although for the experiments up to ten clients were used. The client and its Dockerfile expect data batches in a `data` folder in its root. As CIFAR has been used for the examples, the data batches are placed in `./data/cifar-10/cifar-10-batches-py/`. The data can be downloaded in the [main cifar-10 dataset page](http://www.cs.toronto.edu/~kriz/cifar.html).

There are other parameters for the client besides the IP and the number of client epochs that relate to the convolution neural network. This **cannot be changed without significant changes in the model, so I don't recommend tweaking them unless you know exactly what you are doing**.

The client is powered by the [Flower Framework](https://flower.dev/) and works by implementing the required client interfaces.

## Observer

The observer collects metrics for the other running containers and persist them to a local folder. In the `docker-compose` file, this folder is also mapped to a Swarm volume to enable persistence to the host VM.

To generate API documentation for the `docker-handler` service, inside the `observability` folder run:

```
npm run gen-doc
```

A `docs` folder will be created containing the service documentation. To access it, simply open the `index.html` file.

The generated log will be persisted after each container finishes its lifecycle, it will be separated in folders according to the given `EXPERIMENT_NAME` and then after its image name. The logs contain an array with `ContainerStats` objects. Each object in this array has been retrieved in a tick, so they represent the resource usage per time retrieved by the [Docker Stats API](https://docs.docker.com/engine/api/v1.21/), as well as the accuracy if it's a server. 

The observer represents a robust and clean way to log container stats, as it retrieves a lot of useful information in a very organized manner by separating the files in a meaningful folder structure. I consider the observer the most vital part of this work and recommend to anyone interested in it to familiarize with the observer module.

## Plotting

This is the module used for plotting the experiment results. There are many utility methods, such as averaging every log in a folder and subfolders, and generating the main final average stats file with stats for network (packets and bytes received and transmitted), CPU usage, memory usage, and accuracy if the container is a server.

Additionally, every ran plot is also described in the main plotter file.

## Utilities

This module has been used to separate the 5 CIFAR-10 data batches into 500 for higher granularity when running experiments.

# Recommended Reading

- [Example: PyTorch - From Centralized To Federated](https://flower.dev/docs/example-pytorch-from-centralized-to-federated.html)
- [Server Aggregation Strategies](https://flower.dev/docs/strategies.html)
- [Docker Stats API](https://docs.docker.com/engine/api/v1.21/)
- [Docker Swarm Overview](https://docs.docker.com/engine/swarm/)
- [Docker Volumes](https://docs.docker.com/storage/volumes/)
- Bilbiographic references cited on the main work
