Title: Code is for Humans
Date: 2017-02-25 20:34
Tags: programming, readability, immutable, configuration, dependencies

[TOC]

## Code is the automation of a solution

I often feel like the purpose of Programming is lost in the many discussions and debates about Programming.

1. Sometimes the code is conflated as being the solution.  Whatever problem is being worked on has to be thought through and different possible solutions evaluated.  Then one approach has to be implemented and tested.  That implementation can take many forms: <https://en.wikipedia.org/wiki/Turing_completeness>

2. Alternatively a solution is seen as perfected because it is written in code.  Yet all it takes is one more edge case, one more nuance on a variable, and the "solution" will fail.  (Bugs!)  Perhaps this is because the trivial examples of coding are often related to math, like adding two numbers, that we are somewhat misled to believe that the correct code will always solve the problem (and amplified by Computer Science which uses proofs to mathematically prove algorithmic solutions).  <https://en.wikipedia.org/wiki/P_versus_NP_problem>

3. Selecting the correct algorithm assumes understanding of the problem, the constraints, and of course the end goal.  Much like picking an off-the-shelf tool or open source library or framework, there has to be some comprehension of whether their solution is your solution.

The purpose of the automation is to repeatedly solve the problem (assuming the same environment and same inputs).

So first you really have to sit down and think through the solution.  Usually this involves pen (or pencil) and paper though the whiteboard is certainly one of my favorites.

I certainly understand people who want to work towards solutions by coding (i.e. the IntegratedDevelopmentEnvironment and programming paradigm as just another tool for our brains) but I suspect it can also lead to distractions of accidental complexity (limitations or unfamiliarities of the programming language syntax/framework) and sometimes worse yet unnoticed biases of the tools preclude some of the best solutions.  (The infamous "imperative vs functional" debates ;)

- <https://en.wikipedia.org/wiki/Imperative_programming>
- <https://en.wikipedia.org/wiki/Functional_programming>

Non trivial problems will require solutions that involve tradeoffs and compromises (i.e. the classic "execution time" vs "resources required").

- <https://en.wikipedia.org/wiki/Software_engineering>

## Code is for humans, not computers

Human readable code must be transformed into instructions for a machine which is what executes all of the computations.  The machine has no understanding of whether the instructions will solve the problem.

- <https://en.wikipedia.org/wiki/Compiler>
- <https://en.wikipedia.org/wiki/Machine_code>

This fundamental impedance mismatch is one of the major challenges to programming.  Humans do not always know all of the correct instructions to provide.  Machines will faithfully execute whatever is given to them, including conflicting commands or erroneous data.

So the history of the abstraction of computer programming very often reads like the evolution away from the physical hardware towards humans expressiveness because the better able we are to describe something the more likely we are to document a correct automation of a solution.

- <https://en.wikipedia.org/wiki/History_of_programming_languages>

### Solving Yesterdays Problems of Performance

While the earliest hardwired machines filled large rooms and had different kinds of accidental complexity and bugs
<https://americanhistory.si.edu/collections/search/object/nmah_334663> , later generations had to deal with getting the most performance out of the machines <https://en.wikipedia.org/wiki/Assembly_language#Historical_perspective>.

These powerful low level languages can also generate some of the most persistent and pernicious bugs via manual memory management, pointers, and buffer overflows.

- <https://en.wikipedia.org/wiki/C_dynamic_memory_allocation#Common_errors>
- <https://en.wikipedia.org/wiki/Software_bug#Resource>

The amount of developer time required to create correct code has dramatically reduced as the speed of computation has increased and the tools (including the programming languages) are better able to "get out of the way" and avoid the accidental complexity of optimizing for performance.

> It is rare that the purpose of a program is to add numbers as quickly as possible

### Programming languages help with explicitness by removing ambiguity in natural languages

A sentence in English, "We saw her duck", can have multiple meanings <https://en.wikipedia.org/wiki/Ambiguity#Linguistic_forms>)

Programming languages force human expressiveness to be less ambiguous (i.e. the responsibility of the mismatch impedance of incorrect instructions falls squarely on the humans).

