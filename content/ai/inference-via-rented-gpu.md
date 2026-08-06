Title: Beyond the ratelimit - hosting the model yourself on a GPU with vLLM
Date: 2026-07-31 08:08
Tags: ai, inference, benchmark, gpu

[TOC]

# Findings

A single A100 with 80GB VRAM running Gemma4 31B with vLLM sustained 138 output tokens per second (serving 8 concurrent client agents). *(extrapolates to a ceiling of ~500k tokens per hour)*

The bottleneck to more parallelism is the amount of VRAM available for KV cache; the model took roughly 60 GB of VRAM in BF16, with ~14 GB for vLLM runtime overhead and KV cache. *(10 agents achieved 160 tokens per second - but also pushed to 87% of KV.)*

So why/when would I prefer renting a GPU that costs more even when fully utilized, where I pay even when it's idle?

**Running specific configs like quantized or custom models, no mystery ratelimit, data remains in infra you control... with predictable spend.**

## Diagram

```
A100 GPU with vLLM (127.0.0.1:8000)
    |
    |
SSH local tunnel
    |
	|
Harbor agents on a VPS -> http://127.0.0.1:18000/v1
```


# API vs Buy Server vs Rent GPUs

APIs look like a fixed price where someone else handles the hardware/infrastructure complexity.

Some real downsides I've seen are ratelimits, intermittent failures, outages, breaking API changes, and surprise large bills. *And there's the opacity of exactly what they do with your data.*

At the other end of the spectrum is buying and operating a GPU server which provides maximum control, but requires substantial capital, specialized operational knowledge, and enough sustained use to justify owning hardware that depreciates quickly.

Some less obvious downsides are: hardware availability, finding a place to run the server that's secure, with cheap electricity in the KWs, and liquid cooling!

The pragmatic compromise: rent GPUs on demand.

*Similar pros and cons of cloud servers vs colocated datacenters: convenience vs cost, how much expertise is needed versus how much control you need/get.*

The right answer is always **it depends**.

# Here to Learn

> Learning how it works is something you get to keep

Even if you bought the hardware, having a software abstraction layer above the hardware and loose coupling makes sense.

Understanding how cloud inference providers actually operate their APIs can give you better insights into failure modes and best practices as an end user managing workloads.


# API superiority

I used a deliberately biased comparison: Cerebras offer some of the fastest inference available, 35x faster than other APIs on Gemma 4.

It only took ~3 mins to run a single harbor terminal-bench-2.1 task (regex-log), most of the time was taken up by Harbor's setup and verification. You only pay for an API when you use it: I ran 8 concurrently, and theoretically can go as parallel as my budget allows.

Specifically for Cerebras, with its specialized feature of low latency, it's $.99 per M input tokens and $1.49 per M output tokens. *(Usually Gemma4 costs about $0.40 per million output tokens)*

Yet cost is only a single dimension. When a 429 ratelimit kicked in - I'm not in control. The vendor answer makes sense: prevent runaway issues running up huge bills, prevent bad actors from consuming all of the resources. *Just create another API key, pay for a higher limit.*

And with an API vendor, they decide which models to offer, and tomorrow they could decide to remove the one you depend on.

# Agents demand more inference

> Interactive chat < agentic coding < many agents in parallel

Agentic workflows, Evals, and removing the "human in the loop" unlocks exponentially more need for inference.

Paying per token became fuzzy math: input vs output tokens, invisible thinking tokens, and more tokens needed to accomplish a task.

And when agents get stuck going in a circle or Loops that don't converge, failure is even more costly.

This is not new: cost over-runs were a regular challenge of early (~2010s) cloud adoption, and I've personally seen shocking cloud bills in 2026. Amazon even have a special support request for "huge accidental charges".


# Privacy and Predictable Spend
If the data the agents are working on has strict privacy and confidentiality requirements, you may not be able to use most LLM API vendors.

GPU rental solves it for a known price.

At $1.09 per hour for an A100 with 80GB of VRAM, full utilization (500k tokens per hour) for 2 hours costs $2.18 for a million output tokens.

The API cost is less, maybe $1 (from a blended rate of input, reasoning, and output tokens).

The difference is what you get for the money: any model you want, any configuration, no ratelimit, and a bill you can predict before you start.

*The tradeoff is real: you own the ops. A misconfiguration can cause the server to OOM and lose the work in flight.*

*If you need a single agent to run faster than 20 tokens per second, then you need more hardware speed (GB/s) or Quantization or even speculative decoding*

When the workload needs a specific model or config that isn't offered, or is heavy enough to trigger limits, having the know-how to rent a GPU and manage it yourself gives you a solution.

Walk through the full setup step by step in the Appendix =)

# Appendix and Methodology

*all IP addresses are fictional - replace with your real values*

