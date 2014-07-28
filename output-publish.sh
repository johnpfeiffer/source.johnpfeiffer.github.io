#!/bin/bash
OUTPUT="../../output-johnpfeiffer.bitbucket.org"
if [ ! -d "$OUTPUT" ]; then 
  echo "requires dir $OUTPUT"
fi
git checkout source
git pull
GITMSG=$(git log -n 1)
./output-clean.sh
pelican content

ls -ahl ../

cp -a ./output/* "$OUTPUT"
rm -rf ./output
rm -rf ./cache
rm -f *.pyc
cd "$OUTPUT"
git checkout source
git pull
git checkout master
git pull
git add --all .
git commit -m "source $GITMSG"
git push
