Title: Getting stable with DeepSeek-V4-Flash-0731 on a single Nvidia B300
Date: 2026-08-04 15:00
Tags: inference, benchmark, open weight

[TOC]

# Findings

**DeepSeek-V4-Flash-0731 runs fast on a single B300.**

> I spent $40 to learn, so you don't have to!

There is a reproducible issue with "Breakable CUDA Graph" enabled that causes a FlashMLA/TMA assertion and crash *(triggered by my usual 8 harbor agents on regex-log)*

Workaround was to disable the Breakable CUDA Graph `VLLM_USE_BREAKABLE_CUDAGRAPH=0`

Good:

- Nvidia B300 with **DeepSeek V4 Flash 0731** handled 8 concurrent agents without breaking a sweat
- - **55 tokens per second, per agent**
- Prefix cache ~92% = can double output to 880 t/s
- - FULL + PIECEWISE graph capture, and DSpark graph capture

**Other Gotchas**:

- I needed to build locally deepGEMM
- watching JIT compile and no change in the logs for 10+ mins can be unnerving
- Seeing *TileLang compile* in the logs means you should consider manually sending representative traffic to warm caches


## Why DeepSeek V4 Flash 0731 and Nvida B300

> The 155 GiB checkpoint fits in the VRAM with ~87 GiB left for KV cache

**DeepSeek-V4-Flash-0731** is the latest in a series of open weights model to drop, and it promises close to frontier performance at an incredibly low price/size.

They use a series of advanced techniques like "Mixture of Experts", speculative decoding, and others to achieve this.

The **Nvidia B300** is the latest in the Blackwell architecture, and its native FP4 support with 288 GB of HBM3e memory (VRAM) are just large enough to run frontier-scale open models (eliminates the complexity of multi-GPU parallelism).



<https://feneky.com/benchmarks>

If you happen to use runpod, you can use my code: <https://runpod.io?ref=hvmpumdd>

*You will get from Runpod "A one-time credit from $5" when you add $10 for the first time, I will also receive extras from Runpod*

## The configuration that works

I successfully adapted it for a single B300 with the following (full explanation in the appendix):

```
export VLLM_USE_DEEP_GEMM=1
export VLLM_USE_BREAKABLE_CUDAGRAPH=0

vllm serve /MODELS/DeepSeek-V4-Flash-0731 \
  --served-model-name deepseek-v4-flash-0731 \
  --host 127.0.0.1 --port 8000 \
  --max-model-len 65536 \
  --tokenizer-mode deepseek_v4 \
  --reasoning-parser deepseek_v4 \
  --tool-call-parser deepseek_v4 \
  --enable-auto-tool-choice \
  --trust-remote-code --kv-cache-dtype fp8 --block-size 256 \
  --enable-expert-parallel \
  --attention-config '{"use_fp4_indexer_cache": true}' \
  --speculative-config '{"method":"dspark","num_speculative_tokens":7,"draft_sample_method":"greedy"}' \
  2>&1 | tee /workspace/vllm-warmup.log
```

*`--enforce-eager` is also even more conservative and "safe"*


DeepSeek recommend, when using 4x B300s <https://huggingface.co/deepseek-ai/DeepSeek-V4-Flash-0731#how-to-run-with-vllm>:
<details>

```
vllm serve deepseek-ai/DeepSeek-V4-Flash-0731 \
  --trust-remote-code --kv-cache-dtype fp8 --block-size 256 \
  --data-parallel-size 4 --enable-expert-parallel \
  --moe-backend deep_gemm_mega_moe \
  --attention-config '{"use_fp4_indexer_cache": true}' \
  --speculative-config '{"method":"dspark","num_speculative_tokens":7,"draft_sample_method":"greedy"}'
```

The `--data-parallel-size 4` only makes sense if you have four B300s.
</details>


### Explanations of flags

What works:

- native FP4/FP8 checkpoint
- DeepGEMM
- expert parallel enabled
- FP4 indexer cache
- DSpark enabled



| Flag | Description |
|------|----------------------|
| `--served-model-name deepseek-v4-flash-0731` | Model name exposed through the API |
| `--host 127.0.0.1` | **Security**: listen only on localhost |
| `--port 8000` | HTTP server port |
| `--max-model-len 65536` | Maximum context window (input + output tokens) per request |
| `--tokenizer-mode deepseek_v4` | Use DeepSeek-V4 tokenizer/chat formatting |
| `--reasoning-parser deepseek_v4` | Parse DeepSeek reasoning output into structured API fields |
| `--tool-call-parser deepseek_v4` | Parse DeepSeek-native tool calls into OpenAI tool calls |
| `--enable-auto-tool-choice` | Allow the model to automatically decide whether to call tools |
| `--trust-remote-code` | *Insecure:* Execute custom model code from the Hugging Face repository |
| `--kv-cache-dtype fp8` | Store the KV cache in FP8 to reduce memory usage |
| `--block-size 256` | Allocate KV cache in 256-token pages |
| `--enable-expert-parallel` | Distribute MoE experts across GPUs instead of tensor-splitting them |
| `--attention-config '{"use_fp4_indexer_cache": true}'` | Enable FP4 compressed attention index cache to reduce memory/bandwidth |
| `--speculative-config '{"method":"dspark","num_speculative_tokens":7,"draft_sample_method":"greedy"}'` | Enable DSpark speculative decoding with a 7-token draft window |


*considered but not used    --moe-backend deep_gemm_mega_moe , --enforce-eager (for safe compatibility)*



## GOTCHAS

> If you "migrate your pod" it auto-starts

So if you're not there when it's completed, then you can burn through your credit balance.


> If you change a flag or config you may re-trigger auto-tuning which eats ~5 to 10 mins

If for instance "Breakable CUDA graphs" auto-tunes but then crashes, so then you launch with `VLLM_USE_BREAKABLE_CUDAGRAPH=0` , yup it will auto-tune again.


> Sparse Attention Indexer CUDA op requires DeepGEMM support

```
(EngineCore pid=23360) INFO 08-04 18:50:10 [quant_config.py:75] DeepSeek V4 expert_dtype resolved to 'fp4'
(EngineCore pid=23360) WARNING 08-04 18:50:10 [import_utils.py:408] Module vllm.third_party.deep_gemm was found but failed to import
```

> actively compiling GPU kernels with ptxas -arch sm_103a

The log looks very slow but... this is fine:

```
(EngineCore pid=69594) 2026-08-04 19:20:05,325 - INFO - cubin_loader.py:84 - flashinfer.jit: Acquired lock for /root/.cache/flashinfer/cubins/481dce07c89a216cbfd18cf39de49a82d40739a8/batched_gemm-dd6d23e-721ae60/include/trtllmGen_bmm_export/trtllm/gen/SparsityDecl.h
(EngineCore pid=69594) 2026-08-04 19:20:05,510 - INFO - cubin_loader.py:114 - flashinfer.jit: File downloaded successfully: https://edge.urm.nvidia.com/artifactory/sw-kernelinferencelibrary-public-generic-local/481dce07c89a216cbfd18cf39de49a82d40739a8/batched_gemm-dd6d23e-721ae60/include/trtllmGen_bmm_export/trtllm/gen/SparsityDecl.h -> /root/.cache/flashinfer/cubins/481dce07c89a216cbfd18cf39de49a82d40739a8/batched_gemm-dd6d23e-721ae60/include/trtllmGen_bmm_export/trtllm/gen/SparsityDecl.h


root@2d6c42f12b28:/# ps -eo pid,pcpu,pmem,etime,cmd --sort=-pcpu | head
    PID %CPU %MEM     ELAPSED CMD
  69594 1261  0.1       12:51 VLLM::EngineCore
 104433  100  0.0       01:41 ptxas -arch sm_103a -m64 /tmp/tmpxft_000164dc_00000000-6_trtllm_fused_moe_routing_custom.ptx -o /tmp/tmpxft_000164dc_00000000-8_trtllm_fused_moe_routing_custom.cubin
  68524  3.6  0.0       13:06 /MODELS/.venv/bin/python3 /MODELS/.venv/bin/vllm serve /MODELS/DeepSeek-V4-Flash-0731 --served-model-name deepseek-v4-flash-0731 --host 127.0.0.1 --port 8000 --trust-remote-code --kv-cache-dtype fp8 --block-size 256 --enable-expert-parallel --attention-config {"use_fp4_indexer_cache": true} --speculative-config {"method":"dspark","num_speculative_tokens":7,"draft_sample_method":"greedy"}
   1784  0.9  0.0       52:53 tmux -u -2 -f /usr/share/byobu/profiles/tmuxrc new-session -n - /usr/bin/byobu-shell
 108873  0.1  0.0       00:24 sshd: root@pts/4
      1  0.0  0.0       55:16 /sbin/docker-init -- /start.sh
    655  0.0  0.0       55:15 /bin/bash /start.sh
    668  0.0  0.0       55:15 nginx: master process /usr/sbin/nginx
    669  0.0  0.0       55:15 nginx: worker process

```

*Preserve /root/.cache/flashinfer if you recreate or restart the environment; otherwise you may pay this compilation cost again.*


### Skip warmup

> This is a real DeepGEMM kernel failure on SM103

```
export VLLM_USE_DEEP_GEMM=1
```


### Sparse-Prefill invalid pointer 


>  known upstream vLLM/FlashMLA class of failure

There is an open vLLM issue describing essentially the same DeepSeek V4 + DSpark failure: the FlashMLA sparse-prefill kernel receives an invalid pointer during TMA descriptor initialization. 

# Performance Benchmarks

One specific task (`regex-log`) from Terminal Bench 2.1.

- <https://blog.john-pfeiffer.com/reproducing-a-coding-benchmark-with-harbor-and-terminal-bench-21/>
- <https://www.tbench.ai/benchmarks/terminal-bench-2/regex-log>
- <https://github.com/harbor-framework/terminal-bench-2-1/tree/main/tasks/regex-log>

**DeepSeek V4 Flash 0731**

- 15 of 16 agents succeeded
- - **55 tokens per second, per agent**
- Prefix cache ~92% = can double output to 880 t/s


**Gemma4 31B**

- Giving plenty of hardware (B300 vs A100) to a weaker model can improve its performance (15 of 16 "terminal benchmark 2.1" for one specific task attempts pass)
- 64 tokens per second for a 1 agent  *(scales to about 60 t/s at 4x agents)*
- 55 tokens per second for 8 agents *(Avg generation throughput: 440.0 tokens/s, Running: 8 reqs)*


# Appendix and Methodology

*all IP addresses are fictional - replace with your real values*

1. setup and started vLLM
2. before metrics
3. First Harbor batch of 8 parallel
4. warm up batch metrics
5. Second batch of 8 parallel
6. final metrics

## Runpod

Setup an account, add credits (at $0 all instances will be deleted), **B300 costs about $8 per hour**.

1. Select a B300 - add 500GB of storage (better safe than sorry - for storing the weights), "Secure cloud"
2. click "Deploy Pod"
3. Get the IP address

`ssh root@192.168.1.111 -p 34567 -i ~/.ssh/MYKEY`

`apt update && apt install -y byobu`

`byobu`

*aka fancy tmux - able to run multiple terminal shells in parallel, and trivial to reconnect/resume*

## CUDA 13 Toolkit

Starting from Ubuntu 22.04, and then making sure we have the necessary underlying dependencies.

*This can take awhile so running this in one window and while it cooks do the huggingface and model downloads in another window.*

```
apt install -y wget ca-certificates gnupg

wget -q https://developer.download.nvidia.com/compute/cuda/repos/ubuntu2204/x86_64/cuda-keyring_1.1-1_all.deb \
  -O /tmp/cuda-keyring.deb

dpkg -i /tmp/cuda-keyring.deb

apt update && apt install -y cuda-toolkit-13-0

cat >> ~/.bashrc <<'EOF'

export CUDA_HOME=/usr/local/cuda-13.0
export PATH="$CUDA_HOME/bin:$PATH"
export LD_LIBRARY_PATH="$CUDA_HOME/lib64:${LD_LIBRARY_PATH:-}"

EOF
```

`source ~/.bashrc`

`nvcc --version`

```
nvcc: NVIDIA (R) Cuda compiler driver
Copyright (c) 2005-2025 NVIDIA Corporation
Built on Wed_Aug_20_01:58:59_PM_PDT_2025
Cuda compilation tools, release 13.0, V13.0.88
Build cuda_13.0.r13.0/compiler.36424714_0
```

## HuggingFace

*for convenience trusting the astral shell script install rather than a pinned version from a package:*

```
curl -LsSf https://astral.sh/uv/install.sh | sh
source $HOME/.local/bin/env

uv tool install huggingface-hub 
```

### Download the Model

> Save the model locally to the larger disk

`mkdir -p /MODELS`

`hf download deepseek-ai/DeepSeek-V4-Flash-0731 --local-dir /MODELS/DeepSeek-V4-Flash-0731`

<https://huggingface.co/deepseek-ai/DeepSeek-V4-Flash-0731>


## Server Diagnostics

`nvidia-smi`

```
Tue Aug  4 18:21:21 2026
+-----------------------------------------------------------------------------------------+
| NVIDIA-SMI 580.126.09             Driver Version: 580.126.09     CUDA Version: 13.0     |
+-----------------------------------------+------------------------+----------------------+
| GPU  Name                 Persistence-M | Bus-Id          Disp.A | Volatile Uncorr. ECC |
| Fan  Temp   Perf          Pwr:Usage/Cap |           Memory-Usage | GPU-Util  Compute M. |
|                                         |                        |               MIG M. |
|=========================================+========================+======================|
|   0  NVIDIA B300 SXM6 AC            On  |   00000000:9A:00.0 Off |                    0 |
| N/A   23C    P0            135W / 1100W |       0MiB / 275040MiB |      0%      Default |
|                                         |                        |             Disabled |
```

> Need at least 200GB for downloading the model locally

`df -h`
```
Filesystem                      Size  Used Avail Use% Mounted on
overlay                         500G  175M  500G   1% /
tmpfs                            64M     0   64M   0% /dev
shm                             234G   84K  234G   1% /dev/shm
/dev/md0                        3.5T  242G  3.1T   8% /usr/bin/nvidia-smi
tmpfs                           404G  8.7M  404G   1% /run/nvidia-persistenced/socket
/dev/mapper/pod-opf9hiftvk2n1j   98G  1.9G   92G   2% /workspace
/dev/md1                         11T  3.7T  6.8T  36% /etc/hosts
tmpfs                           4.0K  4.0K     0 100% /run/nvidia-ctk-hookd59618f4-5824-4ebc-a146-f34419511b6f
tmpfs                           4.0K     0  4.0K   0% /proc/acpi
```


## vLLM Setup - DeepGEMM

> More complicated dependencies needed for DeepSeek specific components

*NOT: uv tool install vllm*

```
cd /workspace

uv venv
source .venv/bin/activate

uv pip install "vllm==0.26.0" --torch-backend=auto

vllm --version
	0.26.0

python -c 'import torch; print(torch.__version__, torch.version.cuda)'
	2.11.0+cu130 13.0
```


**DeepGEMM** specific installation steps:
```
git clone --recursive https://github.com/deepseek-ai/DeepGEMM.git

uv pip install --no-build-isolation ./DeepGEMM

	Resolved 1 package in 2.74s
      Built deep-gemm @ file:///workspace/DeepGEMM Prepared 1 package in 1m 00[0/1] Installing wheels...                                                                                                                                                              
warning: Failed to hardlink files; falling back to full copy. This may lead to degraded performance.
         If the cache and target directories are on different filesystems, hardlinking may not be supported.
         If this is intentional, set `export UV_LINK_MODE=copy` or use `--link-mode=copy` to suppress this warning.
Installed 1 package in 87ms
 + deep-gemm==2.6.1+559d79f (from file:///workspace/DeepGEMM)
```

## Run VLLM

```
source ~/.bashrc
source /workspace/.venv/bin/activate
```

See the main post.

The usual verification checks:

`curl -s localhost:8000/health -o /dev/null -w '%{http_code}\n'`
  
`curl -s http://localhost:8000/v1/models | jq`



---
# Linode and Harbor

I suggest using 16B as you can push the B300 harder =)

`ssh -i ~/.ssh/mykey root@192.168.2.222`

setup instructions *and more info on the Harbor framework for agent benchmarking*: <https://blog.john-pfeiffer.com/reproducing-a-coding-benchmark-with-harbor-and-terminal-bench-21/#install-docker>

`apt install -y autossh`

*ensure the MYKEY ssh key for ThunderCompute is put onto the Linode box, and `chmod 400 /root/.ssh/MYKEY`*

**SSH Tunnel**

First verify you can connect to the GPU host box: `ssh -i /root/.ssh/MYKEY  ubuntu@192.168.1.111 -p 34567`

*(accept the unknown fingerprint)* 

Then setup a more resilient tunnel with **autossh**:

```
autossh -M 0 -f -N -T \
  -o ExitOnForwardFailure=yes -o ServerAliveInterval=30 -o ServerAliveCountMax=3 -o Compression=no \
  -L 127.0.0.1:18000:127.0.0.1:8000 \
  -p 34567 -i /root/.ssh/MYKEY root@192.168.1.111


ss -ltnp | grep ':18000'
	LISTEN 0      128        127.0.0.1:18000      0.0.0.0:*    users:(("ssh",pid=123778,fd=4))
```


`curl -s http://localhost:18000/v1/models | jq`

```{"object": "list","data": [{"id": "deepseek-v4-flash-0731",...```



```
export OPENAI_BASE_URL=http://localhost:18000/v1
export OPENAI_API_KEY=EMPTY

harbor run -d terminal-bench/terminal-bench-2-1 --agent terminus-2 --model openai/deepseek-v4-flash-0731 -n 1 -k 1 --include-task-name terminal-bench/regex-log

	⠹ 0/1 Running trials... ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 0:00:37 -:--:--
	⠇ 0:00:33 regex-log__CdrJ3ug: running agent...
```

Usually it's boring to watch the agents, but to track progress...

`watch -n 5 'date && cat result.json && grep -r \'"step_id":\' .'`


# What is DSpark speculative decoding?

Guess and win a prize =)

DSpark is DeepSeek’s speculative-decoding system.

1. draft module proposes:  [token 1 ... token 7]
2. target model verifies:  all proposed tokens together
3. accept:                 the batch of tokens
4. retry:                  from the first rejected token

This can speed up the rate of tokens output - verification by the "main model" is cheaper than it generating each of those tokens itself.

For this workload this length of speculative decoding was inefficient.

The per-position acceptance drops off a cliff: 67% -> 43% -> 31% -> 24% -> 17% -> 12% -> 9%. 

**The learning**: worth try num_speculative tokens as 4.

| `--speculative-config '{"method":"dspark","num_speculative_tokens":7,"draft_sample_method":"greedy"}'` | Enable DSpark speculative decoding with a 7-token draft window |



---

# Example vLLM logs

Waiting 20 minutes for a lot of JIT compilation takes patience.

Concurrently (byobu/tmux) check on things with `ps aux | grep ptax`

```
(APIServer pid=347228) INFO:     Started server process [347228]
(APIServer pid=347228) INFO:     Waiting for application startup.
(APIServer pid=347228) INFO:     Application startup complete.
(EngineCore pid=348187) WARNING 08-04 20:50:56 [jit_monitor.py:135] TileLang JIT compilation during inference: mhc_pre_big_fuse_broadcast_with_norm_tilelang. This causes a latency spike; consider extending warmup to cover this shape/config.
(EngineCore pid=348187) WARNING 08-04 20:50:56 [jit_monitor.py:135] CuTeDSL JIT compilation during inference: DequantGatherKCacheKernel. This causes a latency spike; consider extending warmup to cover this shape/config.
(EngineCore pid=348187) WARNING 08-04 20:50:57 [jit_monitor.py:135] TileLang JIT compilation during inference: mhc_pre_big_fuse_with_norm_tilelang. This causes a latency spike; consider extending warmup to cover this shape/config.
(EngineCore pid=348187) WARNING 08-04 20:50:58 [jit_monitor.py:135] Triton kernel JIT compilation during inference: _prepare_dflash_inputs_kernel. This causes a latency spike; consider extending warmup to cover this shape/config.
(APIServer pid=347228) INFO 08-04 20:51:08 [loggers.py:310] Engine 000: Avg prompt throughput: 93.9 tokens/s, Avg generation throughput: 13.0 tokens/s, Running: 1 reqs, Waiting: 0 reqs, GPU KV cache usage: 0.0%, Prefix cache hit rate: 0.0%
(APIServer pid=347228) INFO 08-04 20:51:08 [metrics.py:120] SpecDecoding metrics: Mean acceptance length: 3.49, Accepted throughput: 0.12 tokens/s, Drafted throughput: 0.34 tokens/s, Accepted: 92 tokens, Drafted: 259 tokens, Per-position acceptance rate: 0.757, 0.622, 0.432, 0.324, 0.189, 0.108, 0.054, Avg Draft acceptance rate: 35.5%
(APIServer pid=347228) INFO 08-04 20:51:18 [loggers.py:310] Engine 000: Avg prompt throughput: 0.0 tokens/s, Avg generation throughput: 6.2 tokens/s, Running: 1 reqs, Waiting: 0 reqs, GPU KV cache usage: 0.0%, Prefix cache hit rate: 0.0%


...

(APIServer pid=347228) INFO 08-04 21:01:58 [metrics.py:120] SpecDecoding metrics: Mean acceptance length: 7.24, Accepted throughput: 23.10 tokens/s, Drafted throughput: 25.90 tokens/s, Accepted: 231 tokens, Drafted: 259 tokens, Per-position acceptance rate: 1.000, 1.000, 0.973, 0.973, 0.892, 0.784, 0.622, Avg Draft acceptance rate: 89.2%
(APIServer pid=347228) INFO:     127.0.0.1:56326 - "POST /v1/chat/completions HTTP/1.1" 200 OK
(EngineCore pid=348187) 2026-08-04 21:02:03  [TileLang:tilelang.jit.kernel:INFO] (kernel.py:133): TileLang begins to compile kernel `mhc_pre_big_fuse_broadcast_with_norm_tilelang` with `out_idx=None`
(APIServer pid=347228) INFO 08-04 21:02:08 [loggers.py:310] Engine 000: Avg prompt throughput: 0.0 tokens/s, Avg generation throughput: 4.4 tokens/s, Running: 0 reqs, Waiting: 0 reqs, GPU KV cache usage: 0.0%, Prefix cache hit rate: 83.7%
(APIServer pid=347228) INFO 08-04 21:02:08 [metrics.py:120] SpecDecoding metrics: Mean acceptance length: 7.50, Accepted throughput: 3.90 tokens/s, Drafted throughput: 4.20 tokens/s, Accepted: 39 tokens, Drafted: 42 tokens, Per-position acceptance rate: 1.000, 1.000, 1.000, 1.000, 1.000, 1.000, 0.500, Avg Draft acceptance rate: 92.9%
```

