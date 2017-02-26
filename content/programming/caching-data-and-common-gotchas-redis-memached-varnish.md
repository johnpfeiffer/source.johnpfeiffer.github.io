Title: Caching data and common gotchas and an intro to redis memcached and varnish
Date: 2015-03-26 00:00
Tags: cache, caching, redis, memcached, varnish

[TOC]

**Caching is when you use a copy of a data set rather than using the original source.**

Caching often involves a "Key Value Lookup":

1. A request is received and the service checks the cache using a Key
1. The cache does not contain the Key
1. The service generates the result from the originating data source (i.e. database)
1. The service then stores the result in the cache with the Key as the index (and the result as the Value)
1. A subsequent request is received and the service checks (looks up) the cache using a Key
1. The cache **does** contain the Key
1. The service retrieves the Value from the cache and returns the result

A more concrete example would be to cache a User object by Email, so that whenever a request came in for a particular Users details the cache would contain their Name, Address, and Phone Number.

<https://en.wikipedia.org/wiki/Associative_array>


## Why Cache?

A tradeoff of memory for cpu (or latency or some other business cost).

- computation is expensive (in terms of cpu, time, or money)
- accessing the data from source is too slow
- the data actually comes from multiple sources (complex and expensive to retrieve)
- to reduce load on the service originating data
- to reduce contention (i.e. reads not served from the same persistence that does writes)
- server side caching can protect backend resources and improve throughput and performance
- for a client-server architecture, caching on the client reduces the number of required connections to a server


### Questions to ask when caching

