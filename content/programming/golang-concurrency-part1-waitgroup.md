Title: Golang Concurrency Part 1 WaitGroup
Date: 2024-04-23 22:22
Tags: go, golang, goroutines, concurrency, waitgroup

[TOC]

When I tried to read my previous article on concurrency in Golang I felt like it tried to pack too much in so this is the same topic broken into parts, which may even leave room for more depth.
- previous article <https://blog.john-pfeiffer.com/golang-concurrency-goroutines-and-channels/>

# Background on Concurrency and Goroutines
Goroutines are like lightweight threads. This removes some of the overhead of attempting to use concurrency with OperatingSystem threads.
Here is someone else's better explanation of threads

- <https://www.youtube.com/watch?v=oV9rvDllKEg> Rob Pike describing Concurrency
- <https://en.wikipedia.org/wiki/Thread_(computing)>
- <https://www.cs.uic.edu/~jbell/CourseNotes/OperatingSystems/4_Threads.html>

# Goroutines
Normally in programs main executes sequentially from top to bottom.
Go routines can operate concurrently to main (and any other go routines). It only takes the simple syntax of prepending the keyword "go". 

    :::go
	package main
	
	import (
		"fmt"
		"time"
	)
	
	func main() {
		fmt.Println("start")
		go count()
		go foo()
		time.Sleep(1)
		fmt.Println("done")
	}
	
	func count() {
		fmt.Println("sleep then count")
		time.Sleep(2)
		for i := 0; i < 100; i++ {
			fmt.Printf("%d", i)
		}
	}

	func foo() {
		fmt.Println("foo")
	}

<https://go.dev/play/p/KX-bMG0KBBu> 

This code example highlighted that when main exits all goroutines also exit, even if they have not completed.


# Golang WaitGroup
In order to add control over the goroutines there are many tools, the simplest is WaitGroup. 

   :::go
    package main
    
    import (
        "fmt"
        "sync"
        "time"
    )
    
    func example(s string) {
        time.Sleep(1 * time.Second)
        fmt.Println(s)
    }
	
	func exampleAsync(s string, wg *sync.WaitGroup) {
		defer wg.Done()
		time.Sleep(1 * time.Second)
		fmt.Println(s)
	}
	
	func main() {
		fmt.Println(time.Now())
		example("hello")
		example("world")
		fmt.Println(time.Now())
	
		var wg sync.WaitGroup
		wg.Add(2)
		go func(s string) {
			example(s)
			wg.Done()
		}("foo")
	
		go exampleAsync("bar", &wg)

		wg.Wait()
		fmt.Println(time.Now())
		fmt.Println("done")
	}

<https://go.dev/play/p/YYJVC36uB5r>

The whole program executes in 3 seconds: even as sequentially things take 2 seconds, the next 2 sleep statements occur concurrently.

A WaitGroup must in advance be passed a count that matches every execution of "Done()" (usually by goroutines).

Even though the anonymous function that wraps "example()" and "exampleAsync()" both have a 1 second sleep statement the output shows they run concurrently.

_The anonymous function in the middle shows how to pass a string parameter, and also that the waitgroup variable is available through "closure"._
_For readability, maintainability, and re-use most people write a separate function rather than using anonymous functions._

Passing the waitgroup by reference is safe as it is designed for coordinating goroutines, and the "defer" keyword just ensures that just as the function exits that statement will immediately execute.


   :::go
    package main

    import (
        "fmt"
        "sync"
    )
	
        func main() {
                var wg sync.WaitGroup
                wg.Add(2)
                go func(s string) {
                        example(s)
                        wg.Done()
                }("foo")

                wg.Wait()
                fmt.Println("done")
        }

This is a common gotcha where the program will deadlock as the WaitGroup forever expects one more "Done()" than the code provides.


