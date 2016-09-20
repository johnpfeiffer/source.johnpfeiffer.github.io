Title: Debian Packages for Deployment and Reprepro for a local apt repository
Date: 2016-02-24 20:40
Tags: debian, deb, build, packaging, deployment, scale, reprepro, apt

[TOC]

### What is a Debian Package?

A debian package is a way to distribute and install a collection of files (aka software) onto a system (i.e. Debian or Ubuntu).

While a piece of software might depend on other debian packages (e.g. libraries) usually a single .deb file represents some sort of module that serves a single purpose.

Once a debian package is built any client (dpkg or apt which also uses dpkg ;) can use it to install the software.

- <https://www.debian.org/doc/manuals/debian-faq/ch-pkg_basics.en.html>

### Why use a Debian Package?

> When you're developing on your own box you can pretty much get away with anything

A complex and large scale production environment typically has a lot of costs (both operationally and in not becoming a bottleneck to dev velocity). Any opportunity to increase determinism and reduce risk is welcome.

Deploying source code directly from version control does not always scale well (streaming tons of small files, dedicated read only service user direct to production, etc.) nor does it create enough determinism with regards to dependency management.

As deployments become more frequent and Continuous Integration becomes more complex it is really important to embrace the "build once" principle so that a single artifact (hopefully with all of its dependencies) can pass through the gauntlet of integration testing and canary/incremental rollout.

So now that you're convinced "Artifacts" are the way to go lets just skip .exe, .msi, .jar, .etc and go straight to...

The Debian Package is a "battle tested" format with lots of features (dependency requirements, preinst scripts, postinst scripts, etc.) but if there is a bug in a specific .deb file it is not always practical to get the full source code and rebuild the whole thing (especially considering static bindings and specific compilation environment/parameters).

One example people give is an erroneous pre install or post install script that is preventing either installation or removal.

The example below is more on just simply changing the control file "Description:"

#### How to unpack a debian package, modify the control file, and repack it

To unpack, modify, and repack a debian package:

    :::bash
    docker run --rm --it --volume /tmp:/tmp ubuntu:14.04 /bin/bash
    sudo apt-get update
    apt-get install --yes vim wget
    wget https://example.com/example.deb --output-document /tmp/example.deb
    cd /tmp
    mkdir emptydir
    dpkg-deb -R example.deb /tmp/emptydir
    ls -ahl /tmp/emptydir
    ls -ahl /tmp/emptydir/DEBIAN
    vi /tmp/emptydir/DEBIAN/control
    dpkg-deb -b emptydir /tmp/example-fixed.deb

On your host /tmp should now contain example.deb and example-fixed.deb


- <https://unix.stackexchange.com/questions/138188/easily-unpack-deb-edit-postinst-and-repack-deb>
- <http://manpages.ubuntu.com/manpages/xenial/en/man1/dpkg-deb.1.html>

### reprepro for a local apt repository

Just as a debian provides more control over packaging and dependency management, you can also have your apt repository where you store debian packages.

By hosting your own apt repository you can:

- Create your own distribution server (e.g. in an s3 bucket)
- Create your own intermediate mirror or cache of an upstream repository (e.g. in a local area network shared drive)
- Create a local apt repository on local disk for a non internet connected device

The tool `reprepro` creates and manages the apt database and filesystem.

#### Setup Ubuntu 14.04 to install reprepro

It might be as simple as a single command to install reprepro but here is the full example in the case where you have broken or corrupted your sources.list:

    :::bash
    cat << EOF > /etc/apt/sources.list
        deb http://archive.ubuntu.com/ubuntu/ trusty main
        deb http://archive.ubuntu.com/ubuntu/ trusty universe
        deb http://archive.ubuntu.com/ubuntu/ trusty multiverse
        deb http://security.ubuntu.com/ubuntu trusty-security main restricted
    EOF
    
    rm -rf /var/lib/apt/lists
    apt-get clean; apt-get update
    apt-get install reprepro

- <http://manpages.ubuntu.com/manpages/trusty/en/man1/reprepro.1.html>


#### Setup the GPG key

A gpg key is an important part of apt for providing a digital signature of authenticity

    gpg --list-keys
    gpg --list-keys --with-fingerprint
    gpg --list-secret-keys --with-fingerprint
    gpg --allow-secret-key-import --import YOURKEY.gpg
> This allows for importing an existing gpg key into the local keyring (otherwise reprepro actions will not persist)

    gpg --yes --batch --delete-secret-keys "21E29B5B3F6D550EF4E2C2C9E9991E312341234"
    gpg --yes --batch --delete-keys "21E29B5B3F6D550EF4E2C2C9E9991E312341234"
