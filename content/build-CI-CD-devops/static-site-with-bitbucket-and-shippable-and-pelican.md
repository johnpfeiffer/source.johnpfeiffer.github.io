Title: Static site with Bitbucket and Shippable and Pelican
Date: 2015-12-21 12:24
Tags: static site, pelican, bitbucket, shippable ci, ci, cd

[TOC]

## Running Software Costs Money

One of the most overlooked costs in running a service is operations.  While Research and Development (aka coding) is often cited as the largest expense (software developer salaries! <https://www.quora.com/What-are-the-average-operating-costs-of-SaaS-companies>), and 80% (or more) of (successful) software's life is maintenance (<http://www.ncbi.nlm.nih.gov/pmc/articles/PMC3610582/>), you have to run the darn thing all the time.

## A Free and Efficient Static Web Site
 
What is one cost effective (free!) and efficient solution to running a static site?

- Bitbucket also has a free static site capability (as long as the DNS is USERNAME.bitbucket.org), so no server/hosting required
- Bitbucket have free private repositories
- The Bitbucket static site repository can be private (only the html exposed will be visible to anonymous users)
- Shippable have a free plan with 1 container that will do your builds (fine by me, Docker is fast!)
- Pelican converts markdown into .html and you can still use javascript for fancy things <http://docs.getpelican.com/>

The basic process is to be triggered by a git push to the private repository of new/updated source markdown, use pelican to process it into .html, and then publish (git push) the new/updated .html to the static site repository.

One reason to use two seperate repositories instead of only one repository is that if you make a commit to your markdown source repository that will trigger a CI run which will push the updated .html files to the repository which would be detected and maybe trigger an infinite loop.  Or at the least interleave your source code changes with generated output changes in the commit logs.  =]

An alternative is using multiple branches but you'd better hope nobody ever deletes your source branch by accident.

Another alternative is to include an IF statement in your shippable code to not push if the diff/md5 of the source files (or maybe check against the output .html?) still match.  

> I say keep it super simple ;)


## Bitbucket setup

### Create The Source and Target Repositories

Create a new private repository (for your markdown), consider prefixing the name with source or something (good names makes for good maintenance)

Make sure you have cloned the pelican project and setup a basic static site: <http://blog.john-pfeiffer.com/how-to-set-up-a-pelican-static-blog-site/>

Inside your .gitignore you will probably want to exclude .pyc and ./output and any other pelican created artifacts.

Inside your repository at the root level you will need a shippable.yaml file:

    language: python
    python:
        - "2.7"
    install:
        - pip install pelican Markdown beautifulsoup4
    script:
        - rm -rf ./output
        - rm -rf ./cache
        - rm -rf ./plugins/*
        - mv ./pelican-project/* .
        - ls -ahl ./content
        - pelican ./content -o ./output -s ./publishconf.py
    after_script:
        - ls -ahl
        - ls -ahl ./output
    
> This assumes that the pelican-project is a subdirectory in the repository using the best practice of leaving the top level of a repository for build and test artifacts and isolating the source code into a subdirectory.

Create another private repository for your public html.  It MUST be named USERNAME.bitbucket.org to make use of the bitbucket static site capabilities.

> (yes, the name must include those dots/domain name of the service)

<https://confluence.atlassian.com/bitbucket/publishing-a-website-on-bitbucket-cloud-221449776.html>

### Get OAuth Access

Generate a Consumer OAuth2 Token with <https://confluence.atlassian.com/bitbucket/oauth-on-bitbucket-cloud-238027431.html#OAuthonBitbucketCloud-Createaconsumer>

Use curl to verify your token (this is how Shippable will get a 1 hour expiring access token to work on the target output repository)

    curl https://bitbucket.org/site/oauth2/access_token -d grant_type=client_credentials -u yourkeyhere:yoursecrethere

<http://stackoverflow.com/questions/24965307/how-to-manipulate-bitbucket-repository-with-token>

## Shippable setup

Enable the integration with Bitbucket: <http://docs.shippable.com/#step-0-prerequisite>

*Right from the beginning Shippable tries to ask which source repository provider (either GitHub or Bitbucket) you will be using.*

Use Shippable's OAuth implementation (Account Integration) to pick which Bitbucket repository

Home -> CI (dropdown) -> Bitbucket (hopefully you have a different avatar between Bitbucket and GitHub)
    
> Press "Sync" if you have a newly created repository that is not listed yet

Add the Bitbucket OAuth2 Key and Secret as a Shippable secure environment variable in the format KEY:SECRET

> Go to https://app.shippable.com/projects/1234d2ea1895ca4474661234/settings and look for the Encrypt section
> Fill it in with something like OAUTH_USER=yourkeyhere:yoursecrethere

<http://shippable-docs-20.readthedocs.org/en/latest/config.html#secure-environment-variables>

Copy the output to your shippable.yml file

## Putting it all together

Update the source repository top level shippable.yaml file:

    language: python
    python:
        - "2.7"
    install:
        - pip install pelican Markdown beautifulsoup4
    env:
        - secure: yourencryptedkeyandsecret==
    script:
        - rm -f token.json
        - rm -rf ./output
        - rm -rf ./cache
        - rm -rf ./plugins/*
        - mv ./pelican-project/* .
        - ls -ahl
        - ls -ahl ./content
        - pelican ./content -o ./output -s ./publishconf.py
        - ls -ahl ./output
        - curl https://bitbucket.org/site/oauth2/access_token -d grant_type=client_credentials -u $OAUTH_USER >> token.json
        - BBTOKEN=$(cat token.json | python -c 'import sys, json; print json.load(sys.stdin)["access_token"]')
        - git clone "https://x-token-auth:$BBTOKEN==@bitbucket.org/USERNAME/USERNAME.bitbucket.org"
        - ls -ahl USERNAME.bitbucket.org/
        - rm -rf USERNAME.bitbucket.org/*
        - cd USERNAME.bitbucket.org
        - mv ../output/* .
        - ls -ahl .
        - git config user.email "me@example.com"
        - git config user.name "John Pfeiffer"
        - git add -f .
        - git commit -m "build $BUILD_NUMBER commit $COMMIT"
        - git push -fq origin master > /dev/null
        - rm -f ../token.json
    after_script:
        - ls -ahl
    
> - Adding the bitbucket oauth2 consumer key and secret (separated by a colon) as an encrypted environment variable
> - using curl to generate a temporary access_token and extracting it into a local environment variable
> - cloning with the access)token and removing the previous contents and replacing them with the newly generated output
> - leveraging the CI variables to indicate on the output html repository what markdown source commits triggered this build

## Reviewing the output

The full output of the run is available at something like https://app.shippable.com/builds/1234dec1d00e020c0011234

This is really helpful for debugging (especially seeing how many seconds each step took)

Possible improvements:

1. use a python application best practice of documenting dependencies with a requirements.txt file at the top level
1. putting all of the commands into a script like publish-in-ci.sh so that it could be run locally in a dev environment
1. add the Dockerfile used for local development into the source repository to consolidate and simplify development in one place


## Misc

One thing that is interesting about this is that using OAuth tokens through a service is merely wrapping all of the manual steps I have in a previous blog post into a nice SaaS wrapper =)
<http://blog.john-pfeiffer.com/publish-a-pelican-blog-using-a-bitbucket-post-webhook/>

