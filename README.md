# Federated Learning

This repository contains the architectural block implementations along Dockerfiles to be used for distributed federated learning experiments using containers. The `docker-compose` file in the root is an example to deploy the application, containing the expected environment variables, and running on an infrastructure with 3 worker VMs and one manager.

This code has been used for the Analyzing Federated Learning in Distributed Edge Scenarios paper, which will be available here when published.

# Components

## Server

The server is responsible for starting the gRPC connection with the clients, and averaging the models that are uploaded.

## Client

The client is responsible for connecting to the gRPC connection opened by the server, training a local model, and uploading the model to the server.


## Observer

The observer collects metrics for the other running clients and persist them to a volume mapped to the host.

To generate API documentation for the `docker-handler` service, inside the `observability` folder run:

```
npm run gen-doc
```

A `docs` folder will be created containing the service documentation. To access it, simply open the `index.html` file.
