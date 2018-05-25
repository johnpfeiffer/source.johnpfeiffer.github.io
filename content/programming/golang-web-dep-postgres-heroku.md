Title: Go Web Development and Templates with Heroku
Date: 2018-05-01 20:37
Tags: go, golang, web, gorilla mux, http, template, heroku, postgres

[TOC]

## Prerequisites

- Please create a new version controlled source code repository using Github or Bitbucket or ?.
- Have Golang installed
- Download and install the official Go dependency tool "dep", <https://golang.github.io/dep/docs/installation.html>


## A simple http server

Your source repository currently only needs a single file: **main.go**

    :::go
    package main
    
    import (
            "fmt"
            "log"
            "net/http"
            "os"
    )
    
    func myHandler(w http.ResponseWriter, r *http.Request) {
            w.Write([]byte("hi"))
    }
    
    func main() {
            port := getEnvOrDefault("PORT", "8080")
            log.Println("Listening on port", port)
            http.HandleFunc("/", myHandler)
            http.ListenAndServe(":"+port, nil)
    }
    
    func getEnvOrDefault(key, defaultValue string) string {
            result := defaultValue
            val, ok := os.LookupEnv(key)
            if ok {
                    result = val
            }
            return result
    }
> another example of a trivial web server using only the standard library

Verify it runs locally with: `go run main.go`
> your browser should see "hi" in http://localhost:8080 and use "control + c" to cancel and quit the command line web server application

While previous examples used Google App Engine  <https://blog.john-pfeiffer.com/go-programming-intro-with-vs-code-and-arrays-slices-functions-and-testing/#a-simple-web-server>, here we will leverage Heroku for deploying our web application.

## Go Dependency Management

First download and install the Go dependency tool: <https://github.com/golang/dep>

    :::bash
    cd DIRECTORY/OF/WEBAPP
    dep init
    go list -e .
    echo "[metadata.heroku]" >> Gopkg.toml
    echo "  root-package = \"`go list -e .`\"" >> Gopkg.toml
    git status ; git diff
    git add --all .
    git commit -m "initial web app and using go dep"
    git push

- An example simple Go dep configuration file <https://github.com/johnpfeiffer/web-go/blob/master/Gopkg.toml>
- Further heroku metadata config options: <https://devcenter.heroku.com/articles/go-apps-with-dep#build-configuration>
- Similar heroku instructions on dep: <https://devcenter.heroku.com/articles/go-apps-with-dep#getting-started>


## Deploying to Heroku from Github via Travis-CI

### Heroku Prerequisites
1. Download and install the heroku CLI <https://devcenter.heroku.com/articles/getting-started-with-go#set-up>
1. `cd /opt ; wget https://cli-assets.heroku.com/branches/stable/heroku-linux-amd64.tar.gz`
1. `tar xf heroku-linux-amd64.tar.gz`
1. `/opt/heroku/bin/heroku --version ; /opt/heroku/bin/heroku --help`
1. `/opt/heroku/bin/heroku login`  *this will prompt for your email and password and store the credentials in ~/.netrc*

> For extra security consider using heroku CLI inside of an ephemeral docker container or a script that removes the credentials after each usage

*These instructions will now assume heroku "just works", i.e. `alias heroku='/opt/heroku/bin/heroku'`*

### Configuring the Application with Heroku

    :::bash
    cd DIRECTORY/OF/WEBAPP
    heroku help
    heroku create APPNAME --buildpack heroku/go
    heroku status
> This has created an empty Go application in Heroku

Later on when deploying the application to heroku if you receive the following error: *No default language could be detected for this app*, it means you did not set the buildpack language yet...

*If you missed setting the buildpack language via CLI you can also use the WebUI after the app was already created:*

-  <https://dashboard.heroku.com/apps/APPNAME/settings>
- <https://devcenter.heroku.com/articles/buildpacks>

Another gotcha is if you have not configured a dependency manager (even without dependencies!) you will see this error *App not compatible with buildpack*.

