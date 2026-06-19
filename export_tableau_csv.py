import psycopg2
import pandas as pd
import os
from dotenv import load_dotenv

load_dotenv()

conn = psycopg2.connect(
    host=os.getenv("DB_HOST"),
    database=os.getenv("DB_NAME"),
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD"),
    port=os.getenv("DB_PORT"),
)

# Export all mart tables as CSV for Tableau
tables = [
    "analytics.mart_market_overview",
    "analytics.mart_skill_demand", 
    "analytics.mart_salary_benchmarks",
    "analytics.mart_dashboard_kpis"
]

os.makedirs("data/tableau", exist_ok=True)

for table in tables:
    df = pd.read_sql(f"SELECT * FROM {table}", conn)
    filename = table.split(".")[1]
    df.to_csv(f"data/tableau/{filename}.csv", index=False)
    print(f"Exported {filename}.csv — {len(df)} rows")

conn.close()
print("All Tableau CSVs exported!")
