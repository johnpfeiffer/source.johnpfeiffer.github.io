Title: Golang Interfaces Stack Linked List Queue Map Set
Date: 2016-10-05 20:34
Tags: go, golang, interfaces, stack, linked list, queue, map, set, strategy pattern

[TOC]

Two of the most useful tools in daily professional programming are hash maps and frameworks for modular abstractions.  It's the blend of performance and composability that makes Go an attractive language for getting things done.

## Maps aka Hash Tables in Go

For hash tables basic operations like insert, lookup, delete are basically "constant time" in big O notation which makes it the "go to" default data structure for a lot of basic coding.  That helps avoid having to write and maintain all the complexity and operations of an in-memory sorted data structure.

It is also often the desired data structure answer in a programming interview problem =]

Here's the basics of using a map since someone else has already done all of the hard work of figuring out the correct math of the hash function to avoid collisions and the engineering behind implementing it in a performant fashion.


### Using a map in go

    :::go
    package main

    import (
        "fmt"
    )

    func inSet(s string, m map[string]bool) bool {
        // gotcha: do not depend on just the return value but use a the second value which returns in map or not
        value, ok := m[s]
        fmt.Println(s, "has value", value, "and is in?", ok)
        if ok {
            return true
        } else {
            return false
        }
    }

    func main() {
        m := make(map[string]bool)
        // never use var m map[string]bool because m is nil and assign causes a panic
        m["foo"] = true
        m["bar"] = false

        fmt.Println(inSet("foo", m))
        fmt.Println(inSet("bar", m))
        fmt.Println(inSet("foobar", m))

        fmt.Println(len(m), " elements in map", m)
        delete(m, "bar")

        m2 := map[rune]int{'a': 1, 'b': 2, 'c': 3}
        for k, v := range m2 {
            fmt.Println(string(k), v)
        }
    }

> the two main gotchas for maps in go are to not accidentally assume that the value coming back from a map means that the key was in the map since if the key is not in the map it will return the default "empty" value which will be 0 or false, and to not start with a nil pointer since later assignment will cause a panic

- <https://play.golang.org/p/fqvNrELy1S> *play with maps yourself*
- <https://en.m.wikipedia.org/wiki/Hash_table>
- <https://blog.golang.org/go-maps-in-action>
- <https://golang.org/src/runtime/hashmap.go#L9>

### Sets

A common question in coding is whether a certain key or object has already been seen before.  The lookup cost in a set is  cheaper than a full search through a more complex data structure like a binary tree.

Golang currently does not have a "set" built into the language but given the code example you can see how to quickly achieve the same functionality with a map.  This is a common pattern: they keep the language simple and focus on low level components that perform and compose well while we code exactly what we need for a given usage.  (i.e. a huge meta "YouAren'tGoingToNeedIt")

- <https://en.wikipedia.org/wiki/Set_(abstract_data_type)>
- <https://xlinux.nist.gov/dads/HTML/set.html>
- <https://github.com/golang/go/wiki/MethodSets>

#### Low memory footprint map as a set

When implementing a Set, in some cases you can be very parsimonious with memory by using an empty struct.
This means you will rely on the very explicit _, ok pattern of checking for presence in the set.

    :::go
    package main
    
    import (
        "fmt"
        "unsafe"
    )
    
    func main() {
        m := make(map[rune]struct{})
        fmt.Println(m)
        m['a'] = struct{}{}
        fmt.Println(m)
        fmt.Printf("%#v \n", m)
        fmt.Println(unsafe.Sizeof(m['a']))
    
        var b bool
        fmt.Println(unsafe.Sizeof(b))
        var n int8
        fmt.Println(unsafe.Sizeof(n))
        var i interface{}
        fmt.Println(unsafe.Sizeof(i))
    }

> An empty struct is 0, a boolean and an int8 are size 1 (byte), an interface is size 8

- <https://play.golang.org/p/9cUE9-wwDY>
- <https://golang.org/pkg/unsafe/#Sizeof>

## Polymorphism with Go Interfaces

While definitely a distinctly different approach on objects and polymorphism than Object Oriented languages like Java and Python, the critical capabilities of Interfaces allows flexibility and re-usability in functionality enabling things like the Strategy Pattern.

Starting with the fundamentals of Types and Structs, Interfaces are a natural extension to separating "What" behavior is desired versus "How" it is implemented.

