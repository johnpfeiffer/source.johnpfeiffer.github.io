Title: Code Review and Project Structure - Consistency and Consensus
Date: 2022-06-04 11:22
Tags: management, manager, code review, architecture

[TOC]

# Managers Own Shared Processes

Messy, ambiguous, intersections of people and technology is exactly the domain of a great Engineering Manager. Caring about how people work together, understanding the organization as a system, and prioritizing business outcomes.

It may take experience and serious people skills to understand the technical domain and get consensus, buy-in, and even "disagree and commit".

## Code Review

Code Review Guidelines assist a team to focus on solving the hard problems instead of side quests and possible distraction in Pull Request Reviews.

Codebases transition ownership between individuals and teams over time, having a shared understanding and approach makes all of our work easier.

Creating a new project should be low friction and easily and automatically leverage existing tools (e.g. CI/CD).

Also, Code Review can not only be a silent inefficiency in people hours, but could be a real bottleneck in your SDLC and release frequency.

- Your *goal* is reduced friction and increased value delivery
- Your *output* is an authoritative documented process

*Leverage delegation to the people most invested and experienced, and have a schedule/process for revision and improvements =)*

One thing I've found really helps is "standing on the shoulders of giants": prior art and approaches rather than re-inventing the wheel.

As an example, Golang is a pragmatic production language: `gofmt` as a built in tool and concept standardizes the style removing a whole class of discussions ("tabs vs spaces").


# A philosophical question - Why Review

> Why do we do Pull Request Reviews?

I ask many engineers this in 1:1s, some of the most common (and good) answers:

- to find bugs
- to prevent issues in production
- to call out missing test coverage
- to raise concerns about coding patterns
- to have consistent coding style
- to educate others on best practices
- shared understanding of the codebases

I somewhat cheekily provide my zinger: **"To merge the code and ship something valuable"**

When there is a bug affecting a User, or some incredibly valuable feature that needs to go out, we should consider the goal of our org/group.

## Separation of concerns

Overloading the Review process may mean we lose sight of our true goal, or that the review burden becomes so high people instinctively do less or do it begrudgingly.

- we need automated tests (dev, staging, synthetic for production) to verify correctness
- we use observability to monitor production - the "unknown unknowns"
- we can and should use tools like **linters** for automatically enforcing shared code style
- we can use pair programming or lunch and learns or dedicated study time to learn codebases and coding patterns

Our work is to help others get their work done.

## Some Successful Strategies

There are a number of things I've learned (thank you all previous co-workers and the internet!) and used successfully:

- Small Pull Requests: less to review so better focus, less change **usually** means less risk
- - <https://robertheaton.com/2015/10/26/why-and-how-to-make-smaller-pull-requests/>
- TestDrivenDevelopment: "Red" is first only add tests that fail, "Green" is doing the minimum code changes to make the tests pass
- Heuristics for Quickly Scanning: <https://robertheaton.com/2014/06/20/code-review-without-your-eyes/>
- Sandi Metz on "code smells" <https://www.youtube.com/watch?v=MksJTtt7jS4&t=93s>

## Communication

Given that our goal is to unblock a team mate from shipping something valuable for the Users/Customers/Company, it's worthwhile to ensure our interactions are truly helpful.

The core of it is: clarity is kindness, recognize you are communicating with another being, not just "fixing a code problem".

I have found the following articles to do a great job and defer to them:

- [Alex Hill's Giving and Receiving Code Reviews](https://web.archive.org/web/20200111065923/https://www.alexandra-hill.com/2018/06/25/the-art-of-giving-and-receiving-code-reviews/)
- <https://web.hypothes.is/blog/code-review-in-remote-teams/>
- <https://github.com/google/eng-practices/blob/master/review/reviewer/comments.md>


# Template for Doing a Code Review

Here's Google's, but read onward for my take ;)

- <https://github.com/google/eng-practices/blob/master/review/reviewer/looking-for.md>

- <https://talks.golang.org/2014/names.slide>
- <https://dave.cheney.net/practical-go/presentations/qcon-china.html#_avoid_package_names_like_base_common_or_util>


## A guide for doing a review  

1. Scan for structure, areas of interest, obvious/large concerns (i.e. separation of Infra and Domain)
2. Consider intent, confirm source of truth and canonical documents
3. Is this a moment to escalate, or "end early and reframe"?
4. Spend X minutes writing review comments
5. Pause: double check prioritization, Communicating well 
6. Spend X minutes writing review comments
7. Decision: do you approve or just directly notify the author you have done a review


### Priority order

- Understood intent?
- Correctness/security/operational risks?
- Context needed before requiring changes?
- Maintainability/readability/test improvements?



### Pragmatism

- avoid comments/suggestions that lead to rewriting everything
- avoid over-indexing on style
- identify the smallest safe fix
- ask whether context changes the decision



### Correctness and safety

