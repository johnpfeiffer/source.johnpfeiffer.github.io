Title: Continuous Delivery with Bitbucket Pipelines and Google App Engine Deployment and the storage.objects.list error
Date: 2017-05-23 22:24
Tags: bitbucket, google app engine, gae, bitbucket, pipelines, ci, cd, deployment, storage.objects.list

[TOC]

One thing that critical to writing software is actually delivering value.  That means shipping the bits, luckily the internet makes the cost of moving 1's and 0's near zero.

Like any other chore or drudge work the release process should be automated.

<https://en.wikipedia.org/wiki/Continuous_delivery>

I attempted to follow Google App Engine's documentation on how to setup Bitbucket Pipelines (yeah it's crazy how much free compute there is in the world such that I can tie together a free Continuous Integration service with a free Application Hosting service) but ran into a few snags I thought I'd document.

> Leveraging SaaS source control, CI, and CD means inherently placing trust in those vendors (and their ops and security teams)

## Google Cloud Setup

<https://cloud.google.com/solutions/continuous-delivery-bitbucket-app-engine>

Besides creating an App Engine Project the credentials to allow the automated deployment must also be generated.

1. Create a new project in Google: <https://console.cloud.google.com/appengine/create?lang=python&project=example-john>
2. Or use the Web UI <https://console.cloud.google.com/iam-admin/iam/project?project=example-john> (Use the "Select a project dropdown" in the middle and in the Select menu use the + symbol on the right to "Create project")
2. Note the ID: <https://console.cloud.google.com/home/dashboard?project=example-john>
3. BILLING on the left, enable that (and link your credit card I guess, Google are moving everything away from free - and the credit card is another way to track and correlate everything you do)
4. Enable the App Engine Admin API <https://console.cloud.google.com/apis/library?project=example-john>
5. Navigate to the Google Cloud Platform Console credentials page <https://console.cloud.google.com/apis/credentials?project=example-john>
6. Click Create credentials -> Service account key
7. Select "New service account" from the Service account dropdown
8. Input a name like "Bitbucket authorization" in the Service account name field
9. ENSURE the ROLES contain at least: App Engine -> **App Engine Admin** and Storage -> **Storage Admin**
10. Click the Create button. A copy of the JSON file will automatically download to your computer.   (if necessary on the right three dots choose "create key" -> create private key for "..." JSON
11. Click Create credentials > API key

## Bitbucket Setup

Create a new repository in bitbucket that will contain the code deployed to Google App Engine (in my example I'll use the Python native one but I know soon everything will Docker based)

The minimum version of the two app engine python app you will need are:

### app.yaml

    runtime: python27
    api_version: 1
    threadsafe: yes
    
    handlers:
    - url: .*
      script: main.app
    
    libraries:
    - name: webapp2
      version: "2.5.2"

For more info <https://developers.google.com/appengine/docs/python/config/appconfig>

### main.py

    #!/usr/bin/env python
    import webapp2
    
    class MainHandler(webapp2.RequestHandler):
        def get(self):
            self.response.write('hello')
    
    app = webapp2.WSGIApplication([('/', MainHandler)], debug=True)


A previous example of writing a Python web app with Google App Engine <https://blog.john-pfeiffer.com/google-app-engine-python/>

## Bitbucket Pipelines Configuration

### Configuring the secure environment variables in Bitbucket Pipelines

Use the Bitbucket WebUI in order to securely add the three variables (project id, api key, secrets json).

i.e. <https://bitbucket.org/johnpfeiffer/continuous-deployment-bitbucket/admin/addon/admin/pipelines/repository-variables>


- CLOUDSDK_CORE_PROJECT (the app engine project id)
- GOOGLE_API_KEY
- GOOGLE_CLIENT_SECRET (all of the contents of the json file pasted in)

**Ensure the Pipelines Environment variable of GOOGLE_CLIENT_SECRET is "Secured"** so that they are encrypted in log output


Full instructions: <https://cloud.google.com/solutions/continuous-delivery-bitbucket-app-engine#setting_up_environment_variables>


### bitbucket-pipelines.yml file

A yaml configuration file describes the work that you instruct Bitbucket Pipelines to do, in this case we are doing the extra work of grabbing the remote google cloud SDK and installing it so that we use it with the credentials to deploy the app.

    image: python:2.7
    
    pipelines:
      default:
        - step:
            script:
              - export CLOUDSDK_CORE_DISABLE_PROMPTS=1
              - SDK_VERSION=127.0.0
              - SDK_FILENAME=google-cloud-sdk-${SDK_VERSION}-linux-x86_64.tar.gz
              - curl -O -J https://dl.google.com/dl/cloudsdk/channels/rapid/downloads/${SDK_FILENAME}
              - tar -zxvf ${SDK_FILENAME} --directory ${HOME}
              - export PATH=${PATH}:${HOME}/google-cloud-sdk/bin
              - GAE_PYTHONPATH=${HOME}/google_appengine
              - export PYTHONPATH=${PYTHONPATH}:${GAE_PYTHONPATH}
              - python scripts/fetch_gae_sdk.py $(dirname "${GAE_PYTHONPATH}")
              - echo "${PYTHONPATH}" && ls ${GAE_PYTHONPATH}
              - echo "key = '${GOOGLE_API_KEY}'" > api_key.py
              - echo ${GOOGLE_CLIENT_SECRET} > client-secret.json
              - gcloud auth activate-service-account --key-file client-secret.json
              - gcloud --verbosity=error app deploy app.yaml --promote
> A best practice is to pull the dependency from storage you have control over (or simply vendor the SDK in the source code) rather than downloading it every time and risking the upstream pinned version being removed

### scripts/fetch_gae_sdk.py

    #!/usr/bin/env python
    # Copyright 2015 Google Inc. All rights reserved.
    #
    # Licensed under the Apache License, Version 2.0 (the "License");
    # you may not use this file except in compliance with the License.
    # You may obtain a copy of the License at
    #
    #     http://www.apache.org/licenses/LICENSE-2.0
    #
    # Unless required by applicable law or agreed to in writing, software
    # distributed under the License is distributed on an "AS IS" BASIS,
    # WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
    # See the License for the specific language governing permissions and
    # limitations under the License.
    
    # Retrieved from https://github.com/Google/oauth2client
    """Fetch the most recent GAE SDK and decompress it in the current directory.
    Usage:
        fetch_gae_sdk.py [<dest_dir>]
    Current releases are listed here:
        https://www.googleapis.com/storage/v1/b/appengine-sdks/o?prefix=featured
    """
    
    import json
    import os
    import StringIO
    import sys
    import urllib2
    import zipfile
    
    _SDK_URL = (
        'https://www.googleapis.com/storage/v1/b/appengine-sdks/o?prefix=featured')
    
    
    def get_gae_versions():
        try:
            version_info_json = urllib2.urlopen(_SDK_URL).read()
        except:
            return {}
        try:
            version_info = json.loads(version_info_json)
        except:
            return {}
        return version_info.get('items', {})
    
    def _version_tuple(v):
        version_string = os.path.splitext(v['name'])[0].rpartition('_')[2]
        return tuple(int(x) for x in version_string.split('.'))
    
    
    def get_sdk_urls(sdk_versions):
        python_releases = [
            v for v in sdk_versions
            if v['name'].startswith('featured/google_appengine')]
        current_releases = sorted(
            python_releases, key=_version_tuple, reverse=True)
        return [release['mediaLink'] for release in current_releases]
    
    
    def main(argv):
        if len(argv) > 2:
            print('Usage: {} [<destination_dir>]'.format(argv[0]))
            return 1
        dest_dir = argv[1] if len(argv) > 1 else '.'
        if not os.path.exists(dest_dir):
            os.makedirs(dest_dir)
    
        if os.path.exists(os.path.join(dest_dir, 'google_appengine')):
            print('GAE SDK already installed at {}, exiting.'.format(dest_dir))
            return 0
    
        sdk_versions = get_gae_versions()
        if not sdk_versions:
            print('Error fetching GAE SDK version info')
            return 1
        sdk_urls = get_sdk_urls(sdk_versions)
        for sdk_url in sdk_urls:
            try:
                sdk_contents = StringIO.StringIO(urllib2.urlopen(sdk_url).read())
                break
            except:
                pass
        else:
            print('Could not read SDK from any of {}'.format(sdk_urls))
            return 1
        sdk_contents.seek(0)
        try:
            zip_contents = zipfile.ZipFile(sdk_contents)
            zip_contents.extractall(dest_dir)
            print('GAE SDK Installed to {}.'.format(dest_dir))
        except:
            print('Error extracting SDK contents')
            return 1
    
    if __name__ == '__main__':
        sys.exit(main(sys.argv[:]))
> This is google's script to download and extract their App Engine SDK , included here only for completeness


## Push a commit to trigger a deployment

The whole point of all of that work is to make life easier for every commit that follows.

    git add --all .
    git commit -m 'example google app engine app deployed via bitbucket pipelines'
    git push

You can monitor the results of every change in the Addon's output logs:

- <https://bitbucket.org/johnpfeiffer/continuous-deployment-bitbucket/addon/pipelines/home#!/>

You can monitor the deployment history in Google App Engine's console:

- <https://console.cloud.google.com/appengine/versions?project=bitbucket-pipelines&serviceId=default>

And of course see the currently deployed application in action:

- <https://bitbucket-pipelines.appspot.com/>

## Actually using automated testing

CI (continuous integration) testing is the ideal next thing to add as this allows you to automatically prevent critical errors from being deployed to production.

This means adding unit tests (test_main.py) and then running them by updating bitbucket-pipelines.yml

    - python test_main.py

It is also possible to keep extending the work required by installing any requirements.txt dependencies (i.e. only required for testing) or running post deployment end-to-end smoke tests.

## Double checking security

If your repository is public the pipelines log outputs will be public.  Double check that you are not "leaking" your API key, secrets, or hardcoded passwords. =|

## Troubleshooting

**"Does not contain a valid app engine project"**
> Most likely the app.yaml has deprecated fields or invalid characters

**"does not contain an App Engine application."**
> Most likely the app.yaml has deprecated fields or invalid characters, or maybe missing a main.py altogether

**"ERROR: The [application] field is specified in file [/opt/atlassian/pipelines/agent/build/app.yaml]"**
> This is because previously app.yaml included "application" and "version" but those lines are now deprecated, delete them

**"You do not have permission to access app "**
> Most likely the Role of "App Engine Admin" still needs to be added, use the IAM for the project to update the Permissions

e.g. <https://console.cloud.google.com/iam-admin/iam/project?project=bitbucket-pipelines>

Or ensure you have an API key generated and added to the Bitbucket Pipelines environment ... or delete all API keys and service accounts and do them again (because it seems to get stuck if you have encrypted API key or something)

- <https://console.cloud.google.com/apis/credentials?project=bitbucket-pipelines>
- <https://console.cloud.google.com/iam-admin/serviceaccounts/project?project=bitbucket-pipelines>

**"Caller does not have storage.objects.list access to bucket staging.bitbucket-pipelines.appspot.com."**
> Ensure the Role "Storage Object Admin" was added to the Roles during creation, see above

This guy got really close and helped me find the hint about Storage Object Admin: <http://www.deadunicornz.org/blog/2017/01/31/travis-ci-and-deploying-golang-apps-to-gae/>


## Using Docker with Bitbucket Pipelines

I could reduce the time required to build (and decouple the build stages) by using a Docker image that already contains the GCloud SDK.

This also extends the flexibility if part of your build flow is to build and tag a Docker image as an artifact that can be used for multiple tests (i.e. parallelization) and especially if you are already using Docker in Production.

- <https://confluence.atlassian.com/bitbucket/use-docker-images-as-build-environments-in-bitbucket-pipelines-792298897.html>
- <https://confluence.atlassian.com/bitbucket/debug-your-pipelines-locally-with-docker-838273569.html>

