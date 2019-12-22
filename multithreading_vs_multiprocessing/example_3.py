import time
from concurrent.futures import ThreadPoolExecutor


def multi_threading(func, args, workers):
    with ThreadPoolExecutor(workers) as ex:
        res = ex.map(func, args)

    return list(res)


def cpu_heavy_task(x):
    print(f'x={x}')

    count = 0
    for i in range(10**8):
        count += i


def main():
    n_jobs = 4

    marker = time.time()
    for i in range(n_jobs):
        cpu_heavy_task(i)

    print("Serial time:", time.time() - marker)

    marker = time.time()
    multi_threading(cpu_heavy_task, range(n_jobs), 4)
    print("Multithreading time:", time.time() - marker)


if __name__ == '__main__':
    main()
