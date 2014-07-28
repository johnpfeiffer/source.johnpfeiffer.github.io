Title: How To Install Virtualbox 3 on Centos 5 Minimal
Date: 2009-11-15 20:59
Author: John Pfeiffer
Slug: how-to-install-virtualbox-3-on-centos-5-minimal

<div class="field field-name-body field-type-text-with-summary field-label-hidden">
<div class="field-items">
<div class="field-item even">
From the install DVD  

choose no packages and customize all to deselect all packages

</p>

BEWARE: this is a very empty configuration so you will have to install
ALOT from yum...

</p>

yum install wget elinks sudo which

</p>

IF you need to do anything with "compiling"  

yum install make gcc

</p>

yum install kernel ? maybe necessary?  

yum install kernel-devel-$(uname -r)  

yum install kernel-headers-$(uname -r)

</p>

export KERN\_DIR=/usr/src/kernels/$(uname -r)-x86\_64

</p>

to add a repository, e.g. VirtualBox

</p>

So create the following file (in the directory)
/etc/yum.repos.d/virtualbox.repo

</p>

[virtualbox]  

name=RHEL/CentOS-$releasever / $basearch - VirtualBox  

baseurl=[http://download.virtualbox.org/virtualbox/rpm/rhel/][]$releasever/$basearch  

enabled=1  

gpgcheck=1  

gpgkey=[http://download.virtualbox.org/virtualbox/debian/sun\_vbox.asc][]

</p>

then try

</p>
<p>
</div>
</div>
</div>
</p>

  [http://download.virtualbox.org/virtualbox/rpm/rhel/]: http://download.virtualbox.org/virtualbox/rpm/rhel/
  [http://download.virtualbox.org/virtualbox/debian/sun\_vbox.asc]: http://download.virtualbox.org/virtualbox/debian/sun_vbox.asc
