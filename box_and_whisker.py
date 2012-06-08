'''Box and whisker plots of obesity related data'''

import matplotlib as ma
ma.use('agg')
import matplotlib.pyplot as plt
import numpy as np
import sample_data
import sys


def main():
    data = sample_data.pull_data(sys.argv[1])
    samples = {}
    n = 1000
    for k,v in data.iteritems():
        samples[k] = sample_data.sample_year(v,n)

    years = samples.keys()

    rez = np.zeros((n, len(years)))

    for i,year in enumerate(years):
        rez[:,i] = samples[year][:,0]

    plt.boxplot(rez)

    plt.ylim((0,500))

    plt.savefig('boxplot_weight_byyear.png')

if __name__ == "__main__":
    main()
