Title: Voice dictation and overcoming friction with Claude Code Cloud sessions
Date: 2026-10-02 11:11
Tags: ai, agent, productivity, voice

[TOC]

Liberating yourself from the laptop is part of the promise of this new Era of AI. 🙌

Using your voice to dictate to your agent: ideas to be researched, projects planned, and of course, have it write the code!

My previous experiments on agents in the cloud have proven to me that being untethered and quickly/casually sending prompts improves productivity  <https://blog.john-pfeiffer.com/real-velocity-from-a-backlog-deferred-and-a-skilld-agent/> 

I eventually got Claude Code Cloud to work, and it's genuinely helpful, but the process reminded me of how much these AI vendors are attempting to lock you in to a very narrow walled garden. 🤔

# Voice

> "This is the way"

Having an agent in the cloud means you don't need that cpu (desktop/laptop) physically in front of you. (The GPUs and most advanced LLMs are already in the cloud). Going all the way means ditching the keyboard too!

*I alternate between Wispr Flow (highest quality), Apple's built-in (best integration), and the AI vendor's voice dictation option.*

I open one thread and dictate for it to start research on an idea - the agent does a lot of searching and synthesis. I open another thread and have it fix a bug in a repo. All while walking or washing dishes.

Many Pros:

- hands free means you can do it while walking or otherwise not typing or at a keyboard
- it is genuinely faster to convey a lot of information
- low friction means you are more likely to add details or a followup correction
- it captures your authentic tone and natural expressions
- more context in a prompt (that the friction of typing often reduces) actually improves the behaviors of LLMs

A few Cons:

- poor speech recognition will end up with the wrong words = completely wrong prompt
- a stream of consciousness jumping between topics is not a good prompt
- when you put out a lot of text - then editing it takes longer
- sometimes you get random real world snippets about driving, food, or family members 😹


Yes it feels weird to suddenly be having long conversations (maybe just whispering) with your computer or your phone - with an AI. Conversely it is totally normal to have long conversations with a coworker.

*I use the GitHub mobile app to review and approve and merge*

# Build vs Buy and an off the shelf commodity

I've already cobbled together a version of "agent in the cloud": <https://blog.john-pfeiffer.com/a-coding-agent-in-the-cloud-with-factory-and-railway/>

Yet the slick Claude mobile app and a $1T company's product and engineering resources probably make for a superior experience?

*Anthropic bundle the cloud compute, sandbox, and network in for free: understandable since LLM tokens are at least an order of magnitude more expensive!*

A little confusing in the UI and terminology: Claude chats, but Code sessions. Local Projects can be code folders, and a new Code session can be Local.

The easy part was setting up an Environment: Cloud, Full network access (it's their infra), didn't trust it with an API creds yet

- <https://code.claude.com/docs/en/cloud-environments>



## Troubleshooting 403 Errors

> This does not work: I am not "holding it wrong" =|

From my previous experience and security best practices, I tried to setup the Claude "Code" app with a dedicated "agent github account". I as the human own a code repository, the agent is a collaborator on the repo.

I connected my Claude account to my agent's GitHub account, and only gave it access to a single unimportant code repository. *least privilege, start with low risk and low consequence*

A new "cloud session" in the mobile app successfully pulled down the code, and based on my prompt did a bunch of research and prepared code changes...

Then it got a 403 when trying to push the branch to remote. It prompted me to check my github connection and to either try the Claude GitHub App or add a Personal Access Token to the environment.

I provided a Personal Access Token. Nope - still 403's

The LLM tried to be helpful, so many suggestions of what I was doing wrong.

1. Are you sure that was the correct repository?
1. Are you sure you are the owner of the repository?
1. Are you sure the agent's account has accepted the collaborator invite for that repository?
1. Verify your intended local `gh` credential can access the repository with `gh repo view OWNER/REPO`
1. In the local Claude Code CLI, sign in to your Claude account using `/login`, run `/web-setup` and approve uploading that `gh` token to Anthropic
1. You may need to start a new session to see the permissions take effect


# Authorization and Control

GitHub already is a platform: along with organizational roles and permissions, it supports APIs, OAuth, Personal Access Tokens... it even has a CLI (`gh`)

The crucial distinction is between **authentication** and Anthropic's authorization rules.

Anthropic says all GitHub operations in its hosted environments pass through a dedicated proxy. That proxy restricts API and access to repositories attached to the session, limits git pushes to the session’s working branch, etc.

Most tellingly, its documentation says:

> “The restriction applies to every request through the proxy regardless of the credentials you supply, so a `GH_TOKEN` you set gets the same 403.”

| Path or feature | Documented behavior |
| :-- | :-- |
| Browser GitHub connection | Private repositories require the Claude GitHub App; public repositories can be cloned without installing it on their owners’ accounts. |
| CLI `/web-setup` | Uploads the token returned by local `gh auth token` to your Claude account. User-started cloud sessions can access repositories that token can access, without the Claude App. |
| Project threads | Require the Claude App on each repository they clone, even if you connected through `/web-setup`. |
| PR auto-fix | Requires the Claude App. |
| `GH_TOKEN` inside the cloud environment | Supported for scripts and `gh`, but does not remove the cloud proxy’s restrictions. |



## Claude GitHub App

> Not simply a remote machine running `gh` with credentials

If you don't want to give the Claude GitHub App access to all of your repositories, then you configure "Only select repositories". That integration applies only to Claude cloud sessions.

With a collaborator who has been added to repositories that already occurred; it's explicit. The Personal Access Token conveys that permission grant regardless of cloud sandbox, laptop, or any other place.


The downsides of the Claude GitHub App:

- tight coupling: switching costs increased since now there's an app installed on every repo
- the expansive permission footprint: Anthropic uses one official App across multiple features, requesting write access to Actions, Checks, Contents, Discussions, Issues, Pull Requests, Repository hooks, and Workflows

Its docs explicitly acknowledge that individual features don’t need all those permissions, yet installing the App requires accepting the full set

<https://code.claude.com/docs/en/github-actions#github-app-permissions>

And truly supporting a non-GitHub-App install is "Not Planned" <https://github.com/anthropics/claude-code/issues/57641>

This app deliberately puts an Anthropic-controlled layer between you and GitHub.

# Summary

For $20 a month with subsidized tokens and a polished UX I'll use it for specific code repositories and projects.

After frequent outages, models getting nerfed or pulled entirely, (silent) "fallback" to a different model, refusals even on non-sensitive topics, and a distinct trend of verticalization and lack of choice/control... I'm keeping my options open with other approaches and vendors.

# Appendix

## Cloud Environment Customizations

- Yes to Environment variables to ensure a specific Cloud Environment maps to Staging or other overrides.
- Self-hosting the container/sandbox is sensible for full audit controls.
- Locking down network access to specific domains does sound like a useful tool for specific situations.
- I haven't thought through a startup shell script - but that does sound like a shim for bootstrapping infrastructure as code for reproducible sessions.

## References

- <https://claude.com/blog/claude-code-on-the-web>

