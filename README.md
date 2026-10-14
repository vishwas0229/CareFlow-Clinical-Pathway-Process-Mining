# CareFlow — Clinical Pathway Process Mining

**A data analytics pipeline for understanding hospital patient journeys, detecting operational bottlenecks, and analyzing clinical process inefficiencies.**

## Project Overview

CareFlow is a healthcare operations analytics project focused on understanding how patients move through hospital workflows, particularly Emergency Room (ER) pathways.

Traditional dashboards report aggregate metrics such as average waiting time, but they often fail to explain the actual sequence of events experienced by patients. CareFlow aims to use event-log data and process mining to uncover repeated activities, workflow deviations, waiting-time bottlenecks, and opportunities for operational improvement.

The project is being developed as a data pipeline that combines synthetic Electronic Health Record (EHR) event data, Google BigQuery, Python, dbt, PM4Py, and Power BI.

> **Current milestone:** Week 1 — Initial data pipeline, BigQuery ingestion, dbt staging, and data-quality validation.

## Project Objectives

- Generate synthetic hospital case and event-log datasets.
- Clean and validate event-level healthcare data.
- Store raw datasets in Google BigQuery.
- Transform raw event logs using dbt.
- Validate identifiers, required fields, duplicate records, and case references.
- Compare locally cleaned data against BigQuery-transformed data.
- Prepare the data for subsequent process mining and operational dashboard development.

## Technology Stack

| Technology | Purpose |
|---|---|
| Python | Synthetic data generation and data cleaning |
| Anaconda / Conda | Python environment management |
| Pandas and NumPy | Data manipulation and generation |
| Google BigQuery | Cloud data warehouse |
| dbt Core | SQL transformations and data tests |
| PM4Py | Planned process mining analysis |
| Power BI | Planned operational analytics dashboard |
| Git and GitHub | Version control and project tracking |
| JupyterLab | Development and validation notebooks |

## Architecture

```text
Synthetic Hospital Data
          |
          v
  Python Data Generator
          |
          v
      Raw CSV Files
          |
          v
 Local Cleaning & Quality Audit
          |
          v
    Google BigQuery
          |
          v
      Raw Datasets
          |
          v
     dbt Sources
          |
          v
  dbt Staging Model
          |
          v
 Data Quality & Validation
          |
          v
   Process Mining (PM4Py)
          |
          v
   Power BI Dashboard
```

*The pipeline through dbt staging has been implemented. Process mining analysis and dashboard development are subsequent project phases.*

## Current Dataset

The initial synthetic dataset contains 500 hospital cases.

### Event-level dataset

| Metric | Current result |
|---|---:|
| Raw event rows | 4,900 |
| Distinct raw event IDs | 4,875 |
| Deliberately introduced duplicate rows | 25 |
| Cleaned event rows | 4,875 |
| Event-level columns | 32 |
| Cases represented | 500 |
| Cases with loop-back behaviour | 144 |
| Intentionally missing resource IDs | 50 |

### Case-level dataset

| Metric | Current result |
|---|---:|
| Raw case rows | 500 |
| Cleaned case rows | 500 |
| Case-level columns | 20 |

The dataset is synthetic and is intended for development, testing, and process-mining demonstrations. It is not real patient data.

## Data Storage

### Local project files

```text
E:\careflow\
├── 01_week1_environment_check.ipynb
├── data\
│   ├── raw\
│   │   ├── ehr_event_log_raw.csv
│   │   └── ehr_cases_raw.csv
│   └── processed\
│       ├── ehr_event_log_clean.csv
│       └── ehr_cases_clean.csv
├── reports\
│   └── week1_data_quality_report.json
├── notebooks\
├── outputs\
├── logs\
├── src\
└── careflow_dbt\
    ├── dbt_project.yml
    ├── models\
    │   └── staging\
    │       ├── sources.yml
    │       ├── stg_ehr_event_log.sql
    │       └── schema.yml
    └── README.md
```

Generated dbt artifacts, logs, and notebook checkpoint files are excluded from version control through `.gitignore`.

