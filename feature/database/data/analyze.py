import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

####################################################
BASE_DIR = Path(__file__).parent
db_path = BASE_DIR / "turbine_clean.db"
conn = sqlite3.connect(db_path)

df = pd.read_sql(
    "SELECT * FROM turbine_clean",
    conn
)

BASE_DIR = Path(__file__).parent
db_path = BASE_DIR / "wind_turbine.db"
conn = sqlite3.connect(db_path)
hourly_df = pd.read_sql(
    "SELECT * FROM weather_data",
    conn
)

query = """SELECT *
FROM turbine_clean
"""
df = pd.read_sql(query, conn)
###############################
conn = sqlite3.connect(db_path)

tables = pd.read_sql(
    "SELECT name FROM sqlite_master WHERE type='table'",
    conn
)

print(tables)

conn.close()
############################

conn.close()

city_count = df["gemeinde"].value_counts().head(10)

plt.figure(figsize=(10, 6))
city_count.plot(kind="bar")

plt.title("Top 10 Cities with Wind Turbines")
plt.xlabel("City")
plt.ylabel("Number of Turbines")
plt.xticks(rotation=45)

plt.tight_layout()
plt.show()

###################################################


###### Power calculate follower the time #######

turbine = df.iloc[0]

rotor_diameter = turbine["rotordurchmesser"]
rotor_area = turbine["rotor_area"]

rho = 1.225
cp = 0.4

weather_df["estimated_power_kw"] = (
    0.5 * rho * rotor_area * (weather_df["wind_speed_10m"] ** 3)
    * cp
)/1000

##### power_output VS wind_speed#####

plt.plot(
    weather_df["time"],
    weather_df["estimated_power_kw"]
)

plt.xlabel("Time")
plt.ylabel("Estimated Power (kW)")
plt.title("Estimated Power Output Over Time")
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()
