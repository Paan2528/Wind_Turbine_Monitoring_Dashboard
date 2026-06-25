
import sqlite3
import pandas as pd
from pathlib import Path


#  Low wind alert  <20m/S
#  Hight wind warning >20m/s
#  Emergency Shutdown alert >25m/s
#  Low power output alert <100kw but wind_speed >10
# ++++++++ Alert Table +++++++++
# id, turbine_id, time, alert_type, severity, message, wind_speed

BASE_DIR = Path(__file__).resolve().parent.parent / "database" / "data"
db_path = BASE_DIR / "wind_turbine.db"
print(db_path)

conn = sqlite3.connect(db_path)
weather_df = pd.read_sql("SELECT * FROM weather_data", conn)
wind_speed = pd.read_sql("SELECT * FROM weather_data", conn)

print("wind speed:", wind_speed)

###########################


alerts = []
# example: check latest weather row

latest_weather = weather_df.iloc[-1]
wind_speed = latest_weather["wind_speed"]
print("wind speed:", wind_speed)

if wind_speed > 20:
    alerts.append({
        "alert_type": "Hight wind speed",
        "message": f"wind speed is too hight: {wind_speed} m/s",
        "severity": "hight"
    })
elif wind_speed < 3:
    alerts.append({
        "alert_type": "Low wind speed",
        "message": f"wind speed is too low: {wind_speed} m/s",
        "severity": "low"
    })
else:  # wind_speed <= 3 and wind_speed <= 20
    alerts.append({
        "alert_type": "Appropriate wind speed",
        "message": f"wind speed is appropriate: {wind_speed} m/s",
        "severity": "appropriate"
    })

alerts_df = pd.DataFrame(alerts)
if not alerts_df.empty:
    alerts_df.to_sql(
        "alerts",
        conn,
        if_exists="append",
        index=False
    )

print(alerts)
print(alerts_df)
conn.close()
print("Alert system checked.")
