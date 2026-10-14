
{{ config(
    materialized='table',
    schema='analytics'
) }}

WITH source_events AS (
    SELECT *
    FROM `careflow-process-mining-511312.careflow_raw.ehr_event_log_raw`
),

deduplicated AS (
    SELECT *
    FROM source_events
    QUALIFY ROW_NUMBER() OVER (
        PARTITION BY event_id
        ORDER BY timestamp, event_sequence
    ) = 1
)

SELECT *
FROM deduplicated
