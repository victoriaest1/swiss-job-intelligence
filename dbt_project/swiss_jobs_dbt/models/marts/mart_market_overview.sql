WITH enriched AS (
    SELECT * FROM {{ ref('int_job_postings_enriched') }}
),

overview AS (
    SELECT
        city_clean,
        canton_clean,
        region,
        industry_clean,
        DATE_TRUNC('month', date_posted)     AS month_year,
        COUNT(*)                             AS postings_count,
        ROUND(AVG(salary_mid))               AS avg_salary_chf,
        ROUND(MIN(salary_mid))               AS min_salary_chf,
        ROUND(MAX(salary_mid))               AS max_salary_chf,
        ROUND(AVG(experience_yr), 1)         AS avg_experience_yr,
        ROUND(SUM(CASE WHEN remote THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 1) AS remote_pct
    FROM enriched
    GROUP BY
        city_clean,
        canton_clean,
        region,
        industry_clean,
        DATE_TRUNC('month', date_posted)
)

SELECT * FROM overview
