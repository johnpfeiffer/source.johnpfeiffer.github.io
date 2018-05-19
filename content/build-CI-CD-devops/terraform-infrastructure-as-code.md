Title: Infrastructure as Code with Terraform and AWS
Date: 2018-05-12 07:35
Tags: terraform, aws, digital ocean, devops, immutable

[TOC]

## Overview

Just like building and maintaining hardware and physical servers by hand is manual drudge work (aka "toil"),
so is the manual deployment of servers and networking etc. even on "Infrastructure as a Service".

The "Infrastructure as Code" movement emphasizes the value of human time and leverages source code and version control to manage the increasing complexity.
*(Think of the exponential growth of logical systems with virtualization, cloud services, containers, and micro-services etc.)*

Imagine a tool to automate deploying and managing virtual infrastructure...

While AmazonWebServices CloudFormation works for setting up infrastructure via a config file, the user experience is non-optimal and there is definitely "vendor-lock-in".

Hashicorp are a trusted brand in DevOps and having produced Vagrant, Packer, Consul, etc. it is easy to pick their Terraform product.
> I have no affiliation with Hashicorp besides as a user of their software =)

While packer can build a single immutable image (an application or component) of a (virtual) server (or container),
Terraform is the higher level tool where the full setup including Load Balancer, Database, etc. are managed.
Terraform can also maintain "state" like replacing servers with (deploying) newer images that were built by packer.

The configuration files can be applied to various Cloud and Infrastructure vendors providing some measure of portability.

References:

- <https://en.wikipedia.org/wiki/Infrastructure_as_Code>
- <https://blog.john-pfeiffer.com/build-automation-using-packer-to-build-an-ami-use-immutable-not-chef> (packer runs commands to create a machine image - aka a server frozen as a file)
- <https://aws.amazon.com/documentation/cloudformation>
- <https://www.digitalocean.com/community/tutorials/how-to-use-terraform-with-digitalocean>

## Prerequisites

Basically you need access to the remote infrastructure, permissions to make changes (resources cost money!), and of course the Terraform tool.

1. Download from <https://www.terraform.io/downloads.html> (and probably unzip to \opt) the terraform binary, *you may also want to `echo "alias terraform='/opt/terraform'" >> ~/.bashrc `*
2. Verify that the terraform binary has been installed and can execute: `terraform version ; terraform help`
3. Create an SSH keypair: `ssh-keygen -t rsa -C "myemail@example.com" -f $HOME/.ssh/aws.id_rsa`
4. Upload the keypair to AWS <https://us-west-1.console.aws.amazon.com/ec2/v2/home?region=us-west-1#KeyPairs:sort=keyName>
5. Create a dedicated User with limited permissions: <https://console.aws.amazon.com/iam/home?region=us-west-1#/users>
6. Ensure the new User (i.e. terraform-demo) only has "Programmatic Access" (aka API only, not WebUI)
7. Ensure the new User has permissions, i.e. is part of a Group (named ec2-only) that leverages the pre-generated policy name of EC2FullAccess)
8. The last step of the create user wizard should show the ACCESS_KEY and SECRET_KEY , make sure you **save these in a password manager**.

> Using Environment variables is a fairly standard and portable/secure way of providing credentials to Terraform, the **region will determine where** resources are created

    export AWS_ACCESS_KEY_ID="AKIAyourACCESSkey"
    export AWS_SECRET_ACCESS_KEY="yourSECRETkeyABC123"
    export AWS_DEFAULT_REGION="us-west-1"

*Alternatively save the credentials in the default amazon credentials file (~/.aws/credentials) by using `aws configure`*

References:

- <https://www.terraform.io/docs/providers/aws/index.html>
- <https://docs.aws.amazon.com/cli/latest/userguide/cli-chap-getting-started.html>
- <https://docs.aws.amazon.com/IAM/latest/UserGuide/access_policies_managed-vs-inline.html>
- <https://aws.amazon.com/about-aws/global-infrastructure>

## A simple build

The simple and common example of deploying a new server instance from an AmazonMachineImage (with a new VPC for network control)

### Example Terraform File

**example.tf**

    :::terraform
    provider "aws" {
      region = "us-west-1"
    }
    resource "aws_instance" "example" {
      ami = "ami-dc2739bc"
      instance_type = "t2.nano"
      subnet_id = "${aws_subnet.us-west-1a-public.id}"
    }
    resource "aws_vpc" "example" {
      cidr_block = "192.168.1.0/24"
      enable_dns_hostnames = true
      enable_dns_support = true
    }
    resource "aws_subnet" "us-east-1a-public" {
      vpc_id = "${aws_vpc.example.id}"
      cidr_block = "192.168.1.0/28"
      availability_zone = "us-west-1a"
    }
