import subprocess, sys, time, psutil, os, json

if len(sys.argv) < 3:
    print("Usage: python3 benchmark.py <model_path> <prompt>")
    sys.exit(1)

model_path = sys.argv[1]
prompt = sys.argv[2]

print(f"model_path: {model_path}", flush=True)
print(f"prompt: {prompt}", flush=True)

start_time = time.time()

print("benchmark script started", flush=True)

proc = psutil.Popen(
    ["llama-cli", "-m", model_path, "-p", prompt, "-n", "50", "--single-turn"],
    stdout=subprocess.PIPE,
    stderr=subprocess.PIPE
)

print("llama-cli run started", flush=True)

cpu_usage = []
mem_usage = []
while proc.poll() is None:
    try:
        cpu_usage.append(proc.cpu_percent(interval=0.1))
        mem_usage.append(proc.memory_info().rss / (1024 * 1024)) # in MB
    except psutil.NoSuchProcess:
        break

stdout, stderr = proc.communicate()
end_time = time.time()

result = {
        "model": model_path,
        "prompt": prompt,
        "duration_sec": round(end_time - start_time, 2),
        "avg_cpu_percent": round(sum(cpu_usage) / len(cpu_usage), 2) if cpu_usage else 0,
        "peak_memory_mb": round(max(mem_usage), 2) if mem_usage else 0,
        "output_preview": stdout.decode(errors="ignore")[:200],
    }

os.makedirs("../results", exist_ok=True)
output_file = f"../results/{os.path.basename(model_path)}.json"
with open(output_file, "w") as f:
    json.dump(result, f, indent=2)

print(f"✅ Benchmark done! Results saved to {output_file}")