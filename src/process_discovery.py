
from pathlib import Path

import pandas as pd
from google.cloud import bigquery
import pm4py

PROJECT_ID = "careflow-process-mining-511312"
TABLE_ID = (
    "careflow-process-mining-511312."
    "careflow_raw_analytics.fct_careflow_event_log"
)

ROOT = Path(__file__).resolve().parents[1]
OUTPUT_DIR = ROOT / "outputs"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

query = f"""
SELECT
    case_id,
    activity_name,
    event_timestamp,
    event_id,
    event_sequence
FROM `{TABLE_ID}`
WHERE case_id IS NOT NULL
  AND activity_name IS NOT NULL
  AND event_timestamp IS NOT NULL
ORDER BY case_id, event_timestamp, event_sequence
"""

print("Connecting to BigQuery...")
client = bigquery.Client(project=PROJECT_ID)
df = client.query(query).to_dataframe()

if df.empty:
    raise ValueError("No valid events found in the normalized Event Log.")

df["event_timestamp"] = pd.to_datetime(
    df["event_timestamp"], errors="coerce", utc=True
)
df = df.dropna(
    subset=["case_id", "activity_name", "event_timestamp"]
).copy()

df["case_id"] = df["case_id"].astype(str)
df["activity_name"] = df["activity_name"].astype(str)

# PM4Py requires the standard event-log column mapping.
event_log = pm4py.format_dataframe(
    df,
    case_id="case_id",
    activity_key="activity_name",
    timestamp_key="event_timestamp",
)

# Discover the directly-follows graph.
dfg, start_activities, end_activities = pm4py.discover_dfg(
    event_log,
    case_id_key="case:concept:name",
    activity_key="concept:name",
    timestamp_key="time:timestamp",
)

# Save the graph edges and their observed frequencies.
edges = pd.DataFrame(
    [
        {
            "source_activity": source,
            "target_activity": target,
            "frequency": frequency,
        }
        for (source, target), frequency in dfg.items()
    ],
    columns=["source_activity", "target_activity", "frequency"],
)

edges.to_csv(OUTPUT_DIR / "careflow_process_edges.csv", index=False)

pd.DataFrame(
    [
        {"activity": activity, "frequency": frequency}
        for activity, frequency in start_activities.items()
    ],
    columns=["activity", "frequency"],
).to_csv(OUTPUT_DIR / "careflow_start_activities.csv", index=False)

pd.DataFrame(
    [
        {"activity": activity, "frequency": frequency}
        for activity, frequency in end_activities.items()
    ],
    columns=["activity", "frequency"],
).to_csv(OUTPUT_DIR / "careflow_end_activities.csv", index=False)

# Export a frequency-based process map.
from pm4py.visualization.dfg import visualizer as dfg_visualizer

gviz = dfg_visualizer.apply(
    dfg,
    log=event_log,
    variant=dfg_visualizer.Variants.FREQUENCY,
)
dfg_visualizer.save(
    gviz, str(OUTPUT_DIR / "careflow_as_is_process_map.png")
)

print(f"Events processed: {len(event_log)}")
print(f"Cases processed: {event_log['case:concept:name'].nunique()}")
print(f"Activities discovered: {len(set(event_log['concept:name']))}")
print(f"Directed transitions discovered: {len(dfg)}")
print(f"Output directory: {OUTPUT_DIR}")
print("Process discovery completed.")
