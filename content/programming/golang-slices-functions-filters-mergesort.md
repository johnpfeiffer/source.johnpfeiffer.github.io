Title: Golang Slices Functions Filters Mergesort
Date: 2016-10-02 23:45
Tags: go, golang, testing, arrays, slices, functions, filter, algorithms, merge, mergesort, strategy pattern

[TOC]

## Tips on learning a new programming language
Learning a new programming language takes a lot of effort.  Here are some tips I've found to make it easier:

1. Layering: read through the material and just accept things without trying to understand every piece, small pieces are easier to digest and absorb
1. Repetition: it is natural to read and re-read before comprehension occurs, learning right before sleep is scientifically proven to better enter long term memory
1. Immersion: surround yourself with reminders of the material like books, web sites, on your phone, flash cards, online and real life discussions, videos
1. Variety: sometimes it sticks better with a book, other times a video or podcast.  Different teachers will emphasize or convey certain topics better.  Do not give up because it's confusing from one source, there are many many sources to learn from
1. Practice: apply yourself as programming is far better internalized "in action" rather than just theory
1. Engage: using provided exercises will get you to the solution the instructor expects, creating your own coding projects will force you to use the tools in ways that make sense to you (and discover why certain things are "best practice")
1. Go Deep: once comfortable moving around, real fluency and understanding requires digging into exactly how something is architected and implemented, what are the corner cases, and why things are done one way over another

## Arrays underlying slices with memory addresses and unsafe pointers

Arrays are a mainstay of programming (mechanical sympathy for memory addresses and our very serial brains).
Here is a major digression into Go slices which is a pointer structure that holds an array and manages the dynamic resizing.
*Hint: the whole point of Go is to not need to use low level unsafe pointer arithmetic*

    :::go
    package main
     
    import (
        "fmt"
        "unsafe"
    )
     
    func main() {
        capacityDoubles()
    }
     
    func capacityDoubles() {
        // slice of zero length and zero capacity, basically just a "slice header"
        // NOTE this is different from a "nil slice" which is a nil pointer
        var nilPointer []int
        fmt.Printf("example nil pointer: %#v \n", nilPointer)
        fmt.Printf("has memory adddress: %p \n", &nilPointer)
    
        s := make([]int, 0, 0)
        fmt.Printf("example empty slice: %#v \n", s)
        fmt.Printf("has memory adddress: %p \n", &s)
        fmt.Println("both have the same length:", len(nilPointer), len(s), "but does each equal nil? ", nilPointer == nil, s == nil)
    
        fmt.Println(s)
        for i := 0; i < 3; i++ {
            // capacity doubles so a new underlying array, if we checked with reflect the memory address would change
            s = append(s, i)
            fmt.Printf("len=%d cap=%d %v\n", len(s), cap(s), s)
        }
    
        // https://golang.org/pkg/reflect/#SliceHeader
        // since a slice is a struct containing an underlying array of memory addresses...
        // https://golang.org/pkg/builtin/#byte
        h := make([]byte, 2, 2)
        h[1] = 5
        fmt.Printf("Slice of byte memory addresses: %p ", &h)
        // 0xc42006e200 example address of the slice
        fmt.Printf("%p ", &h[0])
        fmt.Printf("%p ", &h[1])
        // 0xc420074458 0xc420074459 , the two elements are exactly 1 byte apart in address locations
        // Getting the value from the memory location using a piont
        fmt.Printf("\nThe byte value in the second element is binary five: %b", *(&h[1]))
    
        // https://golang.org/pkg/unsafe/
        fmt.Printf("\nUnsafe pointer of the first memory location: %p", unsafe.Pointer(&h[0]))
        // unsafe pointer arithmetic
        lastAddress := uintptr(unsafe.Pointer(&h[0])) + unsafe.Sizeof(h[0])
        // convert back into a usable pointer type
        lastAddressPtr := (*byte)(unsafe.Pointer(lastAddress))
        fmt.Printf("\nAfter pointer arithmetic and unsafe re-typed: %p, value: %b", lastAddressPtr, *lastAddressPtr)
        fmt.Printf("\nSafe examination of the second location in the slice: %#v", &h[1])
        fmt.Println()
    }
    


    example nil pointer: []int(nil)
    has memory adddress: 0xc42000e440
    example empty slice: []int{}
    has memory adddress: 0xc42000e4a0
    both have the same length: 0 0 but does each equal nil?  true false
    []
    len=1 cap=1 [0]
    len=2 cap=2 [0 1]
    len=3 cap=4 [0 1 2]
    Slice of byte memory addresses: 0xc42000e580 0xc42000a618 0xc42000a619 
    The byte value in the second element is binary five: 101
    Unsafe pointer of the first memory location: 0xc42000a618
    after pointer arithmetic and unsafe re-type: 0xc42000a619, value: 101
    Safe examination of the second location in the slice: (*uint8)(0xc42000a619)
> Reminder, just because we can does not mean we should =p

