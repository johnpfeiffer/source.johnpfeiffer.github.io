Title: Consul Service Discovery and Cluster Configuration
Date: 2016-08-27 21:01
Tags: service discovery, consul, cluster, clustering, config

[TOC]

## Overview

Basically consul is an out-of-the-box service discovery system intended for clustered and highly available applications.

- <https://www.consul.io/intro/>
- <https://www.consul.io/docs/internals/jepsen.html>

This kind of infrastructure simplifies the programming of distributed systems so that it is easier to deliver value quickly on the actual domain problems.

*I have certainly done my fair share of hardcoded config files to "discover" dependency services and even used chef for "config management"...
But with the evolution of dev-ops, web scale, microservices, containers, etc. it is great to leverage an existing battle tested solution*

## Consul Cluster using Docker

Following the straightforward work from this Docker Image we can run a cluster on a single machine:

<https://hub.docker.com/r/progrium/consul/>


    :::bash
    sudo su
    docker run -d --name node1 -h node1 progrium/consul -server -bootstrap-expect 3
    JOIN_IP="$(docker inspect -f '{{.NetworkSettings.IPAddress}}' node1)"
    docker run -d --name node2 -h node2 progrium/consul -server -join $JOIN_IP
    docker run -d --name node3 -h node3 progrium/consul -server -join $JOIN_IP
    docker run -d -p 8400:8400 -p 8500:8500 -p 8600:53/udp --name node4 -h node4 progrium/consul -join $JOIN_IP

> The second 2 nodes join the first one in the cluster by using the inspected IP Address,
> the last container is a consul agent (not in the quorum) but has public ports for interactivity

    :::bash
    curl localhost:8500/v1/catalog/nodes
        [{"Node":"node1","Address":"172.17.0.2"},{"Node":"node2","Address":"172.17.0.3"},
        {"Node":"node3","Address":"172.17.0.4"},{"Node":"node4","Address":"172.17.0.5"}]
    dig @0.0.0.0 -p 8600 node1.node.consul
        ;; QUESTION SECTION:
        ;node1.node.consul.     IN  ANY
    
        ;; ANSWER SECTION:
        node1.node.consul.  0   IN  A   172.17.0.2


> REST API call to the list of nodes, then DNS client to get the Record for the first node

    :::bash
    curl http://localhost:8500/v1/status/leader
        "172.17.0.2:8300"
    curl http://localhost:8500/v1/status/peers
        ["172.17.0.2:8300","172.17.0.3:8300","172.17.0.4:8300"]
    
    curl http://localhost:8500/v1/health/node/node1

> some more REST calls about the basic nodes, RAFT leadership and peers, and node health

- <https://www.consul.io/docs/agent/http.html>
- <https://www.consul.io/docs/agent/dns.html>


    :::bash
    
    curl http://localhost:8500/v1/catalog/services
        {"consul":[]}
    curl http://localhost:8500/v1/catalog/service/web
        []
> Listing of the services available, no web service yet =)

### Alternative Install from Zip

    apt-­get install unzip
    wget https://releases.hashicorp.com/consul/0.7.0/consul_0.7.0_linux_amd64.zip
    unzip consul_0.7.0_linux_amd64.zip
    BINDIP=$(ifconfig eth0 | grep "inet addr" | cut -d ':' ­-f 2 | cut ­-d ' ' ­-f 1)
    ./consul agent ­bootstrap ­server ­bind=$BINDIP ­data­dir /tmp/consul
    
    netstat ­antp  | grep consul
    curl http://localhost:8500/v1/status/peers
> Note getting the IP Address on ubuntu 16.04 uses enp3s0 or enp25 which can be changed back via grub workaround: GRUB_CMDLINE_LINUX="net.ifnames=0 biosdevname=0"

- <https://www.consul.io/docs/agent/options.html>

## Registering a Service

Creating and running a very simplistic golang web server (assuming you have go installed ;) , `go run web.go`
<https://blog.john-pfeiffer.com/go-programming-intro-with-vs-code-and-arrays-slices-functions-and-testing/>
(though you could also use nginx in docker)

    :::go
    import (
        "fmt"
        "net/http"
    )
    
    func myHandler(w http.ResponseWriter, r *http.Request) {
        fmt.Fprintf(w, "hi\n")
    }
    
    func main() {
        http.HandleFunc("/", myHandler)
        http.ListenAndServe(":8080", nil)
    }

