Title: React with Material-UI and Google SSO
Date: 2024-09-07 12:34
Tags: react, javascript, js, material-ui, sso, oauth

[TOC]

tldr: React + Vite + MUI + simple Google sign-in for rapid building

React is almost a defacto standard for responsive frontend applications, so it can be helpful to layer on a few more "standard choices" to simplify building apps for production.

*if you need a more basic react intro see my previous post <https://blog.john-pfeiffer.com/react-javascript-intro/>*

# History of Style

As HTML took over the world, the need became obvious for separating out the "styling" of the presentation and content. Thus CSS was created, though it took awhile to become a fully adopted and usable standard (due to interests that would have preferred a private single browser definition and control).

<https://en.wikipedia.org/wiki/CSS>



ascii diagram:
```text
┌─────────────────────────────────────────────────────────────┐
│  SOURCE CODE FILES (what you write)                         │
│                                                             │
│   index.html          style.css                             │
│   ┌───────────┐       ┌──────────────────┐                  │
│   │ <h1>      │       │ h1 {             │                  │
│   │ <p>       │       │   color: blue;   │                  │
│   │ <button>  │       │ }                │                  │
│   └───────────┘       └──────────────────┘                  │
│         │                     │                             │
│         └──────────┬──────────┘                             │
│                    ▼                                        │
│              ┌───────────┐                                  │
│              │  Browser  │                                  │
│              └─────┬─────┘                                  │
│                    ▼                                        │
│   ┌─────────────────────────────────────────────────────┐   │
│   │  DOM (Document Object Model) - what the browser     │   │
│   │  builds in memory, combining structure + style      │   │
│   │                                                     │   │
│   │  document                                           │   │
│   │    └── html                                         │   │
│   │          └── body                                   │   │
│   │                ├── h1 (color: blue)                 │   │
│   │                ├── p                                │   │
│   │                └── button                           │   │
│   └─────────────────────────────────────────────────────┘   │
│                    │                                        │
│                    ▼                                        │
│            What you see on screen                           │
└─────────────────────────────────────────────────────────────┘
```

As an application grows, or if you are not keen on customizing every detail of the style, it can become overwhelming managing a lot of CSS files (and which setting overrides which thing).

## Material UI for Styling

Material UI (MUI) provides pre-built components that look decent out of the box and handle responsive design, accessibility, and theming.

It is a framework that generates both HTML and CSS for you - so it is simple, but opinionated.

To add Material UI dependencies to an existing React project:

```bash
npm install @mui/material @emotion/react @emotion/styled
```
<https://mui.com/material-ui/getting-started/>

<details>
<summary>example package.json</summary>
```json
	{
	  "name": "material-ui-example",
	  "private": true,
	  "version": "1.0.0",
	  "type": "module",
	  "scripts": {
	    "dev": "vite",
	    "build": "vite build",
	    "preview": "vite preview"
	  },
	  "dependencies": {
	    "@emotion/react": "^11.14.0",
	    "@emotion/styled": "^11.14.1",
	    "@mui/material": "^7.3.6",
	    "react": "^18.2.0",
	    "react-dom": "^18.2.0",
	    "react-router-dom": "^6.20.0"
	  },
	  "devDependencies": {
	    "@types/react": "^18.2.0",
	    "@types/react-dom": "^18.2.0",
	    "@vitejs/plugin-react": "^4.2.0",
	    "vite": "^7.1.3"
	  }
	}
```
</details>



### A simple React and MUI code example


**App.jsx**

```javascript
import { useState } from 'react';
import { Button, Box, Typography } from '@mui/material';

const content = [
  ["hello world", "more content on line 2"],
  ["github.com/mui has more info"]
];

function App() {
	const [activeContentIndex, setActiveContentIndex] = useState(0);

	return (
		<Box sx={{ p: 2 }}>
			<Box sx={{ mb: 2 }}>
				<Button onClick={() => setActiveContentIndex(0)}>View 1</Button>
				<Button onClick={() => setActiveContentIndex(1)}>View 2</Button>
			</Box>
			<div>
				{content[activeContentIndex].map((line, i) => (
					<Typography key={i} paragraph>{line}</Typography>
				))}
			</div>
		</Box>
	);
}

export default App;
```

- Box is a Material-UI generic wrapper: a `<div>` that accepts the sx property
- sx is a Material-UI shorthand for a property
- - p = padding, all sides, 2 x 8px = 16px
- - m = margin-bottom, 2 x 8px = 16px
- Button has Material Design ripple effect, hover states, and theming
- Typography applies Material Design font family, sizes, and spacing and renders as `<p>` by default


