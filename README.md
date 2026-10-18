# CareFlow — Clinical Pathway Process Mining

**A healthcare analytics pipeline for understanding patient journeys, discovering clinical workflows, and identifying operational bottlenecks using process mining.**

## Project Overview

CareFlow analyzes synthetic Electronic Health Record (EHR) event logs to understand how patients move through hospital workflows, particularly Emergency Room (ER) pathways.

The project combines data engineering, data quality validation, process discovery, and operational analytics to identify workflow transitions, repeated activities, potential delays, and opportunities for improvement.

## Project Objectives

- Generate and validate synthetic hospital event-log data.
- Ingest raw data into Google BigQuery.
- Transform event logs using dbt.
- Validate event identifiers, timestamps, case references, and required fields.
- Discover clinical process flows using PM4Py.
- Analyze waiting times, activity durations, and loop-back behaviour.
- Develop a Power BI dashboard for operational insights.

## Technology Stack

| Technology | Purpose |
|---|---|
| Python | Data generation, validation, and analysis |
| Pandas and NumPy | Data manipulation |
| Google BigQuery | Cloud data warehouse |
| dbt Core | SQL transformations and data tests |
| PM4Py | Process discovery and process mining |
| Power BI | Planned operational dashboard |
| Conda | Python environment management |
| Git and GitHub | Version control |

## Architecture

```text
Synthetic Hospital EHR Data
          |
          v
    Python Data Pipeline
          |
          v
     Raw CSV Files
          |
          v
    Google BigQuery
          |
          v
    dbt Transformations
          |
          v
  Validated Event Log
          |
          v
   PM4Py Process Discovery
          |
          v
 Operational Metrics and
   Bottleneck Analysis
          |
          v
    Power BI Dashboard
```

## Current Project Status

**Completed milestone: Week 2 — Event Log Preparation and Process Discovery**

| Milestone | Status |
|---|---|
| Environment and project setup | Complete |
| Synthetic data generation | Complete |
| Local data cleaning and quality audit | Complete |
| BigQuery raw data ingestion | Complete |
| dbt staging model | Complete |
| dbt mart model | Complete |
| dbt tests | 5 passed |
| Process transition extraction | Complete |
| Initial process map and discovery report | Generated |
| Operational performance metrics | Remaining work |
| Power BI dashboard | Remaining work |

## Dataset and Validation

The project uses synthetic data for development and demonstration. It does not represent real patient records.

### Event Log

| Metric | Validated result |
|---|---:|
| Raw event rows | 4,900 |
| Cleaned event rows | 4,875 |
| Unique event IDs in normalized event log | 4,875 |
| Distinct cases | 500 |
| Missing activity names | 0 |
| Missing event timestamps | 0 |
| dbt tests passed | 5 |

The raw event log contains 25 deliberately introduced duplicate rows. The normalized event log contains 4,875 unique event IDs.

### Process Discovery Results

The PM4Py process-discovery workflow generated an initial activity-transition map and supporting CSV artifacts.

| Metric | Result |
|---|---:|
| Directed activity transitions | 23 |
| Duplicate transition edges | 0 |
| Transitions with missing edge values | 0 |
| Self-loop transitions | 0 |
| Cases starting with Registration | 500 |
| Cases ending with Discharge | 500 |

These results describe the current synthetic dataset and should not be interpreted as clinical findings about a real hospital.

## Google BigQuery

**GCP project ID:** `careflow-process-mining-511312`

| Dataset | Purpose |
|---|---|
| `careflow_raw` | Raw source datasets |
| `careflow_raw_analytics` | dbt models and analytics tables |

Key tables:

- `careflow_raw.ehr_event_log_raw`
- `careflow_raw.ehr_cases_raw`
- `careflow_raw_analytics.stg_ehr_event_log`
- `careflow_raw_analytics.fct_careflow_event_log`
- `careflow_raw_analytics.ehr_event_log_clean_reference`

The staging model cleans and deduplicates event records. The mart model provides a normalized event log for process analysis.

## Project Artifacts

Generated outputs are stored in the `outputs/` directory.

| Artifact | Description |
|---|---|
| `careflow_as_is_process_map.png` | Initial process map |
| `careflow_process_edges.csv` | Directed activity transitions |
| `careflow_start_activities.csv` | Start activity frequencies |
| `careflow_end_activities.csv` | End activity frequencies |
| `week2_process_discovery_report.json` | Process discovery summary |

The Week 2 implementation report is available at:

`reports/CareFlow_Week_2_Report.md`

## Local Project Structure

```text
E:\careflow\
├── careflow_dbt\
│   └── models\
│       ├── staging\
│       │   └── stg_ehr_event_log.sql
│       └── marts\
│           ├── fct_careflow_event_log.sql
│           └── schema.yml
├── data\
├── notebooks\
├── outputs\
├── reports\
│   ├── week1_data_quality_report.json
│   ├── week1_handoff.md
│   └── CareFlow_Week_2_Report.md
└── src\
    └── process_discovery.py
```

## Environment Setup

Activate the Conda environment:

```cmd
conda activate careflow
```

Navigate to the dbt project:

```cmd
cd /d E:\careflow\careflow_dbt
```

Verify the environment and dbt configuration:

```cmd
python --version
dbt --version
dbt debug
```

Run the staging and mart models:

```cmd
dbt run --select stg_ehr_event_log
dbt run --select fct_careflow_event_log
```

Run the dbt tests:

```cmd
dbt test
```

The BigQuery connection uses locally configured authentication. Do not commit credentials, OAuth tokens, or sensitive configuration files.

## Process Discovery

The process-discovery script is located at:

`src/process_discovery.py`

Run it from the project root using the configured Conda environment:

```cmd
conda activate careflow
python src\process_discovery.py
```

The generated process map and supporting CSV and JSON artifacts are saved in `outputs/`.

A clean rerun may require resolving the existing Graphviz DLL/environment issue. Previously generated artifacts are available, but a successful clean rerun should be confirmed after that issue is resolved.

## Remaining Work

### Week 3 — Operational Analysis

- Calculate activity durations and waiting times.
- Calculate case turnaround time.
- Quantify loop-back and repeated-activity behaviour.
- Identify bottlenecks and high-frequency transitions.
- Validate the derived metrics and document assumptions.

### Subsequent Work

- Build a Power BI dashboard.
- Present process flows and operational metrics.
- Document findings, limitations, and recommendations.
- Perform final validation and prepare project handoff documentation.

## GitHub Repository

Repository: [CareFlow — Clinical Pathway Process Mining](https://github.com/vishwas0229/CareFlow-Clinical-Pathway-Process-Mining)

The project uses the `main` branch for version control. Review changes before committing, and ensure generated artifacts and credentials are handled appropriately.

## Data and Privacy Notice

CareFlow uses synthetic data for development and demonstration. Do not add real patient information, credentials, OAuth tokens, or other sensitive information to the repository.
s