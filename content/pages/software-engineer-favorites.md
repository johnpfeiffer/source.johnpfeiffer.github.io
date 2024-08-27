Title: Software Engineer Favorites

[TOC]

This is roughly ordered as

1. learn to do
2. do it well
3. it lives in production
4. big concepts and big picture
5. protect
6. learn from others

_(if you are in a hurry, ask your favorite/best AI to summarize any of these ;)_

# Programming Craft

Books take more investment, yet when they have stood the test of time it is because they have incredible value and information density

_Podcasts tip: listen at 1.5x or 2x speed_

- The Pragmatic Programmer: From Journeyman to Master by Andy Hunt and Dave Thomas
- Foundations of Programming - Building Better Software by Karl Seguin

- Clean Code by Robert C. "Uncle Bob" Martin
- Working Effectively with Legacy Code by Michael Feathers
- <https://www.se-radio.net/2017/06/se-radio-episode-295-michael-feathers-on-legacy-code>
- <https://fragmentedpodcast.com/episodes/219/> (the legacy code change algorithm)
  
- <https://changelog.com/gotime/6> (Mechanical Sympathy with Bill Kennedy)
- <https://fragmentedpodcast.com/episodes/214/> (3 Things Every Developer Needs To Know How To Do)
- <https://fragmentedpodcast.com/episodes/41/> (YAGNI you aren't going to need it)
- <https://mbuffett.com/posts/programming-advice-younger-self>
- <https://www.youtube.com/watch?v=MksJTtt7jS4&t=93s> Presentation on Code Smells by Sandi Metz at Laracon 2016
- <https://robertheaton.com/2015/10/26/why-and-how-to-make-smaller-pull-requests/>
- <https://robertheaton.com/2014/06/20/code-review-without-your-eyes/> (Heuristics for quickly reviewing code)
- <https://two-wrongs.com/code-reviews-do-find-bugs>
- <https://www.alexandra-hill.com/2018/06/25/the-art-of-giving-and-receiving-code-reviews/>


## Languages

Even if you do not code in these languages these books can provide invaluable understanding of decisions made in "how stuff works"

- The C Programming Language (2nd Edition) by Brian Kernighan and Dennis Ritchie
- Effective Java Programming Language Guide by Joshua Bloch
- The Go Programming Language by Alan Donovan and Brian Kernighan

## Key Ideas

- <https://www.se-radio.net/2015/05/the-cap-theorem-then-and-now>
- <https://www.se-radio.net/2015/04/episode-224-sven-johann-and-eberhard-wolff-on-technical-debt> 
- <https://engineering.linkedin.com/distributed-systems/log-what-every-software-engineer-should-know-about-real-time-datas-unifying> Logging
- <https://increment.com/documentation/>
- <https://se-radio.net/2024/02/se-radio-604-karl-wiegers-and-candase-hokanson-on-software-requirements-essentials/>


## Doing it well

### Quality and Testing

Why what we do is important...

- <https://medium.com/dataseries/the-rise-and-fall-of-knight-capital-buy-high-sell-low-rinse-and-repeat-ae17fae780f6>
- <https://www.bbc.co.uk/programmes/w3csz4dn> (13 minutes to the moon episode 5: the 4th astronaut - the first mission critical software)
- <https://timharford.com/2019/11/cautionary-tales-ep-3-lala-land-galileos-warning/> (quality "theater")

How to do it well...

- Testing Computer Software, 2nd Edition by Cem Kaner, Jack Falk, Hung Q. Nguyen
- <https://programmingisterrible.com/post/173883533613/code-to-debug>
- <https://www.se-radio.net/2017/01/se-radio-episode-280-gerald-weinberg-on-bugs-errors-and-software-quality>
  
- <https://rbcs-us.com/documents/Why-Most-Unit-Testing-is-Waste.pdf>
- <https://news.ycombinator.com/item?id=15565875> (Write tests. Not too many. Mostly integration)
- <https://news.ycombinator.com/item?id=18466787> List of strings to use in QA testing

- <https://news.ycombinator.com/item?id=11416746> Crowd sourcing how to review code
- <https://www.bluematador.com/blog/delight-customers-this-black-friday-7-surefire-strategies-to-prevent-downtime>
- <https://queue.acm.org/detail.cfm?id=3197520> (Always be automating, Thomas Limoncelli)
- <https://queue.acm.org/detail.cfm?id=2945077> (Small batches principle, Thomas Limoncelli)
- <https://fragmentedpodcast.com/episodes/183/> (The Testing Paradox)
- <https://martinfowler.com/articles/developer-effectiveness.html>
- <https://www.se-radio.net/2010/09/episode-167-the-history-of-junit-and-the-future-of-testing-with-kent-beck>


### Infrastructure

