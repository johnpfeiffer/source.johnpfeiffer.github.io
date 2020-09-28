Title: Localstack APIGateway Lambda and S3 integration testing
Date: 2020-03-05 21:10
Tags: go, golang, localstack, aws, testing, lambda, apigateway, s3, integration testing, docker-compose

[TOC]

One of the challenges with "serverless" is how to develop locally, especially things like running integration tests in your dev environment.

Imagine writing code for a lambda that reads and writes from S3, but without any AWS.

The AWS tool SAM does have a local mode but does not cover S3 nor Dynamo, etc.

A great tool to fill this need is Localstack.  Since its interfaces are compatible with AWS it is an excellent proxy.

_Mirroring environments of Development, Staging, and Production, along with Integration or Acceptance tests, are best practices that allow you to write code with confidence and catch issues much earlier (and therefore more cheaply) than "Using your Users as QA in Production"_

## Prerequisites

Background: my previous article about writing a lambda with Golang and deploying it to AWS.

- <https://blog.john-pfeiffer.com/go-faas-with-aws-lambda/>

### Install and configure the AWS CLI

In order to interact with Localstack we will use the AWS CLI, welcome to the beauty of Interfaces (API driven development ;)

`sudo apt install awscli` _or for all the alternate installation options <https://aws.amazon.com/cli/>_

Setup fake credentials...

**this will overwrite any existing ~/.aws/ config or credentials**

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

`mkdir task; cd task; vim task.go`
> creates a directory/package and file with the same name to be the lambda code

    :::go
    package main
    
    import (
    	"fmt"
    	"github.com/aws/aws-lambda-go/lambda"
    )
    
    // MyEvent is a thing
    type MyEvent struct {
    	Name string `json:"name"`
    }
    
    // HandleRequest for an event
    func HandleRequest(name MyEvent) (string, error) {
    	return fmt.Sprintf("hi %s", name.Name), nil
    }
    
    func main() {
    	lambda.Start(HandleRequest)
    }

`go build`
> outputs a binary file "task", if on MacOS you may want to cross compile with: `GOOS=linux go build`

`zip task.zip task`
> lambda code uploads must be zipped in advance

### Create-Function aka Upload the golang code to the localstack lambda

`aws --endpoint-url=http://localhost:4574 lambda create-function --function-name=task --runtime="go1.x" --role=fakerole --handler=task --zip-file fileb://task.zip`

> localstack_1  | 2020-03-06T05:09:38:DEBUG:localstack.utils.common: Starting download from http://a46a9ed6f485:4574/2015-03-31/functions/task/code to /tmp/tmpfile.6f1d50ce9ccf62f3094d3c7f9eb82573/archive.zip (5060419 bytes)

> localstack_1  | 2020-03-06T05:09:38:DEBUG:localstack.utils.common: Writing 1048576 bytes (total 1048576) to /tmp/tmpfile.6f1d50ce9ccf62f3094d3c7f9eb82573/archive.zip

> localstack_1  | 2020-03-06T05:09:38:DEBUG:localstack.utils.common: Done downloading http://a46a9ed6f485:4574/2015-03-31/functions/task/code, response code 200, total bytes 5060419

<https://docs.aws.amazon.com/cli/latest/reference/lambda/create-function.html>
> Note that we used a fake role name "fakerole", localstack does not enforce IAM roles or permissions

### Get the dependency docker container that actually executes Golang

`docker pull lambci/lambda:go1.x`

**Now you can invoke the Lambda with an input...**

`aws lambda --endpoint-url=http://localhost:4574 invoke --function-name task --payload='{"Name": "world"}' --region=us-east-1 myout.log`

> {    "StatusCode": 200    }

> localstack_1  | 2020-03-06T05:45:22:DEBUG:localstack.services.awslambda.lambda_executors: Lambda arn:aws:lambda:us-east-1:000000000000:function:task result / log output:
> "hi world"


### Other useful commands for updating or deleting your localstack lambda
`aws --endpoint-url=http://localhost:4574 lambda list-functions`

`aws --endpoint-url=http://localhost:4574 lambda update-function-code --function-name=task --zip-file fileb://task.zip`
`aws --endpoint-url=http://localhost:4574 lambda delete-function --function-name task`

