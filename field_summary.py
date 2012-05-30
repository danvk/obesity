#!/usr/bin/python

from collections import defaultdict
import gzip
import json

def GetFieldsFromZipFile(path):
  z = gzip.GzipFile(filename=path)
  line = z.readline()
  d = json.loads(line)
  return sorted(d.keys())


counts = defaultdict(int)

for year in xrange(1984, 2011):
  for field in GetFieldsFromZipFile('data/json/%s.json.gz' % year):
    counts[field] += 1

pairs = reversed(sorted([(c, k) for k, c in counts.iteritems()]))

for count, field in pairs:
  print '%2d %s' % (count, field)
