blog source markdown for <https://blog.john-pfeiffer.com/>

*A pelican static site*

# Develop

Add or modify markdown files in "/content"

## Prerequisites

https://docs.astral.sh/uv/

`brew install uv; cat pyproject.toml`

*Dependencies are managed in `pyproject.toml`*

## Run it locally

```shell
uv sync
source .venv/bin/activate
pelican --version
pelican content -o output -s pelicanconf.py
```

open output/index.html in a browser to see the landing page (or be fancy and run a local python web server or even a docker container)

## Docker and Python and CircleCI

`docker run -it --rm --entrypoint=/bin/bash cimg/python:3.13`

> interactively explore the base python image from CircleCI: `python --version; uv --version`

*replace USERNAME and MYDIRECTORY, and note that the "output" directory is auto-generated*

```shell

docker run --volume /Users/USERNAME/MYDIRECTORY:/home/circleci/blogsource --publish 127.0.0.1:8000:8000 --rm -it cimg/python:3.13 /bin/bash
cd /home/circleci/blogsource
uv sync
uv run pelican --version
uv run pelican content -o output -s pelicanconf.py
cd output
python3 -m http.server
```

Now from a browser you can visit <http://localhost:8000>

*note some modules like [TOC] do not seem to work*

## Publish

To see the "fully published" output you can use:

`uv pelican content -o output -s publishconf.py`

*urls will be absolute and reference the fqdn in the "cloud", and better rending of some modules like TOC*

# Deploy
auto builds with CircleCI and deploys the static website to GitHub Pages (with a custom sub-domain)

Tutorial on how it was done: <https://blog.john-pfeiffer.com/circleci-for-a-pelican-static-github-site/>

A gotcha: in .circleci/config.yaml there is a specific line to clear the ssh key that was used for checking out the repo.

`ssh-add -D` clears all keys from the build agent before add_ssh_keys loads the write-enabled key to publish to GitHub static pages

