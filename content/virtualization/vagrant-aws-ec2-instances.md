Title: Using Vagrant to deploy instances on AWS
Date: 2014-07-16 21:12

[TOC]

Vagrant is an infrastructure tool that simplifies deployment, such as virtual machines or in this case Amazon EC2 instances.

### Install Vagrant and the Vagrant AWS plugin

Download and install vagrant: **<https://www.vagrantup.com/downloads>**

    wget https://releases.hashicorp.com/vagrant/1.7.4/vagrant_1.7.4_x86_64.deb
    dpkg -i vagrant_1.7.4_x86_64.deb
    vagrant --version
    vagrant plugin install vagrant-aws

### Vagrant and VirtualBox with Ubuntu Trusty 14.04

The simple local VirtualBox method was:

    virtualbox --help
    vagrant init ubuntu/trusty64; vagrant up --provider virtualbox
    
        ==> default: Box 'ubuntu/trusty64' could not be found. Attempting to find and install...
        default: Box Provider: virtualbox
        default: Box Version: >= 0
        ==> default: Loading metadata for box 'ubuntu/trusty64'
        default: URL: https://atlas.hashicorp.com/ubuntu/trusty64


> this will do all the extra work for you of finding and downloading the "box" and starting it in VirtualBox

### Vagrant and AWS EC2 with Ubuntu Precise 12.04

`vagrant box add dummy https://github.com/mitchellh/vagrant-aws/raw/master/dummy.box`
> <https://atlas.hashicorp.com/boxes/search>

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
            aws.instance_type = "m4.large"
            aws.tags = {
                "Name" => "MyCloudInstance",
            }
            override.vm.box = "dummy"
            override.vm.box_url = "https://github.com/mitchellh/vagrant-aws/raw/master/dummy.box"
            override.ssh.username = "ubuntu"
            override.ssh.private_key_path = "./YOURKEYPAIRNAME.pem"
        end
    end

> ubuntu/images/ubuntu-precise-12.04-amd64-server-20130204 - ami-7747d01e , no ebs storage - just instance storage , <https://cloud-images.ubuntu.com/releases/> and <https://atlas.hashicorp.com/boxes/search>

> vagrant will by default upload all folders and files in your "project" folder where the Vagrantfile is located

> vagrant will start with the current working directory and look for a Vagrantfile, then go up one directory until it finds one: <https://docs.vagrantup.com/v2/vagrantfile/>


`vagrant up --provider=aws --debug`
> --debug is interactive mode and requires pressing enter between every step

    Bringing machine 'default' up with 'aws' provider...
    ==> default: HandleBoxUrl middleware is deprecated. Use HandleBox instead.
    ==> default: This is a bug with the provider. Please contact the creator
    ==> default: of the provider you use to fix this.
    ==> default: Warning! The AWS provider doesn't support any of the Vagrant
    ==> default: high-level network configurations (`config.vm.network`). They
    ==> default: will be silently ignored.
    ==> default: Launching an instance with the following settings...
    ==> default:  -- Type: m4.large
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
> the default-easiest-interface way of getting SSH access into the machine

`vagrant ssh-config`
> alternative interactive ssh session: Use the HostName or AWS EC2 WebUI or <http://aws.amazon.com/cli> to discover the remote machine IP address

> ssh -i YOURKEYPAIRHERE.pem ubuntu@1.2.3.4 ls -ahl /vagrant

`exit`

`vagrant ssh -c "ls -ahl"` for a non interactive listing of the home directory

> **vagrant ssh -c "pidof ntpd | xargs sudo kill -9"**

`vagrant up` , `vagrant reload` , and `vagrant provision` will have the AWS provider use rsync to push data to /vagrant

<https://docs.vagrantup.com/v2/synced-folders/rsync.html>

`vagrant stop`

> UnsupportedOperation => The instance 'i-1295bf39' does not have an 'ebs' root device type and cannot be stopped. (Fog::Compute::AWS::Error)

`vagrant destroy`

    > default: Are you sure you want to destroy the 'default' VM? [y/N] Y
    >
    > ==> default: Terminating the instance...

`vagrant destroy -f`

> non interactively destroy the instance and avoid the misleading error message: Vagrant is attempting to interface with the UI in a way that requires a TTY

