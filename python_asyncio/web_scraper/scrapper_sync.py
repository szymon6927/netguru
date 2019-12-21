import time
import requests


def get_website_content(url):
    response = requests.get(url)

    if response.status_code != 200:
        return

    return response.content


def save_website_content(n, content):
    file_path = f'./data/sync_{n}.html'

    with open(file_path, 'wb') as file:
        file.write(content)


if __name__ == '__main__':
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

    t1 = time.perf_counter()

    for n, url in enumerate(url_list):
        content = get_website_content(url)
        save_website_content(n, content)

    t2 = time.perf_counter() - t1

    print(f'Total time: {t2}')