### Travis-CI

- <https://docs.travis-ci.com/user/deployment/heroku/>

First you will need to have retrieved your auth token: `heroku auth:token`

You can connect the repository that was already created in Github to Travis via <https://travis-ci.org> , more specifically at <https://travis-ci.org/profile/USERNAME>

> you may need to "sync account" if you very recently created a repository , otherwise you will see this error: *repository not known to https://api.travis-ci.org/: USERNAME/REPONAME*

    :::bash
    sudo docker run -it --rm --volume /absolute/path/repo:/opt/repo --volume /opt/heroku:/opt/heroku ruby:alpine /bin/sh
    apk update
    apk add --no-cache build-base git
    gem install travis travis-lint
    travis help
> This docker example avoids installing ruby (or travis) locally ;p

`cd /opt/repo ; touch .travis.yml ; travis setup heroku`

    /opt/web-go # travis setup heroku
    Heroku API token: ************************************
    Heroku application name: |web-go|
    Deploy only from GITHUBUSERNAME/web-go? |yes| yes
    Encrypt API key? |yes| yes

> This simple CLI wizard prompts for the Heroku auth token and populates the .travis.yml with the encrypted value


*If you want to do it manually you will need (using "vi" ;) to create a dummy .travis.yml file with the content:*

    deploy:
      provider: heroku
      api_key:
        secure: "YOUR ENCRYPTED API KEY"

You can then run the following command which will update the .travis.yml file with the real encrypted auth token.
`travis encrypt YOUR-HEROKU-TOKEN --add deploy.api_key -r GITHUBUSERNAME/REPONAME`
> You may get prompted to login if you use the incorrect USERNAME


In your source code repository your more complete .travis.yml file will be:

    language: go
    script: go get && go test -v
    notifications:
      email: false
    
    deploy:
      provider: heroku
      api_key:
        secure: ABCD1234XYZLONGENCRYPTEDSTRING

An interesting alternative to github and travis is bitbucket: <https://confluence.atlassian.com/bitbucket/deploy-to-heroku-872013667.html>

### Test It

Now a browser that hits the Heroku URL will see "hi" , <https://web-go.herokuapp.com/>

## Templates for Content

Separating out the static html content from dynamic and business logic parts of the application is a key way to remain modular.
Templates built into the Go standard library can provide output that is safe from code injection.


    :::go
    var indexTemplate = GetIndexTemplate()
    
    func myHandler(w http.ResponseWriter, r *http.Request) {
        indexTemplate.Execute(w, NoData{})
    }
> These small changes (var indexTemplate and indexTemplate.Execute) to the previous **main.go** allows the default web handler (aka controller) to return html

**indextemplate.go**

    :::go
    package main
    
    import "html/template"
    
    // NoData is an empty struct as I do not pass anything into the template
    type NoData struct{}
    
    // GetIndexTemplate returns the index.html template https://golang.org/pkg/html/template/#Template
    func GetIndexTemplate() *template.Template {
        var indexTemplate = template.Must(template.New("index").Parse(`<html><head><style type="text/css">
    body{
      font-size: 1.9em;
    }
    </style></head><body>hi</body></html>
    `))
        return indexTemplate
    }
> The function just returns the rendered template; since it is only called once in main it is not inefficient, and Must will panic if the template has an error

`go run main.go indextemplate.go` allows you to test it locally

- <https://golang.org/pkg/html/template/>

### Passing Variables to a Template

Dynamic, data driven web sites emphasize the power of software to create tables that nobody wants to write by hand.

Building on the previous two examples (main.go, indextemplate.go) we now have a variation that passes data to the template.

