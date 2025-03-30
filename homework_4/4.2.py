import math
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor
import time
import os


def _worker(f, a, step, start, end):
    partial_acc = 0.0
    for i in range(start, end):
        x = a + i * step
        partial_acc += f(x) * step
    return partial_acc


def integrate(f, a, b, *, n_jobs=1, n_iter=20000000, executor_class=ThreadPoolExecutor):
    step = (b - a) / n_iter
    total_iterations = n_iter

    chunk_size = total_iterations // n_jobs
    remainder = total_iterations % n_jobs

    chunks = []
    start_idx = 0
    for i in range(n_jobs):
        end_idx = start_idx + chunk_size
        if i < remainder:
            end_idx += 1
        chunks.append((start_idx, end_idx))
        start_idx = end_idx

    with executor_class(max_workers=n_jobs) as executor:
        futures = []
        for s, e in chunks:
            future = executor.submit(_worker, f, a, step, s, e)
            futures.append(future)

        total = 0.0
        for future in futures:
            total += future.result()

    return total


def benchmark():
    cpu_num = os.cpu_count()
    max_jobs = cpu_num * 2
    results = []

    for n_jobs in range(1, max_jobs + 1):
        start_threads = time.time()
        integrate(math.cos, 0, math.pi / 2, n_jobs=n_jobs, executor_class=ThreadPoolExecutor)
        time_threads = time.time() - start_threads

        start_processes = time.time()
        integrate(math.cos, 0, math.pi / 2, n_jobs=n_jobs, executor_class=ProcessPoolExecutor)
        time_processes = time.time() - start_processes

        results.append((n_jobs, time_threads, time_processes))
        print(f"n_jobs={n_jobs}, Threads: {time_threads:.2f}s, Processes: {time_processes:.2f}s")

    with open("artifacts/4_2_result.txt", "w") as f:
        f.write("+--------+-------------------+-------------------+\n")
        f.write("| n_jobs | ThreadPool (s)    | ProcessPool (s)   |\n")
        f.write("+--------+-------------------+-------------------+\n")

        for n_jobs, t_time, p_time in results:
            f.write(f"| {n_jobs:^6} | {t_time:^17.4f} | {p_time:^17.4f} |\n")
            f.write("+--------+-------------------+-------------------+\n")


if __name__ == "__main__":
    benchmark()