> Removing or deleting a key seems to only work when you delete a key exactly by fingerprint

    echo ENCPASSWORD | gpg --yes --no-tty --batch --passphrase-fd 0 --output 8F13E123.key --decrypt 8F13E123.key.gpg
> Decrypt a password encrypted gpg key (that was encrypted with gpg - so meta!)

- <https://wiki.debian.org/SettingUpSignedAptRepositoryWithReprepro>

#### Setup a simple reprepro

Here we will setup a local apt mirror that is a filtered subset of the upstream mariadb repository

    :::bash
    mkdir -p /home/admin/apt/conf
    mkdir -p /home/admin/apt/logs
    mkdir -p /home/admin/apt/archive
    
    cat << EOF > /home/admin/apt/conf/distributions
    Origin: digitalocean-mariadb-10-trusty
    Codename: digitalocean-mariadb-10-trusty
    Description: local mirror of mariadb 10 trusty from the digital ocean sf mirror
    Architectures: amd64
    Components: main
    SignWith: 8F13E123
    Update: - digitalocean-mariadb-10-trusty
    Log: /home/admin/apt/logs/bintray-mirror.log
    EOF
    
    cat << EOF > /home/admin/apt/conf/options
        outdir /home/admin/apt/archive
        ask-passphrase
    EOF
    
    cat << EOF > /home/admin/apt/conf/updates
    Name: digitalocean-mariadb-10-trusty
    Suite: trusty
    Method: http://sfo1.mirrors.digitalocean.com/mariadb/repo/10.0/ubuntu/
    Components: main
    Architectures: amd64
    FilterList: deinstall /home/admin/apt/conf/mariadb-partial.list
    VerifyRelease: blindtrust
    EOF
    
    cat << EOF > /home/admin/apt/conf/mariadb-partial.list
    mariadb-partial.list
    libmariadbclient-dev install
    libmariadbclient18 install
    libmariadbd-dev install
    libmysqlclient18 install
    mariadb-client install
    mariadb-client-10.0 install
    mariadb-client-core-10.0 install
    mariadb-common install
    mariadb-connect-engine-10.0 install
    mariadb-server install
    mariadb-server-10.0 install
    mariadb-server-core-10.0 install
    mysql-common install
    EOF
    

> The configuration created
> - defines the Distribution
> - the option of output directory
> - how the Distribution becomes updated (blindtrust (lol))
> - explicitly what to download or blacklist from the upstream (exclude everything else)

- <https://mirrorer.alioth.debian.org/reprepro.1.html#CONFIG FILES>

#### Updating a remote source

Assuming the installation of reprepro and correct configuration of conf/options, conf/distributions, conf/updates, and conf/NAME-partial.list

Update a local repository from an upstream:

    :::bash
    reprepro --verbose --basedir /home/admin/apt check digitalocean-mariadb-10-trusty

    reprepro --verbose --basedir /home/admin/apt update digitalocean-mariadb-10-trusty
        aptmethod got 'http://sfo1.mirrors.digitalocean.com/mariadb/repo/10.0/ubuntu/dists/trusty/InRelease'
        aptmethod got 'http://sfo1.mirrors.digitalocean.com/mariadb/repo/10.0/ubuntu/dists/trusty/main/binary-amd64/Packages.gz'
        Calculating packages to get...
        Getting packages...
        aptmethod got 'http://sfo1.mirrors.digitalocean.com/mariadb/repo/10.0/ubuntu/pool/main/m/mariadb-10.0/libmariadbclient-dev_10.0.26+maria-1~trusty_amd64.deb'
    
    ls -ahl /home/admin/apt/archive
> should contain two directories: dists and pool

    reprepro --verbose --basedir /home/admin/apt check
> This will check all Distributions that have been configured for upstream changes

#### Listing or Adding or Removing a debian package with reprepro

Assuming you have setup your gpg signing key and config files correctly you can also just add a single package ad-hoc to your local apt repository

    :::bash
    reprepro dumpreferences
    reprepro --verbose --basedir . remove digitalocean-mariadb-10-trusty SOMEPACKAGENAME
    reprepro --verbose --basedir . includedeb digitalocean-mariadb-10-trusty SOMEFILENAME.deb
    reprepro export digitalocean-mariadb-10-trusty

- <https://mirrorer.alioth.debian.org/reprepro.1.html>
- <https://wikitech.wikimedia.org/wiki/Reprepro>

#### Configuring a client

    cat /etc/apt/sources.list.d/mariadb.list
        deb     file:///home/admin/apt/archive trusty main
    apt-get clean
    apt-get update
    apt-get search mariadb
> Now you can install mariadb from your local apt repository, or host it on s3 and change mariadb.list to have the bucket FQDN (`aws s3 --delete --exact-timestamps sync ./archive s3://mybucket`)

