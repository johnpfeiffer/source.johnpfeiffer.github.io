Title: Intro to MCP - give your LLM tools with model context protocol
Date: 2025-07-27 19:20
Tags: ai, llm, mcp

[TOC]

# Why is weather so hard?

Let's start with a problem...

*(rather than technology looking for a problem ;)*

Getting the weather can be frustrating

- which of the 6+ websites would you choose?
- how many annoying ads?
- why does one show the city first, another shows daily temperature, and a third jumps to the week ahead?

It can take many clicks to view a specific city that you're interested in...

And many prompts to "sign up as a user" or "subscribe aka pay money" to have your view of the weather customized

So pay for a weather app - that still doesn't do what you want?

Or find a weather API, write your own app/website, just the way you want it:

> "5 day forecast of days and nights - temperatures in both F and C

# How useful is your toilet without the plumbing?

LLMs (Large Language Models) excel at natural language processing (NLP) - like asking the computer about the weather (typos and all!)

But the LLM doesn't have access to up to date info (weather, prices) or private data (emails, databases).

Model Context Protocol is a way to solve multiple things:

- A user would like the LLM to utilize newer or specific info
- Each LLM vendor has a "custom way to configure"
- With multiple LLM applications running locally... and you have a lot of tools
- Organizations want a centralized way to control access to tools and (potentially private) information

Therefore this is an "N x M" problem: N (LLM) applications for M tools

The grand vision: 

1. LLM vendors have a standard way to give users more leverage/capabilities
2. Developers can build these "MCP Servers" once - and support every LLM product
3. Organizations can centralize and manage all the LLMs accessing a given capability or dataset
4. Users have far more powerful tools with very little setup


# Pre-Requisites
Install the python dependency manager

`curl -LsSf https://astral.sh/uv/install.sh | sh`

Or for MacOS `brew install uv`

background: <https://docs.astral.sh/uv/>

Create a default project from a built in template with uv:

`uv init mcp-server-demo`

This creates a very minimal package (dependency) management configuration file
- <https://packaging.python.org/en/latest/guides/writing-pyproject-toml/>

	[project]
	name = "mcp-server-demo"
	version = "0.1.0"
	description = "Add your description here"
	readme = "README.md"
	requires-python = ">=3.13"
	dependencies = []
	
_you can ignore or remove the extraneous .gitignore, .git, README.md files_

Remove (delete) main.py as it is extraneous for this project.

Next create a python virtual environment and activate it, and install dependencies:
- <https://docs.python.org/3/library/venv.html>

`cd mcp-server-demo`

`uv venv`

`source .venv/bin/activate`

`uv add "mcp[cli]" httpx`

# The code

Use a coding editor to create weather.py that queries the national weather service and provides the MCP hook:

	:::python3
	from typing import Any
	import httpx
	from mcp.server.fastmcp import FastMCP
	
	mcp = FastMCP("weather")
	
	NWS_API_BASE = "https://api.weather.gov"
	USER_AGENT = "weather-app/1.0"
	
	async def make_nws_request(url: str) -> dict[str, Any] | None:
    headers = {
        "User-Agent": USER_AGENT,
        "Accept": "application/geo+json"
    }
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(url, headers=headers, timeout=30.0)
            response.raise_for_status()
            return response.json()
        except Exception:
            return None
	
	@mcp.tool()
	async def get_forecast(latitude: float, longitude: float) -> str:
	    # First get the forecast grid endpoint
	    points_url = f"{NWS_API_BASE}/points/{latitude},{longitude}"
	    points_data = await make_nws_request(points_url)

	    if not points_data:
	        return "Unable to fetch forecast data for this location."

	    # Get the forecast URL from the points response
	    forecast_url = points_data["properties"]["forecast"]
	    forecast_data = await make_nws_request(forecast_url)

	    if not forecast_data:
	        return "Unable to fetch detailed forecast."

	    # Format the periods into a readable forecast
	    periods = forecast_data["properties"]["periods"]
	    forecasts = []
	    for period in periods[:5]:  # Only show next 5 periods
	        forecast = f"""
	{period['name']}:
	Temperature: {period['temperature']}°{period['temperatureUnit']}
	Wind: {period['windSpeed']} {period['windDirection']}
	Forecast: {period['detailedForecast']}
	"""
	        forecasts.append(forecast)

	    return "\n---\n".join(forecasts)
	
	
	def main():
	    # Initialize and run the server
	    mcp.run(transport='stdio')    
	
	if __name__ == "__main__":
	    main()
	

