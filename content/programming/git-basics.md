Title: Git Basics and Hard to Scratch Itches
Date: 2013-07-07 12:34
Tags: git

[TOC]

Like "tabs vs spaces" there are tools and choices which create more controversy than others.

Here's my pragmatic take on how to get stuff done...

### Git Cheat Sheet

    git branch
> see the current branch

    git status
> are there any files changed?

    git stash
> save and hide any modified files to a temporary cache

    git checkout master
> set the local working files to the shared canonical branch (aka "master")

    git pull
> get and merge any changes, many others prefer the more precise git fetch

    git log
> examine the history of changes made upstream (consider pre-emptively how the merge will affect things)

    git checkout mybranch
> change the focus back to the working dev branch

    git pull
> ensure the local working files from the branch are the latest (i.e. if other contributors or devices have made modifications)

    git merge master
> force reconciliation of master and the current working branch

   RESOLVE CONFLICTS IN THE CODE MANUALLY
> one thing to remember is that "merge" is best effort so sometimes code/lines will be added or removed that are not the desired semantic outcome

    git commit
> indicate a merge from master and any conflict resolution fixes

    git push
> **never force** , the changed branch may be worked on by others and a forked history means no reconciliation...

### Extra Credit

    cp -a FOOBAR /tmp
> manually back up the files

    git checkout -- ./name
> reset a single changed file back to the previously committed version

    git log ; git revert COMMITID
> identify a mistaken commit and create a commit to undo all changes until the working files (and git history) match that specific commit id

    git reset --soft HEAD^^
> correct and recommit change A, then go back to recommitting change B

    git reset HARD
> reset all of the working files to a previously committed version

    rm -rf FOOBAR; git clone
> throw away entirely a locally copy and start again from the remote version


### Simple Git Theory

Distributed Version Control

Directed Acyclical Graph

Any branch can be "master".

But in practice most developes use an agreed centralized location (i.e. good availability/uptime), especially a SaaS like github or bitbucket.

### Basic Git Commands

`git clone`

> SSH is far more convenient and secure

`git clone `
> HTTPS is common for "read-only" downloads of an open source project


`git add --all .`
> the extra parameter ensures new files are added (which I otherwise forget), and as a bonus will detect file/directory renaming

`git log`
> Show the history of commits (and hashes)

`git rebase -i`
> interactively rewrite git history, NEVER do this on a shared/collaborative branch/repository

### Remove a large file from history

`git filter-branch --tree-filter "rm -rf VeryLargeDirOrFileName" -f HEAD --all`

<https://git-scm.com/docs/git-filter-branch>

`git rev-list --objects --all | grep "$(git verify-pack -v .git/objects/pack/*.idx | sort -k 3 -n | tail -10 | awk '{print$1}')"`


### Split a subdirectory into its own repo

`git subtree push --prefix examplesubdir https://bitbucket.org/USERNAME/examplereponame master`
> whoa, one line to take a subdirectory and push it into the waiting empty new repo

<https://developer.atlassian.com/blog/2015/05/the-power-of-git-subtree/>


