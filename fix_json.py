#!/usr/bin/python
"""
R outputs JSON like:

{
 "X_WTFORHT": [ " 9530" ],
"X_POSTSTR": [ " 5157.09" ],
"X_FINALWT": [ " 10314.18" ],
"X_STATE": [ "17" ],
"X_STRATA": [ "1" ],
"X_STSTR": [ "171" ],
...
}

This puts full records on a single line and converts strings to numbers where
appropriate. So the data above becomes:

{ "X_WTFORHT": 9530, "X_POSTSTR": 5157.09, "X_FINALWT": 10314.18, "X_STATE": 17, ... }

"""

import re
import sys
import json

data = json.load(sys.stdin)
sys.stderr.write('Loaded %d records\n' % len(data))

# has a few false positives, like '1.2.3'
num_re = re.compile(r'^ *[0-9 .]+ *$')

for rec in data:
  for k, v in rec.iteritems():
    if not v: continue
    if len(v) == 1: v = v[0]
    if v and re.match(num_re, v):
      v = float(v)
    rec[k] = v
  print json.dumps(rec, separators=(',',':'), sort_keys=True)
