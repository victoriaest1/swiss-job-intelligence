WITH enriched AS (
    SELECT * FROM {{ ref('int_job_postings_enriched') }}
),

kpis AS (
    SELECT
        COUNT(*)                             AS total_postings,
        ROUND(AVG(salary_mid))               AS avg_salary_chf,
        ROUND(AVG(CASE WHEN remote THEN 1.0 ELSE 0.0 END) * 100, 1) AS remote_pct,
        COUNT(DISTINCT company_clean)        AS total_companies,
        COUNT(DISTINCT city_clean)           AS total_cities,
        COUNT(DISTINCT title_clean)          AS total_roles,
        ROUND(AVG(experience_yr), 1)         AS avg_experience_yr,
        SUM(CASE WHEN is_recent THEN 1 ELSE 0 END) AS recent_postings
    FROM enriched
)

SELECT * FROM kpis