The second function in the file specifically creates the "MCP Tool"

The end of the file is the classic python main to have this run as a server

## one last config pyproject.toml

Also, modify `pyproject.toml` to ensure it connects the weather.py and main:

[project.scripts]

weather = "weather:main"

example of the final **pyproject.toml** file

	:::toml
	[project]
	name = "mcp-server-demo"
	version = "0.1.0"
	description = "Add your description here"
	readme = "README.md"
	requires-python = ">=3.13"
	dependencies = [
	    "httpx>=0.28.1",
	    "mcp[cli]>=1.17.0",
	]
	
	[project.scripts]
	weather = "weather:main"


# Configure Claude to use your new Weather MCP

The following tells your LLM application (i.e. Claude for Desktop)

- There is an MCP server named “weather”
- launch it by running uv --directory /ABSOLUTE/PATH/TO/PARENT/FOLDER/weather run weather.py

Modify to add the JSON to the file ~/Library/Application\ Support/Claude/claude_desktop_config.json


	:::json
	{
	  "mcpServers": {
	    "weather": {
	      "command": "uv",
	      "args": [
	        "--directory",
	        "/ABSOLUTE/PATH/TO/PARENT/FOLDER/weather",
	        "run",
	        "weather.py"
	      ]
	    }
	  }
	}

Restart your LLM application (claude for desktkop)

You should be able to see it in the UI: Settings -> Developer 

"your new MCP server"


# A better response about the weather

*(When the LLM application "aka MCP host" starts, it also launches your MCP server as a subprocess)*

You (the user) have your LLM running locally and ask:

> What's the weather in San Francisco?

The LLM decides it can use the "weather" tool to help answer the question

*It actually prompts at first to to approve the permissions:*

> Claude wants to use Get Forecast from weather

The LLM has geographic data in its training and can use it's "super distilled storage" to convert a city name to coordinates

	:::json
	Request
	{
		`latitude`: 37.7749,
		`longitude`: -122.4194
	}

- The LLM (MCP Host) is the client which communicates via JSON-RPC over stdin/stdout with the "MCP weather server"

- The (local) MCP weather server makes HTTP requests to the National Weather Service API

- The forecast data (JSON) is returned from the MCP Server to the "MCP Host"

The LLM (MCP Host) incorporates and reformats the JSON into a natural language response


<https://modelcontextprotocol.io/docs/develop/build-server>

<https://github.com/modelcontextprotocol>

# Last thoughts

Adding tools to an LLM further extends the leverage already available with amazing default NLP that has fact sets and token generation.

Capabilities like "current weather" can be added in a straightforward manner.

MCP unlocks current data, private data, specialized tools, or even running a machine in the physical world - bridging the many fragmented and distinct APIs and interfaces


# Bonus Content

You can directly see what the National Weather Service API returns

`curl https://api.weather.gov/points/37.780,-122.420`

*interestingly lat,lon are converted into "grids" which each local forecast office uses, so the JSON returns "Daly City" or "Sausalito"*

https://forecast.weather.gov/MapClick.php?lon=-122.4192&lat=37.7793

Send JSON RPC in bash

`uv run weather.py << 'EOF'`

heredoc> 

	:::json
	{"jsonrpc": "2.0", "method": "initialize", "params": {"protocolVersion": "2024-11-05", "capabilities": {}, "clientInfo": {"name": "test", "version": "1.0"}}, "id": 1}
EOF

**A response**
	
	:::json
	{"jsonrpc":"2.0","id":1,"result":{"protocolVersion":"2024-11-05","capabilities":{"experimental":{},"prompts":{"listChanged":false},"resources":{"subscribe":false,"listChanged":false},"tools":{"listChanged":false}},"serverInfo":{"name":"weather","version":"1.17.0"}}}

