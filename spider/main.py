from multiprocessing import Process
from spider.MysqlManager import MysqlManager
from Spider import Spider
import random
import logging

logging.basicConfig(level=logging.INFO)


# def crawl(url, brand, class_):
#     print(os.getpid(), url, brand, class_)
#     spider = Spider(url, brand, class_)
#     spider.work()


if __name__ == "__main__":
    records = MysqlManager().fetch_all_source()
    random.shuffle(records)
    for record in records:
        url = record.get("url")
        brand = record.get("brand")
        class_ = record.get("class")
        # p = Process(target=crawl, args=(url, brand, class_))
        # p.start()
        spider = Spider(url, brand, class_)
        spider.work()
