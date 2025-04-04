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

def prime_search(start, step, max_time):
    highest = 0
    num = start
    local_start = time.time()
    while time.time() - local_start < max_time:
        if is_prime(num):
            highest = num
        num += step
    return highest

#multiprocessing
def multiprocessing_search(start, step, max_time, result_list):
    result = prime_search(start, step, max_time)
    result_list.append(result)

def multiprocessing_prime(max_time=180):
    cores = multiprocessing.cpu_count()
    manager = multiprocessing.Manager()
    result_list = manager.list()
    processes = []

    for i in range(cores):
        p = multiprocessing.Process(target=multiprocessing_search, args=(i, cores, max_time, result_list))
        processes.append(p)
        p.start()

    for p in processes:
        p.join()

    return max(result_list) if result_list else 0

#threading
def threaded_prime(max_time=180, thread_num=2):
    result_list = [0]  
    lock = threading.Lock()

    def thread_search(i):
        result = prime_search(i, thread_num, max_time)
        with lock:
            result_list[0] = max(result_list[0], result)

    threads = []
    for i in range(thread_num):
        t = threading.Thread(target=thread_search, args=(i, ))
        threads.append(t)
        t.start()
    for t in threads:
        t.join()

    return result_list[0]

#asynchronous
async def asynchronous_prime(max_time=180):
    highest = 0
    num = 0
    start_time = time.time()

    while time.time() - start_time < max_time:
        result = await asyncio.to_thread(is_prime, num)
        if result:
            highest = num
        num += 1

    return highest

if __name__ == "__main__":
    print("Multiprocessing:", multiprocessing_prime(180))
    print("Threading:", threaded_prime(180))
    print("Asynchronous:", asyncio.run(asynchronous_prime(180)))