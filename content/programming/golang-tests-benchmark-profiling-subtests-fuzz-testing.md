Title: Golang Testing Benchmark Profiling Subtests Fuzz Testing
Date: 2016-10-22 20:44
Tags: go, golang, testing, benchmark, profiling, subtests, tdd

[TOC]

Go makes it very easy to unit test with the packagename_test.go file right next to the package source code file(s).

As a pragmatic language designed for developers who ship to production the amount of built in tooling (testing, benchmarks, etc.) is impressive.

Taking an earlier example I gave of MergeSort let's examine how TestDrivenDevelopment (or Design) was used to implement it.

## Small functions make for good tests

Small functions are easier to read and code is read 1000 times more often than it is written. *(completely made up but believable fact).*

Less lines of very-readable-code is usually an ok approximation for complexity, and less complexity means your program is easier to reason about (and easier to validate with tests!).


### Some reasons to not use MEGA-OBJECTS

One of the things that TDD helps focus on is modularity and requirements.  Two tensions to balance are the needs of the caller versus the needs of the function.

What I mean is that the function caller wants to understand what they have to provide and what they'll get back.  If the function asks for a MEGA-OBJECT then somehow the caller has to find or create a MEGA-OBJECT (which sounds very expensive).  And if the function didn't really need the MEGA-OBJECT then the function will extract the one value it actually needs and throw all that work away.

If instead the function asks for the integer primitive that is the value of the MEGA-OBJECT's this should be very easy to fulfill.  (Which is how tests help discover this MEGA-OBJECT anti-pattern, because even MEGA-OBJECT mocks are difficult).

A second reason to not pass a MEGA-OBJECT is that those are usually "pass by reference" for performance reasons and if modifying/side-effects are allowed then the function may accidentally invalidate other values (or intentionally corrupt data or override permissions).

The less state being passed around the easier it is to quickly write a large base of non brittle unit tests to isolate exactly where the logic goes wrong when doing "the simplest thing" and of course to communicate to others/callers how they might use your function or how it handles failure modes.

- <http://martinfowler.com/bliki/TestPyramid.html>
- <https://testing.googleblog.com/2015/04/just-say-no-to-more-end-to-end-tests.html>


## Example function with go unit tests

This example function requires two slices of integers.

    :::go
    package main

    import (
        "fmt"
    )
    
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
    
    func main() {
        a := []int{1, 3, 5}
        b := []int{2, 4, 6}
        fmt.Println("merged:", SlicesMerge(a, b))
    }
> a main function with print statements is the tried and true way of manual testing , `go run main.go`


### main_test.go

> Automated units tests means another developer can fix a bug and ensure it does not regress, read and learn expected behavior, and of course have automated continuous integration catch problems as early as possible, `go test`

    :::go
    package main
    
    import (
        "reflect"
        "testing"
    )
    
    
    var nilslice []int
    
    var empty = []int{}
    
    func TestSlicesMergeEmpty(t *testing.T) {
        t.Parallel()
        assertSlicesEqual(t, empty, SlicesMerge(empty, empty))
        assertSlicesEqual(t, empty, SlicesMerge(empty, nil))
        assertSlicesEqual(t, empty, SlicesMerge(nil, empty))
        assertSlicesEqual(t, empty, SlicesMerge(nil, nil))
    }
    
    func TestSlicesMergeHalfEmpty(t *testing.T) {
        t.Parallel()
        a := []int{1}
        assertSlicesEqual(t, a, SlicesMerge(a, empty))
        assertSlicesEqual(t, a, SlicesMerge(empty, a))

        a = []int{1, 2}
        assertSlicesEqual(t, a, SlicesMerge(a, empty))
        assertSlicesEqual(t, a, SlicesMerge(empty, a))
    }
    
    func TestSlicesMergeNegative(t *testing.T) {
        // if os.Getenv("MY_ENVIRONMENT_VARIABLE") == "" {
        t.Skip("skipping test: $MY_ENVIRONMENT_VARIABLE is not set")
    
        t.Parallel()
        a := []int{1, 3}
        b := []int{-2870837225030527764, -2}
        assertSlicesEqual(t, []int{-2870837225030527764, -2, 1, 3}, SlicesMerge(a, b))
    }
    
    
    // Helper Functions
    
    func assertSlicesEqual(t *testing.T, expected []int, result []int) {
        if !reflect.DeepEqual(expected, result) {
            t.Error("\nExpected:", expected, "\nReceived: ", result)
        }
    }

> The idea is to have code that is testable, and just use Go code to write the tests (not another DomainSpecificLanguage to learn)

- <https://golang.org/pkg/testing/>

