Title: Docker Intro install run and port forward
Date: 2014-07-10 17:00

Docker is a union file system based layer system leveraging linux lxc containers for ultra lightweight virtualization/compartmentalization.

Much like AWS cloud servers (api based dynamic deployment that should be tolerant of node failure) and automated deployment/configuration infrastructure (chef or puppet such that cloud servers are created idempotent, remotely and automatically managed at scale), Docker requires a change of mindset.

Docker encourages design of modular, deterministic and defined, single purpose components that are easy to compose into larger services.


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

`docker rmi trustyssh`

`docker rmi -f $(docker images --all --quiet | grep -v 5506de2b643b)`
> remove ALL images except one by taking the output (quiet means only image ids), excluding a specific one, and then force removing the images (by id)

docker images --quiet --filter "dangling=true" | xargs docker rmi
> remove all images that do not have a tag and are not a parent of a tagged image

`docker rmi -f $(docker images --all --quiet)`
> remove ALL images


`du -sh /var/lib/docker/aufs`
>  72K    /var/lib/docker/aufs/


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

`docker images --tree`
> view the hashes and sizes of all of the parent images

- - -
## Controlling Containers

### Starting a container (from an image)

#### Create a container

First you must create a container from an image:

`docker run`
> get a helpful list of how to run a container

`docker run --rm -i -t ubuntu:14.04 /bin/bash`

    :::text
    creates a container
    --rm: automatically remove the container when it exits
    -i: keep stdin open even if not attached
    -t: allocate a tty, attach stdin and stdout
    use the ubuntu 14.04 minimal image
    Docker automatically gives the container a random name
    Runs an interactive bash shell

> This will continue to exist in a stopped state once exited (see "docker ps -a")

    root@f5878ed6016e:/# cat /etc/issue
    root@f5878ed6016e:/# uname -a
    root@f5878ed6016e:/# df -h

Control-p then Control-q to detach the tty without exiting the shell

`docker ps`

`docker run -d -p 127.0.0.1:5000:5000 training/webapp python app.py`
> detached with port 5000 available and executing

#### Start a container

After a container has already been created (which starts it so ironically this is actually a "restart")

`docker start --interactive --attach container_id_or_name`

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


### Deleting aka removing a container

`docker rm e4b436320442`
> Alternatively: `docker rm --force elegant_engelbart`

`docker rm -f $(docker ps -a -q)`
> Deletes forcibly all containers (be careful!)


- - -
## Dockerfile to automate building an image

Dockerfiles allow automating the creation docker images.

Containers as fast, reliable, and deterministic prod/qa/dev environments can also be extended to be just an improved experimentation sandbox (for those used to SSH and using Linux as a common base OS).


`mkdir -p dockerfiles/trustyssh`

`vi dockerfiles/trustyssh/Dockerfile`

    FROM ubuntu:trusty
    MAINTAINER John Pfeiffer "https://bitbucket.org/johnpfeiffer"
    
    RUN apt-get update -y
    RUN apt-get install -y openssh-server byobu
    RUN mkdir /var/run/sshd
    RUN echo 'root:root' | chpasswd
    RUN echo 'ubuntu:ubuntu' | chpasswd
    RUN sed -ri 's/^PermitRootLogin\s+.*/PermitRootLogin yes/' /etc/ssh/sshd_config
    RUN sed -ri 's/UsePAM yes/#UsePAM yes/g' /etc/ssh/sshd_config
    EXPOSE 22
    CMD    ["/usr/sbin/sshd", "-D"]
    
`docker build --tag=newimagename --rm ./dockerfiles/ubuntu-trusty-ssh`
> Each RUN command creates an intermediate container, so make sure you use the -rm option

    :::text
    Sending build context to Docker daemon  2.56 kB
    Sending build context to Docker daemon
    Step 0 : FROM ubuntu:trusty
     ---> 5506de2b643b
    ...
    Removing intermediate container 135b686d82a6
    Step 2 : RUN apt-get update -y
     ---> Running in 7fe06a9ef41b
    Ign http://archive.ubuntu.com trusty InRelease
    ...


- - -
## Add a port to a container

`docker run --detach --publish 127.0.0.1:2222:22 --name johnssh trustyssh`
> run a detached container based on the trustyssh image that binds the private container port 22 to the host port 2222 (in this case the trustyssh image from above is running sshd on port 22)

`docker port johnssh 22`
> 127.0.0.1:2222

`netstat -antp | grep 2222`
> tcp        0      0 127.0.0.1:2222          0.0.0.0:*               LISTEN      24393/docker-proxy

`ssh -o StrictHostKeychecking=no -p 2222 root@127.0.0.1`
> root@19ad0614b237:~#

- - -
## Host data with a Docker Container
Volumes are where Docker Containers can access storage (either from the Host or other Containers)

<https://docs.docker.com/userguide/dockervolumes>

`docker run --interactive --tty --name mydata --volume /tmp/mydata:/opt/mydata trustyssh /bin/bash`
> create an interactive container named "mydata" that maps /tmp/mydata from the host onto /opt/mydata (warning: overriding any existing!)

- - - 
## Saving a docker container as a new image

`docker commit --help`

### docker commit for a container: ubuntu:trusty with git

1. `docker run -i -t ubuntu:trusty /bin/bash`
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

    :::text
    REPOSITORY               TAG                 IMAGE ID            CREATED             VIRTUAL SIZE
    johnpfeiffer_git_repo    latest              4a74440186d9        54 seconds ago      402 MB
    ubuntu                   14.04               e54ca5efa2e9        3 weeks ago         276.5 MB


- - -
## Misc

### Python and Pelican static site generator on docker ubuntu:14.04
1. `apt-get update; apt-get install python python-setuptools openssl wget -y`
1. `wget -qO- https://raw.github.com/pypa/pip/master/contrib/get-pip.py | sudo python`
1. `pip install pelican Markdown beautifulsoup4`
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
## Advanced Docker pre built images

`docker search stackbrew/ubuntu`
> FYI stackbrew/ubuntu is the same as ubuntu , [stackbrew is the curated Docker registry](https://registry.hub.docker.com/u/stackbrew/ubuntu)

<https://registry.hub.docker.com>

- <https://registry.hub.docker.com/_/redis/>
- - `docker run --name some-redis -d redis`
- - > the image already includes by default the expose port command: EXPOSE 6379
- - `docker run --name some-app --link some-redis:redis -d application-that-uses-redis`


- - -
## More Info
- <https://docs.docker.com/articles/basics>
- <https://github.com/wsargent/docker-cheat-sheet>
- <https://docs.docker.com/reference/commandline/cli/#run>

- <http://blog.oddbit.com/2014/08/11/four-ways-to-connect-a-docker>
- <http://jpetazzo.github.io/2014/06/23/docker-ssh-considered-evil>
