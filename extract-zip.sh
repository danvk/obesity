#!/bin/bash
set -o errexit

test ! -z $1

# creates a file named something like "CDBRFS84.XPT"
unzip $1

# make sure one and exactly one file is extracted.
if [ -e data.xpt ]; then
  rm data.xpt
fi
test $(ls *.XPT *.xpt | wc -l) -eq 1

mv $(ls *.XPT *.xpt) data.xpt

echo Success: extracted $1 -\> data.xpt
