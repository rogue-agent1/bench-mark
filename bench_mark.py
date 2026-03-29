#!/usr/bin/env python3
"""bench_mark: Microbenchmarking framework with statistics."""
import time, math, sys

class BenchResult:
    def __init__(self, name, times):
        self.name = name; self.times = sorted(times)
        self.n = len(times)
    @property
    def mean(self): return sum(self.times)/self.n
    @property
    def median(self): return self.times[self.n//2]
    @property
    def min(self): return self.times[0]
    @property
    def max(self): return self.times[-1]
    @property
    def stdev(self):
        m = self.mean
        return math.sqrt(sum((t-m)**2 for t in self.times)/self.n)
    @property
    def p95(self): return self.times[int(self.n*0.95)]
    def __repr__(self):
        return f"{self.name}: mean={self.mean*1e6:.1f}us median={self.median*1e6:.1f}us min={self.min*1e6:.1f}us max={self.max*1e6:.1f}us stdev={self.stdev*1e6:.1f}us (n={self.n})"

def bench(name, fn, n=1000, warmup=100):
    for _ in range(warmup): fn()
    times = []
    for _ in range(n):
        t0 = time.perf_counter()
        fn()
        times.append(time.perf_counter() - t0)
    return BenchResult(name, times)

def compare(results):
    baseline = results[0]
    lines = [str(baseline)]
    for r in results[1:]:
        ratio = r.mean / baseline.mean if baseline.mean > 0 else 0
        lines.append(f"{r} ({ratio:.2f}x vs {baseline.name})")
    return "\n".join(lines)

def test():
    r = bench("noop", lambda: None, n=100, warmup=10)
    assert r.n == 100
    assert r.mean >= 0
    assert r.min <= r.median <= r.max
    assert r.stdev >= 0
    assert "noop" in repr(r)
    # Compare
    r1 = bench("list", lambda: list(range(10)), n=50, warmup=5)
    r2 = bench("tuple", lambda: tuple(range(10)), n=50, warmup=5)
    text = compare([r1, r2])
    assert "list" in text
    assert "tuple" in text
    print("All tests passed!")

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "test": test()
    else: print("Usage: bench_mark.py test")