Using Interfaces can feel tricky at first but really the main challenge is the distinction between pointer receiver methods vs the default that Go has of pass by value (considering a pointer to be an integer value of an address ;)

Also, testing in Go relies heavily on the developer paying that up front cost of creating Interfaces (which is a much better longer term modular abstraction) rather than using Mocks.

This example uses a trivial Stack data structure but implements it 3 different ways to illustrate how the interface can have a variety of implementations and the caller can decide which one they prefer.

    :::go
    package main

    import (
        "fmt"
    )

    // Stacker is a data structure that has specific data access and storage properties
    // also known as a Last In First Out queue, and not fully implemented for this example =]
    // This interfaces only requires two methods to implement
    type Stacker interface {
        Push(n int)
        Show() []int
    }

    // DemoStack shows a demo example of different implementations of the interface
    func DemoStack(s Stacker, name string) {
        fmt.Println("Pushing 2, 1, 0, onto", name)
        s.Push(2)
        s.Push(1)
        s.Push(0)
        fmt.Println(name, "contains: ", s.Show())
    }

    // FakeStack implements the interface using only value receivers
    type FakeStack struct {
    }

    var fakeStackCheater []int

    // Show returns the global slice
    func (s FakeStack) Show() []int {
        return fakeStackCheater
    }

    // Push uses a global variable (evil) so it can get away with a value method receiver
    func (s FakeStack) Push(n int) {
        fakeStackCheater = append(fakeStackCheater, n)
    }

    // SliceStack is an integer stack data structure built using a slice
    type SliceStack struct {
        s []int
    }

    // Show displays the contents of the stack, pass a copy as no modification needed
    func (s SliceStack) Show() []int {
        return s.s
    }

    // Push an integer onto the stack, pass a reference so the receiver method can directly modify
    // https://github.com/golang/go/wiki/CodeReviewComments#receiver-type
    func (s *SliceStack) Push(n int) {
        s.s = append(s.s, n)
    }

    /* A real stack based upon a linked list */

    // IntNode is a pointer data structure for holding an integer
    type IntNode struct {
        value int
        left  *IntNode
        right *IntNode
    }

    // LinkedListStack is an integer stack data structure built using a slice
    type LinkedListStack struct {
        head *IntNode
    }

    // Show returns the total number of elements currently stored in the LinkedListStack
    func (s LinkedListStack) Show() []int {
        var result []int
        for current := s.head; current != nil; current = current.right {
            result = append(result, current.value)
        }
        return result
    }

    // Push an integer onto the stack, pass a reference so the receiver method can directly modify
    func (s *LinkedListStack) Push(n int) {
        new := IntNode{value: n}
        if s.head == nil {
            s.head = &new
        } else {
            new.right = s.head
            s.head = &new
        }
    }

    func main() {
        // a fake stack does not use pointer method receivers and must modify the data structure some other way
        var f FakeStack
        DemoStack(f, "FakeStack")

        // stacks that modify their underlying data structure must pass a reference
        var s SliceStack
        DemoStack(&s, "SliceStack")
        var k LinkedListStack
        DemoStack(&k, "LinkedListStack")
    }
> This example contradicts one of the best practices: pointer receivers should be consistent <https://tour.golang.org/methods/4> , so Show() and Push() should have the same receiver type

