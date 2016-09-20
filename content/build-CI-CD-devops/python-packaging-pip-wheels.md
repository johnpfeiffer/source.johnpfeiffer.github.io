Title: Python packaging pip wheels
Date: 2016-01-05 20:00
Tags: python, packaging, pip, wheels

[TOC]

### Installing packages with python

Pip is the standard way to install python packages

    sudo pip install packagename
> searches <https://pypi.python.org> and finds the latest version of the package, full docs <https://pip.pypa.io/en/latest/>

If you get the package name wrong you will have installed something completely different.

    sudo pip search packagename
> find packages similar to the name you provided (from pypi or whatever provider you are using)

<https://pip.pypa.io/en/stable/reference/pip_search/>

    sudo pip freeze
> displays what is installed

### Virtualenv for sanity and isolation

A common mistake is to use the global pip installation of the Operating System to store all of the installed dependencies.  As soon as you have conflicting version requirements this breaks.  As soon as you have multiple applications/services installing globally it becomes unmanageable.

Virtualenv creates a virtual environment (basically injecting a PATH into the environment) for python binaries and package installation.

#### Pinning Versions and Guaranteed Sourcing

One common mistake is to not pin version numbers and depend on <https://pypi.python.org>

Without pinning version numbers for your dependencies (listed one per line in requirements.txt) you will receive a nasty surprise when the maintainers make a breaking change and you get a newer version unexpectedly.  Since python is a dynamic language you may receive the worst kind of surprise in production (hopefully nothing as bad as data corruption or security issues).

When you do pin the version number BUT still depend on https://pypi.python.org to provide the file then the project maintainers may remove the version you are pinned to (causing your builds to fail - though some for some cowboys this will cause production deployments to fail).

**Pin the version of your dependencies, provide the dependencies locally or through a system under your control (your own pypi server or s3 bucket)** , explicit is better than implicit.

### Wheels are better Python Packaging
Wheels are (awesome), it's the beginning of trying to make python installations more deterministic and pip less dynamic at install time. <http://wheel.readthedocs.org/en/latest/>

An output directory of the wheels of a project are known by convention as a "wheelhouse".

As a side effect the wheel directory, “/tmp/wheelhouse” in the example, contains installable copies of the exact versions of your application’s dependencies. By installing from those cached wheels you can recreate that environment quickly and with no surprises.

When you install using pip it looks for a “wheel file” (*.whl which is the newer zip compressed format, goodbye .egg) of the correct name for your (virtual) environment (e.g. py2 or py3 or x86 linux).  This wheel file saves time and bugs from installing a package/.egg  from source (usually that time is spent compiling C code for the python library).

    :::bash
    sudo pip install wheel
    cd projectsource
    python setup.py bdist_wheel
    ls -l ./dist
    pip wheel  --find-links /root/wheelhouse --wheel-dir=/root/wheelhouse -r requirements.txt


- <https://pip.pypa.io/en/stable/reference/pip_wheel/>
- <http://pip-python3.readthedocs.org/en/latest/reference/pip_wheel.html#build-system-interface>

#### installing using a wheel file

    pip install somepackage-version-py2.py3.whl
    pip freeze

#### error: invalid command 'bdist_wheel'

<https://pypi.python.org/pypi/docutils#downloads> only provided a py3 wheel (facepalm)

Downloading the source .tar.gz and running python setup.py bdist_wheel resulted in:
    error: invalid command 'bdist_wheel'

Reading the internet provided no comprehensible answers (lots of "setuptools does not match your version of pip or wheel or whatever")

The following hacking seems to have provided a solution:

   :::bash
    python --version
    pip --version
    cd /tmp
    wget https://pypi.python.org/packages/source/d/docutils/docutils-0.12.tar.gz#md5=4622263b62c5c771c03502afa3157768
    tar xf docutils-0.12.tar.gz
    cd docutils-0.12
    virtualenv venv
    source venv/bin/activate
    python --version
    pip --version
    pip install wheel
    pip freeze
    python setup.py install
    pip freeze
    pip wheel .
    ls /tmp/docutils-0.12/wheelhouse
        docutils-0.12-py2-none-any.whl

