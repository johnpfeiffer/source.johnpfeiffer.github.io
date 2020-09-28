Title: Using AWS CDK to configure deploy a Golang Lambda with APIGateway
Date: 2020-09-27 14:48
Tags: go, golang, aws, lambda, apigateway, cdk

[TOC]

Infrastructure as Code helps guarantee the elusive determinism we all seek in building applications and services.

AWS have brought their own specific product out which competes with the venerable Terraform and nicely focused Serverless.

_All of these products use the json syntax of CloudFormation which is the foundational AWS syntax for describing resources_

It is straightforward to iteratively setup and use AWS CDK (with the native Typescript syntax).

_TODO: later add a quick CDK vocabulary guide_

## Install the AWS CDK Tool

Have to use npm to install the cdk tool...

`npm install -g aws-cdk`

## Setup the project directories
`mkdir cdk-example`

`cd cdk-example`

Create a subdirectory to compartmentalize all the infrastructure code (from the rest of the application)

`mkdir infra`

`cd infra`

`cdk init app --language typescript`

`cdk ls`
>        InfraStack

> Names are hard but whatever you pick, like **"Infra"**, will then show up in the AWS resources everywhere related to this project

## Install the dependencies for AWS resources that CDK will manage

Option 1: manually install dependencies _(it will automatically insert this into package.json)_

`npm install @aws-cdk/aws-s3 @aws-cdk/aws-lambda`

Option 2: write the lines into packages.json and run at the command line in the infra directory: `npm install`
> Writing files first (and ensuring they are in version control) is a more IaaC pattern

    :::json
    "dependencies": {
      "@aws-cdk/aws-s3": "*",
      "@aws-cdk/core": "*",
      "source-map-support": "^0.5.16"
    }


## Write the actual Infrastructure Code
The initial application template creates an empty "class" that represents the "stack"
_A stack is the group of resources together_

**lib/infra-stack.ts** has only 2 changes to the default file, the import of S3 and the new Bucket resource "MyExampleBucket"

    :::typescript
    import * as cdk from '@aws-cdk/core';
    import * as s3 from '@aws-cdk/aws-s3';
    
    export class InfraStack extends cdk.Stack {
      constructor(scope: cdk.Construct, id: string, props?: cdk.StackProps) {
        super(scope, id, props);
    
        new s3.Bucket(this, 'MyExampleBucket', {
          versioned: true
        });
      }
    }

> The import renames are important to be consistent in subsequent code, so if something is "cdk" then it is cdk.Construct

### Output CloudFormation from a CDK Typescript file

`cdk synth`
> this command will output to the display the CloudFormation that will be sent/used by AWS

    :::yaml
    Resources:
      MyExampleBucket8D68EFCA:
        Type: AWS::S3::Bucket
        Properties:
          VersioningConfiguration:
            Status: Enabled
        UpdateReplacePolicy: Retain
        DeletionPolicy: Retain
        Metadata:
          aws:cdk:path: InfraStack/MyExampleBucket/Resource
      CDKMetadata:
        Type: AWS::CDK::Metadata
        Properties:
    

To preview what will occur between changes to the .ts file...

`cdk diff`

## Deploy resources that CDK has defined

`cdk deploy`
> warning, really making a change in AWS (based on your creds)

    :::bash
    InfraStack
    
    InfraStack: deploying...
    InfraStack: creating CloudFormation changeset...
    (3/3)
    
    Stack ARN:
    arn:aws:cloudformation:us-east-1:409670809604:stack/InfraStack/b5167030-00fb-11eb-9f36-12f8925a37c4
    

### Verify the new bucket was created

`aws s3 ls | grep MyExampleBucket`

_this assumes you have installed the AWS CLI like `sudo apt install awscli`_

`aws cloudformation list-stacks | grep InfraStack`
> this listing will also show deleted Stacks


## Making updates with CDK

A tiny snippet change to allow bucket deletion...

- <https://docs.aws.amazon.com/cdk/latest/guide/hello_world.html>
- <https://docs.aws.amazon.com/cdk/api/latest/typescript/api/aws-s3.html>
- <https://docs.aws.amazon.com/cdk/api/latest/typescript/api/aws-s3/bucketpolicyprops.html#aws_s3_BucketPolicyProps>
- <https://docs.aws.amazon.com/cdk/api/latest/typescript/api/core/removalpolicy.html#core_RemovalPolicy>

    :::typescript
    new s3.Bucket(this, 'MyExampleBucket', {
      versioned: true,
          removalPolicy: cdk.RemovalPolicy.DESTROY
    });

