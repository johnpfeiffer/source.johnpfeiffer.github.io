Title: Static site pelican blog with GitHub Pages and Travis CI
Date: 2014-09-15 04:04
Tags: static site, pelican blog, github pages, travis ci

[TOC]

Setting up a static blog site I decided to follow some great Dev Ops principles:

- Convention over customization
- Minimal infrastructure to maintain
- Leverage the cloud (from reliable vendors)

Also, being "an efficient engineer" I had the extra hard requirement of "free" =p

Related articles:

- <https://blog.john-pfeiffer.com/how-to-set-up-a-pelican-static-blog-site/>
- <https://blog.john-pfeiffer.com/static-site-with-bitbucket-and-shippable-and-pelican/>

## Github Setup

Sign in to GitHub , <https://github.com/login>

Create two new **public repos**: username.github.io and source.username.github.io

In source.username.github.io you will put the source markdown and theme etc. from the pelican static blog.

The username.github.io will be where the output pelican transformed .html is automatically pushed by Travis CI and is conveniently served by GitHub pages. <https://pages.github.com/>


Ensure <https://github.com/integrations/travis-ci> is authorized by clicking on the Configure button.

(You can review the OAuth apps with <https://github.com/settings/applications>)

While the Integration allows Travis CI to detect commits to your repositories it does not necessarily allow it to push changes into a repository, for that we'll use an OAuth Token.

Create a new personal oauth token: <https://github.com/settings/tokens/new>
> scope should be public repos only

*The long way is to use the GitHub WebUI -> Applications -> Personal Access Token -> public_repo (only)*

Make sure you store the personal access token in a password manager or somewhere safe (i.e. not in plaintext in your email or published on your website ;)


## Travis CI Setup

The beauty of these tightly integrated continuous integration systems is that when a commit is pushed into a specific github repo you can trigger some command execution, in this case to convert the markdown to html and then push it to a different repository. (The github pages special repository which is why it must be specifically username.github.io)

> I use **travis-ci.org** which is free for public repos, travis-ci.com is the paid professional service for private repositories

Register the repository and github personal access token in TravisCI ...

1. From the Travis Side also "Authorize Application" using https://travis-ci.org/profile/yourusername
2. Find the list of repositories (you may have to first click "sync now" to see the list)
3. Slide to ON (checkmark) for the source.username.github.io repository
4. Click on the gear symbol next to the name of the source.username.github.io repository (should result in the URL https://travis-ci.org/username/source.username.github.io/settings)
5. Scroll down to Environment Variables - oh but maybe this last step isn't necessary because it is in the YAML file (travis.yml

### Travis CLI with Docker to encrypt the OAuth Token

You do not want the unencrypted oauth token in your yaml file or even in the logs.  Instead leverage the handy feature of encrypted environment variables by encrypting your oauth token using the Travis CLI (ruby based so...)

> There is a special travis requirement of knowing the owner/repo , i.e. **username/source.username.github.io**

> The easy way
    docker run -it --rm ruby:alpine /bin/sh
    apk add --no-cache build-base
    gem install travis travis-lint

> The slightly longer way with Ubuntu
    docker run -it --rm ubuntu:trusty
    apt-get update
    apt-get install -y ruby1.9.3 build-essential
    sudo gem install travis travis-lint

The actual travis commands...

    travis help
    travis pubkey -r username/source.username.github.io
    travis encrypt GH_TOKEN=your_github_personal_oauth_token -r username/source.username.github.io

> Alternatively make a fake yaml file and get the exact output added by the command, `touch .travis.yml && travis encrypt GH_TOKEN=your_github_personal_oauth_token -r username/source.username.github.io --add env.global && less .travis.yml`

- <https://docs.travis-ci.com/user/environment-variables/#Defining-encrypted-variables-in-.travis.yml>
- <https://docs.travis-ci.com/user/encryption-keys#Fetching-the-public-key-for-your-repository>
- <https://github.com/travis-ci/travis.rb/issues/296>

#### .travis.yml

At the root of your source.username.github.io you'll need the Travis configuration file (yaml)

    language: python
    python:
        - "2.7"
    before_install:
     - sudo apt-get update -qq
    install:
        - pip install pelican==3.6.3 Markdown==2.6.7 beautifulsoup4==4.5.1
    script:
        - rm -rf ./output
        - rm -rf ./cache
        - rm -rf ./plugins/*
        - git clone https://github.com/getpelican/pelican-plugins.git
        - mv ./pelican-plugins/* ./plugins
        - pelican ./content -o ./output -s ./publishconf.py
        - git clone --quiet https://${GH_TOKEN}@github.com/johnpfeiffer/johnpfeiffer.github.io.git > /dev/null
        - cd johnpfeiffer.github.io
        - git config user.email "me@john-pfeiffer.com"
        - git config user.name "John Pfeiffer"
        - rsync -rv --exclude=.git ../output/* .
        - git add -f .
        - git commit -m "Travis build $TRAVIS_BUILD_NUMBER"
        - git push -fq origin master > /dev/null
        - echo -e "Done\n"
    env:
       global:
         secure: example126xOnLRCabGeZrxMUne9W0l5LTbN/hR5Wnq0P3nwrL4slWJ3rFAoi/wqivbINwZGOkU7e/OPVvjDCRivAIxeti61xtnKgyFL6rTvc7u5vAjCF6m4qx6+bXOx9YbXCEUdJmBd25qGBy3PIg4rt/524DOBZhZ9t4glt8Qo=
    
> - Use a python2.7 based travis builder with the pelican and its dependencies and the encrypted oauth token
> - Also helpful: <https://lint.travis-ci.org> (validate .travis.yml) or `gem install travis-lint`

The "target" repository is manually cloned using the encrypted oauth token, and the pelican output is then pushed to it.  No humans involved!

## Using a CNAME to have your own custom domain point to the GitHub Pages Pelican Blog

To ensure maximum coolness (and SEO points) make sure you have DNS control over the domain you have in mind so you can redirect it to your new static pelican-based blog (hosted for free by github pages).

1. Basically in the GitHub repo settings of source.username.github.io choose "Custom domain"
2. Then add a CNAME with your DNS provider (i.e. from Namecheap I pointed blog.john-pfeiffer.com to johnpfeiffer.github.io)

- <https://help.github.com/articles/using-a-custom-domain-with-github-pages/>
- <https://help.github.com/articles/adding-or-removing-a-custom-domain-for-your-github-pages-site/>
- <https://help.github.com/articles/setting-up-a-custom-subdomain/>



