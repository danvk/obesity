#!/usr/bin/env python
'''Determines the non-null values for each json object specified in the first argument

usage: %prog "*.json"'''

import sys
import json
import glob
import gzip

def badval(v):
    if v == None: return True
    if v == 999: return True
    if v == 777: return True
    if v == 9999: return True
    if v == 7777: return True
    return False

def freq(f):
    '''Go through f and return the frequency of non-nulls for each variable'''
    vals = {}
    nulls = {}
    for row in f:
        row = json.loads(row.strip())
        for k,v in row.iteritems():
            if badval(v):
                nulls[k] = nulls.get(k,0) + 1.
            else:
                vals[k] = vals.get(k,0) + 1.

    out = {}
    for k,v in vals.iteritems():
        out[k] = v/(v+nulls.get(k,0))

    return out

def process(fname):
    f = gzip.GzipFile(filename=fname)
    year = fname.split('.')[0]
    out = freq(f)
    return year, out

def summary(rez):
    out = ""
    means = {}
    years = []
    for k,v in rez.iteritems():
        years.append(k)
        for kk,vv in v.iteritems():
            means.setdefault(kk,[]).append(vv)

    years = sorted(years)
    means = {k: sum(v)/len(years) for k,v in means.iteritems()}

    for k,v in sorted(means.items(),key=lambda x:x[1])[::-1]:
        out += str(k).rjust(20) + '\t' + '\t'.join(["%.02f"%(rez[y].get(k,0)) for y in years]) + '\n'

    return out

def main():
    rez = {}
    files = glob.iglob(sys.argv[1])
    for fname in files:
       year, out = process(fname) 
       rez[year] = out
    print(summary(rez))


if __name__ == "__main__":
    main()
