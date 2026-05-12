Title: Web scraping and crawling as a rite of passage
Date: 2025-01-11 11:11
Tags: programming, c, python, golang, http, html

[TOC]

The internet and HTTP has had an "agent" concept long before AI. <https://www.rfc-editor.org/rfc/rfc9110.html#name-user-agent>

Connecting to a server (with TCP) underpins FTP and HTTP; a simple client can download resources.

Sometimes they are commonly called a "scraper" or "crawler", I can remember one of my first joys in coding was writing a "download a page" program.

# Good old C

```c
#include <stdio.h>       // printf, perror
#include <string.h>      // memset, memcpy
#include <unistd.h>      // close
#include <netdb.h>       // gethostbyname, herror, struct hostent
#include <sys/socket.h>  // socket, connect
#include <netinet/in.h>  // sockaddr_in, htons

int main(void) {
    struct hostent *h = gethostbyname("example.com");
    if (!h) {
        herror("gethostbyname");
        return 1;
    }
    int s = socket(AF_INET, SOCK_STREAM, 0);
    if (s < 0) {
        perror("socket");
        return 1;
    }
    struct sockaddr_in addr;
    memset(&addr, 0, sizeof(addr));
    addr.sin_family = AF_INET;
    addr.sin_port = htons(80);
    memcpy(&addr.sin_addr, h->h_addr, h->h_length);

    if (connect(s, (struct sockaddr *)&addr, sizeof(addr)) < 0) {
        perror("connect");
        close(s);
        return 1;
    }
    printf("successful CONNECT\n");

    const char *req =
        "GET / HTTP/1.0\r\n"
        "Host: example.com\r\n"
        "\r\n";

    // send to the socket the HTTP string
    write(s, req, strlen(req));
    char buf[4096];
    ssize_t n;
    while ((n = read(s, buf, sizeof(buf))) > 0) {
        fwrite(buf, 1, n, stdout);
    }

    printf("\ndone\n");
    close(s);
    return 0;
}

```

*Oh the joys of hours of syntax and compilation errors - to finally successfully reach across the network =]*

Each popular programming language has this foundational piece: 

- Java
- Python (thank you BeautifulSoup4 and Requests <https://requests.readthedocs.io/en/latest/>)
- Golang <https://pkg.go.dev/net/http>


And of course there are some excellent dedicated tools:

- **curl** <https://curl.se/docs/tutorial.html> `curl -H "Host: example.com" 172.66.147.243:80`
- **wget** <https://www.gnu.org/software/wget/manual/wget.html> 

## ASCII Diagrams

This utility will convert the domain name into an IP address: `dig example.com`

```plaintext
;; ANSWER SECTION:
example.com.		159	IN	A	172.66.147.243
```

**Client Server Interactions**

```plaintext
CLIENT                                  [DNS SERVER]
  |   What IP Address is example.com ->    |
  |     <- example.com = "172.66.147.243"  |
  |
  |      TCP connect to 172.66.147.243 ->            | [WEB SERVER at 172.66.147.243]
  |      HTTP GET / Host: example.com  ->            | 
  |     <- HTTP 200 OK, response: headers + HTML     |

```

- - -

# Firecrawl

New kid on the block: firecrawl

You can download the open source project and run it locally with docker <https://github.com/firecrawl/firecrawl>

```plaintext
Firecrawl API
Redis
Postgres / queue backing store
Playwright service
workers
queue UI
```

- - -

`vim .env`

```
# Minimal local Docker Compose Firecrawl config

PORT=3002
HOST=0.0.0.0
USE_DB_AUTHENTICATION=false

# Queue admin:
# http://localhost:3002/admin/localdev/queues
BULL_AUTH_KEY=localdev

# prefer explicit even though these are in docker compose
REDIS_URL=redis://redis:6379
REDIS_RATE_LIMIT_URL=redis://redis:6379
PLAYWRIGHT_MICROSERVICE_URL=http://playwright-service:3000/scrape

# Reasonable laptop defaults
NUM_WORKERS_PER_QUEUE=4
CRAWL_CONCURRENT_REQUESTS=4
MAX_CONCURRENT_JOBS=2
BROWSER_POOL_SIZE=2

LOGGING_LEVEL=INFO
```

gotcha do not build everything locally in docker containers: you also have to modify **docker-compose.yaml**

`grep -n "build:" docker-compose.yaml`

comment out those build statements, and make active the "image" statements

```yaml
x-common-service: &common-service
  image: ghcr.io/firecrawl/firecrawl:latest
  # build: apps/api
```


`docker compose build`

`docker compose up`

# firecrawl scrape a single page 

Use the Scrape endpoint - it only retrieves a single page:

`curl -X POST http://localhost:3002/v1/scrape -H 'Content-Type: application/json' -d '{"url": "https://example.com","formats": ["html"]}' > temp.json`

```json
{
  "success": true,
  "data": {
    "metadata": {
      "title": "Example Domain",
      "sourceURL": "https://example.com",
      "url": "https://example.com",
      "statusCode": 200,
      "contentType": "text/html",
    },
    "html": "<!DOCTYPE html><html lang=\"en\"><body><div><h1>Example Domain</h1><p>This domain is for use in documentation examples without needing permission. Avoid use in operations.</p><p><a href=\"https://iana.org/domains/example\">Learn more</a></p></div>\n</body></html>"
  }
}
```

*Some jq fun to just see the html `jq -r '.data.html' temp.json`*

If you just want the links from a given page:

`curl -X POST http://localhost:3002/v1/scrape -H 'Content-Type: application/json' -d '{"url": "https://example.com","formats": ["links"]}' > example-links.json`

`cat example-links.json | jq`



TODO: How to use it crawl a whole website

The local queue system will show you each page as it prepares to scrape/download:

- <http://localhost:3002/admin/localdev/queues>

# Known Limitations

These approaches all focus on HTML. The rise of JavaScript and React mean that content needs even more advanced tools.

Often people use the python framework Playwright (ideological successor to Selenium) as a headless browser to interact with interactive websites.


TODO: section on playwright
