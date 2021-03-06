Title: Build Automation using packer to build an AMI use immutable not chef
Date: 2015-07-06 20:40
Tags: cloud, packer, build, ami, chef

[TOC]

### Why build automation?

Software has always been about automation and leveraging the computer's capacity for precision and repetition.

Somehow though, software is sometimes still deployed using a series of often poorly documented steps (to physical hardware even!). I've been there, it ain't pretty. (badpokerface)

The second time you need to build a server running service(s) you may be under time pressure. (Murphy's law says you might be building it again because the first one which was business critical blew up unexpectedly.)

Building things by hand is possibly the most expensive way to generate impossible to reproduce bugs and job security for the personality challenged.

(Almost everyone agrees that technology employees are expensive and so by extension their time is constantly being wasted by everything they do).

As virtualization (and linux!) took over the world there was an explosion of virtual machines that needed to be deployed and an evolution of a fairly standard virtual harwdare layer. (x86 cpu and Intel NIC anyone?)

Suddenly you couldn't hire enough antisocial people to run around with floppies and scratching cds while shoving them into servers.

### Why not chef?

Chef, Puppet, and Ansible are the well known configuration management and build/deployment automation tools.

Automated configuration management which tries to keep a remote server in a specific state seems like a good recipe for things going wrong

I've used chef successfully quite a few times and the main things that make it a specialized tool that I prefer not to use:

1. It's really easy to do chef wrong: nested roles and recipes that keep exploding exponentially with circular dependencies which make you think software development starts looking easy again.
2. Community cookbooks are written to allow deployment on every architecture ever created (Debian, Ubuntu, RedHat, Windows, SPARC, etc.) which makes them challenging to read and debug, almost impossible to customize to do what you actually want.
3. The ruby based DSL isn't bad but it's pretty annoying to constantly make syntax errors (which unless you're all TDD rambo and use Kitchen you'll find during the never ending waiting many minutes for a deployment to fail)
4. It's difficult to debug the non intuitive "compilation phase" and "execution phase" way chef does its dependency tree magic, and the "shoot yourself in the foot" is compounded with the apparently edge case necessary compile time run executions
5. The "best practices" have changed 3 or 4 times (write your own custom cookbooks, leverage the community cookbooks, write a custom wrapper for the community cookbook, don't ever use set_unless even though it still exists, etc.) and the 6 layers of variable overrides makes it hard to keep track of what the actual output of a script will be (don't worry, they have pages of documentation explaining it)
6. The recommended "chef client server architecture" does not scale to really large numbers well and creates administration overhead and a lot of authorization complexity - and my preferred method with "chef solo" still requires an annoying amount of bootstrap setup on the target machines.
7. Polling not only creates network congestion but worse creates windows of uncertainty about deployment state and the possibility of nodes silently dropping out <https://docs.chef.io/chef_client.html>
8. Chef tends to encourage the pattern of long lived mutable servers (with their therefore necessary expensive and obnoxious biological caretakers)

- <https://docs.chef.io/resource_common.html#lazy-evaluation>
- <https://docs.chef.io/resource_common.html#run-in-compile-phase>
- <http://erik.hollensbe.org/2013/03/16/the-chef-resource-run-queue/>

So is there a simpler way to just reliably, reproducibly, build a box?

### Packer to the rescue

Packer is from the same people who brought you Vagrant <https://www.vagrantup.com/> , that really easy way to set up a virtual machine... <https://blog.john-pfeiffer.com/using-vagrant-to-deploy-instances-on-aws>

It is very straightforward to read and actually you can still leverage chef (unless you realize that a series of shell commands is all you wanted anyways...)

This leads to the better path of "immutable servers" <http://martinfowler.com/bliki/ImmutableServer.html>

`packer --version`


#### my_example_box.json

    :::json
    {
      "variables": {
        "aws_access_key": "",
        "aws_secret_key": ""
      },
      "builders": [{
        "type": "amazon-ebs",
        "access_key": "{{user `aws_access_key`}}",
        "secret_key": "{{user `aws_secret_key`}}",
        "region": "us-east-1",
        "source_ami": "ami-de0d9eb7",
        "instance_type": "t1.micro",
        "ssh_username": "ubuntu",
        "ami_name": "packer-example {{timestamp}}"
      }]
    }
    
`packer validate mybox.json`

`packer build mybox.json`

`packer build -debug mybox.json`
> This will prompt for the enter key to continue at each step

Once it's done it will terminate the EC2 instance for you (it only runs as long as it takes to build the machine and then burn the Amazon Machine Image).

**us-east-1: ami-19601234**
> Unfortunately it is not machine readable json output so you have to do some bash-fu to extract just the id

> Also unfortunately there is no way to tell packer to not terminate so you can troubleshoot, the workarounds are the -debug which is essentially "interactive" or adding sleep commands


#### my_advanced_box.json

    :::json
    {
      "_comment": "This is a comment",
      "variables": {
          "my_secret": "{{env `MY_SECRET`}}",
      },
      "builders": [{
        "type": "amazon-ebs",
        "region": "us-east-1",
        "source_ami": "ami-de0d9eb7",
        "instance_type": "t1.micro",
        "ssh_username": "ubuntu",
        "ami_name": "packer-example {{timestamp}}"
        "subnet_id": "subnet-f0be1234",
        "security_group_id": "sg-9bf51234",
        "associate_public_ip_address": true,
        "ssh_keypair_name": "my-packer",
        "ssh_private_key_file": "./my-packer.pem"
      }],
      "provisioners": [{
        "type": "file",
        "source": "./debs/",
        "destination": "/tmp"
      },
      {
        "type": "shell",
        "inline": [
          "/sbin/ip a",
          "curl -s http://checkip.amazonaws.com",
          "ls -ahl /tmp",
          "echo {{user `my_secret`}} > /tmp/{{isotime \"2006-01-02-030405\"}}--my-secret.txt",
          "sudo dpkg -i --force-confnew /tmp/*.deb",
          "machine_state_validation.sh"
        ]
      }]
    }
    
> The access credentials could instead be environment variables: AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY

> Post instantiation validation is a really handy safeguard as statistically something always goes wrong somewhere and it's far cheaper to find out with a quick test versus a system that loses data.


### Packer and DigitalOcean

DigitalOcean is a relatively new player (compared to Linode and even AWS) but they provide a very fast and easy to use way of building boxes (a snapshot can be used like an AMI to spin up multiple instances).

    {
      "_comment": "https://www.packer.io/docs/builders/digitalocean.html",
      "variables": {
        "digitalocean_api_token": "{{env `DIGITALOCEAN_API_TOKEN`}}",
        "newuser_name": "{{env `NEWUSER_NAME`}}",
        "newuser_password": "{{env `NEWUSER_PASSWORD`}}"
      },
    
      "builders": [{
        "type": "digitalocean",
        "api_token": "{{user `digitalocean_api_token`}}",
        "size": "512mb",
        "region": "lon1",
        "image": "ubuntu-16-04-x64",
        "droplet_name": "built-from-packer-{{timestamp}}",
        "snapshot_name": "built-from-packer-{{timestamp}}"
      }],
    
      "provisioners": [
        {
          "type": "shell",
          "inline": [
            "ip a",
            "curl -s http://checkip.amazonaws.com",
            "apt-get update",
            "sudo apt-get install -y vim curl wget byobu ntp",
            "timedatectl set-timezone Etc/UTC",
            "cat /etc/timezone",
            "date",
            "useradd -s /bin/bash -m {{user `newuser_name`}}",
            "usermod -a -G admin {{user `newuser_name`}}",
            "echo '{{user `newuser_name`}}:{{user `newuser_password`}}'|chpasswd",
            "cat /etc/passwd",
            "sed -i 's/Port 22/Port 2222/g' /etc/ssh/sshd_config",
            "sed -i 's/PermitRootLogin yes/PermitRootLogin no/g' /etc/ssh/sshd_config",
            "echo 'PasswordAuthentication no' >> /etc/ssh/sshd_config",
            "cat /etc/ssh/sshd_config",
            "mkdir -p /home/{{user `newuser_name`}}/.ssh",
            "mkdir -p /opt/www/html"
          ]
        },
        {
          "type": "file",
          "source": "authorized_keys",
          "destination": "/home/{{user `newuser_name`}}/.ssh/authorized_keys"
        }
      ]
    
    }
    
> This is a simple example that automates some of the security best practices of a non standard username, non standard ssh port, no ssh root login, no ssh password based login, etc.

    NEWUSER_NAME=yourusername NEWUSER_PASSWORD=yourpassword DIGITALOCEAN_API_TOKEN=012345yourtoken /opt/packer build packer.json


### Why not docker containers?

Actually I prefer docker containers as the artifact and deployment vehicle for services but it's not the only hammer in your toolbelt.  And you have to setup the Docker hosts somehow, right? 

(Unless you've already uploaded your soul into the matrix and are using Googazon's PaaS and never have to sully your container delicate fingers with a crude virtual machine again).

### more info

- https://www.packer.io/docs/installation.html
- https://www.packer.io/docs/builders/amazon-ebs.html
- https://www.packer.io/intro/getting-started/build-image.html
- https://www.packer.io/docs/templates/configuration-templates.html
- https://www.packer.io/docs/templates/user-variables.html

