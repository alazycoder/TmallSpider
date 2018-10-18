import requests
from bs4 import BeautifulSoup
from selenium import webdriver
import time
import random
import traceback
from datetime import date
import uuid
import os

from AgentPool import AgentPool


class Spider:
    def __init__(self, list_url, brand, class_):
        self.agent_pool = AgentPool()
        self.list_url = list_url
        # self.all_item_url = set()
        self.all_item_url = set(["https://detail.m.tmall.com/item.htm?id=573760068252&pic=//img.alicdn.com/bao/uploaded/i2/2228361831/O1CN011POde8wb6Jlnau4_!!2228361831.jpg_Q50s50.jpg_.webp&itemTitle=ZARA%E5%A5%B3%E8%A3%85%20%E6%8B%BC%E5%B8%83%E5%AE%BD%E6%9D%BE%E8%A1%AC%E8%A1%AB%2004786256505&price=299.00&from=h5&sku_properties=1627207:28331",
                                 "https://detail.m.tmall.com/item.htm?id=578834890415&pic=//img.alicdn.com/bao/uploaded/i2/2228361831/O1CN011POdf5cPMmG3PwR_!!0-item_pic.jpg_Q50s50.jpg_.webp&itemTitle=ZARA%E6%96%B0%E6%AC%BE%20%E5%A5%B3%E8%A3%85%20%E5%BA%9C%E7%BB%B8%E6%8B%BC%E6%8E%A5%E4%B8%8A%E8%A1%A3%2001971175060&price=229.00&from=h5&sku_properties=1627207:420360311"])
        self.max_try_times = 5
        self.list_page_time_out = 300
        self.item_page_time_out = 30
        self.image_time_out = 10
        self.brand = brand
        self.class_ = class_
        self.original_dir = r"E:\tmall\%s\%s\%s\original" % (str(date.today()), brand, class_)
        self.picked_dir = r"E:\tmall\%s\%s\%s\picked" % (str(date.today()), brand, class_)

    def work(self):
        # self.try_func(self.get_all_item_url)
        for item_url in self.all_item_url:
            all_image_url = self.try_func(self.get_all_image_url, item_url)
            uid = str(uuid.uuid1())
            for image_url in all_image_url:
                self.save_image(image_url, uid)

    def get_driver(self):
        # 从这里得到的driver要执行quit函数
        opt = webdriver.ChromeOptions()
        agent = self.agent_pool.get_agent()
        opt.add_argument("--proxy-server=http://%s" % agent)
        print("agent :", agent)
        driver = webdriver.Chrome(options=opt)
        driver.set_page_load_timeout(self.list_page_time_out)
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
        return res

    def get_all_image_url(self, item_url):
        print(item_url)
        res = set()
        agent = self.agent_pool.get_agent()
        print(agent)
        proxies = {
            "http": agent,
            "https": agent,
        }
        r = requests.get(item_url, proxies=proxies, timeout=self.item_page_time_out)
        r.raise_for_status()
        r.encoding = r.apparent_encoding
        soup = BeautifulSoup(r.text, "html.parser")
        div = soup.find('div', {'class': 'scroller preview-scroller'})
        soup.prettify()
        all_a = div.find_all('a')
        for a in all_a:
            print(a)
            img = a.find('img')
            res.add("https:" + img.attrs["data-src"])
        return res

    def get_all_item_url(self):
        driver = self.get_driver()
        driver.get(self.list_url)
        page_len = len(driver.page_source)
        while True:
            soup = BeautifulSoup(driver.page_source, "html.parser")
            item_list = soup.find_all('a', {'class': 'tile_item'})
            print(len(item_list))
            for item in item_list:
                self.all_item_url.add("https:" + item.attrs["href"])

            driver.execute_script("window.scrollTo(0,document.body.scrollHeight)")
            self.sleep(1, 1.5)
            new_page_len = len(driver.page_source)
            print(page_len, new_page_len)
            if page_len == new_page_len:
                break
            page_len = new_page_len
        driver.quit()
        return len(self.all_item_url)

    def save_image(self, url, uid):
        image = requests.get(url, timeout=self.image_time_out)
        image_name = url.split('/')[-1]
        save_dir = os.path.join(self.original_dir, uid)
        if not os.path.exists(save_dir):
            os.makedirs(save_dir)
        save_path = os.path.join(save_dir, image_name)
        with open(save_path, "wb") as f:
            f.write(image.content)

    def sleep(self, l, r):
        stop_time = random.uniform(l, r)
        time.sleep(stop_time)


url = "https://handuyishe.m.tmall.com/shop/shop_auction_search.htm?spm=a1z60.7754813.0.0.54114ef5k4qAO6&sort=default&shop_cn=T%E6%81%A4&ascid=950888245&scid=950888245"
spider = Spider(url, "handuyishe", "T恤")
spider.work()
