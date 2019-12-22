from concurrent.futures import ProcessPoolExecutor
from concurrent.futures import ThreadPoolExecutor

import matplotlib.pyplot as plt
import numpy as np
import time


def multi_threading(func, args, workers):
    with ThreadPoolExecutor(workers) as ex:
        res = ex.map(func, args)

    return list(res)


def multi_processing(func, args, workers):
    with ProcessPoolExecutor(workers) as ex:
        res = ex.map(func, args)

    return list(res)


def cpu_heavy_task(x):
    print(f'x={x}')

    start = time.time()

    count = 0
    for i in range(10**8):
        count += i

    stop = time.time()

    return start, stop


def visualize_runtimes(results, title):
    print("results: ", results)
    print("np.array: ", np.array(results).T)

    start, stop = np.array(results).T
    plt.barh(range(len(start)), stop - start)
    plt.grid(axis='x')
    plt.ylabel("Tasks")
    plt.xlabel("Seconds")
    plt.xlim(0, 22.5)
    ytks = range(len(results))
    plt.yticks(ytks, ['job {}'.format(exp) for exp in ytks])
    plt.title(title)
    return stop[-1] - start[0]


def main():
    plt.subplot(1, 2, 1)
    visualize_runtimes(multi_threading(cpu_heavy_task, range(4), 4), "Multithreading")

    plt.subplot(1, 2, 2)
    visualize_runtimes(multi_processing(cpu_heavy_task, range(4), 4), "Multiprocessing")

    plt.show()


if __name__ == '__main__':
    main()