- Names are important and should be well thought out <https://en.wikipedia.org/wiki/Naming_convention_(programming)>
- Short variables and acronyms can confuse, mislead, or misdirect other humans who will modify or extend code based on that misunderstanding
- Performance specific changes can become digressions and noise that distract or make brittle the tracing of the required solution logic

## Explicit communication because magic is incomprehensible

The problem with short meaningless variable names in unreadable code littered with performance optimizations is they prevent solving **The Problem**.

Some considerations and anti-patterns:

- Straight to coding (no research)
- - Real time systems that keep an aircraft in the air must pay attention to runtime constraints
- - Overlooked requirements and misunderstanding the problem domain
- - Not knowing what the correct answer will look like (i.e. not having test/control inputs and outputs)
- Absence of acceptance tests to prove that it really is solved and the infamous "it works on my machine"
- The fallacy of "Perfection"; for a solution to provide value there has to be a mechanism to empirically prove it works
- "Done" is not "code complete" (even with tests ;) , it is Integration Tests, Acceptance Tests, Performance Tests, Soak Tests, actually shipped to the "wild" where it survives real environments and edge cases
- Intermittent behavior = automating of a solution should provide consistent results
- Ideologue = a technology looking for a problem
- Premature Optimization <https://en.wikipedia.org/wiki/Program_optimization#When_to_optimize>
- Premature Generalization <http://wiki.c2.com/?PrematureGeneralization>
- <https://en.wikipedia.org/wiki/Spaghetti_code>
- <https://en.wikipedia.org/wiki/Big_ball_of_mud>
- Now is the only time that matters, when actually the more successful you are the more likely the code will continue and need maintenance <https://en.wikipedia.org/wiki/Software_maintenance>

## Process Improvements to actually Solve a Problem

Considering the complexity required to actually solve a problem it would be fair to say many iterations are required.

Some of the "tools" that have helped the iterative process:

- Software <https://en.wikipedia.org/wiki/Stored-program_computer#History>
- Testing <http://web.archive.org/web/20161024015955/http://www.testingreferences.com/testinghistory.php>
- Logging <https://engineering.linkedin.com/distributed-systems/log-what-every-software-engineer-should-know-about-real-time-datas-unifying>
- Monitoring
- Automated deployments
- Version Control <http://web.archive.org/web/20170104162946/http://layervault.tumblr.com/post/102541175774/the-history-of-version-control>

Additionally any implementation must be bound by a "good enough" state as perfection cannot coexist with the ever changing real world.

Data is required to understand progress (or regression).