### Preview changes with diff
`cdk diff`

    :::bash
    Stack InfraStack
    Resources
    [~] AWS::S3::Bucket JohnPBucket JohnPBucket8D68EFCA
     ├─ [~] DeletionPolicy
     │   ├─ [-] Retain
     │   └─ [+] Delete
     └─ [~] UpdateReplacePolicy
         ├─ [-] Retain
         └─ [+] Delete

### Apply the new changes
`cdk deploy`

    :::bash
    InfraStack: deploying...
    InfraStack: creating CloudFormation changeset...

`cdk destroy`

`aws s3 ls | grep MyExampleBucket`

`aws cloudformation list-stacks | grep InfraStack`


CDK enables "InfrastructureAsCode" and command line (or scripted) resource management, yet you must still understand the intricacies of the domain (i.e. that s3 buckets have policies and do not get destroyed by default)

> s3 buckets are designed by default to not delete with a Stack, you must change the removal policy to do so

- - -

## APIGateway plus Lambda plus Go


### A tiny Go Web Request Handler
Put a simple placeholder Golang Lambda in place _using the Gin web framework for convenience_

`mkdir cdk-example/examplefunction/ ; cd cdk-example/examplefunction/`

`vim main.go`

    :::golang
    package main
    
    import (
            "context"
            "log"
    
            "github.com/aws/aws-lambda-go/events"
            "github.com/aws/aws-lambda-go/lambda"
            "github.com/awslabs/aws-lambda-go-api-proxy/gin"
            "github.com/gin-gonic/gin"
    )
    
    var ginLambda *ginadapter.GinLambda

    // for convenience leverage the Go init startup concept to define a global web server object
    func init() {
            // stdout and stderr are sent to AWS CloudWatch Logs
            log.Printf("Gin starting")
            r := gin.Default()
            r.GET("/ping", func(c *gin.Context) {
                    c.JSON(200, gin.H{
                            "message": "pong",
                    })
            })
            ginLambda = ginadapter.New(r)
    }
    

    // Handler is the function that executes for every Request passed into the Lambda
    func Handler(ctx context.Context, req events.APIGatewayProxyRequest) (events.APIGatewayProxyResponse, error) {
            return ginLambda.ProxyWithContext(ctx, req)
    }
    
    func main() {
            lambda.Start(Handler)
    }


`go mod init`
> Ensure dependencies (like the AWS SDK) are recognized by the Go package manager

`go test`
> This is the simplest way to trigger downloading the dependencies (imported packages)

<https://blog.golang.org/using-go-modules>


`GOOS=linux GOARCH=amd64 go build -o main main.go`
> compile for the target arch , AWS Lambda ("firecracker") is Linux =]

<https://www.usenix.org/system/files/nsdi20-paper-agache.pdf>


### CDK with a Golang Lambda

No working from just the "infra" subdirectory in our project:

- **cdk-example/infra/package.json**
- **cdk-example/infra/lib/infra-stack.ts**

`cd cdk-example/infra/`

First update **package.json**

    :::typescript
    "dependencies": {
      "@aws-cdk/core": "*",
      "@aws-cdk/aws-s3": "*",
      "@aws-cdk/aws-s3-assets": "*",
      "@aws-cdk/aws-lambda": "*",
      "source-map-support": "^0.5.16"
    }

Do not forget to `npm install`

Next update the **lib/infra-stack.ts**

> Layout the resources from the deepest dependency first, so in this case a place for the golang function to be zipped

- <https://docs.aws.amazon.com/cdk/api/latest/docs/aws-s3-assets-readme.html>
- <https://docs.aws.amazon.com/cdk/api/latest/docs/aws-lambda-readme.html#handler-code>

    :::typescript
    import * as cdk from '@aws-cdk/core';
    import * as s3 from '@aws-cdk/aws-s3';
    import * as lambda from '@aws-cdk/aws-lambda';
    import assets = require("@aws-cdk/aws-s3-assets")
    import path = require("path")
    
    export class InfraStack extends cdk.Stack {
      constructor(scope: cdk.Construct, id: string, props?: cdk.StackProps) {
        super(scope, id, props);
    
        // Golang binaries must have a place where they are uploaded to s3 as a .zip
        const asset = new assets.Asset(this, 'ExampleFunctionZip', {
          path: path.join(__dirname, '../../examplefunction'),
        });
    
        const handler = new lambda.Function(this, "ExampleFunction", {
          runtime: lambda.Runtime.GO_1_X,
          handler: "main",
          code: lambda.Code.fromBucket(
            asset.bucket,
            asset.s3ObjectKey
          ),
        });
      }
    }


