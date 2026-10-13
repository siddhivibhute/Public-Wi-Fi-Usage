#!/usr/bin/env python3
"""Generate a synthetic Wi-Fi usage dataset for an academic Big Data micro-project.

The dataset is intentionally synthetic and clearly labeled as a simulated dataset.
It contains 10,000+ records and is designed to mimic realistic Wi-Fi usage patterns
for hotspot analysis, time trends, duration, and data consumption.
"""

import csv
import os
import random
from datetime import datetime, timedelta

OUTPUT_DIR = os.path.join(os.path.dirname(__file__), "raw")
OUTPUT_FILE = os.path.join(OUTPUT_DIR, "wifi_usage.csv")

HOTSPOT_LOCATIONS = {
    "HS-101": "Library North Wing",
    "HS-102": "Cafeteria Block",
    "HS-103": "Main Gate Plaza",
    "HS-104": "Computer Lab 1",
    "HS-105": "Lecture Hall A",
    "HS-106": "Student Center",
    "HS-107": "Sports Complex",
    "HS-108": "Hostel Lobby",
    "HS-109": "Research Block",
    "HS-110": "Auditorium Entrance",
}

DEVICE_TYPES = ["Smartphone", "Laptop", "Tablet", "Wearable", "IoT"]
AUTH_TYPES = ["Open", "WPA2", "Captive Portal", "802.1X"]
NETWORK_TYPES = ["2.4GHz", "5GHz"]
SESSION_STATUS = ["Connected", "Idle", "Disconnected"]


def random_date(start_year=2024, end_year=2025):
    start = datetime(start_year, 1, 1)
    end = datetime(end_year, 12, 31)
    delta = end - start
    random_days = random.randint(0, delta.days)
    return (start + timedelta(days=random_days)).strftime("%Y-%m-%d")


def random_time():
    hour = random.randint(0, 23)
    minute = random.randint(0, 59)
    second = random.randint(0, 59)
    return f"{hour:02d}:{minute:02d}:{second:02d}"


def build_duration_minutes():
    # Use a realistic distribution emphasizing shorter sessions while allowing longer sessions.
    return max(5, int(random.betavariate(2.2, 5.5) * 250))


def build_data_used_mb(duration_minutes, device_type):
    base = {"Smartphone": 4.5, "Laptop": 14.0, "Tablet": 6.2, "Wearable": 1.1, "IoT": 0.7}
    multiplier = random.uniform(0.8, 1.7)
    data_mb = duration_minutes * base[device_type] * multiplier
    return round(max(1.0, data_mb), 2)


def generate_dataset(rows=12000):
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    fieldnames = [
        "connection_id",
        "date",
        "time",
        "hotspot_id",
        "hotspot_location",
        "user_id",
        "device_type",
        "duration_minutes",
        "data_used_mb",
        "authentication_type",
        "network_type",
        "session_status",
        "download_mb",
        "upload_mb",
    ]

    with open(OUTPUT_FILE, "w", newline="", encoding="utf-8") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

        hotspot_ids = list(HOTSPOT_LOCATIONS.keys())
        for idx in range(1, rows + 1):
            hotspot_id = random.choice(hotspot_ids)
            device_type = random.choice(DEVICE_TYPES)
            duration = build_duration_minutes()
            data_used = build_data_used_mb(duration, device_type)
            download = round(data_used * random.uniform(0.55, 0.75), 2)
            upload = round(data_used - download, 2)
            row = {
                "connection_id": f"CONN-{idx:06d}",
                "date": random_date(),
                "time": random_time(),
                "hotspot_id": hotspot_id,
                "hotspot_location": HOTSPOT_LOCATIONS[hotspot_id],
                "user_id": f"USER-{random.randint(1000, 9999)}",
                "device_type": device_type,
                "duration_minutes": duration,
                "data_used_mb": data_used,
                "authentication_type": random.choice(AUTH_TYPES),
                "network_type": random.choice(NETWORK_TYPES),
                "session_status": random.choice(SESSION_STATUS),
                "download_mb": download,
                "upload_mb": upload,
            }
            writer.writerow(row)

    print(f"Generated {rows} synthetic Wi-Fi records in {OUTPUT_FILE}")
    print("Note: This dataset is synthetic and intended for academic Big Data demonstration.")


if __name__ == "__main__":
    generate_dataset(rows=12000)
