#!/usr/bin/env python
"""
Generates tabbed data on mean & median BMI broken down by year and gender.
"""

import brfss

def ExtractDeciles(values_weights, total_weight=None):
    """Returns the deciles given an unordered (value, weight) array.
    
    Side effect: Sorts the array.
    """
    if not total_weight:
        total_weight = sum([w for v, w in values_weights])

    values_weights.sort()

    tally = 0.0
    out = []
    for v, w in values_weights:
        tally += w
        for i in xrange(len(out),11):
            # small adjustment for summation error
            if tally+.0001 >= total_weight * (i*.1):
                out.append(v)
    try:
        assert len(out) == 11
    except:
        print(out,tally,total_weight,values_weights[:10])
        raise IndexError
    return out


def ExtractMean(values_weights, total_weight=None):
    """Returns the mean value given an unordered (value, weight) array."""
    if not total_weight:
        total_weight = sum([w for v, w in values_weights])

    return sum([w*v for v, w in values_weights]) / total_weight


def main():
    header = ['year']
    for t in ['Both','Male','Female']:
        for k in ['Mean'] + ['%ith_pctile'%(i*10) for i in xrange(1,10)]:
            header.append("%s-%s"%(t,k))
    print '\t'.join(header)
    for year, rec_it in brfss.RecordsByYear():
        # compute mean & median per-year
        bmis = [[], []]  # (bmi, record_weight) for [male, female]

        for rec in rec_it:
            bmi = brfss.BMIForRecord(rec)
            if not bmi: continue
            rec_wt = rec['record_weight']

            idx = 0 if rec['is_male'] else 1

            bmis[idx].append((bmi, rec_wt))

        male_mean = ExtractMean(bmis[0])
        male_deciles = ExtractDeciles(bmis[0])[1:-1]
        female_mean = ExtractMean(bmis[1])
        female_deciles = ExtractDeciles(bmis[0])[1:-1]

        both_bmis = bmis[0] + bmis[1]
        both_mean = ExtractMean(both_bmis)
        both_deciles = ExtractDeciles(both_bmis)[1:-1]

        
        
        print '\t'.join([str(x) for x in
          [year,
           both_mean] + both_deciles + \
           [male_mean] + male_deciles +  \
           [female_mean] + female_deciles])


if __name__ == "__main__":
    main()
