import asyncio
import aiohttp
import time

async def get_website_content(url):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            content = await response.read()
            return content


async def save_website_content(n, content):
    filepath = f'./data/async_{n}.html'

    with open(filepath, 'wb') as file:
        file.write(content)


async def task(n, url):
    content = await get_website_content(url)
    await save_website_content(n, content)


async def main():
    url_list = [
        "https://www.netguru.com/career/senior-product-design-consultant",
        "https://www.netguru.com/career/senior-sales-consultant-berlin",
        "https://www.netguru.com/career/senior-android-developer",
        "https://www.netguru.com/career/senior-ui-designer",
        "https://www.netguru.com/career/senior-data-engineer-0",
        "https://www.netguru.com/career/growth-hacker",
        "https://www.netguru.com/career/demand-generation-team-leader",
        "https://www.netguru.com/career/senior-ux-researcher",
        "https://www.netguru.com/career/account-manager"
    ]

    tasks = []

    for n, url in enumerate(url_list):
        tasks.append(task(n, url))

    await asyncio.wait(tasks)


if __name__ == '__main__':
    t1 = time.perf_counter()
    asyncio.run(main())
    t2 = time.perf_counter() - t1

    print(f'Total time: {t2}')

