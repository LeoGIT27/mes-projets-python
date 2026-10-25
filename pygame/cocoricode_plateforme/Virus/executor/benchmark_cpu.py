import time
import math

def run_cpu_benchmark(duration=5):
    start = time.time()
    iterations = 0

    x = 1.000001

    while time.time() - start < duration:
        for _ in range(100000):
            x = math.sin(x) * math.cos(x) + math.sqrt(abs(x) + 1)
            iterations += 1

    elapsed = time.time() - start
    score = int(iterations / elapsed)

    return {
        "temps": round(elapsed, 2),
        "iterations": iterations,
        "score_cpu": score
    }