Title: Using Vagrant to deploy instances on AWS
Date: 2014-07-16 21:12

[TOC]

Using Vagrant to deploy instances on AWS...

### Install Vagrant and the Vagrant AWS plugin

Download and install vagrant: **[https://www.vagrantup.com/downloads](https://www.vagrantup.com/downloads)**

`wget https://dl.bintray.com/mitchellh/vagrant/vagrant_1.6.3_x86_64.deb ; dpkg -i vagrant_1.6.3_x86_64.deb`

`vagrant box add dummy https://github.com/mitchellh/vagrant-aws/raw/master/dummy.box`

`vagrant box list`

`vi Vagrantfile`

    Vagrant.configure("2") do |config|
        config.vm.box = "dummy"
        config.vm.provider :aws do |aws, override|
            aws.access_key_id = "YOURACCESSKEY"
            aws.secret_access_key = "YOURSECRETKEY"
            aws.keypair_name = "YOURKEYPAIRNAME"
            aws.ami = "ami-7747d01e"
            aws.instance_ready_timeout = 300
            aws.instance_type = "m3.large"
            aws.tags = {
                "Name" => "MyCloudInstance",
            }
            override.vm.box = "dummy"
            override.vm.box_url = "https://github.com/mitchellh/vagrant-aws/raw/master/dummy.box"
            override.ssh.username = "ubuntu"
            override.ssh.private_key_path = "./YOURKEYPAIRNAME.pem"
        end
    end

> ubuntu/images/ubuntu-precise-12.04-amd64-server-20130204 - ami-7747d01e , no ebs storage - just instance storage

> vagrant will by default upload all folders and files in your "project" folder where the Vagrantfile is located


`vagrant plugin install vagrant-aws`

`vagrant up --provider=aws --debug`

    Bringing machine 'default' up with 'aws' provider...
    ==> default: HandleBoxUrl middleware is deprecated. Use HandleBox instead.
    ==> default: This is a bug with the provider. Please contact the creator
    ==> default: of the provider you use to fix this.
    ==> default: Warning! The AWS provider doesn't support any of the Vagrant
    ==> default: high-level network configurations (`config.vm.network`). They
    ==> default: will be silently ignored.
    ==> default: Launching an instance with the following settings...
    ==> default:  -- Type: m3.large
    ==> default:  -- AMI: ami-7747d01e
    ==> default:  -- Region: us-east-1
    ==> default:  -- Keypair: YOURKEYPAIRHERE
    ==> default:  -- Block Device Mapping: []
    ==> default:  -- Terminate On Shutdown: false
    ==> default:  -- Monitoring: false
    ==> default:  -- EBS optimized: false
    ==> default:  -- Assigning a public IP address in a VPC: false
    ==> default: Waiting for instance to become "ready"...
    ==> default: Waiting for SSH to become available...
    ==> default: Machine is booted and ready for use!
    ==> default: Rsyncing folder: /home/ubuntu/myproject/ => /vagrant

`vagrant ssh`

> alternative interactive ssh session: Use the AWS EC2 WebUI or [http://aws.amazon.com/cli](http://aws.amazon.com/cli/) to discover the IP address

> ssh -i YOURKEYPAIRHERE.pem ubuntu@1.2.3.4 ls -ahl /vagrant

`exit`

`vagrant ssh -c "ls -ahl"` for a non interactive listing of the home directory

`vagrant up` , `vagrant reload` , and `vagrant provision` will have the AWS provider use rsync to push data to /vagrant
[https://docs.vagrantup.com/v2/synced-folders/rsync.html](https://docs.vagrantup.com/v2/synced-folders/rsync.html)

`vagrant stop`

> UnsupportedOperation => The instance 'i-1295bf39' does not have an 'ebs' root device type and cannot be stopped. (Fog::Compute::AWS::Error)

`vagrant destroy`

    > default: Are you sure you want to destroy the 'default' VM? [y/N] Y
    >
    > ==> default: Terminating the instance...

### Vagrant provisioning

Allows for automated installation of software bundled into the `vagrant up` command

`vagrant up --provider=aws --no-provision` to prevent any provisioning

    config.vm.provision "shell", inline: "echo Hello, World"

    config.vm.provision "shell", path: "script.sh"

    config.vm.provision "shell", path: "https://example.com/script.sh"

[http://docs.vagrantup.com/v2/provisioning](http://docs.vagrantup.com/v2/provisioning)

[http://docs.vagrantup.com/v2/provisioning/shell.html](http://docs.vagrantup.com/v2/provisioning/shell.html)

### Advanced Vagrantfile example
    # -*- mode: ruby -*-
    # vi: set ft=ruby :

    if ENV['UPDATEFQDN']
      updatedfqdn=ENV['UPDATEFQDN']
    end
    
    $fqdnscript = <<FQDNSCRIPT
    echo "I am updating fqdn to #{updatedfqdn}..."
    cat /etc/hosts | grep "#{updatedfqdn}" || sudo sed 's/127.0.0.1/127.0.0.1 #{updatedfqdn}/' -i /etc/hosts
    hostname | grep "#{updatedfqdn}" || sudo hostname #{updatedfqdn}
    FQDNSCRIPT

    Vagrant.configure("2") do |config|
        config.vm.box = "dummy"
        config.vm.provider :aws do |aws, override|
            aws.access_key_id = "YOURACCESSKEY"
            aws.secret_access_key = "YOURSECRETKEY"
            aws.keypair_name = "YOURKEYPAIRNAME"
            aws.ami = "ami-7747d01e"
            aws.instance_ready_timeout = 300
            aws.instance_type = "m3.large"
            aws.tags = {
                "Name" => "MyCloudInstance",
            }
            override.vm.box = "dummy"
            override.vm.box_url = "https://github.com/mitchellh/vagrant-aws/raw/master/dummy.box"
            override.ssh.username = "ubuntu"
            override.ssh.private_key_path = "./YOURKEYPAIRNAME.pem"
            override.vm.synced_folder "./chef-repo", "/tmp/chef-repo", type: "rsync", create: true, rsync__exclude: ".git/"
        end
        config.vm.provision :shell, :inline => "echo `hostname -f` >> /home/ubuntu/currenthostname.txt"
        config.vm.provision :shell, :inline => $fqdnscript
    end

    Bringing machine 'default' up with 'aws' provider...
    ==> default: Running provisioner: shell...
    ==> default: Running: inline script
    stdin: is not a ttty
    I am provisioning and updating hostname...
    

> synced_folder is to sync other folders in your filesystem besides the folder with the Vagrantfile

> config.vm.hostname does not appear to work on AWS EC2 so the workaround above (|| statements to prevent extra reconfiguration)


### more info

[https://github.com/mitchellh/vagrant-aws](https://github.com/mitchellh/vagrant-aws)


### Troubleshooting

`vagrant up --provider=aws --debug`

> ERROR: The provider 'aws' could not be found, but was requested to back the machine 'default'. Please use a provider that exists.

> RESOLUTION: try re-installing the vagrant-aws plugin again and immediately running the vagrant up command afterwards

> ERROR: Timeout when waiting for SSH , SSH not up: ... The private key to connect to the machine via SSH must be owned

> RESOLUTION: chown root:root  and chmod 400