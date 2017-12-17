Title: Golang Buffalo Tutorial To Create A Web Site With Authentication
Date: 2017-12-02 19:44
Tags: go, golang, web, buffalo, authentication, sso, saml

[TOC]

Go's considerable tooling makes it a very productive and performant static language. Besides being ideal for developing APIs (goroutines!) it can then be convenient to also write the Web UI in Go.

Although the standard library allows for writing a Go based website with templates and maximum flexibility, what if you want a quick start with "batteries included"?

> Code generation makes it easy to get started but all future customization depends on the developer, this is not a CMS =p

## Buffalo Installation and Prerequisites

*Assuming the Go dev environment is already setup...*

`go get -u -v github.com/gobuffalo/buffalo/buffalo`

`buffalo new example`

`sudo docker run --rm -it --publish 0.0.0.0:5432:5432 --name pg -e POSTGRES_PASSWORD=postgres postgres:alpine`
> this will make the username and password match the default database.yml that buffalo generates...

cat database.yml

    :::yaml
    development:
      dialect: postgres
      database: example_development
      user: postgres
      password: postgres
      host: 127.0.0.1
      pool: 5
    
    test:
      url: {{envOr "TEST_DATABASE_URL" "postgres://postgres:postgres@127.0.0.1:5432/example_test?sslmode=disable"}}
    
    production:
      url: {{envOr "DATABASE_URL" "postgres://postgres:postgres@127.0.0.1:5432/example_production?sslmode=disable"}}


`buffalo db create --all`
> the buffalo framework will create all the necessary databases and tables

*(you can also `buffalo db drop --all` or `buffalo db drop --env test` to remove all or just one db)*

references:

- <https://hub.docker.com/_/postgres/>
- <https://gobuffalo.io/docs/db>

It is worth reading about the convention of how Buffalo lays out the directories and code <https://gobuffalo.io/docs/directory-structure>

## Start Developing with a Resource Generator

`buffalo dev`

(Or use the following syntax for a non default port: `PORT=3001 buffalo dev`)

`curl localhost:3000`
> Yup a default web page is routed and served

    :::bash
    buffalo generate resource users name email title:nulls.Text
    buffalo db migrate

Resulting output...

    :::text
    --> actions/users.go
    --> actions/users_test.go
    --> locales/users.en-us.yaml
    --> templates/users/_form.html
    --> templates/users/edit.html
    --> templates/users/index.html
    --> templates/users/new.html
    --> templates/users/show.html
    --> buffalo db g model user name email title:nulls.Text
    v3.41.1
    
    --> models/user.go
    --> models/user_test.go
    --> goimports -w actions/actions_test.go actions/app.go actions/home.go actions/home_test.go actions/render.go actions/users.go actions/users_test.go grifts/db.go grifts/init.go main.go models/models.go models/models_test.go models/user.go models/user_test.go
    > migrations/20171203042126_create_users.up.fizz
    > migrations/20171203042126_create_users.down.fizz
    --> goimports -w actions/actions_test.go actions/app.go actions/home.go actions/home_test.go actions/render.go actions/users.go actions/users_test.go grifts/db.go grifts/init.go main.go models/models.go models/models_test.go models/user.go models/user_test.go
> The code generator is very helpful, especially after the database tables are updated with the migrate command


`curl localhost:3000`
> The list of REST resources now includes all the usual HTTP methods

`curl localhost:3000/users`
> The GET endpoint lists all of the existing users (in the database) and has a button to create a new user

Now you can use a web browser to play with the Web UI

You can also query the database

    sudo docker run -it --rm --link pg:postgres postgres:alpine psql --help
    sudo docker run -it --rm --link pg:postgres postgres:alpine psql --host postgres --username postgres
        \list
        \connect example_development
        \dt+
        \d+ users
        select * from users;

## Avoiding the Frontend

Because javascript moves so quickly (and breaks things) it is easier to skip these steps and focus on the backend.

    # maybe skip these (and all the accompanying dependencies) to avoid suckiness
    sudo apt-get install -y npm
    sudo npm cache clean -f
    sudo npm install -g n
    npm --version
    node --version
    npm install
> npm installs the authrecipe dependencies but first use npm in order to install nodejs via the "n" helper

Without these the javascript assets or other things that were supposed to make the forms look pretty are not available but everything still works.

## Authentication

One of the first building blocks of any decent site is authentication.  Luckily there are a couple of packages that make basic and SSO authentication easier.

### Basic Authentication with the Database

To just use an example (leverage the Buffalo author's in-progress tutorial ;)

    sudo docker run --rm -it --publish 0.0.0.0:5432:5432 --name pg -e POSTGRES_PASSWORD=postgres postgres:alpine
    git clone https://github.com/gobuffalo/authrecipe
    cd authrecipe
    go get
    buffalo db create --all
    buffalo db migrate
    buffalo dev

> that is the minimum to get up and runnning...


With a browser you can "sign in" or "register" (create a new user with a password)

TODO: more work to port over how to create secure endpoints with a "CheckAuth" middleware...

### Authentication using an External Identity Provider

For instructions on how to have users authenticate and secure resources with identity providers like Github, Facebook, Google, etc.


    sudo docker run --rm -it --publish 0.0.0.0:5432:5432 --name pg -e POSTGRES_PASSWORD=postgres postgres:alpine
    go get -u -v github.com/gobuffalo/buffalo/buffalo
    go get buffalo-goth
    buffalo new example
    buffalo generate goth-auth bitbucket

In order to set up the Bitbucket OAuth credentials:
*Log into bitbucket -> from your user profile (avatar) dropdown choose "bitbucket settings" -> click on OAuth (on the left) -> Add consumer*

CallbackURL (for development): http://127.0.0.1:3000/auth/bitbucket
Permissions: account email

Now you have a KEY and SECRET

- <https://confluence.atlassian.com/bitbucket/oauth-on-bitbucket-cloud-238027431.html>
- <https://blog.gobuffalo.io/buffalo-tutorial-create-a-site-with-github-auth-629582e2763e>
- <https://github.com/markbates/goth>

`BITBUCKET_KEY=foobar BITBUCKET_SECRET=barfoo buffalo dev`