**hexcolors.go**

    :::go
    package main
    
    import (
        "fmt"
        "html/template"
        "net/http"
    )
    
    // HexColors wraps a list of colors as hexadecimal strings
    type HexColors struct {
        Colors []string
    }
    
    // GetHexTemplate returns the parsed file as a template object
    func GetHexTemplate() *template.Template {
        return template.Must(template.ParseFiles("hexcolorstemplate.html"))
    }
    
    func hexController(w http.ResponseWriter, r *http.Request) {
        colors := []string{}
        for i := 255; i <= 16711680; i = i * 256 {
            s := fmt.Sprintf("%06X", i)
            colors = append(colors, s)
        }
        data := HexColors{colors}
        hexTemplate.Execute(w, data)
    }
> A handler/controller that generates hex color data

**hexcolorstemplate.html**

    :::html
    <table>
      {{range .Colors}}
      <tr><td>{{.}}</td><td style="background-color: {{.}}; ">__</td></tr>
      {{end}}
    </table>
> range iterates and creates a table row for each color , (the html and body is elided, see the previous example)

For the full implementation see the web-go code example: <https://github.com/johnpfeiffer/web-go/commit/c8636ee4f54ff95d4a804a152954874f5c23b682>

`go run main.go indextemplate.go hexcolors.go` allows you to test it locally, *note that you do not have to pass the html template as a parameter*

More info:

- <https://golang.org/pkg/html/template/#Template.ParseFiles>
- <https://blog.gopheracademy.com/advent-2017/using-go-templates/>

### HTML Template Blocks as Reusable Components

Besides dynamic data and tables for "do not repeat yourself" there are also structural components that can be deduplicated.
Changes in a base html or css template (or common component definition) can therefore reliably be applied to a large number of files.

Jinja2 is famous in Python for making it easier to work with websites, here are two different helpful mechanisms in Go:

1. Use the keyword "define" to create a fragment that can be explicitly included
2. Use the keyword "block" to create a default value that can be overridden
> the keyword "template" loads a template that has been created by a "define"


**indextemplate.go**

    :::go
    ...
    func GetIndexTemplate() *template.Template {
        indexTemplate := template.Must(template.ParseFiles("base.tmpl", "index.html"))
        return indexTemplate
    }
> This replaces the previous examples hardcoded html with a default base.tmpl that is then overridden by the "define" block in the index.html file, **order matters**!

**base.tmpl**

    :::html
    <html><head>
    <style type="text/css">
    {{block "style" .}}
    body{
      font-family: "Georgia";
      font-size: 1.9em;
    }
    {{end}}
    </style>
    </head>
    <body>
    {{block "content" .}}
    {{end}}
    </body></html>
> The HTML in base.tmpl has a "block" that provides a default style, content is an empty "block", *(clearly you can define variations of bases templates)*

**index.html**

    :::html
    {{define "content"}}
    hi , try <a href="/hexcolors">hexcolors</a>
    {{end}}
> The tiny index file heavily leverages the default base template and uses "define" to only override the content block

`go run main.go indextemplate.go hexcolors.go` allows you to test it locally, *you do not pass the .tmpl nor .html template files as parameters*

Further illustration by extending the templates usage a little further:

**hexcolors.go**

    :::go
    func GetHexTemplate() *template.Template {
        return template.Must(template.ParseFiles("base.tmpl", "components.tmpl", "hexcolorstemplate.html"))
    }
> the template files must exist in the relative path and build in order

**components.tmpl**

    :::html
    {{define "tablestyle"}}
      table, th, td {
        border: 2px solid black;
        font-size: 2.5em;
      }
    {{end}}
> defining a specific fragment that can be used anywhere

**hexcolorstemplate.html**

    :::html
    {{define "style"}}
    {{template "tablestyle" .}}
    {{end}}
    
    {{define "content"}}
      <table>
        {{range .Colors}}
        <tr><td>{{.}}</td><td style="background-color: {{.}}; ">__</td></tr>
        {{end}}
      </table>
    {{end}}
> the most complex example: the base template content is overridden with a table that gets data at runtime

> the style definition overrides the base template default style ; it actually gets populated by loading the tablestyle fragment definition

