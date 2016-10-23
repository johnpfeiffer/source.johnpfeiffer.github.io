Title: Docker Intro install run and port forward
Date: 2014-07-10 17:00
Tags: docker, containers

Docker is a union file system based layer system (previously leveraging linux lxc containers) for ultra lightweight virtualization/compartmentalization.

Much like AWS cloud servers (api based dynamic deployment that should be tolerant of node failure) and automated deployment/configuration infrastructure (chef or puppet such that cloud servers are created idempotent, remotely and automatically managed at scale), Docker requires a change of mindset.

Docker encourages design of modular, deterministic and defined, single purpose components that are easy to compose into larger services.

As any tool, using it for managing complexity and packaging can be very helpful but it does expose other potential issues (composability, orchestration, security).

[TOC]

- **Images** are the initial templates, each image has a unique ID <https://docs.docker.com/engine/userguide/storagedriver/imagesandcontainers/#content-addressable-storage>
- **Containers** are the running virtual machines, each container has a unique ID  <https://en.wikipedia.org/wiki/Operating-system-level_virtualization>
- *From now on it is assumed you use **sudo** before any docker command!*

- - -
## Install Docker

<https://docs.docker.com/engine/installation/linux/ubuntulinux/>

1. `apt-key adv --keyserver hkp://pgp.mit.edu:80 --recv-keys 58118E89F3A912897C070ADBF76221572C52609D`
1. `sudo sh -c "echo 'deb https://apt.dockerproject.org/repo ubuntu-trusty main' > /etc/apt/sources.list.d/docker.list"`
1. `sudo apt-get update`
1. `apt-get install linux-image-extra-$(uname -r)`
1. `apt-get install docker-engine`
1. `service docker status`
1. `docker info`

> Make sure it lists /var/lib/docker/aufs

> OPTIONAL STEP IF YOU HAD AN OLD DOCKER INSTALLATION
`apt-get purge lxc-docker*`

### Installing on Mac or Windows
<https://www.docker.com/docker-toolbox>

### Custom docker0 ip range
> Fixing the Docker Bridge docker0 taking a huge 172.17.0.1/16 address space...

Private IP address space is not normally a thing to worry about, unless someone does something silly and grabs 65,534 addresses (stare) (docker)

Because the default docker0 bridge seems to cater to organizations that want to run thousands of containers simultaneously local developers need to do the following fix:

1. `apt-get install bridge-utils`
1. `service docker stop`
1. `ip link set docker0 down`
1. `brctl delbr docker0`
1. `docker daemon --bip=192.168.239.1/24`
1. `ifconfig`

> Docker will be running interactively so you can see all the fun log messages

> You should see docker0 "inet addr:192.168.239.1  Bcast:0.0.0.0  Mask:255.255.255.0"

*Assuming you do not have some other purpose for the 192.168.239 range in which case you can change it to something else*

To permanently have this custom ip range configuration for docker (assuming you have done the steps above):

1. Control + C to quit the previously interactive docker daemon
1. `vi /etc/default/docker`
1. `DOCKER_OPTS="--bip=192.168.239.1/24"`
1. `service docker start`
1. `ifconfig`

> You should see docker0 "inet addr:192.168.239.1  Bcast:0.0.0.0  Mask:255.255.255.0"

More docs to further troubleshoot the docker0 bridge...

- <https://docs.docker.com/engine/userguide/networking/default_network/custom-docker0/>
- <https://docs.docker.com/engine/admin/systemd/>


- - -
## Quick Start Summary

    docker run --rm busybox /bin/sh -c "echo 'hi'"
    hi

    docker run -it --rm -e MYVAR=123 busybox env
> "run" will pull the image from Docker Hub by default, e injects an environment variable, overrides the Docker Image CMD with "env"

    docker run -it --rm --entrypoint=/bin/sh python:latest

