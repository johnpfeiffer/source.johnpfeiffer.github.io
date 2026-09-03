Title: Multi-Region Active-Active on AWS in Hours instead of Weeks
Date: 2026-09-02 18:00
Tags: aws, devops, dynamodb, lambda, cdk

[TOC]

# Multi-Region Active-Active on AWS: A POC in Hours, Not Weeks

> The best disaster recovery is the one you build and test before the disaster, not the one still on the whiteboard

## Why

- At Atlassian, and then at Helix, we lived through multiple AWS outages; we were in us-east-1 so we waited patiently (along with many other SaaS/cloud companies)
- The us-east-1 control plane going down can cascade globally — even if your workload runs elsewhere
- Active-active multi-region is a strong answer, but historically it's been weeks of infrastructure work

"AWS Post-Event Summaries": note that often outages in one service cascade into issues in other services or even regions.

- <https://aws.amazon.com/premiumsupport/technology/pes/>
- <https://aws.amazon.com/message/101925/> DynamoDB, Network (Load Balancers), Lambda
- <https://aws.amazon.com/message/12721/> Control Plane
- <https://aws.amazon.com/message/11201/> Kinesis and Cloudwatch
- <https://aws.amazon.com/message/41926/> S3

# The Architecture

```text
Client → www.example.com (DNS)
  → AWS Global Accelerator (anycast static IPs)
    → Private ALB (us-west-2) → Go Lambda → DynamoDB MRSC Global Table
    → Private ALB (us-east-1) → Go Lambda → DynamoDB MRSC Global Table
                                              └── Witness: us-east-2
```

**Key design decisions:**

- **Global Accelerator** as the only public entry point — ALBs are private
- **DynamoDB Multi-Region Strong Consistency (MRSC)** global table with active-active writes with strong consistency, witness region (us-east-2) for quorum
- **Serverless: Lambda in Golang** — minimal cold start, single binary deployment
- **AWS CDK in Go** — infrastructure as code, deterministic deploys
- **HTTPS everywhere** — ACM certs in both regions, TLS terminates at the ALB

*East and West gives you a very large geographic separation, but may also provide lower local latency*

## What's In the Stack

- ACM certificates (one per region)
- Private ALBs with HTTPS listeners in us-west-2 and us-east-1
- Global Accelerator with endpoint groups in both regions (TCP 443 passthrough)
- Go Lambda behind each ALB
- DynamoDB MRSC global table (us-west-2, us-east-1 replicas + us-east-2 witness)
- DNS CNAME (`www` → Global Accelerator)

# LLM-Assisted Development

I oversaw an LLM, pair-programmed it all. I approved and deployed.

- **CDK stack, Lambda code, Makefile** — written by coding agents, every line reviewed by me (a human :)
- - executed the Makefile locally, had it build/leverage the local docker container approach to DynamoDB *(another item forever on my wish list!)*
- **DNS, ACM, Global Accelerator setup** step-by-step guided by an LLM, including debugging cert SANs, DNS propagation, DNS config quirks
- **Total wall-clock time**: hours, not the days/weeks this would have taken reading docs cold and slogging through the mis-steps and misunderstandings

*Agents are great for research and toil*

## Proof It Works

`curl -X POST "https://www.example.com/items"  -H 'Content-Type: application/json' -d '{"id":"demo","seq":1,"payload":"hello"}'`

```shell
{"id":"demo","occurred_at":"2026-09-02T19:16:55Z","seq":1,"payload":"hello","written_in":"us-west-2"}
```

`curl "https://www.example.com/items?id=demo"`

*Authentication elided for brevity*

```shell
{"count":1,"items":[...],"region":"us-west-2"}
```

The `written_in` and `region` fields prove which region handled the request and Global Accelerator routes to the nearest healthy endpoint.


## Deeper on DynamoDB and Strong Consistency

Multi-region strong consistency is a hard problem that's nice as a managed product/service feature. (DynamoDB MRSC)

<https://aws.amazon.com/blogs/aws/build-the-highest-resilience-apps-with-multi-region-strong-consistency-in-amazon-dynamodb-global-tables/>

Traditional global tables (MREC) replicate asynchronously — fast writes, but if a region dies, recent writes might be lost (non-zero RecoveryPointObjective). MRSC changes the deal: a write must be durably committed to at least 2 of 3 regions before it's acknowledged. This gives you zero RPO, but adds cross-region latency to every write and strongly consistent read.

An example latency tradeoff for your regions (~P50 data)

us-west-2 <-> us-east-1: ~65ms RTT
us-west-2 <-> us-east-2: ~55ms RTT
us-east-1 <-> us-east-2: ~15ms RTT

So for MRSC writes, expect roughly:

Write from us-east-1: fast — quorum partner us-east-2 is only ~13ms away
Write from us-west-2: slower — nearest quorum partner (us-east-2) is ~53ms away

Eventually consistent reads remain local-speed (single-digit ms). Strongly consistent reads also pay the cross-region heartbeat cost.

The witness region (us-east-2) is clever as it participates in quorum but doesn't serve traffic, so you don't pay for a full third replica. Placing it near us-east-1 means east-coast writes get a fast quorum partner.

*Key constraints: exactly 3 regions, no transactions API, can't change consistency mode after creation.*


# Next Steps

- **Failure simulation**: kill a health check, verify GA routes 100% to the surviving region
- **Deeper health checks**: Lambda health endpoint that verifies DynamoDB connectivity, not just Lambda liveness
- **Simulate DynamoDB regional failure**: prove the witness region enables the remaining replica to continue serving strong-consistency reads
- **Latency measurement**: compare single-region vs. GA-routed multi-region from different geographies

# Resources

- <https://github.com/johnpfeiffer/multiregion> (the source code)
- <https://docs.aws.amazon.com/global-accelerator/latest/dg/about-endpoints.html>
- <https://docs.aws.amazon.com/elasticloadbalancing/latest/application/introduction.html>
- <https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/GlobalTables.html>
- <https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/DynamoDBLocal.DownloadingAndRunning.html>
