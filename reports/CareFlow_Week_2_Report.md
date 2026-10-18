# CareFlow — Week 2 Implementation Report



**Project:** CareFlow — Clinical Pathway Process Mining  

**Reporting period:** Week 2 implementation  

**Environment:** Windows / Conda (`careflow`), dbt Core, Google BigQuery, Python, PM4Py



## 1. Executive Summary



During Week 2, CareFlow was extended beyond the existing staging model by creating a normalized downstream Event Log model and using PM4Py to discover an As-Is process map from hospital event data. The downstream dbt table was created successfully. Validation returned **4,875 rows across 500 cases**, with no missing activity names or event timestamps. The user confirmed that all **5 configured dbt tests passed**. Process-discovery artifacts were generated and structurally checked.



## 2. Objectives



- Create a downstream normalized Event Log model without modifying the Week 1 staging model.

- Validate event uniqueness, case coverage, activity values, and timestamps.

- Use PM4Py to discover a directly-follows process graph from the normalized Event Log.

- Export the process map, transition frequencies, start/end activities, and a machine-readable report.

- Keep implementation code and validation evidence organized for project handoff.



## 3. Implementation Completed



### 3.1 dbt Event Log Model



Added `careflow_dbt/models/marts/fct_careflow_event_log.sql`.



The model reads from `stg_ehr_event_log`, standardizes event, case, patient, activity, timestamp, sequence, previous-activity, and event-status fields, filters rows with missing required identifiers/activity/timestamp, and deduplicates by `event_id`.



The model was built successfully in BigQuery as:



`careflow_raw_analytics.fct_careflow_event_log`



The successful dbt run reported **4,875 rows**.



### 3.2 Automated dbt Tests



Added `careflow_dbt/models/marts/schema.yml` with column-level tests for:



- `event_id`: `not_null`, `unique`

- `case_id`: `not_null`

- `activity_name`: `not_null`

- `event_timestamp`: `not_null`



**Result:** 5 tests passed (user-confirmed).



### 3.3 PM4Py Process Discovery



Added `src/process_discovery.py` to query the normalized BigQuery Event Log, format data for PM4Py, discover a directly-follows graph, and export graph edges, start activities, end activities, and a process map image.



Graphviz initially raised a Windows DLL/entry-point error during an attempted re-run. However, the project outputs directory contained an existing process map PNG and all three CSV artifacts. The artifacts were inspected, and the report-generation command completed successfully.



## 4. Validation Results



| Validation | Result | Status |

|---|---:|---|

| `dbt parse` | Completed successfully | PASS |

| `dbt run --select fct_careflow_event_log` | Table created; 4,875 rows | PASS |

| Total rows vs. unique event IDs | 4,875 vs. 4,875 | PASS |

| Distinct cases | 500 | PASS |

| Missing activity names | 0 | PASS |

| Missing event timestamps | 0 | PASS |

| Automated dbt tests | 5 tests passed | PASS |

| Directed transitions exported | 23 | PASS |

| Duplicate transition edges | 0 | PASS |

| Missing transition values | 0 | PASS |

| Self-loops in exported edge list | 0 | PASS |

| Start activity | Registration — frequency 500 | Recorded |

| End activity | Discharge — frequency 500 | Recorded |

| Process map PNG | File exists; visually inspected | PASS |

| JSON report | `week2_process_discovery_report.json` generated | PASS |



## 5. Observed Process Transitions



The exported directly-follows edge list contains **23 directed transitions**. Examples observed in the CSV include:



- Registration → Triage: 500

- Doctor Assessment → Lab Order: 373

- Lab Order → Lab Sample Collection: 373

- Lab Sample Collection → Lab Result: 373

- Lab Result → Imaging Order: 147

- Lab Result → Treatment: 226

- Treatment → Discharge Preparation: 309

- Discharge Preparation → Discharge: 500

- Reassessment → Triage: 79

- Treatment → Doctor Assessment: 65



These frequencies describe observed transitions in the synthetic event log. They should not be interpreted as clinical quality conclusions without additional duration, case-level, and pathway analysis.



## 6. Output Artifacts



| Artifact | Purpose |

|---|---|

| `outputs/careflow_as_is_process_map.png` | Visual As-Is process map |

| `outputs/careflow_process_edges.csv` | Directed activity transitions and frequencies |

| `outputs/careflow_start_activities.csv` | Start activities and frequencies |

| `outputs/careflow_end_activities.csv` | End activities and frequencies |

| `outputs/week2_process_discovery_report.json` | Machine-readable process-discovery validation summary |

| `careflow_dbt/models/marts/fct_careflow_event_log.sql` | Normalized Event Log model |

| `careflow_dbt/models/marts/schema.yml` | Automated tests for the downstream model |

| `src/process_discovery.py` | PM4Py process-discovery script |



## 7. Git Status



The implementation files were staged and committed on the local `main` branch.



- **Commit:** `a1da16a`

- **Message:** `feat: implement Week 2 event log and process discovery`



The most recent screenshot showed remaining untracked directories: `careflow_dbt/analyses/`, `careflow_dbt/backup_example/`, `careflow_dbt/macros/`, `careflow_dbt/seeds/`, `careflow_dbt/snapshots/`, `careflow_dbt/tests/`, and `outputs/`.



A successful push to the remote GitHub repository was **not confirmed** during the session.



## 8. Known Limitations and Follow-up



- Graphviz encountered a Windows DLL/entry-point issue during a later re-run. Existing process-map and CSV artifacts were present, but a clean end-to-end rerun should be verified after resolving the environment issue.

- The report validates structural data quality and transition outputs; it does not yet quantify waiting-time bottlenecks or activity durations.

- The synthetic event log is suitable for demonstration and development, not for conclusions about real patient outcomes.

- Confirm the remote GitHub push separately; a local commit does not prove remote publication.

- Week 3 should calculate activity duration, waiting time, case turnaround time, and loop-back frequency before building the Power BI dashboard.



## 9. Conclusion



Week 2's core implementation objectives were achieved: the normalized Event Log table was built, the user-confirmed five dbt tests passed, PM4Py transition artifacts were generated, and output files and the JSON summary were verified. The next phase is operational metrics and bottleneck analysis, followed by dashboard development and final project documentation.



