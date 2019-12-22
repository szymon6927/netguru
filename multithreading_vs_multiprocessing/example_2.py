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


def tracker(x):
    print(f'x={x}')
    test_list = []

    for _ in range(10**6):
        test_list.append(time.time())

    return test_list


def visualize_runtimes(results, title):
    for i, exp in enumerate(results):
        print(i)
        plt.scatter(exp, np.ones(len(exp)) * i, alpha=0.8, c='red', edgecolors='none', s=1)

    plt.grid(axis='x')
    plt.ylabel("Tasks")
    ytks = range(len(results))
    plt.yticks(ytks, ['job {}'.format(exp) for exp in ytks])
    plt.xlabel("Seconds")
    plt.title(title)


def main():
    plt.subplot(1, 2, 1)
    visualize_runtimes(multi_threading(tracker, range(4), 4), "Multithreading")

    plt.subplot(1, 2, 2)
    visualize_runtimes(multi_processing(tracker, range(4), 4), "Multiprocessing")

    plt.show()


if __name__ == '__main__':
    main()
