Title: Go Programming Intro with VS Code and Arrays Slices Functions and Testing
Date: 2015-11-15 21:19
Tags: go, golang, vscode, testing, arrays, slices, binary search

[TOC]

Introducing the Go Programming Language (aka golang) basics, interactive sandbox with <http://play.golang.org>

## Prerequisites

Tooling is often essential to productivity.

### Download and install the go language compiler and tools

#### vim and Docker

Or alternatively just avoid the IDE and Environment and use vim and a docker container ;) <https://hub.docker.com/_/golang/>

### Installing and the Environment

<https://golang.org/dl/> and `cd /opt; tar xf go.tar.gz`

Instead of the ephemeral `export PATH=$PATH:/usr/local/go/bin` I prefer the persistent ~/.profile (or for all users /etc/profile though clearly /opt indicates a single user system ;)

    # Go Programming
    export GOROOT=/opt/go
    export PATH=$PATH:$GOROOT/bin
    export GOPATH=/opt/goprojects
    export PATH=$PATH:$GOPATH/bin
    
    source ~/.profile

> The last step gets you going without needing to reload your shell, full docs at <https://golang.org/doc/install>

**WARNING** be careful how you name your executables as the $GOPATH/bin will contain the names of the projects as binaries (so don't create a project or binary named bash!)


### Download and install an IDE

If you are used to larger projects then an IDE is quite helpful for colorization, auto completion, (right click or f12) goto definition, rename, build on save, auto formatting, etc.

Suprisingly one of the most popular and effective golang IDE combinations is: <https://code.visualstudio.com/Docs/?dv=linux64_deb>

    dpkg -i vscode-amd64.deb

To install <https://marketplace.visualstudio.com/items?itemName=lukehoban.Go> aka <https://github.com/Microsoft/vscode-go> you actually:

1. open Visual Studio Code
2. Control + P (Launches VS Code Quick Open)
3. `ext install Go` (capital G for "lukehoban")
4. restart when prompted
5. File -> Preferences -> Color Theme (Light Visual Studio ;)

> At this point you probably need to reboot to get VSCode to recognize the GOPATH correctly

In your shell where you setup the GOPATH run the following to get all of the analysis tools that "Go for Visual Studio Code" uses, though it's a lot easier to just use the IDE in the bottom right corner "Analysis Tools Missing"

To take advantage of those tools (like gofmt on save), in your workspace (GOPATH) there will be a .vscode directory with settings.json <https://code.visualstudio.com/docs/customization/userandworkspace>

    // Place your settings in this file to overwrite default and user settings.
    {
        "go.buildOnSave": true,
        "go.lintOnSave": true,
        "go.vetOnSave": true,
        "go.buildFlags": [],
        "go.lintFlags": [],
        "go.vetFlags": [],
        "go.coverOnSave": false,
        "go.useCodeSnippetsOnFunctionSuggest": false,
        "go.formatOnSave": true,
        "go.formatTool": "goreturns"
    }

> Just in case restart VSCode to recognize the updated settings

Unfortunately it is not quite simple to execute the code directly in VSCode <https://github.com/Microsoft/vscode-go/issues/21>

### Install or Build or Run

Because Go is a static language there is a compilation (and linking) phase where the source code is transformed into a binary.

#### Manual CLI compilation and installation and execution

The traditional command line method is:

    cd $GOPATH/path-to-your-project/PROJECTNAME
    go install
    $GOPATH/bin/PROJECTNAME

- <https://golang.org/doc/code.html#Command>
- <http://dave.cheney.net/2014/01/21/using-go-test-build-and-install>

A concrete example:

1. Compile with: `cd /opt/goprojects/src/github.com/johnpfeiffer/intro/ ; go install`
2. Execute with: `/opt/goprojects/bin/intro`

### Debugging with Delve

    go get github.com/derekparker/delve/cmd/dlv
    cd /opt/goprojects/src
    go install /derekparker/delve/cmd/dlv

The first time I attempted to do it manually:

    ls -ahl /opt/goprojects/bin/
    cd /opt/goprojects/src/github.com/johnpfeiffer/YOURPROJECT
    /opt/goprojects/bin/dlv  debug --headless --listen=:2345 --log

Now in the VSCode IDE open the project folder and create your helloworld.go source file and Control + S to save (and auto gofmt) and then press **F5** and it will connect to the Delve Debugger and display the output

#### Delve Debugging and running your application with F5 is automatic once installed correctly

1. The first time you run "Continue" with F5 on a file it will prompt you to setup your launch.json (and the IDE will open the default template for you)
2. Use the IDE to go back to your source .go file and press F5 again, this time since the .vscode subdirectory was created and the default delve launch.json file was created, it will just start in debug mode with the Debug Console output at the bottom


## Coding and Compiling

For VSCode IDE keyboard shortcuts: <https://code.visualstudio.com/docs/customization/keybindings>

### Comments Types Strings Slices For Loops

The main package it where the execution begins (aka "main" in c <https://en.wikipedia.org/wiki/Entry_point>)

Comments are either single line with double slashes or block comments <https://golang.org/doc/effective_go.html#commentary>

#### intro.go

    :::go
    package main
    
    import "fmt"
    
    /* https://golang.org/doc/effective_go.html#mixed-caps
       https://golang.org/ref/spec#Constants */
    const alphabetMax int = 26
    
    func main() {
    
    	// while
    	j := 0
    	for j < 4 {
    		fmt.Println(j)
    		j += 2
    	}
    	for i := 0; i < 4; i += 2 {
    		fmt.Println(i)
    	}
    	for {
    		fmt.Println("break or return exits an infinite loop")
    		break
    	}
    
    	// arrays are contiguous memory, fixed size and type
    	// initialized to capacity 5 with values inserted, alternatively just initialized to empty with: var a [5]string
    	a := [5]string{"a", "b", "c", "d", "e"}

    	// prefer Slices which are Reference Objects that wrap the underlying arrays
        // https://blog.golang.org/go-slices-usage-and-internals
        s := []string

    	for i := 0; i < len(a); i++ {
    		fmt.Println(i, a[i])
    	}
    	
    	// cleaner way of iterating over key and value
    	for k, v := range a {
    		fmt.Println(k, v)
    	}
       	fmt.Println(s)    // []
        s = a[:]
        fmt.Println(s)    // [a b c d e]
        s = a[2:]
        fmt.Println(s)    // [c d e]
    }


### arrays are contiguous memory and 4 bytes is normal

    :::go
    // int is usually the 4 byte int32 https://golang.org/ref/spec#Numeric_types
    b := [2]int{1, 2}
    // dereference the addresses that are holding the values 1 and 2
    fmt.Printf("%d %d\n", &b[0], &b[1])
    
    // rune is also int32
    c := [2]rune{'a', 'ä'}
    fmt.Printf("%d %d\n", &c[0], &c[1])

### fizzbuzz and switch

<https://golang.org/ref/spec#Switch_statements>

    :::go
	for i := 1; i < 16; i++ {
		// usually static case values and "switch i {" , note it will NOT fall through by default
		switch {
		case i%3 == 0 && i%5 == 0:
			fmt.Println("fizzbuzz")
		case i%3 == 0:
			fmt.Println("fizz")
		case i%5 == 0:
			fmt.Println("buzz")
		default:
			fmt.Println(i)
		}
	}

### time

    :::go
    import "time"
    // https://golang.org/pkg/time/#Now
    now := time.Now()
    fmt.Println("local:", now)
    fmt.Println(now.UnixNano()/1000000, "ms")
    fmt.Println("in UTC:", now.UTC().Format(time.UnixDate))


### Packages and String Reverse

When you modularize your code into packages then multiple programs can make use of DRY <https://en.wikipedia.org/wiki/Don%27t_repeat_yourself>

#### main

    :::go
    package main
    
    import (
    	"fmt"
    	"github.com/johnpfeiffer/mystringutil"
    )
    
    func main() {
    	fmt.Printf(stringutil.Reverse("!oG ,olleH"))
    }
    
#### package mystringutil with Reverse

    :::go
    // Package mystringutil contains utility functions for working with strings. "go build"
    package mystringutil
    
    // Reverse returns its argument string reversed rune-wise left to right.
    func Reverse(s string) string {
            r := []rune(s)
            for i, j := 0, len(r)-1; i < len(r)/2; i, j = i+1, j-1 {
                    r[i], r[j] = r[j], r[i]
            }
            return string(r)
    }
    


### palindrome and string conversion integer to ascii

Besides the main function for executing you will obviously create re-usable packages which will contain functions.

Here is the source code for a simple "is this string a palindrome" and "is this integer a palindrome" programs:

    :::go
    package main
    
    import (
    	"fmt"
    	"strconv"
    )
    
    func main() {
    	fmt.Println(isPalindrome("a"))
    	fmt.Println(isPalindrome("ala"))
    	fmt.Println(isPalindrome("noon"))
    	fmt.Println(isPalindrome("ab"))
    	fmt.Println(isPalindrome("racecar"))
    	fmt.Println(isPalindrome("abfooba"))
    
    	// slower and uses extra memory
    	fmt.Println(isPalindrome(strconv.Itoa(1991)))
    	fmt.Println(isPalindrome(strconv.Itoa(1981)))
    
    	// takes advantage of math (mindblown)
    	number := 9
    	reversed := reverseInteger(number)
    	fmt.Println(number, reversed)
    	fmt.Println(number, "is a palindrome: ", number == reversed)
    	number = 123
    	reversed = reverseInteger(number)
    	fmt.Println(number, reversed)
    	fmt.Println(number, "is a palindrome: ", number == reversed)
    	number = 121
    	reversed = reverseInteger(number)
    	fmt.Println(number, reversed)
    	fmt.Println(number, "is a palindrome: ", number == reversed)
    }
    
    func isPalindrome(word string) bool {
    	for index, value := range word {
    		oppositeIndex := len(word) - index - 1
    		opposite := rune(word[oppositeIndex])
    		fmt.Printf("%d %T %c compared to %d %c \n", index, value, value, oppositeIndex, opposite)
    		if index >= oppositeIndex {
    			break
    		}
    		if value != opposite {
    			return false
    		}
    
    	}
    	return true
    }
    
    func reverseInteger(x int) int {
    	reversed := 0
    	for ; x > 0; x /= 10 {
    		remainder := x % 10
    		reversed = (reversed * 10) + remainder
    		fmt.Println(remainder, x, reversed)
    	}
    	return reversed
    }
    
### Random Integers

    :::go
	// https://golang.org/pkg/crypto/rand/
	// https://golang.org/pkg/math/big/
	var max big.Int
	var myRandom *big.Int
	var err error
	max.SetUint64(10)
	myRandom, err = rand.Int(rand.Reader, &max)

	fmt.Println(*myRandom)
	fmt.Println(err)


### Binary Search

Using main and print is the poor man's Unit Testing ;)

    :::go
    package main
    
    import (
    	"bytes"
    	"fmt"
    )
    
    //todo pass by ref?
    func binarySearch(a []int, target, low, mid, high int) int {
    	fmt.Println("low =", low, "mid =", mid, "high =", high)
    	if a[mid] == target {
    		return mid
    	}
    	if mid >= high || mid <= low {
    		return -1
    	}
    
    	if a[mid] < target {
    		low = mid + 1
    	}
    	if a[mid] > target {
    		high = mid
    	}
    	mid = ((high - low) / 2) + low
    	return binarySearch(a, target, low, mid, high)
    }
    
    func main() {
    	a := []int{1, 4, 6, 8}
    	fmt.Println(a)
    	targets := []int{1, 4, 6, 8, 0, 3, 5, 7, 9}
    	for _, t := range targets {
    		result := binarySearch(a, t, 0, len(a)/2, len(a))
    		fmt.Println("found", t, "at location", result)
    	}
    
    }

### Efficient String append and replacement

<http://stackoverflow.com/questions/1760757/how-to-efficiently-concatenate-strings-in-go>

    :::go
    func myReplace(source string) string {
    	var b bytes.Buffer
    	for _, c := range source {
    		if c == ' ' {
    			b.WriteString("%20")
    		} else {
    			b.WriteString(string(c))
    		}
    	}
    	return b.String()
    }


### Testing with Go

- <https://golang.org/pkg/testing/>
- <http://nathanleclaire.com/blog/2015/10/10/interfaces-and-composition-for-effective-unit-testing-in-golang/>
- <https://cloud.google.com/appengine/docs/go/tools/localunittesting/#Go_Introducing_the_Go_testing_package>

### A simple web server

    :::go
    package main

    import (
        "fmt"
        "net/http"
    )

    func myHandler(w http.ResponseWriter, r *http.Request) {
        fmt.Fprintf(w, "hi")
    }

    func main() {
        http.HandleFunc("/", myHandler)
        http.ListenAndServe(":8080", nil)
    }


Verify with `curl localhost:8080`


#### Deploying a Go Web Application to Google AppEngine


First create an **app.yaml** file in your package

    application: MyApplicationName
    version: 1
    runtime: go
    api_version: go1
    
    handlers:
    - url: /.*
      script: _go_app


Second adapt your source code to the Google App Engine entrypoint:

    :::go
    package myapplicationname
    // package main

    import (
            "fmt"
            "net/http"
    )

    func myHandler(w http.ResponseWriter, r *http.Request) {
            fmt.Fprintf(w, "hi")
    }

    // The App Engine PaaS provides its own main() that handles the Listening and Serving ;)
    //func main() {
    func init() {
            http.HandleFunc("/", myHandler)
    //      http.ListenAndServe(":8080", nil)
    }


Assuming you have created the project with <https://console.cloud.google.com/> and received a unique application id...

A prerequisite is to use the SDK if you want to test it locally: <https://cloud.google.com/appengine/downloads#Google_App_Engine_SDK_for_Go>

    unzip go_appengine_sdk...zip
    /opt/go_appengine/goapp serve /path-to-project/MyProjectFolder/

      INFO     2016-06-02 06:30:27,493 devappserver2.py:769] Skipping SDK update check.
      INFO     2016-06-02 06:30:27,527 api_server.py:205] Starting API server at: http://localhost:38837
      INFO     2016-06-02 06:30:27,530 dispatcher.py:197] Starting module "default" running at: http://localhost:8080
      INFO     2016-06-02 06:30:27,531 admin_server.py:116] Starting admin server at: http://localhost:8000


