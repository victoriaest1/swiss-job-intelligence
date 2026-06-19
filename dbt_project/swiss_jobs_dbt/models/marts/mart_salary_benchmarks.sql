WITH enriched AS (
    SELECT * FROM {{ ref('int_job_postings_enriched') }}
),

benchmarks AS (
    SELECT
        title_clean                          AS role,
        city_clean,
        region,
        seniority_level,
        salary_band,
        COUNT(*)                             AS postings_count,
        ROUND(AVG(salary_mid))               AS avg_salary_chf,
        ROUND(PERCENTILE_CONT(0.25) WITHIN GROUP (ORDER BY salary_mid)) AS p25_salary,
        ROUND(PERCENTILE_CONT(0.50) WITHIN GROUP (ORDER BY salary_mid)) AS median_salary,
        ROUND(PERCENTILE_CONT(0.75) WITHIN GROUP (ORDER BY salary_mid)) AS p75_salary,
        ROUND(MIN(salary_mid))               AS min_salary,
        ROUND(MAX(salary_mid))               AS max_salary,
        ROUND(AVG(experience_yr), 1)         AS avg_experience_yr
    FROM enriched
    GROUP BY
        title_clean,
        city_clean,
        region,
        seniority_level,
        salary_band
)

SELECT * FROM benchmarks
ORDER BY avg_salary_chf DESC
