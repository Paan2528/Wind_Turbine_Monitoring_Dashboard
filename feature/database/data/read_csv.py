import pandas as pd

# read file CSV of opendata with conditon messy column (on_bad_lines="skip")
# mort of open data is complicate to read because some column missing
# can read file with carecther (ä,ü,ö)

df = pd.read_csv("opendata.csv",
                 sep=";",
                 encoding="latin1",
                 on_bad_lines="skip")

# structure of DataFrame, how many rows, column or what kind of column type
print(df.info())
# name of column
print(df.columns.tolist())
# print first 5 rows
print(df.head())
