Title: Go FaaS with AWS Lambda
Date: 2018-06-11 19:48
Tags: go, golang, aws, lambda, cron, iam, cloudwatch, dynamodb, apigateway

[TOC]

The promise of creating functions that do not require server administration is amazing,
the reality though includes a huge maze of vendor specific commands and frameworks (including permissions).

## Why Function as a Service

In many ways most of the work in software engineering is "accidental complexity". Deployment. Input/Output Parsing. Monitoring. Logging. etc.

The "web request" model conquered (much like the historical domination of SQL) in the 90's as networks and the "inter-network" became popular 
(overwhelming the fragmented and isolated vendor specific applications approaches).

- <https://www.nap.edu/read/6323/chapter/8#159>
- <https://en.wikipedia.org/wiki/SQL>
- <https://en.wikipedia.org/wiki/Web_application#History>
- <https://en.wikipedia.org/wiki/Hypertext_Transfer_Protocol#History>


Yet what if your problem/data is not an input/output web request? (Yes of course there are GPUs and dedicated co-location centers...)

Or what about loads of traffic that spike in very extreme bursts (and diminish to almost nothing)?

The allure then is to have a function that runs on demand: truly elastic compute that does not require provisioning a server (not a virtual one and even without a web server).

Without mangaing an OS (and all that security headache!) and especially not paying for idle resources but instead only getting/paying for lots of compute when needed.

Of course there's no free lunch so as that complexity balloon gets squeezed it is the infrastructure/framework vendor that must "magically" provide the input, execute the function, and return the output.

> The irony of "serverless" is that there's still a physical server, drivers, an operating system, and even a web framework, it's just someone else's (problem/revenue).

For "straightforward" web applications it may make more sense to directly offload the hosting/framework but still be in the same comfortable web server model (like Heroku)

- <https://blog.john-pfeiffer.com/infrastructure-as-code-with-terraform-and-aws/#tools-to-manage-state-vs-platform-as-a-service>
- <https://blog.john-pfeiffer.com/go-web-development-and-templates-with-heroku>

## Source Code

    :::go
    package main
    
    import (
        "context"
        "fmt"
        "time"

        "github.com/aws/aws-lambda-go/lambda"
    )
    
    // MyRequest demonstrates an input value
    type MyRequest struct {
        Value string `json:"value"`
    }
    
    // MyResponse helps illustrate how AWS Lambda auto
    type MyResponse struct {
        Message string `json:"message"`
        Created string `json:"created"`
    }
    
    // HandleRequest https://docs.aws.amazon.com/lambda/latest/dg/go-programming-model-handler-types.html
    func HandleRequest(ctx context.Context, req MyRequest) (MyResponse, error) {
        t := time.Now().UTC()
        return MyResponse{
            Message: fmt.Sprintf("hi %s", req.Value),
            Created: fmt.Sprintf("%s", t.Format(time.RFC3339))}, nil
    }
    
    func main() {
        lambda.Start(HandleRequest)
    }


- <https://aws.amazon.com/blogs/compute/announcing-go-support-for-aws-lambda>
- <https://docs.aws.amazon.com/lambda/latest/dg/go-programming-model-handler-types.html>


## AWS CLI Deployment

To avoid some of the complexity with the CLI you may want to first dip your toes in with the Web UI creation of a Go Lambda:
<https://us-west-1.console.aws.amazon.com/lambda/home?region=us-west-1#/create?firstrun=true>

### Packaging for Upload

The easy part is creating a binary...

`go build -o examplebinary`
> build into a single binary

`zip deployment.zip examplebinary`
> wrap it up in a zip

### Prerequisites

Installing the awscli may be a chore (if pip is broken), but `sudo apt install awscli` (from 16.04 should be advanced enough)

*Unable to locate credentials. You can configure credentials by running "aws configure".*

So in order to have credentials you must create a User in your AWS Account (with programmatic access only) which will generate an API key for you. (I suggest using the WebUI)

