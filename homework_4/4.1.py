import time
import threading
import multiprocessing

def fib(n):
    a, b = 0, 1
    for _ in range(n):
        a, b = b, a + b
    return a

def benchmark_sync(n, runs):
    start = time.time()
    for _ in range(runs):
        fib(n)
    return time.time() - start

def benchmark_threads(n, runs):
    threads = []
    start = time.time()
    for _ in range(runs):
        t = threading.Thread(target=fib, args=(n,))
        threads.append(t)
        t.start()
    for t in threads:
        t.join()
    return time.time() - start

def benchmark_processes(n, runs):
    processes = []
    start = time.time()
    for _ in range(runs):
        p = multiprocessing.Process(target=fib, args=(n,))
        processes.append(p)
        p.start()
    for p in processes:
        p.join()
    return time.time() - start

if __name__ == "__main__":
    n = 500000
    runs = 10

    sync_time = benchmark_sync(n, runs)

    threads_time = benchmark_threads(n, runs)

    processes_time = benchmark_processes(n, runs)

    with open("artifacts/4_1_result.txt", "w") as f:
        f.write(f"Synchronous execution ({runs} runs): {sync_time:.2f} sec\n")
        f.write(f"Threads ({runs} threads): {threads_time:.2f} sec\n")
        f.write(f"Processes ({runs} processes): {processes_time:.2f} sec\n")
