def run(coroutine):
    try:
        coroutine.send(None)
    except StopIteration as e:
        return e.value


async def fib(n):
    if n < 2:
        return 1

    return await fib(n - 1) + await fib(n - 2)


async def main():
    for i in range(10):
        print(await fib(i))

if __name__ == '__main__':
    run(main())
