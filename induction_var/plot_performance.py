import subprocess
import json
import matplotlib.pyplot as plt
import os
import sys

def run_benchmark(version):
    print(f"Building and running benchmark for version {version}...")
    
    # Set the FUNC environment variable for just
    env = os.environ.copy()
    env["FUNC"] = str(version)
    
    build_cmd = ["just", "build"]
    subprocess.check_call(build_cmd, cwd="induction_var", env=env)

    # Run the benchmark executable directly to get JSON output
    # The executable is likely at induction_var/build/bench
    bench_executable = os.path.join("induction_var", "build", "bench")
    
    # Verify executable exists
    if not os.path.exists(bench_executable):
        raise FileNotFoundError(f"Benchmark executable not found at {bench_executable}")

    cmd = [bench_executable, "--benchmark_format=json"]
    result = subprocess.run(cmd, capture_output=True, text=True)
    
    if result.returncode != 0:
        print(f"Error running benchmark for version {version}:")
        print(result.stderr)
        return None

    try:
        data = json.loads(result.stdout)
        # Assuming there is only one benchmark run per execution or we take the first one
        # The benchmark name is BM_Func
        for benchmark in data['benchmarks']:
            if benchmark['name'] == 'BM_Func':
                return benchmark
    except json.JSONDecodeError:
        print(f"Failed to parse JSON output for version {version}")
        print(result.stdout)
    
    return None

def main():
    versions = [1, 2, 3, 4]
    results = []

    for v in versions:
        res = run_benchmark(v)
        if res:
            results.append(res)
        else:
            print(f"Skipping version {v} due to errors.")

    if not results:
        print("No results collected.")
        return

    # Extract data for plotting
    # We will use 'cpu_time' as the metric, or 'real_time'
    times = [r['cpu_time'] for r in results]
    labels = [f"Ver {v}" for v in versions] # Simplified labels
    
    # Optional: Get time unit
    time_unit = results[0].get('time_unit', 'ns')

    # Plotting
    plt.figure(figsize=(10, 6))
    bars = plt.bar(labels, times, color=['skyblue', 'lightgreen', 'orange', 'lightcoral'])
    
    plt.xlabel('Function Version')
    plt.ylabel(f'CPU Time ({time_unit})')
    plt.title('Performance Comparison of Loop Optimization Versions')
    plt.grid(axis='y', linestyle='--', alpha=0.7)

    # Add value labels on top of bars
    for bar in bars:
        yval = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2, yval, f'{yval:.2f}', ha='center', va='bottom')

    output_file = "induction_var/performance_graph.png"
    plt.savefig(output_file)
    print(f"Graph saved to {output_file}")

if __name__ == "__main__":
    main()
