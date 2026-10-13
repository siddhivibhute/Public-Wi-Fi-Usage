#!/usr/bin/env python3
"""MapReduce for total data consumption by hotspot.

Mapper output: hotspot_id -> data_used_mb
Reducer output: hotspot_id -> total data used
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
            data_used = float(row[8].strip())
        except (IndexError, ValueError):
            continue
        if hotspot_id and hotspot_id != "hotspot_id" and data_used >= 0:
            print(f"{hotspot_id}\t{data_used}")


def reducer():
    current_hotspot = None
    current_total = 0.0

    for line in sys.stdin:
        line = line.strip()
        if not line:
            continue
        parts = line.split("\t")
        if len(parts) != 2:
            continue
        hotspot_id, value = parts[0], parts[1]
        try:
            amount = float(value)
        except ValueError:
            continue

        if current_hotspot is None:
            current_hotspot = hotspot_id
        if hotspot_id == current_hotspot:
            current_total += amount
        else:
            print(f"{current_hotspot}\t{current_total:.2f}")
            current_hotspot = hotspot_id
            current_total = amount

    if current_hotspot is not None:
        print(f"{current_hotspot}\t{current_total:.2f}")


if __name__ == "__main__":
    mode = sys.argv[1].lower() if len(sys.argv) > 1 else "map"
    if mode == "map":
        mapper()
    elif mode == "reduce":
        reducer()
    else:
        raise ValueError("Usage: data_usage.py [map|reduce]")
