WITH enriched AS (
    SELECT * FROM {{ ref('int_job_postings_enriched') }}
),

skills_split AS (
    SELECT
        id,
        title_clean,
        city_clean,
        canton_clean,
        salary_mid,
        industry_clean,
        remote,
        seniority_level,
        role_category,
        region,
        date_posted,
        -- Split comma-separated skills into individual rows
        TRIM(UNNEST(STRING_TO_ARRAY(skills_raw, ','))) AS skill
    FROM enriched
)

SELECT * FROM skills_split
WHERE skill IS NOT NULL
AND skill != ''
