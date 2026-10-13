#!/usr/bin/env bash
set -euo pipefail

PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
DATASET_PATH="$PROJECT_ROOT/data/raw/wifi_usage.csv"

if ! command -v hdfs >/dev/null 2>&1; then
  echo "[ERROR] Hadoop HDFS is not available in the PATH. Install Hadoop first."
  exit 1
fi

if [[ ! -f "$DATASET_PATH" ]]; then
  echo "[ERROR] Dataset not found: $DATASET_PATH"
  echo "Run: python3 $PROJECT_ROOT/data/generate_wifi_usage.py"
  exit 1
fi

hdfs dfs -mkdir -p /wifi/raw /wifi/output /wifi/tmp
hdfs dfs -put -f "$DATASET_PATH" /wifi/raw/
hdfs dfs -ls -R /wifi
hdfs dfs -cat /wifi/raw/wifi_usage.csv | head -n 5

echo "[INFO] Wi-Fi dataset successfully loaded into HDFS at /wifi/raw/wifi_usage.csv"
