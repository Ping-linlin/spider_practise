from multiprocessing import Pool
from page_parsing import get_links_from


if __name__ == '__main__':
    pool = Pool()
    for num in range(1, 90):
        pool.apply_async(get_links_from(num))