- Edge cases
- Error handling
- Auth/authz
- Nil/Null/zero-value behavior
- Ordering assumptions and logical dependency
- Production operability
- Timeouts
- Data races
- Cancellation, Clean Exits, and Partial failures
- Retries and Idempotence
- Backpressure
- Observability
- Data consistency, Transaction boundaries, Atomicity

### Maintainability

- Separation of concerns
- Cohesion
- Locality of behavior
- Interface size
- Readability
- YAGNI / over-abstraction


## Shorthand list of Concepts to Suggest

- deterministic, least surprise
- idempotent, copy vs dependency/mutation
- boundary, contract, pipeline, modeling (OO and “semantics”), impedance mismatch
- modular, decompose
- locality, cohesion
- encapsulation, abstraction, distraction by details
- open-close principle, ripple effect
- composition
- KISS, DRY (rule of 3 or 5?)
- single responsibility, separation of concerns
- least privilege, conservative defaults, god object
- nil and null and zero values
- fail fast, “outdent”
- atomic/transactions - cancellation/failure mode, partial, split brain
- race condition, out of order
- unbounded growth/exploding work
- readability, YAGNI, prefer explicit
- observability, logging/debugging, causality
- TestDrivenDesign (TDD) and BehaviorDrivenDevelopment (BDD)

### Example format for review comments

```
Blocking (correctness): no test coverage
Suggestion: have a clear set of test cases focused on happy path and critical edge cases, consider TDD
```

```
Non-Blocking (observability): no log statements
Suggestion: a few log statements of concrete progress in the workflow and safe-to-log Identifiers will make any future debugging a lot easier 
```

# Code Project Layout

> What goes Where?

A complement or almost pre-cursor to code review is which files go in which places in a code repository.

A manager can and should facilitate the understanding and standardization of common structure(s) that clarify and speed things up.  

**Principles**

- Should follow a convention
- Should be easy to read and understand
- Should be easy to maintain
- - including easy to test (i.e. empirically prove correctness, confidence of expected behavior in production)
- Should be re-usable

## Hexagonal Architecture

Where something goes should not be arbitrary, it should have a **Why**.

Having a well reasoned theory behind the file layout approach helps guide all the numerous decisions in a logical and consistent way.

Consider the benefits of this framing <https://en.wikipedia.org/wiki/Hexagonal_architecture_(software)>

> Applications work like this: Events arrive from the outside world. The transformer converts it into a usable procedure call or message and passes it to the application. The application is blissfully ignorant of the nature of the input device 

- *<https://wiki.c2.com/?HexagonalArchitecture> (Alistair Cockburn)*



```text

        [UI]        [CLI]        [Database]        [Email]        [Logging]
          \           |              |               |              /
           \          |              |               |             /
            v         v              v               v            v

      +----------------------------------------------------------------+
      |                            FRAMEWORK                           |
      |  HTTP, routing, persistence libraries, queues, SDKs, vendors    |
      |                                                                |
      |   +--------------------------------------------------------+   |
      |   |                      APPLICATION                       |   |
      |   |        use cases, commands, workflows, orchestration    |   |
      |   |                                                        |   |
      |   |   +------------------------------------------------+   |   |
      |   |   |                     DOMAIN                     |   |   |
      |   |   |       entities, value objects, domain logic     |   |   |
      |   |   |                                                |   |   |
      |   |   |        +------------------------------+        |   |   |
      |   |   |        |         CORE DOMAIN          |        |   |   |
      |   |   |        |   key business rules         |        |   |   |
      |   |   |        |   invariants                 |        |   |   |
      |   |   |        +------------------------------+        |   |   |
      |   |   +------------------------------------------------+   |   |
      |   +--------------------------------------------------------+   |
      +----------------------------------------------------------------+

             adapters talk inward through ports / interfaces

```


If you’re just writing a one-off script with 3 files, maybe your project/repo can be "flat" - but the general consensus is that this is not good for anything of complexity.

## Concrete Project Layout in Go

Top-level directories:

- `cmd` (for your binaries) 
- `pkg` (for your packages)
- `clients` (for external dependencies)

> Group by context, not generic functionality.

- Mocks: shared subpackage

All other project files (fixtures, resources, docs, Docker, etc) in the root dir of your project.

The `main` package initialises and ties everything together.

*Avoid global scope and init()*

- [GopherCon 2018 - How do you structure your Go Apps by Kat Zien](https://www.youtube.com/watch?v=oL6JBUk6tj0&t=681s)

- [GoLab 2018 - DataDog Project layout patterns in Go by Massimiliano Pippi](https://youtu.be/3gQa1LWwuzk?si=RiyzUL_37Vn9D2DH&t=503)

- A standard/template people can leverage: **<https://github.com/golang-standards/project-layout>**


# More Resources

- <https://www.educative.io/blog/how-to-build-maintainable-web-apps-with-hexagonal-architecture>

