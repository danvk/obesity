'''Routines to pull data and make samples from it'''

import csv
import sys
import numpy as np
from operator import itemgetter
import sqlite3

renorm = lambda arr: arr/arr.sum()
np.random.seed(834296)

def tofloat(x):
    try:
        return float(x)
    except:
        return np.nan

def pull_data(f):
    '''Gets the data in to year -> [ht_lbs, wt_lbs, rec_wt] as array'''
    yearly = {}
    con = sqlite3.connect(f)
    con.row_factory = sqlite3.Row

    cur = con.cursor()
    cur.execute("select * from brfss;")

    micro = itemgetter('weight_lbs', 'height_ins', 'record_weight')
    for i,row in enumerate(cur):
        yearly.setdefault(row['year'],[]).append(map(tofloat,micro(row)))

    for yr in yearly:
        yearly[yr] = np.asarray(yearly[yr])
    return yearly

def sample_year(year, n=1000):
    '''assumes the last row is the record weight'''
    wt = np.random.multinomial(n, renorm(year[:,-1]))
    s = np.repeat(year, wt, 0)
    return s


def main():
    data = pull_data(sys.argv[1])
    test = sample_year(data[1984],20)
    print test

if __name__ == "__main__":
    main()
