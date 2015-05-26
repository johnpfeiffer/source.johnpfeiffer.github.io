Title: Pragmatic testing, from Makefile to CI with Docker
Date: 2015-05-25 10:00
Tags: testing, selenium, docker

[TOC]

A colleague recently suggested "Hey, why don't you run those tests from outside of the target server under test?"

And I thought to myself, "Hmm.... why are we doing it that way?  Was I just dumb when I did this the first time?

The answer is the journey of successfully testing a successful product and the pragmatic choices made along the way.  I believe that engineering requires compromises because without achieving short term progress we would have never reached our bigger, long term goals.

### Humble beginnings with Makefile

Our initial project was to deliver an OVA (open virtualization archive) that packaged all of the services (and dependencies) into an easy to deploy and maintain virtual appliance.

Will, as the project lead, had already spent some time setting up the build environment using vStudio and an Ubuntu ISO but one of our first issues after generating an OVA was to try and determine if it was "good".  Could it even be deployed?  Did it have the services installed correctly?

I leveraged the Makefile that we were already using for the build to create a "test": deploy the latest OVA artifact and check that it was basically sound.

This was a good start as, at the very least, we could quickly determine and bisect where we were producing bad builds.

### Adding some tests, but where?

Once the initial spike ("tracer bullet") was done I began adding in selenium python based tests to verify the Web UI interface.

Since our Continuous Integration system was basically bash and Makefile (which was also our build system) I opted to run the tests from inside of each deployed Virtual Machine.

This allowed for isolation of the test execution from the build process and for each test run.  

While not ideal for product acceptance testing it provided a basic safety net that allowed us to know if a breaking change occurred upstream and was the first automated verification (followed by lots of manual testing) of the exact OVA we were shipping to Customers in the Beta.

### Bamboo Continuous Integration for visibility and the team

A further improvement was to improve visibility of the test results.  In parallel, after the team discussion during "HipCon" and with motivation from Don and Sam, I setup a private Bamboo installation in our VM area and helped get Integration tests setup for our upstream backend code.

Once again I stuck with the tried and true "tests inside of the target virtual machine" pattern as the Bamboo server was only using "local agents" and I was concerned about trying to maintain a clean environment and the resources required as the number of test plans scaled.

Additionally I migrated all of the previous test plans from the "build factory" into Bamboo which really helped with failed test visibility and tracking over time.

The unit tests continued to run in a different SaaS version of Bamboo so I avoided scope creep and left things that were working alone.

### Migrating to a managed service

One of the most asked questions whenever a new person joined was "Why are the tests spread across so many different servers/services"?  I had to answer that question so many times!  The answer basically boiled down to "the testing grew organically as different people in the team solved the problem they faced".  Unsatisfactory? "Be the change you seek" didn't seem to get anyone else to solve the problem for me ;)

Using the opportunity presented by a service outage issue I pushed forward a plan I had to migrate all of the test plans into a newly provisioned Bamboo server run by Build Engineering. (awthanks)

There was an awesome team effort by a lot of people to make that happen (made even more challenging by doing it when the source service was out). (awesome)

This solved quite a few problems:

1. The Unit, Integration, and Product Acceptance tests were all finally combined under one roof... one UI to rule them all!
1. New people joining the team needing access to Bamboo: since I hadn't linked it to any directory/authentication I was adding users manually - we were finally able to leverage an Atlassian backend Directory system
1. I had been managing upgrades and maintenance of the Bamboo software (not fun and not my core expertise)
1. I began to worry about the resource consumption (since this was running on hardware that also provided for our Build Factory) - no longer a worry with lots of Remote Agents and Elastic Agents (all provided by Build Engineering)

Bonuses:

1. More plugins and capabilities and knowledge from the Bamboo server and Build Engineering expertise
1. Plan Templates to keep test plans in version control and macros for common functionality
1. A successful spike of using Docker for unit testing

With so much going on during the migration I avoided changing the testing paradigm, so tests continued to execute inside of each VM/EC2 Instance deployed. (shrug)

### Adopting Docker and refactoring

Remember that question at the beginning?  When something goes wrong, while it makes sense to separate "fixing it" from "improving it" I'm a big fan of taking advantage of having the hood open to go the extra mile and leave the campground cleaner =)

So some of the selenium based tests were failing and it occurred to me that some of how we were changing our dependency infrastructure at the operating system level could be the cause.  After some unproductive poking around I tried to reproduce and isolate the issue by running the tests from outside of the VM.

Aha! In that moment I realized that this was actually the desired (original intention, honest!) way to run the blackbox product acceptance tests.

So I pulled up my sleeves and tried out the "hot fancy new silver bullet technology that solves every problem".

#### Why Docker?

Docker encourages design of modular, deterministic and defined, single purpose components that are easy to reuse and compose into larger services. 

Not only are (Docker) Containers fast, one of the biggest advantages of Containers is the ability to reduce complexity. Docker can turn an application/service, it's dependencies, and even the OS level requirements into a single blackbox package (that you can still inspect inside if you really want to).

So I built a Docker Image containing python selenium and <http://phantomjs.org/> (a headless javascript based browser) and other dependencies.

Sure enough I the tests passed when leveraging the previous Docker spike to run my new docker container. (success)

Refactoring the bamboo plan (since it was leveraging Plan Templates and the Groovy DSL macros) didn't take too long and with other stakeholders PR/approval we're moving full speed ahead towards the "ideal" solution. (It only took about 2 years).

### What does this all mean?

It's easy to draw up how things should work according to best practice.  It's even easier if it's work that someone else has to do and there aren't any deadlines.

Success comes in stages.  Overengineering and premature optimization cost way more in opportunity cost and thrown away work than doing things the "wrong way".

This story could be massaged to fit a parable of "Lean and Agile" but it's really just common sense about transparently understanding the cost/value tradeof of the work, solving the current needs, and moving forward onto something better (by keeping informed of new solutions) when the opportunity shows up.
