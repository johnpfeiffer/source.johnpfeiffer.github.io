Title: React Javascript Intro
Date: 2024-08-25 12:34
Tags: react, javascript, js

[TOC]
The intent of this post is to help people build and understand simple reactive web applications

**2025 update**: due to the never-ending nature of tech breaking things - this post needed an update (goodbye Create React App)

<https://react.dev/blog/2025/02/14/sunsetting-create-react-app>


# Pre-Requisites
install node.js (which also includes `npm`) from <https://nodejs.org/en>

check if they are installed:
`node -v`
`npm -v`

## install the default react project
in a directory (probably a code repository)

 	:::bash
	npm create vite@latest my-app -- --template react
 	cd my-app
	npm install
	npm run dev
  
_(obsolete: npx create-react-app my-app)_

- - -
Essential folder structure (that is created by the framework with default files)

**my-app/**

```
	index.html	(this is the entrypoint, yes it's all just html and http ;)
  
	src/
		index.css      (this is for styles for the output - if you want things to look good)
		main.jsx       (connects the App to the starting index.html entrypoint)
		App.css
		App.jsx		(this is where you add code)
```
		
_(Remove the "vitals" phone home stats because privacy should be a default)_

The defacto web standard for the first document (for a web server) to return when no resource is specified is "index.html"

<https://en.wikipedia.org/wiki/HTML>

**INDEX.HTML**

	:::html
	<!DOCTYPE html>
	<html lang="en"><body>
	<noscript>You need to enable JavaScript to run this app.</noscript>
		<div id="root"></div>
		<script type="module" src="/src/main.jsx"></script>
	</body></html>


**MAIN.JSX**

	:::javascript
	// this wrapper is connecting the App to the root
	import React from 'react'
	import ReactDOM from 'react-dom/client'
	import './index.css';
	import App from './App.jsx'
	
	const rootElement = document.getElementById("root");
	const root = ReactDOM.createRoot(rootElement);
	root.render(
	  <React.StrictMode>
		<App />
	  </React.StrictMode>
	);


**APP.JSX**

	:::javascript
	// very simple app that switches the content displayed when the button is clicked
	import './App.css';
	import { useState } from 'react';
	
	const content = [
	  ["hello world", "more content on line 2"],
	  ["react.dev has tutorials and documentation"]
	 ];
	  
	 function App() {
	  const [activeContentIndex, activeContent] = useState(0);
	 
	  return (
	  	<div className="App">
      		<header className="App-header">
			</header>
			<div id="tabs">
			<button onClick={() => activeContent(0)}>Tab 1</button>
			<button onClick={() => activeContent(1)}>Tab 2</button>
			</div>
			<div id="tab-content">
				{content[activeContentIndex].map((line, i) => <p key={i}>{line}</p>)}
			</div>
		</div>
	);
	}
	
	export default App;

_A React component is a JavaScript function that returns JSX (looks like HTML but is not HTML)_

**/public** is a directory with image or binary files that are served directly
- - -

# Build and Deploy

A critical file created by the default app generator is `package.json` , it lists all your project dependencies and scripts

To build this for deployment to a place where browsers will retrieve it

`npm run build`

This framework compiles/reformats the code into a production bundle of files that can be uploaded to a server

the new directory `dist` contains the index.html and static files along with "minified" javascript and css

<https://vite.dev/guide/static-deploy.html>