- <https://docs.aws.amazon.com/cli/latest/userguide/cli-chap-getting-started.html>
- <https://console.aws.amazon.com/iam/home?region=us-west-1#/users>

> Do not use your "Root" Admin account in AWS for the API credentials, security best practice means creating at least one separate User

### AWS Permissions and Roles

> You may have to use the Web UI or some other mechanism to create the IAM role with the correct permissions

Gotcha: the minimum permission would be "lambda:CreateFunction"

- <https://docs.aws.amazon.com/lambda/latest/dg/intro-permission-model.html#lambda-intro-execution-role>
- <https://console.aws.amazon.com/iam/home?region=us-west-1#/policies>
- <https://console.aws.amazon.com/iam/home?region=us-west-1#/roles>

This means the laborious process of creating a Policy that includes all the Lambda permissions (not very secure but it works)

> iam:PassRole

Hilariously the pre-created roles listed in the documentation do not have that specific IAM extra permission, somehow by default an Admin of the account should deploy lambdas?

    {
        "Version": "2012-10-17",
        "Statement": [
            {
                "Sid": "VisualEditor0",
                "Effect": "Allow",
                "Action": [
                    "iam:PassRole",
                    "lambda:*"
                ],
                "Resource": "*"
            }
        ]
    }


## Create an AWS user with API Credentials

So in order to have API credentials (~/.aws/credentials) you have already created:

1. A Policy
2. A Role that can use that Policy
3. A Group that has the Policy attached
4. A User that has credentials (and is in the Group)


### The Actual Create Lambda Command

    :::bash
    aws lambda create-function \
    --region us-west-1 \
    --function-name ExampleFunction \
    --zip-file fileb://./deployment.zip \
    --runtime go1.x \
    --role arn:aws:iam::1234YOURACCOUNT:role/lambda-all \
    --handler examplebinary
> fileb format = file binary


The JSON response from creating the new lambda function (and uploading the zipped Go binary)...

    {
        "LastModified": "2018-06-12T04:55:36.327+0000",
        "Version": "$LATEST",
        "FunctionArn": "arn:aws:lambda:us-west-1:1234YOURACCOUNT:function:ExampleFunction",
        "MemorySize": 128,
        "Runtime": "go1.x",
        "Role": "arn:aws:iam::1234YOURACCOUNT:role/lambda-all",
        "Description": "",
        "CodeSha256": "45R3BZKesxMM3AuZ96lS9UoiOEGX964oHD/J8QQfLfQ=",
        "Timeout": 3,
        "FunctionName": "ExampleFunction",
        "Handler": "examplebinary",
        "CodeSize": 2793060
    }

- <https://docs.aws.amazon.com/cli/latest/reference/lambda/create-function.html>

## Trigger a Lambda Manually

Using the WebUI (AWS Console) you can select the function created with the CLI
<https://us-west-1.console.aws.amazon.com/lambda/home?region=us-west-1#/functions>

By using the "Configure test events" (sometimes a dropdown on the right next to the Test button)

You can create a new "test event" , in this case a MyRequest (though any arbitrary extraneous JSON will be ignored)

    :::json
    {
      "value": "john",
      "key2": "value2",
      "key1": "value1"
    }
> this test event sends one value and some extraneous JSON keys as input to the lambda function


    :::json
    {
      "message": "hi john",
      "created": "2018-06-12T04:34:22Z"
    }
> the lambda function output is automatically converted from an object to JSON


Note that the WebUI also provides a way to upload a newer definition of the lambda function (zipped in a file)


## Lambda Cron aka CloudWatch Scheduled Events

The real power of AWS Lambdas involves how it becomes glue for connecting lots of other AWS services (and transformations).

For example CloudWatch can be used to schedule/trigger a lambda.

In the WebUI you can add a trigger via the Designer (on the left)

Select "CloudWatch Events" -> Configure triggers (scroll down) -> Create a new rule

Configure a trigger, "Scheduled" (as opposed to Rate which is similar but different ;)

Name: "examplecron"