- <https://play.golang.org/p/QaGtbfPwkS> *(you can try it yourself!)*
- <https://blog.golang.org/go-slices-usage-and-internals>
- <https://golang.org/pkg/reflect/#SliceHeader>
- <https://golang.org/pkg/unsafe/>
- <https://en.wikipedia.org/wiki/Dereference_operator>

### Examples of Go Slice operations and tricks

- <https://github.com/golang/go/wiki/SliceTricks>

    :::go
    package main
    
    import (
        "fmt"
    )
    
    func main() {
        a := []int{1, 2, 3}
        fmt.Println(a[1:2])			// 2
        fmt.Println(append(a, a[1:2]...))	// 1, 2, 3, 2
    
        // pre-allocating might be premature optimization and lead to bugs
        premature := make([]string, 10, 10)
        premature[0] = "foo"
        premature = append(premature, "bar")
        fmt.Println(len(premature), premature) // "11 [foo          bar]"
    
        var s []string
        s = append(s, "add", "multiple", "items", "at", "once")
        fmt.Println(len(s), s) // "5 [add multiple items at once]"
    
        // COPY also known as ADD to a slice (in this case add to a nil slice)
        b := append([]string(nil), s...) // the triple dots (ellipsis in english) indicates a variadic parameter
        // https://golang.org/ref/spec#Passing_arguments_to_..._parameters , https://golang.org/src/builtin/builtin.go?s=4716:4763#L124
        fmt.Println(len(b), b) // "5 [add multiple items at once]"
    
        c := make([]string, len(s)) // perhaps more readable
        copy(c, s)
        fmt.Println(len(c), c) // "5 [add multiple items at once]"
    
        // CUT - but warning, this only removes it from the slice, NOT the underlying array so a possible memory leak
        s = append(s[:1], s[4:]...) // up to but not including index 1, start at index 4 to the end
        fmt.Println(len(s), s)      // "2 [add once]"
    
        // DELETE index 2 (same ordering), no memory leak by correctly setting it to the zero value (usually nil for objects)
        copy(b[2:], b[2+1:])
        b[len(b)-1] = ""
        b = b[:len(b)-1]
        fmt.Println(len(b), b) // "4 [add multiple at once]"
    
        // INSERT into index 2 a new value
        // b = append(b[:2], append([]string{"foobar"}, b[2:]...)...)
        // Preferred more readable and avoid the extra slice creation with copy sleight of hand
        b = append(b, "")
        copy(b[3:], b[2:])
        b[2] = "foobar"
        fmt.Println(len(b), b) // "5 [add multiple foobar at once]"
    
        // SWAP two values
        b[0], b[1] = b[1], b[0]
        fmt.Println(len(b), b) // "5 [multiple add foobar at once]"
    
        // REVERSE by using the mirror image effect and multiple assignments
        for i := len(b)/2 - 1; i >= 0; i-- {
            opp := len(b) - 1 - i
            b[i], b[opp] = b[opp], b[i]
        }
        fmt.Println(len(b), b) // "5 [once at foobar add multiple]"
    }

> Slices are fairly fundamental and while most things are easy there are definitely some gotchas

> A critical thing to remember when reasoning is that slices are references to underlying arrays, so small subslice from a very large slice will prevent that larger object/array from being garbage collected

- <https://play.golang.org/p/znwrmQavmn> (work with the slice tricks example yourself)
- <https://golang.org/ref/spec#Passing_arguments_to_..._parameters>
- <https://golang.org/src/builtin/builtin.go?s=4716:4763#L124>

> Of course, read the docs and test it for your requirements, situation, and circumstances!

### Gotcha with Slices and Pointers

Assigning a new slice variable (pointer) to an existing slice will link the two together.  This may lead to undesired "side-effects".

    :::go
    package main
    
    import (
        "fmt"
    )
    
    func main() {
        s := []string{"a", "b", "c"}
        fmt.Println(s) // [a b c]
        i := 1
        temp := s
        temp = append(temp[:i], temp[i+1:]...)
        fmt.Println(temp) // [a c]
        fmt.Println(s) // [a c c]
    
        fmt.Printf("%p \n", &s)
        fmt.Printf("%p \n", &temp)
    }
> removing (cut or delete) a specific element in the slice using the new pointer affects the original slice


<https://play.golang.org/p/togSAlnj6J>


## Functions, Anonymous Functions, Functions as Parameters, and Filters

