Title: React JavaScript Intro
Date: 2024-08-25 12:34
Tags: react, javascript, js

[TOC]

This post is to help people who are familiar with coding to build and understand simple reactive web applications.

**2025 update**: due to the never-ending nature of tech breaking things - this post needed an update (goodbye Create React App)

<https://react.dev/blog/2025/02/14/sunsetting-create-react-app>


# Pre-Requisites
install node.js (which also includes `npm`) from <https://nodejs.org/en>

check if they are installed:

`node -v`

`npm -v`

> Note that **nvm** is often used for managing multiple versions of NodeJS

*This is a practical tool given how frequently different projects end up with dependencies that require a specific version of NodeJS*

<https://www.nvmnode.com/>

## Use Vite to start a simple React project
in a directory (probably a code repository)

```shell
	npm create vite@latest my-app -- --template react
 	cd my-app
	npm install
	npm run dev
```

_(obsolete: npx create-react-app my-app)_

note that `npm run dev` starts a web server at http://localhost:5173

- - -
# Folder structure
Essential folder structure (that is created by the framework with default files)

**my-app/**

```text
	index.html	    (this is the entrypoint, yes it's all just html and http ;)

	src/
		main.jsx    (connects the App to the starting index.html entrypoint)
		App.jsx		(this is where you add code)
		index.css   (this is for styling the output)
		App.css
```

*Ignoring index.css and App.css as CascadingStyleSheets is a completely different topic*
		
**/public** is a directory with image or binary files that are served directly

## The MVP Files

**INDEX.HTML**

*The simplest beginning from decades ago that still powers the internet...*

"index.html" is the defacto web standard for the first document (for a web server) to return when no resource is specified.

<https://en.wikipedia.org/wiki/HTML> HyperText[Markup](https://en.wikipedia.org/wiki/Markup_language)Language

```html
	<!DOCTYPE html>
	<html lang="en"><body>
	<noscript>You need to enable JavaScript to run this app.</noscript>
		<div id="root"></div>
		<script type="module" src="/src/main.jsx"></script>
	</body></html>
```

> React is a structured way to have JavaScript produce the UI via code; not hand written HTML, not unstructured JavaScript files, not imperative modification of the DOM

**MAIN.JSX**

```jsx
	// this wrapper is connecting the App to the root
	import React from 'react';
	import ReactDOM from 'react-dom/client';
	import App from './App.jsx';
	
	const rootElement = document.getElementById("root");
	const root = ReactDOM.createRoot(rootElement);
	root.render(
	  <React.StrictMode>
		<App />
	  </React.StrictMode>
	);
```

**APP.JSX**

```jsx
	// very simple app that switches the content displayed when the button is clicked
	import { useState } from 'react';

	const content = [
		["hello world", "more content on line 2"],
		["react.dev has tutorials and documentation"]
	];

	function App() {
		const [myValue, setMyValue] = useState(0);
		return (
			<div>
				<header>the header area</header>
				<div id="tabs">
					<button onClick={() => setMyValue(0)}>Tab 1</button>
					<button onClick={() => setMyValue(1)}>Tab 2</button>
				</div>
				<div id="tab-content">
					{content[myValue].map((line, i) => <p key={i}>{line}</p>)}
				</div>
			</div>
		);

	}

	export default App;
```

### Components

A React component is a JavaScript function that returns JSX (looks like but is not HTML).

*React component names must always start with a capital letter, while HTML tags must be lowercase.*

Modifying the above **App.jsx** to add a react component MyButton inside the existing App function:

```jsx

				</div>
				<MyButton mytext="just text"/>
			</div>
		);

		function MyButton({ mytext }) {
			return (
				<button>
					this button does nothing - {mytext}
				</button>
			);
		}

	}

	export default App;
```

The MyButton function has a mytext argument so callers can pass in a parameter.

Or in React terminology: the MyButton component has a property aka prop, "mytext". MyButton is in the tree where it is a child of the parent "App".

The curly brackets `{ }` escape back into JavaScript - any expression inside gets evaluated.


- - -

# Build and Deploy

A critical file created by the default app generation is `package.json`, it lists all your project dependencies and scripts (including "how to build")

The build framework reads your package.json to understand which tools to run, in this case `vite` compiles/reformats the code into a production bundle of files that can be uploaded to a server

The command to "build", or convert all of these files into a single bundle that is easily deployed:

`npm run build`

The new output directory `dist` contains the index.html and static files along with "minified" JavaScript and css

<https://vite.dev/guide/static-deploy.html>


- - -

# Code Architecture

React is mostly three things:

1.	Components: functions that render UI
2.	State: data that changes over time and causes re-rendering
3.	Props: data passed from parent to child

> The visible interface is a function of the current data

