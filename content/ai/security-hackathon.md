Title: What a Security Hackathon Taught Me About Agents in the Cloud
Date: 2026-03-16 20:20
Tags: ai, hackathon, security

[TOC]

# All you need is Agents and Human intent

Took 3rd place (according to the AI judge) and won the "Scariest" award at the NEBULA:FOG, an AI × Security hackathon in San Francisco on March 14, 2026.

My teammate's genius was giving human intent while 5+ (Claude Opus 4.6) agents did the work in the cloud (they'd melt a laptop). They downloaded the code, built and exercised targets, ran exploits, and auto-generated POC findings with evidence. They even created the presentation.

My role was knowing which tools are widely used in genomics, and observing the future be unevenly distributed. 

*Responsible disclosures in progress!*

# Security has always mattered

The tag line from our presentation was:

> Low priority for scientists, High priority for security

As a teenager reading "The Cuckoo's Egg" by Cliff Stoll, I was inspired by the insights into the earliest days of networked computing and hacking. Systems need to be secure by design, and people have to understand their role for it to work.

Later, Steven Levy's "Crypto: How the Code Rebels Beat the Government, Saving Privacy in the Digital Age" impressed upon me that a single determined person like Whitfield Diffie could democratize privacy through technology. I also learned how the awesome innovation and implementation of asymmetric cipher keys underpins all secure communication and business today.

Add Schneier's principles and systematic thinking on security, Krebs's reporting on the actual threat landscape, and Troy Hunt's work (<https://haveibeenpwned.com/>) making breach data accessible to the public, and you understand the worldview that security is not just a feature, it's a transparent and deliberate foundation.

# How it happened

We focused on key open source projects for genomics. We found a set of vulnerabilities in the tools and dependencies that are hiding in plain sight. They're not a crypto wallet or a bank, but people's genomic information is incredibly private and sensitive.

My teammate's years of experience were distilled into prompts in English, then the AI agents automated everything.

No Burp Suite. No Metasploit. No hand-crafted exploit scripts. Instead we had tea and pizza.

I'm used to running AI on my laptop, often tethered to foundation model vendors.

But I witnessed the future: that many agents working in parallel - they have to run in the cloud.

## Agents in the Cloud

The abstraction pattern: hardware -> hosted infrastructure -> service -> intent-level runtime

**evolution of running code:**

- physical servers in an office *(that you maybe sometimes have to kick into rebooting)*
- data centers ("Colo's") handling the physical stuff *(but you still start with bare metal and remotely install the OS, hopefully with a KVM-over-IP)*
- virtual servers and the rise of VMware *(ok, managing dozens of VMs from templates, with snapshots, isn't so bad... until the over-provisioned host crashes)*
- AWS leading the way in 2006 with "cloud instances" *(API for a server, cattle not pets! new scale, new problems like noisy neighbors and thousands of "machines")*
- PaaS (RIP Heroku) and then FaaS (AWS Lambda): "function as a service" = pure focus on the code

**evolution of running generative AI:**

- [2 physical GPUs proved deep learning scales on Alexnet (Alex Krizhevsky and Ilya Sutskever)](https://papers.nips.cc/paper_files/paper/2012/file/c399862d3b9d6b76c8436e924a68c45b-Paper.pdf)
- Nvidia DGX: GPUs as an appliance aka purpose built hardware for AI, in your datacenter
- Renting GPUs from vendors like AWS (P2), Azure (N-series), Google Cloud (P100)
- "intelligence on demand" from foundation models like OpenAI and Anthropic, albeit a clunky interface
- Agents running "somewhere", taking human intent and just returning results

*now for the fun problems with queuing, orchestration, observability, failure modes...*


## The Results

Those vulnerabilities were real, with evidence for each exploit. We (the humans) had to read the findings to ensure the most critical ones were real.

Note the hackathon judges' reaction — awarding us the "scariest" prize — tells you the severity.

Now the barrier to discovering serious vulnerabilities in critical open source infrastructure just dropped by an order of magnitude.

What previously required deep domain expertise in specific codebases, custom tooling, and hours of manual analysis, can now be directed by someone who understands vulnerability classes and can write clear prompts.

> The economics favor the attacker: they only have to find one exploitable path, defenders have to patch all of them.

# Hackathon Notes

I love hackathons: the ideas and energy, teams coming together, the action of building. "ShipIt" days were highpoints for me at Atlassian.

At Helix I evolved from participant to organizer of a company-wide 100+ person hackathon, including working closely with external guests (doctors/professors/professionals from the Medical University of South Carolina).

Hats off to the NebulaFog organizers/hosts, they created an environment I rarely see at tech events: genuinely high-trust, positive, and kind. Lots of different tracks and challenges. A 13-year-old demo'd and he was amazing.

<https://nebulafog.ai/>

> No pitches. No spectators. A room full of people who ship, learning from each other, forming alliances, stress-testing what's possible.

A perfect situation to connect and learn, I'll keep in touch with folks and be back next year!

