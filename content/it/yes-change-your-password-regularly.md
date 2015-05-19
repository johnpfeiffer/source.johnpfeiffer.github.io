Title: Yes, Change your Password regularly
Date: 2011-12-27 17:10
Tags: security, password

[TOC]

### Security is risk management

The hundreds of articles about "changing passwords doesn't improve security" are just hype/noise without context.

There is an absolute spectrum of password management that creates untenable risk (no password or simply the word "password") all the way to very low risk (100 random characters of every category changed every day) but at an unbearable overhead.

While "changing the highly complex password every 90 days" is considered inefficient and draconian...

### What about at least changing the password once a year?

While it's likely that an external attacker or disgruntled employee will use a compromised password immediately, it doesn't mean there isn't a good reason to choose a frequency of password change:

> If a sticky note attached to a laptop sold at a garage sale is still valid for the company's online bank account then you're in trouble.

Reduce the risk, have a policy to manage that window of access to something you're comfortable with.

### Dependency Visibility

The opportunity to improve your infrastructure is well worth the cost of finding every hard coded place that a password is embedded in your organization:

- The password was just changed
- You quickly find something is not working
- You either change the password back or refactor/reorganized and break the dependency

**Far better than:**
- a random event like a forgotten password reset by one individual in the organization
- creates a mystery problem in mission critical systems for everyone else to track down


### But I use a password management tool!

Password management tools have to store their passwords somewhere (hopefully encrypted).  

Over time there is a chance that a "bad actor" will end up with your local password store.

Man in the middle attacks (NSA anyone?) can snatch credentials from secure channels.

There is an even higher likelihood that the remote services you are using will be compromised (database or password hashes leak).

Given time hackers can use rainbow tables and GPU based brute force attacks they will crack your password.

**Every time you change your password you reset the clock on every type of attack**
