Title: Using CircleCI as continuous integration and continuous deployment
Date: 2021-04-14 20:43
Tags: ci, circleci, continuous integration, continuous deployment, github, golang, go, go mod

[TOC]

I avoid providing free advertising for products but often end up writing about how I have leveraged free products. =]

I have many posts over the years using vmware, openshift, heroku, google app engine, aws elastic beanstalk, ec2, aws lambdas, github, bitbucket, bitbucket pipelines, docker, digital ocean, and many more things. *(all lowercase ;)*

I wanted to document how I successfully migrated some of my other hobby projects to CircleCI so future me (and anyone else) can more easily replicate the steps because CircleCI has a free tier for CI/CD (continuous integration and continuous deployment).

I make no guarantee that CircleCI will continue to be free in the future (but if stops being free I will likely write another blog post about how to use a different service ;)

## Why I chose CircleCI

1. Free (even more free for open source projects)
2. Straightforward documentation with good examples
3. Integrated with github (and bitbucket)
4. It just works (relatively quick execution and feedback loop)

### CircleCI Build Terminology

- A **Project** maps to a code repository
- You configure each Project to do certain things when a new commit occurs.
- A **pipeline** are all the things that happen when your Project is triggered (i.e. new code or manual re-run).
- A **workflow** is the definition (and execution) of all the jobs in a pipeline; note that jobs can run in parallel.
- A **job** is a collection of steps that are going to happen (i.e. checkout code and run a command)
- A job must have an execution environment (i.e. a docker container)
- A **step** is doing a single thing (i.e. checkout code)
- <https://circleci.com/docs/2.0/concepts/?section=getting-started>

## Getting Started by Authorizing CircleCI

Start with the source code: setup a repository (i.e. in github) , e.g. <https://github.com/johnpfeiffer/stringsmoar>

Go to CircleCI's login page and choose to "Sign Up" <https://circleci.com/signup/>

_For the paranoid like me you can choose to only share your public github repos_

Once you use the oauth-like permissions screen that provides your username and password to Github so it can authorize CircleCI to access all of your bits.

This is the one time you "authorize all the access", everything afterwards are config files that are fine to be in public code repos.

> In Github you can review what applications have access to your github account's source code with <https://github.com/settings/applications>
> **"Authorized Oauth Apps"**

In CircleCI you can now see what projects you can setup builds, apparently segregated by "organization" <https://app.circleci.com/projects/>

## Setup a Project

Not too surprisingly the UI then displays a list of all of the repos <https://app.circleci.com/projects/project-dashboard/github/johnpfeiffer/>

_"Set Up Project" makes sense but for some odd reason the terminology is to "follow a project" when something has been configured by someone else in your organization_

The UI will attempt to helpfully suggest a configuration yaml based on auto-detecting the repository's programming language.

_For Golang CircleCI presumes you are using **go mod** so I guess I ought to upgrade my old code repos now that there's an official standard_

If you choose the pre-generated configuration file CircleCI will attempt to commit and push that new .circleci/config.yml into your repo and then start a Build.

Instead of the auto-generated configuration you can select **Use Existing Config** (in which case you should have already uploaded into github remote your preferred CircleCI reference)...

**your-repo/.circleci/config.yml**

    :::yaml
    version: 2.1 # https://circleci.com/docs/2.0/configuration-reference
    jobs:
      resource_class: small
      build:
        working_directory: ~/repo # the circleCI default for where code is checked out to in the docker build container
      docker:
        - image: circleci/golang:1.16 # https://hub.docker.com/r/circleci/golang/ , https://hub.docker.com/_/golang?tab=description
      steps:
        - checkout
        - run:
            name: Run unit tests
            command: |
              go test -v ./...

### Double checking your Golang Version

The wonderful thing about Docker is the extra transparency. In this case we might want to double check the version of Golang that is being used by the build agent.

You can download and execute the same environment locally:

`docker run --rm -it circleci/golang:1.16`
`go version`
> go version go1.16.3 linux/amd64

- <https://hub.docker.com/r/circleci/golang/>

### Cannot find main module is a common error for older golang code repos

> go: cannot find main module

This means you have created a golang repo awhile back *(Golang 1.15 and older)* but are now using a later Golang binary...

To resolve the issue run this golang command in the top directory of your source code:

`go mod init`

This will create a **go.mod** file in your repository that allows dependencies to be properly resolved (and `go test` which implicitly uses "go mod" to execute successfully)

