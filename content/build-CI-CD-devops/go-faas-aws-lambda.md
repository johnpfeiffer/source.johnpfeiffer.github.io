Title: Go FaaS with AWS Lambda
Date: 2018-06-11 19:48
Tags: go, golang, aws, lambda, cron, iam, cloudwatch

[TOC]

The promise of creating functions that do not require server administration is amazing,
the reality though includes a huge maze of vendor specific commands and frameworks (including permissions).


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
4. A User that has credentials (and is in the Group with


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

> Note that the WebUI also provides a way to upload a newer zip file




## Lambda Cron aka CloudWatch Scheduled Events

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

## More Info

Here's a full source code example: <https://github.com/johnpfeiffer/aws-go-lambda>
Compare the unit tests to those from a full web server handler: <https://github.com/johnpfeiffer/go-web-example/blob/master/controller_test.go>

Apparently in order to test the tight integration with using AWS Lambda to consume events from other AWS Services there's a tool:
<https://aws.amazon.com/about-aws/whats-new/2017/08/introducing-aws-sam-local-a-cli-tool-to-test-aws-lambda-functions-locally>



## API Gateway

TODO (and probably using S3 too)

