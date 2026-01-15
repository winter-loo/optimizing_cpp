#include <benchmark/benchmark.h>

// Declaration of the function from main.cc, conditionally compiled
void Func(int a[], int & r);

static void BM_Func(benchmark::State& state) {
  int a[100];
  int r = 10;
  for (auto _ : state) {
    Func(a, r);
    benchmark::DoNotOptimize(a);
  }
}
BENCHMARK(BM_Func);

BENCHMARK_MAIN();