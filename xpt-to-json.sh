#!/bin/bash
#
# Usage: ./xpt-to-json.sh 1984
# Reads data/xpt/1984.xpt.zip
# Writes data/json/1984.json.gz

set -o errexit
set -x

test ! -z $1

./extract-zip.sh data/xpt/$1.xpt.zip  # creates data.xpt
R -f xpt_to_json.R --args data.xpt | gzip -c > data/json/$1.json.gz
