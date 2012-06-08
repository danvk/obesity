#!/usr/bin/env python
"""Prints out the years in which a field is present.

Usage: ./field_years FIELDNAME
"""

import glob
import gzip
import json
import os
import sys
import itertools

def year_from_name(fname):
    return int(os.path.basename(fname).split('.')[0])


def extract_first_record(fname):
    f = gzip.GzipFile(filename=fname)
    row = f.next()
    return json.loads(row.strip())


def main():
    assert len(sys.argv) == 2, (
      "Usage: %s FIELD_NAME" % sys.argv[0])
    field_name = sys.argv[1]

    files = glob.iglob('data/json/*.gz')
    years = {}
    for fname in sorted(files):
        year = year_from_name(fname)
        d = extract_first_record(fname)
        years[year] = field_name in d

    all_years = sorted(years.keys())
    states = [k if years[k] else None for k in all_years]

    runs = itertools.groupby(states, lambda x: not not x)
    present_runs = []
    for present, years in runs:
      if not present: continue

      years = list(years)
      first = years[0]
      last = years[-1]
      if first == last:
        present_runs.append(str(first))
      else:
        present_runs.append('%d-%d' % (first, last))

    if present_runs:
      print 'Present: %s' % (', '.join(present_runs))
    else:
      print 'Not present in any year.'


if __name__ == "__main__":
    main()
