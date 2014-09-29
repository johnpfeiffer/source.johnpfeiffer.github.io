Title: Docker Intro install run and port forward
Date: 2014-07-10 17:00

Docker is a union file system based layer system leveraging linux lxc containers for ultra lightweight virtualization/compartmentalization

[TOC]

- Images are the initial templates, each image has a unique ID
- Containers are the running virtual machines, each container has a unique ID

### Install Docker
**[Docker on Ubuntu 14.04][dockerlink]**
[dockerlink]: http://docs.docker.com/installation/ubuntulinux/#ubuntu-trusty-1404-lts-64-bit

1. `sudo apt-key adv --keyserver hkp://keyserver.ubuntu.com:80 --recv-keys 36A1D7869245C8950F966E92D8576A8BA88D21E9`
1. `sudo sh -c "echo deb https://get.docker.io/ubuntu docker main > /etc/apt/sources.list.d/docker.list"`
1. `sudo apt-get update`
1. `sudo apt-get install lxc-docker`

- - -
### Start a docker image
`sudo docker pull ubuntu:14.04`


**From now on it is assumed you use sudo before any docker command!**

`docker run --help`

`docker run --rm -i -t ubuntu:14.04 /bin/bash`

    create a container
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

`docker run ubuntu:14.04 uname -a`

`docker attach f5878ed6016e`

`Control + C`  *(now we have exited the container and it will clean itself up)*

`docker ps -a`

    spun up another container but only long enough to run the command
    CONTAINER ID IMAGE        COMMAND      CREATED      STATUS    PORTS         NAMES
    e4b436320442 ubuntu:14.04 -uname -a  3 minutes ago              elegant_engelbart

`docker rm e4b436320442`
> Alternatively: `docker rm elegant_engelbart`


- - - 
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
- - - 
### DockerFile to automate building a container

vi mydockerfile

    FROM ubuntu:14.04
    MAINTAINER John Pfeiffer

    RUN apt-get update -y
    RUN apt-get upgrade -y
    RUN apt-get install -y openssh-server
    RUN mkdir /var/run/sshd
    CMD /usr/sbin/sshd -D
    
    > Each RUN command creates an intermediate container, so make sure you use the -rm option

docker build -t=newimagetag -rm=true .


- - - 

docker run -v $HOSTDIR:$DOCKERDIR

### Useful Commands
`sudo docker info`

`docker images`

`docker images --help`

`docker ps -a`

### Download all ubuntu docker images
`sudo docker pull ubuntu`
> Pulling repository ubuntu
> 58faa899733f: Download complete 
> 195eb90b5349: Download complete 
*hundreds of megabytes downloaded*

`docker images`

### Remove an image
`docker rmi 3db9c44f4520`

`docker search stackbrew/ubuntu`
> FYI stackbrew/ubuntu is the same as ubuntu , 
> [stackbrew is the curated Docker registry](https://registry.hub.docker.com/u/stackbrew/ubuntu)


`docker start -i -a IDORNAME`

`docker images --tree`

`docker commit --help`


`docker run -d -p 127.0.0.1:5000:5000 training/webapp python app.py`

`docker port IDORNAME`

- - - 
### Advanced Docker pre built images

<https://registry.hub.docker.com>

`docker run --name some-redis -d redis`
`docker run --name some-app --link some-redis:redis -d application-that-uses-redis`


- - -
### More Info
<https://github.com/wsargent/docker-cheat-sheet>
<https://docs.docker.com/reference/commandline/cli/#run>

