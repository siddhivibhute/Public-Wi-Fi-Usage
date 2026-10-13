#!/usr/bin/env python3
"""Generate PNG charts and summary CSV report from Hive/MapReduce output data.
Acts as Python visualization generator matching output/charts and output/reports.
"""

import csv
from pathlib import Path
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

PROJECT_ROOT = Path(__file__).resolve().parent.parent
HIVE_DIR = PROJECT_ROOT / "output" / "hive"
MAPREDUCE_DIR = PROJECT_ROOT / "output" / "mapreduce"
CHARTS_DIR = PROJECT_ROOT / "output" / "charts"
REPORTS_DIR = PROJECT_ROOT / "output" / "reports"

CHARTS_DIR.mkdir(parents=True, exist_ok=True)
REPORTS_DIR.mkdir(parents=True, exist_ok=True)


def read_csv(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        reader = csv.reader(f)
        header = next(reader, None)
        rows = list(reader)
    return header, rows


def generate_visualizations():
    plt.style.use('seaborn-v0_8-whitegrid' if 'seaborn-v0_8-whitegrid' in plt.style.available else 'default')

    # 1. Hotspot Connections
    _, rows = read_csv(HIVE_DIR / "hotspot_connections")
    hotspots = [r[0] for r in rows]
    counts = [int(r[1]) for r in rows]

    plt.figure(figsize=(10, 6))
    plt.bar(hotspots, counts, color='#1f6feb')
    plt.title("Wi-Fi Connections by Hotspot", fontsize=14, fontweight='bold')
    plt.xlabel("Hotspot ID")
    plt.ylabel("Connection Count")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig(CHARTS_DIR / "hotspot_connections.png", dpi=150)
    plt.close()

    # 2. Usage Over Time
    _, rows = read_csv(HIVE_DIR / "hourly_usage")
    hours = [int(r[0]) for r in rows]
    hourly_counts = [int(r[1]) for r in rows]

    plt.figure(figsize=(10, 6))
    plt.plot(hours, hourly_counts, marker='o', color='#0f9d58', linewidth=2)
    plt.title("Wi-Fi Usage Over Time", fontsize=14, fontweight='bold')
    plt.xlabel("Hour of Day")
    plt.ylabel("Number of Connections")
    plt.xticks(range(0, 24))
    plt.grid(True, linestyle='--', alpha=0.6)
    plt.tight_layout()
    plt.savefig(CHARTS_DIR / "usage_over_time.png", dpi=150)
    plt.close()

    # 3. Data Usage by Hotspot
    _, rows = read_csv(HIVE_DIR / "total_data_usage_by_hotspot")
    data_hotspots = [r[0] for r in rows]
    data_mb = [float(r[1]) for r in rows]

    plt.figure(figsize=(10, 6))
    plt.bar(data_hotspots, data_mb, color='#ff8a3d')
    plt.title("Total Data Consumption by Hotspot", fontsize=14, fontweight='bold')
    plt.xlabel("Hotspot ID")
    plt.ylabel("Data Used (MB)")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig(CHARTS_DIR / "data_usage_by_hotspot.png", dpi=150)
    plt.close()

    # 4. Device Type Distribution
    _, rows = read_csv(HIVE_DIR / "device_distribution")
    devices = [r[0] for r in rows]
    device_counts = [int(r[1]) for r in rows]

    plt.figure(figsize=(8, 8))
    colors = ['#1f6feb', '#0f9d58', '#ff8a3d', '#d93240', '#7c4dff']
    plt.pie(device_counts, labels=devices, autopct='%1.1f%%', colors=colors[:len(devices)], startangle=140)
    plt.title("Device Type Distribution", fontsize=14, fontweight='bold')
    plt.tight_layout()
    plt.savefig(CHARTS_DIR / "device_type_distribution.png", dpi=150)
    plt.close()

    # 5. Duration Histogram
    _, rows = read_csv(MAPREDUCE_DIR / "duration_analysis")
    durations = [float(r[1]) for r in rows]

    plt.figure(figsize=(10, 6))
    plt.hist(durations, bins=10, color='purple', edgecolor='white', alpha=0.7)
    plt.title("Histogram of Average Connection Duration", fontsize=14, fontweight='bold')
    plt.xlabel("Average Duration (Minutes)")
    plt.ylabel("Frequency")
    plt.tight_layout()
    plt.savefig(CHARTS_DIR / "duration_histogram.png", dpi=150)
    plt.close()

    # 6. Hotspot-Hour Heatmap
    _, rows = read_csv(HIVE_DIR / "hotspot_hour_matrix")
    matrix_dict = {}
    for r in rows:
        hs, hr, cnt = r[0], int(r[1]), int(r[2])
        if hs not in matrix_dict:
            matrix_dict[hs] = [0] * 24
        matrix_dict[hs][hr] = cnt

    hs_keys = sorted(matrix_dict.keys())
    heatmap_matrix = np.array([matrix_dict[hs] for hs in hs_keys])

    plt.figure(figsize=(12, 7))
    sns.heatmap(heatmap_matrix, xticklabels=range(24), yticklabels=hs_keys, cmap="YlOrRd", annot=False)
    plt.title("Hotspot x Hour Usage Heatmap", fontsize=14, fontweight='bold')
    plt.xlabel("Hour of Day")
    plt.ylabel("Hotspot ID")
    plt.tight_layout()
    plt.savefig(CHARTS_DIR / "hotspot_hour_heatmap.png", dpi=150)
    plt.close()

    # 7. Average Duration by Hotspot
    _, rows = read_csv(HIVE_DIR / "avg_duration_by_hotspot")
    avg_hs = [r[0] for r in rows]
    avg_dur = [float(r[1]) for r in rows]

    plt.figure(figsize=(10, 6))
    plt.bar(avg_hs, avg_dur, color='darkorange')
    plt.title("Average Duration by Hotspot", fontsize=14, fontweight='bold')
    plt.xlabel("Hotspot ID")
    plt.ylabel("Average Duration (Minutes)")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig(CHARTS_DIR / "avg_duration_by_hotspot.png", dpi=150)
    plt.close()

    # Summary Report CSV
    peak_idx = int(np.argmax(hourly_counts))
    most_used_idx = int(np.argmax(counts))

    report_rows = [
        ["metric", "value"],
        ["total_connections", sum(counts)],
        ["total_hotspots", len(hotspots)],
        ["avg_device_count", round(np.mean(device_counts), 2)],
        ["peak_usage_hour", hours[peak_idx]],
        ["peak_usage_count", hourly_counts[peak_idx]],
        ["most_used_hotspot", hotspots[most_used_idx]],
        ["most_used_hotspot_connections", counts[most_used_idx]],
    ]

    with open(REPORTS_DIR / "wifi_summary_report.csv", "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerows(report_rows)

    print("Charts and summary report successfully generated under output/charts and output/reports!")


if __name__ == "__main__":
    generate_visualizations()
