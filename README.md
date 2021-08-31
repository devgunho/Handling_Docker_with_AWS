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

#### Create a base image - pytorch/pytorch

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

<br/>

##### # Issue 01 - Closed

```bash
IMAGE             COMMAND		CREATED			STATUS
pytorch/pytorch   "/bin/bash"	7 minutes ago	Exited (0)
```

```bash
$ sudo docker run -d -it --name dev-env2 pytorch/pytorch
```

```bash
IMAGE             STATUS					NAMES
pytorch/pytorch   Up 8 seconds				dev-env2
pytorch/pytorch   Exited (0) 13 minutes ago	dev-env1
registry          Up 5 hours				local-registry
```

```bash
$ sudo docker exec -it dev-env2 bash
:/# apt-get update
```

<br/>

`docker diff`

```bash
$ sudo docker diff dev-env2
C /var
C /var/lib
C /var/lib/apt
C /var/lib/apt/lists
A /var/lib/apt/lists/archive.ubuntu.com_ubuntu_dists_bionic_multiverse_binary-amd64_Packages.lz4
A /var/lib/apt/lists/security.ubuntu.com_ubuntu_dists_bionic-security_InRelease
A /var/lib/apt/lists/security.ubuntu.com_ubuntu_dists_bionic-security_universe_binary-amd64_Packages.lz4
A /var/lib/apt/lists/archive.ubuntu.com_ubuntu_dists_bionic-backports_main_binary-amd64_Packages.lz4
A /var/lib/apt/lists/archive.ubuntu.com_ubuntu_dists_bionic-updates_universe_binary-amd64_Packages.lz4
A /var/lib/apt/lists/archive.ubuntu.com_ubuntu_dists_bionic_restricted_binary-amd64_Packages.lz4
A /var/lib/apt/lists/lock
A /var/lib/apt/lists/partial
A /var/lib/apt/lists/security.ubuntu.com_ubuntu_dists_bionic-security_restricted_binary-amd64_Packages.lz4
A /var/lib/apt/lists/archive.ubuntu.com_ubuntu_dists_bionic-backports_InRelease
A /var/lib/apt/lists/archive.ubuntu.com_ubuntu_dists_bionic-updates_restricted_binary-amd64_Packages.lz4
A /var/lib/apt/lists/archive.ubuntu.com_ubuntu_dists_bionic_InRelease
A /var/lib/apt/lists/archive.ubuntu.com_ubuntu_dists_bionic_main_binary-amd64_Packages.lz4
A /var/lib/apt/lists/auxfiles
A /var/lib/apt/lists/security.ubuntu.com_ubuntu_dists_bionic-security_main_binary-amd64_Packages.lz4
A /var/lib/apt/lists/archive.ubuntu.com_ubuntu_dists_bionic-backports_universe_binary-amd64_Packages.lz4
A /var/lib/apt/lists/archive.ubuntu.com_ubuntu_dists_bionic-updates_main_binary-amd64_Packages.lz4
A /var/lib/apt/lists/archive.ubuntu.com_ubuntu_dists_bionic-updates_multiverse_binary-amd64_Packages.lz4
A /var/lib/apt/lists/archive.ubuntu.com_ubuntu_dists_bionic_universe_binary-amd64_Packages.lz4
A /var/lib/apt/lists/security.ubuntu.com_ubuntu_dists_bionic-security_multiverse_binary-amd64_Packages.lz4
A /var/lib/apt/lists/archive.ubuntu.com_ubuntu_dists_bionic-updates_InRelease
C /root
A /root/.bash_history
```

<br/>

#### Create a base image - ubuntu:18.04

```bash
$ sudo docker pull ubuntu:18.04
$ sudo docker run -d -it --name dev-env3 ubuntu
$ sudo docker exec -it dev-env3 bash
:/# apt-get update
```

<br/>

### 4. from Local Registry Server to AWS

<br/>