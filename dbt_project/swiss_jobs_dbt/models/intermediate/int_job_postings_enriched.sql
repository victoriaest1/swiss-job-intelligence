WITH staging AS (
    SELECT * FROM {{ ref('stg_job_postings') }}
),

enriched AS (
    SELECT
        id,
        title_clean,
        company_clean,
        city_clean,
        canton_clean,
        salary_min,
        salary_max,
        salary_mid,
        skills_raw,
        industry_clean,
        remote,
        language_clean,
        date_posted,
        experience_yr,
        seniority_level,
        role_category,
        created_at,

        -- Salary bands
        CASE
            WHEN salary_mid < 90000  THEN 'Junior (< 90K)'
            WHEN salary_mid < 120000 THEN 'Mid (90K-120K)'
            WHEN salary_mid < 150000 THEN 'Senior (120K-150K)'
            ELSE 'Lead (150K+)'
        END AS salary_band,

        -- Days since posted
        CURRENT_DATE - date_posted AS days_since_posted,

        -- Is recent (posted in last 30 days)
        CASE
            WHEN CURRENT_DATE - date_posted <= 30 THEN true
            ELSE false
        END AS is_recent,

        -- Region
        CASE
            WHEN city_clean IN ('Geneva', 'Lausanne') THEN 'Romandy'
            WHEN city_clean IN ('Zurich', 'Basel', 'Bern', 'Zug', 'Winterthur', 'Lucerne', 'St. Gallen') THEN 'Deutschschweiz'
            WHEN city_clean = 'Lugano' THEN 'Ticino'
            ELSE 'Other'
        END AS region

    FROM staging
)

SELECT * FROM enriched
