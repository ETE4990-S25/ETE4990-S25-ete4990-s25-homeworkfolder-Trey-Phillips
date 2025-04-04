import time
import multiprocessing
import threading
import asyncio

# prime checker
def is_prime(n):
    if n <= 1:
        return False
    for i in range(2, int(n ** 0.5) + 1):
        if n % i == 0:
            return False
    return True

def prime_search(start, step, max_time, prime_list):
    highest = 0
    num = start
    local_start = time.time()
    while time.time() - local_start < max_time:
        if is_prime(num):
            highest = num
        num += step
    prime_list.append(highest)

#multiprocessing
def multiprocessing_prime(max_time=180):
    cores = multiprocessing.cpu_count()
    manager = multiprocessing.Manager()
    results = manager.list()
    processes = []

    for i in range(cores):
        p = multiprocessing.Process(target=prime_search, args=(i, cores, max_time, results))
        processes.append(p)
        p.start()

    for p in processes:
        p.join()
    return max(results) if results else 0

if __name__ == "__main__":
    print("Multiprocessing:", multiprocessing_prime(180))
