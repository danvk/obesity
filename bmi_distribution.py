from collections import defaultdict
import sqlite3

conn = sqlite3.connect('brfss.py')
c = conn.cursor()

# Sum of all record weights in each year.
year_weights = defaultdict(float)

# year -> floor(bmi) -> sum of record_weights
bmi_weights = defaultdict(lambda: defaultdict(float))

# Get the total weighting for each year.
result = c.execute("""select year, record_weight, weight_lbs, height_ins from brfss""")
for row in result:
  year, record_weight, weight_lbs, height_ins = row

  # Ignore "don't know" and "refused to say" and miscodes.
  if not weight_lbs or not height_ins: continue

  year_weights[year] += record_weight
  bmi_