`cron(16 * ? * MON-FRI *)`
> This would be on the 16th minute every hour every day every month on Monday through Friday (every year)
> cron(Minutes Hours Day-of-month Month Day-of-week Year)

Disabling the "example" Cloud Watch Event is as easy as toggling a radio button
(this is an interesting way of controlling how/when your function executes)

- <https://docs.aws.amazon.com/lambda/latest/dg/tutorial-scheduled-events-schedule-expressions.html>

## Lambda Monitoring

In the same WebUI where you view the Lambda function (by name) you can click on Monitoring and click around to see Metrics
(i.e. Lambda Cron aka CloudWatch Scheduled Events) actually "invoked" your function.

Of course if you haven't enabled CloudWatch Logging or more importantly created a "Log Group" then you get nothing.

- <https://docs.aws.amazon.com/AmazonCloudWatch/latest/logs/Working-with-log-groups-and-streams.html>

## More Info on Lambdas

Here's a full source code example: <https://github.com/johnpfeiffer/aws-go-lambda>
Compare the unit tests to those from a full web server handler: <https://github.com/johnpfeiffer/go-web-example/blob/master/controller_test.go>

Apparently in order to test the tight integration with using AWS Lambda to consume events from other AWS Services there's a tool:
<https://aws.amazon.com/about-aws/whats-new/2017/08/introducing-aws-sam-local-a-cli-tool-to-test-aws-lambda-functions-locally>


## API Gateway

As a pre-requisite (and to leverage the fully integrated nature of the AWS ecosystem) we will create some data first...

**And of course create a new Role that is linked to a Policy =(**

<https://console.aws.amazon.com/iam/home?region=us-west-1#/roles>

Ensure you have a new Role (confusingly in the UI click through as a Lambda Service needing access) and choose the predefined Policy "AmazonDynamoDBFullAccess"

    arn:aws:iam::123476797434:role/DynamoDBFull
> Of course you'll have your own unique ARN and Security best practice would involve defining a more precise role (i.e. not giving permission for Auto Scaling)

Modify whom can assume the Role (using the AWS Web UI Console) <https://console.aws.amazon.com/iam/home?region=us-west-1#/roles/DynamoDBFull?section=trust>

*If you receive an error later on it will be because of the Edit Trust Relationship, "API Gateway does not have permission to assume the provided role"*

    {
      "Version": "2012-10-17",
      "Statement": [
        {
          "Effect": "Allow",
          "Principal": {
            "Service": ["apigateway.amazonaws.com", "lambda.amazonaws.com"]
          },
          "Action": "sts:AssumeRole"
        }
      ]
    }
Click on "Update Trust Policy"

### Readonly via DynamoDB

Use the WebUI (console) to create a new table <https://us-west-1.console.aws.amazon.com/dynamodb/home?region=us-west-1>

- Create a table named: stocks
- Primary Key: symbol (string)
- Sort Key: timestamp (number)

*Uncheck Auto Scaling "Read capacity" and "Write capacity" checkboxes*

> Do not use the default settings, we will disable autoscaling in order to save money and somewhat arrive at fixed cost

- <https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/AutoScaling.Console.html#AutoScaling.Console.Modifying>
- <https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/HowItWorks.NamingRulesDataTypes.html#HowItWorks.DataTypes>

*(Note that types are quite specific in DynamoDB, e.g. the binary "scalar" value can only contain up to 400KB of base64 encoded data)*


After a few minutes of initialization select the "Items" tab then the "Create item" button to manually create an entry:

- <https://us-west-1.console.aws.amazon.com/dynamodb/home?region=us-west-1#tables:selected=stocks;tab=items>

In the Web UI you will have to choose the dropdown (upper left) and change it from "Tree" to "Text" in order to enter a price

    :::json
    {
      "symbol": "VFINX",
      "timestamp": 1529697600,
      "price": 255.44
    }
> Using a historical stock price (in dollars) at the close of business

*(Adding a second entry for 1529611200 and 254.95 can be helpful too)*

After clicking Save and possibly a "Refresh data from server" (arrow lines in a circle on the right) you will see the new entries.

#### Setup a new API Gateway connected to DynamoDB

<https://console.aws.amazon.com/apigateway/home?region=us-west-1#/apis/create>

- "New API"

    API Name: stocks
    Endpoint Type: regional

- Actions (Resource Actions) -> Create Resource

    Resource Name: stock
    Resource Path: /{symbol}

- Click "Create Resource" to save.
- Actions (Resource Actions) -> Create Method (a dropdown appears in the WebUI below /{symbol}) , choose "GET"

	Integration type: AWS Service
	Region: us-west-1
	AWS Service: DynamoDB
	HTTP Method: POST (for interactions with DynamoDB)
	Action Type: Use action name
	Action: GetItem
	Execution role: arn:aws:iam::123476797434:role/DynamoDBFull
	Content Handling: Passthrough

> The permissions/role ARN was created earlier and GET using POST is actually for interacting with DynamoDB

- Click on the "Integration Request" for the /{symbol} - Get 
- Scroll all the way to the bottom and expand "Body Mapping Templates" so that you can click on "Add mapping template"

Content-Type: application/json
 
Confusingly after you create your type you must click on it to get a UI to define the JSON transformation, use the following:

	{
	  "TableName": "stocks",
	  "Key": {
	    "symbol": {"S": "$input.params('symbol')"},
	    "timestamp": {"N": "1529697600"}
	    }
	  }
	}