- - -
## API Gateway and Lambda with Localstack

A very simple bit of "handler" code to exemplify the AWS Lambda Proxy Integration

    :::go
    package main
    
    import (
    	"context"
    	"fmt"
    	"net/http"
    
    	"github.com/aws/aws-lambda-go/events"
    	"github.com/aws/aws-lambda-go/lambda"
    )
    
    // HandleRequest for an event https://docs.aws.amazon.com/lambda/latest/dg/golang-handler.html
    // input object defined here https://godoc.org/github.com/aws/aws-lambda-go/events#APIGatewayProxyRequest
    func HandleRequest(ctx context.Context, req events.APIGatewayProxyRequest) (events.APIGatewayProxyResponse, error) {
    	fmt.Printf("DEBUG: %#v", req)
    
    	// https://docs.aws.amazon.com/apigateway/latest/developerguide/set-up-lambda-proxy-integrations.html#api-gateway-simple-proxy-for-lambda-output-format
    	return events.APIGatewayProxyResponse{
    		StatusCode: http.StatusOK,
    		Body: req.Body,
    	}, nil
    }
    
    func main() {
    	lambda.Start(HandleRequest)
    }

<https://docs.aws.amazon.com/lambda/latest/dg/golang-handler.html>

> How to parse the inputs provided to the Lambda by the AWS API Gateway
<https://docs.aws.amazon.com/apigateway/latest/developerguide/set-up-lambda-proxy-integrations.html#api-gateway-simple-proxy-for-lambda-input-format>


> Output for a (Proxy Integration) Lambda with APIGateway needs a specific JSON format
<https://docs.aws.amazon.com/apigateway/latest/developerguide/set-up-lambda-proxy-integrations.html#api-gateway-simple-proxy-for-lambda-output-format>
> The custom reponse headers are where CORS can be configured

`GOOS=linux go build && zip task.zip task`

`aws --endpoint-url=http://localhost:4574 lambda update-function-code --function-name=task --zip-file fileb://task.zip`
`aws --endpoint-url=http://localhost:4574 lambda list-functions`
> arn:aws:lambda:us-east-1:000000000000:function:task


**Again invoke the Lambda, with an input...**
`aws lambda --endpoint-url=http://localhost:4574 invoke --function-name task --payload='{"body": "foobar"}' --region=us-east-1 myout.log`
> {"StatusCode": 200}

- - -
`aws --endpoint-url=http://localhost:4567 apigateway create-rest-api --name myapi`

    :::json
    {
        "createdDate": 1583558847,
        "apiKeySource": "HEADER",
        "tags": {},
        "name": "myapi",
        "endpointConfiguration": {
            "types": [
                "EDGE"
            ]
        },
        "id": "29a3p9encp"
    }

> That "id" of this REST API is important throughout the rest of the commands

`aws --endpoint-url=http://localhost:4567 apigateway get-resources --rest-api-id 29a3p9encp`

    :::json
    {
        "items": [
            {
                "id": "62wy7bzofu",
                "resourceMethods": {
                    "GET": {}
                },
                "path": "/"
            }
        ]
    }
> The "id" for the "/" resource is used as the "parent" for adding a "child" resource

`aws --endpoint-url=http://localhost:4567 apigateway create-resource --rest-api-id 29a3p9encp --parent-id 62wy7bzofu --path-part mywidget`

    :::json
    {
        "pathPart": "mywidget",
        "resourceMethods": {
            "GET": {}
        },
        "id": "jylycd8v4u",
        "parentId": "62wy7bzofu",
        "path": "/mywidget"
    }
> We have created a REST resource /mywidget

`aws --endpoint-url=http://localhost:4567 apigateway put-method --rest-api-id 29a3p9encp --resource-id jylycd8v4u --http-method GET --authorization-type NONE`

    :::json
    {
        "authorizationType": "NONE",
        "httpMethod": "GET"
    }
> Now /mywidget does not require any authentication for GET requests


