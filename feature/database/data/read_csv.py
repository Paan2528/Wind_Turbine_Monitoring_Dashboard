import pandas as pd

# read file CSV of opendata with conditon messy column (on_bad_lines="skip")
# mort of open data is complicate to read because some column missing
# can read file with carecther (ä,ü,ö)

df = pd.read_csv("opendata.csv",
                 sep=";",
                 encoding="latin1",
                 on_bad_lines="skip")

print(df.info())
print(df.columns.tolist())
print(df.head())
