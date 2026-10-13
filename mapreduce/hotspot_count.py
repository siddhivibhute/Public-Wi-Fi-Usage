#!/usr/bin/env python3
"""MapReduce for hotspot connection count.

Mapper output: hotspot_id -> 1
Reducer output: hotspot_id -> total connections
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
        except IndexError:
            continue
        if hotspot_id and hotspot_id != "hotspot_id":
            print(f"{hotspot_id}\t1")


def reducer():
    current_hotspot = None
    total = 0
    for line in sys.stdin:
        line = line.strip()
        if not line:
            continue
        parts = line.split("\t")
        if len(parts) != 2:
            continue
        hotspot_id, count = parts[0], parts[1]
        try:
            count_value = int(count)
        except ValueError:
            continue

        if current_hotspot is None:
            current_hotspot = hotspot_id
        if hotspot_id == current_hotspot:
            total += count_value
        else:
            print(f"{current_hotspot}\t{total}")
            current_hotspot = hotspot_id
            total = count_value

    if current_hotspot is not None:
        print(f"{current_hotspot}\t{total}")


if __name__ == "__main__":
    mode = sys.argv[1].lower() if len(sys.argv) > 1 else "map"
    if mode == "map":
        mapper()
    elif mode == "reduce":
        reducer()
    else:
        raise ValueError("Usage: hotspot_count.py [map|reduce]")
