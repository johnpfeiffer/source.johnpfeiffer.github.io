Title: Golang JSON is challenging
Date: 2016-12-30 20:34
Tags: go, golang, json, interfaces

[TOC]

Parsing JSON can be a relatively simple subject covered early in other programming languages (i.e. JavaScript ;)

JSON is a really popular way to persist or transmit data, especially for APIs.  So it is really common to need to use it and yet...

JSON can be surprisingly difficult in Go because even though it is built into the language it depends already understanding a few other somewhat advanced topics.  And the challenge can be compounded by the Go philosophy of "We Did Not Put It In the Language Do It Yourself".

## A quick overview of JSON

JSON (I never hear humans actually say the full thing: JavaScript Object Notation , though "Jason" does get annoyed) is a way to format data structures as text and it is the modern alternative to XML.

- <https://en.wikipedia.org/wiki/JSON>
- <http://json.org/>

There is some fuzziness about Numbers and other definitions but its beauty is definitely simplicity.

## Why does Go in JSON seem (unnecessarily) advanced or challenging?

1. Go with JSON requires defining/using structs for objects.  This upfront cost certainly fits the "statically compiled" model ;)  But Javascript or Python magically "just make an object" (or dictionary) which has fields/values that are very accessible.

It is actually pretty common that we might not know or want to define the full (nested?) object structures we've received (as if the JSON format was for portability of data from a service outside of your control), but we're forced to figure something out...

2. To generically parse an object from JSON (i.e. you do not know the full structure) you must use the "empty interface" (the most generic object), and Interfaces are more advanced than simply defining structs.