#### To deploy to Google App Engine

    /opt/go_appengine/appcfg.py -A MyApplicationID update ./MyProjectFolder/

> View the version deployed and stats with <https://console.cloud.google.com/appengine/versions?project=MyApplicationId>

    curl http://MyApplicationId.appspot.com/

> A gotcha is future updates deployed need the app.yaml version to increment AND either use the Web UI to set the new "default" or...

    /opt/go_appengine/appcfg.py -A MyApplicationId set_default_version /MyProjectFolder


### HandlerFunc and Anonymous Functions and Closure

The decorator pattern Anonymous functions an

    :::go
    package main
    
    import (
    	"fmt"
    	"net/http"
    )
    
    /* using an anonymous function and closure to wrap the HandlerFunc
    https://golang.org/pkg/net/http/#HandlerFunc
    https://medium.com/@matryer/the-http-handlerfunc-wrapper-technique-in-golang-c60bf76e6124
    */
    func makeHandler(name string) http.HandlerFunc {
    	return func(w http.ResponseWriter, r *http.Request) {
    		// https://golang.org/src/net/http/request.go
    		fmt.Println("serving: ", r.URL.Path)
    		fmt.Fprintf(w, "<h1>%s</h1>", name)
    	}
    }
    
    func main() {
    	fmt.Println("starting...")
    	indexHandler := makeHandler("Index")
    	myHandler := makeHandler("John")
    	// https://golang.org/pkg/net/http/#HandleFunc , string, func(ResponseWriter, *Request)
    	http.HandleFunc("/", indexHandler)
    	http.HandleFunc("/john", myHandler)
    	http.ListenAndServe(":8080", nil)
    }
    

### More Info

- <https://tour.golang.org/basics/>
- <https://blog.joshsoftware.com/2014/03/12/learn-to-build-and-deploy-simple-go-web-apps-part-one/>
