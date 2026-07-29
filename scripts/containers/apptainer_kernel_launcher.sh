#!/bin/bash
set -euo pipefail

source /etc/profile.d/modules.sh
module load apptainer/1.4.1

IMAGE="$1"
EXECUTABLE="$2"
CONNECTION="$3"

if [[ "$EXECUTABLE" == "R" ]]; then
    exec apptainer exec \
        --writable-tmpfs \
        -B /run/user/$UID:/run/user/$UID \
        "$IMAGE" \
        R --slave -e "IRkernel::main()" --args "$CONNECTION"
else
    exec apptainer exec \
        --writable-tmpfs \
        -B /run/user/$UID:/run/user/$UID \
        "$IMAGE" \
        "$EXECUTABLE" \
        -m ipykernel_launcher \
        -f "$CONNECTION"
fi