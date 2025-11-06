#!/usr/bin/env python3
import json
import argparse
import os

from benchmark import benchmark_model

def run_batch_benchmark(runs, num_runs=1):
    run_results = []
    for run_config in runs['runs']:
        model_path = run_config["model_path"]
        prompt = run_config["prompt"]
        tokens = 50
        replication_results = {}
        for run_idx in range(1, num_runs + 1):
            print(f"\n=== Running benchmark {run_idx}/{num_runs} for model '{model_path}' ===\n")
            try:
                result = benchmark_model(model_path, prompt, tokens)
                replication_results[run_idx] = result
            except Exception as e:
                print(f"Error running benchmark for model {model_path} prompt {prompt}: {e}")
        run_results.append(replication_results)
    
    results = {"result": run_results}
    return results

if __name__ == "__main__":
        # ---------------------------
    # Parse command-line arguments
    # ---------------------------
    parser = argparse.ArgumentParser(description="Batch benchmark LLaMA models from CSV")
    parser.add_argument("--json_file", required=True, help="Path to json file with columns: model,prompt")
    parser.add_argument("-r", "--runs", type=int, default=1, help="Number of times to run each pair sequentially")
    parser.add_argument("--output_folder", default=os.getcwd(), help="Number of times to run each pair sequentially")
    args = parser.parse_args()

    json_file = args.json_file
    num_runs = args.runs
    output_folder = args.output_folder

    with open(json_file, "r", encoding="utf-8") as f:
        runs = json.load(f)
        results = run_batch_benchmark(runs, num_runs)

    out_file = output_path = os.path.join(output_folder, "results.json")
    # ✅ Save JSON file
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2)

    print(f"Saved JSON to {out_file}")
    
