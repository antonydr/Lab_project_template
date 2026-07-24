#!/bin/bash

#
# Activate datasync CLI environment
#

# Prevent execution instead of sourcing
if [[ "${BASH_SOURCE[0]}" == "${0}" ]]; then
    echo "Please run:"
    echo "  source scripts/cli/datasync/activate_datasync.sh"
    exit 1
fi


PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../../.." && pwd)"

DATASYNC_BIN="$PROJECT_ROOT/scripts/cli/datasync"


#
# Check if already activated
#

if [[ -n "${DATASYNC_ROOT}" ]]; then
    if [[ "${DATASYNC_ROOT}" == "${PROJECT_ROOT}" ]]; then
        echo "datasync already activated"
        return 0
    fi
fi


#
# Add CLI location to PATH
#

case ":$PATH:" in
    *":${DATASYNC_BIN}:"*)
        ;;
    *)
        export PATH="${DATASYNC_BIN}:${PATH}"
        ;;
esac


#
# Store activation state
#

export DATASYNC_ROOT="$PROJECT_ROOT"


echo "datasync activated"
echo "Run: datasync --help"
