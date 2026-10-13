#!/usr/bin/env python3
"""MapReduce for average connection duration by hotspot.

Mapper output: hotspot_id -> duration_minutes
Reducer output: hotspot_id -> average duration
"""

import csv
import sys


def parse_csv_line(line):
    raw = line.strip()
    if not raw:
        return None
    values = next(csv.reader([raw]))
    if len(values) < 9:
        return None
    return values


def mapper():
    for line in sys.stdin:
        row = parse_csv_line(line)
        if row is None:
            continue
        try:
            hotspot_id = row[3].strip()
            duration = float(row[7].strip())
        except (IndexError, ValueError):
            continue
        if hotspot_id and hotspot_id != "hotspot_id" and duration >= 0:
            print(f"{hotspot_id}\t{duration}")


def reducer():
    current_hotspot = None
    running_total = 0.0
    count = 0

    for line in sys.stdin:
        line = line.strip()
        if not line:
            continue
        parts = line.split("\t")
        if len(parts) != 2:
            continue
        hotspot_id, duration_raw = parts[0], parts[1]
        try:
            duration_value = float(duration_raw)
        except ValueError:
            continue

        if current_hotspot is None:
            current_hotspot = hotspot_id
        if hotspot_id == current_hotspot:
            running_total += duration_value
            count += 1
        else:
            avg = running_total / count if count else 0.0
            print(f"{current_hotspot}\t{avg:.2f}")
            current_hotspot = hotspot_id
            running_total = duration_value
            count = 1

    if current_hotspot is not None:
        avg = running_total / count if count else 0.0
        print(f"{current_hotspot}\t{avg:.2f}")


if __name__ == "__main__":
    mode = sys.argv[1].lower() if len(sys.argv) > 1 else "map"
    if mode == "map":
        mapper()
    elif mode == "reduce":
        reducer()
    else:
        raise ValueError("Usage: duration_analysis.py [map|reduce]")
