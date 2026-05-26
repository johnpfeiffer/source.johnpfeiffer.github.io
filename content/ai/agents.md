Title: AI with Agents aka LLMs with Tools
Date: 2025-08-30 18:18
Tags: ai, llm, mlx, agents, tools

[TOC]

> To a hammer, everything looks like a nail

Large Language Models are powerful but non-deterministic. Existing tools are still better for deterministic and efficient answers. Why not both?

# Definitions and Background

Tools: simple things humans have used since forever =p

- Single Responsibility Principle - having a singular purpose and doing it very well.
- Unix (and Linux) philosophy: connecting software tools with pipes

Example: a tool like `cat` is focused on displaying the contents of a file

> Tools in the AI context: **"functionality that is specifically provided to the model"**

*This relies on foundation model vendors who have trained the model to "understand" a tool call.*

- LLM: stochastic highest probability token generator
- MCP is the new "model context protocol" for allowing an LLM (Large Language Model) to connect externally

If you need further background: My previous article more focused on (local) LLMs and MCP:

- <https://blog.john-pfeiffer.com/cars-not-helicopters-or-running-a-local-llm-with-mlx-on-a-macbook-pro/>
`uv venv; uv pip install mlx-lm; \
  uv run mlx_lm.generate --model mlx-community/Meta-Llama-3.1-8B-Instruct-4bit --prompt "tell me a joke"`

- <https://blog.john-pfeiffer.com/intro-to-mcp-give-your-llm-tools-with-model-context-protocol/>


# Simplest Chat Loop

Start with the simplest way to interact with a (local) LLM at the command line.

In a loop, the user message is provided to the LLM, and the LLM response is displayed.

`source .venv/bin/activate; python 01-chat-loop.py`

```python
from mlx_lm import load, generate

def main():
    model, tokenizer = load("mlx-community/Meta-Llama-3.1-8B-Instruct-4bit")
    system_message = "You are a helpful, concise Assistant"
    messages = [{"role": "system", "content": system_message}]
    run(model, tokenizer, messages, get_user_message)


 # run loops getting the user message and displaying the LLM response
def run(model, tokenizer, messages, get_msg_fn):
    while True:
        user_input, ok = get_msg_fn()
        if not ok:
            break

        messages.append({"role": "user", "content": user_input})
        prompt = tokenizer.apply_chat_template(messages, tokenize=False, add_generation_prompt=True)
        response = generate(model, tokenizer, prompt=prompt, max_tokens=10000)
        print(f"\nAssistant: {response}\n")
        messages.append({"role": "assistant", "content": response})


def get_user_message():
    try:
        user_input = input("You (provide input or type quit): ").strip()
        if user_input.lower() in {"exit", "quit"}:
            return "", False
        return user_input, True
    except (EOFError, KeyboardInterrupt):
        print()
        return "", False


if __name__ == "__main__":
    main()


```

> You (provide input or type quit): tell me a joke

*Assistant: A man walked into a library and asked the librarian, "Do you have any books on Pavlov's dogs and Schrödinger's cat?" The librarian replied, "It rings a bell, but I'm not sure if it's here or not."*

> You (provide input or type quit):  summarize the file 02-chat-loop-with-read-file-tool.py 

*Assistant: I don't have access to your local files. However... [long unhelpful hallucination continues]*

## Tools and Agents

Is there a simple way to give an LLM precise accurate context to answer a query?

Simpler than training data, pre-training and post-training (RLHF), easier than an MCP Server?

Yes! Give the LLM a "tool".

An AI agent is software that is looping with repeated calls to an LLM until it achieves a goal.

*Many other definitions of AI agents are out there - feel free to pick your favorite ;)*

"tool use" is a more lightweight way of giving an LLM (AI agent) access to external or recent information. Just like giving a tool to a human, this provides the LLM incredible leverage.

## Tool Definition

The technical specification definition of a "Tool" is quite small and simple, and it's mostly english:

**Name**: a unique identifier for the tool

**Description**: a natural language explanation of what the tool does, its primary purpose, any important capabilities, and potentially its limitations

**Input Schema**: JSON object defining the expected (required and optional) parameters

### Example Tool - Read File

```
Name:        "read_file"

Description: "Read the contents of a given file path. Use this to see everything in a file. Do not use this with directory names.",

InputSchema:
    "type": "object",
    "properties": {
        "file_path": {
            "type": "string",
            "description": "The path of the file to read",
        },
    },
    "required": ["file_path"],

```

> It is required to provide a file path for the tool to read a file =)

The most complicated part is being very specific in JSON about exactly what is being sent to the tool.

*Note in developer jargon, tool calling for LLMs is often called "function-calling"*


# MVP Agent with a Tool

> generate_response() is the new function abstracting away the complexity of tool calls

