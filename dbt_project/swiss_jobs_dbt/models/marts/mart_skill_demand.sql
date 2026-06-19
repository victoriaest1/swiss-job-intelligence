WITH skills AS (
    SELECT * FROM {{ ref('int_skills_exploded') }}
),

skill_stats AS (
    SELECT
        skill,
        city_clean,
        region,
        COUNT(*)                             AS job_count,
        ROUND(AVG(salary_mid))               AS avg_salary_chf,
        ROUND(AVG(CASE WHEN remote THEN 1.0 ELSE 0.0 END) * 100, 1) AS remote_pct,
        COUNT(*) * 100.0 / SUM(COUNT(*)) OVER (PARTITION BY city_clean) AS pct_of_city_jobs
    FROM skills
    GROUP BY skill, city_clean, region
),

ranked AS (
    SELECT
        *,
        RANK() OVER (PARTITION BY city_clean ORDER BY job_count DESC) AS skill_rank
    FROM skill_stats
)

SELECT * FROM ranked