## vLLM start with Breakable CUDA Graph enabled

This is the configuration that crashed when the following load was added:

```
harbor run -d terminal-bench/terminal-bench-2-1 --agent terminus-2 --model openai/deepseek-v4-flash-0731 \
  -n 8 -k 8 --include-task-name terminal-bench/regex-log
```

<details>
```
(APIServer pid=57071) INFO 08-06 20:48:31 [api_utils.py:345] 
(APIServer pid=57071) INFO 08-06 20:48:31 [api_utils.py:345]        █     █     █▄   ▄█
(APIServer pid=57071) INFO 08-06 20:48:31 [api_utils.py:345]  ▄▄ ▄█ █     █     █ ▀▄▀ █  version 0.26.0
(APIServer pid=57071) INFO 08-06 20:48:31 [api_utils.py:345]   █▄█▀ █     █     █     █  model   /MODELS/DeepSeek-V4-Flash-0731
(APIServer pid=57071) INFO 08-06 20:48:31 [api_utils.py:345]    ▀▀  ▀▀▀▀▀ ▀▀▀▀▀ ▀     ▀
(APIServer pid=57071) INFO 08-06 20:48:31 [api_utils.py:345] 
(APIServer pid=57071) INFO 08-06 20:48:31 [api_utils.py:273] non-default args: {'model_tag': '/MODELS/DeepSeek-V4-Flash-0731', 'enable_auto_tool_choice': True, 'tool_call_parser': 'deepseek_v4', 'host': '127.0.0.1', 'model': '/MODELS/DeepSeek-V4-Flash-0731', 'tokenizer_mode': 'deepseek_v4', 'trust_remote_code': True, 'max_model_len': 65536, 'served_model_name': ['deepseek-v4-flash-0731'], 'reasoning_parser': 'deepseek_v4', 'enable_expert_parallel': True, 'block_size': 256, 'kv_cache_dtype': 'fp8', 'speculative_config': {'method': 'dspark', 'num_speculative_tokens': 7, 'draft_sample_method': 'greedy'}, 'attention_config': AttentionConfig(backend=None, backend_per_kind={}, flash_attn_version=None, use_prefill_decode_attention=False, flash_attn_max_num_splits_for_cuda_graph=32, tq_max_kv_splits_for_cuda_graph=32, use_trtllm_attention=None, disable_flashinfer_q_quantization=False, mla_prefill_backend=None, use_prefill_query_quantization=False, use_fp4_indexer_cache=True, indexer_kv_dtype='bf16', use_non_causal=False, sparse_mla_force_mqa=False, flex_attn_block_m=None, flex_attn_block_n=None, flex_attn_q_block_size=None, flex_attn_kv_block_size=None)}
(APIServer pid=57071) INFO 08-06 20:48:31 [config.py:776] Detected quantization_config.scale_fmt=ue8m0; enabling UE8M0 for DeepGEMM.
(APIServer pid=57071) INFO 08-06 20:48:31 [model.py:623] Resolved architecture: DeepseekV4ForCausalLM
(APIServer pid=57071) INFO 08-06 20:48:31 [model.py:1788] Using max model len 65536
(APIServer pid=57071) INFO 08-06 20:48:32 [cache.py:285] Using fp8 data type to store kv cache. It reduces the GPU memory footprint and boosts the performance. Meanwhile, it may cause accuracy drop without a proper scaling factor
(APIServer pid=57071) INFO 08-06 20:48:32 [model.py:623] Resolved architecture: DeepSeekV4MTPModel
(APIServer pid=57071) INFO 08-06 20:48:32 [model.py:1788] Using max model len 1048576
(APIServer pid=57071) INFO 08-06 20:48:32 [speculative.py:1126] Overriding draft model max model len from 1048576 to 65536
(APIServer pid=57071) INFO 08-06 20:48:32 [scheduler.py:252] Chunked prefill is enabled with max_num_batched_tokens=8192.
(APIServer pid=57071) INFO 08-06 20:48:32 [vllm.py:1109] Asynchronous scheduling is enabled.
(APIServer pid=57071) INFO 08-06 20:48:32 [vllm.py:1197] Auto-enabling VLLM_USE_BREAKABLE_CUDAGRAPH=1. Set VLLM_USE_BREAKABLE_CUDAGRAPH=0 to opt out.
(APIServer pid=57071) WARNING 08-06 20:48:32 [vllm.py:1203] VLLM_USE_BREAKABLE_CUDAGRAPH is set, disabling vLLM's torch.compile pipeline. Equivalent to -cc.mode=none.
(APIServer pid=57071) WARNING 08-06 20:48:32 [vllm.py:1213] Inductor compilation was disabled by user settings, optimizations settings that are only active during inductor compilation will be ignored.
(APIServer pid=57071) INFO 08-06 20:48:32 [kernel.py:295] Final IR op priority after setting platform defaults: IrOpPriorityConfig(rms_norm=['vllm_c', 'native'], fused_add_rms_norm=['vllm_c', 'native'])
(APIServer pid=57071) WARNING 08-06 20:48:32 [vllm.py:1718] max_num_scheduled_tokens is set to 2048 based on the speculative decoding settings. This may lead to suboptimal performance. Consider increasing max_num_batched_tokens to accommodate the additional draft token slots, or decrease num_speculative_tokens or max_num_seqs.
(APIServer pid=57071) WARNING 08-06 20:48:32 [vllm.py:2228] Model Runner V2 does not yet support the thinking_token_budget request parameter. Set VLLM_USE_V2_MODEL_RUNNER=0 if this is required.
(APIServer pid=57071) INFO 08-06 20:48:33 [compilation.py:329] Enabled custom fusions: norm_quant, act_quant
(EngineCore pid=57666) INFO 08-06 20:48:39 [core.py:116] Initializing a V1 LLM engine (v0.26.0) with config: model='/MODELS/DeepSeek-V4-Flash-0731', speculative_config=SpeculativeConfig(method='dspark', model='/MODELS/DeepSeek-V4-Flash-0731', num_spec_tokens=7), tokenizer='/MODELS/DeepSeek-V4-Flash-0731', skip_tokenizer_init=False, tokenizer_mode=deepseek_v4, revision=None, tokenizer_revision=None, trust_remote_code=True, dtype=torch.bfloat16, max_seq_len=65536, download_dir=None, load_format=auto, tensor_parallel_size=1, pipeline_parallel_size=1, data_parallel_size=1, decode_context_parallel_size=1, dcp_comm_backend=ag_rs, disable_custom_all_reduce=False, quantization=deepseek_v4_fp8, quantization_config=None, enforce_eager=False, enable_return_routed_experts=False, kv_cache_dtype=fp8, device_config=cuda, structured_outputs_config=StructuredOutputsConfig(backend='auto', disable_any_whitespace=False, disable_additional_properties=False, reasoning_parser='deepseek_v4', reasoning_parser_plugin='', enable_in_reasoning=False), observability_config=ObservabilityConfig(show_hidden_metrics_for_version=None, otlp_traces_endpoint=None, collect_detailed_traces=None, kv_cache_metrics=False, kv_cache_metrics_sample=0.01, cudagraph_metrics=False, enable_layerwise_nvtx_tracing=False, enable_mfu_metrics=False, enable_mm_processor_stats=False, enable_logging_iteration_details=False, jit_monitor_mode='warn', jit_monitor_verbose=False), seed=0, served_model_name=deepseek-v4-flash-0731, enable_prefix_caching=True, enable_chunked_prefill=True, pooler_config=None, compilation_config={'mode': <CompilationMode.NONE: 0>, 'debug_dump_path': None, 'cache_dir': '', 'compile_cache_save_format': 'binary', 'backend': 'inductor', 'custom_ops': ['+quant_fp8', 'all', '+quant_fp8'], 'ir_enable_torch_wrap': False, 'splitting_ops': [], 'compile_mm_encoder': False, 'cudagraph_mm_encoder': False, 'encoder_cudagraph_token_budgets': [], 'encoder_cudagraph_max_vision_items_per_batch': 0, 'encoder_cudagraph_max_frames_per_batch': None, 'compile_sizes': [], 'compile_ranges_endpoints': [8192], 'inductor_compile_config': {'enable_auto_functionalized_v2': False, 'size_asserts': False, 'alignment_asserts': False, 'scalar_asserts': False, 'combo_kernels': True, 'benchmark_combo_kernel': True}, 'inductor_passes': {}, 'cudagraph_mode': <CUDAGraphMode.FULL_AND_PIECEWISE: (2, 1)>, 'cudagraph_num_of_warmups': 1, 'cudagraph_capture_sizes': [1, 2, 4, 8, 16, 24, 32, 40, 48, 56, 64, 72, 80, 88, 96, 104, 112, 120, 128, 136, 144, 152, 160, 168, 176, 184, 192, 200, 208, 216, 224, 232, 240, 248, 256, 272, 288, 304, 320, 336, 352, 368, 384, 400, 416, 432, 448, 464, 480, 496, 512], 'cudagraph_copy_inputs': False, 'cudagraph_specialize_lora': True, 'use_inductor_graph_partition': False, 'pass_config': {'fuse_norm_quant': True, 'fuse_act_quant': True, 'fuse_attn_quant': False, 'enable_sp': False, 'fuse_gemm_comms': False, 'fuse_allreduce_rms': False, 'enable_qk_norm_rope_fusion': False, 'fuse_rope_kvcache_cat_mla': False, 'fuse_act_padding': False, 'fuse_qk_norm_rope_kvcache': False}, 'max_cudagraph_capture_size': 512, 'dynamic_shapes_config': {'type': <DynamicShapesType.BACKED: 'backed'>, 'evaluate_guards': False, 'assume_32_bit_indexing': False}, 'local_cache_dir': None, 'fast_moe_cold_start': False, 'static_all_moe_layers': []}, kernel_config=KernelConfig(ir_op_priority=IrOpPriorityConfig(rms_norm=['vllm_c', 'native'], fused_add_rms_norm=['vllm_c', 'native']), enable_flashinfer_autotune=True, enable_cutedsl_warmup=True, enable_bf16x3_router_gemm=False, moe_backend='auto', linear_backend='auto')
(EngineCore pid=57666) INFO 08-06 20:48:41 [parallel_state.py:1615] world_size=1 rank=0 local_rank=0 distributed_init_method=tcp://172.21.0.2:56475 backend=nccl
(EngineCore pid=57666) INFO 08-06 20:48:41 [parallel_state.py:1946] rank 0 in world size 1 is assigned as DP rank 0, PP rank 0, PCP rank 0, TP rank 0, EP rank 0, EPLB rank N/A
(EngineCore pid=57666) INFO 08-06 20:48:41 [gpu_worker.py:378] Using V2 Model Runner
(EngineCore pid=57666) INFO 08-06 20:48:42 [model_runner.py:284] Loading model from scratch...
(EngineCore pid=57666) INFO 08-06 20:48:42 [quant_config.py:75] DeepSeek V4 expert_dtype resolved to 'fp4'
(EngineCore pid=57666) INFO 08-06 20:48:42 [__init__.py:604] Selected DeepGemmFp8BlockScaledMMKernel for Fp8LinearMethod
(EngineCore pid=57666) INFO 08-06 20:48:42 [deep_gemm.py:175] deep_gemm not found in site-packages, trying vendored vllm.third_party.deep_gemm
(EngineCore pid=57666) INFO 08-06 20:48:42 [deep_gemm.py:202] DeepGEMM PDL enabled on vllm.third_party.deep_gemm.
(EngineCore pid=57666) INFO 08-06 20:48:42 [deep_gemm.py:120] DeepGEMM E8M0 enabled on current platform.
(EngineCore pid=57666) INFO 08-06 20:48:42 [attention.py:91] Using DeepSeek's fp8_ds_mla KV cache format.
(EngineCore pid=57666) INFO 08-06 20:48:43 [mxfp4.py:625] Using 'FLASHINFER_TRTLLM_MXFP4_MXFP8' Mxfp4 MoE backend.
(EngineCore pid=57666) INFO 08-06 20:48:43 [attention.py:694] Using MXFP4 indexer cache for Lightning Indexer.
(EngineCore pid=57666) INFO 08-06 20:48:44 [weight_utils.py:869] Filesystem type for checkpoints: OVERLAY. Checkpoint size: 155.43 GiB. Available RAM: 3902.34 GiB.
(EngineCore pid=57666) INFO 08-06 20:48:44 [weight_utils.py:892] Auto-prefetch is disabled because the filesystem (OVERLAY) is not a recognized network FS (NFS/Lustre). If you want to force prefetching, start vLLM with --safetensors-load-strategy=prefetch.
Loading safetensors checkpoint shards:   0% Completed | 0/48 [00:00<?, ?it/s]
Loading safetensors checkpoint shards:   2% Completed | 1/48 [00:00<00:09,  5.13it/s]
...

Loading safetensors checkpoint shards: 100% Completed | 48/48 [03:25<00:00,  4.27s/it]
(EngineCore pid=57666) 
(EngineCore pid=57666) INFO 08-06 20:52:10 [default_loader.py:430] Loading weights took 206.61 seconds
(EngineCore pid=57666) INFO 08-06 20:52:14 [mxfp4.py:1718] Using MoEPrepareAndFinalizeNoDPEPModular
(EngineCore pid=57666) INFO 08-06 20:52:14 [mxfp4.py:1719] Using TrtLlmMxfp4ExpertsModular
(EngineCore pid=57666) INFO 08-06 20:52:18 [eagle3_utils.py:28] Using Eagle3 auxiliary layers from config: (41, 42, 43)
(EngineCore pid=57666) INFO 08-06 20:52:18 [vllm.py:1109] Asynchronous scheduling is enabled.
(EngineCore pid=57666) WARNING 08-06 20:52:18 [vllm.py:1203] VLLM_USE_BREAKABLE_CUDAGRAPH is set, disabling vLLM's torch.compile pipeline. Equivalent to -cc.mode=none.
(EngineCore pid=57666) WARNING 08-06 20:52:18 [vllm.py:1213] Inductor compilation was disabled by user settings, optimizations settings that are only active during inductor compilation will be ignored.
(EngineCore pid=57666) INFO 08-06 20:52:18 [kernel.py:295] Final IR op priority after setting platform defaults: IrOpPriorityConfig(rms_norm=['vllm_c', 'native'], fused_add_rms_norm=['vllm_c', 'native'])
(EngineCore pid=57666) WARNING 08-06 20:52:18 [vllm.py:1718] max_num_scheduled_tokens is set to 2048 based on the speculative decoding settings. This may lead to suboptimal performance. Consider increasing max_num_batched_tokens to accommodate the additional draft token slots, or decrease num_speculative_tokens or max_num_seqs.
(EngineCore pid=57666) WARNING 08-06 20:52:18 [vllm.py:2228] Model Runner V2 does not yet support the thinking_token_budget request parameter. Set VLLM_USE_V2_MODEL_RUNNER=0 if this is required.
(EngineCore pid=57666) INFO 08-06 20:52:18 [compilation.py:329] Enabled custom fusions: norm_quant, act_quant
(EngineCore pid=57666) INFO 08-06 20:52:18 [weight_utils.py:869] Filesystem type for checkpoints: OVERLAY. Checkpoint size: 155.43 GiB. Available RAM: 3902.17 GiB.
Loading safetensors checkpoint shards:   0% Completed | 0/48 [00:00<?, ?it/s]
Loading safetensors checkpoint shards:  10% Completed | 5/48 [00:00<00:00, 45.17it/s]
...

Loading safetensors checkpoint shards:  98% Completed | 47/48 [00:10<00:00,  1.36it/s]
Loading safetensors checkpoint shards: 100% Completed | 48/48 [00:15<00:00,  3.15it/s]
(EngineCore pid=57666) 
(EngineCore pid=57666) INFO 08-06 20:52:34 [dspark.py:457] DSpark draft model loaded: 96 params
(EngineCore pid=57666) INFO 08-06 20:52:34 [default_loader.py:430] Loading weights took 15.31 seconds
(EngineCore pid=57666) INFO 08-06 20:52:35 [model_runner.py:305] Model loading took 156.32 GiB and 233.014771 seconds
(EngineCore pid=57666) INFO 08-06 20:52:35 [topk_topp_sampler.py:55] Using FlashInfer for top-p & top-k sampling.
(EngineCore pid=57666) 2026-08-06 20:52:40  [TileLang:tilelang.jit.kernel:INFO] (kernel.py:133): TileLang begins to compile kernel `mhc_pre_big_fuse_broadcast_with_norm_tilelang` with `out_idx=None`
(EngineCore pid=57666) 2026-08-06 20:52:48  [TileLang:tilelang.jit.kernel:INFO] (kernel.py:141): TileLang completes to compile kernel `mhc_pre_big_fuse_broadcast_with_norm_tilelang`
(EngineCore pid=57666) 2026-08-06 20:52:59  [TileLang:tilelang.jit.kernel:INFO] (kernel.py:133): TileLang begins to compile kernel `mhc_post_tilelang` with `out_idx=None`
(EngineCore pid=57666) 2026-08-06 20:53:02  [TileLang:tilelang.jit.kernel:INFO] (kernel.py:141): TileLang completes to compile kernel `mhc_post_tilelang`
(EngineCore pid=57666) 2026-08-06 20:53:04  [TileLang:tilelang.jit.kernel:INFO] (kernel.py:133): TileLang begins to compile kernel `mhc_pre_big_fuse_with_norm_tilelang` with `out_idx=None`
(EngineCore pid=57666) 2026-08-06 20:53:12  [TileLang:tilelang.jit.kernel:INFO] (kernel.py:141): TileLang completes to compile kernel `mhc_pre_big_fuse_with_norm_tilelang`
(EngineCore pid=57666) 2026-08-06 20:53:29  [TileLang:tilelang.jit.kernel:INFO] (kernel.py:133): TileLang begins to compile kernel `hc_head_fuse_tilelang` with `out_idx=None`
(EngineCore pid=57666) 2026-08-06 20:53:33  [TileLang:tilelang.jit.kernel:INFO] (kernel.py:141): TileLang completes to compile kernel `hc_head_fuse_tilelang`
(EngineCore pid=57666) INFO 08-06 20:53:42 [gpu_worker.py:560] Available KV cache memory: 86.74 GiB
(EngineCore pid=57666) INFO 08-06 20:53:42 [kv_cache_utils.py:2177] GPU KV cache size: 913,657 tokens
(EngineCore pid=57666) INFO 08-06 20:53:42 [kv_cache_utils.py:2178] Maximum concurrency for 65,536 tokens per request: 13.94x
(EngineCore pid=57666) INFO 08-06 20:53:42 [indexer.py:306] DSA indexer decode path: use_flattening=False (next_n=8, use_fp4_indexer_cache=True)
(EngineCore pid=57666) WARNING 08-06 20:53:42 [vllm.py:1213] Inductor compilation was disabled by user settings, optimizations settings that are only active during inductor compilation will be ignored.
(EngineCore pid=57666) INFO 08-06 20:53:42 [kernel.py:295] Final IR op priority after setting platform defaults: IrOpPriorityConfig(rms_norm=['vllm_c', 'native'], fused_add_rms_norm=['vllm_c', 'native'])
(EngineCore pid=57666) INFO 08-06 20:53:51 [flashinfer_sparse_mla_warmup.py:233] Warming up DeepSeek V4 sparse MLA attention for mixed tokens=16.
(EngineCore pid=57666) 2026-08-06 20:53:57  [TileLang:tilelang.jit.kernel:INFO] (kernel.py:133): TileLang begins to compile kernel `mhc_pre_big_fuse_broadcast_with_norm_tilelang` with `out_idx=None`
(EngineCore pid=57666) 2026-08-06 20:54:05  [TileLang:tilelang.jit.kernel:INFO] (kernel.py:141): TileLang completes to compile kernel `mhc_pre_big_fuse_broadcast_with_norm_tilelang`
...

(EngineCore pid=57666) 2026-08-06 20:54:58  [TileLang:tilelang.jit.kernel:INFO] (kernel.py:133): TileLang begins to compile kernel `mhc_pre_big_fuse_with_norm_tilelang` with `out_idx=None`
(EngineCore pid=57666) 2026-08-06 20:55:05  [TileLang:tilelang.jit.kernel:INFO] (kernel.py:141): TileLang completes to compile kernel `mhc_pre_big_fuse_with_norm_tilelang`
DeepGEMM warmup: 100%|██████████| 1670/1670 [03:15<00:00,  8.55it/s]
(EngineCore pid=57666) INFO 08-06 20:58:26 [kernel_warmup.py:227] Using FlashInfer autotune cache file: /root/.cache/vllm/flashinfer_autotune_cache/0.6.14/103a/82dc49d0549fea2496625650ed2ab56b389c8855250771c6f1de898521a9302f/autotune_configs.json
(EngineCore pid=57666) 2026-08-06 20:58:26,931 - INFO - autotuner.py:651 - flashinfer.jit: [Autotuner]: Autotuning process starts ...



[AutoTuner]: Tuning flashinfer::trtllm_fp4_block_scale_moe: 100%|██████████| 10/10 [09:22<00:00, 56.28s/profile]
(EngineCore pid=57666) 2026-08-06 21:07:57,803 - INFO - autotuner.py:674 - flashinfer.jit: [Autotuner]: Autotuning process ends
(EngineCore pid=57666) 2026-08-06 21:07:57,810 - INFO - autotuner.py:1808 - flashinfer.jit: [Autotuner]: Saved 10 configs to /root/.cache/vllm/flashinfer_autotune_cache/0.6.14/103a/82dc49d0549fea2496625650ed2ab56b389c8855250771c6f1de898521a9302f/autotune_configs.json (10 new, 0 from previous config)
(EngineCore pid=57666) 2026-08-06 21:07:57,815 - INFO - autotuner.py:1899 - flashinfer.jit: [Autotuner]: Loaded 10 configs from /root/.cache/vllm/flashinfer_autotune_cache/0.6.14/103a/82dc49d0549fea2496625650ed2ab56b389c8855250771c6f1de898521a9302f/autotune_configs.json
(EngineCore pid=57666) INFO 08-06 21:07:57 [kernel_warmup.py:268] FlashInfer autotune cache loaded on rank 0 from /root/.cache/vllm/flashinfer_autotune_cache/0.6.14/103a/82dc49d0549fea2496625650ed2ab56b389c8855250771c6f1de898521a9302f/autotune_configs.json.
(EngineCore pid=57666) INFO 08-06 21:07:57 [kernel_warmup.py:65] Warming up ll_bf16 router GEMM kernels.
(EngineCore pid=57666) INFO 08-06 21:08:05 [cutedsl_warmup.py:101] Skipping CuTeDSL warmup because no compile units were requested.
(EngineCore pid=57666) INFO 08-06 21:08:05 [breakable_cudagraph.py:288] Breakable CUDA graph enabled
(EngineCore pid=57666) 2026-08-06 21:08:11  [TileLang:tilelang.jit.kernel:INFO] (kernel.py:133): TileLang begins to compile kernel `mhc_pre_big_fuse_with_norm_tilelang` with `out_idx=None`
(EngineCore pid=57666) 2026-08-06 21:08:19  [TileLang:tilelang.jit.kernel:INFO] (kernel.py:141): TileLang completes to compile kernel `mhc_pre_big_fuse_with_norm_tilelang`
(EngineCore pid=57666) 2026-08-06 21:08:28  [TileLang:tilelang.jit.kernel:INFO] (kernel.py:133): TileLang begins to compile kernel `mhc_pre_big_fuse_with_norm_tilelang` with `out_idx=None`
(EngineCore pid=57666) 2026-08-06 21:08:36  [TileLang:tilelang.jit.kernel:INFO] (kernel.py:141): TileLang completes to compile kernel `mhc_pre_big_fuse_with_norm_tilelang`
(EngineCore pid=57666) 2026-08-06 21:08:48  [TileLang:tilelang.jit.kernel:INFO] (kernel.py:133): TileLang begins to compile kernel `mhc_pre_big_fuse_with_norm_tilelang` with `out_idx=None`
(EngineCore pid=57666) 2026-08-06 21:08:56  [TileLang:tilelang.jit.kernel:INFO] (kernel.py:141): TileLang completes to compile kernel `mhc_pre_big_fuse_with_norm_tilelang`
(EngineCore pid=57666) 2026-08-06 21:09:09  [TileLang:tilelang.jit.kernel:INFO] (kernel.py:133): TileLang begins to compile kernel `mhc_pre_big_fuse_with_norm_tilelang` with `out_idx=None`
(EngineCore pid=57666) 2026-08-06 21:09:17  [TileLang:tilelang.jit.kernel:INFO] (kernel.py:141): TileLang completes to compile kernel `mhc_pre_big_fuse_with_norm_tilelang`
(EngineCore pid=57666) 2026-08-06 21:09:28  [TileLang:tilelang.jit.kernel:INFO] (kernel.py:133): TileLang begins to compile kernel `mhc_pre_big_fuse_with_norm_tilelang` with `out_idx=None`
(EngineCore pid=57666) 2026-08-06 21:09:35  [TileLang:tilelang.jit.kernel:INFO] (kernel.py:141): TileLang completes to compile kernel `mhc_pre_big_fuse_with_norm_tilelang`
(EngineCore pid=57666) 2026-08-06 21:09:52  [TileLang:tilelang.jit.kernel:INFO] (kernel.py:133): TileLang begins to compile kernel `mhc_pre_big_fuse_with_norm_tilelang` with `out_idx=None`
(EngineCore pid=57666) 2026-08-06 21:10:00  [TileLang:tilelang.jit.kernel:INFO] (kernel.py:141): TileLang completes to compile kernel `mhc_pre_big_fuse_with_norm_tilelang`
Capturing CUDA graphs (PIECEWISE): 100%|██████████| 51/51 [02:28<00:00,  2.92s/it]
Capturing CUDA graphs (FULL): 100%|██████████| 48/48 [00:20<00:00,  2.36it/s]
(EngineCore pid=57666) INFO 08-06 21:10:54 [speculator.py:127] Capturing model for DSpark speculator...
Capturing dspark CUDA graphs (FULL): 100%|██████████| 48/48 [00:01<00:00, 30.49it/s]
(EngineCore pid=57666) INFO 08-06 21:10:56 [model_runner.py:747] Graph capturing finished in 171 secs, took 3.06 GiB
(EngineCore pid=57666) INFO 08-06 21:10:56 [gpu_worker.py:857] Free memory on device (267.08/267.69 GiB) on startup. Desired GPU memory utilization is (0.92, 246.27 GiB). Actual usage is 156.32 GiB for weight, 2.99 GiB for peak activation, 0.23 GiB for non-torch memory, and 3.06 GiB for CUDAGraph memory. Replace gpu_memory_utilization config with `--kv-cache-memory=89686801859` (83.53 GiB) to fit into requested memory, or `--kv-cache-memory=112025012224` (104.33 GiB) to fully utilize gpu memory. Current kv cache memory in use is 86.74 GiB.


(EngineCore pid=57666) INFO 08-06 21:11:10 [jit_monitor.py:79] Kernel JIT monitor activated; monitored JIT compilations during inference will use mode=warn.
(EngineCore pid=57666) INFO 08-06 21:11:11 [core.py:347] init engine (profile, create kv cache, warmup model) took 1115.80 s
(EngineCore pid=57666) WARNING 08-06 21:11:12 [vllm.py:1213] Inductor compilation was disabled by user settings, optimizations settings that are only active during inductor compilation will be ignored.
(EngineCore pid=57666) INFO 08-06 21:11:12 [kernel.py:295] Final IR op priority after setting platform defaults: IrOpPriorityConfig(rms_norm=['vllm_c', 'native'], fused_add_rms_norm=['vllm_c', 'native'])
(APIServer pid=57071) INFO 08-06 21:11:12 [api_server.py:673] Supported tasks: ['generate']
(APIServer pid=57071) INFO 08-06 21:11:12 [parser_manager.py:37] "auto" tool choice has been enabled.
(APIServer pid=57071) WARNING 08-06 21:11:12 [model.py:1546] Default vLLM sampling parameters have been overridden by the model's `generation_config.json`: `{'temperature': 1.0, 'top_p': 1.0}`. If this is not intended, please relaunch vLLM instance with `--generation-config vllm`.
(APIServer pid=57071) INFO 08-06 21:11:12 [api_server.py:677] Starting vLLM server on http://127.0.0.1:8000
(APIServer pid=57071) INFO 08-06 21:11:12 [launcher.py:37] Available routes are:
(APIServer pid=57071) INFO 08-06 21:11:12 [launcher.py:46] Route: /openapi.json, Methods: GET, HEAD
(APIServer pid=57071) INFO 08-06 21:11:12 [launcher.py:46] Route: /inference/v1/generate, Methods: POST

(APIServer pid=57071) INFO:     Started server process [57071]
(APIServer pid=57071) INFO:     Waiting for application startup.
(APIServer pid=57071) INFO:     Application startup complete.

```
</details>

