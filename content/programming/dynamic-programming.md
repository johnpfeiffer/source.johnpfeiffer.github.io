Title: Dynamic Programming and Memoization and the Compute versus Storage Tradeoff
Date: 2017-11-06 20:45
Tags: dynamic programming, memoization, benchmark, golang, play.golang.org, time, milliseconds

[TOC]

## Tradeoffs

There is an inevitable tradeoff of storage versus computation speed, or space used versus time to run, in every program.

Caching is often viewed as a performance optimization but sometimes it is the only way to achieve a result in a finite amount of time.

<https://en.wikipedia.org/wiki/Dynamic_programming> is about breaking down a problem into sub-problems where each solution can be stored so that it can be looked up rather than recomputed.

<https://en.wikipedia.org/wiki/Memoization> is related in that it is about storing the output of a function call when specific parameters are provided.
Thus it is often conceptualized as a special kind of caching.

## Naive Fibonacci Recursion

<https://en.wikipedia.org/wiki/Fibonacci_number> is a classic numerical series where each subsequent number is the sum of the previous two numbers: `1 1 2 3 5 8 13...` 

An interesting problem is to calculate the series up to a certain point.  The straightforward solution uses recursion:

    :::go
    package main
    
    import (
        "fmt"
    )
    
    func main() {
        fibSeries(37)
    }
    
    func fibSeries(n int) []int {
        a := make([]int, n)
        for i := 1; i <= n; i++ {
            a[i-1] = fib(i)
        }
        return a
    }
    
    func fib(x int) int {
        if x < 2 {
            return x
        }
        return fib(x-1) + fib(x-2)
    }

`go run main.go`

> Each iteration in the series discards the previous results and then re-calculates the intermediate steps for each subsequent iteration

## Fibonacci timings and golang playground time is frozen

<https://play.golang.org/p/esejwsN0lQ> is an example with timings but...
...sorry, the Go Playground does not really use time (and caches all output) so to really see the difference you must run the program locally (Andrew Gerrand explains)...

- https://groups.google.com/forum/#!topic/golang-nuts/Dh0P1VzXmq8
- https://groups.google.com/forum/#!topic/golang-nuts/NLZJahiMk58
- https://github.com/golang/playground/blob/master/sandbox/play.go
- http://www.gophercon.in/blog/2015/02/17/andrew/
- https://talks.golang.org/2014/go4gophers.slide#3

## Memoization aka Caching with Fibonacci

It almost seems common sense that we should not be re-calculating answers that we already know for every step...

    :::go
    func fibSeriesMemoization(n int) []int {
        a := make([]int, n)
        m := make(map[int]int)
        for i := 1; i <= n; i++ {
            a[i-1] = fibMemo(i, m)
        }
        return a
    }
    
    func fibMemo(x int, m map[int]int) int {
        if x < 2 {
            m[x] = x
            return x
        }
        _, ok := m[x-1]
        if !ok {
            m[x-1] = fibMemo(x-1, m)
        }
        _, ok = m[x-2]
        if !ok {
            m[x-2] = fibMemo(x-2, m)
        }
        return m[x-1] + m[x-2]
    }
> Using a map as a lookup table caches the result of each function call during each iteration

<https://play.golang.org/p/Wxgl_OwkTY> again provides the full code (despite the Go playground not really providing time elapsed)

That's it: identifying the extra work and storing it somewhere that can be referenced, the trade-off is now that more memory is required. =]

## Dynamic Programming with Fibonacci Numbers

This alternative implementation removes the recursion (and helper function) and instead uses a simple for loop and a slice of ints.
It highlights the nuance of how Dynamic Programming is not necessarily just storing the result of a function call but genuinely understanding the nature of the problem.

    :::go
    func fibDynamic(n int) []int {
        a := []int{1}
        if n == 1 {
            return a
        }
        a = append(a, 1)
        if n == 2 {
            return a
        }
        for i := 2; i < n; i++ {
            a = append(a, a[i-2]+a[i-1])
        }
        return a
    }
> this trivial example also benefits from the slice index corresponding well to a key for each fibonacci value in the "lookup table"

The example Dynamic Programming solution avoids the map lookup and so should be the most performant <https://play.golang.org/p/VY9ul6ievC>, but since the Go Playground time elapsed does not work...

## Comparing with Benchmarks

Besides the "manual performance testing" with time and print statements you can use Go's more sophisticated tooling with bench.

Create **main_test.go** and run `go test -v -run=NOMATCH -bench=BenchmarkFibonacciSeries`

    :::go
    func BenchmarkFibonacciSeriesRecursive(b *testing.B) {
        for n := 0; n < b.N; n++ {
            fibSeriesRecursive(20)
        }
    }
    
    func BenchmarkFibonacciSeriesMemoization(b *testing.B) {
        for n := 0; n < b.N; n++ {
            fibSeriesMemoization(20)
        }
    }
    
    func BenchmarkFibonacciSeriesDynamicProgramming(b *testing.B) {
        for n := 0; n < b.N; n++ {
            fibDynamic(20)
        }
    }

> The nanoseconds per operation are dramatically less in the side-by-side comparison

    goos: linux
    goarch: amd64
    pkg: bitbucket.org/johnpfeiffer/gosrc/benchmarking
    BenchmarkFibonacciSeriesRecursive-4                10000            191632 ns/op
    BenchmarkFibonacciSeriesMemoization-4             200000             13675 ns/op
    BenchmarkFibonacciSeriesDynamicProgramming-4     2000000               814 ns/op
    PASS
    ok      bitbucket.org/johnpfeiffer/gosrc/benchmarking   7.157s

- <https://github.com/johnpfeiffer/go-fibonacci> for full source code
- *Reference for running go benchmarking <https://blog.john-pfeiffer.com/golang-testing-benchmark-profiling-subtests-fuzz-testing/#running-specific-benchmarks>*

## Insights
The hardest part of applying caching is understanding the problem well enough to see where the extra work can be avoided.
Thus I recommend pen and paper (or whiteboard) for diagramming the tree of (usually recursive) calls in order to see any patterns.

The tradeoff of memory for computation (time!) is usually worth it given modern large amounts of cheap memory available (assuming we do not have to worry about cache invalidation ;).

**<https://blog.john-pfeiffer.com/caching-data-and-common-gotchas-and-an-intro-to-redis-memcached-and-varnish/>**

Further exercises:

- the coin problem (do not need to re-calculate the sub problems) , <https://en.wikipedia.org/wiki/Coin_problem>
- towers of hanoi instructions series (rotate previous instructions rather than full recursion) , <https://en.wikipedia.org/wiki/Tower_of_Hanoi>

