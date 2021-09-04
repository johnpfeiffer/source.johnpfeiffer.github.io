Title: CircleCI for a Pelican static Github site
Date: 2021-09-03 21:00
Tags: circleci pelican github

[TOC]

When I realized my previous CI/CD vendor had finally broken something _(after 7 years travis.org incompatibly became travis.com)_ I decided out with the old and in with the new. Also, Python2 was deprecated so onto Python3!

So this article is a non-comprehensive reprise of How to Setup a Static Site with Github Pages...

- <https://blog.john-pfeiffer.com/how-to-set-up-a-pelican-static-blog-site/>
- <https://blog.john-pfeiffer.com/static-site-pelican-blog-with-github-pages-and-travis-ci/>

Luckily I already had dabbled in CircleCI so the fundamentals were an easy copy paste: <https://blog.john-pfeiffer.com/using-circleci-as-continuous-integration-and-continuous-deployment/>

Roughly we will:

1. have python
2. install dependencies (pelican)
3. (optional) install plugins
4. get blog source markdown _(ideally from version control like github)_
5. run build commands _(to convert markdown to html)_
6. push to a second github repository

# A new Pelican Dev Environment

_unfortunately getting Docker setup is outside the scope of this tutorial_

Just a practice run so you get a feel for it:

    :::bash
    sudo docker run --rm -it cimg/python:3.8 /bin/bash
    python --version
    python -m pip install "pelican[markdown]" beautifulsoup4
    exit
> an ephemeral docker container with interactive bash shell, cimg is the CircleCI optimized docker image, https://hub.docker.com/u/cimg versus https://hub.docker.com/r/circleci/python/

Installing Pelican is documented: <https://docs.getpelican.com/en/latest/>

## Using pelican-quickstart for a skeleton

_assuming you are still in your docker container shell_

    :::bash
    PYVER=$(ls /home/circleci/.pyenv/versions | grep 3.8)
    cd "/home/circleci/.pyenv/versions/$PYVER/bin/"
    ./pelican --version
    mkdir yoursite
    cd yoursite
    ../pelican-quickstart
      Welcome to pelican-quickstart v4.6.0.
      This script will help you create a new Pelican-based website.
      ... (accept all defaults) ...
      Done. Your new project is available at /home/circleci/.pyenv/versions/3.8.11/bin/yoursite
> A little directory dancing in the container to get to the pip installed pelican binary

You still need an article with a minimum of content...

`vim yoursite/content/my-article.md`

    :::text
    Title: My Article
    Date: 2021-09-09 22:22
    Category: Technology 
    
    Hello world.


## Generate html from markdown 

`./pelican yoursite/content/`
> creates an "output" directory with the HTML and all the index and other pages also updated

    :::text
    my-article.html
    archives.html
    authors.html
    categories.html
    category
    feeds
    index.html
    tags.html
    theme


## Docker volume with your pre-existing blog content

    :::bash
    sudo docker run --volume /home/ubuntu/blogsource/:/home/circleci/blogsource --rm -it cimg/python:3.8 /bin/bash
    mkdir /home/circleci/OUT
    PYVER=$(ls /home/circleci/.pyenv/versions | grep 3.8)
    cd "/home/circleci/.pyenv/versions/$PYVER/bin/"
   ./pelican /home/circleci/blogsource/pelican-project/content -o /home/circleci/OUT -s /home/circleci/blogsource/pelican-project/publishconf.py

> Docker will mount your local directory with pelican project markdown mapped to "/home/circleci/blogsource" in the docker container
_your local directory name and subdirectories are up to you ;)_

_If you do not specify a new "output directory" then pelican may get confused if there is already content in "pelican-project/output"_


# Linking Github to CircleCI

_assuming you have your blog markdown in a Github repository and logged into CircleCI and authorized it for access to your Github repos_

Click on the CircleCI button for your source code: "Setup a Project"

- Use CircleCI's template for a configuration (a python project)
- customize it: <https://circleci.com/docs/2.0/executor-types/>
- trial and error to get various commands in the docker container right (use the Dev environment above)
- There is a live-config-editor "Edit Config"

**save and merge (.circleci/config.yml)**

Now your source code (markdown) for your (pelican) blog should have a CircleCI configuration like the following:

