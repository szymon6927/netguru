import time


def count():
    time.sleep(1)
    print('1')
    time.sleep(1)
    print('2')
    time.sleep(1)
    print('3')


def main():
    for i in range(3):
        count()


if __name__ == '__main__':
    start = time.perf_counter()
    main()
    stop = time.perf_counter()
    print(f'Total time: {stop - start}')

