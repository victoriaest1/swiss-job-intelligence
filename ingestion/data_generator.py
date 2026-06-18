import pandas as pd
import numpy as np
import random
import psycopg2
from faker import Faker
from datetime import date, timedelta
from dotenv import load_dotenv
import os

load_dotenv()
fake = Faker(['fr_CH', 'en_US'])
random.seed(42)

# ── SWISS COMPANIES ───────────────────────────────────────────
SWISS_COMPANIES = [
    # Zurich -- Finance & Big Tech
    "UBS", "Julius Baer", "Zuercher Kantonalbank", "Swiss Re",
    "Google Zurich", "Microsoft Zurich", "Zalando", "Spotify Zurich",
    "ABB", "Zurich Insurance", "Swisscom", "SIX Group",
    "Credit Suisse", "Vontobel", "Helvetia", "AXA Switzerland",
    "Baloise Group", "Adecco Group", "Dufry", "Georg Fischer",
    "Sulzer", "OC Oerlikon", "Schindler Group", "Sonova",
    "Straumann", "Tecan", "u-blox", "Sensirion",
    "Open Systems", "Avaloq", "Finnova", "Crealogix",

    # Basel -- Pharma & Life Sciences
    "Roche", "Novartis", "Lonza", "Syngenta",
    "Clariant", "Endress+Hauser", "Siegfried",
    "Bachem", "Dottikon", "Actelion", "Vifor Pharma",
    "Staeubli", "Mettler-Toledo", "Bruker",

    # Geneva -- International Organisations & Finance
    "Pictet Group", "Lombard Odier", "WHO", "ICRC",
    "WTO", "ILO", "UN Geneva", "CERN", "Geneva Trading",
    "UNHCR", "UNAIDS", "ITU", "WIPO",
    "Glencore", "Trafigura", "Vitol", "Mercuria",
    "Gunvor", "Freeport", "Louis Dreyfus",
    "Banque Cantonale de Geneve", "Edmond de Rothschild",

    # Lausanne -- Startups & Education
    "Nestle", "Logitech", "EPFL", "Philip Morris International",
    "IMD Business School", "Kudelski Group",
    "Bobst Group", "Tetra Pak", "Medtronic Lausanne",
    "Blueface", "Bestmile", "Sophia Genetics",
    "Anokion", "Aleva Neurotherapeutics",

    # Bern -- Federal & Insurance
    "Swiss Post", "BKW Energy", "Mobiliar",
    "Bernische Kraftwerke", "Swissmedic",
    "Federal IT Steering Unit", "Skyguide",
    "Bernmobil", "BERNEXPO",

    # Zug -- Fintech & Crypto Valley
    "Crypto Finance", "Cardano Foundation",
    "Ethereum Foundation", "Tezos Foundation",
    "Bitcoin Suisse", "SEBA Bank", "Sygnum Bank",
    "V-ZUG", "Siemens Switzerland", "Johnson & Johnson Zug",

    # Other Swiss Cities
    "Schaffner Group",       # Winterthur
    "Sulzer Pumps",          # Winterthur
    "Georg Fischer Piping",  # Schaffhausen
    "IWC Schaffhausen",      # Schaffhausen
    "Pilatus Aircraft",      # Stans/Lucerne
    "Emmi Group",            # Lucerne
    "Schurter",              # Lucerne
    "Buhler Group",          # St. Gallen
    "Huber+Suhner",          # St. Gallen
    "Raiffeisen Switzerland",# St. Gallen
    "Rivella",               # Rothrist
    "Migros",                # National
    "Coop",                  # National
    "Manor",                 # National
    "Digitec Galaxus",       # National
    "Competec",              # National
    "TX Group",              # National
    "Ringier",               # National
    "PubliGroupe",           # National
    "Tamedia",               # National
]

# ── JOB TITLES ────────────────────────────────────────────────
TITLES = [
    "Data Engineer", "Senior Data Engineer",
    "Data Scientist", "Senior Data Scientist",
    "Data Analyst", "Senior Data Analyst",
    "Analytics Engineer", "BI Developer",
    "Full Stack Engineer", "Backend Engineer",
    "Software Engineer", "ML Engineer",
]

# ── CITIES ───────────────────────────────────────────────────
CITIES = ["Zurich", "Basel", "Geneva", "Lausanne", "Bern",
          "Zug", "Winterthur", "Lucerne", "St. Gallen", "Lugano"]
CITY_WEIGHTS = [0.38, 0.20, 0.17, 0.12, 0.08,
                0.02, 0.01, 0.01, 0.005, 0.005]

CANTON_MAP = {
    "Zurich": "ZH",     "Basel": "BS",      "Geneva": "GE",
    "Lausanne": "VD",   "Bern": "BE",       "Zug": "ZG",
    "Winterthur": "ZH", "Lucerne": "LU",    "St. Gallen": "SG",
    "Lugano": "TI",
}

