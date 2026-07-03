#!/bin/bash

set -e

repo_root=$(git rev-parse --show-toplevel)
cd "$repo_root" || exit 1

echo "Repo root: $repo_root"
echo "Running from: $(pwd)"

DIR="${DIR:-.}"
DRY_RUN=0

if [[ "$1" == "--dry-run" ]]; then
    DRY_RUN=1
    echo "🔍 DRY RUN MODE ENABLED"
fi

CONFIG_FILE="config/git_stage.yaml"

MAX_SIZE_MB=100
LOG_DIR="logs/git_stage"
SKIPPED_FILE="$LOG_DIR/skipped_files.txt"
SKIPPED_ABS_FILE="$LOG_DIR/skipped_files_abs_paths.txt"

# ----------------------------
# Counters (ADDED)
# ----------------------------
staged_count=0
skipped_ignore=0
skipped_size=0
deleted_count=0

# ----------------------------
# Load YAML config (if available)
# ----------------------------
if command -v python3 >/dev/null 2>&1 && [ -f "$CONFIG_FILE" ]; then
    MAX_SIZE_MB=$(python3 - <<EOF
import yaml
cfg = yaml.safe_load(open("$CONFIG_FILE"))
print(cfg["git_stage"]["max_size_mb"])
EOF
)
fi

max_size=$((MAX_SIZE_MB * 1024 * 1024))

mkdir -p "$LOG_DIR"

echo "Max file size: ${MAX_SIZE_MB}MB"

skipped_files=()

mapfile -d '' all_files < <(find "$DIR" -type f -not -path "*/.git/*" -print0)

total_files=${#all_files[@]}
processed=0
bar_width=50

update_progress_bar() {
    if (( total_files == 0 )); then return; fi

    percent=$((processed * 100 / total_files))
    filled=$((processed * bar_width / total_files))
    empty=$((bar_width - filled))

    bar=$(printf "%${filled}s" | tr ' ' '#')
    bar+=$(printf "%${empty}s" | tr ' ' '-')

    printf "\r[%s] %d%% (%d/%d)" "$bar" "$percent" "$processed" "$total_files"
}

for f in "${all_files[@]}"; do
    actual_size=$(stat -c%s "$f")

    if git check-ignore -q "$f"; then
        skipped_files+=("$f | ignored | $actual_size bytes")
        ((skipped_ignore++))

    elif (( actual_size > max_size )); then
        skipped_files+=("$f | too large | $actual_size bytes")
        ((skipped_size++))

    else
        if [[ "$DRY_RUN" -eq 0 ]]; then
            git add "$f"
            ((staged_count++))
        fi
    fi

    ((processed++))
    update_progress_bar
done

echo ""

# ----------------------------
# Write skipped logs
# ----------------------------
if [ ${#skipped_files[@]} -gt 0 ]; then
    printf "%s\n" "${skipped_files[@]}" > "$SKIPPED_FILE"
    echo "Skipped files saved to $SKIPPED_FILE"
fi

> "$SKIPPED_ABS_FILE"

if [ -f "$SKIPPED_FILE" ]; then
    while IFS='|' read -r filepath _; do
        filepath=$(echo "$filepath" | xargs)
        abs_path=$(readlink -f "$filepath" 2>/dev/null || true)

        if [ -n "$abs_path" ]; then
            echo "$abs_path" >> "$SKIPPED_ABS_FILE"
        fi
    done < "$SKIPPED_FILE"
fi

echo "Absolute paths saved to $SKIPPED_ABS_FILE"

# ----------------------------
# Stage deletions (safe)
# ----------------------------
if [[ "$DRY_RUN" -eq 0 ]]; then
    deleted_count=$(git ls-files --deleted "$DIR" | wc -l)
    git add -u "$DIR"
else
    echo "Dry run: no git staging performed"
fi

echo "Completed staging."

echo ""
echo "========================================"
echo "📦 Staging Summary"
echo "========================================"

echo "Total files scanned: $total_files"
echo "Staged: $staged_count"
echo "Deleted: $deleted_count"
echo "Skipped (ignored): $skipped_ignore"
echo "Skipped (too large): $skipped_size"

echo "========================================"
