Title: A micro story about migrating a personal monolith into microservices
Date: 2016-07-29 20:59
Tags: microservices, monolith, linode, digitalocean, packer, drupal, php, python, go, cherokee, nginx

[TOC]

I'm a fan of best practices (who isn't?) and as complexity increases one of the modern paradigms is to use microservices to more transparently manage complexity, reduce tight coupling, and decrease maintenance overhead.

Taking a different approach to my "less than webscale" personal web services has still made great improvements to the services and my quality of life.

This article is categorized as Build and CI/CD and DevOps because while microservices is transformative for larger organizations to avoid the negative consequences of Conway's Law and provides a better architecture for really complex systems, in my case it was simply about decoupling deployments and not having all of my eggs in one basket. (e.g. the Drupal migration below actually did not affect the User Experience in any visible way).

## How to grow a monolith

### Value, value, value

I've had a Virtual Private Server for many years and have been always able to find something for free (or as my requirements increased at most $10 a month).  This has been at least 1000x worth the investment as it has provided a platform for learning and experimenting with all sorts of technology (Linux, PHP, Python, Twisted, MySQL, Redis, etc.) and of course a useful catch all tool (to check DNS resolution or temporarily store a file).

I'm a firm believer in understanding the whole stack.  Maintaining the OS and managing deployments has made me conscious of the many hidden costs and compromises/trade-offs in software and services.

### Organic Sprawl

While I started with a personal notes site in PHP, I eventually added a couple of personal blogs using Drupal, and then another Drupal site about physics (<http://physicstime.com>) for my father in law, and then a few experiments in Python (including uwsgi and Twisted).  This was all of course underpinned by the shared underlying Cherokee web server, Drupal, PHP, Python, MySQL, and Ubuntu.

Physicstime alone has served over 500,000 visitors =)

I envisioned that having a common platform would make it easier to add more sites and the shared maintenance meant I would only have to pay it once, especially considering the alternative of paying for and deploying many separate servers.

I got to try a lot of different technologies but it started to be clear that it was not a "common platform" and maintenance (and just the mental energy of worrying about deferred maintenance) started to take up way too much time and effort.

### The downsides of a monolith

Anecdotes: a security update meant the infrastructure provider needed to restart all of their host machines which meant "hmmm, will all my services restart correctly on reboot?" - luckily yes.  Then I had to patch my virtual server (anything on the Internet is one vulnerability away from becoming taken over and in the least case being used for spam/DDoS and eventually being unable to actually serve my sites, in the worst case rooted or keystroke-logged in an attempt to hack my life or in a serious criminal pursuit).

Oh and then there's the times the logs (web or auth due to anonymous attackers scanning) or backups filled the disk... (facepalm)


Unavailability Due To:

- any infrastructure vendor maintenance 
- any OS maintenance/upgrade 
- incorrectly configured/rogue application
- a security issue in one affects them all
- they all contend for the same resources
- they all share the same version/dependency requiring upgrading and testing everything at once

### In Context: Linode, Ubuntu, Cherokee, and Drupal were good choices at the time 

Firstly let me say I picked a great vendor (Linode) who was very solid (they limit bad actor customers which tends to make resources predictable) and that Ubuntu OS and Cherokee webserver are very easy to setup and maintain which is one reason why I've put this off for so long.

Drupal does an ok job of separating the tech stack from the content publishing so it was possible to ignore the tech side for awhile.

Another factor is that iPhones/Android, Dropbox, Bitbucket/GitHub, PaaS, and a whole generation of technologies were not around when I set this up.

Finally, maybe it's a corollary to Moore's law and the prevalence of the cloud but there's quite a bit of free compute around than there used to be ;)

## Thinking Microservices 

Thinking about microservices is like TDD (Test Driven Design): it exposes assumptions, unmanaged organic evolution, and accidental complexity.

### Discovering the real problem domain

> When you have a hammer everything looks like a nail

It becomes too easy to just use an interesting or popular technology for everything regardless of the true problem.

Analyzing what I actually did with the various services I realized there were actually two distinct phases: creation and distribution.

I did not have a "realtime" or "high volume dynamic data" use case, nor even a large number of content publishers that needed extra tooling.  (The plugins/additions I used weren't even that exotic.)

In contrast the overhead was my irreplaceable time spent for the maintenance of Ubuntu patching/upgrades, including the underlying PHP, Drupal upgrades, backups, and of course the inestimable risk of running something on the Internet. ;)

## How I Converted to Microservices: Big Bang vs Kanban

A common question is "how", and since "it depends" ;) in this case I had limited free hours to accomplish change and a strong desire to not break existing service.
 
Rather than "Big Bang" I went Kanban https://en.m.wikipedia.org/wiki/Kanban_(development) (a much better analogy than Martin Fowler's "strangler pattern" analogy http://www.martinfowler.com/bliki/StranglerApplication.html).  This allowed gradual migration with the least disruption and the most flexibility in when changes would occur.  As a not-to-be-underestimated bonus it was also the least stressful.

Since I publish a post maybe once a month my blog was the simplest start .

Feature parity requirements:

