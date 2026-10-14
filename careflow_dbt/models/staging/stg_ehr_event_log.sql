
{{ config(
    materialized='table',
    schema='analytics'
) }}

WITH source_events AS (
    SELECT *
    FROM {{ source('careflow_raw', 'ehr_event_log_raw') }}
),

valid_events AS (
    SELECT *
    FROM source_events
    WHERE event_id IS NOT NULL
      AND case_id IS NOT NULL
      AND timestamp IS NOT NULL
      AND EXISTS (
          SELECT 1
          FROM {{ source('careflow_raw', 'ehr_cases_raw') }} AS cases
          WHERE cases.case_id = source_events.case_id
      )
),

deduplicated AS (
    SELECT *
    FROM valid_events
    QUALIFY ROW_NUMBER() OVER (
        PARTITION BY event_id
        ORDER BY timestamp, event_sequence
    ) = 1
)
SELECT
    * REPLACE (
        COALESCE(resource_id, 'Unknown') AS resource_id,
        CASE
            WHEN TRIM(comorbidities) = 'None'
              OR TRIM(comorbidities) = ''
            THEN NULL
            ELSE comorbidities
        END AS comorbidities
    )
FROM deduplicated