## Harbor Terminal 2.1 Benchmark

Harbor is a well respected, widely adopted, agentic benchmark framework that's open source and used by frontier labs.

For comparing APIs to vLLM on GPUs, Harbor acts as proxy for agents making varied LLM calls over time.

As an open standard, well structured to ramp up real world challenges for LLMs, it makes findings both applicable and reproducible. And the framework also provides a simple way to scale up load in parallel. Also, the standardized format of results provides an easy way to inspect start and end times, agent trajectories.

Useful side-effect is more data (and a methodology) on specific models that we're interested in. Direct observations on how they actually performed on a known benchmark.

- <https://www.harborframework.com/docs>
- <https://artificialanalysis.ai/evaluations/terminalbench-v2-1>
- <https://blog.john-pfeiffer.com/reproducing-a-coding-benchmark-with-harbor-and-terminal-bench-21/>

*Terminal Bench 2.1 is 89 tasks. If they all ran serially until before the framework's max timeout of 15 mins = ~22.25 hours.*

**Quick Analysis**

With the weights loaded and taking VRAM, KV quickly becomes the bottleneck for concurrency.

A nuance: 8 short agent trajectories may use less KV than 4 long trajectories (where the prompt accumulates more and more context over the turns).

## Evaluating Renting GPUs

Critical thinking is needed for careful vendor analysis: what specifically do you need, what exactly are they offering?

1. Control - what configurations can you modify
2. Stable and Predictable - both in their product and in their pricing
3. Transparency - how it is setup, and metrics on how it's operating

*During the transition from magnetic disks to solid-state-drives (SSD) I learned to depend on their interface/drivers, but to run the benchmarks myself.*

And similarly we've seen this when everyone was learning to adopt the cloud (examples from Netflix):

- <https://netflixtechblog.com/5-lessons-weve-learned-using-aws-1f2a28588e4c>
- <https://www.brendangregg.com/Slides/AWSreInvent2017_performance_tuning_EC2.pdf>

## ThunderCompute GPU rental

> ~10 mins from server launch to serving an LLM

*I have no connection to Thundercompute, just a simple place to create an account and pre-pay for credits, "Instances and snapshots are automatically deleted if your balance reaches $0"*

- create and provide an SSH key
- Use the UI to launch a single A100 with the default 64GB RAM and 100GB disk
- copy the IP address of the newly launched box

`ssh ubuntu@192.168.1.111 -p 34567 -i ~/.ssh/MYKEY`

*Tip of the hat to default security by obscurity random ssh port number*

To be clear:

```
VM with CPU and RAM
   |
   | ThunderCompute network/proxy transport
   v

remote A100 VRAM
```

*This means changing models or transferring to the GPU will take time*

### Install UV and vLLM and HuggingFace
```
sudo su # slightly unsafe but conveniently fast
apt update && apt install -y byobu

curl -LsSf https://astral.sh/uv/install.sh | sh
source $HOME/.local/bin/env

uv tool install huggingface-hub 
uv tool install vllm

```

### Download the Model Weights
```
hf download google/gemma-4-31B-it
ll /root/.cache/huggingface/hub/

du -sh /root/.cache/huggingface/hub/models--google--gemma-4-31B-it/
	59G     /root/.cache/huggingface/hub/models--google--gemma-4-31B-it/
```

*actually only took about 3 mins*  <https://huggingface.co/google/gemma-4-31B-it>

### vLLM serving

> as simple as one long command

```
VLLM_USE_V2_MODEL_RUNNER=0 uv tool run vllm serve google/gemma-4-31B-it \
  --dtype bfloat16 \
  --max-model-len 16384 \
  --gpu-memory-utilization 0.92 \
  --enable-auto-tool-choice \
  --reasoning-parser gemma4 \
  --tool-call-parser gemma4 \
  --default-chat-template-kwargs '{"enable_thinking":true}' \
  --limit-mm-per-prompt '{"image":0,"audio":0}' \
  --host 127.0.0.1 \
  --port 8000
```

- *preferred the VLLM V1 model runner as a stable baseline*
- *vLLM resolves google/gemma-4-31B-it , the capital B matters, against the local HF cache before hitting the network*
- constrain a single request to at most 16k tokens (prompt + generated)
- **security** *note: local binding to 127.0.0.1*
- enable "Reasoning"
- disabled the multimodal (image and audio) capabilities

*maybe the agent, with thinking disabled, would have performed better (used less tokens to fail faster)*

> Verify that it is successful locally 

`curl -s localhost:8000/health -o /dev/null -w '%{http_code}\n'` = *200*

`curl -s localhost:8000/v1/models`

```
{"object":"list","data":[{"id":"google/gemma-4-31B-it",...
```

*When you are finally done just delete the box to stop the per minute charges.*

