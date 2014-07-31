#!/bin/bash

rm -rf ./output
rm -rf ./cache
rm -f *.pyc

if [ $# -eq 1 ] ; then
  SOURCE=$1
fi
if [ ! -d "$SOURCE" ]; then
  echo "ERROR, require a directory $SOURCE"
  exit 1
else
  echo "$SOURCE"
  ls -ahl "$SOURCE"
  echo "DELETING..."
fi
for ITEM in $SOURCE/*
do
  if [ -d "$ITEM" ]; then
    rm -rf "$ITEM"
  else
    rm -f "$ITEM"
  fi
done

