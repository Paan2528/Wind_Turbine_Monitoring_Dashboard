import pandas as pd
import sqlite3
import requests

# read file CSV of opendata with conditon messy column (on_bad_lines="skip")
# mort of open data is complicate to read because some column missing
# can read file with carecther (ä,ü,ö)

df = pd.read_csv("database/data/opendata.csv",
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

# call the current weather
weather_url = "https://api.open-meteo.com/v1/forecast"
weather_params = {
    "latitude": lat,
    "longitude": lon,
    "current": "temperature_2m,wind_speed_10m,wind_direction_10m,weather_code"
}

weather = requests.get(weather_url, params=weather_params).json()

print(city)
print(weather)
if "current" in weather:
    print(weather["current"])
else:
    print("No current weather found")


#########################################
# Weather API into the Table(Wind_Turbine.db)
weather_data_update = requests.get(weather_url, params=weather_params).json()

current = weather_data_update["current"]

df["temperature"] = current["temperature_2m"]
df["wind_speed"] = current["wind_speed_10m"]
df["wind_direction"] = current["wind_direction_10m"]
df["weather_code"] = current["weather_code"]

print(weather_data_update)
############# Table########################
# connect to SQLite database
conn = sqlite3.connect("wind_turbine.db")

# that's creat only one table
df.to_sql(
    "turbines",
    conn,
    if_exists="replace",
    index=False
)


conn.close()
print("Database created successfully!")