## Linode
Linode 8GB with Harbor setup: <https://blog.john-pfeiffer.com/reproducing-a-coding-benchmark-with-harbor-and-terminal-bench-21/#install-docker>

`apt install -y autossh`

*ensure the MYKEY ssh key for ThunderCompute is put onto the Linode box, and `chmod 400 /root/.ssh/MYKEY`*

**Why an external benchmark box?**

- the same starting point for comparisons to running Harbor with API
- not as operationally sound or supported to run "docker in docker" for Thundercompute (or any GPU provider)
- network latency (milliseconds) was negligible as a factor compared to LLM response times (seconds to minutes)
- real world usage will be from "a server somewhere over a network"

###  SSH tunnel

Verify you can connect to the GPU host box:

`ssh -i /root/.ssh/MYKEY  ubuntu@192.168.1.111 -p 34567`

*(accept the unknown fingerprint)*

Setup a more resilient tunnel with **autossh**:

```
autossh -M 0 -f -N -T \
  -o ExitOnForwardFailure=yes -o ServerAliveInterval=30 -o ServerAliveCountMax=3 -o Compression=no \
  -L 127.0.0.1:18000:127.0.0.1:8000 \
  -p 34567 -i /root/.ssh/MYKEY ubuntu@192.168.1.111


ss -ltnp | grep ':18000'
```

*security note: local binding to 127.0.0.1*

### Verify the SSH tunnel to vLLM

`curl -s http://127.0.0.1:18000/v1/models | jq`

```
{"object":"list","data":[{"id":"google/gemma-4-31B-it",...
```

**Initial metrics before testing** with `curl -s http://127.0.0.1:18000/metrics > vllm-before.log`

*The metrics are cumulative so you could consider offloading them if you want to disaggregate.*

After done with all testing get the stats: `curl -s http://127.0.0.1:18000/metrics > vllm-after.log`

*To download results to your local machine afterwards:*
`scp -i ~/.ssh/MYKEY root@192.168.2.222:/jobs .`


An alternative one-off way to load test:

```
seq 1 32 | xargs -P32 -I{} curl -s -o /dev/null -w '%{time_total}\n' \
  http://127.0.0.1:18000/v1/completions -H 'Content-Type: application/json' \
  -d '{"model":"google/gemma-4-31B-it","prompt":"write 3 long detailed paragraphs about a random animal","max_tokens":4096}' | sort -n
```

### Run The Harbor Benchmark

`export OPENAI_API_KEY=dummy`

`export OPENAI_BASE_URL=http://127.0.0.1:18000/v1`

```
harbor run -d terminal-bench/terminal-bench-2-1 --agent terminus-2 \
  --model openai/google/gemma-4-31B-it \
  --include-task-name terminal-bench/regex-log -k 8 -n 8
```
 
It worked, started producing the result.json with tasks running and eventual successes and fails.


Via vLLM verifying the agent requests and token generation stats:

```
curl -s http://127.0.0.1:18000/metrics | grep 'request_success_total'
	vllm:request_success_total{engine="0",finished_reason="stop",model_name="google/gemma-4-31B-it"} 19.0
	vllm:request_success_total{engine="0",finished_reason="length",model_name="google/gemma-4-31B-it"} 96.0

curl -s http://127.0.0.1:18000/metrics | grep 'tokens_sum'
	vllm:request_prompt_tokens_sum{engine="0",model_name="google/gemma-4-31B-it"} 50222.0
	vllm:request_generation_tokens_sum{engine="0",model_name="google/gemma-4-31B-it"} 27900.0
	vllm:request_max_num_generation_tokens_sum{engine="0",model_name="google/gemma-4-31B-it"} 27900.0
	vllm:request_params_max_tokens_sum{engine="0",model_name="google/gemma-4-31B-it"} 257100.0
	vllm:request_prefill_kv_computed_tokens_sum{engine="0",model_name="google/gemma-4-31B-it"} 17646.0
```

### Tokens Per Second and KV Usage

From the vLLM streaming logs:

