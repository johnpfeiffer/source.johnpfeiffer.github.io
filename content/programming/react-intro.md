Title: React Javascript Intro
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

> React is a structured way to have javascript produce the UI via code; not hand written HTML, not unstructured javascript files, not imperative modification of the DOM

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

The curly brackets `{ }` escape back into Javascript - any expression inside gets evaluated.

`useState()` returns the a matched pair: currentValue and setterFunction.

*(ironically in the one-liner JS cleverness the value passed into useState becomes the initial value assigned to currentValue)*

One magical piece of React is that it tracks the state for you. =]


- - -

# Build and Deploy

A critical file created by the default app generation is `package.json`, it lists all your project dependencies and scripts (including "how to build")

The build framework reads your package.json to understand which tools to run, in this case `vite` compiles/reformats the code into a production bundle of files that can be uploaded to a server

The command to "build", or convert all of these files into a single bundle that is easily deployed:

`npm run build`

The new output directory `dist` contains the index.html and static files along with "minified" javascript and css

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

`App.tsx` is the highest level shared state, control plane, and composition area.

*Avoid making App.tsx a-very-long-file monolith =(*

Tiny components can be a button or search box - a reusable piece of the UI.

Yet "component" can also be a larger grouping to organize complexity.

Splitting components by responsibility and domain helps ensure future bug fixes or feature extensibility be simple in a cohesive manner - not a ripple effect on every file or a ball of mud untangling.

- Do `components/Search/` with its own state and sub-components
- Avoid `components/buttons/` collecting every button in the app