- Is the complexity of caching worth the performance gain? (a simpler implementation is often better, less chance of bugs!)
- Does my cache need to be consistent? (meaning the cache and data source return identical results)
- Can my cache be "eventually consistent"? (meaning a wrong answer for some specified period of time is ok)
- Am I caching at a high level? (meaning aggregating a lot of work/responses from lower level systems)
- Am I caching at a low level? (meaning inside of my Data Access Object pattern I'm protecting a single simple resource, i.e. a MySQL table, from being accessed too often)
- How unique are my Keys in my cache (i.e. if multiple users can have the same identifier it would be very bad to return the wrong session to the wrong user)
- Do I have the ability to operate or pay for a caching service?
- What will happen if the cache is unavailable?

### Cache Latency Times in Perspective

Taking "why cache" to another level, the relative speeds of different cache levels highlight why some applications or algorithms will fail if they do not leverage cache.

- If your application uses a very large amount of data the network may actually be better than disk; optimization would probably not be focused on "loop unrolling"
- If your application depends on data across the internet then network caching, routing algorithms, and data modeling (eventual consistency!) may be more important than "tail recursion vs iterative"


|Action|nanoseconds|microseconds|milliseconds|human scale comparison|
|:-:|:-:|:-:|:-:|:-:|
|A typical cpu instruction | 1 ns | | | 1 second basis (approximations) |
|L1 cache fetch | 0.5 ns | | | |
| Branch misprediction | 4 ns | | | |
| L2 cache fetch | 7 ns | | | 7 seconds |
| Mutex lock/unlock | 25 ns | | | |
| RAM "main memory" fetch | 100 ns | 0.1 us | | 2 minutes |
| Read 4K randomly from SSD | 100,000 ns | 100 us | | 28 hours |
| Read 1 MB sequentially from memory | 250,000 ns | 250 us | | 3 days |
| Send 1000 bytes over 1 Gbps network | 500,000 ns | 500 us | 0.5 ms | 6 days |
| Read 1 MB sequentially from SSD | 1,000,000 ns | 1,000 us | 1 ms | 12 days |
| Spinning Hard Disk seek | 8,000,000 ns | 8,000 us | 8 ms | 3 months |
| Read 1 MB sequentially from disk | 20,000,000 ns | 20,000 us | 20 ms | 7.6 months |
| Packet Roundtrip SF to NY | 70,000,000 ns | 70,000 us | 70 ms | 2 years |
| Packet Roundtrip SF to NY | 150,000,000 ns | 150,000 us | 150 ms | 5 years |


> The L1 cache is the memory cache integrated into the CPU that is closest

> Light travels 30 cm or about 1 foot in 1 nanosecond

> ns = nanoseconds, us = microseconds, ms = milliseconds

- <http://norvig.com/21-days.html#answers> (Peter Norvig) 
- <https://en.wikipedia.org/wiki/CPU_cache>
- <https://en.wikipedia.org/wiki/Solid-state_drive#Controller>
- <http://www.codingblocks.net/podcast/episode-45-caching-overview-and-hardware/>
- <https://wondernetwork.com/pings>
- <https://twitter.com/rzezeski/status/398306728263315456/photo/1> (Brendan Gregg)


### Caches are another Operational component with Overhead

The best advice is to definitely avoiding caching until the last possible moment (*"less is the best" and "premature optimization" and "be future flexible" and "defer architecture decisions"*)

Not only do you have to write code complexity for using a cache, there's the nitty gritty of running a cache (which can be a completely different expertise than programming)

- Install
- Deployment
- Upgrades
- Security
- Monitoring
- Metrics
- Testing (i.e. synthetic smoke tests or load)

None of this operational cost is free, and there are plenty of issues when just implementing caching in code...


## How to Cache

### Cache on Write

Also known as "cache on write through"

Whenever new data is written a cache must also be updated.


### Cache on Read

Also known as "cache on read through"

Whenever a query is made first the cache is checked.

- If there is a "cache miss" then the data source is queried and the cache is updated and the result is returned.  
- If there is a "cache hit" and the data is in the cache then it is returned (and potentially a cache key expiration updated as this cache hit improved the cache efficiency).

### Cache Warming

Pre-emptively adding data to the cache is "cache warming" in order to improve "cache hit" percentages and reduce the risk of "cold cache" issues.

### Flush the Cache

Removing some or all data from the cache in order to invalidate a chunk of data (i.e. all users need to reset their passwords) or pre-emptively free up memory/space.


## Common Gotchas

Caching is challenging because of the need for data consistency, parallel requests, and race conditions.

One good way to think about it is a banking system with money...
> If two people both try to empty a bank account at an ATM at the same time how will your caching system handle it?


### Cache on write gotchas

One implementation flaw is to update the cache first; if the update to the data source fails then some requests may have been given incorrect data.

Another flaw would be to not have a "transaction" defined around both the update of the data and then the update of the cache since if either fails future requests will receive inconsistent results.

There may be a design mismatch as since data is only cached on write, if reads are occurring mostly on data written a long time ago they will be expired/pushed out and you will have poor cache efficiency.

While "cache on write" is a sometimes band-aid for NoSQL "eventual consistency" when it fails (i.e. all applications should expect that a cache will not exist or have a cache miss) the result may be data inconsistency.

One workaround is "check and set" (or "compare and set") where the cache will auto-invalidate if two conflicting entries are attempted.

<https://neopythonic.blogspot.com/2011/08/compare-and-set-in-memcache.html>


### Expiration: a cache full of stale junk

A naive implementation of caching will store every result in the cache forever...

While this seems like a good idea (*"The cache application/service will just evict unused items based some algorithm"*) it is essentially forcing your cache to be full of potentially low value information on the hope that someone else will solve the problem.

Since some caching tools/framework do not set a default **Time To Live** or **Expiration** and in that case all of your data may quickly fill up the cache (not a bad thing per se), but then it will use whatever default or global "eviction policy" that is defined.

Even O(1) can be broken by a pathological data set, and keeping every item seems like a good way to find an edge case (i.e. hash collisions and chaining).

Applying business logic and empirical data to pick sane expiration values might not only improve cache performance but may protect your service from security issues or bugs due to serving really stale data.

> e.g. for security reasons, **caching a session "forever" is a bad idea** as an attacker may get access to an old client cache or token and be able to impersonate a legimate user

Issues with Expiration Set Too Long:

- Security concerns
- Lack of control/non determinism for when and what items might be evicted
- Poor performance, memory pressure, and possibly increased operational cost
- Stale data
- Large cache sizes may end up writing to disk (i.e. redis sync to disk may use copy on write)

**Set a TTL or Expiration, whenever possible, that matches your domain** (i.e. for a session 1 day or 1 week).

> If the Time to Live is too short then the cache may have very poor efficiency (items expire before they can generate even one cache hit), meaning all of the coding and operational cost are for nothing =[


### Cold Cache and the Thundering Herd
1. If the cache is "cold", i.e. has not been populated, then all queries will go directly to the source
2. If the source is not prepared for the "thundering herd" of requests (that were usually handled by the cache) then the source may become overloaded and bad things will happen
3. It is therefore best practice to "warm the cache" by seeding data from the source into the cache before significant load events

Cold cache not only can cause problems from the source but when lot of data is written simultaneously to the cache, if the cache uses underlying disk or some other IO resource, it may temporarily overwhelm the cache (system/framework).

### Upgrading your application

In a sense the cache layer is an external persistence that has to stay in sync with the application code; they are logically and semantically bound together.

Modification to your application code, specifically the way it reads and writes to the cache, may return "bad" data.

1. Cache key "admins" stored a list of usernames of admin users for the application
2. Cache key "ausers" stored a list of usernames that begin with the letter "a"
3. An application upgrade occurs
4. Now the code has a bug that looks up "ausers" in order to give administrator permssions
5. (oops)


## Tools for caching
Much like encryption it is probably a good idea to use a time tested caching component over writing your own implementation.

A local in memory cache is a tried and true way of speeding up an application but it may not provide the transparency and visibility when there are bugs.

While it seems trivial to setup it will slow down your dev velocity on your high value focus area and every new feature you realize you need (automatic expiration, authentication, etc.) will create a distraction and eventual maintenance requirement.

Instead there are quite a few very popular battle tested options...

### Memcached
- <http://memcached.org>
- <https://en.wikipedia.org/wiki/Memcached>
- <https://hub.docker.com/r/_/memcached/>

`docker run --rm -it --publish 11211:11211 --name mymemcached memcached:alpine`

    echo -e 'add foo 0 60 11\r\nhello world\r' | nc localhost 11211
    telnet localhost 11211
    get foo
> VALUE foo 0 11
> hello world


<https://github.com/memcached/memcached/wiki/Commands>


### Redis Examples

Redis has surpassed memcached in terms of speed and functionality and if you need to store more than "just a string" you should experiment with it.

Besides having a cache to speed up lookups for your application or as a globally shared cache (be careful!) between multiple application serveers there can be a nice convenience as a "meta" persistence such that you can deploy a new version of your application and not lose all of the data in the cache.

One thing to think about is that local redis might be far more effective than remote over the network redis.

If your application can depend less shared state this is good because sharing is a nightmare for cache semantics and distributed computing.

> When possible avoid a globally shared cache between multiple processes or servers, or invest in learning about atomic operations

Regardless of securing your remote cache you will always want to measure cache effectiveness.

- <https://redis.io/commands>

### Installing Redis

The simplest way is to use Docker, <https://hub.docker.com/r/_/redis/>

`docker run --rm -it --publish 6379:6379 --name myredis redis:alpine`
`docker run -it --link myredis:redis --rm redis:alpine redis-cli -h redis -p 6379 set message hello`
`docker run -it --link myredis:redis --rm redis:alpine redis-cli -h redis -p 6379 get message`
> run an ephemeral docker container and then non-interactively use the same docker image to set and get a string key

If you prefer installing locally to your filesystem or server:

- <https://redis.io/topics/quickstart> (compiling from source)
- <https://packages.ubuntu.com/trusty/redis-server> (sudo apt-get install redis-server)

    redis-cli -h localhost:6379 ping
> PONG , aka verify a remote server connectivity

#### Interactive Redis Prompt

    redis-cli
    keys *

#### Non Interactive Redis Commands

    redis-cli KEYS *:*
> non-interactively get all of the keys that have subkeys

    redis-cli KEYS "session:3:*" | xargs redis-cli DEL
> non-interactively delete/remove all of the subkeys under the sub subkey

    redis-cli KEYS session:1:*
    redis-cli hgetall session:1:web
    redis-cli hgetall session:1:web:presence
     
    redis-cli KEYS session:1:*  | grep session:1:web-48
      session:1:web-48679:rooms
      session:1:web-48679:presence
      session:1:web-48679:message_ids
      session:1:web-48679
     
    redis-cli zrange sessions:1 0 9
      1) "1:web"
      2) "1:web-48679"
     
    redis-cli zrem sessions:1 1:web-48679
    redis-cli del   session:1:web-48679:rooms
    redis-cli del   session:1:web-48679:presence
    redis-cli del   session:1:web-48679:message_ids
    redis-cli del   session:1:web-48679


#### Redis Clients

    pip install redis
> <http://redis.io/clients#python>

    import redis
    r = redis.StrictRedis(host='localhost', port=6379)
    r.flushall()
> <https://pypi.python.org/pypi/redis>

**Go** `go get github.com/garyburd/redigo`

    :::golang
    package main
    
    import (
        "fmt"
    
        "github.com/garyburd/redigo/redis"
    )
    
    func main() {
        c, _ := redis.Dial("tcp", ":6379")
        defer c.Close()
        c.Do("SET", "message", "hi")
        s, _ := redis.String(c.Do("GET", "message"))
        fmt.Println(s)
    }

A more complete example: <https://bitbucket.org/johnpfeiffer/go-cache>

### Varnish
- <https://www.varnish-cache.org/about> REST web caching