3. Inferring or attempting to lazily load JSON (i.e. a mixed list of different objects - since there isn't a slice of mixed types in Go!) requires Reflection which is a relatively advanced topic for a beginning programmer.

4. Static typing is great, except for when you're reading from JSON and you're not sure which type you should really use and you probably just want it to work simply. This impedance mismatch is natural when moving from a portable data format to a specific language and application, but it doesn't reduce the cursing.

5. To really have the Go compiler figure out the translation between JSON to object requires "hinting" which helps with compiling Reflection magic, but starts to complicate your structs (and interfaces!)

6. Nested Structs (fields) are the answer to Nested JSON, but then you have to really figure out how many (and lists with multiple types of objects!) and how deep you expect any nesting you'll receive. (Or just give in to your recursive desires.)

7. Pointers.  They are efficient.  Since JSON parsing can be memory intensive you will end up using them... in Nested Structs... with Interfaces... and Reflection Hints... (and since Pointers are messy and confusing there will be bugs).

`associative array < struct/object < interface < pointers < reflection`
> a completely made up ordering of complexity, arrays being the least hard to grok

- <http://research.swtch.com/interfaces>
- <https://blog.golang.org/laws-of-reflection>

To summarize, it is really common to get some json from somewhere from someone else and want to just peek at one field, update another field, add a key and value, and save the json.

And that kind of dynamic behavior isn't inherently easy in Go. =[


## Example code of Marshalling and Unmarshalling JSON with Go

- <https://blog.golang.org/json-and-go>

    :::go
    package main
    
    import (
            "encoding/json"
            "fmt"
            "io"
            "io/ioutil"
            "log"
            "os"
    )
    
    func logIfError(err error) {
            if err != nil {
                    log.Fatal(err)
            }
    }
    
    // readFile is a convenience function to read a whole file at once, LOL similar to ioutil.ReadFile()
    func readFile(f *os.File) {
            var data = make([]byte, 1024)
            totalBytes := 0
            for {
                    count, err := f.Read(data)
                    // https://golang.org/pkg/io/ , EOF is an expected error condition
                    if err != io.EOF {
                            logIfError(err)
                    }
                    // TODO: 0 bytes could be returned when not an EOF
                    if count == 0 {
                            break
                    }
                    totalBytes += count
                    fmt.Printf("Read %d bytes: \n%s\n", count, string(data))
            }
            fmt.Printf("Read %d total bytes from the file\n", totalBytes)
    }
    
    // genericParsing is an example of the empty interface https://blog.golang.org/json-and-go
    // https://en.wikipedia.org/wiki/JSON
    func genericParsing(data []byte) {
            var f interface{}
            err := json.Unmarshal(data, &f)
            logIfError(err)
    
            // https://golang.org/doc/effective_go.html#interface_conversions
            m := f.(map[string]interface{})
            fmt.Println("\ngeneric json parsing")
            for k, v := range m {
                    switch vv := v.(type) {
                    case string:
                            fmt.Println("  ", k, "is string:", vv)
                    case int:
                            fmt.Println("  ", k, "is int:", vv)
                    case bool:
                            fmt.Println("  ", k, "is bool:", vv)
                    case []interface{}:
                            fmt.Println("  ", k, "is an array:")
                            for _, u := range vv {
                                    fmt.Println("    ", u)
                            }
                    default:
                            fmt.Println("  ", k, "is of a type I don't know how to handle")
                            fmt.Printf("  but I could have checked another way and found %v is a %T\n", v, v)
                            // JSONNumber https://golang.org/pkg/encoding/json/#Decoder.UseNumber
                            // http://json.org/ no floats so hinting is appreciated
                    }
            }
    }

    // Assuming top level keys are strings, i.e. NOT [] , https://gobyexample.com/json
    func rootStringsOnlyParsing(data []byte) map[string]interface{} {
            // A map of string to any type https://blog.golang.org/laws-of-reflection , http://research.swtch.com/interfaces
            var datmap map[string]interface{}
            e := json.Unmarshal(data, &datmap)
            logIfError(e)
            fmt.Println("\nKeys are Strings in a Map:", datmap)
            return datmap
    }
    
    // ExampleSimpleObject must be exported to parse correctly , the fields order here is used by json.Marshal output
    type ExampleSimpleObject struct {
            Age  int    `json:"age"`
            Name string `json:"name"`
    }
    
    // ExampleComplexObject is the magic of auto parsing, if your data never gets corrupted...
    // helpful understanding of Go and JSON nesting https://eager.io/blog/go-and-json/
    // hints are very powerful leveraging of Reflection that Go core libraries use for JSON
    type ExampleComplexObject struct {
            ArrayOfObjects []ExampleSimpleObject `json:"jsonArrayOfObjects,omitempty"`
            ArrayOfStrings []string              `json:"jsonArrayOfStrings"`
            JSONBoolean    bool                  `json:"jsonBoolean"`
            JSONNumber     int                   `json:"jsonNumber"`
            JSONString     string                `json:"jsonString, omitempty"`
            // jsonArrayOfNumbers is not defined and so is not included in the parsed object
    }
    
    // autoUnmarshal shows Go structs making parsing JSON look easy https://golang.org/pkg/encoding/json/#example_Unmarshal
    func autoUnmarshal(data []byte) ExampleComplexObject {
            var ex ExampleComplexObject
            err := json.Unmarshal(data, &ex)
            logIfError(err)
            fmt.Printf("Auto Unmarshal: %+v \n", ex)
            return ex
    }
    
    // writeJSONFile demonstrates the power of interfaces for shared functionality
    func writeJSONFile(name string, thing interface{}) {
            theJSON, err := json.MarshalIndent(thing, "", "  ")
            logIfError(err)
            err = ioutil.WriteFile(name, theJSON, 0644)
            logIfError(err)
            // See the omitted fields with: diff --ignore-all-space types.json output.json
    }
    
    func main() {
            // https://golang.org/pkg/os/
            myFile, ferr := os.Open("types.json")
            logIfError(ferr)
            readFile(myFile)
    
            // hint: read a file and return a slice of bytes: https://golang.org/pkg/io/ioutil/#ReadFile
            data, _ := ioutil.ReadFile("types.json")
    
            genericParsing(data)
            datamap := rootStringsOnlyParsing(data)
            // modifying or adding to a JSON file can be tricky
            datamap["injectedKey"] = "injected value"
            writeJSONFile("dataMapModified.json", datamap)
    
            auto := autoUnmarshal(data)
            writeJSONFile("autoUnmarshalOmits.json", auto)
            fmt.Println("done")
    }


- <https://gobyexample.com/json>
- <https://eager.io/blog/go-and-json/>
- <https://golang.org/doc/effective_go.html#interface_conversions>
- <http://attilaolah.eu/2014/09/10/json-and-struct-composition-in-go/>
- <https://blog.gopheracademy.com/advent-2016/advanced-encoding-decoding/>

## Common JSON gotchas with Go

1. The data structures need to be exported, otherwise you'll only end up with an empty JSON object

    :::go
    type Oops struct {
        Name string `json:"name"`
        i int    `json:"timestamp"`
    }
> The i int field will not be Marshaled and will therefore not exist in the JSON object

- <https://play.golang.org/p/ukkjLQnSSq>
- <https://golang.org/pkg/encoding/json/#example_Unmarshal>

2. Types are strict in Go.  JSON is unclear about "Number".  Golang will assume float64 without any hints.  Use hints, or reflection and type assertions and a magic wand...

- <https://golang.org/pkg/encoding/json/#Decoder.UseNumber>

3. Marshal() returns a slice of bytes which is not a string.  so string()

- <https://golang.org/pkg/encoding/json/#Marshal>

4. "The argument to Unmarshal must be a non-nil pointer", <https://golang.org/pkg/encoding/json/#InvalidUnmarshalError>

## A more "real world" code example of parsing JSON with Go

I wanted to import the bookmarks from Chrome but I hadn't exported them.  I wrote this utility to parse the default chrome bookmarks json file that I did have:

- <https://bitbucket.org/johnpfeiffer/bookmarks/src>
