Title: Virtualenv Python Interpreter from source
Date: 2014-10-31 00:00
Tags: python, python3, pip, virtualenv, dependency management

[TOC]

When building an application (including an external facing webapp or an internal test suite) it is critical to manage your dependencies.

Virtualenv is a tool that keeps all the dependencies in a file system based container (and overcomes permissions based issues as well).

To really isolate your application from the environment not only do you need a specific version of libraries (i.e. you know your application works fine with requests 2.4.3 and selenium 2.44) but additionally a specific version of the Python Interpreter.


## Build python from source

    wget https://www.python.org/ftp/python/2.7.8/Python-2.7.8.tgz
    tar -xf Python-2.7.8.tar.gz
    cd Python-2.7.8
    ./configure --prefix=/home/ubuntu/python --enable-unicode=ucs4
    make && make altinstall
    
    /home/ubuntu/python/bin/python2.7 --version

> altinstall ensures we do not try to override the existing /usr/bin/python binary which can be important if you want python 2.7.3 and python 2.7.8 to exist side by side

Optionally: `echo 'alias py="/home/ubuntu/python/bin/python2.7"' >> ~/.bashrc`

### python3 from source

    wget https://www.python.org/ftp/python/3.4.2/Python-3.4.2.tgz
    tar -xf Python-3.4.2.tar.gz
    cd Python-3.4.2
    ./configure --prefix=/opt/python3.4.2 && make -j$(nproc) && make altinstall
    ls -ahl /usr/local/bin | grep 3.4
    
    /usr/local/bin/pip3.4 install --upgrade virtualenv

### If you mess up your OS level python

`apt-get install python3`

    python3 depends on dh-python; however:
    Package dh-python is not configured yet.

Look at the stack trace, reinstalling may not have put all of the helper directory and .py files in place

    File "/usr/lib/python3.4/site.py", line 586, in <module>
    ImportError: No module named '_sysconfigdata_m'
	
    mv /usr/lib/python3.4 /usr/lib/python3.4-OLD
    wget http://mirrors.kernel.org/ubuntu/pool/main/d/dh-python/dh-python_1.20140128-1ubuntu8_all.deb
    dpkg -i --force-depends dh-python_1.20140128-1ubuntu8_all.deb
    apt-get install python3


And in my case I needed to reinstall loads of python3 stuff: `apt-get install xubuntu-destkop`
    
## Installing virtualenv

**`sudo pip install --upgrade virtualenv`**
> getting the latest version of virtualenv as any OS packages are likely to be outdated
> alternatively you can go all out and just use virtualenv locally from source

### virtualenv from source
   
    wget https://pypi.python.org/packages/source/v/virtualenv/virtualenv-X.X.tar.gz
    tar -xf virtualenv-X.X.tar.gz
    cd virtualenv-X.X
    /home/ubuntu/python/bin/python2.7 virtualenv.py myvenv

> does not require sudo and works around path or permissions requirements

## Example Usage

**`virtualenv myvenv`**
> creates a local copy of required files like the python interpreter and its own version of pip

    :::text
    myvenv
    | -- bin
         | -- activate
         | -- easy_install
         | -- pip
         | -- python
    | -- include
    | -- lib
         | -- python2.7
             | -- site-packages
                  | -- pip
                  | -- setuptools
    | -- local
    
    
`myenv/bin/pip install --upgrade requests`
> no sudo was required to add locally myvenv/lib/python2.7/site-packages/requests

    myenv/bin/python
    >>> import requests
    >>> print requests.__version__



### Using virtualenv with a specific python version or binary

    virtualenv -p python3.5 venv
    source venv/bin/activate
    python --version
    which pip
> Python 3.5.0+
> the shortest example to use the OS python3.5 binary when creating the venv directory with the virtual environment

    virtualenv --python=/home/ubuntu/python/bin/python2.7 myvenv
    myenv/bin/python
> Python 2.7.8
> the advanced example uses a python binary that was created from source to ensure the application does not suffer when the OS has a python upgrade (or your libraries need a newer version of python than provided)

`virtualenv --version`
> just in case your version of virtualenv has a bug and needs to be upgraded first


### activate and deactivate to update your environment temporarily

Rather than using the explicit paths (which is the most clear but cumbersome) you can override your shell Environment:

`/usr/bin/python --version`
> 2.7.3

`source myenv/bin/activate`
`python --version`
> 2.7.8

`pip install requests`
> no sudo was required to add locally myvenv/lib/python2.7/site-packages/requests

`deactivate`



## More Info

When using git make sure .gitignore contains the "myenv" directory as you do not want to store these binaries in version control.

Typically Heroku or other PaaS allow you to specify a python interpreter version and library requirements in a configuration file.

- <http://virtualenv.readthedocs.org/en/latest/virtualenv.html>
- <https://www.python.org/downloads>
- <https://www.digitalocean.com/community/tutorials/common-python-tools-using-virtualenv-installing-with-pip-and-managing-packages>
