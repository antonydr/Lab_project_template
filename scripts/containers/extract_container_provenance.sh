#!/usr/bin/env bash
set -euo pipefail

if [ "$#" -ne 1 ]; then
    echo "Usage:"
    echo "  $0 <container_name>"
    exit 1
fi

NAME="$1"

# Find project root from script location
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(realpath "${SCRIPT_DIR}/../..")"

#CONTAINER_DIR="${PROJECT_ROOT}/envs/containers"
CONTAINER_DIR="/nobackup/proj/comet_mrfichthyosis/users/nadr6/containers/sifs"

SIF="${CONTAINER_DIR}/${NAME}.sif"

OUT_DIR="${PROJECT_ROOT}/envs/containers/artifacts/${NAME}"

# ---- Check SIF exists ----

if [ ! -f "${SIF}" ]; then
    echo "ERROR: SIF not found:"
    echo "  ${SIF}"
    exit 1
fi

# ---- Create output directory ----

mkdir -p "${OUT_DIR}"

echo "Project root:"
echo "  ${PROJECT_ROOT}"

echo "Container:"
echo "  ${SIF}"

echo "Output:"
echo "  ${OUT_DIR}"
echo

# ---- Extract provenance files ----

FILES=(
    "${NAME}-explicit.txt"
    "${NAME}-environment.yml"
    "${NAME}-history.yml"
)

for FILE in "${FILES[@]}"; do

    echo "Extracting ${FILE}"

    apptainer exec "${SIF}" \
        cat "/opt/${FILE}" \
        > "${OUT_DIR}/${FILE}"

done


# ---- Record SIF checksum ----

echo "Creating checksum"

sha256sum "${SIF}" \
    > "${OUT_DIR}/${NAME}.sif.sha256"


echo
echo "Completed successfully."
echo
echo "Artifacts:"
ls -lh "${OUT_DIR}"
