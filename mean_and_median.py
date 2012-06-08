#!/usr/bin/env python
"""
Generates tabbed data on mean & median BMI broken down by year and gender.
"""

import brfss

def ExtractMedian(values_weights, total_weight=None):
    """Returns the median value given an unordered (value, weight) array.
    
    Side effect: Sorts the array.
    """
    if not total_weight:
        total_weight = sum([w for v, w in values_weights])

    values_weights.sort()

    tally = 0.0
    for v, w in values_weights:
        tally += w
        # TODO(danvk): handle in-between case
        if 2 * tally >= total_weight:
            return v


def ExtractMean(values_weights, total_weight=None):
    """Returns the mean value given an unordered (value, weight) array."""
    if not total_weight:
        total_weight = sum([w for v, w in values_weights])

    return sum([w*v for v, w in values_weights]) / total_weight


def main():
    print '\tBoth\t\tMale\t\tFemale\t'
    print 'Year\tMean\tMedian\tMean\tMedian\tMean\tMedian'
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
        male_median = ExtractMedian(bmis[0])
        female_mean = ExtractMean(bmis[1])
        female_median = ExtractMedian(bmis[1])

        both_bmis = bmis[0] + bmis[1]
        both_mean = ExtractMean(both_bmis)
        both_median = ExtractMedian(both_bmis)

        print '\t'.join([str(x) for x in
          [year,
           both_mean, both_median,
           male_mean, male_median,
           female_mean, female_median]])


if __name__ == "__main__":
    main()
