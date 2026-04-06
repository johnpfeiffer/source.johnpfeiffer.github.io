Title: AI Natives do not question the gifts from the gods
Date: 2026-04-03 23:59
Tags: ai, career, engineering, management, leadership, navigating change

[TOC]

# AI Natives don't question the gifts from the gods

At a recent SF hackathon we used ChatGPT to understand Clinical Trials, defaulted to Claude Code to code up everything, and used LangChain plus Minimax LLMs as the core solution.

My teammates are AI natives: just graduating from university and they don't question the answers at their fingertips.

Unfazed by the entirely new-to-them problem space of clinicaltrials.gov being a mess. Valuable information with awkward technology and clunky documentation was unlocked in just a few hours of "vibe coding".

No hesitation to try something, see what happens, and then just prompt again. Any unfamiliar domain term or technical issue is resolved with a quick prompt. No google, no stack overflow.

It was a joy to work with them and see the new possibilities as they take for granted the powerful capabilities and apply them without hesitation.

- <https://en.wikipedia.org/wiki/Prometheus> 🔥

# Reflecting on Arbitrage or Persistent Advantage

Extracting and analyzing data with a customized UI/product is now a weekend project, so what makes a business successful?

"Ship it" hackathon mode means we didn't spend any time thinking about the ["7 powers"](https://www.lennysnewsletter.com/p/business-strategy-with-hamilton-helmer). Identifying investment in opportunities based on clinical trials has no network effect, no economies of scale, no entrenched switching costs, no counter-positioning, no cornered resource, no branding, and especially no process power.

Or as [Warren Buffett popularized](https://www.berkshirehathaway.com/letters/1986.html)

> ...moat that protects a valuable and much-sought-after business castle.

Coding agents raise the software floor dramatically, which increases the speed of competition.

Cloning or reverse-engineering from an interface/API reduces the "Switching Costs" of migration, as exemplified by the recent fierce AI-powered cloud competition: <https://newsletter.pragmaticengineer.com/p/the-pulse-cloudflare-rewrites-nextjs>

Google DeepMind spun out Isomorphic Labs and Anthropic acquired Coefficient Bio because the major AI players recognize the deep moats in biotech; having very private data is more valuable than ever.


# What you get from People

When building something is cheaper and faster, how do you differentiate?

More than a business strategy, you need talented hard-working people who take the initiative because "Culture eats strategy".

Thanks to the organizers [Hanwha AI Center](https://hac.ai/event/detail/52) + [AI Valley](https://www.aivalley.io/hackathons/vibe-coding-hacathon-building-ai-for-finance/projects), the rooms were abuzz with energy. Everyone was participating in the future: fast experimentation and doing more with less.

In-person had creativity, spontaneous connections... and loud talking-over-each-other, not enough conference rooms, caffeine shortages, and lines for lunch and the bathroom.

## People vs Agents is a false dichotomy

Anthropic and OpenAI have unimaginably high valuations while profitable SaaS incumbents are feeling pressure from the stock market 2026 ["SaaSPocalypse"](https://www.bloomberg.com/news/newsletters/2026-02-04/new-ai-fear-unlocked-as-traders-ditch-companies-at-risk-of-disruption).

One way of viewing the world is replacing all human employees with AI agents = zero sum.

A more ambitious vision is augmenting every human in your org to 10x productivity.

But doubling business productivity doesn't help when your competitor has something magical with an AI-powered product. 🦄

**I believe tackling the hardest problems that AI now unlocks creates huge customer demand... which needs AI-augmented humans to keep up.**

# Too much of a good thing?

We were coding so fast that we quickly hit complexity overload and spent the last hour of the hackathon debugging. A [ball of mud monolith](https://web.archive.org/web/20210414115314/http://www.laputan.org/mud/), lots of AI-generated code, no tests. =(

Decades of experience suddenly became invaluable:

- Keeping the "main" core loop tight and easy to read
- Modularized code like separating "external vendor/network calls" into separate clients
- Each specific feature into manageable areas of partitioned complexity
- Compartmentalization of failures to not affect the rest of the application
- Logging, Tests

We need to question these "gifts from the gods", and know that hard-won principles still matter. Even when we're going as fast as possible for a hackathon demo.

Of course I'm disappointed we didn't win an award, but I am energized by seeing a glimpse of the future and connecting with the next generation of builders.
