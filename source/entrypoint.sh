#!/bin/bash
set -e

# Example usage:
# docker run myimage --csv_file /workspace/source/batch_inputs.csv -r 2

python3 /workspace/source/batch_benchmark.py "$@"
