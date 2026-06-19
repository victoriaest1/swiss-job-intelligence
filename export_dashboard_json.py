import psycopg2
import json
import os
from dotenv import load_dotenv

load_dotenv()

def export_dashboard_data():
    conn = psycopg2.connect(
        host=os.getenv("DB_HOST"),
        database=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        port=os.getenv("DB_PORT"),
    )
    cur = conn.cursor()

    # KPIs
    cur.execute("SELECT total_postings, avg_salary_chf, remote_pct, total_companies, total_cities FROM analytics.mart_dashboard_kpis")
    kpi = cur.fetchone()

    # City data
    cur.execute("""
        SELECT city_clean, SUM(postings_count) as postings,
               ROUND(AVG(avg_salary_chf)) as avg_salary,
               ROUND(AVG(remote_pct), 1) as remote_pct
        FROM analytics.mart_market_overview
        GROUP BY city_clean
        ORDER BY postings DESC
    """)
    cities = [{"city": r[0], "postings": int(r[1]), "avg_salary": int(r[2]), "remote_pct": float(r[3])} for r in cur.fetchall()]

    # Top skills
    cur.execute("""
        SELECT skill, SUM(job_count) as total, ROUND(AVG(avg_salary_chf)) as avg_salary
        FROM analytics.mart_skill_demand
        GROUP BY skill
        ORDER BY total DESC
        LIMIT 15
    """)
    skills = [{"skill": r[0], "count": int(r[1]), "avg_salary": int(r[2])} for r in cur.fetchall()]

    # Monthly trend
    cur.execute("""
        SELECT TO_CHAR(month_year, 'Mon') as month, SUM(postings_count) as postings
        FROM analytics.mart_market_overview
        GROUP BY month_year
        ORDER BY month_year
    """)
    trend = [{"month": r[0], "postings": int(r[1])} for r in cur.fetchall()]

    dashboard_data = {
        "overview": {
            "total_postings": int(kpi[0]),
            "avg_salary_chf": int(kpi[1]),
            "remote_pct": float(kpi[2]),
            "total_companies": int(kpi[3]),
            "total_cities": int(kpi[4])
        },
        "cities": cities,
        "skills": skills,
        "monthly_trend": trend
    }

    os.makedirs("dashboard", exist_ok=True)
    with open("dashboard/dashboard_data.json", "w") as f:
        json.dump(dashboard_data, f, indent=2)

    cur.close()
    conn.close()
    print(f"Dashboard data exported successfully")
    print(f"  Total postings: {dashboard_data['overview']['total_postings']:,}")
    print(f"  Cities: {len(cities)}")
    print(f"  Skills: {len(skills)}")

if __name__ == "__main__":
    export_dashboard_data()
