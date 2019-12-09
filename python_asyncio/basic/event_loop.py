import asyncio

async def hello(name):
    return f'Hello {name}'


async def main():
    names = ['Piotr', 'Dawid', 'Wojtek']

    for name in names:
        hello_str = await hello(name)
        print(hello_str)


loop = asyncio.get_event_loop()
try:
    loop.run_until_complete(main())
finally:
    loop.close()