### Vagrant provisioning

Allows for automated installation of software bundled into the `vagrant up` command

`vagrant up --provider=aws --no-provision` to prevent any provisioning

    config.vm.provision "shell", inline: "echo Hello, World"

    config.vm.provision "shell", path: "script.sh"

    config.vm.provision "shell", path: "https://example.com/script.sh"

<http://docs.vagrantup.com/v2/provisioning>

<http://docs.vagrantup.com/v2/provisioning/shell.html>

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
            aws.instance_type = "m4.large"
            aws.tags = {
                "Name" => "MyCloudInstance",
            }
            if ENV['bamboo_aws_use_iops']
              aws.block_device_mapping = [{ 'DeviceName' => '/dev/sda1', 'Ebs.VolumeSize' => 100, 'Ebs.VolumeType' => 'io1', 'Ebs.Iops' => 3000 }]
            else
              aws.block_device_mapping = [{ 'DeviceName' => '/dev/sda1', 'Ebs.VolumeSize' => 16, 'Ebs.VolumeType' => 'gp2' }]
            end
                        
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

- <https://github.com/mitchellh/vagrant-aws>
- <http://docs.aws.amazon.com/AWSEC2/latest/UserGuide/block-device-mapping-concepts.html>


### Vagrant and EC2 VPC (AMI that does not have/allow sudo)

    # -*- mode: ruby -*-
    # vi: set ft=ruby :

    Vagrant.configure("2") do |config|
        config.vm.box = "dummy"
        
        config.ssh.pty = true
        config.vm.synced_folder ".", "/vagrant", disabled: true

        config.vm.provider :aws do |aws, override|
        
            aws.access_key_id = "YOURACCESSKEY"
            aws.secret_access_key = "YOURSECRETKEY"
            aws.keypair_name = "YOURKEYPAIRNAME"
            aws.ami = "ami-7747d01e"
            aws.instance_ready_timeout = 300
            aws.instance_type = "m4.large"
            aws.tags = {
                "Name" => "MyCloudInstance",
            }
            aws.security_groups = [ "my_aws_security_group_id" ]
            aws.subnet_id = "my_aws_subnet_id"
            aws.associate_public_ip = true
            
            aws.user_data = "#cloud-boothook\n#!/bin/bash\ntouch /opt/.license/.eula\n"
            
            override.vm.box = "dummy"
            override.vm.box_url = "https://github.com/mitchellh/vagrant-aws/raw/master/dummy.box"

            override.ssh.username = "ubuntu"
            override.ssh.private_key_path = "/home/ubuntu/my_aws.pem"
        end
    end


- - -
**`vagrant up --provider=aws --no-provision --debug`**
- - -

    INFO vagrant: `vagrant` invoked: ["up", "--provider=aws", "--no-provision", "--debug"]

    Bringing machine 'default' up with 'aws' provider...
    ==> default: Launching an instance with the following settings...
    INFO interface: info:  -- Type: m4.large
    INFO interface: info: ==> default:  -- User Data: #cloud-boothook
    INFO interface: info: ==> default:  -- Assigning a public IP address in a VPC: true
    ==> default: Waiting for instance to become "ready"...
    ==> default: Waiting for SSH to become available...

    DEBUG ssh: == Net-SSH connection debug-level log END ==
    INFO ssh: SSH is ready!
    DEBUG ssh: Re-using SSH connection.
    INFO ssh: Execute:  (sudo=false)
    DEBUG ssh: pty obtained for connection
    DEBUG ssh: stdout: export TERM=vt100

    **JOHN: cloud-boothook script should have run by now in here**
    
    DEBUG ssh: stdout: logout
    DEBUG ssh: Exit status: 0
    INFO run_instance: Time for SSH ready: 48.444087982177734
    INFO interface: info: Machine is booted and ready for use!

    which rsync    
    DEBUG ssh: stdout: /usr/bin/rsync
    
    INFO interface: info: Machine not provisioning because `--no-provision` is specified.
    
    
>After all of that it is safe to either have `vagrant provision` or `vagrant ssh -c "ls -ahl"`
    