> The provider is the target (with a specific sub region), and each resource has a type and a name (which can be referenced in later variables)

*While Amazon Linux images are hardened CentOS with security updates it can be convenient to use Ubuntu 16.04 (and most likely real world use cases will be from an AMI you have built yourself)*

> The AMI ID is region specific,  this example comes from us-west-1

References:

- <https://cloud-images.ubuntu.com/locator/ec2>
- <https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/AMIs.html>
- <https://www.terraform.io/docs/providers/aws/r/instance.html>
- <https://aws.amazon.com/premiumsupport/knowledge-center/instance-store-vs-ebs/>
- <https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/virtualization_types.html>
- <https://docs.aws.amazon.com/AmazonVPC/latest/UserGuide/default-vpc.html>
- <https://docs.aws.amazon.com/AmazonVPC/latest/UserGuide/VPC_Subnets.html>
- <https://aws.amazon.com/free> *(not much is free)*


### Terraform Plan and Apply

The single configuration file and the following commands will deploy the prescribed infrastructure to AWS.

`terraform init`
> install the AWS plugin (that is detected via the example.tf configuration file), you will need to git ignore .terraform and plugin binaries

`terraform plan`
> This will preview the steps that will occur

    Terraform will perform the following actions:
        + aws_instance.example
            id:             <computed>
            ami:            "ami-dc2739bc"
            instance_type:    "t2.nano"
            ...
        + aws_subnet.us-west-1a-public
            id:                               <computed>
            assign_ipv6_address_on_creation:  "false"
            availability_zone:                "us-west-1a"
            ...
        + aws_vpc.example
            id:                               <computed>
            assign_generated_ipv6_cidr_block: "false"
            cidr_block:                       "192.168.1.0/24"

> + means created , - means removed , the VPC and subnet ids may even be populated

To avoid the issue of VPC or no VPC (and for better default security) this will explicitly create a new VPC.

`terraform apply`
> Once again the expected results are displayed and a prompt requires confirmation

    aws_instance.example: Creating...
      ami:                          "" => "ami-44273924"
      ...
    aws_instance.example: Still creating... (10s elapsed)
    aws_instance.example: Creation complete after 16s (ID: i-0492ba9707e624a66)

    Apply complete! Resources: 1 added, 0 changed, 0 destroyed.

> the **.terraform.tfstate** file contains the current state of the current infrastructure

`terraform show`
> A full listing of the details of the infrastructure is returned

- To see the instance in the WebUI: <https://us-west-1.console.aws.amazon.com/ec2/v2/home?region=us-west-1#Instances:sort=instanceId>
- Verify the new VPC <https://us-west-1.console.aws.amazon.com/vpc/home?region=us-west-1#vpcs:>

### Updates to Existing Infrastructure and Instances

If you modify and save example.tf file to add a tag Name:

    resource "aws_instance" "example" {
      tags {
        Name = "terraform-example"
      }
    ...

`terraform plan ; terraform apply`
> The remote infrastructure (server) has been updated with a tag/Name "example" , `terraform show`

If you change the resource AMI ID (i.e. the base immutable image from which the server was created) then Terraform will destroy the old server and deploy a new one

- <https://www.terraform.io/intro/getting-started/change.html>
- <https://blog.gruntwork.io/an-introduction-to-terraform-f17df9c6d180>

### Destroying

`terraform destroy`
> This is a destructive command, as always you must type "yes" ... "There is no undo"

    Terraform will perform the following actions:
      - aws_instance.example
      - aws_subnet.us-west-1a-public
      - aws_vpc.example

`terraform show` will return nothing and inspection in the AWS Console (web ui) will show all the resources have been cleaned up =)

## A Load Balanced Example

- <https://www.terraform.io/intro/examples/aws.html>
- <https://github.com/terraform-providers/terraform-provider-aws/tree/master/examples/two-tier>


## Tools to Manage State vs Platform as a Service

Infrastructure as Code focuses on tools to manage complexity. An alternative is to outsource the infrastructure entirely by using something like a PlatformAsAService.

Heroku (or Google AppEngine or Openshift) can simplify application deployment by reducing the input to simply the application code.

The PaaS vendor manages the infrastructure (including load balancers) and can provide a WebUI and APIs for adding dependencies (i.e. databases).

Though it may again require a vendor specific configuration file to specify which application is connected/has permissions to which database...

