# example of using threads to do more work in parallel
# avoid managing Processes and stick to using Pools

import asyncio
import threading
import multiprocessing 
# from multiprocessing import Pool # !!!
from concurrent.futures import ThreadPoolExecutor

import time

def do_work():
    time.sleep(1)
    print("Done")

async def asyncio_solution():
    loop = asyncio.get_event_loop()
    tasks = []
    for i in range(10):
        tasks.append(loop.run_in_executor(None, do_work))
    await asyncio.wait(tasks)


def thread_solution():
    threads = []
    for i in range(10):
        t = threading.Thread(target=do_work)
        threads.append(t)
        t.start()
    for t in threads:
        t.join()


def thread_solution_2():
    with ThreadPoolExecutor(max_workers=10) as executor:
        executor.map(do_work, range(10))

    with multiprocessing.Pool.ThreadPool() as pool:
        results = pool.imap_unordered(do_work, range(10))


def process_solution():
    processes = []
    for i in range(10):
        p = multiprocessing.Process(target=do_work)
        processes.append(p)
        p.start()
    for p in processes:
        p.join()

if __name__ == "__main__":
    start_t = time.perf_counter()
    thread_solution()
    end_t = time.perf_counter()
    print("Time taken: {}".format(end_t - start_t))
