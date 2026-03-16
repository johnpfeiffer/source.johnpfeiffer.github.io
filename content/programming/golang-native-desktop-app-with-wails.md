Title: Building a desktop app with Golang and Wails
Date: 2025-04-06 10:10
Tags: go, golang, react, javascript, js, typescript, desktop

[TOC]

tldr: a Golang native desktop app using Wails (Go backend + React frontend = single binary)

# Why this tech stack and why a desktop app?

Desktop apps provide privacy for the persistence layer, and bypass the "where is it hosted" challenges.

This is a simple and practical way to leverage some great backend + frontend technologies.

*If you need a more basic react intro see my previous post <https://blog.john-pfeiffer.com/react-javascript-intro/>*

The key: Go methods with exported (capitalized) names get auto generated as JavaScript/TypeScript bindings. You call Go functions from React as if they were local async functions.

## Why Wails

Wails uses the operating system's native webview (WebKit on macOS, WebView2 on Windows, WebKitGTK on Linux) so the resulting binary is ~10MB.

As a comparison to a very popular technology, electron bundles an entire Chromium browser into your app - which is why a "hello world" Electron app is ~150MB and idles at 100MB+ of RAM.

```text
┌───────────────────────────────────────────────────────────┐
│  WAILS APPLICATION                                        │
│                                                           │
│   Go Backend              React Frontend                  │
│   ┌───────────┐           ┌──────────────────┐            │
│   │ app.go    │◄─────────►│ App.tsx          │            │
│   │ (structs  │  bindings │ (components,     │            │
│   │  & methods│  ───────► │  hooks, UI)      │            │
│   │  & stdlib)│           │                  │            │
│   └───────────┘           └──────────────────┘            │
│         │                        │                        │
│         └──────────┬──────────────┘                         │
│                    ▼                                        │
│         ┌────────────────────┐                             │
│         │  Native WebView    │                             │
│         │  (WebKit on macOS) │                              │
│         └────────────────────┘                              │
│                    │                                        │
│                    ▼                                        │
│            Single Binary (~10MB)                            │
└─────────────────────────────────────────────────────────────┘
```

## Why golang

Golang is a remarkably performant language but it still automatically handles memory management (with garbage collection)

Golang builds to a single binary


# Pre-requisites

*the assumption here is MacOS...*

Golang: https://go.dev/doc/install

- `brew install golang`
- `which go; go version`
- `echo 'export PATH="$PATH:$(go env GOPATH)/bin"' >> ~/.zshrc`

*because "GOPATH/bin" is the default destination for `go install` - now making tools runnable*

NPM: https://nodejs.org/en/download/
- `brew install node`
- `which npm; npm --version; node --version` 

## Installing Wails
- Wails framework: https://wails.io/docs/gettingstarted/installation/

`go install github.com/wailsapp/wails/v2/cmd/wails@latest`

`ls $(go env GOPATH)/bin`

`wails version`

**Troubleshooting Wails**

`wails doctor`

This checks Go version, node/npm, and platform-specific dependencies (on macOS you need Xcode command line tools)

# Simplest start with Wails

`wails init -l` 
> list the different types of wails default project layouts

```text
Plain HTML/JS/CSS              plain
React + Vite                   react
React + Vite (Typescript)      react-ts
Svelte + Vite                  svelte
Vanilla + Vite                 vanilla
Vue + Vite                     vue
```

*for security reasons it is simplest to avoid 3rd party templates unless you've vetted them thoroughly*

I'll use "React + Vite (Typescript)": `wails init -n myapp -t react-ts`

