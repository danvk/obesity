#!/usr/bin/python
#
# Notes:
# - There are some "888" values which should also be discarded.
# - The "integer" in the table does not enforce int-ness. We must.
# - Should track Gender.
# - Have a few odd non-integer height values.

import gzip
import json
import sys
import sqlite3
import convert

assert len(sys.argv) == 2, (
  'Usage: %s year' % sys.argv[0])

year = int(sys.argv[1])

conn = sqlite3.connect('brfss.db')
# c = conn.cursor()
z = gzip.GzipFile(filename='data/json/%s.json.gz' % year)

table_schema = """
create table brfss (
  year integer,
  weight_lbs integer,
  height_ins integer,
  record_weight float,
  state string,
  is_male boolean,
  age_years integer
);
"""

def ExtractWeight(d):
  global year
  if year <= 2003:
    w = d['WEIGHT']
    if not w or w == 777 or w == 888 or w == 999: return None
    return w

  w = d['WEIGHT2']
  if not w or w == 7777 or w == 8888 or w == 9999: return None

  if w > 9000:
    # metric
    weight_kg = w - 9000
    return int(round(2.20462262 * weight_kg))

  return w


def ExtractHeight(d):
  global year

  if year <= 2003:
    f_in = d['HEIGHT']
    if not f_in or f_in == 777 or f_in == 888 or f_in == 999: return None

    # There are a few oddly-coded values like 5, 5.5, 5.7, 5.9
    if f_in < 100: return None

    f = int(f_in / 100)
    i = f_in % 100

    if i > 12: return None  # miscode
    return 12 * f + i

  if year == 2004:
    f_in = d['HEIGHT2']
  else:
    f_in = d['HEIGHT3']

  if not f_in or f_in == 7777 or f_in == 8888 or f_in == 9999: return None

  if f_in > 9000:
    # Metric
    h_cm = f_in - 9000
    return int(round(h_cm / 2.54))

  f = int(f_in / 100)
  i = f_in % 100
  
  if i > 12: return None  # miscode
  if f > 8: return None  # miscode
  return 12 * f + i


def ExtractState(d):
  return convert.fips_to_state[d['_STATE']]


def ExtractIsMale(d):
  # 1 = Male, 2 = Female
  assert 'SEX' in d
  if d['SEX'] == 1:
    return True
  elif d['SEX'] == 2:
    return False
  return None


def ExtractAgeYears(d):
  # 18-99 = Age on last birthday
  # 07 = Don't Know/Not Sure
  # 09 = Refused
  assert 'AGE' in d
  age = d['AGE']
  if age == None: return None
  assert age == int(age)

  if age == 7 or age == 9: return None
  assert 18 <= age <= 99
  return age


def InsertABunch(conn, tuples):
  return conn.executemany("""insert into brfss values (?, ?, ?, ?, ?, ?, ?)""", tuples)


try:
  conn.execute(table_schema)
except sqlite3.OperationalError as e:
  # table already exists
  pass


tuples = []
for idx, line in enumerate(z):
  d = json.loads(line)

  weight_lbs = ExtractWeight(d)
  height_ins = ExtractHeight(d)
  state_name = ExtractState(d)
  is_male = ExtractIsMale(d)
  age_years = ExtractAgeYears(d)
  record_weight = d['_FINALWT']

  # batch insertions into 1000 row chunks. This is about a 6x speedup.
  tuples.append((year, weight_lbs, height_ins, record_weight, state_name, is_male, age_years))
  if len(tuples) == 1000:
    cursor = InsertABunch(conn, tuples)
    assert cursor.rowcount == 1000
    conn.commit()
    tuples = []
    if idx % 10000 == 9999:
      print '%d...' % (1 + idx)

if tuples:
  InsertABunch(conn, tuples)

conn.commit()
conn.close()