`aws --endpoint-url=http://localhost:4567 apigateway put-integration --rest-api-id 29a3p9encp --resource-id jylycd8v4u --http-method GET --integration-http-method POST --type AWS_PROXY --uri arn:aws:apigateway:us-east-1:lambda:path/2015-03-31/functions/arn:aws:lambda:us-east-1:000000000000:function:task/invocations --passthrough-behavior WHEN_NO_MATCH`

    :::json
    {
        "type": "AWS_PROXY",
        "httpMethod": "POST",
        "uri": "arn:aws:apigateway:us-east-1:lambda:path/2015-03-31/functions/arn:aws:lambda:us-east-1:000000000000:function:task/invocations",
        "integrationResponses": {
            "200": {
                "statusCode": 200,
                "responseTemplates": {
                    "application/json": null
                }
            }
        }
    }
> This connects the AWS API Gateway GET /mywidget calls as a "proxy" (passing through the request) to the specified Lambda
> POST is required <https://docs.aws.amazon.com/lambda/latest/dg/API_Invoke.html>

aws --endpoint-url=http://localhost:4567 apigateway create-deployment --rest-api-id 29a3p9encp --stage-name foobar

    :::json
    {
        "createdDate": 1583565386,
        "description": "",
        "id": "mbe3fwe0pw"
    }
> This actually activates the endpoint for traffic


- - -
List everything that we have created...

`aws --endpoint-url=http://localhost:4567 apigateway get-resources --rest-api-id 29a3p9encp`

    :::json
    {
        "items": [
            {
                "resourceMethods": {
                    "GET": {}
                },
                "path": "/",
                "id": "62wy7bzofu"
            },
            {
                "resourceMethods": {
                    "GET": {
                        "methodIntegration": {
                            "uri": "arn:aws:apigateway:us-east-1:lambda:path/2015-03-31/functions/arn:aws:lambda:us-east-1:000000000000:function:task/invocations",
                            "type": "AWS_PROXY",
                            "httpMethod": "POST",
                            "integrationResponses": {
                                "200": {
                                    "responseTemplates": {
                                        "application/json": null
                                    },
                                    "statusCode": 200
                                }
                            }
                        },
                        "httpMethod": "GET",
                        "authorizationType": "NONE"
                    }
                },
                "parentId": "62wy7bzofu",
                "id": "jylycd8v4u",
                "path": "/mywidget",
                "pathPart": "mywidget"
            }
        ]
    }
> The fully configured API Gateway and /mywidget resource linked to the Lambda code

<https://docs.aws.amazon.com/cli/latest/reference/apigateway/test-invoke-method.html>
` aws apigateway test-invoke-method --endpoint-url=http://localhost:4567 --rest-api-id 29a3p9encp --resource-id jylycd8v4u --http-method GET`

- - -

`curl http://localhost:4567/restapis/29a3p9encp/`

    :::json
    {"id": "29a3p9encp", "name": "myapi", "description": null, "createdDate": 1583565481, 
        "apiKeySource": "HEADER", "endpointConfiguration": {"types": ["EDGE"]}, "tags": {}
    }


`curl -i http://localhost:4567/restapis/29a3p9encp/foobar/`

`curl -i http://localhost:4567/restapis/29a3p9encp/foobar/_user_request_/mywidget`


- - -


Alternatively, HTTP_PROXY means you have to point it to a URI like https://example.com/my-existing-server


- <https://docs.aws.amazon.com/cli/latest/reference/apigateway/create-rest-api.html>
- <https://docs.aws.amazon.com/cli/latest/reference/apigateway/create-resource.html>
- <https://docs.aws.amazon.com/cli/latest/reference/apigateway/put-method.html>
- <https://docs.aws.amazon.com/cli/latest/reference/apigateway/put-integration.html>
- <https://docs.aws.amazon.com/cli/latest/reference/apigateway/create-deployment.html>

- <https://docs.aws.amazon.com/apigateway/latest/developerguide/how-to-create-api.html>
- <https://docs.aws.amazon.com/apigateway/latest/developerguide/api-gateway-create-api-as-simple-proxy-for-lambda.html>
- <https://docs.aws.amazon.com/apigateway/latest/developerguide/set-up-lambda-proxy-integrations.html#api-gateway-simple-proxy-for-lambda-input-format>


- - -
TODO: YAML with APIGateway + Lambda + S3
- Go code for Request Event and write to S3
- curl example integration test

Thanks to:

- <https://github.com/localstack/localstack/issues/561>
- <https://www.alexedwards.net/blog/serverless-api-with-go-and-aws-lambda>