**.circleci/config.yml**

    version: 2.1
    jobs:
      build:
        resource_class: small
        docker:
          - image: cimg/python:3.8
        steps:
          - checkout
          - run:
              name: Install Pelican and Build Content
              command: |
                python -m pip install "pelican[markdown]" beautifulsoup4
                pip freeze | grep pelican
                cd ..
                pwd
                ls -ahl /home/circleci/project
                find . -type f -iname pelican
                PYVER=$(ls /home/circleci/.pyenv/versions | grep 3.8)
                cd ".pyenv/versions/$PYVER/bin/"
                ./pelican --version
                mkdir -p /home/circleci/OUT
                ./pelican /home/circleci/project/content -o /home/circleci/OUT -s /home/circleci/project/publishconf.py
                ssh-add -D
                
          - add_ssh_keys:
                  fingerprints:
                              - "4e:c1:a6:83:...:cc"
          - run:
              name: Publish to GitHub Static Site
              command: |
                cd ..
                ls -ahl
                git clone git@github.com:johnpfeiffer/johnpfeiffer.github.io.git
                cd johnpfeiffer.github.io
                git config user.email "me@john-pfeiffer.com"
                git config user.name "John Pfeiffer CircleCI"
                git checkout master
                cp -a /home/circleci/OUT/* .
                git commit --allow-empty -am "CircleCI publishing $CIRCLE_BUILD_NUM from sha $CIRCLE_SHA1"
                ls -ahl ~/.ssh/
                GIT_SSH_COMMAND='ssh -v -i ~/.ssh/id_rsa_4ec1a683...cc' git push origin master

> Everything from add_ssh_keys and below should only be added once you have completed the SSH Key steps below

**Removing all SSH keys from the CircleCI agent is because we're done checking out this repo and need to not confuse Git later**


# Pushing to a Github Page repository

The target for all of this has been your Github static page: <https://pages.github.com/>

## Create a new SSH key dedicated to only this purpose

    :::bash
    ssh-keygen -t rsa -b 4096 -C "CircleCI Deploy Key with Write Access" -f /tmp/cikey
> Note that this key is just for CircleCI for just this one repo

Navigate to the "Deploy keys" section of the Settings of the Repo in github that will receive the pushes
e.g https://github.com/johnpfeiffer/johnpfeiffer.github.io/settings/keys

- click on "Add deploy key"
- Paste in the cikey.pub file contents
- Ensure the "Allow write access" checkbox is checked

In CircleCI:
Go to your source project (under your username) and choose the "Project Settings" button, then subsection SSH Keys
e.g. https://app.circleci.com/settings/project/github/johnpfeiffer/source.johnpfeiffer.github.io/ssh

Copy the private "cikey" (which starts with "-----BEGIN RSA PRIVATE KEY-----") into your buffer.
> Do not share or paste your private key anywhere else than CircleCI

Add an Additional SSH Key "Add SSH Key"
Hostname: githubstaticpage
Private Key: -----BEGIN RSA PRIVATE KEY-----...

Now copy the "Fingerprint" of the key e.g. something like 4e:c1:...
This is what goes in your circleCI config

## CircleCI config explained

This portion is your CircleCI agent manually checking out the actual "Pages" HTML repository:

    :::text
                git clone git@github.com:johnpfeiffer/johnpfeiffer.github.io.git
                cd johnpfeiffer.github.io
                git config user.email "me@john-pfeiffer.com"
                git config user.name "John Pfeiffer CircleCI"
                git checkout master

It is important to copy the new HTML content in...
                cp -a /home/circleci/OUT/* .

_technical debt is to use the rsync command to actually reflect removed content too_

Later we can use that fingerprint to explicitly specify git use that ssh key to push to github...

            GIT_SSH_COMMAND='ssh -v -i ~/.ssh/id_rsa_4ec1a683...cc' git push origin master

> ssh verbose shows you which Identity/Key is being used to deploy/push to Github


References
- <https://circleci.com/docs/2.0/add-ssh-key/>
- <https://blog.jdblischak.com/posts/circleci-ssh/>
- <https://discuss.circleci.com/t/multiple-deploy-keys-for-github/25658/8>
- <https://discuss.circleci.com/t/cloning-another-private-repo-in-the-build/25505/3>

# Pelican Plugins

My site still uses the old plugins which I "vendored" into the actual repo for simplicity:

- <https://github.com/johnpfeiffer/source.johnpfeiffer.github.io/tree/master/plugins> 
- <https://github.com/getpelican/pelican-plugins>
> 10 MB of legacy plugins at "getpelican" because they still work

Instructions on Pelican Plugins in general (and the new way that I have not yet adopted)
- <https://docs.getpelican.com/en/latest/plugins.html>

Thankfully this person documented how to use Pelican4.6 with MARKDOWN for the built in Table of Contents (TOC):
- <https://cloudbytes.dev/articles/add-a-table-of-contents-using-markdown-in-pelican>

