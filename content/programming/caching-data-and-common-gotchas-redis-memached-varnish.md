Title: Caching data and common gotchas and an intro to redis memcached and varnish
Date: 2015-03-26 00:00
Tags: cache, caching, redis, memcached, varnish

[TOC]

**Caching is when you use a copy of a data set rather than using the source.**

Caching often involves a "Key Value Lookup":

1. A request is received and the service checks the cache using a Key
1. The cache does not contain the Key
1. The service generates the result from the originating data source (i.e. database)
1. The service then stores the result in the cache with the Key as the index (and the result as the Value)
1. A request is received and the service checks the cache using a Key
1. The cache **does** contain the Key
1. The service retrieves the Value from the cache and returns the result

A more concrete example would be to cache a User object by Email, so that whenever a request came in for a particular Users details the cache would contain their Name, Address, and Phone Number.

<https://en.wikipedia.org/wiki/Associative_array>


## Why Cache?

A tradeoff of memory for cpu (or latency or some other business cost).

- accessing the data from source is too slow
- the data actually comes from multiple sources (complex and expensive to retrieve)
- to reduce load on the service originating data
- to reduce contention (i.e. reads and writes)
- for a client-server architecture, caching on the client reduces the number of required connections to a server
- server side caching can protect backend resources and improve throughput and performance
- comp


### Questions to ask when caching

Is the complexity of caching worth the performance gain? (simpler is often better)

Does my cache need to be consistent? (meaning the cache and data source return identical results)

Can my cache be "eventually consistent"? (meaning a wrong answer for some specified period of time is ok)

Am I caching at a high level? (meaning aggregating a lot of work/responses from lower level systems)

Am I caching at a low level? (meaning inside of my Data Access Object pattern I'm protecting a single simple resource, i.e. a MySQL table, from being accessed too often)

How unique are my Keys in my cache (i.e. if multiple users can have the same identifier it would be very bad to return the wrong session to the wrong user)


## How to Cache

### Cache on Write

Also known as "cache on write through"

Whenever new data is written a cache must also be updated.


### Cache on Read

Also known as "cache on read through"

Whenever a query is made first the cache is checked.  If there is a "cache miss" then the data source is queried and the cache is updated and the result is returned.  If there is a "cache hit" and the data is in the cache then it is returned (and potentially a cache key expiration updated as this cache hit improved the cache efficiency).


## Common Gotchas

Caching is challenging because of the need for data consistency, parallel requests, and race conditions.

One good way to think about it is a banking system with money: if two people both try and empty an account at an ATM at the same time how will your caching system handle it?


### Cache on write gotchas

One implementation flaw is to update the cache first; if the update to the data source fails then some requests may have been given incorrect data.

Another flaw would be to not have a "transaction" defined around both the update of the data and then the update of the cache since if either fails future requests will receive inconsistent results.

There may be a design mismatch as since data is only cached on write, if reads are occurring mostly on data written a long time ago they will be expired/pushed out and you will have poor cache efficiency.

While "cache on write" is a sometimes band-aid for NoSQL "eventual consistency" when it fails (i.e. all applications should expect that a cache will not exist or have a cache miss) the result may be data inconsistency.

One workaround is "check and set" (or "compare and set") where the cache will auto-invalidate if two conflicting entries are attempted.

<http://neopythonic.blogspot.com/2011/08/compare-and-set-in-memcache.html>


### Expiration: cache full of stale junk

A naive implementation of caching will store every result in the cache forever.  

While this seems like a good idea ("The cache application/service will just evict unused items based some algorithm") it is essentially forcing your cache to be full of potentially low value information on the hope that someone else will solve the problem.

Since some caching tools/framework do not set a default **Time To Live** or **Expiration** and in that case all of your data may quickly fill up the cache (not a bad thing per se), but then it will use whatever default or global "eviction policy" that is defined.

Applying business logic and empirical data to pick sane expiration values might not only improve cache performance but may protect your service from security issues or bugs due to serving really stale data.

> e.g. for security reasons, **caching a session "forever" is a bad idea** as an attacker may get access to an old client cache or token and be able to impersonate a legimate user

Set a TTL or Expiration whenever possible that matches your domain (i.e. for a session 1 day or 1 week).

If the Time to Live is too short then the cache may have very poor efficiency (items expire before they can generate even one cache hit)


### Cold Cache and the Thundering Herd
1. If the cache is "cold", i.e. has not been populated, then all queries will go directly to the source
1. If the source is not prepared for the "thundering herd" of requests (that were usually handled by the cache) then the source may become overloaded and bad things will happen
1. It is therefore best practice to "warm the cache" by seeding data from the source into the cache before significant load events



## Tools for caching
Much like encryption it is probably a good idea to use a time tested product over writing your own implementation.

### Redis Examples

- <http://redis.io/commands>

#### Interactive Redis Prompt

    redis-cli
    keys *

#### Non Interactive Redis Commands

    redis-cli KEYS *:*
    redis-cli KEYS session:1:*
    redis-cli hgetall session:1:web
    redis-cli hgetall session:1:web:presence
     
    redis-cli KEYS "session:3:*" | xargs redis-cli DEL   # then upgrade --restart
     
    redis-cli KEYS session:1:*  | grep session:1:web-48    # user_session.py , when the hardcoded max of 10 simultaneous sessions is hit no more can be created
      session:1:web-48679:rooms
      session:1:web-48679:presence
      session:1:web-48679:message_ids
      session:1:web-48679
     
    redis-cli zrange sessions:1 0 9
      1) "1:web"
      2) "1:web-48679"
     
    # remove a session manually?
    redis-cli zrem sessions:1 1:web-48679
    redis-cli del   session:1:web-48679:rooms
    redis-cli del   session:1:web-48679:presence
    redis-cli del   session:1:web-48679:message_ids
    redis-cli del   session:1:web-48679
    
- - - - - - - - - - - - - - - - - - - - - - - - -
### Installing Redis

- <http://redis.io/topics/quickstart>
- <http://packages.ubuntu.com/trusty/redis-server> (sudo apt-get install redis-server)

    redis-cli -h example.com ping
> PONG , aka verify a remote server connectivity

#### Redis Clients
<http://redis.io/clients#python>

    pip install redis

<https://pypi.python.org/pypi/redis>

    import redis
    r = redis.StrictRedis(host='localhost', port=6379)
    r.flushall()


### Memcached
- <http://memcached.org>
- <https://en.wikipedia.org/wiki/Memcached>

### Varnish
- <https://www.varnish-cache.org/about> REST web caching