- **Using a pseudo tty** is a required workaround if using an AMI that does not support tty / sudo (i.e. Amazon's default Linux AMI)
- - <https://docs.vagrantup.com/v2/vagrantfile/ssh_settings.html>
- - <https://github.com/mitchellh/vagrant/issues/1482>
- **Disabling the /vagrant synced project folder** is nice if you don't automatically want the Vagrantfile and everything in there rsynced to your EC2 instance (and avoids the ugly `mkdir -p /vagrant` which requires sudo)
- **AWS User Data** can be pushed in via Vagrant which allows for custom scripts / commands / package installation during the EC2 instance boot
- - <https://help.ubuntu.com/community/CloudInit>
- - <https://cloudinit.readthedocs.org/en/latest/topics/format.html#cloud-boothook>
- - <http://stackoverflow.com/questions/17413598/vagrant-rsync-error-before-provisioning>
> One of the use cases for an aws.user_data #cloud-boothook script has been to add to /etc/sudoers.d/ (thus avoiding later sudo issues with rsync)


### VirtualBox

A really easy A way to start an Ubuntu 14.04 box locally with VirtualBox, the shell provisioner is less elegant than chef/puppet/ansible but gets the job done (installs Docker and Docker Compose)

<https://www.virtualbox.org/wiki/Linux_Downloads>

#### Vagrantfile

    VERSIONS = {
      'trusty' => {
        'box' => "canonical-ubuntu-14.04",
        'box_url' => "https://cloud-images.ubuntu.com/vagrant/trusty/current/trusty-server-cloudimg-amd64-vagrant-disk1.box",
        'ami' => "ami-018c9568",
      },
    }
    
    
    Vagrant.configure("2") do |config|
        config.ssh.forward_agent = true
    
        version = VERSIONS[("trusty")]
    
        config.vm.provider "virtualbox" do |v, override|
          v.customize ["modifyvm", :id, "--memory", ENV['VM_MEMORY'] || 4096]
          v.customize ["modifyvm", :id, "--cpus", ENV['VM_CPUS'] || 2]
    
          override.vm.network :private_network, ip: "192.168.33.10"
          override.vm.box = version['box']
          override.vm.box_url = version['box_url']
        end
        
        config.vm.provision :shell, :inline => "sudo apt-key adv --keyserver hkp://keyserver.ubuntu.com:80 --recv-keys 36A1D7869245C8950F966E92D8576A8BA88D21E9"
        config.vm.provision :shell, :inline => "sudo sh -c 'echo deb https://get.docker.io/ubuntu docker main > /etc/apt/sources.list.d/docker.list'"
        config.vm.provision :shell, :inline => "sudo apt-get update"
        config.vm.provision :shell, :inline => "sudo apt-get install -y lxc-docker python-pip"
        config.vm.provision :shell, :inline => "sudo pip install --upgrade pip"
        config.vm.provision :shell, :inline => "sudo pip install --upgrade docker-compose"
        
    end
    

### more info

`ps aux | grep vagrant`
> nothing to see here but there is still state for machines started...

    vagrant global-status
    vagrant global-status --prune
    rm -rf .vagrant
    rm -rf /home/ubuntu/.vagrant.d

*If you use vagrant 1.7 don not be surprised if you see errors related to SSL, 1.6.3 FTW*


<https://github.com/mitchellh/vagrant-aws>


### Troubleshooting

`vagrant up --provider=aws --debug`

> ERROR: The provider 'aws' could not be found, but was requested to back the machine 'default'. Please use a provider that exists.

> RESOLUTION: try re-installing the vagrant-aws plugin again and immediately running the vagrant up command afterwards

> ERROR: Timeout when waiting for SSH , SSH not up: ... The private key to connect to the machine via SSH must be owned

> RESOLUTION: chown root:root  and chmod 400

> ERROR: INFO ssh: SSH not up: #<Vagrant::Errors::SSHAuthenticationFailed: SSH authentication failed! This is typically caused by the public/private keypair for the SSH user not being properly set on the guest VM

> RESOLUTION: ensure the correct user, i.e. ec2-user or ubuntu etc. is used in the override.ssh.username to match what the AMI expects

> ERROR: sudo: no tty present and no askpass program specified

> RESOLUTION: your VM (or more likely, AMI) does not have tty or allow sudo so try using the config.ssh.pty = true (and make sure no provisioning commands require sudo)