Go has functions as first class citizens.  Just assign a function to a variable or define a type that is a function signature.
Since go starts from simple blocks we build, as needed, more complex tools like filtering from a slice of integers.

    :::go
    package main
    
    import( "fmt"
    )
    
    // https://golang.org/doc/codewalk/functions/
    // filter is a type that allows us to apply a test to the provided integer parameter
    type filter func(x int) bool
    
    // applyFilter is a trivial examply of using a filter as a parameter
    func applyFilter(fn filter, x int) bool {
        return fn(x)
    }
    
    // SliceFilter returns a new slice filtered using the filter function parameter
    func SliceFilter(fn filter, n []int) []int {
        var result []int
        for _, x := range n {
            if fn(x) {
                result = append(result, x)
            }
        }
        return result
    }
    
    // isEven returns a filter (the anonymous function inside)
    func isEven() filter {
        return func(x int) bool {
            if x%2 == 0 {
                return true
            }
            return false
        }
    }
    
    func main() {
        a := []int{2, 4, 6}
        b := []int{1, 3, 7, 9}
        c := []int{5, 3, -1, 12}
    
        var iseven = func(x int) bool {
            if x%2 == 0 {
                return true
            }
            return false
        }
        fmt.Println("2 is even: ", iseven(2))
        fmt.Println("4 is even: ", applyFilter(iseven, 4))
        fmt.Println(a, "is even: ", SliceFilter(iseven, a))  // [2 4 6] is even:  [2 4 6]
        fmt.Println(b, "is not even: ", SliceFilter(iseven, b))  // [1 3 7 9] is not even:  []
        fmt.Println(c, "filtered for evens becomes: ", SliceFilter(isEven(), c))  // [5 3 -1 12] filtered for evens becomes:  [12]
    }
> With a function that returns a function, and a function that requires a parameter that is of the type "function signature", we can apply the Strategy Pattern

- <https://play.golang.org/p/Uxm7HZzS-V> *(yes you can mess with functions too)*
- <https://en.wikipedia.org/wiki/Anonymous_function>
- <https://en.wikipedia.org/wiki/Strategy_pattern>

## MergeSort
And because I like source code in blogs, a highly imperfect mergesort.

    :::go
    package main
    
    import (
        "fmt"
    )
    
    // SliceSplit is a function to split a slice into roughly even partitions
    // https://golang.org/doc/effective_go.html#two_dimensional_slices
    /* A more specific implementation than SliceSplit with the special case partitionSize = 1 could have been
    result := make([][]int, len(n), len(n))
    for i := 0; i < len(n); i++ {
        element := make([]int, 1, 1)
        element[0] = n[i]
        result[i] = element
    }
    return result
    */
    func SliceSplit(n []int, count int) ([][]int, error) {
        result := [][]int{}
        // TODO: is there a better way of handling split into 0 pieces?
        if count == 0 || count > len(n) {
            return result, fmt.Errorf("Cannot split length %d into %d pieces", len(n), count)
        }

        partitionSize := len(n) / count
        for i, k := 0, 0; i < count; i, k = i+1, k+partitionSize {
            a := n[k : k+partitionSize]
            // special case to pad the last partition with all elements
            if i == count-1 {
                a = n[k:]
            }
            result = append(result, a)
        }
        return result, nil
    }
    
    // SlicesMerge takes two sorted slices of integers and merges them into a single sorted slice of integers
    func SlicesMerge(a []int, b []int) []int {
        s := make([]int, len(a)+len(b))
        for ai, bi, si := len(a)-1, len(b)-1, len(a)+len(b)-1; si >= 0; si-- {
            if ai < 0 {
                s[si] = b[bi]
                bi--
            } else if bi < 0 {
                s[si] = a[ai]
                ai--
            } else if a[ai] > b[bi] {
                s[si] = a[ai]
                ai--
            } else {
                s[si] = b[bi]
                bi--
            }
        }
        return s
    }
    
    //MergeConsecutiveElements joins two consecutive slice elements together
    func MergeConsecutiveElements(a [][]int) [][]int {
        var result [][]int
        for i, k := 0, 0; i < len(a); i++ {
            if i+1 < len(a) {
                result = append(result, SlicesMerge(a[i], a[i+1]))
                k++
                i++
            } else {
                result = append(result, a[i])
            }
        }
        return result
    }
    
    // MergeSort uses the merge sort algorithm to return a sorted a slice of integers
    func MergeSort(n []int) []int {
        parts, _ := SliceSplit(n, len(n))
        result := MergeConsecutiveElements(parts)
        for len(result) > 1 {
            result = MergeConsecutiveElements(result)
        }
    
        return result[0]
    }
    
    func main() {
    
        n := []int{2, 1, 0, -1}
        fmt.Println("unsorted start:", n)
        fmt.Println("sorted:", MergeSort(n))
    
        n = []int{0, 1, 2}
        fmt.Println("unsorted start:", n)
        fmt.Println("sorted:", MergeSort(n))
    
        n = []int{9, 2, 4, 3}
        fmt.Println("unsorted start:", n)
        fmt.Println("sorted:", MergeSort(n))
    
        n = []int{9, 8, 7, 3, 2, 5}
        fmt.Println("unsorted start:", n)
        fmt.Println("sorted:", MergeSort(n))
    
        fmt.Println("done")
    }


- <https://en.wikipedia.org/wiki/Merge_sort>
- <https://play.golang.org/p/nAHF50zk7m> *(modify the merge online)*
- <https://bitbucket.org/johnpfeiffer/go-slice-mergesort> *(because version control means the fun never stops)*