### Google BigQuery

**GCP project ID:** `careflow-process-mining-511312`

| Dataset | Purpose |
|---|---|
| `careflow_raw` | Raw source datasets |
| `careflow_raw_analytics` | dbt staging output and local-clean reference table |

Current tables include:

- `careflow_raw.ehr_event_log_raw`
- `careflow_raw.ehr_cases_raw`
- `careflow_raw_analytics.stg_ehr_event_log`
- `careflow_raw_analytics.ehr_event_log_clean_reference`

The raw event table contains 4,900 rows, while the staging model contains 4,875 rows after deduplication and configured cleaning rules.

## Implemented Data Quality Rules

The current dbt staging model includes the following rules:

1. Read the raw event log through a formal dbt source definition.
2. Remove duplicate event IDs using `ROW_NUMBER()` and `QUALIFY`.
3. Exclude records missing required event identifiers, case identifiers, or timestamps.
4. Retain events linked to valid case records.
5. Normalize missing resource IDs to `Unknown`.
6. Normalize the literal `None` and blank `comorbidities` values to SQL `NULL`.

The local cleaning pipeline also generates cleaned event and case CSVs and a JSON data-quality report.

## Validation Status

| Validation | Status |
|---|---|
| Python / Conda environment | Complete |
| Synthetic data generation | Complete |
| Local cleaning and quality audit | Complete |
| BigQuery raw ingestion | Complete |
| dbt authentication and connection | Complete |
| dbt source definitions | Configured |
| dbt staging model | Successful |
| dbt tests | 3 passed |
| Raw-to-staging row-count validation | 4,900 raw rows → 4,875 staging rows |
| Duplicate event IDs in staging | None detected |
| Missing required event fields in staging | Zero detected |
| Local vs BigQuery full-row parity | Pending final zero-difference confirmation |
| Week 1 handoff documentation | In progress |

The local cleaned reference table and staging table have the same row count and matching event IDs. A full-row comparison must return zero differing rows before data parity can be marked fully verified.

## Environment Setup

Activate the Conda environment:

```bash
conda activate careflow
```

Navigate to the dbt project:

```bash
cd /d E:\careflow\careflow_dbt
```

Verify the installed tools:

```bash
python --version
dbt --version
```

Check the dbt configuration and source definitions:

```bash
dbt parse
dbt debug
```

Build the staging model and run its tests:

```bash
dbt run --select stg_ehr_event_log
dbt test --select stg_ehr_event_log
```

The BigQuery connection uses dbt OAuth authentication configured locally. Do not commit credentials, OAuth tokens, or `profiles.yml` to GitHub.

## GitHub Repository

Repository: [CareFlow — Clinical Pathway Process Mining](https://github.com/vishwas0229/CareFlow-Clinical-Pathway-Process-Mining)

The project is tracked on the `main` branch. Commits should represent meaningful implementation milestones, validation results, and documentation changes.

Example commit messages:

```bash
git add README.md
git commit -m "docs: update CareFlow project README"
git push origin main
```

Before committing, review staged changes and confirm that generated artifacts and credentials are excluded.

## Remaining Work

### Week 1 — Finalization

- Confirm full-row parity between the cleaned local reference and dbt staging output.
- Record the final validation results in the handoff report.
- Finalize project documentation and publish the verified changes to GitHub.

### Subsequent phases

- Configure additional dbt tests and transformation models as required.
- Perform process discovery and process-flow analysis using PM4Py.
- Calculate operational metrics such as waiting time, activity duration, and loop-back frequency.
- Build a Power BI dashboard for clinical pathway and bottleneck analysis.
- Document findings, limitations, and recommendations.

## Data and Privacy Notice

CareFlow currently uses synthetic data for development and demonstration. No real patient information should be added to the repository. Credentials and local authentication files must remain outside version control.

## Project Status

**Current milestone:** Initial data pipeline and dbt staging implementation.

**Next milestone:** Final data-quality sign-off, followed by process mining analysis and dashboard development.
