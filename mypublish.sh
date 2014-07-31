#!/bin/bash
git pull
GITMESSAGE=$(git log -n 1)
OUTPUT="../output-johnpfeiffer.bitbucket.org"
./clean-output.sh "../output-johnpfeiffer.bitbucket.org"

pelican content
cp -a ./output/* ../output-johnpfeiffer.bitbucket.org

rm -rf ./output
rm -rf ./cache
rm -f *.pyc

cd "$OUTPUT"
git add --all .
git commit -m "source $GITMESSAGE"
git push