- run the docker container (from the latest public python image) and start the shell prompt instead of the python interpreter
- the entrypoint parameter overrides the Docker Image (in case they do not provide a helpfully overridable CMD)
- <https://docs.docker.com/engine/reference/builder/#entrypoint>

- - -
## Download a docker image

Official Images are he easiest to experiment with: <https://hub.docker.com/explore/>

    sudo docker pull ubuntu:trusty
> (**grabs the latest, i.e. 14.04.1**) or use a different tag to download a more specific version `sudo docker pull ubuntu:12.04.3`

**CRITICAL WARNING!** use the colon and a specific version! downloading all of the ubuntu images by accident sucks =(

    sudo docker pull redis:latest
> choose the latest for just messing around but...
> ALWAYS use a specific version to avoid having your dependencies change unexpectedly

Finding what versions of images (tags) you can pull requires using either the UI or the API:

- <https://hub.docker.com/r/library/redis/tags/>
- `docker pull redis:3`
- `docker pull redis:2.8`
- `docker pull redis:2.6`

> Many of the tags are synonyms/symlinks, so latest is the same as 3 is the same as 3.0

### Remove a docker image

    docker rmi redis

    docker rmi -f $(docker images --all --quiet | grep -v 5506de2b643b)
> remove ALL images except one by taking the output (quiet means only image ids), excluding a specific one, and then force removing the images (by id)

    docker images --quiet --filter "dangling=true" | xargs docker rmi
> remove all images that do not have a tag and are not a parent of a tagged image

    docker rmi -f $(docker images --all --quiet)
> remove ALL images


    du -sh /var/lib/docker/aufs
>  Summarize the amount of disk space taken by images and layers, e.g.: 72K    /var/lib/docker/aufs/


Sometimes a docker image is **still connected to a container** (already exited or forgotten)

    docker ps -a
    docker rm name_or_id
    
    docker rm a1b2
    docker rmi image_id
>  **it will "smart match" the first characters of the container ID** the same as git short sha


### Docker info

    docker
> get a helpful list of all the commands

    docker --version

    docker info

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

    du -sh /var/lib/docker/aufs
>    469M    /var/lib/docker/aufs/

    docker ps --all
> no containers are running yet

    docker ps --help


**docker images --tree** is a deprecated command to view the hashes and sizes of all of the parent images

- - -
## Controlling Containers

### Starting a container from an image

#### Create a container

First you must create a container from an image:

    docker run
> get a helpful list of how to run a container

    docker run --rm -i -t ubuntu:14.04 /bin/bash

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

    docker ps

    docker run --detach --name myapp -p 127.0.0.1:5000:5000 training/webapp python app.py
> detached with port 5000 available only to the host and executing the command python with parameter app.py

    docker exec myapp ls -ahl
> runs the ls command inside the container named "myapp"

- `docker run --rm -i -t --link myhipchat_mariadb_1 mariadb:5 /bin/bash -c "exec mysql --version"`
- `docker run --rm -i -t --link myhipchat_mariadb_1:mysql mariadb:5 /bin/bash -c 'exec mysql -h"$MYSQL_PORT_3306_TCP_ADDR" -P"$MYSQL_PORT_3306_TCP_PORT" -uroot -p'`
> an Image can contain both the server and client code so run a "client container" to connect to a running server Container 

#### Start (resume) a container

After a container has already been created (which starts it so ironically this is actually a "restart")

    docker start --interactive --attach container_id_or_name

#### Attaching to a running container

    docker ps -a 
    CONTAINER ID ... STATUS        NAMES
    9e0ebf4421dd ... Up 6 seconds  myexample
    
    docker attach 9e0ebf4421dd
    docker attach myexample

> since the above will expect the container to have /bin/bash it will reuse the instance of shell

    sudo docker exec -i -t 9e0ebf4421dd /bin/bash
    # ps aux
    # exit

> instead a new /bin/bash is executed inside creating a second shell - use the exit command to not leave it around

### Stopping a container

Part of the efficiency in docker is that containers can **run in the background automatically**

    docker run --detach --name myredis redis
    docker ps
    docker stop myredis

Another efficiency is that a docker container will only **run as long as it takes to execute** a command (and any **changes are not forgotten**)

    docker run ubuntu:trusty uname -a
> this runs the container only as long as it takes to execute the command

    docker attach f5878ed6016e

`Control + C`  *(now we have exited the container and it will clean itself up)*

    docker ps -a

> spun up another container but only long enough to run the command

    CONTAINER ID IMAGE        COMMAND      CREATED      STATUS    PORTS         NAMES
    e4b436320442 ubuntu:14.04 -uname -a  3 minutes ago              elegant_engelbart

### Copying a file out of a container

    docker cp <containerId>:/file/path/within/container /host/path/target

<https://docs.docker.com/engine/reference/commandline/cp/>

### Deleting aka removing a container

    docker rm e4b436320442
> Alternatively: `docker rm --force elegant_engelbart`

    docker rm -f $(docker ps -a -q)
> Deletes forcibly all containers (be careful!)


- - -
## Dockerfile to automate building an image

Dockerfiles allow automating the creation docker images.

One advantage to Dockerfile is that each command creates a separate layer so if a specific layer fails all of the previous intermediate images can be re-used.

Also the version style of imagename:tag allows for chaining of upgrades of child images

Containers as fast, reliable, and deterministic prod/qa/dev environments can also be extended to be just an improved experimentation sandbox (for those used to SSH and using Linux as a common base OS).


    mkdir -p dockerfiles/trustyssh
    vi dockerfiles/trustyssh/Dockerfile
> one Dockerfile per directory

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
    

    docker build --tag=newimagename --rm ./dockerfiles/ubuntu-trusty-ssh
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


Since each run command creates a new layer it is best practice to consolidate commands for a single logical action when possible:

    RUN echo "#!/bin/bash" > /root/build-and-run.sh && \
      echo "cd /opt/mydata/pelican-project" >> /root/build-and-run.sh && \
      echo "pelican content -r &" >> /root/build-and-run.sh && \
      echo "cd /opt/mydata/pelican-project/output" >> /root/build-and-run.sh && \
      echo "python -m SimpleHTTPServer" >> /root/build-and-run.sh && \
      chmod +x /root/build-and-run.sh


    docker history ubuntu-utopic-pelican:latest
> view the history of hashes (which can be run by themselves) and timestamps and sizes

    IMAGE               CREATED             CREATED BY                                      SIZE
    39ac388d3c0d        37 seconds ago      /bin/sh -c #(nop) CMD [/bin/bash /root/build-   0 B
    218edf407f18        37 seconds ago      /bin/sh -c echo "#!/bin/bash" > /root/build-a   129 B
    d9d774d344bd        2 weeks ago         /bin/sh -c #(nop) EXPOSE 8000/tcp               0 B
    ae1733e0e1b9        2 weeks ago         /bin/sh -c pip install pelican Markdown beaut   20.64 MB
    24561ed8052f        2 weeks ago         /bin/sh -c curl https://bootstrap.pypa.io/get   9.826 MB
    1878a9a052eb        2 weeks ago         /bin/sh -c apt-get update && apt-get install    60.85 MB
    5e5e0e9171da        2 weeks ago         /bin/sh -c #(nop) MAINTAINER John Pfeiffer "h   0 B
    78949b1e1cfd        7 weeks ago         /bin/sh -c #(nop) CMD [/bin/bash]               0 B
    21abcc4ef877        7 weeks ago         /bin/sh -c sed -i 's/^#\s*\(deb.*universe\)$/   1.895 kB
    f552c527d701        7 weeks ago         /bin/sh -c echo '#!/bin/sh' > /usr/sbin/polic   215 kB
    c4c77a6165f9        7 weeks ago         /bin/sh -c #(nop) ADD file:24ed1895f2e500dcec   194.2 MB
    511136ea3c5a        22 months ago                                                       0 B
    

> experimental:
> `docker save 49b5a7a88d5 | sudo docker-squash -t ubuntu-utopic-pelican:squash | docker load`


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


|command|output|
|:-:|:-:|
|`docker run --detach --publish 0.0.0.0:6379:6379 --name redis redis`|feeb79581810a8c182202c73d4e1c6b905960bcfc860e04285f1ae03c6a47f18|
|`docker port redis`|6379/tcp -> 0.0.0.0:6379|
|`docker port redis 6379`|0.0.0.0:6379|
|`redis-cli -h docker.example.com ping`|PONG|
|`docker run --detach --publish-all --name redis redis`|ff2f6d2e04d565f11d71664bf6cf23638656d9b633e4d3c94444c81b18b807bb|
|`docker port redis`|6379/tcp -> 0.0.0.0:49153|
|`docker port redis 6379`|0.0.0.0:49153|

`docker run --detach -P --name johnssh trustyssh`
> publish all EXPOSE'd ports to random ports on the host


## Logs from the containers

`docker logs container_name`
> view the latest logs of a specific container in stdout

`docker logs -f container_name`
> tail the logs for


- - -
## Host data with a Docker Container
Volumes are where Docker Containers can access storage (either from the Host or other Containers)

<https://docs.docker.com/userguide/dockervolumes>

`docker run --interactive --tty --name mydata --volume /tmp/mydata:/opt/mydata trustyssh /bin/bash`
> create an interactive container named "mydata" that maps /tmp/mydata from the host onto /opt/mydata (warning: overriding any existing!)


- - -
## Managing or limiting the resources available to a Container
<https://docs.docker.com/engine/reference/run/#runtime-constraints-on-resources>

    docker run -i -t --rm --cpuset-cpu 0 --memory 512m ubuntu:14.04 /bin/bash
> the usual ubuntu trusty bash prompt but anything we run will be
> pinned to cpu 0 (i.e. 25% of a 4 core system) and have
> at most 512 MB of RAM and 512 MB of swap available

- - -
## Using Docker for a GUI application

Mostly outside of the vision of containerization (neither isolation nor performance exactly) is using Docker to run GUI applications without installing them on the Host.

Jessie Frazelle has done some excellent work pointing out how sharing the X11 socket from the host means lots of apps can run "without being installed" <https://github.com/jfrazelle/dockerfiles>

One tip she did not include was the part about XManager security, run the following if you run into an error

`xhost local:root`
- <https://www.netsarang.com/knowledgebase/xmanager/3898/xhost_and_how_to_use_it>
- <http://www.x.org/archive/X11R6.8.0/doc/xhost.1.html>

`xhost local:root; docker run --rm -v /tmp/.X11-unix:/tmp/.X11-unix -e DISPLAY=unix$DISPLAY --device /dev/snd jess/chromium`
- modify the xhost security to allow access to x windows
- ephemeral so do not save anything
- share the X11 unix socket
- bind to the current display (i.e. :0.0)
- allow sound from the Docker container


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
## Docker pre built Images from the Registry

### Redis
`docker search redis`
> search from the CLI but NAME, DESCRIPTION, STARS, OFFICIAL will only help you if you sort of already know what you are looking for

**<https://registry.hub.docker.com/_/redis/>**

    docker run --detach --publish 127.0.0.1:6379:6379 --name redis redis
> detached container based on the redis latest bound to the host on port 6379

> the image already includes by default the expose port command: EXPOSE 6379...
`apt-get install redis-tools; redis-cli`

> connect from the host to the redis container to the redis interactive cli


    docker run -i -t --link redis:db  johnssh /bin/bash

    root@d95a758eaa6b:/#
    apt-get install redis-tools
    env
    redis-cli -h $DB_PORT_6379_TCP_ADDR
    ping

> PONG

    get mykey
> "somevalue"

`docker stop johnssh`

`docker start --interactive --attach johnssh`

    root@d95a758eaa6b:/#

**Environment variables are tricky**

`sudo docker run --detach --publish 127.0.0.1:2222:22 --name johnssh trustyssh`
> if you SSH into your container or use byobu "env" will not show you the info

**From the host: **  `sudo docker inspect --format '{{ .NetworkSettings.IPAddress }}' redis`
> 172.17.0.72

    ssh -p 2222 root@localhost
    apt-get install redis-tools
    redis-cli -h 172.17.0.72 keys *
    1) mykey


