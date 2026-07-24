#!/bin/bash

#
# Deactivate datasync CLI environment
#

if [[ "${BASH_SOURCE[0]}" == "${0}" ]]; then
    echo "Please run:"
    echo "  source scripts/cli/datasync/deactivate_datasync.sh"
    exit 1
fi


if [[ -z "${DATASYNC_ROOT}" ]]; then

    echo "datasync is not currently activated"

    return 0

fi


DATASYNC_BIN="${DATASYNC_ROOT}/scripts/cli/datasync"


#
# Remove datasync CLI location from PATH
#

case ":$PATH:" in
    *":${DATASYNC_BIN}:"*)
        PATH=":${PATH}:"
        PATH="${PATH//:${DATASYNC_BIN}:/:}"
        PATH="${PATH#:}"
        PATH="${PATH%:}"
        export PATH
        ;;
esac


#
# Remove environment variable
#

unset DATASYNC_ROOT


echo "datasync deactivated"