Humans must keep modifying until "done" (even in the advanced example of <https://en.wikipedia.org/wiki/Genetic_programming>)

The steady increase in computing power (<https://en.wikipedia.org/wiki/Moore%27s_law>) means **Maintainability trumps Performance**.  Being able to get reproducible results was codified long ago in the <https://en.wikipedia.org/wiki/Scientific_method>. =]


### Collaboration and Crowdsourcing without Group Think

There seems to be a strong reaction to the term "pair programming" and it is no uncommon for code reviews and pull requests to be a source of emotional angst and team friction.

These techniques are well established ways of improving quality:

- <https://en.wikipedia.org/wiki/Pair_programming>
- <https://www.microsoft.com/en-us/research/publication/pair-programming-whats-in-it-for-me/>
- <https://en.wikipedia.org/wiki/Code_review>
- <https://en.wikipedia.org/wiki/Distributed_version_control#Pull_requests>

While the myth of the individual genius over-emphasizes the outlier it is far more common for a group to achieve projects of any large size (even with software and technology acting as a multiplier).

I am not advocating pure democracy (or just accepting status quo) as the only way of building things but it is clearly preferrable to have a variety of skills (i.e. architecture, mathematics, verification, design, etc.)

It may be that working together on intellectual endeavours is currently less intuitive for humans than working together on physical challenges and that a fledgling industry that is chronically short of trained and experienced workers is not selecting and creating environments that are conducive to group working.

One of the most challenging aspects is disambiguating where something has been successful in the field (mature) versus "it's always been that way" complacence.  Different isn't always better but should always be honestly evaluated.

- <https://www.bloomberg.com/news/articles/2014-04-10/the-myth-of-the-lone-genius>
- <https://en.wikipedia.org/wiki/The_Wisdom_of_Crowds>
- <https://en.wikipedia.org/wiki/Groupthink>
- <https://en.wikipedia.org/wiki/Genetic_diversity>


## Configuration Patterns

Configuration is just another part of "Do Not Repeat Yourself" <https://en.wikipedia.org/wiki/Don't_repeat_yourself> .

Without configuration each program would have to be rewritten with the a new "configuration" portion hardcoded each time. (Though software is an improvement over having to build new hardware for each new configuration...)

So it is a pragmatic way to extend the utility of an automated solution.

"When should configurations be applied"?

- Configuration is passed as a parameter when the program first starts
- Configuration is loaded from a configuration file when the program first starts
- Configuration is loaded from Environment variables when the program first starts
- Configuration is loaded from a configuration file whenever a change to that file is detected by the program
- Configuration is loaded from a configuration file whenever a module is loaded (i.e. "lazy loading")
- Configuration is loaded from Environment variables whenever a module is loaded (i.e. "lazy loading")

- <https://12factor.net/config>
- <https://en.wikipedia.org/wiki/Lazy_loading>

> For a short execution time there is little difference between loading at startup versus runtime

What are the impacts of restarting the service (in order to reload the new configuration changes)?

Are there parts that have to be loaded first and then wait for a slower dependency to be available?

## Prefer Determinism for Reasonability

Loading and initializing all configuration when the program first starts is one way of attempting to create determinism in the code paths that are running in memory.

The benefit of "hot swapping" is applying changes to existing code while it is still running.

The computer is not going to get confused.  It does not care if the data being passed to the module in memory is correct or incorrect, but the new dynamic result may ruin that beautifully automated solution, sometimes in almost undetectable ways.

As we humans struggle with ever increasing complexity (both in the software and hardware) we should focus on how to reduce variability (that includes during coding, during compilation, and especially at run time).

Some alternatives tend to take advantage of the cheaper cost of computing and increasingly distributed/networked systems:

- Send a reconnect signal to clients to use a new endpoint
- Start up a second process and have the operating system pass the network connection from the old to the new process
- A Load Balancer or other connection holding component that can direct traffic to the new service

<https://www.martinfowler.com/bliki/BlueGreenDeployment.html>


## Modularity

Smaller pieces can be easier to understand and assert for validity.  The "Do One Thing" principle helps the human who is composing a solution (ideally from re-usable components) to understand which tool is right for the job.

This also allows for leveraging "seams" to investigate or decouple code (which drastically helps with maintenance).

- <https://en.wikipedia.org/wiki/Single_responsibility_principle>
- <http://web.archive.org/web/20160803161738/http://www.informit.com/articles/article.aspx?p=359417&seqNum=2>

Updating, upgrading, or replacing a well defined component will be easier than something that is tightly interwoven with all of the other pieces.

There is a natural tension with re-usability since something with a slight modification that can be re-used reduces the overall code footprint.  The key here is a clear understanding of whether the actual test footprint and complexity have been reduced.

Also it is possible to decompose into such small parts that they have no logical coherence =[

## Immutability

One last technique I would like to highlight is immutability.  The idea is by preventing change it can be easier to trace and determine the expected outcome.  (Or discover the exact point at which there is an unexpected deviation).

- <https://en.wikipedia.org/wiki/Immutable_object>
- <https://martinfowler.com/bliki/ImmutableServer.html>
- <http://web.archive.org/web/20161030171510/http://blog.codeship.com/immutable-infrastructure/>

It comes at a trade-off of increased resource consumption (i.e. memory) and creating an unmanageablely large number of entities (with possible corresponding orchestration or scale issues)

Functional programming definitely tends towards immutability ;)
