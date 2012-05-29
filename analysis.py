#!/usr/bin/python
import math
import xport
from collections import defaultdict

bmi_file = 'BMX_F.xpt'
demo_file = 'DEMO_F.xpt'

def ReadXport(path, field_map, users):
  for row in xport.XportReader(path):
    assert 'SEQN' in row
    seqn = row['SEQN']
    for k, v in field_map.iteritems():
      if k in row:
        users[seqn][v] = row[k]
    

field_map = {
  'BMXBMI': 'bmi',
  'RIDAGEYR': 'age',
  'RIAGENDR': 'gender'
  'WTINT2YR': 'weighting'
}

people = defaultdict(dict)
ReadXport(bmi_file, field_map, people)
ReadXport(demo_file, field_map, people)

print len(people)
count = 0
for k, v in people.iteritems():
  print '%s -> %s' % (k, v)
  count += 1
  if count >= 10: break

#print missing
#print count
#print 'Average: %.2f' % (1.0 * tally / count)
#
#for base in xrange(low, 1 + high):
#  print '%.2f\t%d' % (base, bmis[base])


def Bucket(x):
  return int(math.floor(x))
  #"""Buckets into half integers, e.g. 1.75 -> '[1.50, 2.00)'."""
  #lower = math.floor(x * 2) / 2
  #return '[%2.2f,%2.2f)' % (lower, lower + 0.5)
