from MysqlManager import MysqlManager
from Spider import Spider

mysql_manager = MysqlManager()
records = mysql_manager.fetch_all_source()
for record in records:
    url = record.get("url")
    brand = record.get("brand")
    class_ = record.get("class")
    print(url, brand, class_)
    # spider = Spider(url, brand, class_)
    # spider.work()