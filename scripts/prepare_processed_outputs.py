#!/usr/bin/env python3
"""Prepare local processed output files for the Hadoop/Hive/R workflow.

This script does not replace Hadoop processing. It creates sample processed outputs
from the synthetic dataset so the R scripts can be tested in a non-clustered environment.
"""

import csv
from collections import defaultdict
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATASET = PROJECT_ROOT / "data" / "raw" / "wifi_usage.csv"
OUT_MAPREDUCE = PROJECT_ROOT / "output" / "mapreduce"
OUT_HIVE = PROJECT_ROOT / "output" / "hive"

OUT_MAPREDUCE.mkdir(parents=True, exist_ok=True)
OUT_HIVE.mkdir(parents=True, exist_ok=True)


def write_csv(path, rows):
    if not rows:
        # Keep an empty file for predictable downstream behavior.
        path.write_text("", encoding="utf-8")
        return
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerows(rows)


with DATASET.open("r", newline="", encoding="utf-8") as f:
    reader = csv.DictReader(f)
    hotspot_connections = defaultdict(int)
    hotspot_duration_total = defaultdict(float)
    hotspot_duration_count = defaultdict(int)
    hotspot_data_total = defaultdict(float)
    hourly_usage = defaultdict(int)
    hotspot_hour_matrix = defaultdict(int)
    device_distribution = defaultdict(int)
    avg_duration_by_device = defaultdict(float)
    device_duration_count = defaultdict(int)
    daily_usage = defaultdict(int)
    hotspot_daily_usage = defaultdict(int)
    hotspot_avg_duration = defaultdict(list)

    for row in reader:
        hotspot = (row.get("hotspot_id") or "").strip()
        if not hotspot:
            continue

        duration = float(row.get("duration_minutes", 0) or 0)
        data_used = float(row.get("data_used_mb", 0) or 0)
        hour = (row.get("time") or "00:00:00").split(":")[0]
        device = row.get("device_type") or "Unknown"
        date_val = row.get("date") or "N/A"

        hotspot_connections[hotspot] += 1
        hotspot_duration_total[hotspot] += duration
        hotspot_duration_count[hotspot] += 1
        hotspot_data_total[hotspot] += data_used
        hourly_usage[hour] += 1
        hotspot_hour_matrix[(hotspot, hour)] += 1
        device_distribution[device] += 1
        avg_duration_by_device[device] += duration
        device_duration_count[device] += 1
        daily_usage[date_val] += 1
        hotspot_daily_usage[(hotspot, date_val)] += 1
        hotspot_avg_duration[hotspot].append(duration)

# MapReduce-style outputs
write_csv(OUT_MAPREDUCE / "hotspot_count", [["hotspot_id", "connection_count"]] + [[k, v] for k, v in sorted(hotspot_connections.items())])
write_csv(OUT_MAPREDUCE / "duration_analysis", [["hotspot_id", "avg_duration"]] + [[k, round(hotspot_duration_total[k] / hotspot_duration_count[k], 2)] for k in sorted(hotspot_connections)])
write_csv(OUT_MAPREDUCE / "data_usage", [["hotspot_id", "total_data_used_mb"]] + [[k, round(hotspot_data_total[k], 2)] for k in sorted(hotspot_connections)])
write_csv(OUT_MAPREDUCE / "hourly_usage", [["usage_hour", "connection_count"]] + [[hour, count] for hour, count in sorted(hourly_usage.items(), key=lambda item: int(item[0]))])

# Hive-style outputs
write_csv(OUT_HIVE / "hotspot_connections", [["hotspot_id", "connection_count"]] + [[k, v] for k, v in sorted(hotspot_connections.items())])
write_csv(OUT_HIVE / "avg_duration_by_hotspot", [["hotspot_id", "avg_duration_minutes"]] + [[k, round(hotspot_duration_total[k] / hotspot_duration_count[k], 2)] for k in sorted(hotspot_connections)])
write_csv(OUT_HIVE / "total_data_usage_by_hotspot", [["hotspot_id", "total_data_used_mb"]] + [[k, round(hotspot_data_total[k], 2)] for k in sorted(hotspot_connections)])
write_csv(OUT_HIVE / "device_distribution", [["device_type", "device_count"]] + [[k, v] for k, v in sorted(device_distribution.items())])
write_csv(OUT_HIVE / "hourly_usage", [["usage_hour", "connection_count"]] + [[hour, count] for hour, count in sorted(hourly_usage.items(), key=lambda item: int(item[0]))])
write_csv(OUT_HIVE / "daily_usage", [["date", "connection_count"]] + [[date_val, count] for date_val, count in sorted(daily_usage.items())])
write_csv(OUT_HIVE / "hotspot_hour_matrix", [["hotspot_id", "usage_hour", "connection_count"]] + [[hotspot, hour, count] for (hotspot, hour), count in sorted(hotspot_hour_matrix.items())])

print("Prepared processed outputs for local R analysis under output/mapreduce and output/hive")
