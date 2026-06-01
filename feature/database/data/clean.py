# clean data
# read table (wind_turbine.db -> clean dat with pandas -> save to new table)

import sqlite3
import pandas as pd
from pathlib import Path

print("Before cleaning:")
conn = sqlite3.connect("wind_turbine.db")

query = """
SELECT Gemeinde, temperature, wind_speed, wind_direction, weather_code, rain
FROM turbines 
"""
result = pd.read_sql(query, conn)

print(result)
conn.close()

###########################################
conn = sqlite3.connect("wind_turbine.db")
df = pd.read_sql(
    "SELECT * FROM turbines",
    conn
)

# remove completely empty rows
df = df.dropna(how="all")

# remove duplicated rows
df = df.drop_duplicates()

# clean culumn names
df.columns = (
    df.columns
    .str.strip()
    .str.lower()
    .str.replace(" ", "_")
    .str.replace("_", "_")
)
# remove rows without city name if column existe
if "gemeinde" in df.columns:
    df = df.dropna(subset=["gemeinde"])

# fill missing text values
text_columns = df.select_dtypes(include="object").columns
df[text_columns] = df[text_columns].fillna("Unknown")

# fill missing nummeric values with 0
numeric_column = df.select_dtypes(include="number").columns
df[numeric_column] = df[numeric_column].fillna(0)

print("After clean:")
print(df.head())

BASE_DIR = Path(__file__).parent
db_path = BASE_DIR / "turbine_clean.db"

print("DB PATH:", db_path)

conn = sqlite3.connect(db_path)
df.to_sql(
    "turbine_clean",
    conn,
    if_exists="replace",
    index=False
)

# conn.close()
####### read wind_clean#######


query = """
SELECT Gemeinde, temperature, wind_speed, wind_direction, weather_code, rain
FROM turbine_clean
"""
result = pd.read_sql(query, conn)

# print(result)
conn.close()
