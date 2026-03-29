from bench_mark import benchmark, compare, BenchResult
r = benchmark(lambda: sum(range(10)), iterations=100, label="test")
assert r.n == 100
assert r.mean > 0
assert r.ops_per_sec > 0
assert "test" in str(r)
print("Benchmark tests passed")