> Skipping tests is fairly important to applying logic to parts of the test suite (or maybe deferring paying some technical debt)

> Parallel indicates the tests can run in parallel, not useful here but in larger test suites taking advantage of extra processor power (GOMAXPROCS) to speed up the feedback loop is always appreciated

> Even in a statically compiled language making comparisons of lists of potentially nested objects is unguaranteed, but the reflection function DeepEqual does a best effort job

- <https://golang.org/pkg/reflect/#DeepEqual>

#### Running the tests in sequence and not parallel

`t.Parallel()` indicates a test can run in parallel, but if you are debugging or really need a specific order then using `go test -p 1` will force it to run each test sequentially.

- <https://github.com/golang/go/blob/master/src/testing/testing.go#L300>
- <https://golang.org/pkg/cmd/go/internal/test/>

Note that Go Test will execute multiple different package tests in parallel...

>     -parallel n
>        Allow parallel execution of test functions that call t.Parallel.
>        The value of this flag is the maximum number of tests to run
>        simultaneously; by default, it is set to the value of GOMAXPROCS.
>        Note that -parallel only applies within a single test binary.
>        The 'go test' command may run tests for different packages
>        in parallel as well, according to the setting of the -p flag
>        (see 'go help build').

#### Running a specific test

`go test -v -run TestSlicesMergeHalf`

> Getting verbose output and specifying tests is quite helpful when fixing a piece of code or test.  **Note** the run parameter takes a regular expression


#### Test Coverage

Sometimes people talk about "test coverage" and while it's clear that 100% coverage is rarely possible (nor entirely desirable from the idea of diminishing returns and exponential growth in integration combinations outside of the simplest function) , it's still a useful metric/tool to discover if there's a chunk of code that's "whistling in the wind".

`go test -cover`
> "coverage: 75.0% of statements"

Generate a "coverage profile" of how many times each statement was run, use the current directory:
`go test -covermode=count -coverprofile=count.out . `
> ok      command-line-arguments  0.004s  coverage: 94.7% of statements

`go test -covermode=count -coverprofile=count.out ./stringsmoar.go ./stringsmoar_test.go`
> Alternatively, pass the name of the package (and test files)

`go tool cover -func=count.out`
> utilize the "coverage profile" to see the coverage breakdown by function


    bitbucket.org/johnpfeiffer/stringsmoar/stringsmoar.go:23:       RuneFrequency                   100.0%
    ...
    bitbucket.org/johnpfeiffer/stringsmoar/stringsmoar.go:82:       RemoveNthRune                   100.0%
    bitbucket.org/johnpfeiffer/stringsmoar/stringsmoar.go:96:       RemoveNthItem                   0.0%
    ...
    bitbucket.org/johnpfeiffer/stringsmoar/stringsmoar.go:115:      Permutations                    100.0%
    total:                                                          (statements)                    94.7%

If you have a default browser configured you can use the following: `go tool cover -html=count.out` to generate a "heat map" and see exactly how often each line of code is covered. (red means not at all ;)

- <https://blog.golang.org/cover>


### Subtests

Using the pattern of table driven tests improves the readability and extensibility of the "merge empty test" by applying "Don't Repeat Yourself" and removing the copy pasting of the driver function call.

    :::go
    package main
    
    import (
        "reflect"
        "testing"
    )
    
    var empty = []int{}
    
    func assertSlicesEqual(t *testing.T, expected []int, result []int) {
        if !reflect.DeepEqual(expected, result) {
            t.Error("\nExpected:", expected, "\nReceived: ", result)
        }
    }
    
    // defining the test structure separately and clear naming helps readability
    type slicesMergeTest struct {
        a        []int
        b        []int
        expected []int
    }
    
    func TestSlicesMergeEmpty(t *testing.T) {
    // alternative "anonymous struct" example 
    /* var testCases = [] struct {
           a        []int
           b        []int
           expected []int
       }{ */
    
        testCases := []slicesMergeTest {
            {a: empty, b: empty, expected: empty},
            {a: empty, b: nil, expected: empty},
            {a: nil, b: empty, expected: empty},
            {a: nil, b: nil, expected: empty},
        }
        
        // Without subtests
        // for _, tc := range testCases {
        // 	actual := SlicesMerge(tc.a, tc.b)
        // 	assertSlicesEqual(t, tc.expected, actual)
        // }
        
        for _, tc := range testCases {
            t.Run(fmt.Sprintf("%#v merged with %#v", tc.a, tc.b), func(t *testing.T) {
                actual := SlicesMerge(tc.a, tc.b)
                assertSlicesEqual(t, tc.expected, actual)
            })
        }
    }


