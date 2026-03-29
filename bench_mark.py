#!/usr/bin/env python3
"""Benchmarking tool. Zero dependencies."""
import time, sys, math, gc

def benchmark(fn, iterations=1000, warmup=10, label=None):
    for _ in range(warmup): fn()
    gc.disable()
    times = []
    for _ in range(iterations):
        start = time.perf_counter_ns()
        fn()
        times.append(time.perf_counter_ns() - start)
    gc.enable()
    return BenchResult(label or fn.__name__, times)

class BenchResult:
    def __init__(self, name, times_ns):
        self.name = name
        self.times = sorted(times_ns)
        self.n = len(times_ns)

    @property
    def mean(self): return sum(self.times) / self.n
    @property
    def median(self): return self.times[self.n//2]
    @property
    def p95(self): return self.times[int(self.n*0.95)]
    @property
    def p99(self): return self.times[int(self.n*0.99)]
    @property
    def min(self): return self.times[0]
    @property
    def max(self): return self.times[-1]
    @property
    def stdev(self):
        m = self.mean
        return math.sqrt(sum((t-m)**2 for t in self.times)/self.n)
    @property
    def ops_per_sec(self): return 1e9 / self.mean if self.mean > 0 else 0

    def _fmt(self, ns):
        if ns < 1000: return f"{ns:.0f}ns"
        if ns < 1e6: return f"{ns/1000:.1f}µs"
        if ns < 1e9: return f"{ns/1e6:.2f}ms"
        return f"{ns/1e9:.3f}s"

    def __repr__(self):
        return (f"{self.name}: mean={self._fmt(self.mean)} median={self._fmt(self.median)} "
                f"p95={self._fmt(self.p95)} min={self._fmt(self.min)} max={self._fmt(self.max)} "
                f"({self.ops_per_sec:.0f} ops/s)")

def compare(*results):
    baseline = results[0]
    lines = [str(baseline)]
    for r in results[1:]:
        ratio = r.mean / baseline.mean
        lines.append(f"{r}  ({ratio:.2f}x vs {baseline.name})")
    return "\n".join(lines)

if __name__ == "__main__":
    r1 = benchmark(lambda: sum(range(100)), iterations=10000, label="sum_100")
    r2 = benchmark(lambda: sum(range(1000)), iterations=10000, label="sum_1000")
    print(compare(r1, r2))
