\# CareFlow — Week 1 Handoff Report



\## 1. Objective

Build the initial synthetic hospital event-data pipeline, load raw data into BigQuery, and create a dbt staging model with data-quality checks.



\## 2. Implementation Completed

\- Configured Python and Conda environment.

\- Generated synthetic hospital event and case datasets.

\- Cleaned local CSV files and generated a data-quality audit report.

\- Created BigQuery raw datasets and uploaded source tables.

\- Configured dbt BigQuery authentication and source definitions.

\- Implemented the `stg\_ehr\_event\_log` staging model.

\- Added dbt data tests for event and case identifiers.

\- Created a BigQuery reference table from the locally cleaned event log.



\## 3. Data Validation Results

| Metric | Result |

|---|---:|

| Raw event rows | 4,900 |

| Raw distinct event IDs | 4,875 |

| Staging event rows | 4,875 |

| Staging distinct event IDs | 4,875 |

| Duplicate rows removed | 25 |

| dbt data tests passed | 3 |



\## 4. Cleaning Rules

\- Removed duplicate event IDs.

\- Filtered records with missing required event fields.

\- Retained only events linked to valid cases.

\- Normalized missing `resource\_id` values to `Unknown`.

\- Normalized the literal `None` and blank `comorbidities` values to SQL NULL.



\## 5. Validation Status

\- `dbt parse`: successful.

\- `dbt run`: successful.

\- `dbt test`: 3 tests passed.

\- Local-versus-BigQuery comparison: record the final full-row comparison result here.



\## 6. Week 2 Handoff

Proceed to the next project phase after confirming final data parity and reviewing the project plan.