- A Pointer Receiver allows the method to make a modification (i.e. syntactic sugar where `(s *SliceStack) Push(n int)` could be thought of as `Push(s *SliceStack, n int)`
- A Pointer Receiver prevents an extra copy (in the instance of a very large object)
- All of the methods of an interface should be consistent (as a part of the developer user experience)

References:

- <https://play.golang.org/p/U1l2Ni89L4> *play along with the source code snippet*
- <https://bitbucket.org/johnpfeiffer/go-interfaces-stack-linkedlist> *the more complete source code*
- <https://en.wikipedia.org/wiki/Stack_(abstract_data_type)>
- <https://golang.org/doc/effective_go.html#interfaces>
- <https://github.com/golang/go/wiki/CodeReviewComments#receiver-type>
- <https://en.wikipedia.org/wiki/Polymorphism_(computer_science)>
- <https://en.wikipedia.org/wiki/Strategy_pattern>
- <https://nathanleclaire.com/blog/2015/10/10/interfaces-and-composition-for-effective-unit-testing-in-golang/>
- <https://blog.cloudflare.com/go-interfaces-make-test-stubbing-easy/>


## Doubly Linked List and First In First Out Queue
With some small additions the linked list can be enhanced to provide the functionality of a Queue.
The "doubly linked list" (<https://en.wikipedia.org/wiki/Doubly_linked_list>) means that one can traverse from either the head (using next) or the tail (using previous).
It is not too expensive to add the extra previous pointer to each node and a tail pointer and this makes the FIFO capabilities fairly straightforward.
*Thankfully with a garbage collected language like Go we do not have to worry about manually allocating or deallocating memory, though we should always keep an eye out for memory leaks*

    :::go
    package main

    import (
        "fmt"
    )

    // IntNode is a pointer data structure for holding an integer
    type IntNode struct {
        value    int
        previous *IntNode
        next     *IntNode
    }

    // MyList is a linked list of pointers
    type MyList struct {
        head *IntNode
        tail *IntNode
    }

    // Enqueue adds an integer onto the end of the list
    func (q *MyList) Enqueue(n int) {
        new := IntNode{value: n}
        if q.head == nil {
            q.head = &new
            q.tail = &new
        } else {
            q.tail.next = &new
            q.tail = &new
        }
    }

    // Dequeue removes the first integer added to the list (from the front)
    func (q *MyList) Dequeue() int {
        // TODO: error handling for dequeuing when the list is empty
        result := q.head
        q.head = q.head.next
        return result.value
    }

    func main() {
        var q MyList
        q.Enqueue(3)
        q.Enqueue(4)
        fmt.Printf("FirstInFirstOut head: %v at memory address %p \n", q.head.value, q.head)
        fmt.Printf("FirstInFirstOut tail: %v at memory address %p \n", q.tail.value, q.tail)
        fmt.Println("dequeuing a value: ", q.Dequeue())
        fmt.Printf("FirstInFirstOut head: %v at memory address %p \n", q.head.value, q.head)
        fmt.Printf("FirstInFirstOut tail: %v at memory address %p \n", q.tail.value, q.tail)
    }

> The terminology changed a little bit from Push to Enqueue but now we can have a simple "fair buffer"

- <https://play.golang.org/p/tHIiRsk443C> *your queue in play*
- <https://en.wikipedia.org/wiki/Queue_(abstract_data_type)>
- <https://en.wikipedia.org/wiki/FIFO_(computing_and_electronics)>
- <https://www.cs.cmu.edu/~adamchik/15-121/lectures/Stacks%20and%20Queues/Stacks%20and%20Queues.html>

### Doubly Linked List in the Go Standard Library

Wonderfully there is an implementation of a Doubly Linked List in the Go standard library: <https://golang.org/pkg/container/list/>

    :::go
    package main
    
    import (
	    "container/list"
	    "fmt"
    )
    
    func main() {
	L := list.New()
	e1 := L.PushBack(1)	// enqueue
	L.InsertAfter(3, e1)	
	e3 := L.Back()
	L.InsertBefore(2, e3)	
    
	displayFIFO(L)
	fmt.Printf("\nTraverse in reverse with Prev(): ")
	displayLIFO(L)
    
	L2 := list.New()
	L2.PushBack("D")
	displayFIFO(L2)
	L.PushBackList(L2)
	displayFIFO(L)
    
	L.Remove(e1)
	fmt.Printf("\nRemoved %v", e1.Value)
	displayFIFO(L)
	fmt.Printf("\nFront is now: %v", L.Front().Value)
	fmt.Printf("\n%#v", L)
    }
    
    func displayFIFO(L *list.List) {
        fmt.Printf("\nList length: %v \n", L.Len())
        for e := L.Front(); e != nil; e = e.Next() {
            fmt.Printf("%v ", e.Value)
        }
        fmt.Println()
    }
    
    func displayLIFO(L *list.List) {
        fmt.Printf("\nList length: %v \n", L.Len())
        for e := L.Back(); e != nil; e = e.Prev() {
            fmt.Printf("%d ", e.Value.(int))
        }
        fmt.Println()
    }

> All of the node and pointer implementation is already handled for you, play with it here: <https://play.golang.org/p/FUEtqMNoaP9>

