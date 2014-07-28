#!/bin/bash
OUTPUT="../../output-johnpfeiffer.bitbucket.org/BLOG"
ls "$OUTPUT"
if [ ! -d "$OUTPUT" ]; then
  echo "requires dir $OUTPUT"
fi
cd "$OUTPUT"
git branch
rm -rf ./output
rm -rf ./cache
rm -f *.pyc

SOURCE=../*
for F in $SOURCE; do
  if [ -d "$F" ] && [ "$F" == "../BLOG" ] ; then
    printf "$F\n\n"
  else
    # printf "$F\n"
    rm -rf "$F"
  fi
done