`go run main.go indextemplate.go hexcolors.go` allows you to test it locally, *you do not pass the .tmpl nor .html template files as parameters*
> 2 .tmpl files, 2 .html files, 3 .go files

Full source code for this example: <https://github.com/johnpfeiffer/web-go/commit/b6da397f89c8a6955a30e665ff1aa99be989e5cb>

For further info and advanced features like cloning:

- <https://github.com/golang/example/tree/master/template>
- <https://golang.org/pkg/html/template/#Template.Clone>

## TestDrivenDesign and Gorilla Mux

> Tests communicate. Use libraries and composition, not frameworks and magic

Rather than re-invent the wheel it is useful to leverage well designed libraries to reduce bugs (and repetitive boilerplate code).

Gorilla "mux" is a great idiomatic Go library for multi-plexing and routing. Designed to be modular to prefer composition we can also choose to leverage the Logging handler.

Finally adding a bit of JSON and very concisely you have built a high performing API server.


For the full featured source code with tests: **<https://github.com/johnpfeiffer/go-web-example>**

References:

- <https://github.com/gorilla/mux> in action <https://github.com/johnpfeiffer/go-web-example/blob/master/router.go> *(with dependency injection for database testability)*
- <https://github.com/johnpfeiffer/time-go/blob/master/main.go> leverages <https://github.com/gorilla/handlers#example>
- <https://github.com/johnpfeiffer/go-web-example/blob/master/controller_test.go> has both unit and integration test examples

- TODO: integrating heroku postgres , <https://devcenter.heroku.com/articles/getting-started-with-go#use-a-database>

## Miscellaneous


### How to return specific HTTP Response types

*Note these code snippets are the Handler function only, you should provide your own HTTP listener and multi-plexer*

    :::go
    func headonly(w http.ResponseWriter, r *http.Request) {
        w.Header().Set("Allow", "HEAD, GET")
        w.WriteHeader(200)
    }

- <https://play.golang.org/p/GCfxTLdLGYn> example returning the HTTP Header where clearly the default status code is 200
- <https://www.w3.org/Protocols/rfc2616/rfc2616-sec14.html#sec14.7>

`curl --silent --write-out "%{http_code}" localhost:8080`

    :::go
    func httperror(w http.ResponseWriter, r *http.Request) {
        http.Error(w, "Internal Server Error", http.StatusInternalServerError)
        return
        // without the return statement execution would continue
    }
> The http library understands that unexpected errors do occur but make sure to return so as to not continue executing code

- <https://play.golang.org/p/FyB7FwVp-ZB> example showing why the return statement is so important
- <https://en.wikipedia.org/wiki/List_of_HTTP_status_codes>
- <https://www.w3.org/Protocols/rfc2616/rfc2616-sec10.html>
- <https://curl.haxx.se/docs/manpage.html>

Serving binary files...

    :::go
    func getfile(w http.ResponseWriter, r *http.Request) {
        fp := path.Join("images", "example.png")
        http.ServeFile(w, r, fp)
    }

- <https://play.golang.org/p/G9zQ0SmzjP_K> example writing, reading, and serving a file
- <https://golang.org/pkg/net/http/#ServeFile>
- <https://golang.org/pkg/path/filepath/#Clean> for sanitizing user input for loading file paths


An example http server inside the Go playground: <https://play.golang.org/p/B-aZuQOdFtB>


### Logs from Heroku

To see the logs from the web application running in heroku: `heroku logs --app APPNAME --tail`


### Environment Variables for Configuration

- <https://devcenter.heroku.com/articles/getting-started-with-go#define-config-vars>

### Custom Domains with Heroku
To use a custom domain name for your traffic <https://devcenter.heroku.com/articles/custom-domains>

### Downloading the source code from Heroku
To download the source code from a running Heroku application: `heroku git:clone --app APPNAME` <https://devcenter.heroku.com/articles/git-clone-heroku-app>


