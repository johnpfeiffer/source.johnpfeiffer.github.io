#!/bin/bash
rm -rf ./output
rm -rf ./cache
rm -f *.pyc
pelican content

SOURCE=../*
for F in $SOURCE; do
  if [ -d "$F" ] && [ "$F" == "../BLOG" ] ; then
    printf "$F\n\n"
  else
    # printf "$F\n"
    rm -rf "$F"
  fi
done

ls -ahl ../

cp -a ./output/* ../
rm -rf ./output
rm -rf ./cache
rm -f *.pyc
