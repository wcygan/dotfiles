#!/usr/bin/env bash
set -euo pipefail

if ! command -v mysql >/dev/null 2>&1; then
  echo "mysql client not found. Install mysql client and re-run." >&2
  exit 1
fi

if [[ -n "${MYSQL_PASSWORD:-}" && -z "${MYSQL_PWD:-}" ]]; then
  export MYSQL_PWD="${MYSQL_PASSWORD}"
fi

args=()
[[ -n "${MYSQL_HOST:-}" ]] && args+=("-h" "${MYSQL_HOST}")
[[ -n "${MYSQL_PORT:-}" ]] && args+=("-P" "${MYSQL_PORT}")
[[ -n "${MYSQL_USER:-}" ]] && args+=("-u" "${MYSQL_USER}")
[[ -n "${MYSQL_DATABASE:-}" ]] && args+=("${MYSQL_DATABASE}")

run() {
  local label="$1"
  local sql="$2"
  echo "\n# ${label}"
  mysql "${args[@]}" -e "${sql}"
}

run "Version" "SELECT VERSION() AS version, @@version_comment AS version_comment;"
run "SQL mode" "SELECT @@GLOBAL.sql_mode AS global_sql_mode, @@SESSION.sql_mode AS session_sql_mode;"
run "Engine defaults" "SELECT @@default_storage_engine AS default_storage_engine, @@transaction_isolation AS tx_isolation, @@autocommit AS autocommit;"
run "Character set" "SELECT @@character_set_server AS character_set_server, @@collation_server AS collation_server;"
run "Time zone" "SELECT @@time_zone AS time_zone, @@system_time_zone AS system_time_zone;"
run "Slow query log" "SHOW VARIABLES WHERE Variable_name IN ('slow_query_log','long_query_time','log_output','log_queries_not_using_indexes');"
