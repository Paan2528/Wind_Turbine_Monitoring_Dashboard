import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

####################################################
BASE_DIR = Path(__file__).parent
turbine_db = BASE_DIR / "turbine_clean.db"
weather_db = BASE_DIR / "wind_turbine.db"

conn_turbine = sqlite3.connect(turbine_db)
df = pd.read_sql("SELECT * FROM turbine_clean", conn_turbine)
conn_turbine.close()

conn_weather = sqlite3.connect("wind_turbine.db")
weather_df = pd.read_sql("SELECT * FROM weather_data", conn_weather)
conn_weather.close()

############################


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
    0.5 * rho * rotor_area * (weather_df["wind_speed"] ** 3)
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
