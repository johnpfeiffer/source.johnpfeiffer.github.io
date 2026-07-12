Title: Experiment fast with Cloudflare - Pages and Workers and LLMs
Date: 2025-08-27 20:20
Tags: cloudflare, static-site, react, ai, llm

[TOC]

> Go slow to go fast: building my own frontend app platform sped up my experimentation by 10x

I'm continually exploring free and low cost hosting providers as an avenue for unlimited experimentation within constraints.

Cloudflare's evolution from simple CDN (ContentDeliveryNetwork) serving static assets (e.g. .jpg or .css) into the clever adjacency of more complicated .js files meant a new fast, reliable competitor to the hosting space.

In the React/Javascript pattern, compute occurs on the client side - hence Cloudflare can offer generous "free hosting".

*A previous blog post on Google's ecosystem <https://blog.john-pfeiffer.com/maximum-leverage-and-minimum-ops-with-google-cloud-run-and-the-jules-coding-agent/>*

# Monorepo to move fast

I used a single private github repo that serves as the vehicle for multiple frontend applications.

At first I only used React with JS but later adopted Typescript to improve reliability (and with LLM coding it's "free" to rewrite from JS to TS ;)

Every sub-app is "unaware" that it is in a monorepo, unaware of the "shared hosting" setup. This allows for local development and future portability.

```
/apps
  /example - the most minimal skeleton for easy copy paste as a template
  /material-ui-example
  /sso-example - Google OAuth integration
  /rands-game
...
```

Every new idea can simply be a new directory in "apps". Further accelerated by a template and an LLM.

> Git push and it's live in production

# Cloudflare Pages and GitHub

I started with an LLM to generate the minimum react/typescript app that was compatible with Cloudflare.

- <https://developers.cloudflare.com/pages/framework-guides/deploy-a-react-site/>

Cloudflare's integration with GitHub was very straightforward and smooth:

- https://dash.cloudflare.com/ , (a sometimes confusing/changing UI) ... Build -> Compute -> Workers & Pages
- "Create application" -> Pages -> Import an existing Git repository 
- Add GitHub account (authenticate in the "Install Cloudflare Workers and Pages" popup)

*In the (sometimes confusing) GitHub UI it is listed as Integrations -> Application , "Cloudflare Workers and Pages"*

**Least Privilege Permissions:** make sure you choose "Repository access" -> "Only select repositories"

In this case Cloudflare should only have access to the monorepo.

Easy simple defaults:

- Build command: `npm run build`
- Build output: `dist`

> The Cloudflare GitHub App automatically deploys your code to Cloudflare when it detects a new commit to the default branch of the GitHub repository

## File layout in the monorepo

```
MONOREPO/
├── package.json              # Root: orchestrates builds
├── functions/
│   └── _middleware.js         # Cloudflare Worker: routes requests
├── scripts/
│   ├── build-all-apps.js      # Discovers and builds all apps
│   ├── collect-builds.js      # Assembles dist/ for deployment
├── apps/
│   ├── example/
│   │   ├── package.json
│   │   ├── vite.config.ts
│   │   ├── index.html
│   │   └── src/
│   ├── material-ui-example/
│   │   ├── ...
│   └── ...
└── dist/                      # Generated: what gets deployed
├── apps/
│   ├── example/
│   ├── material-ui-example/
│   └── ...
```

## Scripts for the Build pipeline

The root package.json orchestrates: build every app, collect the outputs into the final deployment artifact.

```json
{
	"scripts": {
	"build": "npm run build:all && npm run collect",
	"build:all": "node scripts/build-all-apps.js",
	"collect": "node scripts/collect-builds.js",
	}
}
```

1. `build-all-apps.js`

- Copies any shared assets (i.e. favicon.ico or robots.txt) from a SHARED/public directory into each app's "/public/"
- Iterates through every directory in /apps and runs `npm install && npm run build` 

2. `collect-builds.js`

- Gathers each app's `dist/` output into the production bundle area: /dist/apps/appname
- Copies the `/functions/` directory into the production bundle area: /dist/functions/


### Deploying to Cloudflare Pages

The monorepo's a platform: modify code in `/apps/example` and commit + push the change.

The GitHub + Cloudflare integration detects the new change, auto-builds, auto-deploys.

# Middleware as an Architectural Seam

> How to scale adding common functionality to every app?

Middleware is a common systems design pattern to take advantage of the "connection/space" between two components.

- <https://martinfowler.com/bliki/LegacySeam.html>

In this monorepo, Apps don't know where they're hosted. *(every app's config sets base: '/')*

Cloudflare sits between the client (browser) and the Application, and via the /functions directory, code can become **Cloudflare Workers** that intercept requests.

`/functions/_middleware.js` intercepts every request, based on the Cloudflare Pages Functions convention...

> A _middleware.js file exports an `onRequest` function

- <https://developers.cloudflare.com/pages/functions/middleware/>

Here's what the Middleware pattern does for my monorepo at runtime:

- At run time in production it routes requests like `https://example.com/myapp/*` to the actual app's build files
- Asset routing: A request for /EXAMPLE/assets/index-abc123.js gets rewritten to /apps/EXAMPLE/assets/index-abc123.js , where the file actually lives.
- SPA fallback: Any path without a file extension (like /EXAMPLE/my-slug) serves EXAMPLE app's index.html so React Router can handle it client-side.
- HTML rewriting: Since each app is built with base: '/', the HTML references assets at /assets/.... The middleware rewrites these to /{appname}/assets/... and injects a <base> tag so the browser resolves relative paths correctly.


## The Hardest Problem - URL Rewriting in SPAs

A gotcha: the middleware rewrite only occurs when the file is first served, i.e. for the first navigation - after that the Browser is interacting with the Application code and the app's own SPA router takes over.

This is not an issue for a simple app (single view, no navigation that modifies the URL) - it always presents the same URL. e.g. https://example.com/SIMPLEAPP/

But if the app is more complex, with functionality that rewrites URLs and/or navigation history, then...

The app needs to preserve the "app name" in any navigation history or url rewriting; the app should work identically with or without the "app name" prefix.

In development the SPA could have /dashboard and /someform , and in production it would be https://example.com/APPNAME/dashboard and https://example.com/APPNAME/someform .

While the default answer would be "modify basename", this hardcodes the production deploy details into every dev environment.

And basename is static and set at app init time, and the app discovers it is in production (has an appname prefix in the URL) at runtime.

My solution is to leverage a clean internal navigation pattern even in simple apps - code that manages URLs/Navigation to ensure it parses the first path segment as an optional app prefix and includes it in every internally generated route.

```typescript

const router = createBrowserRouter([
  {
    path: '/',
    element: <Outlet />,
    children: [
      {
        path: ':app',
        element: <AppLayout />,
        children: [
          {
            index: true,
            element: <HomePage />,
          },
          {
            path: 'survey',
            element: <SurveyPage />,
          },
```

There's a thin layout that extracts the prefix and passes it down via context:

```typescript
  export type AppContext = { app: string }

  function AppLayout() {
    const { app = '' } = useParams()
    return <Outlet context={{ app } satisfies AppContext} />
  }
```

  Then every component just does:

```typescript
  const { app } = useOutletContext<AppContext>()
  navigate(`/${app}/survey`)
  navigate(`/${app}/result/${id}`)
```

That's the pattern, `:app` as a parent route segment means child routes don't duplicate anything — they just exist once under the prefix.

The AppLayout captures it, context distributes it.

This router and URL management pattern is a good practice even if you don't have my specific monorepo multi-app situation.

# Cloudflare Pages Functions convention for Workers

The Cloudflare Pages build system has a convention where `/functions` become Functions - but all generated into a single Worker script.

That Worker is deployed as an internal part of the Pages deployment itself, versioned with each deploy, so it won't appear in the Workers list (it's owned by the Pages project).

*The one binding the middleware needs — env.ASSETS — is system-injected by Pages into every Functions deployment automatically.*

## Debugging Deployments with Realtime Logs

When I was troubleshooting my middleware, from the (Compute -> Workers & Pages) Dashboard for my Application, I could see every deployment; on the right click on the "Details" button.

```
"Production - Deployment details"
Deployment URL: https://6e1762b8.APPNAME.pages.dev
```

Below there are a series of tabs: Build log *(useful for debugging build script issues)*, Assets uploaded, **Functions**, Redirects, Headers

When you click on Functions you can see the deployed **Routing configuration**

```
{
  "routes": [
    {
      "routePath": "/",
      "mountPath": "/",
      "method": "",
      "middleware": [
        "_middleware.js:onRequest"
      ]
    }
  ],
  "baseURL": "/"
}
```

When the code in `_middleware.js` contains log statements - these are then logged in the Functions (Workers) logs.

```javascript
    if (!validApps.includes(appName)) {
      console.log("not a valid app name");
      return context.next();
    }
```

**Functions** have "Real-time Logs" (beta)

> View the console.log output and errors from your Functions.

Click on the button "Begin log stream"

`Websocket connection established. Listening for events...`

Use a browser and navigate to a part of your application that leverages the middleware, i.e. https://example.com/APPNAME

Observe the new streaming events and click for details:

```plaintext
GET https://example.com/favicon.ico

"logs": [
    {
      "message": [
        "not a valid app name"
      ],
      "level": "log",
	  
GET https://example.com/APPNAME
    {
      "message": [
        "Rewriting HTML for:",
        "APPNAME"
      ],	  
```

More detailed info about the internals of Cloudflare Workers:

- <https://blog.cloudflare.com/workerd-open-source-workers-runtime/>
- <https://blog.cloudflare.com/mitigating-spectre-and-other-security-threats-the-cloudflare-workers-security-model/>



# Cloudflare Workers AI

Let's add AI! Cloudflare provides vertical integration from CDN to Hosting to LLMs; The Cloudflare Workers AI models run on Cloudflare’s network, not locally.

This means your Application needs a "Workers AI" binding configured. At the Cloudflare dashboard for your Application:

(Compute) Workers & Pages -> Your Application Name: Deployments, Metrics, Custom Domains, **Settings**

**Bindings** -> +Add -> "Add a resource binding" -> Workers AI

Give your binding a name under Variable name, e.g. AI

| Type   | Name | Value      |
|--------|-----|-----------|
| Workers AI | AI | Workers AI Catalog  |

*Redeploy your project for the binding to take effect.*

- <https://developers.cloudflare.com/workers/runtime-apis/bindings/>

## Code

Since Pages Functions use file-based routing: one more file in the monorepo, `functions/ai/chat.js`, becomes a shared `POST /ai/chat` endpoint for every app.

Exporting `onRequestPost` means Pages handles method routing for you.

```javascript
// functions/ai/chat.js  ->  POST /ai/chat
export async function onRequestPost({ request, env }) {
  const { message } = await request.json();

  if (typeof message !== "string" || !message.trim()) {
    return Response.json({ error: "message is required" }, { status: 400 });
  }

  const result = await env.AI.run("@cf/openai/gpt-oss-120b", {
    instructions: "You are a concise assistant.",
    input: message,
  });

  // gpt-oss speaks the OpenAI Responses API: reasoning items first, the answer is in the "message" item.
  // Shapes vary by model so log the raw result once before writing the extraction.
  const text = (result.output ?? [])
    .filter((item) => item.type === "message")
    .flatMap((item) => item.content ?? [])
    .filter((part) => part.type === "output_text")
    .map((part) => part.text)
    .join("");

  return Response.json({ message: text, usage: result.usage });
}
```

Any app in the monorepo calls it same-origin — no client config, no CORS, no API keys:

```javascript
const res = await fetch("/ai/chat", {
  method: "POST",
  headers: { "Content-Type": "application/json" },
  body: JSON.stringify({ message: "Tell me a joke" }),
});
const { message } = await res.json();
```

**Production notes:**

- my `_middleware.js` passes this route through untouched because `ai` is not an app name. `context.next()` falls through to file-based functions
- as I hardened it in production I added CORS origin checks, input limits, and a retry
- beware that reasoning models can spend your entire `max_tokens` budget thinking before they answer

> finish_reason: "length" with content: null

## Logs

Log before you need it!

A best practice is to "bracket" logs with a start and end (and of course log errors!)

From the (Dashboard) Application -> Deployments -> Details -> Functions

You will see your new route:

```
{
  "routes": [
    {
      "routePath": "/ai/chat",
      "mountPath": "/ai",
      "method": "",
      "module": [
        "ai/chat.js:onRequest"
      ]
    },
    {
      "routePath": "/",
      "mountPath": "/",
      "method": "",
      "middleware": [
        "_middleware.js:onRequest"
      ]
    }
  ],
  "baseURL": "/"
}
```

Real-time Logs (beta) -> "Begin log stream"


## References

For more info on all of the Cloudflare AI models:

- <https://developers.cloudflare.com/workers-ai/platform/pricing/>

