import sqlite3
import pandas as pd

conn = sqlite3.connect("wind_turbine.db")

df = pd.read_sql_query("SELECT * FROM turbines LIMIT 5", conn)

print(df)
conn.close()
