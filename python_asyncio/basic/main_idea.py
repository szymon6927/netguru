def run(coroutine):
    try:
        coroutine.send(None)
    except StopIteration as e:
        return e.value


async def hello(name):
    return f'Hello {name}'


async def test_await():
    names = ['Adam', 'Piotr', 'Dawid']

    for name in names:
        hello_str = await hello(name)
        print(hello_str)


if __name__ == '__main__':
    x = run(hello('Szymon'))
    print(x)
    y = run(hello('Adam'))
    print(y)

    run(test_await())