## More Harbor More Fun Shows the Eager Issue

```
harbor run -d terminal-bench/terminal-bench-2-1 --agent terminus-2 --model openai/deepseek-v4-flash-0731 -n 8 -k 8 --include-task-name terminal-bench/regex-log
⠹ 0/8 Running trials... ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 0:00:18 -:--:--
⠴ 0:00:14 regex-log__KtFFeoC: starting environment...
...

```

Expand for the full stack trace:
<details>

```
(APIServer pid=57071) INFO 08-06 21:11:12 [launcher.py:46] Route: /v1/completions/derender, Methods: POST
(APIServer pid=57071) INFO 08-06 21:11:12 [launcher.py:46] Route: /inference/v1/generate, Methods: POST
(APIServer pid=57071) INFO:     Started server process [57071]
(APIServer pid=57071) INFO:     Waiting for application startup.
(APIServer pid=57071) INFO:     Application startup complete.
(APIServer pid=57071) INFO:     127.0.0.1:52386 - "GET /metrics HTTP/1.1" 200 OK
(EngineCore pid=57666) WARNING 08-06 21:17:25 [jit_monitor.py:135] TileLang JIT compilation during inference: mhc_pre_big_fuse_broadcast_with_norm_tilelang. This causes a latency spike; consider extending warmup to cover this shape/config.
(EngineCore pid=57666) 2026-08-06 21:17:25  [TileLang:tilelang.jit.kernel:INFO] (kernel.py:133): TileLang begins to compile kernel `mhc_pre_big_fuse_broadcast_with_norm_tilelang` with `out_idx=None`
(EngineCore pid=57666) 2026-08-06 21:17:34  [TileLang:tilelang.jit.kernel:INFO] (kernel.py:141): TileLang completes to compile kernel `mhc_pre_big_fuse_broadcast_with_norm_tilelang`
(EngineCore pid=57666) WARNING 08-06 21:17:34 [jit_monitor.py:135] CuTeDSL JIT compilation during inference: DequantGatherKCacheKernel. This causes a latency spike; consider extending warmup to cover this shape/config.
(EngineCore pid=57666) WARNING 08-06 21:17:37 [jit_monitor.py:135] TileLang JIT compilation during inference: mhc_pre_big_fuse_with_norm_tilelang. This causes a latency spike; consider extending warmup to cover this shape/config.
(EngineCore pid=57666) 2026-08-06 21:17:37  [TileLang:tilelang.jit.kernel:INFO] (kernel.py:133): TileLang begins to compile kernel `mhc_pre_big_fuse_with_norm_tilelang` with `out_idx=None`
(EngineCore pid=57666) 2026-08-06 21:17:45  [TileLang:tilelang.jit.kernel:INFO] (kernel.py:141): TileLang completes to compile kernel `mhc_pre_big_fuse_with_norm_tilelang`
(EngineCore pid=57666) WARNING 08-06 21:17:47 [jit_monitor.py:135] Triton kernel JIT compilation during inference: _combine_topk_swa_indices_kernel. This causes a latency spike; consider extending warmup to cover this shape/config.
(EngineCore pid=57666) WARNING 08-06 21:17:47 [jit_monitor.py:135] Triton kernel JIT compilation during inference: _prepare_dflash_inputs_kernel. This causes a latency spike; consider extending warmup to cover this shape/config.
(EngineCore pid=57666) 2026-08-06 21:17:49  [TileLang:tilelang.jit.kernel:INFO] (kernel.py:133): TileLang begins to compile kernel `mhc_pre_big_fuse_broadcast_with_norm_tilelang` with `out_idx=None`
(EngineCore pid=57666) 2026-08-06 21:17:57  [TileLang:tilelang.jit.kernel:INFO] (kernel.py:141): TileLang completes to compile kernel `mhc_pre_big_fuse_broadcast_with_norm_tilelang`
(EngineCore pid=57666) 2026-08-06 21:18:03  [TileLang:tilelang.jit.kernel:INFO] (kernel.py:133): TileLang begins to compile kernel `mhc_pre_big_fuse_with_norm_tilelang` with `out_idx=None`
(EngineCore pid=57666) 2026-08-06 21:18:11  [TileLang:tilelang.jit.kernel:INFO] (kernel.py:141): TileLang completes to compile kernel `mhc_pre_big_fuse_with_norm_tilelang`
(APIServer pid=57071) INFO:     127.0.0.1:54608 - "POST /v1/chat/completions HTTP/1.1" 200 OK
(EngineCore pid=57666) WARNING 08-06 21:18:16 [jit_monitor.py:135] Triton kernel JIT compilation during inference: _compute_prefill_metadata_kernel. This causes a latency spike; consider extending warmup to cover this shape/config.
TMA Desc Addr:   0x7ffcf693e380
format         9
dim            3
gmem_address   0
globalDim      (512,64,0,1,1)
globalStrides  (2,1024,65536,0,0)
boxDim         (64,64,1,1,1)
elementStrides (1,1,1,1,1)
interleave     0
swizzle        3
l2Promotion    2
oobFill        0
Error: Failed to initialize the TMA descriptor 1
TMA Desc Addr:   0x7ffcf693e380
format         9
dim            3
gmem_address   0x400
globalDim      (64,64,0,1,1)
globalStrides  (2,1024,65536,0,0)
boxDim         (32,64,1,1,1)
elementStrides (1,1,1,1,1)
interleave     0
swizzle        2
l2Promotion    2
oobFill        0
Error: Failed to initialize the TMA descriptor 1
TMA Desc Addr:   0x7ffcf693e380
format         9
dim            3
gmem_address   0
globalDim      (512,64,0,1,1)
globalStrides  (2,1024,65536,0,0)
boxDim         (64,64,1,1,1)
elementStrides (1,1,1,1,1)
interleave     0
swizzle        3
l2Promotion    2
oobFill        0
Error: Failed to initialize the TMA descriptor 1
Assertion `res == CUresult::CUDA_SUCCESS` failed (/workspace/.deps/flashmla-src/csrc/sm100/prefill/sparse/fwd/head64/instantiations/../phase1.cuh:651): 
(EngineCore pid=57666) ERROR 08-06 21:18:16 [dump_input.py:72] Dumping input data for V1 LLM engine (v0.26.0) with config: model='/MODELS/DeepSeek-V4-Flash-0731', speculative_config=SpeculativeConfig(method='dspark', model='/MODELS/DeepSeek-V4-Flash-0731', num_spec_tokens=7), tokenizer='/MODELS/DeepSeek-V4-Flash-0731', skip_tokenizer_init=False, tokenizer_mode=deepseek_v4, revision=None, tokenizer_revision=None, trust_remote_code=True, dtype=torch.bfloat16, max_seq_len=65536, download_dir=None, load_format=auto, tensor_parallel_size=1, pipeline_parallel_size=1, data_parallel_size=1, decode_context_parallel_size=1, dcp_comm_backend=ag_rs, disable_custom_all_reduce=False, quantization=deepseek_v4_fp8, quantization_config=None, enforce_eager=False, enable_return_routed_experts=False, kv_cache_dtype=fp8_ds_mla, device_config=cuda, structured_outputs_config=StructuredOutputsConfig(backend='auto', disable_any_whitespace=False, disable_additional_properties=False, reasoning_parser='deepseek_v4', reasoning_parser_plugin='', enable_in_reasoning=False), observability_config=ObservabilityConfig(show_hidden_metrics_for_version=None, otlp_traces_endpoint=None, collect_detailed_traces=None, kv_cache_metrics=False, kv_cache_metrics_sample=0.01, cudagraph_metrics=False, enable_layerwise_nvtx_tracing=False, enable_mfu_metrics=False, enable_mm_processor_stats=False, enable_logging_iteration_details=False, jit_monitor_mode='warn', jit_monitor_verbose=False), seed=0, served_model_name=deepseek-v4-flash-0731, enable_prefix_caching=True, enable_chunked_prefill=True, pooler_config=None, compilation_config={'mode': <CompilationMode.NONE: 0>, 'debug_dump_path': None, 'cache_dir': '', 'compile_cache_save_format': 'binary', 'backend': 'inductor', 'custom_ops': ['+quant_fp8', 'all', '+quant_fp8', '+quant_fp8', '+quant_fp8', '+quant_fp8', '+quant_fp8', '+quant_fp8', '+quant_fp8'], 'ir_enable_torch_wrap': False, 'splitting_ops': [], 'compile_mm_encoder': False, 'cudagraph_mm_encoder': False, 'encoder_cudagraph_token_budgets': [], 'encoder_cudagraph_max_vision_items_per_batch': 0, 'encoder_cudagraph_max_frames_per_batch': None, 'compile_sizes': [], 'compile_ranges_endpoints': [8192], 'inductor_compile_config': {'enable_auto_functionalized_v2': False, 'size_asserts': False, 'alignment_asserts': False, 'scalar_asserts': False, 'combo_kernels': True, 'benchmark_combo_kernel': True}, 'inductor_passes': {}, 'cudagraph_mode': <CUDAGraphMode.FULL_AND_PIECEWISE: (2, 1)>, 'cudagraph_num_of_warmups': 1, 'cudagraph_capture_sizes': [1, 2, 4, 8, 16, 24, 32, 40, 48, 56, 64, 72, 80, 88, 96, 104, 112, 120, 128, 136, 144, 152, 160, 168, 176, 184, 192, 200, 208, 216, 224, 232, 240, 248, 256, 272, 288, 304, 320, 336, 352, 368, 384, 400, 416, 432, 448, 464, 480, 496, 512], 'cudagraph_copy_inputs': False, 'cudagraph_specialize_lora': True, 'use_inductor_graph_partition': False, 'pass_config': {'fuse_norm_quant': True, 'fuse_act_quant': True, 'fuse_attn_quant': False, 'enable_sp': False, 'fuse_gemm_comms': False, 'fuse_allreduce_rms': False, 'enable_qk_norm_rope_fusion': False, 'fuse_rope_kvcache_cat_mla': False, 'fuse_act_padding': False, 'fuse_qk_norm_rope_kvcache': False}, 'max_cudagraph_capture_size': 512, 'dynamic_shapes_config': {'type': <DynamicShapesType.BACKED: 'backed'>, 'evaluate_guards': False, 'assume_32_bit_indexing': False}, 'local_cache_dir': None, 'fast_moe_cold_start': False, 'static_all_moe_layers': ['model.layers.0.ffn.experts', 'model.layers.1.ffn.experts', 'model.layers.2.ffn.experts', 'model.layers.3.ffn.experts', 'model.layers.4.ffn.experts', 'model.layers.5.ffn.experts', 'model.layers.6.ffn.experts', 'model.layers.7.ffn.experts', 'model.layers.8.ffn.experts', 'model.layers.9.ffn.experts', 'model.layers.10.ffn.experts', 'model.layers.11.ffn.experts', 'model.layers.12.ffn.experts', 'model.layers.13.ffn.experts', 'model.layers.14.ffn.experts', 'model.layers.15.ffn.experts', 'model.layers.16.ffn.experts', 'model.layers.17.ffn.experts', 'model.layers.18.ffn.experts', 'model.layers.19.ffn.experts', 'model.layers.20.ffn.experts', 'model.layers.21.ffn.experts', 'model.layers.22.ffn.experts', 'model.layers.23.ffn.experts', 'model.layers.24.ffn.experts', 'model.layers.25.ffn.experts', 'model.layers.26.ffn.experts', 'model.layers.27.ffn.experts', 'model.layers.28.ffn.experts', 'model.layers.29.ffn.experts', 'model.layers.30.ffn.experts', 'model.layers.31.ffn.experts', 'model.layers.32.ffn.experts', 'model.layers.33.ffn.experts', 'model.layers.34.ffn.experts', 'model.layers.35.ffn.experts', 'model.layers.36.ffn.experts', 'model.layers.37.ffn.experts', 'model.layers.38.ffn.experts', 'model.layers.39.ffn.experts', 'model.layers.40.ffn.experts', 'model.layers.41.ffn.experts', 'model.layers.42.ffn.experts', 'model.layers.43.ffn.experts', 'model.layers.44.ffn.experts', 'model.layers.45.ffn.experts']}, kernel_config=KernelConfig(ir_op_priority=IrOpPriorityConfig(rms_norm=['vllm_c', 'native'], fused_add_rms_norm=['vllm_c', 'native']), enable_flashinfer_autotune=True, enable_cutedsl_warmup=True, enable_bf16x3_router_gemm=False, moe_backend='auto', linear_backend='auto'), 
(EngineCore pid=57666) ERROR 08-06 21:18:16 [dump_input.py:79] Dumping scheduler output for model execution: SchedulerOutput(scheduled_new_reqs=[NewRequestData(req_id=chatcmpl-8f90170a1b9374de-abf4985b,prompt_token_ids_len=1420,prefill_token_ids_len=1420,mm_features=[],sampling_params=SamplingParams(n=1, presence_penalty=0.0, frequency_penalty=0.0, repetition_penalty=1.0, temperature=1.0, top_p=1.0, top_k=0, min_p=0.0, seed=None, stop=[], stop_token_ids=[], bad_words=[], thinking_token_budget=None, include_stop_str_in_output=False, ignore_eos=False, max_tokens=64116, min_tokens=0, logprobs=None, prompt_logprobs=None, skip_special_tokens=False, spaces_between_special_tokens=True, structured_outputs=None, extra_args=None),block_ids=([1, 2, 3, 770, 496, 426], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 773, 826, 425, 424, 423, 422, 421, 420, 419], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 776, 825, 418, 417, 416, 415, 414, 413, 412], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 320, 752, 411, 410, 409, 408, 407, 406, 405, 404, 403, 402, 268, 315, 314, 313, 312, 311, 310, 309, 308, 307, 306, 305, 288, 287, 286, 285, 284, 283, 282, 281, 280, 279, 278, 277, 276, 275, 274, 273, 267, 266, 265, 264, 263, 262, 261, 260, 259, 258, 257, 256, 255, 254, 253, 252, 251, 250, 249, 248, 247, 246, 245, 244, 243, 242, 241, 240, 239, 238, 237, 236, 235, 234, 233, 232, 231, 230, 229, 228, 227, 224, 223, 222, 221, 220, 219, 218, 217, 216, 215, 214, 213, 212, 211, 210, 209, 208, 207, 206, 205, 204, 203], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 463, 464, 465, 841, 842, 843, 844, 319, 822, 818, 445, 749, 824, 345, 832, 392, 202, 201, 200, 199, 198, 197, 196, 195, 194, 193, 192, 191, 190, 189, 188, 187, 186, 185, 184, 183, 182, 181, 180, 179, 178, 177, 176, 175, 174, 173, 172, 171, 170, 169, 168, 167, 166, 165, 164, 163, 160, 159, 158, 157, 156, 155, 154, 153, 152, 151, 150]),num_computed_tokens=1024,lora_request=None,prompt_embeds_shape=None)], scheduled_cached_reqs=CachedRequestData(req_ids=['chatcmpl-b2c3d4f7c17f3b40-87b62096', 'chatcmpl-a28c01c1507183dc-9b59b676', 'chatcmpl-8a9ed2ec2332e9b5-8951b03a', 'chatcmpl-a8d58c81437cb0f8-a4fc161f', 'chatcmpl-a490e08100cb8cb2-8ad53edf', 'chatcmpl-8ee6909782f864ca-89950a6c', 'chatcmpl-b743056e88f73457-82906905'],resumed_req_ids=set(),new_token_ids_lens=[],all_token_ids_lens={},new_block_ids=[None, ([], [], [], [458, 785], [427]), None, ([], [], [], [734, 514], [662]), ([], [], [], [728], []), ([], [], [], [910], []), None],num_computed_tokens=[1245, 1442, 1355, 1443, 1248, 1297, 1345],num_output_tokens=[304, 503, 415, 505, 309, 357, 405]), num_scheduled_tokens={chatcmpl-8a9ed2ec2332e9b5-8951b03a: 8, chatcmpl-a490e08100cb8cb2-8ad53edf: 8, chatcmpl-a28c01c1507183dc-9b59b676: 8, chatcmpl-a8d58c81437cb0f8-a4fc161f: 8, chatcmpl-8ee6909782f864ca-89950a6c: 8, chatcmpl-b743056e88f73457-82906905: 8, chatcmpl-8f90170a1b9374de-abf4985b: 396, chatcmpl-b2c3d4f7c17f3b40-87b62096: 8}, total_num_scheduled_tokens=452, scheduled_spec_decode_tokens={chatcmpl-8a9ed2ec2332e9b5-8951b03a: [-1, -1, -1, -1, -1, -1, -1], chatcmpl-a490e08100cb8cb2-8ad53edf: [-1, -1, -1, -1, -1, -1, -1], chatcmpl-a28c01c1507183dc-9b59b676: [-1, -1, -1, -1, -1, -1, -1], chatcmpl-a8d58c81437cb0f8-a4fc161f: [-1, -1, -1, -1, -1, -1, -1], chatcmpl-b2c3d4f7c17f3b40-87b62096: [-1, -1, -1, -1, -1, -1, -1], chatcmpl-8ee6909782f864ca-89950a6c: [-1, -1, -1, -1, -1, -1, -1], chatcmpl-b743056e88f73457-82906905: [-1, -1, -1, -1, -1, -1, -1]}, scheduled_encoder_inputs={}, num_common_prefix_blocks=[3, 0, 0, 0, 0], finished_req_ids=[], free_encoder_mm_hashes=[], scheduled_encoder_input_stats=null, preempted_req_ids=[], has_structured_output_requests=false, pending_structured_output_tokens=false, num_invalid_spec_tokens=null, kv_connector_metadata=null, ec_connector_metadata=null, new_block_ids_to_zero=null, kv_cache_block_copies=null, num_spec_tokens_to_schedule=7)
(EngineCore pid=57666) ERROR 08-06 21:18:16 [dump_input.py:81] Dumping scheduler stats: SchedulerStats(num_running_reqs=8, num_waiting_reqs=0, num_skipped_waiting_reqs=0, step_counter=0, current_wave=0, kv_cache_usage=0.0052161039982420165, iteration_details=None, prefix_cache_stats=PrefixCacheStats(reset=False, requests=1, queries=1420, hits=1024, preempted_requests=0, preempted_queries=0, preempted_hits=0), connector_prefix_cache_stats=None, kv_cache_eviction_events=[], spec_decoding_stats=None, kv_connector_stats=None, waiting_lora_adapters={}, running_lora_adapters={}, cudagraph_stats=None, perf_stats=None)
(EngineCore pid=57666) ERROR 08-06 21:18:16 [core.py:1332] EngineCore encountered a fatal error.
(EngineCore pid=57666) ERROR 08-06 21:18:16 [core.py:1332] Traceback (most recent call last):
(EngineCore pid=57666) ERROR 08-06 21:18:16 [core.py:1332]   File "/MODELS/.venv/lib/python3.12/site-packages/vllm/v1/engine/core.py", line 1323, in run_engine_core
(EngineCore pid=57666) ERROR 08-06 21:18:16 [core.py:1332]     engine_core.run_busy_loop()
(EngineCore pid=57666) ERROR 08-06 21:18:16 [core.py:1332]   File "/MODELS/.venv/lib/python3.12/site-packages/vllm/v1/engine/core.py", line 1364, in run_busy_loop
(EngineCore pid=57666) ERROR 08-06 21:18:16 [core.py:1332]     self._process_engine_step()
(EngineCore pid=57666) ERROR 08-06 21:18:16 [core.py:1332]   File "/MODELS/.venv/lib/python3.12/site-packages/vllm/v1/engine/core.py", line 1403, in _process_engine_step
(EngineCore pid=57666) ERROR 08-06 21:18:16 [core.py:1332]     outputs, model_executed = self.step_fn()
(EngineCore pid=57666) ERROR 08-06 21:18:16 [core.py:1332]                               ^^^^^^^^^^^^^^
(EngineCore pid=57666) ERROR 08-06 21:18:16 [core.py:1332]   File "/MODELS/.venv/lib/python3.12/site-packages/vllm/v1/engine/core.py", line 647, in step_with_batch_queue
(EngineCore pid=57666) ERROR 08-06 21:18:16 [core.py:1332]     exec_future = self.model_executor.execute_model(
(EngineCore pid=57666) ERROR 08-06 21:18:16 [core.py:1332]                   ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
(EngineCore pid=57666) ERROR 08-06 21:18:16 [core.py:1332]   File "/MODELS/.venv/lib/python3.12/site-packages/vllm/v1/executor/uniproc_executor.py", line 120, in execute_model
(EngineCore pid=57666) ERROR 08-06 21:18:16 [core.py:1332]     output.result()
(EngineCore pid=57666) ERROR 08-06 21:18:16 [core.py:1332]   File "/usr/lib/python3.12/concurrent/futures/_base.py", line 449, in result
(EngineCore pid=57666) ERROR 08-06 21:18:16 [core.py:1332]     return self.__get_result()
(EngineCore pid=57666) ERROR 08-06 21:18:16 [core.py:1332]            ^^^^^^^^^^^^^^^^^^^
(EngineCore pid=57666) ERROR 08-06 21:18:16 [core.py:1332]   File "/usr/lib/python3.12/concurrent/futures/_base.py", line 401, in __get_result
(EngineCore pid=57666) ERROR 08-06 21:18:16 [core.py:1332]     raise self._exception
(EngineCore pid=57666) ERROR 08-06 21:18:16 [core.py:1332]   File "/MODELS/.venv/lib/python3.12/site-packages/vllm/v1/executor/uniproc_executor.py", line 98, in collective_rpc
(EngineCore pid=57666) ERROR 08-06 21:18:16 [core.py:1332]     result = run_method(self.driver_worker, method, args, kwargs)
(EngineCore pid=57666) ERROR 08-06 21:18:16 [core.py:1332]              ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
(EngineCore pid=57666) ERROR 08-06 21:18:16 [core.py:1332]   File "/MODELS/.venv/lib/python3.12/site-packages/vllm/v1/serial_utils.py", line 510, in run_method
(EngineCore pid=57666) ERROR 08-06 21:18:16 [core.py:1332]     return func(*args, **kwargs)
(EngineCore pid=57666) ERROR 08-06 21:18:16 [core.py:1332]            ^^^^^^^^^^^^^^^^^^^^^
(EngineCore pid=57666) ERROR 08-06 21:18:16 [core.py:1332]   File "/MODELS/.venv/lib/python3.12/site-packages/vllm/v1/worker/worker_base.py", line 351, in execute_model
(EngineCore pid=57666) ERROR 08-06 21:18:16 [core.py:1332]     return self.worker.execute_model(scheduler_output)
(EngineCore pid=57666) ERROR 08-06 21:18:16 [core.py:1332]            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
(EngineCore pid=57666) ERROR 08-06 21:18:16 [core.py:1332]   File "/MODELS/.venv/lib/python3.12/site-packages/torch/utils/_contextlib.py", line 124, in decorate_context
(EngineCore pid=57666) ERROR 08-06 21:18:16 [core.py:1332]     return func(*args, **kwargs)
(EngineCore pid=57666) ERROR 08-06 21:18:16 [core.py:1332]            ^^^^^^^^^^^^^^^^^^^^^
(EngineCore pid=57666) ERROR 08-06 21:18:16 [core.py:1332]   File "/MODELS/.venv/lib/python3.12/site-packages/vllm/v1/worker/gpu_worker.py", line 1147, in execute_model
(EngineCore pid=57666) ERROR 08-06 21:18:16 [core.py:1332]     output = self.model_runner.execute_model(
(EngineCore pid=57666) ERROR 08-06 21:18:16 [core.py:1332]              ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
(EngineCore pid=57666) ERROR 08-06 21:18:16 [core.py:1332]   File "/MODELS/.venv/lib/python3.12/site-packages/torch/utils/_contextlib.py", line 124, in decorate_context
(EngineCore pid=57666) ERROR 08-06 21:18:16 [core.py:1332]     return func(*args, **kwargs)
(EngineCore pid=57666) ERROR 08-06 21:18:16 [core.py:1332]            ^^^^^^^^^^^^^^^^^^^^^
(EngineCore pid=57666) ERROR 08-06 21:18:16 [core.py:1332]   File "/MODELS/.venv/lib/python3.12/site-packages/vllm/v1/worker/gpu/model_runner.py", line 1356, in execute_model
(EngineCore pid=57666) ERROR 08-06 21:18:16 [core.py:1332]     model_output = self.cudagraph_manager.run_pw_graph(
(EngineCore pid=57666) ERROR 08-06 21:18:16 [core.py:1332]                    ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
(EngineCore pid=57666) ERROR 08-06 21:18:16 [core.py:1332]   File "/MODELS/.venv/lib/python3.12/site-packages/vllm/v1/worker/gpu/cudagraph_utils.py", line 414, in run_pw_graph
(EngineCore pid=57666) ERROR 08-06 21:18:16 [core.py:1332]     return self.breakable_cg_runner(**model_inputs)
(EngineCore pid=57666) ERROR 08-06 21:18:16 [core.py:1332]            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
(EngineCore pid=57666) ERROR 08-06 21:18:16 [core.py:1332]   File "/MODELS/.venv/lib/python3.12/site-packages/vllm/compilation/breakable_cudagraph.py", line 333, in __call__
(EngineCore pid=57666) ERROR 08-06 21:18:16 [core.py:1332]     return self._replay(entry, args, kwargs)
(EngineCore pid=57666) ERROR 08-06 21:18:16 [core.py:1332]            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
(EngineCore pid=57666) ERROR 08-06 21:18:16 [core.py:1332]   File "/MODELS/.venv/lib/python3.12/site-packages/vllm/compilation/breakable_cudagraph.py", line 423, in _replay
(EngineCore pid=57666) ERROR 08-06 21:18:16 [core.py:1332]     entry.capture.replay()
(EngineCore pid=57666) ERROR 08-06 21:18:16 [core.py:1332]   File "/MODELS/.venv/lib/python3.12/site-packages/vllm/compilation/breakable_cudagraph.py", line 214, in replay
(EngineCore pid=57666) ERROR 08-06 21:18:16 [core.py:1332]     r()
(EngineCore pid=57666) ERROR 08-06 21:18:16 [core.py:1332]   File "/MODELS/.venv/lib/python3.12/site-packages/vllm/compilation/breakable_cudagraph.py", line 115, in <lambda>
(EngineCore pid=57666) ERROR 08-06 21:18:16 [core.py:1332]     return capture.add_eager(lambda: fn(*weak_args, **weak_kwargs))
(EngineCore pid=57666) ERROR 08-06 21:18:16 [core.py:1332]                                      ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
(EngineCore pid=57666) ERROR 08-06 21:18:16 [core.py:1332]   File "/MODELS/.venv/lib/python3.12/site-packages/vllm/models/deepseek_v4/attention.py", line 511, in attention_impl
(EngineCore pid=57666) ERROR 08-06 21:18:16 [core.py:1332]     self.forward_mqa(q, kv, positions, out)
(EngineCore pid=57666) ERROR 08-06 21:18:16 [core.py:1332]   File "/MODELS/.venv/lib/python3.12/site-packages/vllm/models/deepseek_v4/nvidia/flashmla.py", line 126, in forward_mqa
(EngineCore pid=57666) ERROR 08-06 21:18:16 [core.py:1332]     self._forward_prefill(
(EngineCore pid=57666) ERROR 08-06 21:18:16 [core.py:1332]   File "/MODELS/.venv/lib/python3.12/site-packages/vllm/models/deepseek_v4/nvidia/flashmla.py", line 339, in _forward_prefill
(EngineCore pid=57666) ERROR 08-06 21:18:16 [core.py:1332]     flash_mla_sparse_fwd(
(EngineCore pid=57666) ERROR 08-06 21:18:16 [core.py:1332]   File "/MODELS/.venv/lib/python3.12/site-packages/vllm/third_party/flashmla/flash_mla_interface.py", line 217, in flash_mla_sparse_fwd
(EngineCore pid=57666) ERROR 08-06 21:18:16 [core.py:1332]     results = flash_mla_cuda.sparse_prefill_fwd(
(EngineCore pid=57666) ERROR 08-06 21:18:16 [core.py:1332]               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
(EngineCore pid=57666) ERROR 08-06 21:18:16 [core.py:1332]   File "/MODELS/.venv/lib/python3.12/site-packages/torch/_ops.py", line 1269, in __call__
(EngineCore pid=57666) ERROR 08-06 21:18:16 [core.py:1332]     return self._op(*args, **kwargs)
(EngineCore pid=57666) ERROR 08-06 21:18:16 [core.py:1332]            ^^^^^^^^^^^^^^^^^^^^^^^^^
(EngineCore pid=57666) ERROR 08-06 21:18:16 [core.py:1332] RuntimeError: Assertion error (/workspace/.deps/flashmla-src/csrc/sm100/prefill/sparse/fwd/head64/instantiations/../phase1.cuh:651): Assertion `res == CUresult::CUDA_SUCCESS` failed.
(APIServer pid=57071) ERROR 08-06 21:18:16 [async_llm.py:704] AsyncLLM output_handler failed.
(APIServer pid=57071) ERROR 08-06 21:18:16 [async_llm.py:704] Traceback (most recent call last):
(APIServer pid=57071) ERROR 08-06 21:18:16 [async_llm.py:704]   File "/MODELS/.venv/lib/python3.12/site-packages/vllm/v1/engine/async_llm.py", line 660, in output_handler
(APIServer pid=57071) ERROR 08-06 21:18:16 [async_llm.py:704]     outputs = await engine_core.get_output_async()
(APIServer pid=57071) ERROR 08-06 21:18:16 [async_llm.py:704]               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
(APIServer pid=57071) ERROR 08-06 21:18:16 [async_llm.py:704]   File "/MODELS/.venv/lib/python3.12/site-packages/vllm/v1/engine/core_client.py", line 1061, in get_output_async
(APIServer pid=57071) ERROR 08-06 21:18:16 [async_llm.py:704]     raise self._format_exception(outputs) from None
(APIServer pid=57071) ERROR 08-06 21:18:16 [async_llm.py:704] vllm.v1.engine.exceptions.EngineDeadError: EngineCore encountered an issue. See stack trace (above) for the root cause.
(APIServer pid=57071) INFO:     127.0.0.1:54536 - "POST /v1/chat/completions HTTP/1.1" 500 Internal Server Error
(APIServer pid=57071) INFO:     127.0.0.1:54544 - "POST /v1/chat/completions HTTP/1.1" 500 Internal Server Error
(APIServer pid=57071) INFO:     127.0.0.1:54554 - "POST /v1/chat/completions HTTP/1.1" 500 Internal Server Error
(APIServer pid=57071) INFO:     127.0.0.1:54564 - "POST /v1/chat/completions HTTP/1.1" 500 Internal Server Error
(APIServer pid=57071) INFO:     127.0.0.1:54578 - "POST /v1/chat/completions HTTP/1.1" 500 Internal Server Error
(APIServer pid=57071) INFO:     127.0.0.1:54592 - "POST /v1/chat/completions HTTP/1.1" 500 Internal Server Error
(APIServer pid=57071) INFO:     127.0.0.1:54622 - "POST /v1/chat/completions HTTP/1.1" 500 Internal Server Error
(APIServer pid=57071) INFO:     127.0.0.1:54608 - "POST /v1/chat/completions HTTP/1.1" 500 Internal Server Error
(APIServer pid=57071) INFO:     Shutting down
(APIServer pid=57071) INFO:     Waiting for application shutdown.
(APIServer pid=57071) INFO:     Application shutdown complete.
(APIServer pid=57071) INFO:     Finished server process [57071]
(APIServer pid=57071) INFO 08-06 21:18:16 [core_client.py:655] [shutdown] MPClient: start timeout=0s
```
</details>