> One variation with the "subtest" feature (which may apply more to benchmarks than straightforward unit tests) is not only that a fatal will not skip subsequent tests but that the output is more verbose

    === RUN   TestSlicesMergeEmpty
    --- PASS: TestSlicesMergeEmpty (0.00s)
    PASS

> With subtests...

    === RUN   TestSlicesMergeEmpty
    === RUN   TestSlicesMergeEmpty/[]int{}_merged_with_[]int{}
    === RUN   TestSlicesMergeEmpty/[]int{}_merged_with_[]int(nil)
    === RUN   TestSlicesMergeEmpty/[]int(nil)_merged_with_[]int{}
    === RUN   TestSlicesMergeEmpty/[]int(nil)_merged_with_[]int(nil)
    --- PASS: TestSlicesMergeEmpty (0.00s)
        --- PASS: TestSlicesMergeEmpty/[]int{}_merged_with_[]int{} (0.00s)
        --- PASS: TestSlicesMergeEmpty/[]int{}_merged_with_[]int(nil) (0.00s)
        --- PASS: TestSlicesMergeEmpty/[]int(nil)_merged_with_[]int{} (0.00s)
        --- PASS: TestSlicesMergeEmpty/[]int(nil)_merged_with_[]int(nil) (0.00s)
    PASS

> Making the "table" of inputs and outputs more obvious AND the output verbosity clearer seems like a small refinement but goes a long way to making production quality testing easier

#### Running a specific subtest

`go test -v -run=TestSlicesMergeEmpty/"nil"`

    --- PASS: TestSlicesMergeEmpty (0.00s)
        --- PASS: TestSlicesMergeEmpty/[]int{}_merged_with_[]int(nil) (0.00s)
        --- PASS: TestSlicesMergeEmpty/[]int(nil)_merged_with_[]int{} (0.00s)
        --- PASS: TestSlicesMergeEmpty/[]int(nil)_merged_with_[]int(nil) (0.00s)

> Yes! You can pattern match on the string from the subtest table and only run a subset of subtests (mindblown)

More info on the "table driven test" pattern:

- <https://blog.golang.org/subtests>
- <https://github.com/golang/go/wiki/TableDrivenTests>
- <http://dave.cheney.net/2013/06/09/writing-table-driven-tests-in-go>


## Benchmarking

Benchmarking is most useful if you're attempting to answer a question of two variations on how to implement something.

I suppose if you recorded every result and ran against exactly the same hardware you might be able to detect performance regressions, though I'd be worried about overly inconsistent/flaky results taking up way too much valuable time.

Inside of a _test.go file you can also write benchmark test functions, here is one of the classic questions of "concatenating strings in Go"

Here we compare the simplest concatenation of two strings and also the continued concatenation of many strings with either + or buffer.WriteString()

Create myconcat_test.go and execute the following with `go test -v -bench=.`

    :::go
    package main
    
    import (
        "bytes"
        "testing"
    )
    
    func MyConcatSimple(a string, b string) string {
        return a + b
    }
    
    func MyConcatSimpleLooped(a string, b string) string {
        for i := 0; i < 101; i++ {
            a += b
        }
        return a
    }
    
    func MyConcatBytesBuffer(a string, b string) string {
        var buffer bytes.Buffer
        buffer.WriteString(a)
        buffer.WriteString(b)
        return buffer.String()
    }
    
    func MyConcatBytesBufferLooped(a string, b string) string {
        var buffer bytes.Buffer
        buffer.WriteString(a)
        for i := 0; i < 101; i++ {
            buffer.WriteString(b)
        }
        return buffer.String()
    }
    
    func BenchmarkConcatSimple(b *testing.B) {
        for n := 0; n < b.N; n++ {
            MyConcatSimple("foo", "bar")
        }
    }
    
    func BenchmarkConcatSimpleLooped(b *testing.B) {
        for n := 0; n < b.N; n++ {
            MyConcatSimpleLooped("foo", "bar")
        }
    }
    
    func BenchmarkConcatBytesBuffer(b *testing.B) {
        for n := 0; n < b.N; n++ {
            MyConcatBytesBuffer("foo", "bar")
        }
    }
    
    func BenchmarkConcatBytesBufferLooped(b *testing.B) {
        for n := 0; n < b.N; n++ {
            MyConcatBytesBufferLooped("foo", "bar")
        }
    }

> The b.N is automatically filled in by Go until the benchmark runner is "satisfied with stability" though you can create a wrapper function for the code under test if you wish to attempt more control over iterations

> Remember that every benchmark is only valid against a specific set of hardware, operating system, libraries, etc. and with any changes (i.e. upgrade from Go 1.6 to 1.7) you may need to retest... unless you're just proving O(N) is better than O(N^2) ;)

