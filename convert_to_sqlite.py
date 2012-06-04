#!/usr/bin/python
#
# create table brfss (year integer, weight_lbs integer, height_in integer, record_weight float);

import gzip
import json
import sys
import sqlite3

assert len(sys.argv) == 2, (
  'Usage: %s year' % sys.argv[0])

year = int(sys.argv[1])

conn = sqlite3.connect('brfss.db')
c = conn.cursor()
z = gzip.GzipFile(filename='data/json/%s.json.gz' % year)


def ExtractWeight(d):
  global year
  if year <= 2003:
    w = d['WEIGHT']
    if not w or w == 777 or w == 999: return None
    return w

  w = d['WEIGHT2']
  if not w or w == 7777 or w == 9999: return None

  if w > 9000:
    weight_kg = w - 9000
    return int(round(2.20462262 * weight_kg))


def ExtractHeight(d):
  global year

  if year <= 2003:
    f_in = d['HEIGHT']
    if not f_in or f_in == 777 or f_in == 999: return None

    f = int(f_in / 100)
    i = f_in % 100

    if i > 12: return None  # miscode
    return 12 * f + i

  if year == 2004:
    h = w['HEIGHT2']
  else:
    h = w['HEIGHT3']

  if not h or h == 7777 or h == 9999: return None

  if h > 9000:
    # Metric
    h_cm = h - 9000
    return int(round(h_cm / 2.54))

  f = int(f_in / 100)
  i = f_in % 100
  
  if i > 12: return None  # miscode
  if f > 8: return None  # miscode
  return 12 * f + i



for idx, line in enumerate(z):
  d = json.loads(line)

  weight_lbs = ExtractWeight(d)
  height_ins = ExtractHeight(d)
  record_weight = d['_FINALWT']

  c.execute("""insert into brfss values (?, ?, ?, ?)""",
              (year, weight_lbs, height_ins, record_weight))
  conn.commit()

  if idx % 1000 == 0:
    print '%d...' % idx

conn.close()
