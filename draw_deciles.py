'''Takes deciles.tab and draws deciles'''

import numpy as np
import matplotlib as ma
ma.use('agg')
import matplotlib.pyplot as plt
import csv

def read(f):
    out = {}
    years = []
    for row in csv.DictReader(f, delimiter='\t'):
        years.append(row.pop('year'))
        for k in row:
            out.setdefault(k, []).append(row[k])
    return map(int,years), out

def main():
    years, data = read(open('deciles.tab'))
    for kind in ['Both','Male','Female']:
        plt.clf()
        plt.plot(years, data[kind + '-Mean'], c='red')
        for k in data:
            if 'pctile' in k and kind in k:
                plt.plot(years, data[k], c='grey')
        plt.xlim((years[0],years[-1]))
        plt.savefig('deciles-%s.png'%kind)

if __name__ == "__main__":
    main()
    
