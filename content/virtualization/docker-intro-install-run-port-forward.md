Title: Docker Intro install run and port forward
Date: 2014-07-10 17:00

Docker is a union file system based layer system leveraging linux lxc containers for ultra lightweight virtualization/compartmentalization.

[TOC]

- **Images** are the initial templates, each image has a unique ID
- **Containers** are the running virtual machines, each container has a unique ID  <http://docs.docker.com/terms/container>
- *From now on it is assumed you use **sudo** before any docker command!*

- - -
## Install Docker
**[Docker on Ubuntu 14.04][dockerlink]**
[dockerlink]: http://docs.docker.com/installation/ubuntulinux/#ubuntu-trusty-1404-lts-64-bit

1. `sudo apt-key adv --keyserver hkp://keyserver.ubuntu.com:80 --recv-keys 36A1D7869245C8950F966E92D8576A8BA88D21E9`
1. `sudo sh -c "echo deb https://get.docker.io/ubuntu docker main > /etc/apt/sources.list.d/docker.list"`
1. `sudo apt-get update`
1. `sudo apt-get install lxc-docker`

- - -
## Download a docker image
`sudo docker pull ubuntu:trusty` (**grabs the latest, i.e. 14.04.1**) or `sudo docker pull ubuntu:12.04.3`
> critical! use the colon and a specific version! downloading all of the ubuntu images by accident sucks

`sudo docker pull redis:latest`
> choose the latest or a specific version to avoid downloading a lot of old crap


### Remove a docker image

`docker rmi 3db9c44f4520`

`docker rmi -f $(docker images --all --quiet | grep -v 5506de2b643b)`
> remove ALL images except one by taking the output (quiet means only image ids), excluding a specific one, and then force removing the images (by id)

`docker rmi -f $(docker images --all --quiet)`
> remove ALL images

`du -sh /var/lib/docker/aufs`
>    72K    /var/lib/docker/aufs/


Sometimes a docker image is **still connected to a container** (already exited or forgotten)

    docker ps -a
    docker rm name_or_id
    docker rmi image_id


### Docker info

`docker`
> get a helpful list of all the commands

`docker --version`

`docker info`

    :::text
    Containers: 1
    Images: 23
    Storage Driver: aufs
     Root Dir: /var/lib/docker/aufs
     Dirs: 25
    Execution Driver: native-0.2
    Kernel Version: 3.13.0-35-generic
    Operating System: Ubuntu 14.04.1 LTS
    WARNING: No swap limit support

`du -sh /var/lib/docker/aufs`
>    469M    /var/lib/docker/aufs/

`docker ps --all`
> no containers are running yet

`docker ps --help`

- - -
## Controlling Containers: run and stop

`docker run`
> get a helpful list of how to run container

`docker run --rm -i -t ubuntu:14.04 /bin/bash`

    :::text
    creates a container
    --rm: automatically remove the container when it exits
    -i: keep stdin open even if not attached
    -t: allocate a tty, attach stdin and stdout
    use the ubuntu 14.04 minimal image
    Runs an interactive bash shell

> This will continue to exist in a stopped state once exited (see "docker ps -a")

    root@f5878ed6016e:/# cat /etc/issue
    root@f5878ed6016e:/# uname -a
    root@f5878ed6016e:/# df -h

Control-p then Control-q to detach the tty without exiting the shell

`docker ps`

### Stopping a container

Part of the efficiency in docker is that containers can **run in the background automatically**

    docker run --name myredis -d redis
    docker ps
    docker stop myredis

Another efficiency is that a docker container will only **run as long as it takes to execute** a command (and any **changes are not forgotten**)

`docker run ubuntu:trusty uname -a`
> this runs the container only as long as it takes to execute the command

`docker attach f5878ed6016e`

`Control + C`  *(now we have exited the container and it will clean itself up)*

`docker ps -a`

    spun up another container but only long enough to run the command
    CONTAINER ID IMAGE        COMMAND      CREATED      STATUS    PORTS         NAMES
    e4b436320442 ubuntu:14.04 -uname -a  3 minutes ago              elegant_engelbart


