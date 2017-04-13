Title: Golang Concurrency Goroutines and Channels
Date: 2017-04-12 22:54
Tags: go, golang, goroutines, concurrency, channels, select, pipelines

[TOC]

If there is a killer feature to Go it is the focus on concurrency.  This article captures some of the basics and I hope to someday write a follow-up article on more advanced topics.

> "Go is a compiled, concurrent, garbage-collected, statically typed language"

- <https://talks.golang.org/2012/splash.article>

Distributed systems and large data sizes mean developers are forced to think in parallelism, or are they?

Using Go channels (based upon Communicating Sequential Processes <https://en.wikipedia.org/wiki/Communicating_sequential_processes>, <http://www.cs.cmu.edu/~crary/819-f09/Hoare78.pdf>) developers can write code that feels very imperative and sequential, but designed in such a way that parallelism comes easily.

- <https://golang.org/doc/effective_go.html#concurrency>
- <https://blog.golang.org/concurrency-is-not-parallelism>

## Go and Goroutines

A goroutine is a "lightweight thread" that allows for a far higher amount of concurrency than just depending on OS processes or even traditional threading (and much simpler than attempting to explicitly organize around a defined number of processors or threads).

In a very meta sense every Go program uses concurrency because the main function itself is an implicit goroutine (and will not wait or might block forever ;)

    :::go
    package main
    
    import (
        "fmt"
        "time"
    )
    
    func example() {
        time.Sleep(1 * time.Second)
        fmt.Println("example")
    }
    
    func main() {
        go example()
        fmt.Println("done")
    }
> This will exit without printing "example" because using the "go" keyword runs the example function in a new goroutine

- <https://play.golang.org/p/h6_B0whHxE>
- <https://golang.org/pkg/testing/#hdr-Main>
- <http://devs.cloudimmunity.com/gotchas-and-common-mistakes-in-go-golang/>
- <https://en.wikipedia.org/wiki/Green_threads>

> There is no explicit external management of a goroutine once it has started, terminating a goroutine is implemented via an exception or exit in the code that the goroutine is running, usually signalled via a channel

Since Goroutines are cooperative they are not pre-empt-able...

- <https://dave.cheney.net/2016/12/22/never-start-a-goroutine-without-knowing-how-it-will-stop>
- <https://en.wikipedia.org/wiki/Preemption_(computing)>
- <https://github.com/golang/go/issues/10958>

## Sync with a WaitGroup

The most straightforward way to fix the previous trivial example is to specify in advance that the implicit main goroutine should wait before continuing...

    :::go
    package main
    
    import (
        "fmt"
        "sync"
        "time"
    )
    
    func example() {
        time.Sleep(1 * time.Second)
        fmt.Println("example")
    }
    
    func main() {
        var wg sync.WaitGroup
        wg.Add(1)
        go func() {
            example()
            wg.Done()
        }()
        wg.Wait()
        fmt.Println("done")
    }
> 1. The example function remains unchanged
> 2. The waitgroup will expect one call of "Done"
> 3. The go keyword now calls an anonymous function that calls wg.Done() (accessed using closure) after example()
> 4. The waitgroup.Wait() blocks until the correct number of Done() calls have been made
> 5. The example function sleep and print finally finish
> 6. The waitgroup unblocks and the main goroutine can finally print "done" and exit

- <https://play.golang.org/p/p0jDoiGBT4>
- <https://golang.org/pkg/sync/#example_WaitGroup>

## Channels

Channels are the recommended way of communicating when using goroutines (and sharing resources).
> <- the arrow always points to the left

    :::go
    package main
    
    import (
        "fmt"
        "time"
    )
    
    func main() {
        c := make(chan int)
        go func() {
            fmt.Println("sleeping...")
            time.Sleep(1 * time.Second)
            c <- 42
            close(c)  // IF NOT CLOSED THEN DEADLOCK
            // c <- 2  DO NOT SEND TO A CLOSED CHANNEL, IT WILL PANIC
        }()
        fmt.Println("anonymous function, a channel passed a value via closure", <-c)
        v, ok := <-c
        fmt.Println(v, ok)
    }
> - since a channel is a reference type "make" is used and the <- sends a value to the channel, later <- is used to receive a value
> - a closed channel cannot be written to further and will PANIC "send on a closed channel"
> - if you forget to close a channel, later reading from an open unbuffered channel which does not have data will exit "fatal error: all goroutines are asleep - deadlock!"
> - an "unbuffered" channel "blocks" until both the sender and receiver are ready
> - the Println function reads from the channel, in this case the channel acts as a synchronization tool that blocks at the Print statement and prevents the main goroutine from exiting
> - The final printed output will be: "0 false", since the channel is closed and empty subsequent receives will return a the empty value "zero" and the state of the channel (in this case "false")

- <https://play.golang.org/p/RR0PWmAeKa>
- <https://gobyexample.com/channels>
- <https://dave.cheney.net/2013/04/30/curious-channels>

### Buffered channels and returning a value

A common problem is one part of the application running faster than another part and one way to "unblock" the fast part is to use a buffer to create a queue for the slower part to catch up.
This kind of issue occurs in a "pipeline" of producers/consumers (also known as sources/sinks)...

    :::go
    package main
    
    import (
    	"fmt"
    	"log"
    	"sync"
    	"time"
    )
    
    func slowReceiver(c <-chan int, wg *sync.WaitGroup) {
    	for {
    		n := <-c
    		fmt.Println("received", n)
    		time.Sleep(time.Second)
    		// c <- 42 // THIS WOULD CAUSE AN ERROR "(send to receive-only type <-chan int)"
    		wg.Done()
    	}
    }
    
    func fastSender(c chan<- int, wg *sync.WaitGroup) {
    	for i := 0; i < 5; i++ {
    		c <- i
    		wg.Add(1)
    		fmt.Println(i)
    		// fmt.Println(<-c) // THIS WOULD CAUSE AN ERROR "(receive from send-only type chan<- int)"
    	}
    }
    
    func main() {
    	start := time.Now()
    	var wg sync.WaitGroup
    	c := make(chan int, 3)
    	go slowReceiver(c, &wg)
    	fastSender(c, &wg)
    	wg.Wait()
    	log.Println(time.Since(start))
    }

> - This example shows how to specify a channel of type that either only sends or only receives
> - log works the same as fmt and Since() a very convenient way to output elapsed time
> - Without the waitgroup Wait() main would exit after 1 second with only "received 1" and never reach "received 4" (5 seconds)

- <https://blog.golang.org/pipelines>
- <https://play.golang.org/p/NcEOgCiSQs>
- <https://tour.golang.org/concurrency/3>


### Using Select to not block a channel

Channels are most useful when they can block asynchronously until an event occurs.

    package main
    
    import "time"
    import "fmt"
    
    func main() {
    	c := make(chan string)
    	q := make(chan bool)
    	go myDelayedQuit(q)
    	go mySleep(c, 1)
    
    	fmt.Println("begin non blocking wait...")
    	for {
    		select {
    		case msg := <-c:
    			fmt.Println("received:", msg)
    		case <-q:
    			fmt.Println("done")
    			return
    		}
    	}
    }
    
    func mySleep(a chan string, n int) {
    	time.Sleep(time.Second * time.Duration(n))
    	a <- "woke up"
    }
    
    func myDelayedQuit(b chan bool) {
    	time.Sleep(time.Second * 2)
    	b <- true
    }
> - **for** loops forever until the return statement
> - **select** will wait and whenever a case can be filled it will unblock
> - after 1 second the sleep function is done and sends the "woke up" message
> - after 2 seconds the true boolean is sent and main finishes

- <https://play.golang.org/p/JBrhHZVq6a>


### Real Example of Concurrency in a LAN Scanner

A real world example is discovering all of the hosts listening on a given port in local area network (subnet).

In a serial example waiting 2 seconds for each host to respond would mean waiting 512 seconds in a "normal" /24 subnet of ~256 hosts (ignoring the .255 broadcast and .0)

    :::go
	found := make(chan IPCheckResult, max)
	var wg sync.WaitGroup
	wg.Add(max)
	for _, a := range addresses {
		fmt.Println("checking", a)
		// https://golang.org/doc/faq#closures_and_goroutines
		go func(ip string) {
			checkIP(ip, *port, found)
			wg.Done()
		}(a)
	}
	wg.Wait()
	close(found)

> Here the channel is simply used as a "lock free" place to aggregate all of the results of the goroutines, sync occurs via the waitgroup which will wait until every pre-added item is decremented by a Done(), there is definitely a possibility for an off-by-one gotcha that will hang your program!

<https://bitbucket.org/johnpfeiffer/go-lanscan/src>

### Troubleshooting Race Conditions

A common gotcha is that in Go maps are not safe for concurrent use:

- <https://blog.golang.org/go-maps-in-action>
- <https://golang.org/doc/faq#atomic_maps>

In this example of a simple in memory cache the expiration was implemented...

    :::go
    func (memory MemoryCache) Set(key string, value string, expiresSeconds int) {
        memory.m[key] = value
        timer := time.NewTimer(time.Duration(expiresSeconds) * time.Second)
        go func() {
            <-timer.C
            memory.Delete(key)
            // log.Println("Timer triggered cache expiration for", key)
        }()
    }
> The error here is that the goroutine that wakes up to "expire" and remove a key/value pair from the map may contend with any other later operation (i.e. Get, Set, Delete) that is also modifying the map

- <https://bitbucket.org/johnpfeiffer/go-cache/src>

A really helpful tool is to run `go test -race` , it may take a little bit but "WARNING: DATA RACE" is pretty clear.

- <https://blog.golang.org/race-detector>

### More random thoughts on concurrency and control

Controlling goroutines is like controlling threads or even any other control flow.

Iterative vs Recursive calculation of factorial means either predetermined count of iterations or an indeterminate count (recursion) with a (base case) signal for termination (often called a sentinel value).

So either the External Controller knows when to stop or each actor checks if it is time to stop.

#### An important consideration to termination is cleanup

If the actor is responsible for self cleanup (as it knows what resources it is using) this can lead to resource leaks if the actor terminates unexpectedly without cleaning up.

If using "dependency injection" then the Controller has knowledge of what resources were shared with the agents and can do cleanup, even if actors terminate unexpectedly.

An increasingly common approach is for the Framework to facilitate cleanup so that the complexity is removed from both the Controller and the actors (e.g. Garbage Collection or Go deferred)

#### Poison Jobs cons and pros

One challenge with workers and a queue is the "poison job" which may create inefficiency or halt the system entirely as each worker who takes the job blocks/loops forever or terminates unexpectedly.

One possible solution is to have a retry count so that any job which has timed out or failed and retried repeatedly is moved to a FailedJob queue (for future manual inspection and debugging) or logged and dropped entirely.

Interestingly something like a "poison job" is actually a useful way to signal to concurrent actors to have an orderly termination even if they have not completed their jobs (i.e. a full system shutdown has been initiated and we want to trigger self cleanup).

#### Patterns for Channels and Flow Control

Go Channels represent a way to map out the dependencies and then allow the compiler to optimize for parallelization.

Waiting indefinitely for all goroutines to return is naive, and any termination signal must have the ability to truly interrupt work in progress, which it does NOT for goroutines, so any call that a goroutine is making MUST have a timebound where it can check for the termination signal.

Therefore write your goroutines carefully knowing that you cannot cancel/aka force them to return from an infinite loop/long call, unless you exit main entirely.

This means that for architecture decisions it is important to consider small separate services/applications that can provide resource usage transparency and termination control.  While this is becomes a tradeoff with coordination/orchestration complexity it is worth having modularity and clear boundaries in any application of decent complexity.

- Simple and deterministic: fan out with predefined count, close the channel
- Provide timeouts and retries: a failure can occur anywhere and graceful degradation means setting limits and dealing with ephemeral errors
- Use the select statement for a non-blocking way to check for early application termination events
- Use buffers to even out spikes in work from sources/production