```python
import json
from mlx_lm import load, generate

def main():
    model, tokenizer = load("mlx-community/Meta-Llama-3.1-8B-Instruct-4bit")
    system_message = """You are a helpful, concise Assistant.
	You have access to a read_file tool, but ONLY use them when the user's request REQUIRES one.
	MOST messages need NO tool call. Just reply in plain text.
	DO NOT call a tool for:
	- Greetings, chitchat, or general questions
	- Questions you already know the answer to
	ONLY call a tool when you literally cannot answer without it.
	When you do NOT need a tool, respond in plain text. Never output JSON unless you are calling a tool."""
	
    messages = [{"role": "system", "content": system_message}]
    run(model, tokenizer, messages, get_user_message)


 # run loops getting the user message and displaying the LLM response
def run(model, tokenizer, messages, get_msg_fn):
    while True:
        user_input, ok = get_msg_fn()
        if not ok:
            break

        messages.append({"role": "user", "content": user_input})
        user_prompt = tokenizer.apply_chat_template(messages, tokenize=False, add_generation_prompt=True, tools=TOOLS)
		
		# dedicated helper function to handle tool calling complexity
        response = generate_response(model, tokenizer, messages, user_prompt)

        print(f"\nAssistant: {response}\n")
        messages.append({"role": "assistant", "content": response})


def get_user_message():
    try:
        user_input = input("You (provide input or type quit): ").strip()
        if user_input.lower() in {"exit", "quit"}:
            return "", False
        return user_input, True
    except (EOFError, KeyboardInterrupt):
        print()
        return "", False


def generate_response(model, tokenizer, messages, user_prompt):
    response = generate(model, tokenizer, prompt=user_prompt, max_tokens=10000)

    # Check if the LLM believes the User query may need a tool call, if the first LLM response is not JSON just ignore
    try:
        response_as_json = json.loads(response)
        if response_as_json.get("name") == "read_file":
            # DEBUG print(f"\nAssistant believes it needs a tool call: {response}\n")
            tool_input = response_as_json["parameters"]
            tool_result = read_file(tool_input["file_path"])
            messages.append({
                "role": "tool",
                "name": "read_file",
                "content": tool_result,
            })

            # create a user friendly response based on the tool call result
            prompt = tokenizer.apply_chat_template(messages, tokenize=False, add_generation_prompt=True)
            response = generate(model, tokenizer, prompt=prompt, max_tokens=10000)

    except (json.JSONDecodeError, KeyError, TypeError):
        pass
    return response


def read_file(file_path):
    try:
        with open(file_path, "r") as f:
            return f.read()
    except Exception as e:
        return f"Error reading file: {e}"


TOOLS = [
    {
        "type": "function",
        "name": "read_file",
		"function": "read_file",
        "description": "Read the contents of a given file path. Use this to see everything in a file. Do not use this with directory names.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "file_path": {
                    "type": "string",
                    "description": "The path of the file to read",
                },
            },
            "required": ["file_path"],
        },
    },
]


if __name__ == "__main__":
    main()

```

## Chatting with tool power

```plaintext
You (provide input or type quit): tell me a joke                                                                         

Assistant: I'm a large language model, I don't have a collection of jokes stored in a file. I can try to come up with a joke on the spot, though!
Why couldn't the bicycle stand up by itself? Because it was two-tired!

You (provide input or type quit): summarize the file 02-chat-loop-with-read-file-tool.py

Assistant: This script is a chat loop that uses a large language model (LLM) to respond to user input. The LLM is loaded from a model and tokenizer, and the chat loop continues until the user types "quit" or "exit".

The script also includes a "read_file" tool that can be used to read the contents of a file. If the LLM believes that a user query may require a tool call, it will print a message indicating that it needs to call a tool, and then call the "read_file" tool with the specified file path. The result of the tool call is then used to create a user-friendly response.
```


## The Tool Calling Flow

1. User requests to the LLM are always accompanied by a list of possible tools available
2. The LLM response indicates in a JSON format which tool with which parameter(s)
3. The harness/code executes on the tool call request
4. The tool/function output is then sent to the LLM
5. The LLMs final response integrates the user request, the tool output, and the enhanced LLM response

> You can have multiple tools, and multiple sub loops to process the tool calls sequentially or even in parallel!

```plain

<-\[o_o]/--c
x--|---|--C
 _/|___|\_

```

# Lack of Standards

**This is a rapidly evolving area of technology. Tool specifications are different for every model**

The "check if the LLM response is JSON with a key 'name'" is my hack to work around a lack of standards:

- OpenAI: inspect **output items** where type == "function_call" , <https://developers.openai.com/api/docs/guides/function-calling>

- Anthropic: inspect **content blocks** where type == "tool_use" , https://platform.claude.com/docs/en/agents-and-tools/tool-use/define-tools#model-responses-with-tools
- - <https://github.com/anthropics/anthropic-sdk-go/blob/main/examples/tools/main.go>


- Gemini: inspect **content parts** that have a function_call object  <https://ai.google.dev/gemini-api/docs/function-calling>


- MLX indicate "tool call format is model specific" <https://github.com/ml-explore/mlx-lm/blob/main/mlx_lm/examples/tool_use.py>

- The open source "OpenCode" repo deliberately handles each separately: <https://github.com/anomalyco/opencode/tree/dev/packages/llm/src/protocols>


**MCP as a standard** pushes LLM vendors to provide a compatible developer experience:

- <https://modelcontextprotocol.io/specification/2025-06-18/server/tools>


## 2026 Addendum

The well crafted open source agent harness "Pi" handles the problem elegantly (if you directly support multiple AI vendors you will need the Adapter Pattern):

- <https://pi.dev/>
- <https://formulae.brew.sh/formula/pi-coding-agent>

- <https://github.com/earendil-works/pi/blob/main/packages/agent/src/agent-loop.ts#L202>

- <https://github.com/earendil-works/pi/blob/main/packages/ai/src/providers/openai-responses-shared.ts#L90>



# More Resources

- <https://ampcode.com/notes/how-to-build-an-agent>

- <https://ghuntley.com/agent/>
- - <https://github.com/ghuntley/how-to-build-a-coding-agent/blob/trunk/README.md>