App.jsx -> main.jsx (mostly empty) -> index.html (mostly empty) -> [DOM](https://en.wikipedia.org/wiki/Document_Object_Model)

Questions to ask when deciding "what goes where and how":

- what data exists?
- who owns the data?
- who reads the data?
- who/what changes the data?

When data needs to be passed to multiple components it should live in their "parent".

`App` is the highest level shared state, control plane, and composition area.

*Avoid making App a-very-long-file monolith =(*

Tiny components can be a button or search box - a reusable piece of the UI.

Yet "component" can also be a larger grouping to organize complexity.

Splitting components by responsibility and domain helps ensure future bug fixes or feature extensibility be simple in a cohesive manner - not a ripple effect on every file or a ball of mud untangling.

- Do `components/Search/` with its own state and sub-components
- Avoid `components/buttons/` collecting every button in the app

- - -

# TypeScript

A particularly important quality for reliability and accuracy in Production is detecting errors as early as possible. TypeScript adds static typing to JavaScript which allows the compiler to catch issues like invalid props, impossible state shapes, and mismatched return values during development and in CI.

The official templates include the React + TypeScript starter:

<https://vite.dev/guide/>

```javascript
	npm create vite@latest my-app -- --template react-ts
 	cd my-app
	npm install
	npm run dev
```

Many files are almost exactly the same (index.html, main.tsx)

There are also some notable differences:

- Many files are now **".ts/.tsx"** or TypeScript rather than ".js/.jsx" JavaScript: vite.config.ts , main.tsx, App.tsx
- There's a new tsconfig.json file
- **package.json** has a special build command: `"build": "tsc -b && vite build",` that runs TypeScript checking before Vite bundles the app


<https://react.dev/learn/typescript>

## App tsx

Replacing the default template's App.tsx code with the following code mirrors the previous JSX example:

**APP.TSX**

```tsx
	// very simple app that switches the content displayed when the button is clicked
	import { useState } from 'react'

	const content: string[][] = [
		["hello world", "more content on line 2"],
		["react.dev has tutorials and documentation"]
	]

	function App(): JSX.Element {
		const [myValue, setMyValue] = useState<number>(0)
		return (
			<div>
				<header>the header area</header>
				<div id="tabs">
					<button onClick={() => setMyValue(0)}>Tab 1</button>
					<button onClick={() => setMyValue(1)}>Tab 2</button>
				</div>
				<div id="tab-content">
					{content[myValue].map((line: string, i: number) => <p key={i}>{line}</p>)}
				</div>
			</div>
		)
	}

	export default App
```

The notable changes are adding explicit types like **string[][] , JSX.Element , number , string**

Being overly explicit encodes intent and lets the automated systems help you ensure correctness rather than depending on inferring the specification.

`const [myValue, setMyValue] = useState('O')` - should it be a capital O?

Usually the most important places to have explicit clarity are boundaries like APIs and interfaces. And of course tests help too ;)

*and a nod to the modern no semi-colons movement*

# State and Hooks

Another piece of leverage that React provides is tracking state: the information stored between renders.

**Hooks** are functions that let components use React features like state, effects, refs, and context.

In the above example the hook `useState()` returns the matched pair: currentValue and setterFunction.

*(Another bit of JS cleverness is the one-liner where the value passed into useState becomes the initial value assigned to currentValue)*


`<button onClick={() => setMyValue(0)}>Tab 1</button>`

When state changes, React renders the component again so the UI reflects the new value.

A more complex example where Types, State, and Hook all work together:

```tsx
type Status = "idle" | "loading" | "success" | "error";

const [status, setStatus] = useState<Status>("idle");
```

## Mounting and useEffect

A component usually goes through a lifecycle of three phases:

- **Mount**: component is added to the page - renders and appears in the DOM for the first time
- **Update**: state or props change, so React re-renders the component again
- **Unmount**: component is removed from the page (DOM),  i.e. user navigates away, conditional hides it, etc.

*remount = old thing gone: old DOM nodes are removed, new DOM nodes are created, logically local component state is reset*


**useEffect** can allow you to mediate the interactions of state and updates, often to synchronize with an external dependency.

useEffect requires a "setup function" that initializes and also optionally returns a "cleanup function", and it requires a list of dependencies that are used inside the setup function.

*For the dependencies if you pass [], the effect runs after the component is added to the page and cleans up when the component is removed. If you omit the dependency array entirely, the effect runs after every render.*

```tsx
import { useState, useEffect } from 'react';

type Position = { x: number; y: number }

export default function App(): JSX.Element {
  const [position, setPosition] = useState<Position>({ x: 0, y: 0 })

  useEffect(() => {
    function handleMove(event: PointerEvent) {
      setPosition({ x: event.clientX, y: event.clientY })
    }
    window.addEventListener('pointermove', handleMove)
    return () => {
      window.removeEventListener('pointermove', handleMove)
    }
  }, [])

  return (
	<div>
    	<p>X: {position.x}</p>
		<p>Y: {position.y}</p>
	</div>

  )
}

```

- PointerEvent is a browser-native type for inputs
- window.addEventListener is the standard browser API for subscribing to events

So these are external inputs that our component now tracks (and updates with latest coordinates).

<https://react.dev/reference/react/useEffect>


Or if you want to see it all put together...

```tsx
// very simple app that switches the content displayed when the button is clicked
import { useState, useEffect } from 'react'

const content: string[][] = [
  ["hello world", "more content on line 2"],
  ["react.dev has tutorials and documentation"]
]

type Position = { x: number; y: number }

export default function App(): JSX.Element {
  const [myValue, setMyValue] = useState<number>(0)

  const [position, setPosition] = useState<Position>({ x: 0, y: 0 })

  useEffect(() => {
    function handleMove(event: PointerEvent) {
      setPosition({ x: event.clientX, y: event.clientY })
    }
    window.addEventListener('pointermove', handleMove)
    return () => {
      window.removeEventListener('pointermove', handleMove)
    }
  }, [])

  return (
    <div>
      <header>the header area</header>
      <div id="tabs">
        <button onClick={() => setMyValue(0)}>Tab 1</button>
        <button onClick={() => setMyValue(1)}>Tab 2</button>
      </div>
      <div id="tab-content">
        {content[myValue].map((line: string, i: number) => <p key={i}>{line}</p>)}
      </div>

      <div>
        <p>X: {position.x}</p>
        <p>Y: {position.y}</p>
      </div>

    </div>
  )
}
```
