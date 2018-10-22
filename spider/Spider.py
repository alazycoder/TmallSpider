import requests
from bs4 import BeautifulSoup
from selenium import webdriver
import time
import random
import traceback
from datetime import date
import uuid
import os
import re
import logging

from util.AgentPool import AgentPool
from util.MysqlManager import MysqlManager
from logger.MyLog import MyLog


class Spider:
    @MyLog
    def __init__(self, list_url, brand, class_):
        logging.info("%s %s %s" % (list_url, brand, class_))
        self.agent_pool = AgentPool()
        self.mysql_manager = MysqlManager()
        self.list_url = list_url
        self.all_item_url = set()
        self.max_try_times = 100
        self.item_page_time_out = 30
        self.image_time_out = 10
        self.brand = brand
        self.class_ = class_
        self.original_dir = r"E:\tmall\%s\%s\%s\original" % (str(date.today()), brand, class_)
        # self.picked_dir = r"E:\tmall\%s\%s\%s\picked" % (str(date.today()), brand, class_)
        self.item_page_image_pattern = re.compile("\/\/gw\.alicdn\.com\/bao\/uploaded\S+?jpg")
        self.item_page_label_pattern = re.compile("\"groupProps\":\[{\"基本信息\":(.+)}],\"propsList\"")

    def work(self):
        self.try_func(self.get_all_item_url)
        print(len(self.all_item_url))
        for item_url in self.all_item_url:
            if not self.mysql_manager.check_item_url_crawled(item_url):
                self.mysql_manager.add_one_record_to_history(item_url, self.brand, self.class_)
                all_image_url = self.try_func(self.get_all_image_url, item_url)
                # add one record into mysql
                uid = str(uuid.uuid1())
                save_dir = os.path.join(self.original_dir, uid)
                self.mysql_manager.add_path_to_item_url(item_url, save_dir)
                for image_url in all_image_url:
                    try:
                        self.save_image(image_url, save_dir)
                    except:
                        logging.error("image save failed %s" % image_url)
                self.mysql_manager.update_status_to_item_url(item_url)

    def get_driver(self):
        # 从这里得到的driver要执行quit函数
        opt = webdriver.ChromeOptions()
        agent = self.agent_pool.get_daxiang_agent()
        opt.add_argument("--proxy-server=http://%s" % agent)
        # opt.add_argument('--headless')
        logging.info("agent : %s" % agent)
        driver = webdriver.Chrome(options=opt)
        driver.set_page_load_timeout(30)
        driver.command_executor.set_timeout(30)
        return driver

    def try_func(self, func, *args):
        times = 0
        res = None
        while times < self.max_try_times:
            try:
                res = func(*args)
                if not res:
                    raise Exception
                else:
                    break
            except:
                times += 1
                traceback.print_exc()
                self.sleep(10, 15)
        if times >= self.max_try_times:
            logging.error("%s had failed %d times" % (func.__name__, times))
            exit(0)
        return res

    @MyLog
    def get_all_image_url(self, item_url):
        logging.info(item_url)
        res = set()
        agent = self.agent_pool.get_data5u_agent()
        logging.info(agent)
        proxies = {
            "http": agent,
            # "https": agent,
        }
        requests.session().keep_alive = False
        r = requests.get(item_url, proxies=proxies, timeout=self.item_page_time_out)
        r.raise_for_status()
        r.encoding = r.apparent_encoding
        soup = BeautifulSoup(r.text, "html.parser")

        # 位置1 展示框内的图片
        div = soup.find('div', {'class': 'scroller preview-scroller'})
        all_a = div.find_all('a')
        for a in all_a:
            img = a.find('img')
            res.add("https:" + img.attrs["data-src"])

        # 位置2  颜色挑选 按imgae url 长度排序， 最多选3个
        color_detail_imgs = self.item_page_image_pattern.findall(r.text)
        color_detail_imgs = sorted(color_detail_imgs, key=lambda s: len(s), reverse=True)
        for i in range(min(3, len(color_detail_imgs))):
            res.add("https:" + color_detail_imgs[i])

        # 获取label
        labels = self.item_page_label_pattern.findall(str(r.text))
        if len(labels) != 1:
            logging.error("len of labels in this page is not 1")
            raise Exception
        label = labels[0]
        # 存储label
        self.mysql_manager.add_label_to_item_url(item_url, label)
        # a = json.loads(label)
        logging.info("This item page has been successful. Let's celebrate! Cheers!")
        return res

    @MyLog
    def get_all_item_url(self):
        driver = self.get_driver()
        driver.get(self.list_url)
        scroll_down_times = 0
        # page_len = len(driver.page_source)
        page_source = ""
        while page_source.find(u"已经看到最后") == -1:
            page_source = driver.page_source
            soup = BeautifulSoup(driver.page_source, "html.parser")
            item_list = soup.find_all('a', {'class': 'tile_item'})
            if len(item_list) == 0:
                break
            for item in item_list:
                self.all_item_url.add("https:" + item.attrs["href"])
            driver.execute_script("window.scrollTo(0,document.body.scrollHeight)")
            self.sleep(1, 1.5)
            scroll_down_times += 1
            print(scroll_down_times)
            if scroll_down_times >= 100:
                break
            # new_page_len = len(driver.page_source)
            # logging.info("page len : %d(old) %d(new)" %(page_len, new_page_len))
            # if page_len == new_page_len:
            #     page_source = driver.page_source
            #     break
            # page_len = new_page_len
        driver.quit()
        logging.info("this page has %d items" % len(self.all_item_url))
        return page_source.find(u"已经看到最后") != -1
        # return len(self.all_item_url)

    @MyLog
    def save_image(self, url, save_dir):
        logging.info("image url: %s" % url)
        requests.session().keep_alive = False
        image = requests.get(url, timeout=self.image_time_out)
        image.raise_for_status()
        image_name = url.split('/')[-1]
        if not os.path.exists(save_dir):
            os.makedirs(save_dir)
        save_path = os.path.join(save_dir, image_name)
        with open(save_path, "wb") as f:
            f.write(image.content)

    def sleep(self, l, r):
        stop_time = random.uniform(l, r)
        time.sleep(stop_time)

# url = "https://handuyishe.m.tmall.com/shop/shop_auction_search.htm?spm=a1z60.7754813.0.0.54114ef5k4qAO6&sort=default&shop_cn=T%E6%81%A4&ascid=950888245&scid=950888245"
# spider = Spider(url, "handuyishe", "T恤")
# spider.work()
