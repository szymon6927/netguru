import requests
import time
from concurrent.futures import ThreadPoolExecutor


def multi_threading(func, args, workers):
    with ThreadPoolExecutor(workers) as ex:
        res = ex.map(func, args)

    return list(res)


def get_website_content(url):
    response = requests.get(url)

    if response.status_code == 200:
        return response.content

    return None


def main():
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

    n_jobs = len(url_list)

    marker = time.time()
    for url in url_list:
        get_website_content(url)

    print("Serial spent", time.time() - marker)

    for n_threads in [4, 8, 16]:
        marker = time.time()
        multi_threading(get_website_content, url_list, n_threads)
        print("Multithreading {} spent".format(n_threads), time.time() - marker)


if __name__ == '__main__':
    main()
