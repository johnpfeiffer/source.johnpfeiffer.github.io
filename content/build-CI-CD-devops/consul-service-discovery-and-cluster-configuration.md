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
But with the evolution of devops, web scale, microservices, containers, etc. it is great to leverage an existing battle tested solution*

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


## Distributed Configuration
A simple use case is to use the key value store to distribute other information besides services that need to be discovered, <https://www.consul.io/docs/agent/http/kv.html>
