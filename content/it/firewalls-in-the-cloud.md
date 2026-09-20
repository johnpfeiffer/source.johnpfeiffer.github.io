Title: Firewalls in the cloud
Date: 2023-02-26 21:21
Tags: network, security, firewall, cloudflare

[TOC]

System Administrators, Network Administrators, and Ops all know 1 truth: if you have a resource on the network, eventually it will be overwhelmed by traffic.

If your server only has a fixed quota or limited amount of network capacity, or you pay for network transfer, attackers can download enough to bankrupt your bandwidth budget.

Even for a simple website with static content, bad actors can "denial of service" your system, saturating your server or network until it can no longer function.

This was one of the reasons I eventually moved my static blog to be distributed by Cloudflare, to not have to think about network traffic and security. Even with that foundation, you still make configuration/policy decisions. And there are a spectrum of tools and approaches, from blunt to surgical, that can help you keep your system alive and usable.

# It happens

Personally I have had to protect a box and keep it up by simply blocking whole IP address ranges. Knowing that none of our customers or employees would be in a certain country, but that country had a disproportionately large number of probes and malicious network traffic, meant it was pragmatic to just block all inbound requests from that range of IP Addresses.

Specifically at work, during security incidents, I have also blocked specific suspicious ip addresses that were in the logs. This firewall level control disrupted their attack while patches, resets, and other hardening efforts were put in place. 

## Before you block anything - the obvious mistake

> One thing that happens to everyone as they lock things down - to lock yourself out!

That moment when you lose access and realize that your ip address is in the group that the firewall is now blocking =|

This sometimes happens when you start over-zealous and decide to use the best practice of whitelists, so you "block everything by default"... before your own addresses are whitelisted.

It can happen over time if you only whitelisted a few IP addresses, and then your IP address changes.

The main mitigations are:

- separate the control of configuring the security from the resources being secured
- have physical control or an out-of-band way to reset the configuration
- have tiered levels of restrictions: only a few areas are outright blocked, whereas others are only rate limited
- have certain short windows of time where you temporarily allow access to the configuration

For more in the weeds details about directly managing a linux firewall see my previous article: <https://blog.john-pfeiffer.com/firewall-iptables-ufw-ssh-https-nat-forwarding-redirect/>

# The basics of Assigning IP Addresses and Network Ranges

The "inter-network" is fundamentally communication between a client with a unique address and a server with a specific address. You may have seen in your network a local device, like a printer, at 192.168.1.10, and your computer at 192.168.1.11.

- Your operations team or network admins are (with hardware and software devices like Routers) ensuring every connected device gets a unique address
- Organizations get blocks of usable (not-already-reserved) addresses from their ISP/Telcos; or more currently hosting/cloud providers - the natural monopoly and distribution through those with (physical) infrastructure
- Internet Service Providers, Telecommunication Providers, and Cloud Providers get assigned blocks of addresses to manage from a "Regional Internet Registry"

IP Addresses are globally allocated by region ("continent-ish")

- <https://en.wikipedia.org/wiki/Regional_Internet_registry>
- <https://www.nro.net/about/rirs/>
- <https://www.ripe.net/about-us/press-centre/understanding-ip-addressing/>

# Brute force defense - blocking by IP Addresses

So everyone comes from somewhere - maybe some places have a very high percent of risky or problematic traffic.

The blunt approach means a few simple techniques and most of your headache goes away. It also means some good traffic may get blocked too.

## Blocking a specific area

Because large address blocks rarely get reassigned, there is a strong correlation between the virtual (IP) address and physical location. 

Here's some examples for looking up large swathes of addresses by country:

- <https://www.nirsoft.net/countryip/ru.html>
- <https://lite.ip2location.com/ip-address-ranges-by-country>

*It is through this system of assignments that common website traffic analytics dashboards can show you X% of visitors from a specific country.*

At the firewall level (or even at the network routing level), now that you know "who/what", you can configure your system to block traffic originating from that IP range (ergo geography). <https://en.wikipedia.org/wiki/Geo-blocking>


## Cloudflare IP access rules

*This IP Address based control  may have been discontinued or merged into Security Rules*

From the [Cloudflare dashboard](https://dash.cloudflare.com/), click on Compute -> Workers & Pages -> select the application

*Alternatively you may click on "Domains" and select the specific one*

Security -> Security Rules

# Blocking by ASN

A more targeted place of control can be the Autonomous System Number

- <https://www.arin.net/resources/guide/asn/>
- <https://radar.cloudflare.com/routing/as132203>


Cloudflare Security -> Security Rules -> Create Rule -> Custom Rules

```
Field: AS Num 
Operator: equals or in
Value: as132203
Action: Block
Status: Active
```
> Using this technique dropped undesirable traffic of 10k requests and 100MB per minute down to zero

## Surgical Use of Blocking

Blocking a whole hosting company like OVH, GCP, or AWS can have serious consequences for your web traffic. 

Consider 

# Polite Blocking with Robots txt

**robots.txt** is a venerable standard, emblematic of an earlier, more trusting internet. <https://en.wikipedia.org/wiki/Robots.txt>

Web crawlers (think Google's bot) would theoretically not scrape and index your website.

My previous article <https://blog.john-pfeiffer.com/attack-of-the-spiders-bots-and-crawlers/>

## Blocking AI Crawlers

*2024 addendum*

With the rise of AI crawlers there is a new kind of traffic that drains resources and clogs your logs and analytics.


If the agent comes from IP address blocks or regions (ASN) you do not want to block outright, and of course if the agent is honest enough to self-disclose and obey:

<https://developers.cloudflare.com/waf/tools/user-agent-blocking/>

People try to catalog all of the AI agents and crawlers and scrapers: <https://github.com/ai-robots-txt/>

<https://blog.cloudflare.com/declaring-your-aindependence-block-ai-bots-scrapers-and-crawlers-with-a-single-click>


