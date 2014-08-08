Title: publish-a-pelican-blog-using-a-bitbucket-post-webhook
Date: 2014-08-08 06:00

[TOC]

Webhooks are an incredibly useful way to tie together disparate network parts, WHEN something happens in one place, it sends a POST HTTP request to another place.

### Steps to 

1. Log in to the Bitbucket WebUI
1. Choose the repository
1. Choose to administer the repository (gear symbol) -> Hooks (left menu) , or simply <https://bitbucket.org/username/reponame/admin/hooks>
1. Select Hook Type (dropdown) , POST , Add Hook (Button)
1. Enter your target URL, SAVE
1. Setup a webserver (easiest might be Bamboo or Jenkins) somewhere
1. Ensure there is a URL that accepts POST requests
1. Ensure that when the POST is received it runs the pelican content generation commands to make the new output
1. Ensure new output is visible

> You may notice any existing POST webhooks, i.e. a HipChat notification add-on, listed: https://hipchat-bitbucket.herokuapp.com/commit?client_id=f955ddb5


### Flask and Bash source code to publish pelican

> This custom solution requires running that flask app manually, i.e. python mypublish.py
> It also requires having two repositories, one for the pelican source content, 
> the other repo (i.e. a bitbucket static web site) will only contain the output (.html files)

#### vi mypublish.py

    :::python
	from flask import Flask
	import os
	from subprocess import Popen, PIPE
	
	app = Flask(__name__)
	
	@app.route('/someuniquekeyhere', methods=['GET', 'POST'])
	def mypublish():
	  try:
	      output = Popen(["./mypublish.sh"], stdout=PIPE).communicate()[0]
	  except Exception as error:
	      return str(error)
	  return output
	
	
	if __name__ == '__main__':
	    app.run('0.0.0.0', 8443, use_reloader=True)


#### vi mypublish.sh

    :::bash
    #!/bin/bash
	git pull
	GITMESSAGE=$(git log -n 1)
	OUTPUT="../reponame.bitbucket.org"
	./clean-output.sh "../reponame.bitbucket.org"  # removes all of the old content
	echo "$GITMESSAGE"
	pelican content
	cp -a ./output/* ../output-johnpfeiffer.bitbucket.org
	
	rm -rf ./output
	rm -rf ./cache
	rm -f *.pyc
	
	cd "$OUTPUT"
	git add --all ./content
	git commit -m "source $GITMESSAGE"
	git push


#### vi clean-output.sh

    :::bash
	#!/bin/bash
	
	rm -rf ./output
	rm -rf ./cache
	rm -f *.pyc

	for ITEM in $SOURCE/*
	do
	  if [ -d "$ITEM" ]; then
	    rm -rf "$ITEM"
	  else
	    rm -f "$ITEM"
	  fi
	done



### More info
- <http://read-the-docs.readthedocs.org/en/latest/webhooks.html>
- <https://confluence.atlassian.com/display/BITBUCKET/POST+hook+management>