---

# Bonus Round - Resuming a Runpod

> 6 minutes from start to serving

Ensuring the /workspace is the location of the .venv (and understanding the .cache) , you can effectively "pre-load" some of the compilation

Compatibility caveat, this specific environment:

* B300 / sm_103a
* CUDA 13.0
* installed FlashInfer version
* PyTorch 2.11.0 cu130
* vLLM 0.26.0
* specific kernel parameters and shapes

Especially copy the cache after Auto-Tuner completes:

* downloaded CUBINs
* autotuning results
* kernel selection decisions

```
cd /root/
tar czf compiled-b300-flashinfer-vllm.tar.gz .cache/
scp -P 34567 -i ~/.ssh/MYKEY root@192.168.1.111:compiled-b300-flashinfer-vllm-autotuned.tar.gz . 
```

Since this is an ephemeral box, when "resuming", you do still have to reinstall dependencies and download the weights which is a few mins work (could probably optimize by persisting those too).

```
cd /root
mv .cache BAK-cache
cp -a /workspace/CACHES/autotuned ./.cache
```

Then use the "vllm serve" command from before. =)

## Resumed is faster - Summarized Logs

```
(APIServer pid=83224) INFO 08-04 23:38:48 [api_utils.py:345]  ▄▄ ▄█ █     █     █ ▀▄▀ █  version 0.26.0
(APIServer pid=83224) INFO 08-04 23:38:48 [api_utils.py:345]   █▄█▀ █     █     █     █  model   /MODELS/DeepSeek-V4-Flash-0731
...
(EngineCore pid=83803) INFO 08-04 23:39:02 [weight_utils.py:869] Filesystem type for checkpoints: OVERLAY. Checkpoint size: 155.43 GiB. Available RAM: 3878.54 GiB.
...
(EngineCore pid=83803) INFO 08-04 23:42:30 [default_loader.py:430] Loading weights took 208.71 seconds
(EngineCore pid=83803) INFO 08-04 23:42:50 [dspark.py:457] DSpark draft model loaded: 96 params
(EngineCore pid=83803) INFO 08-04 23:42:50 [default_loader.py:430] Loading weights took 14.68 seconds
(EngineCore pid=83803) INFO 08-04 23:42:51 [model_runner.py:305] Model loading took 156.32 GiB and 231.038859 seconds
(EngineCore pid=83803) INFO 08-04 23:42:51 [topk_topp_sampler.py:55] Using FlashInfer for top-p & top-k sampling.
(EngineCore pid=83803) INFO 08-04 23:42:57 [gpu_worker.py:560] Available KV cache memory: 85.79 GiB
(EngineCore pid=83803) INFO 08-04 23:42:57 [kv_cache_utils.py:2177] GPU KV cache size: 8,930,229 tokens
...
(EngineCore pid=83803) INFO 08-04 23:43:02 [kernel_warmup.py:227] Using FlashInfer autotune cache file: /root/.cache/vllm/flashinfer_autotune_cache/0.6.14/103a/48785467a4a82d91bbd3acb8ff1ef725fdb567020ab609a5fbe317032ff42b1f/autotune_configs.json
(EngineCore pid=83803) INFO 08-04 23:43:51 [kernel_warmup.py:268] FlashInfer autotune cache loaded on rank 0 from /root/.cache/vllm/flashinfer_autotune_cache/0.6.14/103a/48785467a4a82d91bbd3acb8ff1ef725fdb567020ab609a5fbe317032ff42b1f/autotune_configs.json.
(EngineCore pid=83803) INFO 08-04 23:43:51 [kernel_warmup.py:65] Warming up ll_bf16 router GEMM kernels.
(APIServer pid=83224) INFO 08-04 23:44:13 [api_server.py:677] Starting vLLM server on http://127.0.0.1:8000
```

