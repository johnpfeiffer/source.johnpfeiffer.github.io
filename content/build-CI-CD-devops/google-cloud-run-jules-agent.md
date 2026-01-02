Title: Google Cloud Run and Google Jules coding agent
Date: 2025-06-07 06:07
Tags: github, google cloud run, ci, cd, deployment, ai, agent

[TOC]

# Another day another cloud

Since "Google App Engine" charges for "Artifact Registry" which shouldn't be a big deal but for the "Developer who just wants to run code" it feels like extra overhead and cost

Google Cloud Run "free tier" is ridiculously confusing to calculate (charged by the millisecond) but should "just run".

So here's how to setup a golang web server automatically built and deployed from each GitHub commit.


*Note: apparently Cloud Run also uses Artifact Registry to automatically leverage a Docker image that presumably if deployed enough times could go beyond the free tier :(*

## Different day same Code

If the web server starts automatically on port 8080 then it is "Cloud Run Compatible"

<https://github.com/johnpfeiffer/aws-go-lambda>

*Their official example https://github.com/GoogleCloudPlatform/cloud-run-microservice-template-go*

## Google is project-centric

Then navigate to a project (or make a new one)

<https://console.cloud.google.com/run/overview?project=go-cache>

"Deploy a web service" -> Connect repository

## Configuration
GitHub: "Continuously deploy from a repository (source or function)"
*(this works for languages supported by Google)*

Cloud Build: Can deploy from GitHub repositories.

"Set up with Cloud Build" (button)

Source repository: GitHub

- Currently not authenticated, Authenticate
> You will be asked to authorize the Google Cloud Build GitHub App to access your GitHub Account to proceed. 
- - creates a pop up (check your blockers!): "Authorize Google Cloud Build"


Repository: Manage connected repositories

- creates a pop up to GitHub (simplified integration and authentication/authorization)
- - Only select repositories (choose from the dropdown)
- - - legalese checkbox

**Build Configuration**

Branch: ^main$

Build Type: Go (or Node.js, Python, Java, .NET, Ruby, PHP)

*nothing special for Build context, Entrypoint, or Function target (The name of the exported function to be invoked, leave blank if the source repository is a web server.)*


Service name: go-cache

Region: us-west2 *(tier2 is cheaper than tier1)*

Authentication: Public *(unless you have something specific in mind)*

Billing: Request-based, Charged only when processing requests. CPU is limited outside of requests.

Service scaling: Minimum number of instances = 0 , Maximum number of instances = 1

**very important to set these values to 0 and 1 to stay in the free tier**

"Edit Container" has the opportunity to change things or add a variable/secret - ignore for now


**Create (button)**

<https://docs.cloud.google.com/run/docs/continuous-deployment#existing-service>

## Checking on Builds

When builds are occurring (or failing) 

<https://console.cloud.google.com/cloud-build/>


## Cleanup Artifact Registry

You can search and find amid the 100s of services the one that sometimes invisibly goes over a free tier...

<https://console.cloud.google.com/artifacts/>

Click on "cloud-run-source-deploy" and click in until you get to something like "Digests for aws-go-lambda/go-cache"

Choose an old deploy as a checkbox and then at the top click Delete

> Are you sure you want to delete...

*hopefully this keeps me under the free tier limit*

# Agentic Coding with Google Jules

Google "Gemini" (https://gemini.google.com) is the LLM chat application

*Useful for general questions including about technology terms, architecture options, code snippets, troubleshooting, etc.*

> ...you have encountered the very real friction of Google Cloud's IAM system firsthand. What should feel like a single, simple action often requires a complex combination of permissions... the single App Engine Deployer role is not sufficient for a complete developer workflow, and it does not cover administrative tasks or broader access needs


"Agentic Coding" is where the LLM agent takes instructions in english and modifies the code.

**<https://jules.google.com/>**

*Google account as before, Sign in, accept all the terms and conditions of this experimental AI software*

Has a purple octopus logo

Choose a Repo from the dropdown (top center) -> "Configure repo access"

- opens a new tab (window?) in GitHub for "Google Labs Jules"
- Repository access: Only select repositories (choose the ones the agent can work on)

"Save" (button)

> Successfully authenticated with GitHub!

*<https://github.com/settings/installations> is where GitHub lists integrated Applications*

Choose the repo (i.e. johnpfeiffer/aws-go-lambda)

Give Jules the instructions in the text box (not on the bottom right you can choose a mode like "interactive plan" or "review" - or just **"Start"**)

*These tasks run in an isolated sandbox hosted by Google*

## Watching an agentic task in progress

On the left (expand/collapse) side panel you can see how many "daily sessions" you have left.

Clicking on a session gives you all the details:

- how the agent broke the instructions down into a plan
- it runs `go test -v` on its own
- sends a (draft) pull request to the code repository

*there is a "View PR" button*

<https://github.com/johnpfeiffer/aws-go-lambda/pull/1>

## Iterating on the Pull Request

Leaving a comment on the pull request will feedback to Jules (yay for all the permissions) who then automatically resumes the session.

> I have received the PR comments and am processing them.

> Ready for review 

*the usual GitHub pull request merge process*

## Gotchas with Agents

Lots of posts on the internet but in case you wanted to "hear it here first":

- sounds confident even when wrong or has mistakes
- often imports random libraries or calls external APIs
- deletes tests
- modifies code and says "done"... but the code does not work, is not done
- mediocre code quality that is either one large ball of mud or a tangle of tiny functions
- unnecessarily over-engineered code and abstractions

Mitigations

- read and review critically
- have specifications, documentation, and anchors
- tell it build as simple as possible and not to call external APIs
- give it boundary instructions: that it cannot modify or delete tests
- give it examples of expected input and output
- give it explicit instructions on the level of modularity ("make this 3 functions")

