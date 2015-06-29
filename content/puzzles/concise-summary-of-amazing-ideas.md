Title: A concise summary of amazing ideas
Date: 2011-08-08 00:00
Tags: thoughts, tdd, lean, persuasion

[TOC]

### Test Driven Development (TDD)
Test, Code, Refactor <http://en.wikipedia.org/wiki/Test-driven_development>

### Lean
- Lean: Identify Value -> Breakdown Steps -> Continuous Flow -> Reduce Waste
- Lean Startup: Measure, Learn, Build <http://theleanstartup.com/principles>

### Better than Free 
<http://www.kk.org/thetechnium/archives/2008/01/better_than_fre.php>

1. immediacy
2. personalization
3. interpretation/support
4. authenticity
5. accessibility
6. embodiment
7. patronage
8. findability

### Persuasion 

<http://en.wikipedia.org/wiki/Robert_Cialdini>

1. reciprocity 
2. commitment/consistency
3. social proof
4. authority
5. liking
6. scarcity

### Competition and Profit 

<http://en.wikipedia.org/wiki/Porter_five_forces_analysis>

1. Threat of new competition (barriers to entry, customer loyalty, desirability of that industry/biz model)
2. Threat of substitute products or services (switching costs, quality, compatibility)
3. Bargaining power of customers (switching costs, market options, dependency for other services)
4. Bargaining power of suppliers (switching costs, supplier choice, supplier becoming competitor)
5. Intensity of competitive rivalry (innovation, branding, economies of scale)

### Schelling's segregation model
micromotives and macrobehavior , <http://en.wikipedia.org/wiki/Thomas_Schelling#Models_of_segregation>

Granovetter threshold model for peer effect on collective behavior and Strength of Weak Ties (aka how LinkedIn gets you a new job)

<http://en.wikipedia.org/wiki/Mark_Granovetter>


### Cognitive Biases
- Bandwagon Effect (Groupthink)
- Confirmation Bias: search for and interpret information and memories that support preconceptions
- Gambler's Fallacy: future probabilities are affected by previous outcomes
- Negativity Bias: paying more attention to bad news
- Neglect of Probability: disregarding probabilities when making a decision (risk of flying versus driving)
- Observational Selection Bias (Frequency Illusion): noting something previously ignored results in a misconception that it has increased in frequency 
- Projection Bias: wrongly presuming others think like us
- Status Quo Bias: things should stay the same