- publish read-only pages to the world
- editing
- some minimal data structure (category and tags)
- search
- preserve content and meta data
- regular backup of the content

I migrated my content to a Pelican static site (with advanced functionality via a nice JavaScript theme) running on GitHub static pages and Travis CI.

Having text in git provides a built in backup (published as html and stored remotely in markdown in the free "Software as a Service" repository) with of course a local git repo working copy on my laptop.

The result is I only need to do a single git push of markdown text to deploy to production.  It's highly available, scalable, and as a bonus there is versioning and I got a fairly snazzy facelift with improved search.


### Migration has extra costs of research and tweaks but is an opportunity for new benefits

First I had to research and evaluate static site generators and static site hosts.

Next I had to learn how to setup a workflow with test data to automate the process from writing content to publishing.

The actual data migration was quite lengthy.  This was due to the inevitable format change (export from Drupal to .md) and post transformation validation. 

Of course I also had to update DNS entries and even setup subdomains and 301 redirects.

Like any rewrite I also ended up adding things (like tags).

One of the most beneficial "while I'm already redoing everything anyways" enhancements was adding CDN and SSL via Cloudflare which actually added another layer of availability and security.

### Data Gravity is expensive and Microservices allows polyglot so Go Programming

My personal notes are full of years of research and was the most time consuming, fulfilling the adages of "data gravity" and "unstructured data costs you" =(

A free static site on bitbucket.org (markdown in a free git repository transformed to html for free via Shippable.com) used the same pattern (and Pelican tech) as my blog: version control, offloading the hosting to someone else, and JavaScript for search.

While the file system organically captures metadata like "created date" I had to inject that into the content; I found this to be a data integrity improvement as I had noticed before that FTP and git have a tendency to discard that metadata.

One of the most time consuming transformations was just tweaking the plain text into markdown but this was worth the improvement in readability since the content is far more often read than written =]

While Markdown violates the principle of separating data and presentation I found it to be a pragmatic compromise as it IS a standard and it's machine readable. (I could theoretically use a script to convert it back to plaintext ;)

Oh right, so Go, aka Golang?

I leveraged Google AppEngine and for fun got to use the relatively new programming language Go to write a custom 301 redirector to prevent links on the Internet from breaking and allow search engines link from all of the previous URLs to the new locations.

While Python is very easy to pickup I found Go to be similar enough (especially to C) to be also not so hard to pickup (lots of documentation!) and better able to do what I needed simply within the language (though Python pretty much has a library for everything it also has C dependencies that don't always play nice with a PlatformAsAService).

### Drupal to Drupal

> The more things change the more they stay the same.

> Wherever you go there you are.

The most active Drupal site will stay Drupal on DigitalOcean (to leverage their one click example) and cheaper prices.

Edit: one click was for Drupal8, yet another headache migration, so not in the scope of this project.

Now at least as an isolated service (website) on a dedicated server, updates will be specific to it.

I also put in the effort to use automation via Packer and experiment with Docker...

#### Immutable Packer

I considered Docker Machine and Ansible but both seemed the wrong tools for my purpose.

Docker Machine is still relatively new and is more oriented towards a cluster of nodes.  Additionally the post docker image phase (ssh commands to install things) seems overly complex.

Ansible (SSH paradigm) is simpler than chef but encourages a mutable long lived server.

Packer has a simple and straight forward way of building an immutable server image for DigitalOcean yet retains the flexibility to adapt to other cloud vendors later if needed.

#### Drupal website context and domain problems

Besides the basic components (Docker will simplify this): nginx, php, MySQL

The ongoing issues:

-Backups of the MySQL and uploaded files
-Upgrades of the OS and components (security)
-Upgrades (security) of Drupal and modules

The full details are in a separate post but I'm pretty happy that setting up the box from scratch again, upgrading the various subcomponents, or even migrating to a different vendor will be a lot easier in the future (and won't affect any of the other projects I have going on).

## Why not just automate the monolith 

The "easy" answer may have been to automate more of my "ball of mud" to address the effort/efficiency of applying security updates.

Yet the "better monolith" would mean I still owned the maintenance and uptime for a large percent of my services.

I appreciate the microservices approach resilience that different providers means it is nearly impossible for them to all go down simultaneously or be affected by one another.

Leveraging other platforms that better fit my use case means I benefit from their expertise and by reducing the moving parts I have a reduced security risk.

My experiments in other frameworks and programming languages were never a good match for my "production" web services.

> "because it's there" or "because I can" are very often the reason things continue to be done in a suboptimal way ;) 

Now I will focus more on the "top" of the tech stack and less on the "how to automate and deploy" portion.

## Ongoing and Future Work

I still have to purchase/renew domains, update DNS, and 
write content.

I still have to eventually find a platform that allows my father-in-law to publish content (and upload files) where I'm not responsible for security patches or backups ;)

My experimenting is now done via a PaaS like Google AppEngine, Heroku, Openshift etc. or using Docker containers.  That means more admin and cognitive sprawl but PaaS and CaaS are more predisposed to version control and elastic/disposable architecture so in all a lot less maintenance.

The biggest new cost is managing the increased number of services but this at least makes explicit what I am working on and is mostly mitigated by automation.