### Avoiding Gotchas with venv and recompilation

> hackers TIL

If you have moved any of the absolute filepaths in the ".venv", the "copy paste cache" will be considered "dirty" and loading will take a long time while it recompiles...

Like if you create a new ".venv" (even with the exact same commands)

```
cd /MODELS
uv venv
...
```

those **timestamps are newer** than the saved cache...

So fix the file timestamps with:

```
find /MODELS/.venv/lib/python3.12/site-packages -type f -exec touch -d '2026-08-01 00:00:00' {} +

cd fused_moe_trtllm_sm100/
source /MODELS/.venv/bin/activate

(MODELS) root@516783632cfe:~/.cache/flashinfer/0.6.14/103a/cached_ops/fused_moe_trtllm_sm100# ninja -d explain -n
ninja: no work to do.
```



# B300 with Gemma4 details

`hf download google/gemma-4-31B-it --local-dir /MODELS/gemma-4-31B-it`

`source .venv/bin/activate`

```shell
VLLM_USE_V2_MODEL_RUNNER=0 vllm serve google/gemma-4-31B-it \
  --dtype bfloat16 --max-model-len 16384 --gpu-memory-utilization 0.92 \
  --enable-auto-tool-choice --reasoning-parser gemma4 --tool-call-parser gemma4 \
  --default-chat-template-kwargs '{"enable_thinking":true}'  --limit-mm-per-prompt '{"image":0,"audio":0}' \
  --host 127.0.0.1    --port 8000
```

Expand for vLLM logs:
<details>
```
(APIServer pid=21333) INFO 08-06 20:09:49 [api_utils.py:345] 
(APIServer pid=21333) INFO 08-06 20:09:49 [api_utils.py:345]        █     █     █▄   ▄█
(APIServer pid=21333) INFO 08-06 20:09:49 [api_utils.py:345]  ▄▄ ▄█ █     █     █ ▀▄▀ █  version 0.26.0
(APIServer pid=21333) INFO 08-06 20:09:49 [api_utils.py:345]   █▄█▀ █     █     █     █  model   google/gemma-4-31B-it
(APIServer pid=21333) INFO 08-06 20:09:49 [api_utils.py:345]    ▀▀  ▀▀▀▀▀ ▀▀▀▀▀ ▀     ▀
(APIServer pid=21333) INFO 08-06 20:09:49 [api_utils.py:345] 
(APIServer pid=21333) INFO 08-06 20:09:49 [api_utils.py:273] non-default args: {'model_tag': 'google/gemma-4-31B-it', 'default_chat_template_kwargs': {'enable_thinking': True}, 'enable_auto_tool_choice': True, 'tool_call_parser': 'gemma4', 'host': '127.0.0.1', 'model': 'google/gemma-4-31B-it', 'dtype': 'bfloat16', 'max_model_len': 16384, 'reasoning_parser': 'gemma4', 'limit_mm_per_prompt': {'image': 0, 'audio': 0}}
config.json: 100%|█████████████████████████████| 4.62k/4.62k [00:00<00:00, 19.8MB/s]
(APIServer pid=21333) Warning: You are sending unauthenticated requests to the HF Hub. Please set a HF_TOKEN to enable higher rate limits and faster downloads.
processor_config.json: 100%|████████████████████| 1.69k/1.69k [00:00<00:00, 12.1MB/s]
(APIServer pid=21333) INFO 08-06 20:09:56 [model.py:623] Resolved architecture: Gemma4ForConditionalGeneration
(APIServer pid=21333) INFO 08-06 20:09:56 [model.py:1788] Using max model len 16384
tokenizer_config.json: 100%|██████████████████| 3.08k/3.08k [00:00<00:00, 15.2MB/s]
tokenizer.json: downloading bytes: ███████████████████████████████| 8.75MB,  844kB/s  
tokenizer.json: reconstructing file: 100%|███████████████| 32.2MB / 32.2MB, 3.12MB/s  
chat_template.jinja: 100%|██████████████████████| 18.7k/18.7k [00:00<00:00, 75.5MB/s]
(APIServer pid=21333) INFO 08-06 20:10:01 [scheduler.py:252] Chunked prefill is enabled with max_num_batched_tokens=8192.
(APIServer pid=21333) INFO 08-06 20:10:01 [config.py:231] Gemma4 model has heterogeneous head dimensions (head_dim=256, global_head_dim=512). Using FA4 for all layers to avoid mixed FA3/FA4 penalty.
(APIServer pid=21333) INFO 08-06 20:10:01 [vllm.py:1109] Asynchronous scheduling is enabled.
(APIServer pid=21333) INFO 08-06 20:10:01 [kernel.py:295] Final IR op priority after setting platform defaults: IrOpPriorityConfig(rms_norm=['native'], fused_add_rms_norm=['native'])
(APIServer pid=21333) WARNING 08-06 20:10:01 [cuda.py:323] Forcing --disable_chunked_mm_input for models with multimodal-bidirectional attention.
generation_config.json: 100%|███████████████████████| 208/208 [00:00<00:00, 1.89MB/s]
(EngineCore pid=22228) INFO 08-06 20:10:11 [core.py:116] Initializing a V1 LLM engine (v0.26.0) with config: model='google/gemma-4-31B-it', speculative_config=None, tokenizer='google/gemma-4-31B-it', skip_tokenizer_init=False, tokenizer_mode=auto, revision=None, tokenizer_revision=None, trust_remote_code=False, dtype=torch.bfloat16, max_seq_len=16384, download_dir=None, load_format=auto, tensor_parallel_size=1, pipeline_parallel_size=1, data_parallel_size=1, decode_context_parallel_size=1, dcp_comm_backend=ag_rs, disable_custom_all_reduce=False, quantization=None, quantization_config=None, enforce_eager=False, enable_return_routed_experts=False, kv_cache_dtype=auto, device_config=cuda, structured_outputs_config=StructuredOutputsConfig(backend='auto', disable_any_whitespace=False, disable_additional_properties=False, reasoning_parser='gemma4', reasoning_parser_plugin='', enable_in_reasoning=False), observability_config=ObservabilityConfig(show_hidden_metrics_for_version=None, otlp_traces_endpoint=None, collect_detailed_traces=None, kv_cache_metrics=False, kv_cache_metrics_sample=0.01, cudagraph_metrics=False, enable_layerwise_nvtx_tracing=False, enable_mfu_metrics=False, enable_mm_processor_stats=False, enable_logging_iteration_details=False, jit_monitor_mode='warn', jit_monitor_verbose=False), seed=0, served_model_name=google/gemma-4-31B-it, enable_prefix_caching=True, enable_chunked_prefill=True, pooler_config=None, compilation_config={'mode': <CompilationMode.VLLM_COMPILE: 3>, 'debug_dump_path': None, 'cache_dir': '', 'compile_cache_save_format': 'binary', 'backend': 'inductor', 'custom_ops': ['none'], 'ir_enable_torch_wrap': True, 'splitting_ops': ['vllm::unified_attention_with_output', 'vllm::unified_mla_attention_with_output', 'vllm::mamba_mixer2', 'vllm::mamba_mixer', 'vllm::short_conv', 'vllm::linear_attention', 'vllm::plamo2_mamba_mixer', 'vllm::qwen_gdn_attention_core', 'vllm::gdn_attention_core_xpu', 'vllm::olmo_hybrid_gdn_full_forward', 'vllm::kda_attention', 'vllm::sparse_attn_indexer', 'vllm::rocm_aiter_sparse_attn_indexer', 'vllm::deepseek_v4_attention', 'vllm::hpc_rope_norm_forward', 'vllm::unified_kv_cache_update', 'vllm::unified_mla_kv_cache_update'], 'compile_mm_encoder': False, 'cudagraph_mm_encoder': False, 'encoder_cudagraph_token_budgets': [], 'encoder_cudagraph_max_vision_items_per_batch': 0, 'encoder_cudagraph_max_frames_per_batch': None, 'compile_sizes': [], 'compile_ranges_endpoints': [8192], 'inductor_compile_config': {'enable_auto_functionalized_v2': False, 'size_asserts': False, 'alignment_asserts': False, 'scalar_asserts': False, 'combo_kernels': True, 'benchmark_combo_kernel': True}, 'inductor_passes': {}, 'cudagraph_mode': <CUDAGraphMode.FULL_AND_PIECEWISE: (2, 1)>, 'cudagraph_num_of_warmups': 1, 'cudagraph_capture_sizes': [1, 2, 4, 8, 16, 24, 32, 40, 48, 56, 64, 72, 80, 88, 96, 104, 112, 120, 128, 136, 144, 152, 160, 168, 176, 184, 192, 200, 208, 216, 224, 232, 240, 248, 256, 272, 288, 304, 320, 336, 352, 368, 384, 400, 416, 432, 448, 464, 480, 496, 512], 'cudagraph_copy_inputs': False, 'cudagraph_specialize_lora': True, 'use_inductor_graph_partition': False, 'pass_config': {'fuse_norm_quant': False, 'fuse_act_quant': False, 'fuse_attn_quant': False, 'enable_sp': False, 'fuse_gemm_comms': False, 'fuse_allreduce_rms': False, 'enable_qk_norm_rope_fusion': False, 'fuse_rope_kvcache_cat_mla': False, 'fuse_act_padding': False, 'fuse_qk_norm_rope_kvcache': False}, 'max_cudagraph_capture_size': 512, 'dynamic_shapes_config': {'type': <DynamicShapesType.BACKED: 'backed'>, 'evaluate_guards': False, 'assume_32_bit_indexing': False}, 'local_cache_dir': None, 'fast_moe_cold_start': False, 'static_all_moe_layers': []}, kernel_config=KernelConfig(ir_op_priority=IrOpPriorityConfig(rms_norm=['native'], fused_add_rms_norm=['native']), enable_flashinfer_autotune=True, enable_cutedsl_warmup=True, enable_bf16x3_router_gemm=False, moe_backend='auto', linear_backend='auto')
(EngineCore pid=22228) Warning: You are sending unauthenticated requests to the HF Hub. Please set a HF_TOKEN to enable higher rate limits and faster downloads.
(EngineCore pid=22228) INFO 08-06 20:10:16 [parallel_state.py:1615] world_size=1 rank=0 local_rank=0 distributed_init_method=tcp://172.21.0.2:44813 backend=nccl
(EngineCore pid=22228) INFO 08-06 20:10:16 [parallel_state.py:1946] rank 0 in world size 1 is assigned as DP rank 0, PP rank 0, PCP rank 0, TP rank 0, EP rank N/A, EPLB rank N/A
(EngineCore pid=22228) INFO 08-06 20:10:19 [topk_topp_sampler.py:55] Using FlashInfer for top-p & top-k sampling.
(EngineCore pid=22228) INFO 08-06 20:10:19 [gpu_model_runner.py:5250] Starting to load model google/gemma-4-31B-it...
(EngineCore pid=22228) INFO 08-06 20:10:27 [vllm.py:1109] Asynchronous scheduling is enabled.
(EngineCore pid=22228) INFO 08-06 20:10:27 [kernel.py:295] Final IR op priority after setting platform defaults: IrOpPriorityConfig(rms_norm=['native'], fused_add_rms_norm=['native'])
(EngineCore pid=22228) WARNING 08-06 20:10:28 [fa_utils.py:245] FA4 on Blackwell does not support head_size=256 due to TMEM capacity limits, defaulting to FA version 2.
(EngineCore pid=22228) INFO 08-06 20:10:28 [cuda.py:482] Using TRITON_ATTN attention backend out of potential backends: ['TRITON_ATTN', 'FLEX_ATTENTION'].
(EngineCore pid=22228) WARNING 08-06 20:10:28 [fa_utils.py:245] FA4 on Blackwell does not support head_size=512 due to TMEM capacity limits, defaulting to FA version 2.
model.safetensors.index.json: 100%|████████████████| 120k/120k [00:00<00:00, 229MB/s]
(EngineCore pid=22228) INFO 08-06 20:11:33 [weight_utils.py:530] Time spent downloading weights for google/gemma-4-31B-it: 64.511670 seconds
(EngineCore pid=22228) INFO 08-06 20:11:33 [weight_utils.py:869] Filesystem type for checkpoints: EXT4. Checkpoint size: 58.25 GiB. Available RAM: 3902.01 GiB.
(EngineCore pid=22228) INFO 08-06 20:11:33 [weight_utils.py:892] Auto-prefetch is disabled because the filesystem (EXT4) is not a recognized network FS (NFS/Lustre). If you want to force prefetching, start vLLM with --safetensors-load-strategy=prefetch.
Loading safetensors checkpoint shards:   0% Completed | 0/2 [00:00<?, ?it/s]
Loading safetensors checkpoint shards:  50% Completed | 1/2 [00:11<00:11, 11.63s/it]
Loading safetensors checkpoint shards: 100% Completed | 2/2 [00:16<00:00,  8.33s/it]
(EngineCore pid=22228) 
(EngineCore pid=22228) INFO 08-06 20:11:51 [default_loader.py:430] Loading weights took 17.24 seconds
(EngineCore pid=22228) INFO 08-06 20:11:51 [gpu_model_runner.py:5347] Model loading took 58.99 GiB memory and 91.155902 seconds
(EngineCore pid=22228) INFO 08-06 20:11:51 [gpu_model_runner.py:6396] Encoder cache will be initialized with a budget of 8192 tokens, and profiled with 3 video items of the maximum feature size.
(EngineCore pid=22228) INFO 08-06 20:13:08 [backends.py:1094] Using cache directory: /root/.cache/vllm/torch_compile_cache/8d578ca0fc/rank_0_0/backbone for vLLM's torch.compile
(EngineCore pid=22228) INFO 08-06 20:13:08 [backends.py:1155] Dynamo bytecode transform time: 10.42 s
(EngineCore pid=22228) INFO 08-06 20:13:15 [backends.py:378] Cache the graph of compile range (1, 8192) for later use
(EngineCore pid=22228) INFO 08-06 20:13:29 [backends.py:393] Compiling a graph for compile range (1, 8192) takes 21.13 s
(EngineCore pid=22228) INFO 08-06 20:13:36 [decorators.py:708] saved AOT compiled function to /root/.cache/vllm/torch_compile_cache/torch_aot_compile/d99b59af82e7ded5eea6560b042756b0790e35bdd095ba200803e57b68099628/rank_0_0/model
(EngineCore pid=22228) INFO 08-06 20:13:36 [monitor.py:53] torch.compile took 38.33 s in total
(EngineCore pid=22228) INFO 08-06 20:13:36 [monitor.py:81] Initial profiling/warmup run took 0.65 s
(EngineCore pid=22228) INFO 08-06 20:14:48 [gpu_model_runner.py:6612] Profiling CUDA graph memory: PIECEWISE=51 (largest=512), FULL=51 (largest=512)
(EngineCore pid=22228) INFO 08-06 20:14:51 [gpu_model_runner.py:6737] Estimated CUDA graph memory: 0.76 GiB total
(EngineCore pid=22228) INFO 08-06 20:14:51 [gpu_worker.py:560] Available KV cache memory: 182.37 GiB
(EngineCore pid=22228) INFO 08-06 20:14:51 [gpu_worker.py:575] CUDA graph memory profiling is enabled (default since v0.21.0). The current --gpu-memory-utilization=0.9200 is equivalent to --gpu-memory-utilization=0.9172 without CUDA graph memory profiling. To maintain the same effective KV cache size as before, increase --gpu-memory-utilization to 0.9228. To disable, set VLLM_MEMORY_PROFILER_ESTIMATE_CUDAGRAPHS=0.
(EngineCore pid=22228) INFO 08-06 20:14:51 [kv_cache_utils.py:2177] GPU KV cache size: 217,116 tokens
(EngineCore pid=22228) INFO 08-06 20:14:51 [kv_cache_utils.py:2178] Maximum concurrency for 16,384 tokens per request: 13.25x
(EngineCore pid=22228) INFO 08-06 20:14:52 [kernel_warmup.py:227] Using FlashInfer autotune cache file: /root/.cache/vllm/flashinfer_autotune_cache/0.6.14/103a/4b6b9dbbef6906ef0e9dc77293035abe744648628b57f0a87c4171eac9b1c312/autotune_configs.json
(EngineCore pid=22228) 2026-08-06 20:14:52,092 - INFO - autotuner.py:651 - flashinfer.jit: [Autotuner]: Autotuning process starts ...
(EngineCore pid=22228) 2026-08-06 20:14:52,113 - INFO - autotuner.py:674 - flashinfer.jit: [Autotuner]: Autotuning process ends
(EngineCore pid=22228) WARNING 08-06 20:14:52 [kernel_warmup.py:258] No FlashInfer autotune cache entries found.Falling back to default tactics.
(EngineCore pid=22228) INFO 08-06 20:14:52 [kernel_warmup.py:65] Warming up ll_bf16 router GEMM kernels.
(EngineCore pid=22228) INFO 08-06 20:15:00 [cutedsl_warmup.py:101] Skipping CuTeDSL warmup because no compile units were requested.
(EngineCore pid=22228) INFO 08-06 20:15:00 [gpu_model_runner.py:6798] Rank 0: Torch profiler disabled for CUDA graph capture
Capturing CUDA graphs (mixed prefill-decode, PIECEWISE): 100%|█████████████████████████████████| 51/51 [00:07<00:00,  6.91it/s]
Capturing CUDA graphs (decode, FULL): 100%|███████████| 51/51 [00:09<00:00,  5.58it/s]
(EngineCore pid=22228) INFO 08-06 20:15:17 [gpu_model_runner.py:6844] Graph capturing finished in 18 secs, took 0.70 GiB
(EngineCore pid=22228) INFO 08-06 20:15:17 [gpu_worker.py:793] CUDA graph pool memory: 0.7 GiB (actual), 0.76 GiB (estimated), difference: 0.06 GiB (8.1%).
(EngineCore pid=22228) INFO 08-06 20:15:17 [gpu_worker.py:857] Free memory on device (267.08/267.69 GiB) on startup. Desired GPU memory utilization is (0.92, 246.27 GiB). Actual usage is 58.99 GiB for weight, 3.9 GiB for peak activation, 0.25 GiB for non-torch memory, and 0.7 GiB for CUDAGraph memory. Replace gpu_memory_utilization config with `--kv-cache-memory=195725302211` (182.28 GiB) to fit into requested memory, or `--kv-cache-memory=218063512576` (203.09 GiB) to fully utilize gpu memory. Current kv cache memory in use is 182.37 GiB.
(EngineCore pid=22228) INFO 08-06 20:15:18 [jit_monitor.py:79] Kernel JIT monitor activated; monitored JIT compilations during inference will use mode=warn.
(EngineCore pid=22228) INFO 08-06 20:15:19 [core.py:340] init engine (profile, create kv cache, warmup model) took 207.63 s (compilation: 38.33 s)
(EngineCore pid=22228) INFO 08-06 20:15:19 [kernel.py:295] Final IR op priority after setting platform defaults: IrOpPriorityConfig(rms_norm=['native'], fused_add_rms_norm=['native'])
(APIServer pid=21333) INFO 08-06 20:15:19 [api_server.py:673] Supported tasks: ['generate']
(APIServer pid=21333) INFO 08-06 20:15:19 [parser_manager.py:37] "auto" tool choice has been enabled.
(APIServer pid=21333) WARNING 08-06 20:15:20 [model.py:1546] Default vLLM sampling parameters have been overridden by the model's `generation_config.json`: `{'temperature': 1.0, 'top_k': 64, 'top_p': 0.95}`. If this is not intended, please relaunch vLLM instance with `--generation-config vllm`.
(APIServer pid=21333) INFO 08-06 20:15:25 [hf.py:540] Detected the chat template content format to be 'openai'. You can set `--chat-template-content-format` to override this.
(APIServer pid=21333) INFO 08-06 20:16:22 [base.py:236] Multi-modal warmup completed in 57.656s
(APIServer pid=21333) INFO 08-06 20:16:23 [base.py:236] Readonly multi-modal warmup completed in 0.376s
(APIServer pid=21333) INFO 08-06 20:16:23 [api_server.py:677] Starting vLLM server on http://127.0.0.1:8000
(APIServer pid=21333) INFO 08-06 20:16:23 [launcher.py:37] Available routes are:
(APIServer pid=21333) INFO 08-06 20:16:23 [launcher.py:46] Route: /inference/v1/generate, Methods: POST
(APIServer pid=21333) INFO:     Started server process [21333]
(APIServer pid=21333) INFO:     Waiting for application startup.
(APIServer pid=21333) INFO:     Application startup complete.

```
</details>


