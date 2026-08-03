#!/bin/bash

# --------------------------------------------------
# Development environment activation
# --------------------------------------------------

if [[ "${BASH_SOURCE[0]}" == "${0}" ]]; then
    echo "Error: this script must be sourced"
    echo "Run:"
    echo "  source $0"
    exit 1
fi

set -e

# Activate module if required
echo "Loading Miniforge module..."
module load Miniforge

# Activate conda env
echo "Activating conda environment: environment-dev"
conda activate environment-dev

echo ""
echo "Development environment activated:"
echo "  Environment: $CONDA_DEFAULT_ENV"
echo ""
