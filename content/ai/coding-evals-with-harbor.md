Title: Reproducing a coding benchmark with Harbor and Terminal Bench 2.1
Date: 2026-07-21 23:59
Tags: ai, agent, evals, benchmark

[TOC]

> Reproducibility is under-appreciated

When you say a bridge is engineered to carry a specified load - you must have reproducible evidence of that claim.

In the era of AI and frenetic change, how to discern "good" among so many new Large Language Models?

New LLM capabilities like "reasoning" or "tool use" become table stakes for the next generation; benchmarks become saturated and older models become obsolete.

Since coding is a concrete way to measure one axis of progress, here's how you can actually test a model with a coding benchmark and an agent (harness).

My step by step approach, leveraging mostly free resources (*~$10 to unlock higher rate limits), allows you to reproduce the findings from the paper: <https://arxiv.org/html/2601.11868v1>

> Then, we benchmark frontier LLMs and agents on the 89 tasks in Terminal-Bench 2.0, and find that frontier models and agents resolve less than 65% of tasks, with smaller models scoring around 15%.

# Results

> tldr: agent harness affects outcomes almost as much as model size, including dramatically reducing time and tokens used

| | North Mini Code + mini-swe-agent | Nemotron 3 Ultra + mini-swe-agent | Nemotron 3 Ultra + terminus-2 |
|------------|------------|------------|------------|
| Result | timeout, reward 0.0 | pass, reward 1.0 | pass, reward 1.0 |
| Steps | 15 (timed out) | 16 (completed) | 5 (completed) |
| Reasoning tokens | 57,735 (96% of output) | 9,894 (40% of output) | ~3,500 (41% of output, estimated) |
| Completion tokens | 59,951 | 24,820 | 8,493 |
| Input tokens | 15,323 | 286,276 | 18,962 |
| Cache hits | 0 | 208,896 (73%) | 4,352 (23%) |
| Time | >15 min (killed) | 12m 30s | 4m 10s |
| Behavior | `grep -R "regex" /` | wrote solution, ran 33 edge cases | analyzed, wrote regex, verified in one shot |


## High Level Diagram

```
┌──────────────┐            ┌─────────────┐   ┌─────────────┐
│  Harbor Hub  │            │  OpenRouter │---> LLM Provider│
│  (dataset)   │            │             │	  │             │
└──────┬───────┘            └──────▲──────┘   └─────────────┘
       │ pull                      │ LLM calls
┌──────┤───────────────────────────┤──────────────────────┐ 
│──────▼───────────────────────────┤────────────────────┐ │
│  Harbor CLI                      │                    │ │
│                                  │                    │ │
│  ┌──────────────────┐   ┌────────┘──────────────┐     │ │
│  │ Docker Container │   │ Agent (Harness)       │     │ │
│  │ (per task)       │◄──│ "mini-swe-agent"      │     │ │
│  └──────────────────┘   └───────────────────────┘     │ │
│                                                       │ │
├───────────────────────────────────────────────────────┤ │
│  jobs/<date-and-time>/<task-id>/                      │ │
│    result.json  trajectory.json                       │ │
│───────────────────────────────────────────────────────┘ │
│ VPS (4CPU - 8GB RAM)                                    │
└─────────────────────────────────────────────────────────┘ 

```

*This is an example minimal size to get started*

## LLM API Key

Bring your LLM provider of choice. *I have no affiliation with OpenRouter, it has a free tier and easy access to a large number of models.*

```bash
export OPENROUTER_API_KEY='sk-...'

curl https://openrouter.ai/api/v1/models | jq > openrouter-models.json

less openrouter-models.json

curl https://openrouter.ai/api/v1/chat/completions   -H "Content-Type: application/json"  \
  -H "Authorization: Bearer $OPENROUTER_API_KEY" \
  -d '{
  "model": "cohere/north-mini-code:free",
  "messages": [
    {
      "role": "user",
      "content": "One sentence explaining coding evals with Harbor and Terminal Bench 2.1?"
    }
  ]
}' | jq

```

<https://openrouter.ai/collections/free-models>

**Disclaimer**: *for some free models routed by OpenRouter, the actual Provider may store and use your data*

## Just a smoke test

First let's see if a suite of simple tasks (bug fixes in code) with a small model and minimal agent works.

`harbor run --dataset humanevalfix --agent mini-swe-agent --model openrouter/cohere/north-mini-code:free --n-concurrent 1`

⠴   0/164 Running trials... ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 0:01:20 -:--:--
⠦ 0:01:08 python-63__futnKyJ: starting environment...

