Title: React Javascript Intro
Date: 2024-08-25 12:34
Tags: react, javascript, js

[TOC]

install node.js and npm from <https://nodejs.org/en>

check if they are installed:
`node -v`
`npm -v`

in a directory (probably a code repository)

 	:::bash
	npx create-react-app my-app
 	cd my-app
  	npm start
  
_(sometimes you have to run npm install after installing new modules)_

- - -
Essential folder structure (that is created by the framework with default files)

**my-app/**

```
	public/
		index.html	(this is the entrypoint, yes it's all just html and http ;)
  
	src/
		index.css
		index.js
		App.css
		App.js	(this is where you code)
```
		
_(Remove the "vitals" phone home stats)_

INDEXJS

	:::javascript
	// this wrapper is connecting the App to the root
	
	import React from 'react';
	import ReactDOM from 'react-dom/client';
	import './index.css';
	import App from './App';
	
	const rootElement = document.getElementById("root");
	const root = ReactDOM.createRoot(rootElement);
	root.render(
	  <React.StrictMode>
		<App />
	</React.StrictMode>
	);


APPJS

	:::javascript
	// very simple app with content selected by a button
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

- - -
This framework compiles/reformats the code into a production bundle of files that can be uploaded to a server

(JSX is not html nor javascript, minification, and package.json has the many many dependencies ;)

`npm run build`


