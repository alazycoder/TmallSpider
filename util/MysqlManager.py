import MySQLdb
import logging
from logger.MyLog import MyLog


class MysqlManager:
    def __init__(self):
        self.host = "localhost"
        self.port = 3306
        self.user = "root"
        self.password = "032610"
        self.database = "tmall"

    @MyLog
    def fetch_all_source(self):
        db = MySQLdb.connect(host=self.host, port=self.port, user=self.user, password=self.password,
                             database=self.database, charset='utf8')
        cursor = db.cursor()
        sql = "select * from source order by source_id desc"
        logging.info(sql)
        cursor.execute(sql)
        records = cursor.fetchall()
        db.close()
        res = []
        for record in records:
            res.append({"url": record[1], "brand": record[2], "class": record[3]})
        logging.info("result:")
        logging.info(res)
        return res

    @MyLog
    def add_one_record_to_history(self, item_url, brand, class_):
        db = MySQLdb.connect(host=self.host, port=self.port, user=self.user, password=self.password,
                             database=self.database, charset='utf8')
        cursor = db.cursor()
        sql = 'insert into `history` (`item_url`,`brand`,`class`) values(\"%s\", \"%s\", \"%s\")'% (item_url, brand, class_)
        logging.info(sql)
        try:
            cursor.execute(sql)
            db.commit()
            logging.info("success")
        except:
            db.rollback()
            logging.error("fail")

    @MyLog
    def check_item_url_crawled(self, item_url):
        db = MySQLdb.connect(host=self.host, port=self.port, user=self.user, password=self.password,
                             database=self.database, charset='utf8')
        cursor = db.cursor()
        sql = "select status from `history` where item_url=\"%s\" " % item_url
        logging.info(sql)
        cursor.execute(sql)
        res = cursor.fetchall()
        db.close()
        if res:
            logging.info("return %s" % str(res[0][0]))
            return res[0][0]
        else:
            logging.info("return 0")
            return False

    @MyLog
    def add_label_to_item_url(self, item_url, label):
        label = label.replace("\"", "\\\"")
        label = label.replace("\t", "")
        label = label.replace("\n", "")
        db = MySQLdb.connect(host=self.host, port=self.port, user=self.user, password=self.password,
                             database=self.database, charset='utf8')
        cursor = db.cursor()
        sql = 'update `history` set labels=\"%s\" where item_url=\"%s\"' % (label, item_url)
        logging.info(sql)
        try:
            cursor.execute(sql)
            db.commit()
            logging.info("success")
        except:
            db.rollback()
            logging.error("fail")

    @MyLog
    def add_path_to_item_url(self, item_url, save_dir):
        db = MySQLdb.connect(host=self.host, port=self.port, user=self.user, password=self.password,
                             database=self.database, charset='utf8')
        cursor = db.cursor()
        sql = 'update `history` set path=\"%s\" where item_url=\"%s\"' % (save_dir, item_url)
        logging.info(sql)
        try:
            cursor.execute(sql)
            db.commit()
            logging.info("success")
        except:
            db.rollback()
            logging.error("fail")

    @MyLog
    def update_status_to_item_url(self, item_url):
        db = MySQLdb.connect(host=self.host, port=self.port, user=self.user, password=self.password,
                             database=self.database, charset='utf8')
        cursor = db.cursor()
        sql = 'update `history` set status=1 where item_url=\"%s\"' % item_url
        logging.info(sql)
        try:
            cursor.execute(sql)
            db.commit()
            logging.info("success")
        except:
            # Rollback in case there is any error
            db.rollback()
            logging.error("fail")

    @MyLog
    def get_labels_by_path(self, path):
        db = MySQLdb.connect(host=self.host, port=self.port, user=self.user, password=self.password,
                             database=self.database, charset='utf8')
        cursor = db.cursor()
        sql = "select labels from history where path=\"%s\" " % path
        logging.info(sql)
        cursor.execute(sql)
        records = cursor.fetchall()
        db.close()
        if len(records) > 0 and len(records[0]) > 0:
            label = records[0][0]
            label = label.replace("\t", "")
            label = label.replace("\n", "")
            return label
        else:
            return None