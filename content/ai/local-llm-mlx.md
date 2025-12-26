Title: Cars not Helicoptors, or running a local LLM with MLX on a Macbook Pro
Date: 2024-11-23 19:21
Tags: ai, llm, mlx

[TOC]

# Everything looks like a nail

For Large Language Models (LLMs), Frontier aka "State of the Art" (SOTA) Models provided by big vendors like OpenAI and Anthropic and Google continue to add capabilities at a wondrous rate. Yet there's a very strong case for running LLMs locally, much like every smart phone provides a powerful computer your pocket.

As an example: helicopters can cover in 15 minutes what takes 2 hours by car, but the overhead and extra considerations (fuel, pilots, landings, weather sensitivity, etc.) makes them wildly impractical for routine tasks like picking up kids from school. 

*(Though those new drones can carry pretty heavy loads ;)*

Given English has ~170,000 words but the average working vocabulary is 30,000 words, and  specific domains like "email" (Hello! Best Regards,) are even more narrow and formulaic...
Do you need a model trained on the entirety of human knowledge with latency from expensive GPU clusters?

Writing code, due to its utilitarian nature, has even more structure and repetition and 
rules - especially if it's type-checked and compiled.

# How they work together

In software, experienced engineers propose and design the architecture, whereas less experienced people do the (simpler parts) of implementation - specialization based on skill and scope. Frontier models can design and orchestrate, handle the unusual, while local models do specific, simple things well.

## Inevitable and Resilient

In 2020 an LLM was a research project and by 2024 it's running on your laptop (or smartphone!). Hardware gets better and costs go down which induces "Jevons Paradox"; as people adapt they'll use LLM inference non-stop.

Moreover, users (and businesses!) dependent to always having AI will balk at "cloud outages" or "AI outages" - thus a real need and demand for local LLMs.

(Have you ever seen people struggling without phone reception ;)

And I didn't even trot out the privacy and security arguments...

We don't use Helicoptors for everything, use the right tool for the job.

# Hands On with MLX - install

Apple silicon architecture of "unified memory" is convenient for those trying out "Local LLMs" - and not buying a dedicated server with a GPU.

	:::bash
	brew install uv
	uv --version
	mkdir llm-demo
	cd llm-demo
	
	uv venv
	
	## this installs mlx as it's a dependency of mlx-lm
	uv pip install mlx-lm 
	
	## optional sanity checks - using explicit calls with the local uv
	uv pip list
	uv run python -c "import mlx; import mlx.core as mx; print('mlx ok', mx.__version__)"
	uv run python -c "import mlx_lm; print('mlx_lm ok')"

## Run that LLM with MLX

The following command will both download the model and then load it into memory along with sending it the prompt:

`uv run mlx_lm.generate --model mlx-community/Meta-Llama-3.1-8B-Instruct-4bit \
  --prompt "tell me a joke"`

> A man walked into a library and asked the librarian, "Do you have any books on Pavlov's dogs and Schrödinger's cat?" The librarian replied, "That rings a bell but I'm not sure if they're here or not."
	
> 	Prompt: 47 tokens, 68.789 tokens-per-sec
>	Generation: 100 tokens, 30.293 tokens-per-sec
>	Peak memory: 4.647 GB


A token is a part of word - and this is plenty fast enough to not wait while each word of the joke is printed slowly.

Let's examine where the "open weight" downloaded model is:

`du -sh ~/.cache/huggingface/hub/models--mlx-community--Meta-Llama-3.1-8B-Instruct-4bit`

> 4.2G	models--mlx-community--Meta-Llama-3.1-8B-Instruct-4bit

# Next Level is a Script


create the wrapper script "llm-demo/mychat.py"
	:::python
	import sys
	from mlx_lm import load, generate
	
	if len(sys.argv) < 2:
		print("Usage: python mychat.py 'your prompt here'")
    	sys.exit(1)
		
	model, tokenizer = load("mlx-community/Meta-Llama-3.1-8B-Instruct-4bit")
	prompt = " ".join(sys.argv[1:])
	response = generate(model, tokenizer, prompt=prompt, max_tokens=1000)
	print(response)
	

*assuming you are re-using the "llm-demo" directory and all the pre-requisite UV and venv setup*

source .venv/bin/activate

Create the pyproject.toml and ensure the mlx-lm dependency is added:

	uv init --bare
	uv add mlx-lm

`python mychat.py "tell me a joke"`

> You may notice it 

# TODO

Describe how to fix the LLM running on until abruptly terminating at the max token count:

	:::python
	import sys
	from mlx_lm import load, generate
	
	if len(sys.argv) < 2:
		print("Usage: python mychat.py 'your prompt here'")
		sys.exit(1)
	
	model, tokenizer = load("mlx-community/Meta-Llama-3.1-8B-Instruct-4bit")
	user_prompt = " ".join(sys.argv[1:])
	
	# Format with chat template
	messages = [{"role": "user", "content": user_prompt}]
	prompt = tokenizer.apply_chat_template(messages, tokenize=False, add_generation_prompt=True)
	
	response = generate(model, tokenizer, prompt=prompt, max_tokens=1000, verbose=False)
	print(response)


Also, describe how max tokens can help avoid context overload (and local LLM RAM overload)

monitor memory pressure with top or activity monitor


# Troubleshooting


## Where is that installed?

A python uv gotcha - do not move (or copy) the .venv directory since it includes absolute folder paths - instead use the uv commands for each new project.

UV is awesomely fast - one reason is it uses a cache, here's how to audit how many python versions UV installed/knows:

`ls -ahl ~/.local/share/uv/python/`

And in case you installed uv with both "install.sh" and homebrew...

`which -a uv`

	:::bash
	/opt/homebrew/bin/uv
	~/.local/bin/uv

## Cleanup

To find previously download local models which are large files

	:::bash
	find ~ -type f -size +1G 2>/dev/null
	ls -ahl ~/.cache/huggingface/
	ls -ahl ~/.cache/huggingface/hub
	rm -rf ~/.cache/huggingface/hub/models--mlx-community--Meta-Llama-3...
	
Or maybe you want to clean up a global pip install of MLX

	:::bash
	pip3 list
	brew uninstall mlx



foo

	brew install uv
	uv --version
	which -a uv
	
	mkdir ./llm-demo
	uv init --bare
	uv venv --clear
	source .venv/bin/activate
	uv pip install mlx mlx-lm
	uv pip list
	
	uv run python -c "import mlx; import mlx.core as mx; print('mlx ok', mx.__version__)"
	uv run python -c "import mlx_lm; print('mlx_lm ok')"


# References
<https://github.com/ml-explore/mlx>

<https://www.apple.com/newsroom/2023/10/apple-unveils-m3-m3-pro-and-m3-max-the-most-advanced-chips-for-a-personal-computer/>


**Addendum:**

<https://machinelearning.apple.com/research/exploring-llms-mlx-m5>


