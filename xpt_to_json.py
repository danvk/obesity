#!/usr/bin/python
import math
import xport
import sys
import json

# via http://stackoverflow.com/questions/1447287/format-floats-with-standard-json-module
json.encoder.FLOAT_REPR = lambda f: ("%.10g" % f)

assert len(sys.argv) == 2
path = sys.argv[1]

reader = xport.XportReader(path)

for rec in reader:
  print json.dumps(rec, separators=(',',':'), sort_keys=True)
