#!/usr/bin/python
#
# Initial sanity explorations/sanity checks on the BRFSS xpt dumps.

from collections import defaultdict
import math
import zipfile
import xport

year = 1990

if year == 2008:
  datafile = 'CDBRFS08ASC.ZIP'
elif year == 2000:
  datafile = 'cdbrfss2000asc.zip'
elif year == 1990:
  datafile = 'cdbrfss1990asc.zip'

z = zipfile.ZipFile(datafile, 'r')
assert len(z.namelist()) == 1
f = z.open(z.namelist()[0], 'r')

pound_in_kg = 0.45359237
inch_in_meters = 0.0254
bmi_conversion_factor = pound_in_kg / inch_in_meters ** 2

bmis = defaultdict(int)

for n, line in enumerate(f):
  line = line.rstrip()
  if year == 2008:
    assert len(line) == 1294, '%d != 1294' % len(line)
  if year == 2000:
    assert len(line) == 892, '%d != 892' % len(line)
  if year == 1990:
    assert len(line) == 450, '%d != 450' % len(line)
    
  state = line[0:2]
  #weight2 = line[118:118 + 4]
  #height3 = line[122:122 + 4]
  if year == 2008:
    bmi = line[1258:1258 + 4]
  elif year == 2000:
    bmi = line[861:861 + 3]
  elif year == 1990:
    # no bmi for 1990, but it does have height/weight
    weight = line[99:99+3]
    height = line[102:102+3]
    if weight == '999' or height == '999' or weight == '777' or height == '777':
      # 777 = Don't Know/Not Sure, 999 = Refused
      bmi = '9999'
    else:
      try:
        weight_lbs = int(weight)
        height_ins = 12 * int(height[0:1]) + int(height[1:3])
        bmi = bmi_conversion_factor * weight_lbs / (height_ins ** 2)
        bmi = '%04d' % int(100 * bmi)
      except:
        continue

  if bmi != '9999' and bmi != '999':
    bmis[int(bmi[0:2])] += 1  # this effectively rounds

  # TODO(danvk): sampling

  # print '%s, %s, %s, %s' % (state, weight2, height3, bmi)

  #last_was_blank = True
  #start_last = 0
  #for i, c in enumerate(line):
  #  blank = (c == ' ')
  #  if blank != last_was_blank:
  #    if blank:
  #      print '%4d - %4d' % (1 + start_last, i)
  #    last_was_blank = blank
  #    start_last = i

  # if n > 10: break

# Collapse the tail into a single bucket
for x in xrange(51, 100):
  bmis[50] += bmis[x]
  del bmis[x]
  

for x in xrange(10, 51):
  print '%2d\t%d' % (x, bmis[x])






# The data file is really big, so it makes sense to keep it zipped.
#datafile = 'CDBRFS08.XPT'
#reader = xport.XportReader(datafile)
#
#row = reader.next()
#for k in sorted(row.keys()):
#  print '%s: %s' % (k, row[k])
