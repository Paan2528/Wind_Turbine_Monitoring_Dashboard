import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

BASE_DIR = Path(__file__).parent
db_path = BASE_DIR / "turbine_clean.db"

conn = sqlite3.connect(db_path)

query = """SELECT gemeinde
FROM turbine_clean
"""
df = pd.read_sql(query, conn)
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
