#!/usr/bin/env python3
"""MapReduce for hour-wise usage count.

Mapper output: hour -> 1
Reducer output: hour -> total connections
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
            time_value = row[2].strip()
        except IndexError:
            continue
        if time_value and time_value != "time":
            hour = time_value.split(":")[0]
            try:
                int(hour)
            except ValueError:
                continue
            print(f"{hour}\t1")


def reducer():
    current_hour = None
    total = 0

    for line in sys.stdin:
        line = line.strip()
        if not line:
            continue
        parts = line.split("\t")
        if len(parts) != 2:
            continue
        hour, count = parts[0], parts[1]
        try:
            count_value = int(count)
        except ValueError:
            continue

        if current_hour is None:
            current_hour = hour
        if hour == current_hour:
            total += count_value
        else:
            print(f"{current_hour}\t{total}")
            current_hour = hour
            total = count_value

    if current_hour is not None:
        print(f"{current_hour}\t{total}")


if __name__ == "__main__":
    mode = sys.argv[1].lower() if len(sys.argv) > 1 else "map"
    if mode == "map":
        mapper()
    elif mode == "reduce":
        reducer()
    else:
        raise ValueError("Usage: hourly_usage.py [map|reduce]")
