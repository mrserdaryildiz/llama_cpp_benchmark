#!/usr/bin/env python3
import csv
import subprocess
import sys
import argparse
import os

# ---------------------------
# Parse command-line arguments
# ---------------------------
parser = argparse.ArgumentParser(description="Batch benchmark LLaMA models from CSV")
parser.add_argument("--csv_file", required=True, help="Path to CSV file with columns: model,prompt")
parser.add_argument("-r", "--runs", type=int, default=1, help="Number of times to run each pair sequentially")
parser.add_argument("--benchmark_script", default="/workspace/source/benchmark.py",
                    help="Path to benchmark.py script")
args = parser.parse_args()

csv_file = args.csv_file
num_runs = args.runs
benchmark_script = args.benchmark_script

# ---------------------------
# Check CSV exists
# ---------------------------
if not os.path.exists(csv_file):
    print(f"Error: CSV file '{csv_file}' not found")
    sys.exit(1)

# ---------------------------
# Read CSV and loop
# ---------------------------
with open(csv_file, newline="", encoding="utf-8") as f:
    reader = csv.DictReader(f)
    if "model" not in reader.fieldnames or "prompt" not in reader.fieldnames:
        print("Error: CSV must have columns 'model' and 'prompt'")
        sys.exit(1)

    for row in reader:
        model_path = row["model"]
        prompt = row["prompt"]
        for run_idx in range(1, num_runs + 1):
            print(f"\n=== Running benchmark {run_idx}/{num_runs} for model '{model_path}' ===\n")
            try:
                subprocess.run(
                    ["python3", benchmark_script, model_path, prompt],
                    check=True
                )
            except subprocess.CalledProcessError as e:
                print(f"Error running benchmark for model {model_path}: {e}")
