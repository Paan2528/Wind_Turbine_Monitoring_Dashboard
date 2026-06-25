import pandas as pd
import sqlite3
import requests
from pathlib import Path

# read file CSV of opendata with conditon messy column (on_bad_lines="skip")
# mort of open data is complicate to read because some column missing
# can read file with carecther (ä,ü,ö)
BASE_DIR = Path(__file__).parent
csv_path = BASE_DIR / "opendata.csv"

df = pd.read_csv(csv_path,
                 sep="\t",
                 encoding="latin1",
                 on_bad_lines="skip")

# structure of DataFrame, how many rows, column or what kind of column type
print(df.info())
# name of column
print(df.columns.tolist())
# print first 5 rows
print(df.head())

############ current Weather API############

# find lat/lon from city name (Gemeinde)
city = df.loc[0, "Gemeinde"]

geo_url = "https://geocoding-api.open-meteo.com/v1/search"
geo_params = {
    "name": city,
    "count": 1,
    "language": "de",
    "format": "json"
}
geo = requests.get(geo_url, params=geo_params).json()
location = geo["results"][0]

lat = location["latitude"]
lon = location["longitude"]

########### call the hourly weather ###########################
weather_url = "https://api.open-meteo.com/v1/forecast"
weather_params = {
    "latitude": lat,
    "longitude": lon,
    "hourly": "temperature_2m,wind_speed_10m,wind_direction_80m,weather_code,rain",
    "forecast_days": 1
}


weather = requests.get(weather_url, params=weather_params).json()


# print(city)
# print(weather)
if "hourly" in weather:
    print(weather["hourly"])
else:
    print("No hourly weather found")


#########################################
# Weather API into the Table(Wind_Turbine.db)

weather_data_update = requests.get(weather_url, params=weather_params).json()

hourly = weather_data_update["hourly"]

hourly_df = pd.DataFrame({
    "time": hourly["time"],
    "temperature": hourly["temperature_2m"],
    "wind_speed": hourly["wind_speed_10m"],
    "wind_direction": hourly["wind_direction_80m"],
    "rain": hourly["rain"],

})

############# Table########################
# connect to SQLite database
conn = sqlite3.connect("wind_turbine.db")
hourly_df.to_sql(
    "weather_data",
    conn,
    if_exists="replace",
    index=False
)
result = pd.read_sql(
    "SELECT * FROM weather_data LIMIT 5",
    conn
)
print(result)

###### check table##############
tables = pd.read_sql(
    "SELECT name FROM sqlite_master WHERE type='table'",
    conn
)

print(tables)
###########################

conn.close()
print("Database created successfully!")
