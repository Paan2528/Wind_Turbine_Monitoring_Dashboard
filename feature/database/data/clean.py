# clean data
# add value to missing rows or add value to none rows
import pandas as pd

df = pd.read_csv("/Users/yatoum/Documents/Taschenrecner/Wind_Turbine_Monitoring_Dashboard/feature/database/data/opendata.csv",
                 sep="\t",
                 encoding="latin1",
                 on_bad_lines="skip")
print(df.info())
print(df.head())
print(df.describe())
# find missing value
print(df.isnull().sum())
# deleat missing
print(df.dropna())
