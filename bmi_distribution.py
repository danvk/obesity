import sqlite3

conn = sqlite3.connect('brfss.py')
c = conn.cursor()

# Get the total weighting for each year.
result = c.execute("""select year, record_weight, weight_lbs, height_ins from brfss""")
