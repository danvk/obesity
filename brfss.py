"""
Helpful tools for dealing with BRFSS data.

BRFSS stands for "Behavioral Risk Factor Surveillance System".
"""

import itertools
import sqlite3


def AllRecords(year=None, filename='brfss.db', tablename='brfss'):
    """Returns an iterator over the entire BRFSS database.

    Each item is a dict from field name -> value.

    This should return instantly.

    See also RecordsByYear()
    """
    con = sqlite3.connect(filename)
    con.row_factory = sqlite3.Row
    if year:
      return con.execute("select * from %s where year = %s" % (tablename, year))
    else:
      return con.execute("select * from %s" % tablename)


def RecordsByYear(filename='brfss.db', tablename='brfss'):
    """Returns an iterator of (year, iterator of records for year)
    
    This takes ~1 minute to return.

    Use like:

      for year, rec_it in brfss.RecordsByYear():
        for rec in rec_it:
          pass
    """
    con = sqlite3.connect(filename)
    con.row_factory = sqlite3.Row

    return itertools.groupby(
        con.execute('select * from %s order by year' % tablename),
        lambda rec: rec['year'])


pound_in_kg = 0.45359237
inch_in_meters = 0.0254
bmi_conversion_factor = pound_in_kg / inch_in_meters ** 2
def BMIForRecord(d):
    """Returns BMI given a BRFSS Record dict or None."""
    global bmi_conversion_factor
    w = d['weight_lbs']
    h = d['height_ins']
    if not w or not h: return None

    return bmi_conversion_factor * w / h ** 2