> There is no longer `App.css` and `index.css` since MUI is handling all the styling.

Thus your React framework code is now React + Material-UI, effectively a "Domain Specific Language" that quickly builds and renders frontend apps.

---

# Google Single Sign On

There are quite a few options for security, and identity (followed by authentication and authorization), and if you attempt to write it all yourself you can inadvertantly create a security issue.

One of the most popular Identity Providers to leverage is Google (due to gmail and youtube and large consumer reach).

For simple apps where your users will already have a Google Account, here is an easy way to have them verify their identity with Google and then share their email address with your application.

This allows for a "frontend only" app to have personalization, and is an important pre-requisite when added to a backend.

## Create a Google OAuth Client

For an existing (or new) **Google Cloud Project**, start the flow with the OAuth Consent
> Requests user consent so your app can access the user's data

1. Create https://console.cloud.google.com/auth/overview/create
2. fill out the questionnaire about the Application and intended use (starting with Internal or Test users is simplest)
3. fill in contact email address, and "terms and conditions"
4. "OAuth configuration created"
5. Create  OAuth client (button)
6. Application type: web application
7. Add `http://localhost:5173` to Authorized JavaScript origins (for local dev)
- if you know it already you can add the domain where your production React App runs (i.e. https://yourusername.github.io/)
8. Create (button)
9. Copy the Client ID - this is what you put in your environment variables or code

i.e. really-long-random-numbers-and-characters.apps.googleusercontent.com

*Note that this client ID is a public facing configuration value (ends up in JS code visible in the browser dev tools)*


## Environment Variable

Using an Environment variable allows setting a different value for Development, Staging, and Production.

Create the file `.env` in your project root with the following in it:

```
VITE_GOOGLE_CLIENT_ID=your-client-id-here.apps.googleusercontent.com
```

*(Also make sure you add `.env` to your `.gitignore` ;)*

Make sure you also set the value in your build process (or via integration with a hosting provider like AWS Amplify or Cloudflare ) that creates the final bundle 

### Load the Google Identity Services Script

**index.html**

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>My SSO App</title>
  <script src="https://accounts.google.com/gsi/client" async defer></script>
</head>
<body>
  <noscript>You need to enable JavaScript to run this app.</noscript>
  <div id="root"></div>
  <script type="module" src="/src/main.jsx"></script>
</body>
</html>
```

## Google Sign-In Component

**GoogleSignIn.jsx**

```javascript
import { useEffect, useRef, useState } from "react";

export default function GoogleSignIn({ onAuth }) {
  const [gsiReady, setGsiReady] = useState(false);
  const [authStatus, setAuthStatus] = useState(null);
  const googleButtonRef = useRef(null);
  const renderedRef = useRef(false);

  useEffect(() => {
    const clientId = import.meta.env.VITE_GOOGLE_CLIENT_ID;
    if (!clientId) {
      setAuthStatus({ ok: false, message: "Missing VITE_GOOGLE_CLIENT_ID" });
      return;
    }

    const handleCredentialResponse = (response) => {
      setAuthStatus({ ok: true, token: response.credential });
      if (onAuth) onAuth(response.credential);
    };

    const tryRender = () => {
      const g = window.google;
      if (!g?.accounts?.id || !googleButtonRef.current) {
        requestAnimationFrame(tryRender);
        return;
      }

      setGsiReady(true);

      // Prevent double-render (React 18 StrictMode calls useEffect twice)
      if (renderedRef.current) return;
      renderedRef.current = true;

      g.accounts.id.initialize({
        client_id: clientId,
        callback: handleCredentialResponse,
      });

      googleButtonRef.current.innerHTML = "";

      g.accounts.id.renderButton(googleButtonRef.current, {
        theme: "outline",
        size: "large",
        text: "signin_with",
      });
    };

    tryRender();
  }, [onAuth]);

  return (
    <div>
      <div ref={googleButtonRef} />
      {!gsiReady && <div>Loading Google Sign-In...</div>}
      {authStatus?.ok === false && <div style={{color: 'red'}}>{authStatus.message}</div>}
    </div>
  );
}
```

### Using the Sign-In Component

**App.jsx**

```javascript
import { useState } from 'react';
import { Container, Paper, Typography } from '@mui/material';
import GoogleSignIn from './GoogleSignIn';

function App() {
  const [user, setUser] = useState(null);

  const handleAuth = (credential) => {
    // The credential is a JWT - decode the payload to get user info
    const payload = JSON.parse(atob(credential.split('.')[1]));
    setUser(payload);
  };

  return (
    <Container maxWidth="sm" sx={{ mt: 4 }}>
      <Paper elevation={2} sx={{ p: 3 }}>
        {user ? (
          <div>
            <Typography variant="h6">Welcome, {user.name}</Typography>
            <Typography color="text.secondary">{user.email}</Typography>
          </div>
        ) : (
          <GoogleSignIn onAuth={handleAuth} />
        )}
      </Paper>
    </Container>
  );
}

export default App;
```

The JWT payload from Google includes: `email`, `name`, `picture`, `sub` (unique user ID), and expiration info.

---

# Listing all the files and a diagram

Final folder structure:

```
my-app/
    .env                 (VITE_GOOGLE_CLIENT_ID=...)
    .gitignore           (include .env)
    index.html           (includes gsi script)
    package.json
    src/
        main.jsx
        App.jsx
        GoogleSignIn.jsx
```

*For deployment, remember to add your production domain to the Google OAuth credentials Authorized JavaScript origins.*



```text
┌─────────────────────────────────────────────────────────────────────┐
│  GOOGLE SSO (Client-Side Only)                                      │
│                                                                     │
│                                                                     │
│   ┌──────────┐                              ┌──────────────────┐    │
│   │  Browser │                              │  Google Servers  │    │
│   └────┬─────┘                              └────────┬─────────┘    │
│        │                                             │              │
│        │  1. Page loads GSI script                   │              │
│        │────────────────────────────────────────────>│              │
│        │<────────────────────────────────────────────│              │
│        │                                             │              │
│        │  2. User clicks "Sign in with Google"       │              │
│        │────────────────────────────────────────────>│              │
│        │                                             │              │
│        │         ┌─────────────────────┐             │              │
│        │         │  Google login popup │             │              │
│        │         │  - enter email      │             │              │
│        │         │  - enter password   │             │              │
│        │         │  - consent screen   │             │              │
│        │         └─────────────────────┘             │              │
│        │                                             │              │
│        │  3. Google returns JWT credential           │              │
│        │<────────────────────────────────────────────│              │
│        │                                             │              │
│        │                                                            │
│        ▼                                                            │
│   ┌─────────────────────────────────────────┐                       │
│   │  JWT Payload (decoded in browser by javascript)                 │
│   │                                         │                       │
│   │  {                                      │                       │
│   │    "sub": "1234567890",  ← unique ID    │                       │
│   │    "email": "user@gmail.com",           │                       │
│   │    "name": "John Smith",                │                       │
│   │    "picture": "https://...",            │                       │
│   │    "exp": 1234567890                    │                       │
│   │  }                                      │                       │
│   └─────────────────────────────────────────┘                       │
│                                                                     │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

## Important Caveats

This all depends on trusting the javascript provided by google and their servers - they are responsible for the complexities of passwords, 2-factor-authentication, etc. 

This post uses Google Identity Services to get an ID token directly in the browser (no redirect URI required).

If you use "OAuth authorization code flow", you must configure redirect URIs and handle the code exchange on a backend.

Importantly: if you have any backend/API you should send the Google ID token to the backend and have code to truly verify it (signature + issuer + audience + expiry).




## Bonus Backend Golang Code

```golang

package main

import (
	"context"
	"encoding/json"
	"log"
	"net/http"

	"google.golang.org/api/idtoken"
)

type googleAuthReq struct {
	IDToken string `json:"id_token"`
}

func handleGoogleAuth(w http.ResponseWriter, r *http.Request) {
	var req googleAuthReq
	if err := json.NewDecoder(r.Body).Decode(&req); err != nil {
		http.Error(w, "Invalid request", http.StatusBadRequest)
		return
	}
	clientID := "your-client-id-here.apps.googleusercontent.com"
	ctx := context.Background()
	payload, err := idtoken.Validate(ctx, req.IDToken, clientID)
	if err != nil {
		http.Error(w, "Invalid ID token", http.StatusUnauthorized)
		return
	}
	// payload.Claims contains "email", "email_verified", "name", etc.
	email, _ := payload.Claims["email"].(string)
	emailVerified, _ := payload.Claims["email_verified"].(bool)
	if email == "" || !emailVerified {
		http.Error(w, "Invalid email or email not verified", http.StatusUnauthorized)
		return
	}
	w.Header().Set("Content-Type", "application/json")
	json.NewEncoder(w).Encode(payload.Claims)
}

func main() {
	mux := http.NewServeMux()
	mux.HandleFunc("/{path...}", handleGoogleAuth)
	err := http.ListenAndServe(":8080", mux)
	if err != nil {
		log.Fatalf("failed to start server: %v", err)
	}
}
```

`curl -X POST http://localhost:8080/ -H "Content-Type: application/json" --data '{"id_token":"foobar"}'
`


