import MySQLdb


class MysqlManager:
    def __init__(self):
        self.host = "localhost"
        self.port = 3306
        self.user = "root"
        self.password = "032610"
        self.database = "tmall"

    def fetch_all_source(self):
        db = MySQLdb.connect(host=self.host, port=self.port, user=self.user, password=self.password,
                             database=self.database, charset='utf8')
        cursor = db.cursor()
        sql = "select * from source"
        cursor.execute(sql)
        records = cursor.fetchall()
        db.close()
        res = []
        for record in records:
            res.append({"url": record[1], "brand": record[2], "class": record[3]})
        return res

    def add_one_record_to_history(self, item_url, brand, class_):
        db = MySQLdb.connect(host=self.host, port=self.port, user=self.user, password=self.password,
                             database=self.database, charset='utf8')
        cursor = db.cursor()
        sql = 'insert into `history` (`item_url`,`brand`,`class`) values(\"%s\", \"%s\", \"%s\")'% (item_url, brand, class_)
        try:
            # 执行sql语句
            cursor.execute(sql)
            # 提交到数据库执行
            db.commit()
        except:
            # Rollback in case there is any error
            db.rollback()

    def check_item_url_crawled(self, item_url):
        db = MySQLdb.connect(host=self.host, port=self.port, user=self.user, password=self.password,
                             database=self.database, charset='utf8')
        cursor = db.cursor()
        sql = "select status from `history` where item_url=\"%s\" " % item_url
        cursor.execute(sql)
        res = cursor.fetchall()
        db.close()
        if res:
            return res[0][0]
        return False

    def add_label_to_item_url(self, item_url, label):
        db = MySQLdb.connect(host=self.host, port=self.port, user=self.user, password=self.password,
                             database=self.database, charset='utf8')
        cursor = db.cursor()
        sql = 'update `history` set labels=\"%s\" where item_url=\"%s\"' % (label, item_url)
        try:
            # 执行sql语句
            cursor.execute(sql)
            # 提交到数据库执行
            db.commit()
        except:
            # Rollback in case there is any error
            db.rollback()

    def add_path_to_item_url(self, item_url, save_dir):
        db = MySQLdb.connect(host=self.host, port=self.port, user=self.user, password=self.password,
                             database=self.database, charset='utf8')
        cursor = db.cursor()
        sql = 'update `history` set path=\"%s\" where item_url=\"%s\"' % (save_dir, item_url)
        try:
            # 执行sql语句
            cursor.execute(sql)
            # 提交到数据库执行
            db.commit()
        except:
            # Rollback in case there is any error
            db.rollback()

    def update_status_to_item_url(self, item_url):
        db = MySQLdb.connect(host=self.host, port=self.port, user=self.user, password=self.password,
                             database=self.database, charset='utf8')
        cursor = db.cursor()
        sql = 'update `history` set status=1 where item_url=\"%s\"' % item_url
        try:
            # 执行sql语句
            cursor.execute(sql)
            # 提交到数据库执行
            db.commit()
        except:
            # Rollback in case there is any error
            db.rollback()