Oh right, the results...

    BenchmarkConcatSimple-4                 30000000                40.1 ns/op
    BenchmarkConcatSimpleLooped-4             100000             20728 ns/op
    BenchmarkConcatBytesBuffer-4             5000000               373 ns/op
    BenchmarkConcatBytesBufferLooped-4        300000              7227 ns/op

> the iterations show that the simplest naive concatentation with + is very fast for a couple of small arguments (40 nanoseconds)

> BUT if appending many (100+) items together buffer.Write() is better

This example ignored all sorts of real world questions around how the strings are provided (i.e. a slice of strings might be better served by Join()) (or examine it's source code to see how they implement string concatenation!) , or memory consumption, etc.

- <http://dave.cheney.net/2013/06/30/how-to-write-benchmarks-in-go>
- <https://medium.com/hackintoshrao/daily-code-optimization-using-benchmarks-and-profiling-in-golang-gophercon-india-2016-talk-874c8b4dc3c5>
- <https://golang.org/pkg/strings/#Join>

#### Running specific benchmarks

`go test -v -run=NOMATCH -bench=BenchmarkConcatSimple`
> Since it is using the test runner the -run= regexp not matching allows you to skip any unit tests

> -bench= can take a regexp to match only a subset of benchmark tests

#### Go Benchmark with an expensive setup

If you have some setup (e.g. creating a slice with test data) you probably do not want it inside of the benchmark ;)

`go test -v -run=NOMATCH -bench=BenchmarkKey`

    :::go
    func BenchmarkKey(b *testing.B) {
        a := getData(100)
        b.ResetTimer()	
        for i := 0; i < b.N; i++ {
            problemKey(100, a)
        }
    }
    
    func getData(n int) []int {
        a := make([]int, n)
        for i := 0; i < n; i++ {
            a[i] = i
        }
        return a
     }
> the timer of the benchmark testing has been reset before the "real" load , note that the compiler is smart and this may not always be necessary

## Profiling

TODO:

- <https://medium.com/tjholowaychuk/profiling-golang-851db2d9ae24>
- <http://blog.ralch.com/tutorial/golang-performance-and-memory-analysis/>
- <http://dave.cheney.net/2013/07/07/introducing-profile-super-simple-profiling-for-go-programs>
- <https://blog.golang.org/profiling-go-programs>
- <https://golang.org/pkg/net/http/pprof/>
- <https://golang.org/pkg/runtime/pprof/>

## Go Fuzz Testing

Fuzz testing is furthering the principle of automation (and that computers are inherently better at some things than humans) to  have software discover edge cases for tests.

Basically the idea is to have software run over an extreme range or with randomness and then the edge cases that are discovered can be added into the test suite.  It has been used to enormously good effect on the Go standard library by Dmitry Vyukov.

One thing you start to see when attempting to apply it is that it really a tool for helping validate handling of a specific input.  It is not a magic wand to discover bugs. ;)

This kind of tool assisted exploratory testing is usually reserved for a more mature phase of a product (or in special use cases where there is high value in attempting to prove correctness).

    :::go
    func TestSlicesMergeRandom(t *testing.T) {
        f := fuzz.New()
        var randomSeed int
        f.Fuzz(&randomSeed)
        fmt.Println("random seed:", randomSeed)
        r := rand.New(rand.NewSource(int64(randomSeed)))

        xLength := r.Int() % 5
        yLength := r.Int() % 5
        fmt.Println(xLength, yLength)
        var x []int
        var y []int

        for i := 0; i < xLength; i++ {
            var r int
            f.Fuzz(&r)
            x = append(x, r)
        }
        for i := 0; i < yLength; i++ {
            var r int
            f.Fuzz(&r)
            y = append(y, r)
        }
        sort.Ints(x)
        sort.Ints(y)
        result := SlicesMerge(x, y)
        expected := append(x, y...)
        sort.Ints(expected)
        if !reflect.DeepEqual(expected, result) {
            t.Error("\nExpected:", expected, "\nReceived: ", result)
        }
    }

> Seeding randomness is part of how this gofuzz library is used; the Vyukov version actually produces output that must be parsed separately.

- <https://github.com/google/gofuzz>
- <https://github.com/dvyukov/go-fuzz>
- <https://blog.cloudflare.com/dns-parser-meet-go-fuzzer>
- <https://medium.com/@dgryski/go-fuzz-github-com-arolek-ase-3c74d5a3150c#>

- <https://golang.org/pkg/math/rand/>
- <https://golang.org/pkg/sort/>
