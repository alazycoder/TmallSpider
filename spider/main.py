from multiprocessing import Process

from spider.MysqlManager import MysqlManager


def crawl(url, brand, class_):
    # spider = Spider(url, brand, class_)
    # spider.work()
    pass

if __name__ == "__main__":
    records = MysqlManager().fetch_all_source()
    for record in records:
        url = record.get("url")
        brand = record.get("brand")
        class_ = record.get("class")
        # print(url, brand, class_)
        p = Process(target=crawl, args=(url, brand, class_))
        p.start()
        p.join()
