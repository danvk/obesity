#!/usr/bin/python

"""
Generates per-year distributions of height, weight and BMI.

Scanning the entire database takes ~40 seconds.
"""

from collections import defaultdict
import sys
import sqlite3

pound_in_kg = 0.45359237
inch_in_meters = 0.0254
bmi_conversion_factor = pound_in_kg / inch_in_meters ** 2

conn = sqlite3.connect('brfss.db')
c = conn.cursor()

# Sum of all record weights in each year.
year_weights = defaultdict(float)

# year -> height_ins -> sum of record_weights
heights = defaultdict(lambda: defaultdict(float))

# year -> weight_lbs -> sum of record_weights
weights = defaultdict(lambda: defaultdict(float))

# year -> floor(bmi) -> sum of record_weights
bmis = defaultdict(lambda: defaultdict(float))

# year -> # of records tossed
tossed = defaultdict(int)

# Get the total weighting for each year.
result = c.execute("""select year, record_weight, weight_lbs, height_ins from brfss""")
for idx, row in enumerate(result):
  if idx % 10000 == 0:
    sys.stderr.write('%d...\n' % idx)

  year, record_weight, weight_lbs, height_ins = row

  # Ignore "don't know" and "refused to say" and miscodes.
  if not weight_lbs or not height_ins:
    tossed[year] += 1
    continue

  # Bugs:
  if height_ins < 10: continue

  # People tend to report weights as multiples of 5
  weight_lbs = 5 * round(weight_lbs / 5)

  assert record_weight > 0
  year_weights[year] += record_weight
  heights[year][height_ins] += record_weight
  weights[year][weight_lbs] += record_weight

  bmi = int(round(bmi_conversion_factor * weight_lbs / height_ins ** 2))

  bmis[year][bmi] += record_weight

conn.close()


def Normalize(d):
  """Normalizes a two-level dict so that sum(d[k].values()) == 1 for all k."""
  for k1, d2 in d.iteritems():
    total = sum(d2.itervalues())
    for k2, v2 in d2.iteritems():
      d2[k2] = v2 / total


def SecondaryKeys(d):
  """Returns the set of all secondary keys in a two-level dict."""
  keys = set()
  for k1, d2 in d.iteritems():
    keys.update(d2.iterkeys());
  return keys


def DistributionAsJs(d):
  """Returns distributions in two variables as valid JavaScript."""
  keys1 = sorted(d.keys())
  keys2 = sorted(SecondaryKeys(d))
  
  # Header
  js = '"%s,%s\\n" +' % ('Year', ','.join([str(x) for x in keys2]))
  js += '\n'
  
  for k1 in keys1:
    dk = d[k1]
    js += '"%s,%s\\n" +' % (k1, ','.join([('%.4f' % dk[k2] if k2 in dk else '') for k2 in keys2]))
    js += '\n'

  return js + '""\n'


Normalize(heights)
Normalize(weights)
Normalize(bmis)


f = file('charts/height.js', 'w')
f.write('var heights_csv =')
f.write(DistributionAsJs(heights));
f.close()

f = file('charts/weight.js', 'w')
f.write('var weights_csv =')
f.write(DistributionAsJs(weights));
f.close()

f = file('charts/bmi.js', 'w')
f.write('var bmi_csv =')
f.write(DistributionAsJs(bmis));
f.close()