BF16 dense Gemma 4 using Triton attention, TRITON_ATTN, an intentional (automatic) compatibility fallback that's known to work.


## Harbor Terminal Bench Task
*(of course ssh tunnel)* `curl -s http://127.0.0.1:18000/v1/models | jq`

```
OPENAI_API_KEY=EMPTY
OPENAI_BASE_URL=http://localhost:18000/v1

harbor run -d terminal-bench/terminal-bench-2-1 --agent terminus-2 --model openai/google/gemma-4-31B-it --include-task-name terminal-bench/regex-log -k 8 -n 8

⠸ 0/8 Running trials... ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 0:00:22 -:--:--
⠧ 0:00:19 regex-log__wrA3poy: starting environment...
⠧ 0:00:19 regex-log__Vffh7JH: starting environment...
⠧ 0:00:18 regex-log__sTXeCoZ: starting environment...
⠧ 0:00:18 regex-log__w456Dx7: starting environment...


...

  8/8 Mean: 1.000 ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 0:11:41 0:00:00

terminal-bench/terminal-bench-2-1 • terminus-2 • google/gemma-4-31B-it
┏━━━━━━━━┳━━━━━━━━━━━━┳━━━━━━━┳━━━━━━━━┳━━━━━━━━┳━━━━━━━━┳━━━━━━━━┓
┃ Trials ┃ Exceptions ┃  Mean ┃ Pass@2 ┃ Pass@4 ┃ Pass@5 ┃ Pass@8 ┃
┡━━━━━━━━╇━━━━━━━━━━━━╇━━━━━━━╇━━━━━━━━╇━━━━━━━━╇━━━━━━━━╇━━━━━━━━┩
│      8 │          0 │ 1.000 │  1.000 │  1.000 │  1.000 │  1.000 │
└────────┴────────────┴───────┴────────┴────────┴────────┴────────┘

┏━━━━━━━━┳━━━━━━━┓
┃ Reward ┃ Count ┃
┡━━━━━━━━╇━━━━━━━┩
│ 1.0    │     8 │
└────────┴───────┘

Job Info Total runtime: 11m 41s
```

Expand for vLLM logs while the agents were running:
<details>

```
(APIServer pid=21333) INFO 08-06 20:19:53 [loggers.py:310] Engine 000: Avg prompt throughput: 130.8 tokens/s, Avg generation throughput: 472.8 tokens/s, Running: 8 reqs, Waiting: 0 reqs, GPU KV cache usage: 2.6%, Prefix cache hit rate: 83.7%
(APIServer pid=21333) INFO 08-06 20:20:03 [loggers.py:310] Engine 000: Avg prompt throughput: 0.0 tokens/s, Avg generation throughput: 509.6 tokens/s, Running: 8 reqs, Waiting: 0 reqs, GPU KV cache usage: 3.9%, Prefix cache hit rate: 83.7%
(APIServer pid=21333) INFO 08-06 20:20:13 [loggers.py:310] Engine 000: Avg prompt throughput: 0.0 tokens/s, Avg generation throughput: 503.9 tokens/s, Running: 8 reqs, Waiting: 0 reqs, GPU KV cache usage: 4.2%, Prefix cache hit rate: 83.7%
(APIServer pid=21333) INFO 08-06 20:20:23 [loggers.py:310] Engine 000: Avg prompt throughput: 0.0 tokens/s, Avg generation throughput: 495.2 tokens/s, Running: 8 reqs, Waiting: 0 reqs, GPU KV cache usage: 4.4%, Prefix cache hit rate: 83.7%
(APIServer pid=21333) INFO 08-06 20:20:33 [loggers.py:310] Engine 000: Avg prompt throughput: 0.0 tokens/s, Avg generation throughput: 488.8 tokens/s, Running: 8 reqs, Waiting: 0 reqs, GPU KV cache usage: 4.6%, Prefix cache hit rate: 83.7%
(APIServer pid=21333) INFO 08-06 20:20:43 [loggers.py:310] Engine 000: Avg prompt throughput: 0.0 tokens/s, Avg generation throughput: 487.2 tokens/s, Running: 8 reqs, Waiting: 0 reqs, GPU KV cache usage: 4.8%, Prefix cache hit rate: 83.7%
(APIServer pid=21333) INFO:     127.0.0.1:44582 - "POST /v1/chat/completions HTTP/1.1" 200 OK
(APIServer pid=21333) INFO 08-06 20:20:53 [loggers.py:310] Engine 000: Avg prompt throughput: 196.6 tokens/s, Avg generation throughput: 477.1 tokens/s, Running: 8 reqs, Waiting: 0 reqs, GPU KV cache usage: 4.9%, Prefix cache hit rate: 70.2%
(APIServer pid=21333) INFO 08-06 20:21:03 [loggers.py:310] Engine 000: Avg prompt throughput: 0.0 tokens/s, Avg generation throughput: 483.2 tokens/s, Running: 8 reqs, Waiting: 0 reqs, GPU KV cache usage: 5.1%, Prefix cache hit rate: 70.2%
(APIServer pid=21333) INFO 08-06 20:21:13 [loggers.py:310] Engine 000: Avg prompt throughput: 0.0 tokens/s, Avg generation throughput: 476.8 tokens/s, Running: 8 reqs, Waiting: 0 reqs, GPU KV cache usage: 5.3%, Prefix cache hit rate: 70.2%
(APIServer pid=21333) INFO 08-06 20:21:23 [loggers.py:310] Engine 000: Avg prompt throughput: 0.0 tokens/s, Avg generation throughput: 469.6 tokens/s, Running: 8 reqs, Waiting: 0 reqs, GPU KV cache usage: 5.5%, Prefix cache hit rate: 70.2%
(APIServer pid=21333) INFO 08-06 20:21:33 [loggers.py:310] Engine 000: Avg prompt throughput: 0.0 tokens/s, Avg generation throughput: 463.2 tokens/s, Running: 8 reqs, Waiting: 0 reqs, GPU KV cache usage: 5.7%, Prefix cache hit rate: 70.2%
(APIServer pid=21333) INFO:     127.0.0.1:44600 - "POST /v1/chat/completions HTTP/1.1" 200 OK
(APIServer pid=21333) INFO 08-06 20:21:43 [loggers.py:310] Engine 000: Avg prompt throughput: 128.6 tokens/s, Avg generation throughput: 450.1 tokens/s, Running: 8 reqs, Waiting: 0 reqs, GPU KV cache usage: 5.6%, Prefix cache hit rate: 65.6%
(APIServer pid=21333) INFO:     127.0.0.1:44578 - "POST /v1/chat/completions HTTP/1.1" 200 OK
(APIServer pid=21333) INFO 08-06 20:21:53 [loggers.py:310] Engine 000: Avg prompt throughput: 120.8 tokens/s, Avg generation throughput: 445.4 tokens/s, Running: 8 reqs, Waiting: 0 reqs, GPU KV cache usage: 5.6%, Prefix cache hit rate: 62.7%
(APIServer pid=21333) INFO:     127.0.0.1:44594 - "POST /v1/chat/completions HTTP/1.1" 200 OK
(APIServer pid=21333) INFO 08-06 20:22:03 [loggers.py:310] Engine 000: Avg prompt throughput: 205.5 tokens/s, Avg generation throughput: 435.8 tokens/s, Running: 8 reqs, Waiting: 0 reqs, GPU KV cache usage: 5.5%, Prefix cache hit rate: 57.7%
(APIServer pid=21333) INFO:     127.0.0.1:44608 - "POST /v1/chat/completions HTTP/1.1" 200 OK
(APIServer pid=21333) INFO 08-06 20:22:13 [loggers.py:310] Engine 000: Avg prompt throughput: 98.2 tokens/s, Avg generation throughput: 439.2 tokens/s, Running: 8 reqs, Waiting: 0 reqs, GPU KV cache usage: 5.4%, Prefix cache hit rate: 57.0%
(APIServer pid=21333) INFO:     127.0.0.1:44568 - "POST /v1/chat/completions HTTP/1.1" 200 OK
(APIServer pid=21333) INFO:     127.0.0.1:44582 - "POST /v1/chat/completions HTTP/1.1" 200 OK
(APIServer pid=21333) INFO 08-06 20:22:23 [loggers.py:310] Engine 000: Avg prompt throughput: 133.7 tokens/s, Avg generation throughput: 437.5 tokens/s, Running: 7 reqs, Waiting: 0 reqs, GPU KV cache usage: 4.5%, Prefix cache hit rate: 55.5%
(APIServer pid=21333) INFO 08-06 20:22:33 [loggers.py:310] Engine 000: Avg prompt throughput: 205.8 tokens/s, Avg generation throughput: 433.1 tokens/s, Running: 8 reqs, Waiting: 0 reqs, GPU KV cache usage: 5.3%, Prefix cache hit rate: 56.1%
(APIServer pid=21333) INFO:     127.0.0.1:44554 - "POST /v1/chat/completions HTTP/1.1" 200 OK
(APIServer pid=21333) INFO:     127.0.0.1:44564 - "POST /v1/chat/completions HTTP/1.1" 200 OK
(APIServer pid=21333) INFO 08-06 20:22:43 [loggers.py:310] Engine 000: Avg prompt throughput: 246.3 tokens/s, Avg generation throughput: 453.3 tokens/s, Running: 8 reqs, Waiting: 0 reqs, GPU KV cache usage: 4.7%, Prefix cache hit rate: 54.6%
(APIServer pid=21333) INFO 08-06 20:22:53 [loggers.py:310] Engine 000: Avg prompt throughput: 0.0 tokens/s, Avg generation throughput: 471.2 tokens/s, Running: 8 reqs, Waiting: 0 reqs, GPU KV cache usage: 4.9%, Prefix cache hit rate: 54.6%
(APIServer pid=21333) INFO 08-06 20:23:03 [loggers.py:310] Engine 000: Avg prompt throughput: 0.0 tokens/s, Avg generation throughput: 468.8 tokens/s, Running: 8 reqs, Waiting: 0 reqs, GPU KV cache usage: 5.1%, Prefix cache hit rate: 54.6%
(APIServer pid=21333) INFO:     127.0.0.1:44600 - "POST /v1/chat/completions HTTP/1.1" 200 OK
...


(APIServer pid=21333) INFO 08-06 20:28:03 [loggers.py:310] Engine 000: Avg prompt throughput: 125.0 tokens/s, Avg generation throughput: 61.2 tokens/s, Running: 1 reqs, Waiting: 0 reqs, GPU KV cache usage: 0.8%, Prefix cache hit rate: 69.5%
(APIServer pid=21333) INFO 08-06 20:28:13 [loggers.py:310] Engine 000: Avg prompt throughput: 0.0 tokens/s, Avg generation throughput: 65.7 tokens/s, Running: 1 reqs, Waiting: 0 reqs, GPU KV cache usage: 0.8%, Prefix cache hit rate: 69.5%
(APIServer pid=21333) INFO 08-06 20:28:23 [loggers.py:310] Engine 000: Avg prompt throughput: 0.0 tokens/s, Avg generation throughput: 64.9 tokens/s, Running: 1 reqs, Waiting: 0 reqs, GPU KV cache usage: 0.8%, Prefix cache hit rate: 69.5%
(APIServer pid=21333) INFO 08-06 20:28:33 [loggers.py:310] Engine 000: Avg prompt throughput: 0.0 tokens/s, Avg generation throughput: 64.2 tokens/s, Running: 1 reqs, Waiting: 0 reqs, GPU KV cache usage: 0.9%, Prefix cache hit rate: 69.5%
(APIServer pid=21333) INFO 08-06 20:28:43 [loggers.py:310] Engine 000: Avg prompt throughput: 0.0 tokens/s, Avg generation throughput: 64.0 tokens/s, Running: 1 reqs, Waiting: 0 reqs, GPU KV cache usage: 0.9%, Prefix cache hit rate: 69.5%

```
</details>


A second identical run:

```
harbor run -d terminal-bench/terminal-bench-2-1 --agent terminus-2 --model openai/google/gemma-4-31B-it --include-task-name terminal-bench/regex-log -k 8 -n 8

  8/8 Mean: 0.875 ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 0:07:49 0:00:00

terminal-bench/terminal-bench-2-1 • terminus-2 • google/gemma-4-31B-it
┏━━━━━━━━┳━━━━━━━━━━━━┳━━━━━━━┳━━━━━━━━┳━━━━━━━━┳━━━━━━━━┳━━━━━━━━┓
┃ Trials ┃ Exceptions ┃  Mean ┃ Pass@2 ┃ Pass@4 ┃ Pass@5 ┃ Pass@8 ┃
┡━━━━━━━━╇━━━━━━━━━━━━╇━━━━━━━╇━━━━━━━━╇━━━━━━━━╇━━━━━━━━╇━━━━━━━━┩
│      8 │          0 │ 0.875 │  1.000 │  1.000 │  1.000 │  1.000 │
└────────┴────────────┴───────┴────────┴────────┴────────┴────────┘

┏━━━━━━━━┳━━━━━━━┓
┃ Reward ┃ Count ┃
┡━━━━━━━━╇━━━━━━━┩
│ 1.0    │     7 │
│ 0.0    │     1 │
└────────┴───────┘

Job Info Total runtime: 7m 49s
```


---

# SUCCESS vLLM logs CUDAGraphMode FULL_AND_PIECEWISE


