import time
import multiprocessing
import threading
import asyncio
import sys

sys.set_int_max_str_digits(1000000)

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

def fibonacci(n):
    while n == 0:
        return 0
    a, b = 0, 1
    for num in range(2, n + 1):
        a, b = b, a + b
    return b

def factorial(n):
    fact = 1
    for num in range(2, n + 1):
        fact *= num
    return fact

def math_print(n):
    print(f"Now calculating fibonacci and factorial for prime: {n}")
    print(f"Printing first 15 digits of fibonacci({n}): {str(fibonacci(n))[:15]}")
    print(f"Printing first 15 digits of factorial({n}): {str(factorial(n))[:15]}")

#multiprocessing
def multiprocessing_search(start, step, max_time, result_list):
    result = prime_search(start, step, max_time)
    result_list.append(result)

def multiprocessing_prime(max_time=180):
    cores = multiprocessing.cpu_count()
    manager = multiprocessing.Manager()
    result_list = manager.list()
    processes = []
    print(f"Using multiprocessing to search for the largest prime number in {max_time} seconds")

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
    print(f"Using threading to search for the largest prime number in {max_time} seconds")

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
    print(f"Using asynchronous to search for the largest prime number in {max_time} seconds")

    while time.time() - start_time < max_time:
        result = await asyncio.to_thread(is_prime, num)
        if result:
            highest = num
        num += 1

    return highest

if __name__ == "__main__":
    multiprocessing_result = multiprocessing_prime(180)
    print(f"Multiprocessing: {multiprocessing_result}")
    math_print(multiprocessing_result)

    threaded_result = threaded_prime(180)
    print(f"Threading: {threaded_result}")
    math_print(threaded_result)

    asynchronous_result = asyncio.run(asynchronous_prime(180))
    print(f"Asynchronous: {asynchronous_result}")
    math_print(asynchronous_result)