** Add a route to the Host From inside a Container/Guest **

HOST:

    ip addr show
    ip addr show | grep docker0
    ip addr show | grep docker0 | grep global | awk '{print $2}' | cut -d / -f1
    HOSTIP=$(ip addr show | grep docker0 | grep global | awk '{print $2}' | cut -d / -f1)

`sudo docker run -i -t --rm --add-host=docker:${HOSTIP} python:2 /bin/bash`

    root@1bbe25092f19:/# cat /etc/hosts

    172.17.0.7      1bbe25092f19
    127.0.0.1       localhost
     ::1     localhost ip6-localhost ip6-loopback
    fe00::0 ip6-localnet
    ff00::0 ip6-mcastprefix
    ff02::1 ip6-allnodes
    ff02::2 ip6-allrouters
    
    172.17.42.1     docker

    root@1bbe25092f19:/# ping docker

    PING docker (172.17.42.1): 56 data bytes
    64 bytes from 172.17.42.1: icmp_seq=0 ttl=64 time=0.158 ms

<https://docs.docker.com/engine/reference/commandline/run/>

- - -
## Docker Compose
Complex real systems have multiple dependencies and following the recommended Docker pattern of "do one thing per container" means needing a way to start/orchestrate a bunch of things at once.

While there are some amazing open source projects (<http://kubernetes.io/> , <https://mesos.apache.org/documentation/latest/docker-containerizer/>) it is instructive to start with the simplest model provided directly from Docker, **<https://docs.docker.com/compose/>**

    sudo pip install --upgrade docker-compose
    docker-compose --version

### app.py

    :::python
    from flask import Flask
    from redis import Redis
    import os
    app = Flask(__name__)
    redis = Redis(host='redis', port=6379)
    
    @app.route('/')
    def hello():
        redis.incr('hits')
        return 'Hello World! I have been seen %s times.' % redis.get('hits')
    
    if __name__ == "__main__":
        app.run(host="0.0.0.0", debug=True)
    
### requirements.txt
    flask
    redis
    
### Dockerfile
    FROM python:2.7
    ADD . /code
    WORKDIR /code
    RUN pip install -r requirements.txt
    CMD python app.py

### docker-compose.yml

    web:
      build: .
      ports:
       - "5000:5000"
      volumes:
       - .:/code
      links:
       - redis
    redis:
      image: redis
   
- dependencies like redis are "linked" for network access (ordering in the file is important)
- "web" app (which comes from the current directory Dockerfile)
- ports: exposes ports to the host (all of these are just like the docker run CLI parameters)
- volumes: allows live editing of app.py
- redis comes from the public docker registry image (not a Dockerfile nor a private registry) and is using the default tag of "latest"

### docker-compose up    
    
`docker-compose up`
> this will docker pull redis and build from the Dockerfile and then start them all in the correct order

`docker-compose ps`
> run this command in the directory with the docker-compose.yml to see the state of the system

    :::text
             Name                      Command             State           Ports          
    -------------------------------------------------------------------------------------
    composeexample_redis_1   /entrypoint.sh redis-server   Up      6379/tcp               
    composeexample_web_1     /bin/sh -c python app.py      Up      0.0.0.0:5000->5000/tcp 


`docker ps -a`

`docker-compose stop`

<http://localhost:5000/>
> Hello World! I have been seen 2 times.


<https://bitbucket.org/johnpfeiffer/docker/src>

- - -
## Troubleshooting

### Building images with Dockerfile

**Building images often depends on the network and DNS**

If you are using Wifi be careful as intermittent network connectivity may cause frustrating issues.

For DNS with docker installed onto ubuntu via apt-get, try changing to Google DNS by uncommenting in:

`vi /etc/default/docker`

`sudo service docker restart`

**Building images often depends on dependencies**
look closely at error messages, i.e. make: not found and ensure that an early RUN statement has apt-get update && apt-get install -y build-essential


- - -
## More Info
- Real World example of using Docker for behind the firewall delivery: <https://bitbucket.org/atlassianlabs/ac-koa-hipchat-sassy/pull-request/6/readmemd-contains-instructions-on-how-to/diff>
- <https://github.com/wsargent/docker-cheat-sheet>
- <http://jpetazzo.github.io/2014/06/23/docker-ssh-considered-evil>


### Docker API and the Docker Hub Public Registry

Docker used to have an API endpoint at registry.hub.docker.com/v1 but in a fairly typical move for them they changed it so a lot of internet "documentation" examples are wrong.

Also the Docker Hub was deprecated as of 1.7 so this is the last docs on how to use it (because the service is still running or compatible)

    curl https://index.docker.io/v1/_ping
    true

It uses basic authentication and while you can use the API to sign up it may just be easier to use the web site: <https://hub.docker.com/>

    curl https://username:password@index.docker.io/v1/users/
    "OK"
> just curl with basic auth in order to check the credentials, the trailing slash is IMPORTANT 

**Using a browser with the Docker REST API is often more convenient as it caches the Basic Authentication**

- <https://docs.docker.com/v1.7/reference/api/docker-io_api/#users>
- <https://docs.docker.com/v1.6/reference/api/registry_api/> (because the registry api was deprecated earlier?)

To see all of the images for a given repository (it is json formatted and there will be a lot of results!)
    curl https://username:password@index.docker.io/v1/repositories/python/images

<https://docs.docker.com/v1.6/reference/api/registry_api/>

If you `docker search python` and want to see the tags (i.e. you do not want to pull every python image ever made), then try curl with REST:

    curl https://username:password@index.docker.io/v1/repositories/python/tags

    [{"layer": "a2db1214", "name": "latest"}, {"layer": "edb21ec7", "name": "2"}, {"layer": "82b600dd", "name": "2-alpine"}, {"layer": "6a4e9662", "name": "2-onbuild"}, {"layer": "99b38a11", "name": "2-slim"}, {"layer": "fe724fa0", "name": "2-wheezy"}, {"layer": "edb21ec7", "name": "2.7"}, {"layer": "82b600dd", "name": "2.7-alpine"}, {"layer": "6a4e9662", "name": "2.7-onbuild"}, {"layer": "99b38a11", "name": "2.7-slim"}, {"layer": "fe724fa0", "name": "2.7-wheezy"}, {"layer": "c71c2739", "name": "2.7.10"}, {"layer": "f1f35fa4", "name": "2.7.10-onbuild"}, {"layer": "843123ac", "name": "2.7.10-slim"}, {"layer": "fde41dc3", "name": "2.7.10-wheezy"}, {"layer": "edb21ec7", "name": "2.7.11"}, {"layer": "82b600dd", "name": "2.7.11-alpine"}, {"layer": "6a4e9662", "name": "2.7.11-onbuild"}, {"layer": "99b38a11", "name": "2.7.11-slim"}, {"layer": "fe724fa0", "name": "2.7.11-wheezy"}, {"layer": "a87a2288", "name": "2.7.7"}, {"layer": "481b175a", "name": "2.7.8"}, {"layer": "fbb30ed2", "name": "2.7.8-onbuild"}, {"layer": "3cf7f142", "name": "2.7.8-slim"}, {"layer": "6a873836", "name": "2.7.8-wheezy"}, {"layer": "2d0d0130", "name": "2.7.9"}, {"layer": "10948f7c", "name": "2.7.9-onbuild"}, {"layer": "e86252d0", "name": "2.7.9-slim"}, {"layer": "a11d441b", "name": "2.7.9-wheezy"}, {"layer": "a2db1214", "name": "3"}, {"layer": "bb6cd371", "name": "3-alpine"}, {"layer": "80662aa6", "name": "3-onbuild"}, {"layer": "07bfefb9", "name": "3-slim"}, {"layer": "2edf9614", "name": "3-wheezy"}, {"layer": "7575f4a5", "name": "3.2"}, {"layer": "31b273f6", "name": "3.2-onbuild"}, {"layer": "ca0a0ed6", "name": "3.2-slim"}, {"layer": "f5644650", "name": "3.2-wheezy"}, {"layer": "7575f4a5", "name": "3.2.6"}, {"layer": "31b273f6", "name": "3.2.6-onbuild"}, {"layer": "ca0a0ed6", "name": "3.2.6-slim"}, {"layer": "f5644650", "name": "3.2.6-wheezy"}, {"layer": "84717b99", "name": "3.3"}, {"layer": "4de0c1a0", "name": "3.3-alpine"}, {"layer": "e0985e72", "name": "3.3-onbuild"}, {"layer": "3c0f39af", "name": "3.3-slim"}, {"layer": "a13ad718", "name": "3.3-wheezy"}, {"layer": "e663e96e", "name": "3.3.5"}, {"layer": "79d3367e", "name": "3.3.5-onbuild"}, {"layer": "84717b99", "name": "3.3.6"}, {"layer": "4de0c1a0", "name": "3.3.6-alpine"}, {"layer": "e0985e72", "name": "3.3.6-onbuild"}, {"layer": "3c0f39af", "name": "3.3.6-slim"}, {"layer": "a13ad718", "name": "3.3.6-wheezy"}, {"layer": "c7184f4f", "name": "3.4"}, {"layer": "e6310f15", "name": "3.4-alpine"}, {"layer": "c38d9f7b", "name": "3.4-onbuild"}, {"layer": "ab9f7f65", "name": "3.4-slim"}, {"layer": "c98c4a9d", "name": "3.4-wheezy"}, {"layer": "b504e00c", "name": "3.4.1"}, {"layer": "07e5901a", "name": "3.4.1-onbuild"}, {"layer": "ec50e6a0", "name": "3.4.2"}, {"layer": "ade8543e", "name": "3.4.2-onbuild"}, {"layer": "dd1dee45", "name": "3.4.2-slim"}, {"layer": "de6911d6", "name": "3.4.2-wheezy"}, {"layer": "48bc52cc", "name": "3.4.3"}, {"layer": "bf599bc6", "name": "3.4.3-onbuild"}, {"layer": "0b92f173", "name": "3.4.3-slim"}, {"layer": "b8845e5b", "name": "3.4.3-wheezy"}, {"layer": "c7184f4f", "name": "3.4.4"}, {"layer": "e6310f15", "name": "3.4.4-alpine"}, {"layer": "c38d9f7b", "name": "3.4.4-onbuild"}, {"layer": "ab9f7f65", "name": "3.4.4-slim"}, {"layer": "c98c4a9d", "name": "3.4.4-wheezy"}, {"layer": "a2db1214", "name": "3.5"}, {"layer": "bb6cd371", "name": "3.5-alpine"}, {"layer": "80662aa6", "name": "3.5-onbuild"}, {"layer": "07bfefb9", "name": "3.5-slim"}, {"layer": "c64596cb", "name": "3.5.0"}, {"layer": "c9744d7e", "name": "3.5.0-onbuild"}, {"layer": "ac60c7d8", "name": "3.5.0-slim"}, {"layer": "31ef8f64", "name": "3.5.0b3"}, {"layer": "7c5e081c", "name": "3.5.0b3-onbuild"}, {"layer": "0c47d2de", "name": "3.5.0b3-slim"}, {"layer": "a2db1214", "name": "3.5.1"}, {"layer": "bb6cd371", "name": "3.5.1-alpine"}, {"layer": "80662aa6", "name": "3.5.1-onbuild"}, {"layer": "07bfefb9", "name": "3.5.1-slim"}, {"layer": "bb6cd371", "name": "alpine"}, {"layer": "80662aa6", "name": "onbuild"}, {"layer": "07bfefb9", "name": "slim"}, {"layer": "2edf9614", "name": "wheezy"}]


#### Docker Engine internal API
If instead of the docker client you wish to interact more programatically...

- <https://docs.docker.com/engine/reference/api/docker_remote_api/>
- <https://github.com/docker/distribution>

### Private Docker Registry

#### Login to a private docker registry

    curl -i https://username:password@docker.example.com/v2/
> attempt to login to a private registry

** Using the docker client to login to a private registry **

    docker login docker.example.com:443
    > Username: user@example.com
    > WARNING: login credentials saved in /home/USER/.docker/config.json
    > Login Succeeded


#### private registry basics via the browser

How to deploy your own docker registry: <https://docs.docker.com/registry/deploying/>

    https://docker.example.com/_ping
> {}

    https://docker.example.com/info
    https://docker.example.com/version
> note these commands may not be enabled or available in your private registry version 

    https://docker.example.com/v1/repositories/library/ubuntu/tags
> {"13.04": "5e47ac691989afcd10285ea4e67b46bc0fdc98d90844e57a6d4221c1e3ab4388"}

    https://docker.example.com/v1/repositories/micros/baseimage-ubuntu/tags
> {"latest": "5a14c1498ff4983793f6e5eddd16868dbad257195f0e85c66ece94d881ecb28f"}

    https://docker.example.com/v1/repositories/micros/baseimage-ubuntu/images
> list of the images available: [{"id":"8254ff58b098b72425854555204171352a69f5427ba83dee4642ba45d301d0b1"}]

    https://docker.example.com/v1/repositories/micros/baseimage-ubuntu/json
> inspect an image (what OS, kernel, etc.) {"arch": "amd64", "docker_go_version": "go1.3.3", "docker_version": "1.3.3", "kernel": "3.16.7-tinycore64", "last_update": 1426041024, "os": "linux"}

    https://docker.example.com/v1/repositories/myuser/nginx/0348bf1e7cc54327b8c9ce8407c5b3eadade1ef1771d642d08ae16a6aad5bed5/json
> inspect a very specific image (by id)


#### Searching a private docker registry

    https://registry.hub.docker.com/v1/search?q=pfeiffer
> the public docker registry search query, deprecated in APIv2 so no longer functional

    docker search docker.example.com/myuser
> the cli command returns a listing of all of the images for a user, deprecated in APIv2 so no longer functional

If there is a proxy in front: `docker search user:password@docker.example.com/myuser`

    curl -s -X GET https://user:password@docker.example.com/v1/search
> LIST ALL IMAGES: or use a browser https://docker.example.com/v1/search

    curl -X GET https://user:password@docker.example.com/v1/search?q=ubuntu
> https://docker.example.com/v1/search?q=ubuntu
> {"num_results": 4, "query": "ubuntu", "results": [{"description": null, "name": "example/ubuntu"}, {"description": null, "name": "library/ubuntu"}, {"description": null, "name": "micros/baseimage-ubuntu-ansible"}, {"description": null, "name": "micros/baseimage-ubuntu"}]}


- <https://www.digitalocean.com/community/tutorials/how-to-set-up-a-private-docker-registry-on-ubuntu-14-04>