<details>
```

export VLLM_USE_DEEP_GEMM=1
export VLLM_USE_BREAKABLE_CUDAGRAPH=0

(MODELS) root@f31f388770e0:/MODELS# vllm serve /MODELS/DeepSeek-V4-Flash-0731   --served-model-name deepseek-v4-flash-0731   --host 127.0.0.1 --port 8000   --max-model-len 65536   --tokenizer-mode deepseek_v4   --reasoning-parser deepseek_v4   --tool-call-parser deepseek_v4   --enable-auto-tool-choice   --trust-remote-code --kv-cache-dtype fp8 --block-size 256   --enable-expert-parallel   --attention-config '{"use_fp4_indexer_cache": true}'   --speculative-config '{"method":"dspark","num_speculative_tokens":7,"draft_sample_method":"greedy"}'   2>&1 | tee /workspace/vllm-warmup.log
(APIServer pid=87905) INFO 08-06 21:23:15 [api_utils.py:345] 
(APIServer pid=87905) INFO 08-06 21:23:15 [api_utils.py:345]        █     █     █▄   ▄█
(APIServer pid=87905) INFO 08-06 21:23:15 [api_utils.py:345]  ▄▄ ▄█ █     █     █ ▀▄▀ █  version 0.26.0
(APIServer pid=87905) INFO 08-06 21:23:15 [api_utils.py:345]   █▄█▀ █     █     █     █  model   /MODELS/DeepSeek-V4-Flash-0731
(APIServer pid=87905) INFO 08-06 21:23:15 [api_utils.py:345]    ▀▀  ▀▀▀▀▀ ▀▀▀▀▀ ▀     ▀
(APIServer pid=87905) INFO 08-06 21:23:15 [api_utils.py:345] 
(APIServer pid=87905) INFO 08-06 21:23:15 [api_utils.py:273] non-default args: {'model_tag': '/MODELS/DeepSeek-V4-Flash-0731', 'enable_auto_tool_choice': True, 'tool_call_parser': 'deepseek_v4', 'host': '127.0.0.1', 'model': '/MODELS/DeepSeek-V4-Flash-0731', 'tokenizer_mode': 'deepseek_v4', 'trust_remote_code': True, 'max_model_len': 65536, 'served_model_name': ['deepseek-v4-flash-0731'], 'reasoning_parser': 'deepseek_v4', 'enable_expert_parallel': True, 'block_size': 256, 'kv_cache_dtype': 'fp8', 'speculative_config': {'method': 'dspark', 'num_speculative_tokens': 7, 'draft_sample_method': 'greedy'}, 'attention_config': AttentionConfig(backend=None, backend_per_kind={}, flash_attn_version=None, use_prefill_decode_attention=False, flash_attn_max_num_splits_for_cuda_graph=32, tq_max_kv_splits_for_cuda_graph=32, use_trtllm_attention=None, disable_flashinfer_q_quantization=False, mla_prefill_backend=None, use_prefill_query_quantization=False, use_fp4_indexer_cache=True, indexer_kv_dtype='bf16', use_non_causal=False, sparse_mla_force_mqa=False, flex_attn_block_m=None, flex_attn_block_n=None, flex_attn_q_block_size=None, flex_attn_kv_block_size=None)}
(APIServer pid=87905) INFO 08-06 21:23:15 [config.py:776] Detected quantization_config.scale_fmt=ue8m0; enabling UE8M0 for DeepGEMM.
(APIServer pid=87905) INFO 08-06 21:23:15 [model.py:623] Resolved architecture: DeepseekV4ForCausalLM
(APIServer pid=87905) INFO 08-06 21:23:15 [model.py:1788] Using max model len 65536
(APIServer pid=87905) INFO 08-06 21:23:16 [cache.py:285] Using fp8 data type to store kv cache. It reduces the GPU memory footprint and boosts the performance. Meanwhile, it may cause accuracy drop without a proper scaling factor
(APIServer pid=87905) INFO 08-06 21:23:16 [model.py:623] Resolved architecture: DeepSeekV4MTPModel
(APIServer pid=87905) INFO 08-06 21:23:16 [model.py:1788] Using max model len 1048576
(APIServer pid=87905) INFO 08-06 21:23:16 [speculative.py:1126] Overriding draft model max model len from 1048576 to 65536
(APIServer pid=87905) INFO 08-06 21:23:16 [scheduler.py:252] Chunked prefill is enabled with max_num_batched_tokens=8192.
(APIServer pid=87905) INFO 08-06 21:23:16 [vllm.py:1109] Asynchronous scheduling is enabled.
(APIServer pid=87905) INFO 08-06 21:23:16 [kernel.py:295] Final IR op priority after setting platform defaults: IrOpPriorityConfig(rms_norm=['native'], fused_add_rms_norm=['native'])
(APIServer pid=87905) WARNING 08-06 21:23:16 [vllm.py:1718] max_num_scheduled_tokens is set to 2048 based on the speculative decoding settings. This may lead to suboptimal performance. Consider increasing max_num_batched_tokens to accommodate the additional draft token slots, or decrease num_speculative_tokens or max_num_seqs.
(APIServer pid=87905) WARNING 08-06 21:23:16 [vllm.py:2228] Model Runner V2 does not yet support the thinking_token_budget request parameter. Set VLLM_USE_V2_MODEL_RUNNER=0 if this is required.
(APIServer pid=87905) INFO 08-06 21:23:17 [compilation.py:329] Enabled custom fusions: norm_quant, act_quant
(EngineCore pid=88372) INFO 08-06 21:23:23 [core.py:116] Initializing a V1 LLM engine (v0.26.0) with config: model='/MODELS/DeepSeek-V4-Flash-0731', speculative_config=SpeculativeConfig(method='dspark', model='/MODELS/DeepSeek-V4-Flash-0731', num_spec_tokens=7), tokenizer='/MODELS/DeepSeek-V4-Flash-0731', skip_tokenizer_init=False, tokenizer_mode=deepseek_v4, revision=None, tokenizer_revision=None, trust_remote_code=True, dtype=torch.bfloat16, max_seq_len=65536, download_dir=None, load_format=auto, tensor_parallel_size=1, pipeline_parallel_size=1, data_parallel_size=1, decode_context_parallel_size=1, dcp_comm_backend=ag_rs, disable_custom_all_reduce=False, quantization=deepseek_v4_fp8, quantization_config=None, enforce_eager=False, enable_return_routed_experts=False, kv_cache_dtype=fp8, device_config=cuda, structured_outputs_config=StructuredOutputsConfig(backend='auto', disable_any_whitespace=False, disable_additional_properties=False, reasoning_parser='deepseek_v4', reasoning_parser_plugin='', enable_in_reasoning=False), observability_config=ObservabilityConfig(show_hidden_metrics_for_version=None, otlp_traces_endpoint=None, collect_detailed_traces=None, kv_cache_metrics=False, kv_cache_metrics_sample=0.01, cudagraph_metrics=False, enable_layerwise_nvtx_tracing=False, enable_mfu_metrics=False, enable_mm_processor_stats=False, enable_logging_iteration_details=False, jit_monitor_mode='warn', jit_monitor_verbose=False), seed=0, served_model_name=deepseek-v4-flash-0731, enable_prefix_caching=True, enable_chunked_prefill=True, pooler_config=None, compilation_config={'mode': <CompilationMode.VLLM_COMPILE: 3>, 'debug_dump_path': None, 'cache_dir': '', 'compile_cache_save_format': 'binary', 'backend': 'inductor', 'custom_ops': ['+quant_fp8', 'none', '+quant_fp8'], 'ir_enable_torch_wrap': True, 'splitting_ops': ['vllm::unified_attention_with_output', 'vllm::unified_mla_attention_with_output', 'vllm::mamba_mixer2', 'vllm::mamba_mixer', 'vllm::short_conv', 'vllm::linear_attention', 'vllm::plamo2_mamba_mixer', 'vllm::qwen_gdn_attention_core', 'vllm::gdn_attention_core_xpu', 'vllm::olmo_hybrid_gdn_full_forward', 'vllm::kda_attention', 'vllm::sparse_attn_indexer', 'vllm::rocm_aiter_sparse_attn_indexer', 'vllm::deepseek_v4_attention', 'vllm::hpc_rope_norm_forward', 'vllm::unified_kv_cache_update', 'vllm::unified_mla_kv_cache_update'], 'compile_mm_encoder': False, 'cudagraph_mm_encoder': False, 'encoder_cudagraph_token_budgets': [], 'encoder_cudagraph_max_vision_items_per_batch': 0, 'encoder_cudagraph_max_frames_per_batch': None, 'compile_sizes': [], 'compile_ranges_endpoints': [8192], 'inductor_compile_config': {'enable_auto_functionalized_v2': False, 'size_asserts': False, 'alignment_asserts': False, 'scalar_asserts': False, 'combo_kernels': True, 'benchmark_combo_kernel': True}, 'inductor_passes': {}, 'cudagraph_mode': <CUDAGraphMode.FULL_AND_PIECEWISE: (2, 1)>, 'cudagraph_num_of_warmups': 1, 'cudagraph_capture_sizes': [1, 2, 4, 8, 16, 24, 32, 40, 48, 56, 64, 72, 80, 88, 96, 104, 112, 120, 128, 136, 144, 152, 160, 168, 176, 184, 192, 200, 208, 216, 224, 232, 240, 248, 256, 272, 288, 304, 320, 336, 352, 368, 384, 400, 416, 432, 448, 464, 480, 496, 512], 'cudagraph_copy_inputs': False, 'cudagraph_specialize_lora': True, 'use_inductor_graph_partition': False, 'pass_config': {'fuse_norm_quant': True, 'fuse_act_quant': True, 'fuse_attn_quant': False, 'enable_sp': False, 'fuse_gemm_comms': False, 'fuse_allreduce_rms': False, 'enable_qk_norm_rope_fusion': False, 'fuse_rope_kvcache_cat_mla': False, 'fuse_act_padding': False, 'fuse_qk_norm_rope_kvcache': False}, 'max_cudagraph_capture_size': 512, 'dynamic_shapes_config': {'type': <DynamicShapesType.BACKED: 'backed'>, 'evaluate_guards': False, 'assume_32_bit_indexing': False}, 'local_cache_dir': None, 'fast_moe_cold_start': False, 'static_all_moe_layers': []}, kernel_config=KernelConfig(ir_op_priority=IrOpPriorityConfig(rms_norm=['native'], fused_add_rms_norm=['native']), enable_flashinfer_autotune=True, enable_cutedsl_warmup=True, enable_bf16x3_router_gemm=False, moe_backend='auto', linear_backend='auto')
(EngineCore pid=88372) INFO 08-06 21:23:24 [parallel_state.py:1615] world_size=1 rank=0 local_rank=0 distributed_init_method=tcp://172.21.0.2:35801 backend=nccl
(EngineCore pid=88372) INFO 08-06 21:23:24 [parallel_state.py:1946] rank 0 in world size 1 is assigned as DP rank 0, PP rank 0, PCP rank 0, TP rank 0, EP rank 0, EPLB rank N/A
(EngineCore pid=88372) INFO 08-06 21:23:24 [gpu_worker.py:378] Using V2 Model Runner
(EngineCore pid=88372) INFO 08-06 21:23:25 [model_runner.py:284] Loading model from scratch...
(EngineCore pid=88372) INFO 08-06 21:23:25 [quant_config.py:75] DeepSeek V4 expert_dtype resolved to 'fp4'
(EngineCore pid=88372) INFO 08-06 21:23:25 [__init__.py:604] Selected DeepGemmFp8BlockScaledMMKernel for Fp8LinearMethod
(EngineCore pid=88372) INFO 08-06 21:23:25 [deep_gemm.py:175] deep_gemm not found in site-packages, trying vendored vllm.third_party.deep_gemm
(EngineCore pid=88372) INFO 08-06 21:23:25 [deep_gemm.py:202] DeepGEMM PDL enabled on vllm.third_party.deep_gemm.
(EngineCore pid=88372) INFO 08-06 21:23:25 [deep_gemm.py:120] DeepGEMM E8M0 enabled on current platform.
(EngineCore pid=88372) INFO 08-06 21:23:25 [attention.py:91] Using DeepSeek's fp8_ds_mla KV cache format.
(EngineCore pid=88372) INFO 08-06 21:23:25 [mxfp4.py:625] Using 'FLASHINFER_TRTLLM_MXFP4_MXFP8' Mxfp4 MoE backend.
(EngineCore pid=88372) INFO 08-06 21:23:25 [attention.py:694] Using MXFP4 indexer cache for Lightning Indexer.
(EngineCore pid=88372) WARNING 08-06 21:23:26 [vllm.py:2353] `torch.compile` is turned on, but the model /MODELS/DeepSeek-V4-Flash-0731 does not support it. Please open an issue on GitHub if you want it to be supported.
(EngineCore pid=88372) INFO 08-06 21:23:26 [weight_utils.py:869] Filesystem type for checkpoints: OVERLAY. Checkpoint size: 155.43 GiB. Available RAM: 3901.90 GiB.
(EngineCore pid=88372) INFO 08-06 21:23:26 [weight_utils.py:892] Auto-prefetch is disabled because the filesystem (OVERLAY) is not a recognized network FS (NFS/Lustre). If you want to force prefetching, start vLLM with --safetensors-load-strategy=prefetch.
Loading safetensors checkpoint shards:   0% Completed | 0/48 [00:00<?, ?it/s]
Loading safetensors checkpoint shards:   2% Completed | 1/48 [00:00<00:07,  6.54it/s]
...

Loading safetensors checkpoint shards:  94% Completed | 45/48 [03:28<00:10,  3.52s/it]
Loading safetensors checkpoint shards: 100% Completed | 48/48 [03:28<00:00,  1.56s/it]
Loading safetensors checkpoint shards: 100% Completed | 48/48 [03:28<00:00,  4.35s/it]
(EngineCore pid=88372) 
(EngineCore pid=88372) INFO 08-06 21:26:54 [default_loader.py:430] Loading weights took 208.68 seconds
(EngineCore pid=88372) INFO 08-06 21:26:55 [mxfp4.py:1718] Using MoEPrepareAndFinalizeNoDPEPModular
(EngineCore pid=88372) INFO 08-06 21:26:55 [mxfp4.py:1719] Using TrtLlmMxfp4ExpertsModular
(EngineCore pid=88372) INFO 08-06 21:26:58 [eagle3_utils.py:28] Using Eagle3 auxiliary layers from config: (41, 42, 43)
(EngineCore pid=88372) INFO 08-06 21:26:58 [vllm.py:1109] Asynchronous scheduling is enabled.
(EngineCore pid=88372) INFO 08-06 21:26:58 [kernel.py:295] Final IR op priority after setting platform defaults: IrOpPriorityConfig(rms_norm=['native'], fused_add_rms_norm=['native'])
(EngineCore pid=88372) WARNING 08-06 21:26:58 [vllm.py:1718] max_num_scheduled_tokens is set to 2048 based on the speculative decoding settings. This may lead to suboptimal performance. Consider increasing max_num_batched_tokens to accommodate the additional draft token slots, or decrease num_speculative_tokens or max_num_seqs.
(EngineCore pid=88372) WARNING 08-06 21:26:58 [vllm.py:2228] Model Runner V2 does not yet support the thinking_token_budget request parameter. Set VLLM_USE_V2_MODEL_RUNNER=0 if this is required.
(EngineCore pid=88372) INFO 08-06 21:26:58 [compilation.py:329] Enabled custom fusions: norm_quant, act_quant
(EngineCore pid=88372) WARNING 08-06 21:26:58 [vllm.py:2353] `torch.compile` is turned on, but the model /MODELS/DeepSeek-V4-Flash-0731 does not support it. Please open an issue on GitHub if you want it to be supported.
(EngineCore pid=88372) INFO 08-06 21:26:58 [weight_utils.py:869] Filesystem type for checkpoints: OVERLAY. Checkpoint size: 155.43 GiB. Available RAM: 3902.14 GiB.
Loading safetensors checkpoint shards:   0% Completed | 0/48 [00:00<?, ?it/s]
...

Loading safetensors checkpoint shards:  98% Completed | 47/48 [00:10<00:00,  1.37it/s]
Loading safetensors checkpoint shards: 100% Completed | 48/48 [00:15<00:00,  3.18it/s]
(EngineCore pid=88372) 
(EngineCore pid=88372) INFO 08-06 21:27:13 [dspark.py:457] DSpark draft model loaded: 96 params
(EngineCore pid=88372) INFO 08-06 21:27:13 [default_loader.py:430] Loading weights took 15.18 seconds
(EngineCore pid=88372) INFO 08-06 21:27:14 [model_runner.py:305] Model loading took 156.32 GiB and 229.550621 seconds
(EngineCore pid=88372) INFO 08-06 21:27:14 [topk_topp_sampler.py:55] Using FlashInfer for top-p & top-k sampling.
(EngineCore pid=88372) INFO 08-06 21:27:23 [gpu_worker.py:560] Available KV cache memory: 86.74 GiB
(EngineCore pid=88372) INFO 08-06 21:27:23 [kv_cache_utils.py:2177] GPU KV cache size: 913,657 tokens
(EngineCore pid=88372) INFO 08-06 21:27:23 [kv_cache_utils.py:2178] Maximum concurrency for 65,536 tokens per request: 13.94x
(EngineCore pid=88372) INFO 08-06 21:27:23 [indexer.py:306] DSA indexer decode path: use_flattening=False (next_n=8, use_fp4_indexer_cache=True)
(EngineCore pid=88372) INFO 08-06 21:27:23 [kernel.py:295] Final IR op priority after setting platform defaults: IrOpPriorityConfig(rms_norm=['native'], fused_add_rms_norm=['native'])
(EngineCore pid=88372) INFO 08-06 21:27:30 [flashinfer_sparse_mla_warmup.py:233] Warming up DeepSeek V4 sparse MLA attention for mixed tokens=16.
DeepGEMM warmup: 100%|██████████| 1670/1670 [00:00<00:00, 15498.51it/s]
(EngineCore pid=88372) INFO 08-06 21:27:39 [kernel_warmup.py:227] Using FlashInfer autotune cache file: /root/.cache/vllm/flashinfer_autotune_cache/0.6.14/103a/db0548509d665cab91c39252a8cdccd2eb016206f1fa2641b04e65aa168ccd5e/autotune_configs.json
(EngineCore pid=88372) 2026-08-06 21:27:39,934 - INFO - autotuner.py:651 - flashinfer.jit: [Autotuner]: Autotuning process starts ...
[AutoTuner]: Tuning flashinfer::trtllm_fp4_block_scale_moe:   0%|          | 0/10 [00:00<?, ?profile/s]

(EngineCore pid=88372) 2026-08-06 21:27:39,934 - INFO - autotuner.py:651 - flashinfer.jit: [Autotuner]: Autotuning process starts ...
[AutoTuner]: Tuning flashinfer::trtllm_fp4_block_scale_moe: 100%|██████████| 10/10 [09:18<00:00, 55.87s/profile]
(EngineCore pid=88372) 2026-08-06 21:36:59,247 - INFO - autotuner.py:674 - flashinfer.jit: [Autotuner]: Autotuning process ends
(EngineCore pid=88372) 2026-08-06 21:36:59,254 - INFO - autotuner.py:1808 - flashinfer.jit: [Autotuner]: Saved 10 configs to /root/.cache/vllm/flashinfer_autotune_cache/0.6.14/103a/db0548509d665cab91c39252a8cdccd2eb016206f1fa2641b04e65aa168ccd5e/autotune_configs.json (10 new, 0 from previous config)
(EngineCore pid=88372) 2026-08-06 21:36:59,258 - INFO - autotuner.py:1899 - flashinfer.jit: [Autotuner]: Loaded 10 configs from /root/.cache/vllm/flashinfer_autotune_cache/0.6.14/103a/db0548509d665cab91c39252a8cdccd2eb016206f1fa2641b04e65aa168ccd5e/autotune_configs.json
(EngineCore pid=88372) INFO 08-06 21:36:59 [kernel_warmup.py:268] FlashInfer autotune cache loaded on rank 0 from /root/.cache/vllm/flashinfer_autotune_cache/0.6.14/103a/db0548509d665cab91c39252a8cdccd2eb016206f1fa2641b04e65aa168ccd5e/autotune_configs.json.
(EngineCore pid=88372) INFO 08-06 21:36:59 [kernel_warmup.py:65] Warming up ll_bf16 router GEMM kernels.
(EngineCore pid=88372) INFO 08-06 21:37:06 [cutedsl_warmup.py:101] Skipping CuTeDSL warmup because no compile units were requested.
Capturing CUDA graphs (PIECEWISE): 100%|██████████| 51/51 [00:20<00:00,  2.45it/s]
Capturing CUDA graphs (FULL): 100%|██████████| 48/48 [00:20<00:00,  2.37it/s]
(EngineCore pid=88372) INFO 08-06 21:37:48 [speculator.py:127] Capturing model for DSpark speculator...
Capturing dspark CUDA graphs (FULL): 100%|██████████| 48/48 [00:02<00:00, 23.66it/s]
(EngineCore pid=88372) INFO 08-06 21:37:50 [model_runner.py:747] Graph capturing finished in 43 secs, took 1.58 GiB
(EngineCore pid=88372) INFO 08-06 21:37:50 [gpu_worker.py:857] Free memory on device (267.08/267.69 GiB) on startup. Desired GPU memory utilization is (0.92, 246.27 GiB). Actual usage is 156.32 GiB for weight, 2.99 GiB for peak activation, 0.23 GiB for non-torch memory, and 1.58 GiB for CUDAGraph memory. Replace gpu_memory_utilization config with `--kv-cache-memory=91282734531` (85.01 GiB) to fit into requested memory, or `--kv-cache-memory=113620944896` (105.82 GiB) to fully utilize gpu memory. Current kv cache memory in use is 86.74 GiB.
(EngineCore pid=88372) INFO 08-06 21:38:01 [jit_monitor.py:79] Kernel JIT monitor activated; monitored JIT compilations during inference will use mode=warn.
(EngineCore pid=88372) INFO 08-06 21:38:01 [core.py:347] init engine (profile, create kv cache, warmup model) took 647.45 s
(EngineCore pid=88372) INFO 08-06 21:38:02 [kernel.py:295] Final IR op priority after setting platform defaults: IrOpPriorityConfig(rms_norm=['native'], fused_add_rms_norm=['native'])
(APIServer pid=87905) INFO 08-06 21:38:02 [api_server.py:673] Supported tasks: ['generate']
(APIServer pid=87905) INFO 08-06 21:38:03 [parser_manager.py:37] "auto" tool choice has been enabled.
(APIServer pid=87905) WARNING 08-06 21:38:03 [model.py:1546] Default vLLM sampling parameters have been overridden by the model's `generation_config.json`: `{'temperature': 1.0, 'top_p': 1.0}`. If this is not intended, please relaunch vLLM instance with `--generation-config vllm`.
(APIServer pid=87905) INFO 08-06 21:38:03 [api_server.py:677] Starting vLLM server on http://127.0.0.1:8000
(APIServer pid=87905) INFO 08-06 21:38:03 [launcher.py:37] Available routes are:

(APIServer pid=87905) INFO 08-06 21:38:03 [launcher.py:46] Route: /inference/v1/generate, Methods: POST
(APIServer pid=87905) INFO:     Started server process [87905]
(APIServer pid=87905) INFO:     Waiting for application startup.
(APIServer pid=87905) INFO:     Application startup complete.

```
</details>
	

---

## Example of vLLM logs with an Agent in a bad Loop

7 agents completed successfully, but one kept going...

`(APIServer pid=87905) INFO:     127.0.0.1:56678 - "POST /v1/chat/completions HTTP/1.1" 400 Bad Request`