- Release It!: Design and Deploy Production-Ready Software by Michael Nygard
- <https://www.se-radio.net/2009/05/episode-134-release-it-with-michael-nygard/>
- <https://www.se-radio.net/2015/02/episode-221-jez-humble-on-continuous-delivery>
- <https://changelog.com/gotime/142> (All about that infrastructure and DevOps)
- <https://www.se-radio.net/2016/01/se-radio-show-246-john-wilkes-on-borg-and-kubernetes>
- <https://www.se-radio.net/2020/04/episode-405-yevgeniy-brikman-on-infrastructure-as-code-best-practices/>
- <https://softwareengineeringdaily.com/2020/12/30/cloud-native-applications-with-cornelia-davis-repeat/>

# Algorithms and Architecture

## Algorithms

- The Algorithm Design Manual, 2nd Edition by Steven Skiena
- Design Patterns: Elements of Reusable Object-Oriented Software by Erich Gamma, Ralph Johnson, John Vlissides, Richard Helm
- <https://www.se-radio.net/2014/11/episode-215-gang-of-four-20-years-later> Gang of Four Architecture Patterns

- <https://github.com/joelparkerhenderson/queueing_theory> (summary and links to resources)
- <https://www.se-radio.net/2019/02/se-radio-episode-358-probabilistic-data-structure-for-big-data-problems/>
- <https://queue.acm.org/detail.cfm?id=3104030> (Data Sketching summary)


### Software Architecture

- <https://web.archive.org/web/20210414115314/http://www.laputan.org/mud/> Foundational Essay on architectures and the infamous "Ball of Mud"
- <https://docs.microsoft.com/en-us/archive/msdn-magazine/2009/february/best-practice-an-introduction-to-domain-driven-design>
- <https://www.se-radio.net/2015/05/se-radio-episode-226-eric-evans-on-domain-driven-design-at-10-years>
- <https://www.codingblocks.net/podcast/clean-code-programming-around-boundaries>
- <https://virtualddd.com/sessions/ddddd-20-bounded-contexts-microservices-and-everything-in-between/>

- <https://www.se-radio.net/2017/04/se-radio-episode-287-success-skills-for-architects-with-neil-ford>
- <https://se-radio.net/2024/05/se-radio-616-ori-saporta-on-the-role-of-the-software-architect/>
- <https://www.theartifact.io/videos/ep-4-on-becoming-a-software-architect-with-lee-atchison/>

- <https://www.se-radio.net/2020/05/episode-409-joe-kutner-on-the-twelve-factor-app/>
- - <https://brandur.org/heroku-values>

- <https://www.se-radio.net/2018/03/se-radio-episode-320-nate-taggart-on-serverless-paradigm>
- <https://martinfowler.com/articles/serverless.html#drawbacks> Drawbacks of Serverless
 
- <https://www.se-radio.net/2021/02/episode-447-michael-perry-on-immutable-architecture/>
- <https://virtualddd.com/sessions/orchestration-and-choreography-with-laila-bougria-udi-dahan/>

#### Microservices

- <https://www.se-radio.net/2022/08/episode-525-randy-shoup-on-evolving-architecture-and-organization-at-ebay/>
- Building Microservices by Sam Newman
- <http://www.elidedbranches.com/2016/08/microservices-real-architectural.html> (Camille Fournier) 
- <https://alibaba-cloud.medium.com/conways-law-a-theoretical-basis-for-the-microservice-architecture-c666f7fcc66a>
- <https://news.ycombinator.com/item?id=13960107> (modules vs microservices)
- <https://changelog.com/gotime/126> Go time: monolith vs microservices

#### Architectural Scalability

- <https://highscalability.com/blog/2014/2/26/the-whatsapp-architecture-facebook-bought-for-19-billion.html>
- <https://highscalability.com/blog/2014/3/31/how-whatsapp-grew-to-nearly-500-million-users-11000-cores-an.html>
- <https://highscalability.com/blog/2010/3/16/justintvs-live-video-broadcasting-architecture.html>
- <https://news.ycombinator.com/item?id=18760350> A simple guide to scaling to 10M users *(with commentary from HackerNews)*


## Distributed Systems

- <https://www.se-radio.net/2021/07/episode-470-l-peter-deutsch-on-the-fallacies-of-distributed-computing/>
- <https://www.codingblocks.net/podcast/transactions-in-distributed-systems/>
- <https://www.se-radio.net/2015/11/se-radio-episode-241-kyle-kingsbury-on-consensus-in-distributed-systems>
- <https://www.se-radio.net/2017/02/se-radio-episode-282-donny-nadolny-on-debugging-distributed-systems>
- <https://www.se-radio.net/2017/03/se-radio-episode-285-james-cowling-on-dropboxs-distributed-storage-system>
- <https://www.se-radio.net/2010/03/episode-157-hadoop-with-philip-zeyliger>
- <https://softwareengineeringdaily.com/2020/02/18/go-networking-with-sneha-inguva/>
- <https://blog.golang.org/waza-talk> Concurrency is not parallelism by Rob Pike at Waza 2013
- <https://www.cs.cmu.edu/~crary/819-f09/Hoare78.pdf> (Tony Hoare on Communicating Sequential Processes)

