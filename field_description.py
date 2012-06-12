#!/usr/bin/env python
#
# Prints out summary data about all the fields in an XPT file.
#
# Usage: ./field_description.py path/to/xpt[.zip]

import StringIO
import sys
import xport
import zipfile

assert len(sys.argv) == 2
path = sys.argv[1]

f = path
if path.endswith('.zip') or path.endswith('.ZIP'):
  # xport needs something with a 'seek' method.
  # We read in the first 100K and put it in a StringIO to make xport happy.
  zip_archive = zipfile.ZipFile(path)
  assert len(zip_archive.namelist()) == 1, (
      'Can only read .zip files containing a single xpt file.')
  zip_file = zip_archive.open(zip_archive.namelist()[0])
  f = StringIO.StringIO(zip_file.read(100000))

reader = xport.XportReader(f)

for f in reader.fields:
  print '%4d %10s (%d) %s' % (f['npos'], f['name'], f['field_length'], f['label'])