# ── INDUSTRIES ────────────────────────────────────────────────
INDUSTRIES = [
    "Finance & Banking", "Technology & SaaS",
    "Pharma & Biotech", "International Organisations",
    "Consulting", "Commodities & Trading", "Healthcare",
]
INDUSTRY_WEIGHTS = [0.28, 0.23, 0.16, 0.12, 0.10, 0.07, 0.04]

# ── SKILLS BY ROLE ────────────────────────────────────────────
SKILLS = {
    "Data Engineer":         "Python,SQL,dbt,Airflow,PostgreSQL,Docker",
    "Senior Data Engineer":  "Python,SQL,dbt,Spark,Kafka,AWS",
    "Data Scientist":        "Python,SQL,scikit-learn,XGBoost,TensorFlow",
    "Senior Data Scientist": "Python,R,PyTorch,SQL,MLflow,Docker",
    "Data Analyst":          "SQL,Power BI,Python,Excel,Tableau",
    "Senior Data Analyst":   "SQL,Power BI,Python,DAX,Tableau",
    "Analytics Engineer":    "dbt,SQL,Snowflake,Python,Power BI",
    "BI Developer":          "Power BI,DAX,SQL,Tableau,Excel",
    "Full Stack Engineer":   "TypeScript,React,Node.js,PostgreSQL,Docker",
    "Backend Engineer":      "Python,FastAPI,PostgreSQL,Redis,Docker",
    "Software Engineer":     "Python,Docker,Kubernetes,AWS,PostgreSQL",
    "ML Engineer":           "Python,PyTorch,MLflow,Docker,Kubernetes",
}

# ── SALARY RANGES ─────────────────────────────────────────────
SALARY_RANGES = {
    "Data Engineer":         (88000,  175000),
    "Senior Data Engineer":  (120000, 195000),
    "Data Scientist":        (90000,  185000),
    "Senior Data Scientist": (130000, 210000),
    "Data Analyst":          (72000,  130000),
    "Senior Data Analyst":   (95000,  148000),
    "Analytics Engineer":    (85000,  162000),
    "BI Developer":          (75000,  135000),
    "Full Stack Engineer":   (85000,  165000),
    "Backend Engineer":      (88000,  170000),
    "Software Engineer":     (85000,  168000),
    "ML Engineer":           (95000,  185000),
}


def generate_jobs(n: int = 5000) -> list:
    """Generate n realistic Swiss job postings."""
    jobs = []

    for _ in range(n):
        title    = random.choice(TITLES)
        city     = random.choices(CITIES, weights=CITY_WEIGHTS)[0]
        canton   = CANTON_MAP[city]
        industry = random.choices(INDUSTRIES, weights=INDUSTRY_WEIGHTS)[0]

        sal_range = SALARY_RANGES[title]
        sal_min   = random.randint(sal_range[0], sal_range[1] - 15000)
        sal_max   = sal_min + random.randint(15000, 40000)
        sal_mid   = (sal_min + sal_max) // 2

        days_ago    = random.randint(0, 365)
        date_posted = date.today() - timedelta(days=days_ago)

        jobs.append({
            "title":         title,
            "company":       random.choice(SWISS_COMPANIES),
            "city":          city,
            "canton":        canton,
            "salary_min":    sal_min,
            "salary_max":    sal_max,
            "salary_mid":    sal_mid,
            "skills":        SKILLS.get(title, "Python,SQL"),
            "industry":      industry,
            "remote":        random.random() < 0.41,
            "language":      random.choice(["English", "French+English", "French", "German+English"]),
            "date_posted":   date_posted,
            "experience_yr": random.randint(0, 8),
        })

    return jobs


def load_to_postgres(jobs: list) -> None:
    """Load job postings into PostgreSQL."""
    conn = psycopg2.connect(
        host=os.getenv("DB_HOST"),
        database=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        port=os.getenv("DB_PORT"),
    )
    cur = conn.cursor()

    # Clear existing data
    cur.execute("TRUNCATE TABLE raw_job_postings RESTART IDENTITY;")

    # Insert all jobs
    insert_query = """
        INSERT INTO raw_job_postings (
            title, company, city, canton,
            salary_min, salary_max, salary_mid,
            skills, industry, remote, language,
            date_posted, experience_yr
        ) VALUES (
            %(title)s, %(company)s, %(city)s, %(canton)s,
            %(salary_min)s, %(salary_max)s, %(salary_mid)s,
            %(skills)s, %(industry)s, %(remote)s, %(language)s,
            %(date_posted)s, %(experience_yr)s
        )
    """
    cur.executemany(insert_query, jobs)
    conn.commit()

    print(f"Loaded {len(jobs):,} job postings into PostgreSQL")

    cur.close()
    conn.close()


if __name__ == "__main__":
    print("Generating Swiss job market data...")
    jobs = generate_jobs(5000)
    print(f"Generated {len(jobs):,} job postings")
    print("Loading into PostgreSQL...")
    load_to_postgres(jobs)
    print("Done!")

    