Once that go.mod is committed and sent up to the github repo then CircleCI build will detect it and your go test during the build/test steps will stop failing

- <https://golang.org/ref/mod#mod-commands>

## Tweaks to your CircleCI Config

After you have successfully run a build then the UI will show you:
- how long the build took
- what git sha commit kicked off the build
- commit message
- all the steps executed and output, etc.

<https://app.circleci.com/pipelines/github/johnpfeiffer/stringsmoar/7/workflows/39b3f880-2473-49d7-804d-d1364f08853e/jobs/9>


### Rerun a build in CircleCI

Sometimes it can take a bit to get used to the CircleCI UI, to drill down to a specific build your "breadcrumbs" will look like:

`All Pipelines > your-projectname > branch (main) > workflow > build (4)`

In that detailed output UI, to Rerun a build, choose the "Rerun" button from the beginning (or from a failed step)

_Flaky tests aka intermittent failures is not resolved by re-running your build/tests all the time ;p_

### Specific Project Settings in CircleCI

In a given Project, the three little dots will allow you to choose how to configure the project

<https://app.circleci.com/settings/project/github/johnpfeiffer/stringsmoar>

The one annoying thing is that if you remove your 3rd party access creds in GitHub it's a pain to reconnect CircleCI

In CircleCI project configuration you should see a listing of SSH keys, you have to remove the old one there, unfollow the project, and then re-follow the project.

Afterward you should see a new SSH key that CircleCI created in Github for this Project (the UI's both show the sha of the key but one is sha256 and the other is not)

- <https://github.com/johnpfeiffer/stringsmoar/settings/keys>
- <https://discuss.circleci.com/t/solved-permission-denied-publickey/19562> (someone had the same problem as me)

### Picking the size of your build executor

By default CircleCI will choose "medium", if you want to save (free) credits then for smaller projects use

    :::yaml
    jobs:
      build:
        resource_class: small
        docker:
          - image: circleci/golang:1.16

> Good news is that builds usually trigger almost instantly so all the tweaks have a super fast feedback loop

- <https://circleci.com/docs/2.0/executor-types/#available-docker-resource-classes>
- <https://circleci.com/docs/2.0/getting-started/?section=getting-started>

## Outputting Test Coverage and Artifacts

CircleCI has an extra space in the UI to display specific test output or artifacts whichmakes it easy to see the most common pain points rather than digging through all of the build stages output.

**your-repo/.circleci/config.yml**

    :::yaml
    version: 2.1 # https://circleci.com/docs/2.0/configuration-reference
    jobs:
      resource_class: small
      build:
        working_directory: ~/repo # this is a circleCI default for where code is checked out to in the docker build container
      docker:
        - image: circleci/golang:1.16 # https://hub.docker.com/r/circleci/golang/ , https://hub.docker.com/_/golang?tab=description
    
      environment:
        TEST_RESULTS: /tmp/test-results
    
      steps:
        - checkout
        - run: mkdir -p $TEST_RESULTS
        - run:
            name: Run unit tests
            command: |
              go test -v ./...
        - run:
            name: Run code coverage
            command: |
              go test -coverprofile=c.out
              go tool cover -html=c.out -o coverage.html
              mv coverage.html $TEST_RESULTS
              go test -v ./... | go tool test2json > $TEST_RESULTS/test2json-output.json
              gotestsum --junitfile $TEST_RESULTS/gotestsum-report.xml
    
        - store_artifacts: # Upload test summary for display https://circleci.com/docs/2.0/artifacts/
            path: /tmp/test-results
            destination: raw-test-output
        - store_test_results: # Upload test results for display https://circleci.com/docs/2.0/collect-test-data/
            path: /tmp/test-results


Artifacts will be deleted after 30 days but would be output like this: <https://12-123862890-gh.circle-artifacts.com/0/raw-test-output/coverage.html#file0>

> The golang coverage.html as an artifact can be opened by your web browser and highlight in color specifically which code paths are covered by unit tests

- <https://blog.golang.org/cover>
- <https://circleci.com/docs/2.0/artifacts/>
- <https://circleci.com/docs/2.0/language-go/>
- <https://blog.john-pfeiffer.com/golang-testing-benchmark-profiling-subtests-fuzz-testing/>


_the CircleCI golang docker container has the opensource helper "gotestsum" to generate junit style XML output from tests_
> JUnit XML or Cucumber JSON test metadata files


From here on out you should hopefully have only Green Builds!

TODO: an article about how to do continuous deployment _(maybe CDK and AWS?)_