> Emulating a direct low level request <https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/Programming.LowLevelAPI.html>

Back at the Web UI for "/{symbol} - GET - Method Execution" there is a button "TEST" that allows for validation of the API Gateway.

This is helpful for detecting early the inevitable bugs that crop up.

(Note: it does not seem to me that debugging an API this is way is actually faster...)

In the Test UI enter the stock symbol "VFINX" underneath {symbol} to emulate a GET request, then click on the "Test" button.

The Response Body on the right shows the response (that the client would see - though often revealing an error directly from DynamoDB)

*Careful readers will notice that the timestamp variable is hardcoded in the transformation, todo: make the timestamp part of the query parameter"*

### Where is the Code?

One thing that is missing from this trivial example is how version control is applied to ensure deterministic change (and best practice reviews).

Rather than just using the WebUI we should leverage "Infrastructure as Code" like CloudFormation but I would suggest more complete tools like:

- <https://www.terraform.io/docs/providers/aws/guides/serverless-with-aws-lambda-and-api-gateway.html>
- <https://serverless.com/framework/docs/providers/aws/events/apigateway/>

One thing you might notice as you convert API Gateway + Lambda into code is that it begins to look a lot like code you would see in any web application,
except that it is in a DomainSpecificLanguage for a specific vendor framework.


## Comparisons

Two things that are practically relevant are:

1. Latency
2. Cost

Lambdas will inherently have "warm up time" from a "cold start", while this can be mitigated (with a canary warmer etc.),
if your architecture is deliberately tying together lots of services over the network it may feel slow (and indeterministics).

The contrast is to keep more things in memory or co-located in the same server. (Less network calls)

Cost is fickle: Lambdas may be much cheaper but if configured incorrectly a DOS attack could create a lot of API Gateway events or CloudWatch logs (so indirect cost escalation).

So there are workarounds but investing in them once again means the benefits (reduced overhead) come with a new complexity (and skill set).

Google and Azure both provide functions as a service so while it may be possible to get price competition given the vendor lock-in nature switching costs may be non-trivial.

Amazon cleverly have a "free tier" that covers enough to get developer hobby projects (aka time invested learning = biased professional purchasing choices) which covers everything in this article. <https://aws.amazon.com/free/> *I have no affiliation with Amazon, Google, etc.*


From a philosophical perspective the choice is somewhat whether building with predefined vendor blocks (so WebUI or IaaC) is more valuable (time wise)/preferrable than code.

## Trust

Something that underlies all of the AWS Lambda thinking and work is trust in the vendor.

- Trust in their security practices
- Trust in their uptime and operations team
- Trust in their business (both longevity and pricing)


