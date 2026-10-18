
{{ config(
    materialized='table',
    schema='analytics'
) }}

WITH source_events AS (

    SELECT
        CAST(event_id AS STRING) AS event_id,
        CAST(case_id AS STRING) AS case_id,
        CAST(patient_id AS STRING) AS patient_id,
        CAST(activity AS STRING) AS activity_name,
        CAST(timestamp AS TIMESTAMP) AS event_timestamp,
        CAST(event_sequence AS INT64) AS event_sequence,
        CAST(previous_activity AS STRING) AS previous_activity,
        CAST(event_status AS STRING) AS event_status

    FROM {{ ref('stg_ehr_event_log') }}

),

normalized_events AS (

    SELECT *
    FROM source_events
    WHERE event_id IS NOT NULL
      AND case_id IS NOT NULL
      AND activity_name IS NOT NULL
      AND TRIM(activity_name) != ''
      AND event_timestamp IS NOT NULL

),

deduplicated_events AS (

    SELECT *
    FROM normalized_events
    QUALIFY ROW_NUMBER() OVER (
        PARTITION BY event_id
        ORDER BY event_timestamp, event_sequence
    ) = 1

)

SELECT *
FROM deduplicated_events
