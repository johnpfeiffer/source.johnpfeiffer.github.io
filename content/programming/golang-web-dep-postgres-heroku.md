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
            fmt.Fprintf(w, "hi")
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

First download and install the Go dependency tool:

- <https://github.com/golang/dep>
- <https://devcenter.heroku.com/articles/go-apps-with-dep#build-configuration>
- <https://devcenter.heroku.com/articles/go-apps-with-dep#getting-started>


    cd DIRECTORY/OF/WEBAPP
    dep init
    go list -e .
    echo "[metadata.heroku]" >> Gopkg.toml
    echo "  root-package = \"`go list -e .`\"" >> Gopkg.toml
    git status ; git diff
    git add --all .
    git commit -m "initial web app and using go dep"
    git push

- Example simple Go dep configuration file <https://github.com/johnpfeiffer/web-go/blob/master/Gopkg.toml>

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
> This has created an empty Go application in heroku

Later on when deploying the application to heroku if you receive the following error: *No default language could be detected for this app*, it means you did not set the buildpack language yet...

*If you missed setting the buildpack language via CLI you can also use the WebUI after the app was already created <https://dashboard.heroku.com/apps/APPNAME/settings>*

- <https://devcenter.heroku.com/articles/buildpacks>

Another gotcha is if you have not configured a dependency manager (even without dependencies!) you will see this error *App not compatible with buildpack*.

### Travis-CI

- <https://docs.travis-ci.com/user/deployment/heroku/>

First you will need to have retrieved your auth token: `heroku auth:token`

You can connect the repository that was already created in Github to Travis via <https://travis-ci.org> , more specifically at <https://travis-ci.org/profile/USERNAME>

> you may need to "sync account" if you very recently created a repository , otherwise you will see this error: *repository not known to https://api.travis-ci.org/: USERNAME/REPONAME*

    :::bash
    docker run -it --rm ruby:alpine /bin/sh
    apk update
    apk add --no-cache build-base git
    gem install travis travis-lint
    travis help
> This docker example avoids installing ruby locally ;p

Inside of the docker container you will need (using "vi" ;) to create a dummy .travis.yml file with the content:

    deploy:
      provider: heroku
      api_key:
        secure: "YOUR ENCRYPTED API KEY"

You can then run the following command which will update the .travis.yml file with the real encrypted auth token.
`travis encrypt YOUR-HEROKU-TOKEN --add deploy.api_key -r USERNAME/REPONAME`

In your source code repository your real .travis.yml file will be:

    language: go
    script: go get && go test -v
    notifications:
      email: false
    
    deploy:
      provider: heroku
      api_key:
        secure: ABCD1234XYZLONGENCRYPTEDSTRING

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
> This small change to our previous *main.go* allows our default web handler (aka controller) to return html

*indextemplate.go*

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



## TestDrivenDesign and Gorilla Mux

Tests help us communicate. Libraries and Composition, not Frameworks and Magic.

- TODO: Go Web and JSON
- TODO: integrating heroku postgres , <https://devcenter.heroku.com/articles/getting-started-with-go#use-a-database>
- <https://github.com/johnpfeiffer/go-web-example>


## Miscellaneous

### Logs from Heroku
To see the logs from the web application running in heroku: `heroku logs --app APPNAME --tail`

### Environment Variables for Configuration

- <https://devcenter.heroku.com/articles/getting-started-with-go#define-config-vars>

### Custom Domains with Heroku
To use a custom domain name for your traffic <https://devcenter.heroku.com/articles/custom-domains>

### Downloading the source code from Heroku
To download the source code from a running Heroku application: `heroku git:clone --app APPNAME` <https://devcenter.heroku.com/articles/git-clone-heroku-app>


