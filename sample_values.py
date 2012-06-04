#!/usr/bin/python

import gzip
import json
import sys
from optparse import OptionParser
from collections import defaultdict

parser = OptionParser(usage='%s field year' % sys.argv[0])

parser.add_option("-n", "--num",
                  dest="num", type="int", default=20,
                  help="Number of values to print. Set to -1 for all.")

parser.add_option("-b", "--bucketed",
                  dest="bucketed", default=False, action="store_true",
                  help="Print 'value: count' pairs")

(options, args) = parser.parse_args()
if len(args) != 2:
  parser.print_usage()
  sys.exit(1)

year, field = int(args[0]), args[1]

z = gzip.GzipFile(filename='data/json/%s.json.gz' % year)

def GetRecord(line, field):
  d = json.loads(line)
  assert field in d
  return d[field]

buckets = defaultdict(int)
count = 0
for line in z:
  v = GetRecord(line, field)

  if options.bucketed:
    buckets[v] += 1
    continue

  print v
  count += 1
  if options.num > 0 and count == options.num:
    break

if options.bucketed:
  for k in sorted(buckets.keys()):
    print '%s: %s' % (k, buckets[k])