`docker rm e4b436320442`
> Alternatively: `docker rm elegant_engelbart`


- - - 
## Saving an instance (docker commit)

`docker commit --help`

### Git on docker ubuntu:14.04

1. `docker run -i -t ubuntu:14.04 /bin/bash`
1. `Control + p then Control + q` *(to detach the tty without exiting the shell)*
1. `docker ps -a` *(make a note of the ID or NAME)*
1. `docker attach ID_OR_NAME`
1. `apt-get update; apt-get install git -y`
1. `cd /root`
1. `git --version`
1. `git clone https://johnpfeiffer@bitbucket.org/johnpfeiffer/myrepo.git`
1. `exit`
1. `exit`
> now the Container will have git installed, a repo cloned, and will be stopped
1. docker commit container_name_here johnpfeiffer_git_repo
> 4a74440186d976caeccc52f5ed2bd44269beb84d472391a7ce26ee3db8ffc1e9
1. docker images

> output
    REPOSITORY               TAG                 IMAGE ID            CREATED             VIRTUAL SIZE
    johnpfeiffer_git_repo    latest              4a74440186d9        54 seconds ago      402 MB
    ubuntu                   14.04               e54ca5efa2e9        3 weeks ago         276.5 MB



- - -
### Add a port to an image

1. `docker run -i -t -p 127.0.0.1:8000:8000 --name john johnpfeiffer_git_repo:latest /bin/bash`
1. `control+p then control+q`
1. `docker attach john`
1. `cd /root/myrepo`
1. `pelican content  (assuming pelicanconf.py is here)`
1. `cd output`
1. `python -m SimpleHTTPServer`
1. `control+p then control+q`
1. `docker ps -a`
1. `http://127.0.0.1:8000`

- - - 
### Python and Pelican static site generator on docker ubuntu:14.04
1. `apt-get update; apt-get install python python-setuptools openssl wget -y`
1. `wget -qO- https://raw.github.com/pypa/pip/master/contrib/get-pip.py | sudo python`
1. `pip install pelican Markdown beautifulsoup4`


- - - 
## Dockerfile to automate building a container

`mkdir -p dockerfiles/trustyssh`

`vi dockerfiles/trustyssh/Dockerfile`

    FROM ubuntu:trusty
    MAINTAINER John Pfeiffer
    
    RUN apt-get update -y
    RUN apt-get upgrade -y
    RUN apt-get install -y openssh-server
    RUN mkdir /var/run/sshd
    EXPOSE 22
    CMD /usr/sbin/sshd -D

`docker build --tag=newimagetag --rm ./dockerfiles/trustyssh`
> Each RUN command creates an intermediate container, so make sure you use the -rm option

- - - 

`docker run -v $HOSTDIR:$DOCKERDIR`




### Halt all docker containers
docker rm -f $(docker ps -a -q)



## Misc

`docker search stackbrew/ubuntu`
> FYI stackbrew/ubuntu is the same as ubuntu , [stackbrew is the curated Docker registry](https://registry.hub.docker.com/u/stackbrew/ubuntu)


`docker start -i -a IDORNAME`

`docker images --tree`


`docker run -d -p 127.0.0.1:5000:5000 training/webapp python app.py`

`docker port IDORNAME`

- - - 
### Advanced Docker pre built images

<https://registry.hub.docker.com>

- <https://registry.hub.docker.com/_/redis/>
- - `docker run --name some-redis -d redis`
- - > the image already includes by default the expose port command: EXPOSE 6379
- - `docker run --name some-app --link some-redis:redis -d application-that-uses-redis`


- - -
### More Info
- <https://docs.docker.com/articles/basics>
- <https://github.com/wsargent/docker-cheat-sheet>
- <https://docs.docker.com/reference/commandline/cli/#run>

- <http://jpetazzo.github.io/2014/06/23/docker-ssh-considered-evil>
