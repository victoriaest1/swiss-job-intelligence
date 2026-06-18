WITH source AS (
    SELECT * FROM {{ source('raw', 'raw_job_postings') }}
),
cleaned AS (
    SELECT
        id,
        TRIM(title)                          AS title_clean,
        TRIM(company)                        AS company_clean,
        TRIM(city)                           AS city_clean,
        UPPER(TRIM(canton))                  AS canton_clean,
        salary_min,
        salary_max,
        salary_mid,
        TRIM(skills)                         AS skills_raw,
        TRIM(industry)                       AS industry_clean,
        remote,
        TRIM(language)                       AS language_clean,
        date_posted,
        experience_yr,
        created_at,
        CASE
            WHEN TRIM(title) ILIKE '%senior%' THEN 'Senior'
            WHEN TRIM(title) ILIKE '%junior%' THEN 'Junior'
            WHEN TRIM(title) ILIKE '%lead%'   THEN 'Lead'
            ELSE 'Mid'
        END AS seniority_level,
        CASE
            WHEN TRIM(title) ILIKE '%engineer%'  THEN 'Engineering'
            WHEN TRIM(title) ILIKE '%scientist%' THEN 'Data Science'
            WHEN TRIM(title) ILIKE '%analyst%'   THEN 'Analytics'
            WHEN TRIM(title) ILIKE '%developer%' THEN 'Development'
            ELSE 'Other'
        END AS role_category
    FROM source
    WHERE
        salary_mid BETWEEN 40000 AND 500000
        AND city IS NOT NULL
        AND title IS NOT NULL
)
SELECT * FROM cleaned
