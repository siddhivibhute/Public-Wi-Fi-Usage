#!/usr/bin/env bash
set -euo pipefail

PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
HIVE_DIR="$PROJECT_ROOT/hive"

if ! command -v hive >/dev/null 2>&1; then
  echo "[ERROR] Hive is not installed or not in PATH."
  exit 1
fi

hive -f "$HIVE_DIR/create_database.hql"
hive -f "$HIVE_DIR/create_tables.hql"
hive -f "$HIVE_DIR/load_data.hql"
hive -f "$HIVE_DIR/analytics_queries.hql"

echo "[INFO] Hive database and analytics queries completed."
