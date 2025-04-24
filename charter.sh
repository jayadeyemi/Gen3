#!/usr/bin/env bash
set -euo pipefail

BASE_DIR="yaml_tree/commons"

# List of directories to create
dirs=(
  "$BASE_DIR/charts"
  "$BASE_DIR/crds"
  "$BASE_DIR/templates"
)

# Create directories if they don't exist
for d in "${dirs[@]}"; do
  if [[ ! -d "$d" ]]; then
    mkdir -p "$d"
    echo "Created directory: $d"
  fi
done

# List of files to create
files=(
  "$BASE_DIR/Chart.yaml"
  "$BASE_DIR/README.md"
  "$BASE_DIR/values.yaml"
  "$BASE_DIR/values.schema.json"
  "$BASE_DIR/templates/NOTES.txt"
)

# Create files if they don't exist
for f in "${files[@]}"; do
  if [[ ! -e "$f" ]]; then
    touch "$f"
    echo "Created file: $f"
  fi
done

echo "YAML chart scaffold is now in place."
