# Docker A to Z

**Make Docker Private Registry & Manage docker containers with AWS**

- Ubuntu 18.04

<br/>

### 1. SSH Connection

```bash
$ sudo apt-get update

# install net-tools
$ sudo apt-get install net-tools

# cheak openssh-server
$ dpkg -l | grep openssh

# install openssh-server
$ sudo apt-get install openssh-server

$ ifconfig
```

<br/>

### 2. Docker Registry Server setting (Server)

```bash
$ sudo apt-get install docker.io
$ sudo docker pull registry:latest
$ sudo docker images
REPOSITORY   TAG       IMAGE ID       CREATED        SIZE
registry     latest    X			  15 hours ago   26.2MB

$ sudo docker info
 Insecure Registries:
  127.0.0.0/8
$ sudo service docker stop
$ vi /etc/docker/daemon.json
{
	"insecure-registries":["X.X.X.X:5000"]
}
$ sudo docker info
 Insecure Registries:
  X.X.X.X:5000
  127.0.0.0/8
$ service docker restart
$ service docker state
$ sudo docker run --name local-registry -d -p 5000:5000 registry
$ sudo docker container ls
```

<br/>

### 3. Make Docker Image (Client)

#### Create a base image

```bash
$ sudo docker pull pytorch/pytorch
$ sudo docker images
REPOSITORY        TAG       IMAGE ID       CREATED        SIZE
registry          latest    b2cb11db9d3d   21 hours ago   26.2MB
pytorch/pytorch   latest    5ffed6c83695   5 months ago   7.25GB
$ sudo docker run -d -p 8000:8000 --name dev-env1 pytorch/pytorch
$ sudo docker ps -a
$ sudo docker start dev-env1
```

##### # Issue 01

```bash
CONTAINER ID   IMAGE             COMMAND		CREATED         STATUS
62ab3c761e8c   pytorch/pytorch   "/bin/bash"    7 minutes ago   Exited (0)
```

<br/>

### 4. from Local Registry to AWS

```
```