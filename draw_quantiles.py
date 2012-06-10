'''Takes deciles.tab and draws quantiles'''

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
            if 'pctile' in k:
                pct = int(k.split('-')[1].split('th')[0])
                if pct%20==0:
                    plt.plot(years, data[k], c='grey')
        plt.xlim((years[0],years[-1]))
        plt.savefig('quantiles-%s.png'%kind)

if __name__ == "__main__":
    main()
    
