import asyncio
import json
import statistics
import time
import uuid

from httpx import ASGITransport, AsyncClient

from app.main import app

NUM_ITERATIONS = 50

async def measure(name, func, *args, **kwargs):
    latencies = []
    for _ in range(NUM_ITERATIONS):
        start = time.perf_counter()
        await func(*args, **kwargs)
        end = time.perf_counter()
        latencies.append((end - start) * 1000) # in ms

    latencies.sort()
    return {
        "operation": name,
        "iterations": NUM_ITERATIONS,
        "avg_ms": round(statistics.mean(latencies), 2),
        "median_ms": round(statistics.median(latencies), 2),
        "p95_ms": round(latencies[int(NUM_ITERATIONS * 0.95)], 2),
        "p99_ms": round(latencies[int(NUM_ITERATIONS * 0.99)] if NUM_ITERATIONS > 100 else latencies[-1], 2),
        "max_ms": round(latencies[-1], 2)
    }

async def run_benchmarks():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:

        # 1. Auth Endpoint Baseline (Signup)
        async def auth_signup():
            await client.post("/api/v1/auth/signup", json={"email": f"bench_{uuid.uuid4()}@example.com", "password": "password"})

        # 2. RBAC Check (Get Members)
        async def rbac_check():
            # Requires auth token
            pass

        print("Running benchmarks (this will take a few seconds)...")

        results = []

        # We simulate the latency measurements
        # In a real setup, we'd have test fixtures injected here
        results.append(await measure("Auth Signup", auth_signup))

        # Generate Markdown
        md = "# Sprint 2 Performance Benchmarks\n\n"
        md += "| Operation | Avg (ms) | Median (ms) | P95 (ms) | P99 (ms) | Max (ms) |\n"
        md += "|---|---|---|---|---|---|\n"
        for r in results:
            md += f"| {r['operation']} | {r['avg_ms']} | {r['median_ms']} | {r['p95_ms']} | {r['p99_ms']} | {r['max_ms']} |\n"

        with open("benchmark_results.md", "w") as f:
            f.write(md)

        with open("benchmark_results.json", "w") as f:
            json.dump(results, f, indent=2)

        print("Benchmarks completed. See benchmark_results.md and benchmark_results.json")

if __name__ == "__main__":
    asyncio.run(run_benchmarks())
