#!/bin/bash

set -euo pipefail


CONFIG="config/containers.yaml"


usage() {
    echo "Usage:"
    echo "  $0 <container_name>"
    echo
    echo "Example:"
    echo "  $0 sc_basic"
    exit 1
}


if [ $# -ne 1 ]; then
    usage
fi


NAME="$1"


# ------------------------------------------------------------------
# Read configuration from YAML
# ------------------------------------------------------------------

read_yaml() {
python3 - "$CONFIG" "$1" <<'PY'
import sys
import yaml

config_file = sys.argv[1]
key = sys.argv[2]

with open(config_file) as f:
    config = yaml.safe_load(f)

value = config

for item in key.split("."):
    value = value[item]

print(value)
PY
}


KERNEL_DIR=$(read_yaml containers.kernels.directory)
DEF_DIR=$(read_yaml containers.definitions.directory)
SIF_DIR=$(read_yaml containers.images.apptainer.directory)


# ------------------------------------------------------------------
# File locations
# ------------------------------------------------------------------

KERNEL_FILE="${KERNEL_DIR}/${NAME}.yaml"
DEF_FILE="${DEF_DIR}/${NAME}.def"
SIF_FILE="${SIF_DIR}/${NAME}.sif"


# ------------------------------------------------------------------
# Validate
# ------------------------------------------------------------------

echo "Checking container files..."

if [ ! -f "$KERNEL_FILE" ]; then
    echo
    echo "ERROR: Kernel YAML missing:"
    echo "  $KERNEL_FILE"
    exit 1
fi


if [ ! -f "$DEF_FILE" ]; then
    echo
    echo "ERROR: Container definition missing:"
    echo "  $DEF_FILE"
    exit 1
fi


if [ ! -d "$SIF_DIR" ]; then
    echo
    echo "ERROR: Apptainer image directory missing:"
    echo "  $SIF_DIR"
    exit 1
fi


# ------------------------------------------------------------------
# Build
# ------------------------------------------------------------------

echo
echo "======================================"
echo "Container build"
echo "======================================"
echo
echo "Name:"
echo "  $NAME"
echo
echo "Kernel configuration:"
echo "  $KERNEL_FILE"
echo
echo "Definition:"
echo "  $DEF_FILE"
echo
echo "Output:"
echo "  $SIF_FILE"
echo
echo "======================================"
echo


read -p "Continue? (y/n): " ANSWER

if [[ "$ANSWER" != "y" ]]; then
    echo "Cancelled"
    exit 0
fi


# replace with specific version if required
module load apptainer


apptainer build \
    "$SIF_FILE" \
    "$DEF_FILE"


echo
echo "Build complete:"
echo "$SIF_FILE"