### Logical Fallacies and Disinformation
- Appeal to probability: because something could happen it is inevitable that it will happen (see Gambler's Fallacy and Neglect of Probability)
- Silence, Indignant, Rumors, Straw Man, Ad Hominem, Hit and Run, Question Motives, Invoke Authority, Play Dumb, "That's old news", Confess to a lesser item and "come clean", Enigma, Rube Goldberg Logic, Demand a complete solution, Fit the facts to alternate conclusions, Remove witnesses/evidence, Change the subject, Antagonize, Ignore proof and demand impossible proof, False evidence/facts, Loudly call for a separate investigation (ideally either biased or with confidential findings), Manufacture a new truth, Larger distractions, Silence critics, Lie low

<http://www.nowandfutures.com/spew_tools.html>


### Keys to being successful
- lists
- organize (categorize)
- prioritize
- schedule

brainstorm goals & feelings: "say what you're going to do and then do what you say"

#### Concentrate, Iterate, Automate, Validate, Appreciate
- Software version: core tech strengths & problem, quick releases, automate, test!, style? + recognize the contributions
- Military version: core strength and enemy weaknesses, rapid short executions, make excellence a reflex, check for brittleness, engender loyalty

#### 7 habits of highly effective people
1. be proactive
2. "begin with the end in mind" (envision the goal)
3. "put first things first" (order and prioritize)
4. "think win-win" (good outcomes for everyone)
5. "Seek First to Understand, Then to be Understood" (listen, then persuade)
6. "synergize" (teamwork)
7. "sharpen the saw" (sustainable balance)

<http://en.wikipedia.org/wiki/The_7_Habits_of_Highly_Effective_People>

### Important Software Concepts

- Do Not Repeat Yourself (DRY)
- Model View Controller (MVC)
- Atomic Consistent Isolation Durability (ACID)
- Abstraction Polymorphism (overloading, inheritance, overriding interface) ,  Inheritance , Encapsulation
- Consistency Availability Partition tolerance vs Basically Available Soft-State with Eventual consistency
- Nondeterministic Polynomial ... NP-hard <http://en.wikipedia.org/wiki/NP-hard>
- - NP-complete (subset sum problem can be verified) <http://en.wikipedia.org/wiki/NP-complete>
- - co-NP (verifier of "no" answer")

<http://en.wikipedia.org/wiki/Timeline_of_algorithms>

#### Amdahl's Law
- A system cannot be sped up by parallelization more than the inherently serial steps <http://en.wikipedia.org/wiki/Amdahl%27s_law>
- - So benchmark your system, then determine what parts can be parallelized and how much that will improve the result and how much will it cost to do so

#### Conway's Law
- The system design produced by an organization will reflect the organization's communication structure. <http://www.melconway.com/Home/Conways_Law.html>
- - <http://www.thoughtworks.com/insights/blog/demystifying-conways-law>
- - Possibly disastrous results when combined with Groupthink <http://en.wikipedia.org/wiki/Groupthink>
- - Commonly referred to when considering how adding a new person or new team to organization will affect productivity

####  Brooks' Law
- Adding resources (people) later in a project will make it even later <http://en.wikipedia.org/wiki/Brooks%27s_law> 
- - A decent observation given the above "laws": if a task has serial parts adding people (parallelization) will not speed it up AND every person will have to interface 

#### Moore's Law
- Computing power will double (or become cheaper by half) every two years <http://en.wikipedia.org/wiki/Moore%27s_law>
- - Sustained in part by improvements in complimentary technologies like Memory, Storage, Cooling, etc.
- - At a certain point in the future potentially only possible using parallel computing but with an increased coordination cost (including software that leverages parellization)

#### Postel's Law
Be conservative in what you do, be liberal in what you accept from others

<https://en.m.wikipedia.org/wiki/Robustness_principle>

#### Laws of Unix

<http://en.wikipedia.org/wiki/Unix_philosophy#Eric_Raymond.E2.80.99s_17_Unix_Rules>

- Modularity: Write simple parts connected by clean interfaces.
- Clarity: Clarity is better than cleverness.
- Composition: Design programs to be connected with other programs.
- Separation: Separate policy from mechanism; separate interfaces from engines.
- Simplicity: Design for simplicity; add complexity only where you must.
- Parsimony: Write a big program only when it is clear by demonstration that nothing else will do.
- Transparency: Design for visibility to make inspection and debugging easier.
- Robustness: Robustness is the child of transparency and simplicity.
- Representation: Fold knowledge into data, so program logic can be stupid and robust.
- Least Surprise: In interface design, always do the least surprising thing.
- Silence: When a program has nothing surprising to say, it should say nothing.
- Repair: Repair what you can, but when you must fail, fail noisily and as soon as possible.
- Economy: Programmer time is expensive; conserve it in preference to machine time.
- Generation: Avoid hand-hacking; write programs to write programs when you can.
- Optimization: Prototype before polishing. Get it working before you optimize it.
- Diversity: Distrust all claims for one true way.
- Extensibility: Design for the future, because it will be here sooner than you think. (Or, to put it another way, your creations will last longer than you think!)

#### Clean Code
- Source Code is for humans, make it easy to read and understand
- The code is the authoritative source (comments add context)
- Leave the campground cleaner than you found it
- Tests reveal what the code outputs; clean code runs all of the tests
-  Meaningful Names
- Functions: A minimum number of parameters and the smaller the better
- Open - Close principle
- Single Responsibility (do one thing, and do it well)
- No Duplication (DRY)
- Objects allow modularity, Boundaries keep you sane
- Separate Constructing a System from Using it (and Initialization from Runtime)

### Fallacies of Distributed Computing
<https://en.wikipedia.org/wiki/Fallacies_of_distributed_computing>

1. The network is reliable.
2. Latency is zero.
3. Bandwidth is infinite.
4. The network is secure.
5. Topology doesn't change.
6. There is one administrator.
7. Transport cost is zero.
8. The network is homogeneous.

### Designers/Creators of Programming Languages

|Language|Creator/Designer|Year|more info|
|:-:|:-:|:-:|:-:|
| Fortran | John Backus | &nbsp; 1957 | &nbsp; <https://en.wikipedia.org/wiki/Fortran> |
| Lisp | John McCarthy | &nbsp; 1958 | &nbsp; <https://en.wikipedia.org/wiki/Lisp_(programming_language)> |
| C | Dennis Ritchie | &nbsp; 1972 | &nbsp; <https://en.wikipedia.org/wiki/C_(programming_language)> |
| C++ | Bjarne Stroustrup | &nbsp; 1983 | &nbsp; <https://en.wikipedia.org/wiki/C%2B%2B> |
| Perl | Larry Wall | &nbsp; 1987 | &nbsp; <https://en.wikipedia.org/wiki/Perl> |
| Python | Guido van Roosum | &nbsp; 1991 | &nbsp; <https://en.wikipedia.org/wiki/Python_(programming_language)> |
| Java | James Gosling | &nbsp; 1995 | &nbsp; <https://en.wikipedia.org/wiki/Java_(programming_language)> |
| PHP | Rasmus Lerdorf | &nbsp; 1995 | &nbsp; <https://en.wikipedia.org/wiki/PHP> |
| Javascript | Brendan Eich | &nbsp; 1995 | &nbsp; <https://en.wikipedia.org/wiki/JavaScript> |
| Ruby | Yukihiro Matsumoto | &nbsp; 1995 | &nbsp; <https://en.wikipedia.org/wiki/Ruby_(programming_language)> |
| Go | Robert Griesemer, Rob Pike, Ken Thompson| &nbsp; 2009 | &nbsp; <https://en.wikipedia.org/wiki/Go_(programming_language)> |





### A quick history of software (in ascii)

    hardcoded hardware (ENIAC) ->
      von neumann architecture (stored programs) ->
        mainframes with custom punch cards (assembly) ->
          procedural code (fortran, c) ->
            object oriented (simula, java) ->
              parallel programming ->
                Artificial Intelligence that writes self adapting Domain Specific Langauges for everything?

Start by reading all of the following to nitpick how the above is fast and loose with history and the truth...

- <http://en.wikipedia.org/wiki/Computer>
- <http://en.wikipedia.org/wiki/ENIAC>
- <http://en.wikipedia.org/wiki/Von_Neumann_architecture>
- <http://en.wikipedia.org/wiki/Programming_paradigm>
- <http://en.wikipedia.org/wiki/Object-oriented_programming#History>
- <http://en.wikipedia.org/wiki/Parallel_computing#Software>
- <http://en.wikipedia.org/wiki/Concurrent_computing>

### Hacker's Jargon
- <http://www.catb.org/jargon/oldversions/>