### PAXOS

- <https://bwlampson.site/Slides/PaxosABCDAbstract.htm>
- <https://research.microsoft.com/en-us/um/people/lamport/pubs/lamport-paxos.pdf> (Leslie Lamport on Paxos)
- <https://research.microsoft.com/en-us/um/people/lamport/pubs/paxos-simple.pdf> (Leslie Lamport on Paxos Simplified)
- - <https://www.microsoft.com/en-us/research/uploads/prod/2016/12/paxos-simple-Copy.pdf>

# Security

- Applied Cryptography by Bruce Schneier
- The Tangled Web: A Guide to Securing Modern Web Applications by Michal Zalewski
- <https://darknetdiaries.com/episode/52/> (Magecart: credit card skimming and websites)
- <https://www.wired.com/story/confessions-marcus-hutchins-hacker-who-saved-the-internet/>

# History

- <https://spectrum.ieee.org/tech-history/silicon-revolution/hans-peter-luhn-and-the-birth-of-the-hashing-algorithm>
- <https://segment.com/blog/a-brief-history-of-the-uuid/>
- Racing the Beam by Nick Montfort and Ian Bogost
- <https://www.bbc.co.uk/programmes/m000ncmw> Alan Turing
- <https://guykawasaki.com/steve-wozniak/> Apple hardware wizard
- <https://urchin.biz> (pre-history of google analytics)
- <https://www.cake.co/conversations/VXHSjBG/the-untold-origin-story-of-ebay-that-i-lived-and-the-times-that-could-have-killed-it>
- <https://queue.acm.org/detail.cfm?id=1142065> (Werner Vogels about AWS 2006)
- <https://www.se-radio.net/2015/07/episode-232-mark-nottingham-on-http2/>
- <https://http2-explained.haxx.se/en/part2>

## Artificial Intelligence
- <https://www.wired.com/story/eight-google-employees-invented-modern-ai-transformers-paper/>
- <https://www.acquired.fm/episodes/nvidia-the-dawn-of-the-ai-era>
- <https://lexfridman.com/gustav-soderstrom/> (AI in spotify music)

# Career

- <https://www.se-radio.net/2022/06/episode-515-swizec-teller-on-becoming-a-senior-engineer/>
- <https://rutar.org/writing/how-to-build-a-personal-webpage-from-scratch/> Create yourself a blog ("web log")
- <https://danluu.com>
- <https://danluu.com/sounds-easy/> ("I could build that in a weekend")
 <https://charity.wtf>


# Interesting Ideas

- <https://changelog.com/gotime/132> (The trouble with databases)

- <https://www.se-radio.net/2010/11/episode-169-memory-grid-architecture-with-nati-shalom>
- <https://lexfridman.com/david-patterson/> RISC (reduced instruction set computer)
- <https://blog.devtrovert.com/p/go-get-go-mod-tidy-commands>

- <https://podcasts.apple.com/us/podcast/techmeme-ride-home/id1355212895> (daily tech news)


## Game Theory
- <https://www.bbc.co.uk/programmes/b01h75xp> In our time: game theory
- <https://ncase.me/trust/> (interactive game theory for prisoner's dilemma)
- <https://www.wnycstudios.org/podcasts/radiolab/segments/golden-rule> (game theory in practice)


## Papers and Articles of Huge Ideas

- <http://www.essrl.wustl.edu/~jao/itrg/shannon.pdf> (Claude Shannon on Communication)

- <https://research.microsoft.com/en-us/um/people/lamport/pubs/time-clocks.pdf> (Leslie Lamport on Time)

- <https://bwlampson.site/33-Hints/WebPage.html> (Butler Lampson on Hints for Computer System Design 1983)
- - <https://news.microsoft.com/stories/people/butler-lampson.html>
- <https://bwlampson.site/10-SPEGuestEditorial/WebPage.html> (1972: "Almost everyone who uses a pencil will use a computer")

- <https://cacm.acm.org/magazines/2009/10/42360-retrospective-an-axiomatic-basis-for-computer-programming/fulltext> (C.A.R. Hoare on formal verification)

- <https://www.usenix.org/system/files/nsdi20-paper-agache.pdf> AWS Lambdas are powered by Firecracker OS
- - <https://blog.acolyer.org/2020/03/02/firecracker/>

