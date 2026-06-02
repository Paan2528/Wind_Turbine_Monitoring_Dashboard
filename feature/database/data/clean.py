# clean data
# read table (wind_turbine.db -> clean dat with pandas -> save to new table)

import sqlite3
import pandas as pd
from pathlib import Path
import numpy as np

print("Before cleaning:")
conn = sqlite3.connect("wind_turbine.db")

query = """
SELECT Gemeinde, Rotordurchmesser, temperature, wind_speed, wind_direction, weather_code, rain
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

##### calculate Rotor Area ############
# 1. clean Rotor Diameter
df["rotordurchmesser"] = (
    df["rotordurchmesser"]
    .astype(str)
    .str.replace(",", ".")
)
df["rotordurchmesser"] = pd.to_numeric(
    df["rotordurchmesser"],
    errors="coerce"
)
# 2. calculate Rotor Area
# A = π(r**2)
df["rotor_area"] = (
    np.pi * (df["rotordurchmesser"]/2) ** 2
)
# check data (roterdurchmess,rotor_area)
print(df[
    ["rotordurchmesser", "rotor_area"]
].head()
)
######################################
##### Calculate Power_Output#########
# power = 0.5 * are_density * roter_area * wind_speed

rho = 1.225
cp = 0.4

df["power_output"] = (
    0.5
    * rho
    * df["rotor_area"]
    * (df["wind_speed"] ** 3)
    * cp
)
# convert Watt to kW
df["power_output_kW"] = df["power_output"]/1000

##### check data######################
print(
    df[
        [
            "anlage",
            "rotordurchmesser",
            "rotor_area",
            "wind_speed",
            "power_output_kW"
        ]
    ].head()
)

#####################################

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


####### read wind_clean#######


query = """
SELECT Gemeinde, Rotordurchmesser, temperature, wind_speed, wind_direction, weather_code, rain
FROM turbine_clean
"""
result = pd.read_sql(query, conn)

# print(result)
conn.close()