`cdk synth`
> outputting the CloudFormation is a quick way to valied the syntax and see any warnings

`cdk deploy`

    :::bash
    InfraStack: deploying...
    [0%] start: Publishing 05e95f6b38c932a779e68a7a685e9950eca688e775c77f84787f6fa3e2ade474:current
    [100%] success: Published 05e95f6b38c932a779e68a7a685e9950eca688e775c77f84787f6fa3e2ade474:current
    InfraStack: creating CloudFormation changeset...
     (4/4)
     InfraStack
    
    Stack ARN:
    arn:aws:cloudformation:us-east-1:409670809604:stack/InfraStack/248d2960-0104-11eb-8cc5-0ac853a0932f
    

> Use the AWS Console UI and visually look at the cloud formation stacks

e.g. <https://console.aws.amazon.com/cloudformation/home?region=us-east-1#/stacks/>

When you filter and click on your new stack (e.g. InfraStack) you will be able to see the Resources associated with that stack

The default policy "AWSLambdaBasicExecutionRole" will actually allow the Lambda to output logs to Cloudwatch


### CDK with an APIGateway integrated with a Go Lambda

Create the APIG and attach it to the Lambda:

First update **infra/package.json**

    :::typescript
      "dependencies": {
        "@aws-cdk/aws-apigateway": "*",
        "@aws-cdk/aws-lambda": "*",
        "@aws-cdk/aws-s3": "*",
        "@aws-cdk/aws-s3-assets": "*",
        "@aws-cdk/core": "*",
        "source-map-support": "^0.5.16"
      }

`npm install`


Define the API Gateway in CDK _(only adding a few more lines)_

<https://docs.aws.amazon.com/cdk/api/latest/docs/aws-apigateway-readme.html#aws-lambda-backed-apis>

    :::typescript
    import * as cdk from '@aws-cdk/core';
    import * as s3 from '@aws-cdk/aws-s3';
    import * as lambda from '@aws-cdk/aws-lambda';
    import assets = require("@aws-cdk/aws-s3-assets")
    import apigw = require("@aws-cdk/aws-apigateway")
    import path = require("path")
    
    
    export class InfraStack extends cdk.Stack {
      constructor(scope: cdk.Construct, id: string, props?: cdk.StackProps) {
        super(scope, id, props);
    
        // Golang binaries must have a place where they are uploaded to s3 as a .zip
        const asset = new assets.Asset(this, 'ExampleFunctionZip', {
          path: path.join(__dirname, '../../examplefunction'),
        });
    
        const myhandler = new lambda.Function(this, "ExampleFunction", {
          runtime: lambda.Runtime.GO_1_X,
          handler: "main",
          code: lambda.Code.fromBucket(
            asset.bucket,
            asset.s3ObjectKey
          ),
        });
    
        // all routes (and REST verbs) will pass through to the lambda
        const api = new apigw.LambdaRestApi(this, 'examplefunction', {handler: myhandler});
      }
    }
    
> one gotcha is the ordering of imports, have the "path" one last


`cdk synth`
> now the CloudFormation is very verbose =|

_upon inspection you will see the type of integration Lambda is as desired, AWS_PROXY_

`cdk deploy`
> There is a warning about security because AssumeRole

    :::bash
    InfraStack: deploying...
    [0%] start: Publishing 05e95f6b38c932a779e68a7a685e9950eca688e775c77f84787f6fa3e2ade474:current
    [100%] success: Published 05e95f6b38c932a779e68a7a685e9950eca688e775c77f84787f6fa3e2ade474:current
    InfraStack: creating CloudFormation changeset...
      (14/14)
    InfraStack
    
    Outputs:
    InfraStack.examplefunctionEndpoint65D9943D = https://abc123.execute-api.us-east-1.amazonaws.com/prod/
    
    Stack ARN:
    arn:aws:cloudformation:us-east-1:409670809604:stack/InfraStack/248d2960-0104-11eb-8cc5-0ac853a0932f



## Verify your new API Gateway and Golang Lambda with CURL
The very helpful output means you can use `CURL` directly _(as you get to ignore the whole "this apigateway needs to be deployed to a stage")_

`curl https://abc123.execute-api.us-east-1.amazonaws.com/prod/ping`

_you should get back either 404 or "pong" =)_

To see how much more work it is to do (and understand) the API Gateway concepts... 

- <https://blog.john-pfeiffer.com/localstack-apigateway-lambda-and-s3-integration-testing/>