Run the interactive developer view of the Application (it's responsive to rebuilding for changes): `wails dev`

```shell
Executing: go mod tidy
  • Generating bindings: Done.
  • Installing frontend dependencies: Done.
  • Compiling frontend: Done.
  ...
```

In about 10 seconds you have your example native desktop app running locally.

## Privacy checks in the configuration files

`wails.json` contains the application name - and your **email address**, so do not send that to a git public repo unless you're ready for it

Also, the name "myapp" will show up in a bunch of places so if you change/update the name, look for

```shell
grep -r 'chat-explorer' .
	./go.mod
	./wails.json
	./frontend/index.html
	./app.go
	/main.go
```


- - -

# Explaining the File Structure

```text
myapp/
├── build/
│   ├── appicon.png
│   ├── darwin/
│   │   ├── Info.plist
│   │   └── Info.dev.plist
│   └── windows/
├── frontend/
│   ├── src/
│   │   ├── App.tsx
│   │   ├── main.tsx
│   │   ├── App.css
│   │   └── style.css
│   ├── wailsjs/
│   │   ├── go/main/App.ts    <- auto-generated bindings
│   │   └── runtime/
│   ├── index.html
│   ├── package.json
│   └── tsconfig.json
├── app.go                    <- your Go application logic
├── main.go                   <- entrypoint
├── go.mod
├── go.sum
└── wails.json
```

There are two halves to understand: the Go backend and the React frontend.

## The Golang Backend

**main.go** is the entrypoint for starting the application


```golang
package main

import (
    "embed"
    "github.com/wailsapp/wails/v2"
    "github.com/wailsapp/wails/v2/pkg/options"
    "github.com/wailsapp/wails/v2/pkg/options/assetserver"
)

//go:embed all:frontend/dist
var assets embed.FS

func main() {
    app := NewApp()

    err := wails.Run(&options.App{
        Title:  "myapp",
        Width:  1024,
        Height: 768,
        AssetServer: &assetserver.Options{
            Assets: assets,
        },
        BackgroundColour: &options.RGBA{R: 27, G: 38, B: 54, A: 1},
        OnStartup:        app.startup,
        Bind: []interface{}{
            app,
        },
    })
    if err != nil {
        println("Error:", err.Error())
    }
}
```

`//go:embed all:frontend/dist` is a directive doing something clever: embedding the entire compiled frontend into the Go binary at build time, no separate files to distribute!


`Bind: []interface{}{ app,` is the connection between "Go Exported Methods" and the Javascript/React

**app.go** is the place for application logic (usually just high level, using /models or other places to get all of the details)

```golang
package main

import "context"

type App struct {
    ctx context.Context
}

func NewApp() *App {
    return &App{}
}

func (a *App) startup(ctx context.Context) {
    a.ctx = ctx
}

func (a *App) Greet(name string) string {
    return "Hello " + name + ", welcome to Wails!"
}
```

The magic: every exported method on a bound struct (in this case "App") automatically gets a TypeScript binding generated in frontend/wailsjs/go/main/App.ts


## The React Frontend

Your usual **frontend/index.html** has `<script src="./src/main.tsx" type="module"></script>`

**frontend/src/main.tsx** is the entrypoint for starting the application - nothing surprising here:

```typescript
import React from 'react'
import {createRoot} from 'react-dom/client'
import './style.css'
import App from './App'

const container = document.getElementById('root')

const root = createRoot(container!)

root.render(
    <React.StrictMode>
        <App/>
    </React.StrictMode>
)
```


**frontend/src/App.tsx** is the bridge to the backend Golang Greet function:

```typescript
import { useState } from 'react';
import { Greet } from '../wailsjs/go/main/App';

function App() {
    const [name, setName] = useState('');
    const [result, setResult] = useState('');

    const greet = () => Greet(name).then(setResult);

    return (
        <div>
            <input onChange={(e) => setName(e.target.value)} />
            <button onClick={greet}>Greet</button>
            <p>{result}</p>
        </div>
    );
}

export default App;
```

> Note that the Greet function is a Promise, the call to the backend is async


Now explore adding your own function that returns a map like `func (a *App) GetCurrentTime() map[string]string {`

In the frontend you'd use it with

```typescript
import { GetCurrentTime } from '../wailsjs/go/main/App';

// later in a component...
const [info, setInfo] = useState<Record<string, string>>({});
useEffect(() => {
    GetCurrentTime().then(setInfo);
}, []);
```



# Build and Distribute

`wails build`

There are more instructions you'd need to follow about all the details of Windows, MacOS, etc.

# Conclusion

These are well known concepts of frontend (react) and backend (golang) so you can focus on your domain problems and features.

*Using these standard technologies also makes it very easy to leverage AI/LLMs to write the code*

Stable building blocks and not re-inventing the wheel allows you to ship faster (and deliver value!)