I used OpenRouter's dashboard to watch token consumption:

- At 5 mins had 20 requests for 45k tokens
- At 9 mins had 2 of 164 completed for 39 requests and 140k tokens

In the filesystem you can see a subdirectory created for each task like "python-134" and "python-63":

`ls jobs/2026-07-21__03-45-50/`

```plaintext
config.json
job.log
lock.json
python-134__B5yi6tu
python-63__futnKyJ
result.json
```

`cat jobs/2026-07-21__03-45-50/results.json`

```json
{
...
    "n_total_trials": 164,
    "stats": {
        "n_completed_trials": 3,
        "n_errored_trials": 0,
        "n_running_trials": 1,
        "n_pending_trials": 160,
        "n_cancelled_trials": 0,
        "n_retries": 0,
        "evals": {
            "mini-swe-agent__cohere/north-mini-code:free__humanevalfix": {
...
```

`docker ps -a`

```bash
CONTAINER ID   IMAGE                          COMMAND                  CREATED          STATUS                        PORTS     NAMES
72ef64cd5ccb   python:3.13-slim               "sh -c 'sleep infini…"   35 minutes ago   Up 35 minutes                           analyze-python-30__cejrwg3__a2ojddk__env-main-1
...
````

Stopping the suite rather than running serially through 164 tasks:

`control + c`

> python-16__3Jea2iG: canceling trial; this may take up to a minute...
> ⠴   `6/164` Mean: 0.500 ━╺━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 0:29:30 -:--:--


**HumanEvalFix** was used alongside SWE-bench in SWE-agent's NeurIPS 2024 paper which demonstrated the power of the agent harness compared to just an LLM or an LLM-with-RAG.

- <https://proceedings.neurips.cc/paper_files/paper/2024/hash/5a7c947568c1b1328ccc5230172e1e7c-Abstract-Conference.html>

# Benchmarks

Consider what domain you are interested in using the model for, for instance HumanEvalFix was focused on pure code bug fixing.

A more modern benchmark is **Terminal Bench 2.1** that specifically tests AI agents in terminal environments - like real work =p

Selecting a benchmark means asking:

- how was it designed and constructed? (for which domain: coding, science, math, vision/images, etc)
- - "contamination" or "leaked" benchmarks are ones a new release of models easily get 100%
- - will this benchmark still be relevant a year later?
- is it challenging enough to separate weak models from intermediate and advanced ones?
- Can you run it yourself? What does it require, including costs, to run?
- Is it reputable enough that using it means your results reference something credible?

## Regex Log

I picked a specific task that I can relate to: finding that one log message in a sea of logs!

- <https://www.tbench.ai/benchmarks/terminal-bench-2/regex-log>
- <https://github.com/harbor-framework/terminal-bench-2-1/tree/main/tasks/regex-log>


## Cohere North Mini-Code

Using an open source model focused on coding, a "Mixture of Experts" 30B parameters with just 3B active.

- <https://cohere.com/blog/north-mini-code>
- <https://en.wikipedia.org/wiki/Cohere>
- <https://openrouter.ai/cohere/north-mini-code:free>

**mini-swe-agent** is an open source and minimal agent, often used in published research for benchmarks, <https://github.com/SWE-agent/mini-swe-agent>


`harbor run -d terminal-bench/terminal-bench-2-1 --agent mini-swe-agent --model openrouter/cohere/north-mini-code:free --include-task-name "terminal-bench/regex-log" `


```bash
docker ps -a
CONTAINER ID   IMAGE                          COMMAND                  CREATED         STATUS         PORTS     NAMES
ad18feb94f0d   alexgshaw/regex-log:20251031   "sh -c 'sleep infini…"   2 minutes ago   Up 2 minutes             regex-log__hjz2gsa__env-main-1
```

### Model stuck in a loop

> AgentTimeoutError

Total runtime: 16m 18s, OpenRouter says 14 requests and 88K tokens

`less jobs/2026-07-21__05-21-02/regex-log__uMDx4As/agent/trajectory.json`

``` 
 "final_metrics": {
     "total_prompt_tokens": 15323,
     "total_completion_tokens": 59951,
     "total_steps": 15,
     "extra": {
       "total_reasoning_tokens": 57735
     }
```

The model kept hitting "python: not found" and trying to reinstall python, over and over.

## Nemotron-3-Ultra with mini-swe-agent

**NVIDIA's free endpoint warns**: 'Your use is logged for security purposes and to improve NVIDIA products and services.'

- <https://research.nvidia.com/labs/nemotron/Nemotron-3-Ultra/>


`harbor run -d terminal-bench/terminal-bench-2-1 --agent mini-swe-agent --model openrouter/nvidia/nemotron-3-ultra-550b-a55b:free --include-task-name "terminal-bench/regex-log"`

Sometimes I like to watch the model in realtime by trailing the traces file, seeing each step and reasoning:

`tail -f jobs/2026-07-21__06-18-33/regex-log__Q8Jqf7p/agent/mini-swe-agent.trajectory.json`


The result was successful!

Job Info - Total runtime: 12m 30s

```
"reward_stats": {
                    "reward": {
                        "1.0": [
                            "regex-log__Q8Jqf7p"
                        ]

```

`less jobs/2026-07-21__06-18-33/regex-log__Q8Jqf7p/agent/trajectory.json`

```
"step_id": 15,
"message": "The regex is saved and working correctly. Let me run one more edge case test to ensure robustness.\n",
...
"step_id": 16,
"message": "All 33 edge case tests pass.
...						
  "final_metrics": {
    "total_prompt_tokens": 286276,
    "total_completion_tokens": 24820,
    "total_cached_tokens": 208896,
    "total_steps": 16,
    "extra": {
      "total_reasoning_tokens": 9894
    }
						
```


## Nemotron-3-Ultra with Terminus-2

**Terminus-2** is Harbor's built-in agent, <https://www.harborframework.com/docs/agents/terminus-2>

`harbor run -d terminal-bench/terminal-bench-2-1 --agent terminus-2 --model openrouter/nvidia/nemotron-3-ultra-550b-a55b:free --include-task-name "terminal-bench/regex-log"`


Job Info - Total runtime: 4m 10s
 
```
"reward_stats": {
                    "reward": {
                        "1.0": [
                            "regex-log__GRksoC7"
```

 
```
"step_id": 3,

...
"step_id": 4,
"message": "Analysis: All test cases pass. The regex correctly matches 
...
"step_id": 5, 
 "message": "Analysis: All tests passed, regex is saved in /app/regex.txt, task requirements satisfied.\nPlan: Confirm task completion.",
  "final_metrics": {
    "total_prompt_tokens": 18962,
    "total_completion_tokens": 8493,
    "total_cached_tokens": 4352
  }

``` 

## Non-Determinism

A single run of a model + agent on a task is not sufficient evidence. Since LLMs are non-deterministic, repeated runs even with the exact same environment will produce different traces (and tokens used, steps taken, wall clock time, etc) and sometimes even generate different results.

These particular benchmarks are well designed: even when re-running, the results will consistently cluster, providing confidence in the outcomes.

# Results Analysis

550B parameters and 55B active clearly outperforms 30B parameters with 3B active.

And yet even for Nemotron 3 Ultra, the harness made a difference, 16 steps vs 5 steps:

**mini-swe-agent** exposes a bash tool that takes a single command string and returns its output. 1 tool call per command, then wait for the result, then decide the next command... forced a step-by-step exploration pattern: "which python", ls /app, cat instructions.txt, etc.

**terminus-2** uses keystrokes as its tool as it sends characters to a tmux session. It can and does batch multiple shell commands into a single tool call (write the heredoc and cat to verify in one step). One LLM roundtrip for reasoning through the entire problem, constructing the full regex, writing it out, and verification.

This reproduces the core finding from SWE-agent's NeurIPS 2024 paper: a superior tool interface lets the model do more with fewer roundtrips = a lot more efficiency in both time and tokens.


---


# Appendix

Boring nuts and bolts of setup.

As you scale up testing with concurrency you will naturally want a larger host (more cpu, more ram) and LLM inference capacity (more tokens).

## Troubleshooting Issues

*`harbor run --help` - what does the CLI do?*

> "ApiRateLimitError":

Job Info - Total runtime: 5m 41s

Results written to jobs/2026-07-21__04-33-55/result.json

Debug by looking in the exception.txt and trajectory.json...

```
Command failed
Classified failed command as ApiRateLimitError (pattern: 'rate.?limit')
```

Ran into a ratelimit from OpenRouter free:

- <https://openrouter.zendesk.com/hc/en-us/articles/39501163636379-OpenRouter-Rate-Limits-What-You-Need-to-Know>

**SOLUTION**: have to deposit $10 for credits to unlock higher limits, but by using the free models you can avoid spending those credits


> ValueError: Unknown model: google/gemma-4-31b-it:free

User error, `--model google/gemma-4-31b-it:free` is invalid with the OpenRouter key

**SOLUTION:** the correct name is:  `--model openrouter/google/gemma-4-31b-it:free`


> Provider returned error","code":429

```
RateLimitError: litellm.RateLimitError: RateLimitError: OpenrouterException - 
{"error":{"message":"Provider returned error","code":429,
"metadata":{"raw":"google/gemma-4-31b-it:free is temporarily rate-limited upstream. 
Please retry shortly, or add your own key to accumulate your rate limits: https://openrouter.ai/settings/integrations", 
"provider_name":"Google AI Studio","is_byok":false,"provider_error_code":"429"}},
```

<https://openrouter.ai/google/gemma-4-31b-it:free>

**SOLUTION:** Google AI Studio is not reliable for their free gemma4 offering, attempt using a less popular model and more reliable Provider.


> "AgentTimeoutError": [

Total runtime: 16m 18s, OpenRouter says 14 requests and 88K

```
Exception AgentTimeoutError is in exclude_exceptions, not retrying
Not retrying trial because the exception is not in include_exceptions or the maximum number of retries has been reached
```

**SOLUTION:** The agent failed due to the model's (Cohere: North Mini Code) limitations, try a different model. *This kind of timeout is effectively a "test failed" outcome*.

## Hosting

Launch a VPS with 4 cpu and 8GB RAM, *(usually at most $0.10 per hour and for convenience I used ubuntu 24.04)* 

Or use your own local hardware =]

I caution against running llm-powered agents on your personal laptop/machine (even in Docker) as there are too many risk scenarios from "stuck in a loop consumes all cpu/memory/disk" to reward-hacking.

**Security: ensure you have a firewall with inbound allowing only port 22 for SSH**

### How to connect and download things

*For convenience logged in as root on this ephemeral box ;p*

`ssh -i ~/.ssh/mykey root@192.168.1.123`

To copy files off of the remote box you can use SCP:

`scp -i ~/.ssh/mykey root@192.168.1.123:jobs/2026-07-21__06-55-15/regex-log__GRksoC7/agent/trajectory.json .`

My previous (somewhat dated) notes <https://blog.john-pfeiffer.com/security-encryption-https-openssl-ssh-keygen-vpn-letsencrypt-certbot/#ssh-encryption>

### Increase swap

`free -h`

```bash
               total        used        free      shared  buff/cache   available
Mem:           7.8Gi       395Mi       7.4Gi       968Ki       230Mi       7.4Gi
Swap:          495Mi          0B       4.5Gi
```

Increase swap by 4GB

```bash
swapoff /swapfile
rm /swapfile

fallocate -l 4G /swapfile
chmod 600 /swapfile
mkswap /swapfile
swapon /swapfile


free -h

               total        used        free      shared  buff/cache   available
Mem:            7941         396        7544           0         230        7544
Swap:           4591           0        4591

swapon

	NAME      TYPE      SIZE USED PRIO
	/dev/sdb  partition 496M   0B   -2
	/swapfile file        4G   0B   -3
```


## Install Docker
```bash
sudo install -m 0755 -d /etc/apt/keyrings

sudo curl -fsSL https://download.docker.com/linux/ubuntu/gpg -o /etc/apt/keyrings/docker.asc

sudo chmod a+r /etc/apt/keyrings/docker.asc

sudo tee /etc/apt/sources.list.d/docker.sources >/dev/null <<EOF
Types: deb
URIs: https://download.docker.com/linux/ubuntu
Suites: $(. /etc/os-release && echo "${UBUNTU_CODENAME:-$VERSION_CODENAME}")
Components: stable
Architectures: $(dpkg --print-architecture)
Signed-By: /etc/apt/keyrings/docker.asc
EOF

sudo apt update

sudo apt install -y \
  docker-ce \
  docker-ce-cli \
  containerd.io \
  docker-buildx-plugin \
  docker-compose-plugin
```

`docker info`
`docker compose version`

## Install UV and Harbor

```
curl -LsSf https://astral.sh/uv/install.sh | sh
source $HOME/.local/bin/env
uv tool install "harbor==0.20.0"
harbor --version
```

One of the simplest open standards for running benchmarks (especially with agents)

- <https://github.com/harbor-framework/harbor>
- <https://www.harborframework.com/docs/tasks>
- <https://docs.nvidia.com/nemo-platform/documentation/evaluate-models/agent-eval/harbor-runner>


## Reboot

reboot the VPS, ssh in again, double check the host is on the correct kernel and swap is on

`reboot`

```bash
uname -r  # expecting 6.8.0-136-generic

swapon /swapfile

free -h
```
