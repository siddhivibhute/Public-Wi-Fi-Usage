#!/usr/bin/env bash
set -euo pipefail

PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$PROJECT_ROOT"

if ! command -v hadoop >/dev/null 2>&1; then
  echo "[ERROR] Hadoop is not installed or not in PATH."
  exit 1
fi

if [[ -z "${HADOOP_HOME:-}" ]]; then
  echo "[INFO] HADOOP_HOME is not set. Using default installation path if available."
fi

STREAMING_JAR="$(ls ${HADOOP_HOME:-/usr/local/hadoop}/share/hadoop/tools/lib/hadoop-streaming-*.jar 2>/dev/null | head -n 1)"
if [[ -z "$STREAMING_JAR" ]]; then
  echo "[ERROR] Hadoop streaming JAR not found. Verify HADOOP_HOME or Hadoop installation."
  exit 1
fi

PYTHON_BIN="${PYTHON_BIN:-python3}"

run_job() {
  local job_name="$1"
  local mapper_script="$2"
  local reducer_script="$3"
  local output_path="/wifi/output/${job_name}"

  echo "[INFO] Running ${job_name} job..."
  hadoop jar "$STREAMING_JAR" \
    -files "$PROJECT_ROOT/mapreduce/${mapper_script},$PROJECT_ROOT/mapreduce/${reducer_script}" \
    -mapper "${PYTHON_BIN} ${mapper_script} map" \
    -reducer "${PYTHON_BIN} ${reducer_script} reduce" \
    -input /wifi/raw/wifi_usage.csv \
    -output "$output_path"

  echo "[INFO] ${job_name} output stored at ${output_path}"
}

run_job hotspot_count hotspot_count.py hotspot_count.py
run_job duration_analysis duration_analysis.py duration_analysis.py
run_job data_usage data_usage.py data_usage.py
run_job hourly_usage hourly_usage.py hourly_usage.py

echo "[INFO] All MapReduce jobs completed."
