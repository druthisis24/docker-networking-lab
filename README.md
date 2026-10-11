# Docker Networking with Multiple Containers

## Objective

To understand Docker bridge networking and configure communication between a Flask web application, a MySQL database, and a Redis cache.

## Project Overview

This project demonstrates how multiple Docker containers communicate over a custom bridge network.

### Technologies Used

- Python
- Flask
- Docker
- MySQL
- Redis
- Git and GitHub

## Architecture

The application consists of three containers connected through a custom Docker bridge network named `my-bridge-net`.

- **Flask:** Hosts a REST API on port 5001.
- **MySQL:** Provides a database service on port 3306.
- **Redis:** Provides a cache service on port 6379.

Docker's internal DNS allows containers on the same user-defined bridge network to resolve one another by container name.

## Project Structure

```text
docker-networking-lab/
├── app.py
├── requirements.txt
├── Dockerfile
├── .gitignore
├── README.md
└── screenshots/
```

## Prerequisites

- Docker Desktop
- Visual Studio Code
- Git
- A GitHub account

## Implementation Steps

### 1. Build the Flask Image

```bash
docker build -t flask-api .
```

### 2. Create the Bridge Network

```bash
docker network create --driver bridge my-bridge-net
docker network ls
docker network inspect my-bridge-net
```

### 3. Start MySQL

```bash
docker run -d --name mysql \
  --network my-bridge-net \
  -e MYSQL_ROOT_PASSWORD=LabRoot123! \
  mysql:8.0
```

### 4. Start Redis

```bash
docker run -d --name redis \
  --network my-bridge-net \
  redis:7
```

### 5. Start Flask

```bash
docker run -d --name flask \
  --network my-bridge-net \
  -p 5001:5001 \
  flask-api
```

### 6. Verify Running Containers

```bash
docker ps
```

### 7. Test the REST API

Open the following URLs in a web browser:

- http://localhost:5001/
- http://localhost:5001/about

### 8. Test Container Connectivity

Test connectivity from the Flask container to MySQL:

```bash
docker exec flask python -c "import socket; s=socket.create_connection(('mysql',3306),timeout=5); print('MySQL is reachable'); s.close()"
```

Test connectivity from Flask to Redis:

```bash
docker exec flask python -c "import socket; s=socket.create_connection(('redis',6379),timeout=5); print('Redis is reachable'); s.close()"
```

Inspect the network:

```bash
docker network inspect my-bridge-net
```

## Important Docker Networking Concepts

### 1. What is the `--network` flag?

It specifies the Docker network to which a container should be connected. The `--net` flag is a shorthand.

### 2. How do containers communicate?

Containers connected to the same user-defined bridge network can communicate using container names or IP addresses. Container names are generally preferable because IP addresses can change.

### 3. Bridge Network vs Host Network

- **Bridge network:** Provides an isolated network for containers and supports communication between containers on the same network.
- **Host network:** Uses the host's network stack directly. Port publishing with `-p` is generally unnecessary in this mode, and isolation differs from bridge networking.

### 4. How do you expose a container port?

Use the `-p HOST_PORT:CONTAINER_PORT` option.

Example:

```bash
docker run -d --name flask \
  --network my-bridge-net \
  -p 5001:5001 \
  flask-api
```

This maps host port 5001 to container port 5001.

## Screenshots and Results

Screenshots captured during execution are stored in the `screenshots/` folder.

### 1. Docker Image Build

![Docker image build](screenshots/01-docker-build.png)

### 2. Bridge Network Creation

![Bridge network](screenshots/02-bridge-network.png)

### 3. Running Containers

![Running containers](screenshots/03-running-containers.png)

### 4. Flask REST API Response

![Flask API response](screenshots/04-flask-api.png)

### 5. Container Connectivity

![Container connectivity](screenshots/05-container-connectivity.png)

### 6. Network Inspection

![Network inspection](screenshots/06-network-inspect.png)

## Cleanup

Stop and remove the containers:

```bash
docker stop mysql redis flask
docker rm mysql redis flask
```

Remove the custom bridge network:

```bash
docker network rm my-bridge-net
```

## Conclusion

This lab demonstrates how to create a custom Docker bridge network, deploy a Flask API alongside MySQL and Redis containers, expose the Flask application to the host, and verify container-to-container connectivity using Docker's internal DNS.

The exercise provides a foundation for deploying multi-container applications with isolated networking and service discovery.
