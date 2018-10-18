from MysqlManager import MysqlManager


mysql_manager = MysqlManager()
records = mysql_manager.fetchall()
for record in records:
    url = record.get("url")
    brand = record.get("brand")
    class_ = record.get("class")
    print(url, brand, class_)
