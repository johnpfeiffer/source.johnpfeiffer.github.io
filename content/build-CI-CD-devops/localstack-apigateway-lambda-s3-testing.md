Title: Localstack APIGateway Lambda and S3 integration testing
Date: 2020-03-05 21:10
Tags: go, golang, localstack, aws, testing, lambda, apigateway, s3, integration testing, docker-compose

[TOC]

One of the challenges with serverless is how to run integration tests in your dev environment, especially if you want to use a local development environment.

The AWS tool SAM does have a local mode but does not cover S3 nor Dynamo, etc.

A great tool to fill this need is Localstack.

_Mirroring environments of Development, Staging, and Production, along with Integration or Acceptance tests, are best practices that allow you to write code with confidence and catch issues much earlier (and therefore more cheaply) than "Using your Users as QA in Production"_

## Prerequisites

Background: my previous article about using AWS Lambdas with Golang

- <https://blog.john-pfeiffer.com/go-faas-with-aws-lambda/>

### Install and configure the AWS CLI

`sudo apt install awscli`
_or for all the alternate installation options <https://aws.amazon.com/cli/>_

Setup fake credentials...

    :::bash
    echo -e "[default]\n\
    region=us-east-1\n\
    output=json" > ~/.aws/config
    
    echo -e "[default]\n\
    aws_access_key_id=AKIAFAKE\n\
    aws_secret_access_key=FAKE" > ~/.aws/credentials

<https://docs.aws.amazon.com/cli/latest/userguide/cli-configure-files.html>


## Simplest Localstack Lambda Configuration

    :::yaml
    version: "3"
    
    services:
      localstack:
        image: "localstack/localstack"
        ports:
          - "4574:4574" # lambda
        environment:
          - SERVICES=lambda
          - LAMBDA_EXECUTOR=docker
          - DOCKER_HOST=unix:///var/run/docker.sock
          - DEBUG=1
        volumes:
          - "/var/run/docker.sock:/var/run/docker.sock"

`sudo docker-compose up`
> Creating task_localstack_1 ... done
> Attaching to task_localstack_1
> localstack_1  | Waiting for all LocalStack services to be ready
> localstack_1  | Starting mock Lambda service (http port 4574)...

<https://github.com/localstack/localstack>

## A very simple Go Lambda

`mkdir task`
`cd task`
`vim task.go`

    :::go
    package main
    
    import (
    	"context"
    	"fmt"
    
    	"github.com/aws/aws-lambda-go/lambda"
    )
    
    // MyEvent is a thing
    type MyEvent struct {
    	Name string `json:"name"`
    }
    
    // HandleRequest yes
    func HandleRequest(ctx context.Context, name MyEvent) (string, error) {
    	return fmt.Sprintf("hi %s", name.Name), nil
    }
    
    func main() {
    	lambda.Start(HandleRequest)
    }

`go build`
> outputs a binary file "task", if on MacOS you may want to cross compile with: `GOOS=linux go build`

`zip task.zip task`

### Create-Function aka Upload the golang code to the localstack lambda

`aws --endpoint-url=http://localhost:4574 lambda create-function --function-name=task --runtime="go1.x" --role=r1 --handler=task --zip-file fileb://task.zip`

> localstack_1  | 2020-03-06T05:09:38:DEBUG:localstack.utils.common: Starting download from http://a46a9ed6f485:4574/2015-03-31/functions/task/code to /tmp/tmpfile.6f1d50ce9ccf62f3094d3c7f9eb82573/archive.zip (5060419 bytes)
> localstack_1  | 2020-03-06T05:09:38:DEBUG:localstack.utils.common: Writing 1048576 bytes (total 1048576) to /tmp/tmpfile.6f1d50ce9ccf62f3094d3c7f9eb82573/archive.zip
> localstack_1  | 2020-03-06T05:09:38:DEBUG:localstack.utils.common: Done downloading http://a46a9ed6f485:4574/2015-03-31/functions/task/code, response code 200, total bytes 5060419


### Get the dependency docker container that actually executes Golang

`docker pull lambci/lambda:go1.x`

**Now you can invoke the Lambda with an input...**
`aws lambda --endpoint-url=http://localhost:4574 invoke --function-name task --payload='{"Name": "world"}' --region=us-east-1 myout.log`

> {    "StatusCode": 200    }

> localstack_1  | 2020-03-06T05:45:22:DEBUG:localstack.services.awslambda.lambda_executors: Lambda arn:aws:lambda:us-east-1:000000000000:function:task result / log output:
> "hi world"


### Other useful commands for updating or deleting your localstack lambda
`aws --endpoint-url=http://localhost:4574 lambda update-function-code --function-name=task --zip-file fileb://task.zip`
`aws --endpoint-url=http://localhost:4574 lambda delete-function --function-name task`

- - -
TODO: YAML with APIGateway + Lambda

- Go code for Request Event
- curl example integration test

TODO: YAML with APIGateway + Lambda + S3
- Go code for Request Event and write to S3
- curl example integration test

Thanks to open source: <https://github.com/localstack/localstack/issues/561>