```
> 20 tokens per second

harbor run -d terminal-bench/terminal-bench-2-1 --agent terminus-2   --model openai/google/gemma-4-31B-it  -k 1 -n 1  --include-task-name "terminal-bench/regex-log"

(APIServer pid=11745) INFO 08-01 19:16:16 [loggers.py:310] Engine 000: Avg prompt throughput: 0.0 tokens/s, Avg generation throughput: 20.0 tokens/s, Running: 1 reqs, Waiting: 0 reqs, GPU KV cache usage: 10.9%, Prefix cache hit rate: 0.6%

> 40 tokens per second

harbor run -d terminal-bench/terminal-bench-2-1 --agent terminus-2   --model openai/google/gemma-4-31B-it  -k 1 -n 1  --include-task-name "terminal-bench/regex-log"

(APIServer pid=11745) INFO 08-01 19:29:26 [loggers.py:310] Engine 000: Avg prompt throughput: 0.0 tokens/s, Avg generation throughput: 40.8 tokens/s, Running: 2 reqs, Waiting: 0 reqs, GPU KV cache usage: 16.6%, Prefix cache hit rate: 0.7%

> 76 tokens per second (4 parallel)

harbor run -d terminal-bench/terminal-bench-2-1 --agent terminus-2   --model openai/google/gemma-4-31B-it  -k 2 -n 2  --include-task-name "terminal-bench/regex-log"

(APIServer pid=11745) INFO 08-01 19:32:56 [loggers.py:310] Engine 000: Avg prompt throughput: 0.0 tokens/s, Avg generation throughput: 76.4 tokens/s, Running: 4 reqs, Waiting: 0 reqs, GPU KV cache usage: 34.9%, Prefix cache hit rate: 0.8%

> 108 tokens per second (6 parallel)

harbor run -d terminal-bench/terminal-bench-2-1 --agent terminus-2   --model openai/google/gemma-4-31B-it  -k 2 -n 2  --include-task-name "terminal-bench/regex-log"

(APIServer pid=11745) INFO 08-01 19:37:26 [loggers.py:310] Engine 000: Avg prompt throughput: 0.0 tokens/s, Avg generation throughput: 108.0 tokens/s, Running: 6 reqs, Waiting: 0 reqs, GPU KV cache usage: 52.7%, Prefix cache hit rate: 0.9%

> 138 tokens per second (8 parallel)

(APIServer pid=11745) INFO 08-01 19:44:06 [loggers.py:310] Engine 000: Avg prompt throughput: 0.0 tokens/s, Avg generation throughput: 138.4 tokens/s, Running: 8 reqs, Waiting: 0 reqs, GPU KV cache usage: 70.6%, Prefix cache hit rate: 1.1%

> 160 tokens per second (10 parallel)

(APIServer pid=11745) INFO 08-01 19:47:46 [loggers.py:310] Engine 000: Avg prompt throughput: 0.0 tokens/s, Avg generation throughput: 160.0 tokens/s, Running: 10 reqs, Waiting: 0 reqs, GPU KV cache usage: 87.3%, Prefix cache hit rate: 1.3%
```

`curl -s http://127.0.0.1:18000/metrics > vllm-after.log`


### Quick Server Diagnostics

On the GPU host, confirm the linux kernel, the available memory, and the Nvidia stats:

```
uname -a ; free -m
	64  GB RAM
```

`nvidia-smi`

```plaintext
| NVIDIA-SMI 610.43.02              KMD Version: 610.43.02     CUDA UMD Version: 13.3     |
+-----------------------------------------+------------------------+----------------------+
| GPU  Name                 Persistence-M | Bus-Id          Disp.A | Volatile Uncorr. ECC |
| Fan  Temp   Perf          Pwr:Usage/Cap |           Memory-Usage | GPU-Util  Compute M. |
|                                         |                        |               MIG M. |
|=========================================+========================+======================|
|   0  NVIDIA A100-SXM4-80GB          Off |   00000000:9D:00.0 Off |                    0 |
| N/A   33C    P0             70W /  500W |       4MiB /  81920MiB |      0%      Default |
|                                         |                        |             Disabled |
```

`python3 --version && pip --version`

```
Python 3.12.13
pip 26.1.2 from /usr/local/lib/python3.12/dist-packages/pip (python 3.12)

python3 -c "import torch; print(torch.__version__, torch.version.cuda, torch.cuda.is_available(), torch.cuda.get_device_name(0))" 2>/dev/null || echo "no torch"

2.12.1+cu130 13.0 True NVIDIA A100-SXM4-80GB
```


*the nvidia-smi is not that useful for realtime stats, but watts used does correlate to load*

```
watch -n 1 \
'nvidia-smi --query-gpu=timestamp,name,utilization.gpu,utilization.memory,memory.used,memory.total,power.draw,temperature.gpu --format=csv,noheader'


2026/08/01 18:51:16.773, NVIDIA A100-SXM4-80GB, 92 %, 82 %, 75351 MiB, 81920 MiB, 312.13 W, 59
```

# References

**vLLM** <https://en.wikipedia.org/wiki/VLLM> , <https://github.com/vllm-project/vllm>


**Thundercompute**

> Instead of reserving a GPU, cloud instances on Thunder Compute share a pool of network-attached GPUs.

More details: <https://www.thundercompute.com/blog/how-thunder-compute-works-gpu-over-tcp>

Thunder A100-SXM4-80GB , $1.09/hr

*(Note that a Linode box was $.07 per hour, 1/10th the cost of these very in-demand GPUs)*

