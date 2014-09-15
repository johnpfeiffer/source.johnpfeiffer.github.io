#!/bin/bash
git pull
GITMESSAGE=$(git log -n 1 | tr -d '\n')
OUTPUT="../output-johnpfeiffer.bitbucket.org"
./clean-output.sh "$OUTPUT"
echo "$GITMESSAGE"
pelican content
cp -a ./output/* "$OUTPUT"

rm -rf ./output
rm -rf ./cache
rm -f *.pyc

cd "$OUTPUT"
git add --all .
git commit -m "source $GITMESSAGE"
git push
