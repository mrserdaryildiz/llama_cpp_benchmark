import subprocess, argparse, time, psutil, os
import platform, multiprocessing

def benchmark_model(model_path, prompt, tokens):
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
            "model_path": model_path,
            "prompt": prompt,
            "duration_sec": round(end_time - start_time, 2),
            "avg_cpu_percent": round(sum(cpu_usage) / len(cpu_usage), 2) if cpu_usage else 0,
            "peak_memory_mb": round(max(mem_usage), 2) if mem_usage else 0,

            "tokens_generated": tokens,
            "tokens_per_second": round(tokens / (end_time - start_time), 2),
            "total_cpu_time_sec": sum(cpu_usage) * 0.1,  # approximate CPU time
            "model_size_mb": round(os.path.getsize(model_path) / (1024 * 1024), 2),
        }

    result["system_info"] = {
        "cpu": platform.processor(),
        "cores": multiprocessing.cpu_count(),
        "ram_gb": round(psutil.virtual_memory().total / (1024 ** 3), 2)
    }

    result["output_preview"] = stdout.decode(errors="ignore") # [:200],
    result["stderr_preview"] = stderr.decode(errors="ignore") #[:200],

    print(f"✅ Benchmark done! Results is {result}")
    return result

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Benchmark LLaMA model using llama-cli")
    parser.add_argument("model_path", help="Path to GGUF model file")
    parser.add_argument("prompt", help="Prompt text to use for inference")
    parser.add_argument("-n", "--tokens", type=int, default=50, help="Number of tokens to generate")
    args = parser.parse_args()  

    model_path = args.model_path
    prompt = args.prompt
    tokens = args.tokens

    benchmark_model(model_path, prompt, tokens)