From the previous steps we should have an Agent where we can register the new web service...

    :::bash
    #!/bin/bash

    curl --header "content-type: application/json" -X PUT -d'{
      "ID": "web1",
      "Name": "web",
      "Tags": [
        "master",
        "v1"
      ],
      "Address": "127.0.0.1",
      "Port": 8080,
      "EnableTagOverride": false,
      "Check": {
        "HTTP": "http://localhost:8080/health",
        "Interval": "10s",
        "TTL": "15s"
      }
    }' http://localhost:8500/v1/agent/service/register

In order to verify the new service is registered (besides the 200 response code)

    curl http://localhost:8500/v1/catalog/services
        {"consul":[],"web":["master","v1"]}
    curl http://localhost:8500/v1/health/service/web
> Our new service is created and doing well

So many more things can be done with <https://www.consul.io/docs/agent/http/agent.html#agent_service_register>

Stopping the web server (control + C) and checking that Consul has noticed Status is critical |o/

    :::bash
    curl http://localhost:8500/v1/health/checks/web
        [{"Node":"node4","CheckID":"service:web1","Name":"Service 'web' check","Status":"critical","Notes":"","Output":"TTL expired","ServiceID":"web1","ServiceName":"web"}]


Starting the web server again and check

    :::bash
    curl http://localhost:8500/v1/health/service/web
        [{"Node":{"Node":"node4","Address":"172.17.0.5"},
        "Service":{"ID":"web1","Service":"web","Tags":["master","v1"],"Address":"127.0.0.1","Port":8080},
        "Checks":[{"Node":"node4","CheckID":"service:web1","Name":"Service 'web'check","Status":"critical",
            "Notes":"","Output":"TTL expired","ServiceID":"web1","ServiceName":"web"},
        {"Node":"node4","CheckID":"serfHealth","Name":"Serf Health Status","Status":"passing","Notes":"","Output":"Agent alive and reachable","ServiceID":"","ServiceName":""}]}]


### Redis in Containers as another Service

    docker run --rm -it -p 0.0.0.0:6379:6379 --name redis redis:alpine
    
    docker run --rm -it --link redis:redis redis:alpine redis-cli -h redis -p 6379 help keys
    docker run --rm -it --entrypoint=/bin/sh --link redis:redis redis:alpine
> By running a local redis service we can modify our simple Go web service to query consul and dynamically discover how to reach the correct dependency, "look mom, no config files!"

- <https://hub.docker.com/_/redis/>


## Distributed Configuration and the Go Client Library
A simple use case is to use the key value store to distribute other information besides services that need to be discovered.

Obviously interacting directly with Consul as a client from inside the application is beneficial to "keeping it all in the code" and not relying on config files or shell scripts.

- <https://www.consul.io/docs/agent/http/kv.html>
- <https://github.com/hashicorp/consul/tree/master/api>
- <https://godoc.org/github.com/hashicorp/consul/api>

> Documentation on the Key Value store and the official Go client library

### Python Client

Using an open source client can help avoid "do not repeat yourself" of writing the REST API wrapper (and benefiting from crowd source at work)

- <http://consulate.readthedocs.io/en/stable/>
- <https://github.com/gmr/consulate>

    sudo pip3 install consulate

Like all open source projects this has some bugs and outstanding PRs but it is better than another one I tried which was still in alpha (aka not really fully implemented) , <https://www.consul.io/downloads_tools.html>

## Some Gotchas

Consul has a few edge cases that you may need to address specifically:

1. If a node reboots and changes ip address it will not go well: <https://github.com/hashicorp/consul/issues/457> , the simplest case might be to just remove it's data directory and force it to rejoin without any data
2. If a new node attempts to join a cluster it needs to know the ip address of an existing node, there is no "auto discovery-join" mechanism except to delegate to Atlas, the paid SaaS product from HashiCorp, or of course to write your own workaround <https://www.consul.io/docs/guides/bootstrapping.html>
3. If all of the server nodes in the cluster go down then there is no auto-recovery (which is not surprising I suppose...) <https://www.consul.io/docs/guides/outage.html> , <https://github.com/hashicorp/consul/issues/454> , <https://github.com/hashicorp/consul/issues/526>, again, if you write your own wrapper to detect this scenario as the nodes reboot (or in an immutable world are re-added assuming you have solved #1 and #2 ;) they "should" be able to recover and reload from raft/peers.json
