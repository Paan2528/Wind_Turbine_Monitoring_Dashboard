
import sqlite3
import pandas as pd
from pathlib import Path


#  Low wind alert  <20m/S
#  Hight wind warning >20m/s
#  Emergency Shutdown alert >25m/s
#  Low power output alert <100kw but wind_speed >10
# ++++++++ Alert Table +++++++++
# id, turbine_id, time, alert_type, severity, message, wind_speed

BASE_DIR = Path(__file__).parent
turbine_db = BASE_DIR / "turbine_clean.db"
weather_db = BASE_DIR / "wind_turbine.db"

conn_turbine = sqlite3.connect(turbine_db)
df = pd.read_sql("SELECT * FROM turbine_clean", conn_turbine)
conn_turbine.close()

conn_weather = sqlite3.connect("wind_turbine.db")
weather_df = pd.read_sql("SELECT * FROM weather_data", conn_weather)
conn_weather.close()

###### check table##############
print(conn_turbine)
print(conn_weather)
###########################

alerts = []
# example: check latest weather row

latest_weather = weather_df.iloc[-1]
wind_speed = latest_weather["wind_speed"]
print(wind_speed)
