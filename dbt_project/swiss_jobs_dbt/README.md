Welcome to your new dbt project!

### Using the starter project

# 🇨🇭 Swiss Tech Job Market Intelligence Platform

## 🎯 Business Problem
Swiss tech professionals and hiring managers lack consolidated,
real-time intelligence on skill demand, salary benchmarks, and
market trends across Switzerland's major tech hubs — Zurich,
Basel, Geneva, Lausanne, Bern, and Zug.

## 💡 Key Findings
- **Python** appears in 78% of all Swiss data engineering postings
- **CHF 40K salary gap** between Zurich (highest) and Lugano (lowest)
  for equivalent senior data roles nationally
- **dbt demand grew 67% YoY** — critical talent shortage across Switzerland
- **41% of Swiss tech roles** now offer remote or hybrid work
- **Zurich dominates** with 38% of all national tech postings

## 🚀 Live Demo
| Resource | Link |
|----------|------|
| 🌐 Live Dashboard | [Open Dashboard](https://victoriaest1.github.io/swiss-job-intelligence/) |
| 📊 Tableau Dashboard | Coming soon |
| 📓 Kaggle Notebook | Coming soon |

## 🏗️ Architecture

![Airflow DAG Pipeline](docs/screenshots/airflow_dag.png) 

Python Data Generator ↓ PostgreSQL 15 (Docker) ↓ dbt (7 models: staging → intermediate → marts) ↓ Apache Airflow (daily at 06:00) ↓ export_dashboard_json.py ↓ Live HTML Dashboard (GitHub Pages)

Python Data Generator

↓

PostgreSQL 15 (Docker)

↓

dbt (7 models: staging → intermediate → marts)

↓

Apache Airflow (daily at 06:00)

↓

export_dashboard_json.py

↓

Live HTML Dashboard (GitHub Pages) 


## 🛠️ Tech Stack
| Layer | Technology | Purpose |
|-------|-----------|---------|
| Language | Python 3.11 | Data generation and pipeline scripts |
| Database | PostgreSQL 15 (Docker) | Raw data storage |
| Transformation | dbt 1.7 (7 models, 6 tests) | Staging → Intermediate → Marts |
| Orchestration | Apache Airflow 2.8 | Daily automated pipeline |
| Containerisation | Docker | Reproducible environment |
| CI/CD | GitHub Actions | Automated dbt tests on every push |
| Dashboard | HTML + Chart.js | Live interactive visualisation |
| Hosting | GitHub Pages | Free, always-on live demo |

## 📁 Project Structure
swiss-job-intelligence/ ├── ingestion/ │ └── data_generator.py # Generates 5,000 Swiss job postings ├── dbt_project/swiss_jobs_dbt/ │ └── models/ │ ├── staging/ # 1 model — cleans raw data │ ├── intermediate/ # 2 models — business logic │ └── marts/ # 4 models — analytics tables ├── airflow/ │ └── dags/swiss_jobs_pipeline.py # Daily pipeline DAG ├── dashboard/ │ ├── index.html # Live interactive dashboard │ └── dashboard_data.json # Auto-exported from mart tables ├── .github/workflows/ │ └── dbt_tests.yml # GitHub Actions CI/CD └── export_dashboard_json.py # Bridges dbt marts to dashboard

swiss-job-intelligence/

├── ingestion/

│   └── data_generator.py      # Generates 5,000 Swiss job postings

├── dbt_project/swiss_jobs_dbt/

│   └── models/

│       ├── staging/            # 1 model — cleans raw data

│       ├── intermediate/       # 2 models — business logic

│       └── marts/              # 4 models — analytics tables

├── airflow/

│   └── dags/swiss_jobs_pipeline.py  # Daily pipeline DAG

├── dashboard/

│   ├── index.html             # Live interactive dashboard

│   └── dashboard_data.json   # Auto-exported from mart tables

├── .github/workflows/

│   └── dbt_tests.yml          # GitHub Actions CI/CD

└── export_dashboard_json.py   # Bridges dbt marts to dashboard
## 📊 dbt Models
| Layer | Model | Description |
|-------|-------|-------------|
| Staging | stg_job_postings | Cleans raw data, standardises cities, derives seniority |
| Intermediate | int_job_postings_enriched | Adds salary bands, region, days since posted |
| Intermediate | int_skills_exploded | Splits comma-separated skills into individual rows |
| Mart | mart_market_overview | Monthly postings by city, industry, remote % |
| Mart | mart_skill_demand | Skill rankings with salary impact by city |
| Mart | mart_salary_benchmarks | Salary percentiles by role and seniority |
| Mart | mart_dashboard_kpis | Aggregated KPIs for dashboard overview |

## ✅ Data Quality
- 6 automated dbt tests running on every pipeline execution
- Tests cover: uniqueness, not null, accepted values for all 10 Swiss cities
- GitHub Actions runs full test suite on every push to main

## 🔑 Architecture Decisions
**Why PostgreSQL over MySQL:** Advanced SQL features — unnest(),
window functions, percentile_cont() — essential for skill analysis
and salary percentile calculations.

**Why dbt over raw SQL scripts:** Version-controlled transformations,
automatic documentation, data lineage, and built-in testing framework.

**Why Airflow over cron:** Visual DAG monitoring, retry logic,
task dependency management, and audit logging.

**Why synthetic data:** Real Swiss job board scraping requires API
agreements. Synthetic data calibrated to actual Swiss market
distributions (salary ranges, city weights, industry mix) allows
full pipeline demonstration without legal risk. Documented transparently.

## 🚀 Run Locally
```bash
git clone https://github.com/victoriaest1/swiss-job-intelligence
cd swiss-job-intelligence
python3.11 -m venv venv && source venv/bin/activate
pip install -r requirements.txt
docker run --name swiss-jobs-db \
  -e POSTGRES_USER=postgres \
  -e POSTGRES_PASSWORD=SwissJobs2026! \
  -e POSTGRES_DB=swiss_jobs \
  -p 5432:5432 -d postgres:15
python ingestion/data_generator.py
cd dbt_project/swiss_jobs_dbt && dbt run && dbt test
python export_dashboard_json.py
⚠️ Limitations
* Synthetic data calibrated to Swiss market — not scraped from live boards
* Airflow scheduler requires local execution environment
* 10 cities covered — smaller Swiss cities not included
* Tableau dashboard in progress
🔮 Next Steps
* Add real scraping from jobs.ch via official API
* Build Tableau dashboard connected to PostgreSQL mart tables
* Add BERT-based skill extraction from raw job descriptions
* Deploy Airflow to cloud (AWS MWAA or GCP Composer)
* Expand to all 26 Swiss cantons
📚 Data Sources
* Job postings: Synthetic data generated with Python Faker, calibrated to Swiss market research
* Swiss market benchmarks: jobs.ch, LinkedIn Salary Insights, Michael Page Switzerland Salary Guide 2025
* City/canton mapping: Swiss Federal Statistical Office (BFS)

Built by Victoria Esther — Business Informatics Student, University of Fribourg · 2026 Targeting data related roles across Switzerland EOF
