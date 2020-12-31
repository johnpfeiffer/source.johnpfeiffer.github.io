Title: Sorting in Golang
Date: 2020-09-30
Tags: go, golang, sort, sorting, map

[TOC]

We maybe take for granted that humans sort things: having a list of favorites e.g. "top ten songs".

Computers (and software) are exceptional for sorting since it is both boring and requires precision; especially for large data sets that are beyond the human brain.

Sorting things (not just numbers!) is foundational in Computer Science, <https://en.wikipedia.org/wiki/Sorting_algorithm>

*Sorting is often considered a "free first step" (since sorting is "Big O n logn") for many problems that already would take a least "n logn" to solve.*

Golang has made Sorting really easy and efficient. *Both in terms of compute and memory*

## Verbose implementation of Sorting with Go Primitives like a Map

First, if you want to just stick with primitives, you can sort a particular item like this...

    :::go
    package main

    import (
        "fmt"
        "sort"
    )

    // Person is defined by name and age
    type Person struct {
        Name string
        Age  int
    }

    func main() {
        People := []Person{
            {Name: "Charles", Age: 25},
            {Name: "Alice", Age: 25},
            {Name: "Bob", Age: 24},
        }
        fmt.Printf("Original Listing: %v \n", People)

        // Example of manually sorting using extra primitive data structures
        AgeToPeople := make(map[int][]Person)
        for _, p := range People {
            // handle the edge case of not yet having a list entry in the map
            _, ok := AgeToPeople[p.Age]
            if !ok {
                AgeToPeople[p.Age] = []Person{p}
            } else {
                temp := AgeToPeople[p.Age]
                AgeToPeople[p.Age] = append(temp, p) // this maintains the pre-existing order on duplicates
            }
        }

        // Sort by a property and then dereference the lookup map
        // get the unique list of ages (each map key is unique)
        var Ages []int
        for age := range AgeToPeople {
            Ages = append(Ages, age)
        }

        sort.Ints(Ages)

        var PeopleSortedByAge []Person
        for _, age := range Ages {
            temp := AgeToPeople[age]
            for _, p := range temp {
                PeopleSortedByAge = append(PeopleSortedByAge, p)
            }
        }
        fmt.Printf("Sorted by age Listing: %v \n", PeopleSortedByAge)

        // Optionally create a subset of the "lowest N members"
        // this could be more efficient if it was applied during the PeopleSortedByAge loop
        PeopleSortedByAgeSubset := PeopleSortedByAge[:2]
        fmt.Printf("Stable Subset of Sorted by age: %v \n", PeopleSortedByAgeSubset)

> This code is verbose but does provide visibility and control:
> Not modifying the original slice, the exact property used for sorting, explicit handling of duplicates aka the "stable sort" property

<https://en.wikipedia.org/wiki/Sorting_algorithm#Stability>

*ok, I am "hand-waving" when we use the built in sorting of Integers but I'm not looking to re-invent the wheel...*

To execute (or modify) the code yourself <https://play.golang.org/p/A9IYxubb8yK>

## Very easy and fast way to Sort in Go

    :::go
    package main
    
    import (
        "fmt"
        "sort"
    )
    
    // Person is defined by name and age
    type Person struct {
        Name string
        Age  int
    }
    
    func main() {
        People := []Person{
            {Name: "Charles", Age: 25},
            {Name: "Alice", Age: 25},
            {Name: "Bob", Age: 24},
        }
        fmt.Printf("Original Listing: %v \n", People)

        sort.SliceStable(People, func(i, j int) bool { return People[i].Age < People[j].Age })
        fmt.Printf("Original Sorted using BuiltIn SliceStable: %v \n", People)

> The anonymous function is passed in as a parameter to define how to compare elements in the slice
> and be aware that the Sort function modifies the original slice

This sorting capability comes built in with the Go Standard Library <https://golang.org/pkg/sort/#SliceStable>

### Why sorting with Go is efficient

Leveraging a well established implementation of sort saves a lot of developer time (and provides some guarantee of correctness).

As a compiled language Go is performant in terms of compute (which often translates to reasonably fast wall clock time too).

The use of Slices means under the hood there can be pointers and references rather than full copies which reduces memory consumption.

- <https://blog.golang.org/slices-intro>
- <https://blog.golang.org/slices>
- <https://golang.org/src/sort/sort.go> (quicksort but it could be any highly performant sort)


## Sorting objects in Go with Customization

It is very powerful is to leverage Golang's interface capabilities and the Sort package.

Since Go uses composition instead of inheritance any arbitrary data structure can support Sorting.

- <https://talks.golang.org/2012/splash.article#TOC_15.>
- <https://golang.org/pkg/sort/>

Thus with a struct definition, then writing a few method definitions, one can sort a collection of objects.

    :::go
    package main
    
    import (
        "fmt"
        "sort"
    )
    
    // Person is defined by name and age
    type Person struct {
        Name string
        Age  int
    }
    
    func main() {
        People := []Person{
            {Name: "Charles", Age: 25},
            {Name: "Alice", Age: 25},
            {Name: "Bob", Age: 24},
        }
        fmt.Printf("Original Listing: %v \n", People)
    
        sort.Sort(ByAge(People))
        fmt.Printf("Original Sorted using a Customized Less: %v \n", People)
    }
    
    // ByAge is a list of Persons that can be sorted by age
    type ByAge []Person
    
    // Len implements the interface for Sort
    func (p ByAge) Len() int {
        return len(p)
    }
    
    // Swap implements the interface for Sort
    func (p ByAge) Swap(i, j int) {
        p[i], p[j] = p[j], p[i]
    }
    
    // Less implements the interface for Sort
    func (p ByAge) Less(i, j int) bool {
        // customize sorting on age equivalence to use Name too
        if p[i].Age == p[j].Age {
            if p[i].Name <= p[j].Name {
                return true
            }
            return false
        }
        // otherwise ages are not equal, simply use age
        return p[i].Age < p[j].Age
    }

> This "strategy pattern" allows Golang to provide Sorting as an abstraction

- <https://en.wikipedia.org/wiki/Strategy_pattern#Strategy_and_open/closed_principle>

The ability to customize logic in **Less()** is very powerful, yet callers need only pass an extra **ByAge()** to benefit.


*To execute (or modify) the code yourself use <https://play.golang.org/p/A9IYxubb8yK>*

If I ever put more time into various ideas or helper functions it will end up here <https://github.com/johnpfeiffer/go-sort-example>

## Sorting in Reverse

There is a helper function that just reverses the sorting order, so once you can Sort (because you fulfill the Interface), then you can "reverse sort" =)
**alternatively you could use a for loop and iterate over a sorted slice, starting from index length-1 down to 0**

- <https://golang.org/pkg/sort/#Reverse>
- <https://play.golang.org/p/EdVA6NzNRiF>

    :::go
    package main
    
    import (
	"fmt"
	"sort"
    )
    
    func main() {
	a := []int{4, 2, 1, 3}
	// convert a to an IntSlice so it can be Reverse Sorted
	sort.Sort(sort.Reverse(sort.IntSlice(a)))
	fmt.Println(a)
    }

> Typically this is how to control "ascending" or "descending" sorted order

## Sorting a Map in Go

### Sorting a map by Keys

To sort by keys is relatively trivial, for a given map "m" creating a slice and sorting it

    :::go
	m := make(map[string]string)
	m["z"] = "zebra"
	m["aa"] = "Aardvark"
	m["B"] = "Bear"
	m["a"] = "antelope"
    
	for k := range m {
		sortedKeys = append(sortedKeys, k)
	}
	sort.Strings(sortedKeys)
    
	for _, key := range sortedKeys {
		fmt.Printf("%s %s ", key, m[key])
	}

### Sorting a map by Values
Sorting a map by values is a little harder which is likely why a cursory internet search brings up far fewer code snippet examples ;)

    :::go
    // SortByValue returns the Keys in the sorted order of the Values (does not guarantee Stability)
    func SortByValue(m map[string]string) (sortedKeys []string) {
    
	// create a reverse lookup mapping that can handle collisions
	// (duplicates) when the same value has multiple occurrences
	ValueToKey := make(map[string][]string)
	for k, v := range m {
		_, ok := ValueToKey[v]
		if !ok {
			ValueToKey[v] = []string{k}
		} else {
			temp := ValueToKey[v]
			ValueToKey[v] = append(temp, k)
		}
	}
    
	// sort the Values
	var uniqueValues []string
	for v := range ValueToKey {
		uniqueValues = append(uniqueValues, v)
	}
	sort.Strings(uniqueValues)
    
	// get the corresponding Keys
	for _, v := range uniqueValues {
		keys := ValueToKey[v]
		sortedKeys = append(sortedKeys, keys...)
	}
    
	return
    }

> The gotcha is that different Keys could have the same Value

Full source code examples: <https://github.com/johnpfeiffer/go-sort-example>