<details>
```
APIServer pid=87905) INFO:     127.0.0.1:56678 - "POST /v1/chat/completions HTTP/1.1" 400 Bad Request
(APIServer pid=87905) INFO:     127.0.0.1:56678 - "POST /v1/chat/completions HTTP/1.1" 200 OK
(APIServer pid=87905) INFO:     127.0.0.1:56678 - "POST /v1/chat/completions HTTP/1.1" 400 Bad Request
(APIServer pid=87905) INFO:     127.0.0.1:56678 - "POST /v1/chat/completions HTTP/1.1" 400 Bad Request
(APIServer pid=87905) INFO:     127.0.0.1:56678 - "POST /v1/chat/completions HTTP/1.1" 400 Bad Request
(APIServer pid=87905) INFO:     127.0.0.1:56678 - "POST /v1/chat/completions HTTP/1.1" 200 OK
(APIServer pid=87905) INFO:     127.0.0.1:56678 - "POST /v1/chat/completions HTTP/1.1" 400 Bad Request
(APIServer pid=87905) INFO 08-06 21:47:33 [loggers.py:310] Engine 000: Avg prompt throughput: 62.0 tokens/s, Avg generation throughput: 174.9 tokens/s, Running: 0 reqs, Waiting: 0 reqs, GPU KV cache usage: 0.0%, Prefix cache hit rate: 92.7%
(APIServer pid=87905) INFO 08-06 21:47:33 [metrics.py:120] SpecDecoding metrics: Mean acceptance length: 4.18, Accepted throughput: 133.09 tokens/s, Drafted throughput: 292.57 tokens/s, Accepted: 1331 tokens, Drafted: 2926 tokens, Per-position acceptance rate: 0.797, 0.653, 0.517, 0.409, 0.333, 0.285, 0.191, Avg Draft acceptance rate: 45.5%
(APIServer pid=87905) INFO:     127.0.0.1:56678 - "POST /v1/chat/completions HTTP/1.1" 400 Bad Request
(APIServer pid=87905) INFO:     127.0.0.1:56678 - "POST /v1/chat/completions HTTP/1.1" 400 Bad Request
(APIServer pid=87905) INFO:     127.0.0.1:56678 - "POST /v1/chat/completions HTTP/1.1" 200 OK
(APIServer pid=87905) INFO:     127.0.0.1:56678 - "POST /v1/chat/completions HTTP/1.1" 400 Bad Request
(APIServer pid=87905) INFO:     127.0.0.1:56678 - "POST /v1/chat/completions HTTP/1.1" 400 Bad Request
(APIServer pid=87905) INFO:     127.0.0.1:56678 - "POST /v1/chat/completions HTTP/1.1" 400 Bad Request
(APIServer pid=87905) INFO:     127.0.0.1:56678 - "POST /v1/chat/completions HTTP/1.1" 200 OK
(APIServer pid=87905) INFO:     127.0.0.1:56678 - "POST /v1/chat/completions HTTP/1.1" 400 Bad Request
(APIServer pid=87905) INFO:     127.0.0.1:56678 - "POST /v1/chat/completions HTTP/1.1" 400 Bad Request
(APIServer pid=87905) INFO:     127.0.0.1:56678 - "POST /v1/chat/completions HTTP/1.1" 400 Bad Request
(APIServer pid=87905) INFO:     127.0.0.1:56678 - "POST /v1/chat/completions HTTP/1.1" 200 OK
(APIServer pid=87905) INFO:     127.0.0.1:56678 - "POST /v1/chat/completions HTTP/1.1" 400 Bad Request
(APIServer pid=87905) INFO:     127.0.0.1:56678 - "POST /v1/chat/completions HTTP/1.1" 400 Bad Request
(APIServer pid=87905) INFO:     127.0.0.1:56678 - "POST /v1/chat/completions HTTP/1.1" 400 Bad Request
(APIServer pid=87905) INFO:     127.0.0.1:56678 - "POST /v1/chat/completions HTTP/1.1" 200 OK
(APIServer pid=87905) INFO:     127.0.0.1:56678 - "POST /v1/chat/completions HTTP/1.1" 400 Bad Request
(APIServer pid=87905) INFO:     127.0.0.1:56678 - "POST /v1/chat/completions HTTP/1.1" 400 Bad Request
(APIServer pid=87905) INFO:     127.0.0.1:56678 - "POST /v1/chat/completions HTTP/1.1" 400 Bad Request
(APIServer pid=87905) INFO:     127.0.0.1:56678 - "POST /v1/chat/completions HTTP/1.1" 200 OK
(APIServer pid=87905) INFO:     127.0.0.1:56678 - "POST /v1/chat/completions HTTP/1.1" 400 Bad Request
(APIServer pid=87905) INFO 08-06 21:47:43 [loggers.py:310] Engine 000: Avg prompt throughput: 62.0 tokens/s, Avg generation throughput: 106.5 tokens/s, Running: 0 reqs, Waiting: 0 reqs, GPU KV cache usage: 0.0%, Prefix cache hit rate: 92.7%
(APIServer pid=87905) INFO 08-06 21:47:43 [metrics.py:120] SpecDecoding metrics: Mean acceptance length: 3.06, Accepted throughput: 71.70 tokens/s, Drafted throughput: 243.60 tokens/s, Accepted: 717 tokens, Drafted: 2436 tokens, Per-position acceptance rate: 0.707, 0.483, 0.319, 0.221, 0.149, 0.109, 0.072, Avg Draft acceptance rate: 29.4%
(APIServer pid=87905) INFO:     127.0.0.1:56678 - "POST /v1/chat/completions HTTP/1.1" 400 Bad Request
(APIServer pid=87905) INFO:     127.0.0.1:56678 - "POST /v1/chat/completions HTTP/1.1" 400 Bad Request
(APIServer pid=87905) INFO:     127.0.0.1:56678 - "POST /v1/chat/completions HTTP/1.1" 200 OK
(APIServer pid=87905) INFO:     127.0.0.1:56678 - "POST /v1/chat/completions HTTP/1.1" 400 Bad Request
(APIServer pid=87905) INFO:     127.0.0.1:56678 - "POST /v1/chat/completions HTTP/1.1" 400 Bad Request
(APIServer pid=87905) INFO:     127.0.0.1:56678 - "POST /v1/chat/completions HTTP/1.1" 400 Bad Request
(APIServer pid=87905) INFO:     127.0.0.1:56678 - "POST /v1/chat/completions HTTP/1.1" 200 OK
(APIServer pid=87905) INFO:     127.0.0.1:56678 - "POST /v1/chat/completions HTTP/1.1" 400 Bad Request
(APIServer pid=87905) INFO:     127.0.0.1:56678 - "POST /v1/chat/completions HTTP/1.1" 400 Bad Request
(APIServer pid=87905) INFO:     127.0.0.1:56678 - "POST /v1/chat/completions HTTP/1.1" 400 Bad Request
(APIServer pid=87905) INFO:     127.0.0.1:56678 - "POST /v1/chat/completions HTTP/1.1" 200 OK
(APIServer pid=87905) INFO:     127.0.0.1:56678 - "POST /v1/chat/completions HTTP/1.1" 400 Bad Request
(APIServer pid=87905) INFO:     127.0.0.1:56678 - "POST /v1/chat/completions HTTP/1.1" 400 Bad Request
(APIServer pid=87905) INFO:     127.0.0.1:56678 - "POST /v1/chat/completions HTTP/1.1" 400 Bad Request
(APIServer pid=87905) INFO:     127.0.0.1:56678 - "POST /v1/chat/completions HTTP/1.1" 200 OK
(APIServer pid=87905) INFO:     127.0.0.1:56678 - "POST /v1/chat/completions HTTP/1.1" 400 Bad Request
(APIServer pid=87905) INFO:     127.0.0.1:56678 - "POST /v1/chat/completions HTTP/1.1" 400 Bad Request
(APIServer pid=87905) INFO:     127.0.0.1:56678 - "POST /v1/chat/completions HTTP/1.1" 400 Bad Request
(APIServer pid=87905) INFO 08-06 21:47:53 [loggers.py:310] Engine 000: Avg prompt throughput: 62.0 tokens/s, Avg generation throughput: 144.3 tokens/s, Running: 1 reqs, Waiting: 0 reqs, GPU KV cache usage: 0.0%, Prefix cache hit rate: 92.7%
(APIServer pid=87905) INFO 08-06 21:47:53 [metrics.py:120] SpecDecoding metrics: Mean acceptance length: 3.63, Accepted throughput: 104.49 tokens/s, Drafted throughput: 277.87 tokens/s, Accepted: 1045 tokens, Drafted: 2779 tokens, Per-position acceptance rate: 0.771, 0.567, 0.413, 0.297, 0.239, 0.189, 0.156, Avg Draft acceptance rate: 37.6%
(APIServer pid=87905) INFO:     127.0.0.1:56678 - "POST /v1/chat/completions HTTP/1.1" 200 OK
(APIServer pid=87905) INFO:     127.0.0.1:56678 - "POST /v1/chat/completions HTTP/1.1" 400 Bad Request
(APIServer pid=87905) INFO:     127.0.0.1:56678 - "POST /v1/chat/completions HTTP/1.1" 400 Bad Request
(APIServer pid=87905) INFO:     127.0.0.1:56678 - "POST /v1/chat/completions HTTP/1.1" 400 Bad Request

```
</details>

## DeepSeek successful cache logs

The prompt stage is effectively "free" because Harbor keeps sending prompts that share a very long common prefix.

```
harbor run -d terminal-bench/terminal-bench-2-1 --agent terminus-2 --model openai/deepseek-v4-flash-0731 -n 8 -k 8 --include-task-name terminal-bench/regex-log
  8/8 Mean: 0.875 ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 0:05:27 0:00:00

terminal-bench/terminal-bench-2-1 • terminus-2 • deepseek-v4-flash-0731
┏━━━━━━━━┳━━━━━━━━━━━━┳━━━━━━━┳━━━━━━━━┳━━━━━━━━┳━━━━━━━━┳━━━━━━━━┓
┃ Trials ┃ Exceptions ┃  Mean ┃ Pass@2 ┃ Pass@4 ┃ Pass@5 ┃ Pass@8 ┃
┡━━━━━━━━╇━━━━━━━━━━━━╇━━━━━━━╇━━━━━━━━╇━━━━━━━━╇━━━━━━━━╇━━━━━━━━┩
│      8 │          0 │ 0.875 │  1.000 │  1.000 │  1.000 │  1.000 │
└────────┴────────────┴───────┴────────┴────────┴────────┴────────┘

┏━━━━━━━━┳━━━━━━━┓
┃ Reward ┃ Count ┃
┡━━━━━━━━╇━━━━━━━┩
│ 1.0    │     7 │
│ 0.0    │     1 │
└────────┴───────┘

Job Info Total runtime: 5m 27s
```

vLLM Logs:
<details>
```
(APIServer pid=87905) INFO 08-06 21:51:03 [loggers.py:310] Engine 000: Avg prompt throughput: 49.6 tokens/s, Avg generation throughput: 75.3 tokens/s, Running: 0 reqs, Waiting: 0 reqs, GPU KV cache usage: 0.0%, Prefix cache hit rate: 92.3%
(APIServer pid=87905) INFO 08-06 21:51:03 [metrics.py:120] SpecDecoding metrics: Mean acceptance length: 3.07, Accepted throughput: 50.80 tokens/s, Drafted throughput: 171.50 tokens/s, Accepted: 508 tokens, Drafted: 1715 tokens, Per-position acceptance rate: 0.743, 0.498, 0.322, 0.216, 0.135, 0.094, 0.065, Avg Draft acceptance rate: 29.6%
(APIServer pid=87905) INFO 08-06 21:51:13 [loggers.py:310] Engine 000: Avg prompt throughput: 0.0 tokens/s, Avg generation throughput: 0.0 tokens/s, Running: 0 reqs, Waiting: 0 reqs, GPU KV cache usage: 0.0%, Prefix cache hit rate: 92.3%
(APIServer pid=87905) INFO:     127.0.0.1:59858 - "GET /metrics HTTP/1.1" 200 OK
(APIServer pid=87905) INFO:     127.0.0.1:43840 - "POST /v1/chat/completions HTTP/1.1" 200 OK
(APIServer pid=87905) INFO:     127.0.0.1:43852 - "POST /v1/chat/completions HTTP/1.1" 200 OK
(APIServer pid=87905) INFO:     127.0.0.1:43914 - "POST /v1/chat/completions HTTP/1.1" 200 OK
(APIServer pid=87905) INFO:     127.0.0.1:43840 - "POST /v1/chat/completions HTTP/1.1" 200 OK
(APIServer pid=87905) INFO:     127.0.0.1:43930 - "POST /v1/chat/completions HTTP/1.1" 200 OK
(APIServer pid=87905) INFO 08-06 21:53:03 [loggers.py:310] Engine 000: Avg prompt throughput: 360.8 tokens/s, Avg generation throughput: 883.5 tokens/s, Running: 8 reqs, Waiting: 0 reqs, GPU KV cache usage: 0.4%, Prefix cache hit rate: 92.2%
(APIServer pid=87905) INFO 08-06 21:53:03 [metrics.py:120] SpecDecoding metrics: Mean acceptance length: 3.14, Accepted throughput: 50.11 tokens/s, Drafted throughput: 164.09 tokens/s, Accepted: 6013 tokens, Drafted: 19691 tokens, Per-position acceptance rate: 0.664, 0.461, 0.338, 0.254, 0.194, 0.140, 0.086, Avg Draft acceptance rate: 30.5%
(APIServer pid=87905) INFO:     127.0.0.1:43902 - "POST /v1/chat/completions HTTP/1.1" 200 OK
(APIServer pid=87905) INFO:     127.0.0.1:43840 - "POST /v1/chat/completions HTTP/1.1" 200 OK
(APIServer pid=87905) INFO:     127.0.0.1:43930 - "POST /v1/chat/completions HTTP/1.1" 200 OK
(APIServer pid=87905) INFO:     127.0.0.1:43852 - "POST /v1/chat/completions HTTP/1.1" 200 OK
(APIServer pid=87905) INFO:     127.0.0.1:43914 - "POST /v1/chat/completions HTTP/1.1" 200 OK
(APIServer pid=87905) INFO:     127.0.0.1:43864 - "POST /v1/chat/completions HTTP/1.1" 200 OK
(APIServer pid=87905) INFO:     127.0.0.1:43930 - "POST /v1/chat/completions HTTP/1.1" 200 OK
(APIServer pid=87905) INFO:     127.0.0.1:43840 - "POST /v1/chat/completions HTTP/1.1" 200 OK
(APIServer pid=87905) INFO:     127.0.0.1:43874 - "POST /v1/chat/completions HTTP/1.1" 200 OK
(APIServer pid=87905) INFO:     127.0.0.1:43914 - "POST /v1/chat/completions HTTP/1.1" 200 OK
(APIServer pid=87905) INFO:     127.0.0.1:43864 - "POST /v1/chat/completions HTTP/1.1" 200 OK
(APIServer pid=87905) INFO:     127.0.0.1:43840 - "POST /v1/chat/completions HTTP/1.1" 200 OK
(APIServer pid=87905) INFO:     127.0.0.1:43852 - "POST /v1/chat/completions HTTP/1.1" 200 OK
(APIServer pid=87905) INFO 08-06 21:53:13 [loggers.py:310] Engine 000: Avg prompt throughput: 1141.2 tokens/s, Avg generation throughput: 991.8 tokens/s, Running: 6 reqs, Waiting: 0 reqs, GPU KV cache usage: 0.3%, Prefix cache hit rate: 91.6%
(APIServer pid=87905) INFO 08-06 21:53:13 [metrics.py:120] SpecDecoding metrics: Mean acceptance length: 3.57, Accepted throughput: 713.99 tokens/s, Drafted throughput: 1943.87 tokens/s, Accepted: 7140 tokens, Drafted: 19439 tokens, Per-position acceptance rate: 0.703, 0.516, 0.406, 0.330, 0.270, 0.205, 0.141, Avg Draft acceptance rate: 36.7%
(APIServer pid=87905) INFO:     127.0.0.1:43902 - "POST /v1/chat/completions HTTP/1.1" 200 OK
(APIServer pid=87905) INFO:     127.0.0.1:43874 - "POST /v1/chat/completions HTTP/1.1" 200 OK
(APIServer pid=87905) INFO:     127.0.0.1:43914 - "POST /v1/chat/completions HTTP/1.1" 200 OK
(APIServer pid=87905) INFO:     127.0.0.1:43864 - "POST /v1/chat/completions HTTP/1.1" 200 OK
(APIServer pid=87905) INFO:     127.0.0.1:43902 - "POST /v1/chat/completions HTTP/1.1" 200 OK
(APIServer pid=87905) INFO:     127.0.0.1:43852 - "POST /v1/chat/completions HTTP/1.1" 200 OK
(APIServer pid=87905) INFO:     127.0.0.1:43840 - "POST /v1/chat/completions HTTP/1.1" 200 OK
(APIServer pid=87905) INFO:     127.0.0.1:43864 - "POST /v1/chat/completions HTTP/1.1" 200 OK
(APIServer pid=87905) INFO 08-06 21:53:23 [loggers.py:310] Engine 000: Avg prompt throughput: 871.3 tokens/s, Avg generation throughput: 967.3 tokens/s, Running: 8 reqs, Waiting: 0 reqs, GPU KV cache usage: 0.5%, Prefix cache hit rate: 91.4%
(APIServer pid=87905) INFO 08-06 21:53:23 [metrics.py:120] SpecDecoding metrics: Mean acceptance length: 3.09, Accepted throughput: 653.93 tokens/s, Drafted throughput: 2191.46 tokens/s, Accepted: 6540 tokens, Drafted: 21917 tokens, Per-position acceptance rate: 0.642, 0.435, 0.322, 0.248, 0.194, 0.149, 0.099, Avg Draft acceptance rate: 29.8%
(APIServer pid=87905) INFO:     127.0.0.1:43902 - "POST /v1/chat/completions HTTP/1.1" 200 OK
(APIServer pid=87905) INFO:     127.0.0.1:43914 - "POST /v1/chat/completions HTTP/1.1" 200 OK
(APIServer pid=87905) INFO:     127.0.0.1:43852 - "POST /v1/chat/completions HTTP/1.1" 200 OK
(APIServer pid=87905) INFO:     127.0.0.1:43864 - "POST /v1/chat/completions HTTP/1.1" 200 OK
(APIServer pid=87905) INFO:     127.0.0.1:43840 - "POST /v1/chat/completions HTTP/1.1" 200 OK
(APIServer pid=87905) INFO:     127.0.0.1:43840 - "POST /v1/chat/completions HTTP/1.1" 200 OK
(APIServer pid=87905) INFO:     127.0.0.1:43902 - "POST /v1/chat/completions HTTP/1.1" 200 OK
(APIServer pid=87905) INFO:     127.0.0.1:43914 - "POST /v1/chat/completions HTTP/1.1" 200 OK
(APIServer pid=87905) INFO:     127.0.0.1:43852 - "POST /v1/chat/completions HTTP/1.1" 200 OK
(APIServer pid=87905) INFO:     127.0.0.1:43864 - "POST /v1/chat/completions HTTP/1.1" 200 OK
(APIServer pid=87905) INFO 08-06 21:53:33 [loggers.py:310] Engine 000: Avg prompt throughput: 873.5 tokens/s, Avg generation throughput: 1106.3 tokens/s, Running: 6 reqs, Waiting: 0 reqs, GPU KV cache usage: 0.4%, Prefix cache hit rate: 91.2%
(APIServer pid=87905) INFO 08-06 21:53:33 [metrics.py:120] SpecDecoding metrics: Mean acceptance length: 3.45, Accepted throughput: 785.29 tokens/s, Drafted throughput: 2247.68 tokens/s, Accepted: 7853 tokens, Drafted: 22477 tokens, Per-position acceptance rate: 0.684, 0.499, 0.379, 0.298, 0.251, 0.200, 0.135, Avg Draft acceptance rate: 34.9%
(APIServer pid=87905) INFO:     127.0.0.1:43840 - "POST /v1/chat/completions HTTP/1.1" 200 OK
(APIServer pid=87905) INFO:     127.0.0.1:43902 - "POST /v1/chat/completions HTTP/1.1" 200 OK
(APIServer pid=87905) INFO:     127.0.0.1:43914 - "POST /v1/chat/completions HTTP/1.1" 200 OK
(APIServer pid=87905) INFO:     127.0.0.1:43902 - "POST /v1/chat/completions HTTP/1.1" 200 OK
(APIServer pid=87905) INFO:     127.0.0.1:43914 - "POST /v1/chat/completions HTTP/1.1" 200 OK
(APIServer pid=87905) INFO:     127.0.0.1:43864 - "POST /v1/chat/completions HTTP/1.1" 200 OK
(APIServer pid=87905) INFO:     127.0.0.1:43840 - "POST /v1/chat/completions HTTP/1.1" 200 OK
(APIServer pid=87905) INFO:     127.0.0.1:43852 - "POST /v1/chat/completions HTTP/1.1" 200 OK
(APIServer pid=87905) INFO 08-06 21:53:43 [loggers.py:310] Engine 000: Avg prompt throughput: 882.2 tokens/s, Avg generation throughput: 879.5 tokens/s, Running: 7 reqs, Waiting: 0 reqs, GPU KV cache usage: 0.6%, Prefix cache hit rate: 91.3%
(APIServer pid=87905) INFO 08-06 21:53:43 [metrics.py:120] SpecDecoding metrics: Mean acceptance length: 2.91, Accepted throughput: 576.72 tokens/s, Drafted throughput: 2118.62 tokens/s, Accepted: 5768 tokens, Drafted: 21189 tokens, Per-position acceptance rate: 0.609, 0.402, 0.287, 0.220, 0.173, 0.132, 0.082, Avg Draft acceptance rate: 27.2%
(APIServer pid=87905) INFO:     127.0.0.1:43902 - "POST /v1/chat/completions HTTP/1.1" 200 OK
(APIServer pid=87905) INFO:     127.0.0.1:43864 - "POST /v1/chat/completions HTTP/1.1" 200 OK
(APIServer pid=87905) INFO:     127.0.0.1:43840 - "POST /v1/chat/completions HTTP/1.1" 200 OK
(APIServer pid=87905) INFO:     127.0.0.1:43914 - "POST /v1/chat/completions HTTP/1.1" 200 OK
(APIServer pid=87905) INFO:     127.0.0.1:43852 - "POST /v1/chat/completions HTTP/1.1" 200 OK
(APIServer pid=87905) INFO 08-06 21:53:53 [loggers.py:310] Engine 000: Avg prompt throughput: 484.5 tokens/s, Avg generation throughput: 1041.1 tokens/s, Running: 7 reqs, Waiting: 0 reqs, GPU KV cache usage: 0.7%, Prefix cache hit rate: 91.3%
(APIServer pid=87905) INFO 08-06 21:53:53 [metrics.py:120] SpecDecoding metrics: Mean acceptance length: 3.18, Accepted throughput: 713.96 tokens/s, Drafted throughput: 2289.57 tokens/s, Accepted: 7140 tokens, Drafted: 22897 tokens, Per-position acceptance rate: 0.654, 0.451, 0.342, 0.264, 0.208, 0.157, 0.106, Avg Draft acceptance rate: 31.2%
(APIServer pid=87905) INFO:     127.0.0.1:43902 - "POST /v1/chat/completions HTTP/1.1" 200 OK

```

</details>
