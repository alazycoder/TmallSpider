import os
import shutil
import re
import json
import csv

from classification_network.pick import Picker
from util.MysqlManager import MysqlManager


class FeatureCombiner:
    def __init__(self, brand=None, class_=None):
        self.brand = brand
        self.class_ = class_


class Porter:
    def __init__(self, model_path=None):
        self.picker = None
        self.model_path = model_path
        self.sql_manager = MysqlManager()

    def file_collect(self, source, target):
        # 如果source是文件，则将source复制到target下
        # 如果source是目录，则递归的将source下的文件放到target下
        if os.path.isfile(source):
            _, file_name = os.path.split(source)
            if not os.path.exists(target):
                os.makedirs(target)
            shutil.copyfile(source, os.path.join(target, file_name))
        else:
            object_list = os.listdir(source)
            for obj in object_list:
                self.file_collect(os.path.join(source, obj), target)

    def file_picker(self, target_dir, feature_combiners, source=r"E:\tmall", labels=[]):
        # brand：待选择的品牌， class_: 待选择的衣服类别， labels：需要那些标签
        # target: 将选择好的图片放到target下的images目录下，labels生成csv文件放到

        if not os.path.exists(target_dir):
            os.makedirs(target_dir)

        images_target_dir = os.path.join(target_dir, "images")
        if not os.path.exists(images_target_dir):
            os.makedirs(images_target_dir)

        csv_path = os.path.join(target_dir, "label.csv")
        csv_writer = csv.writer(open(csv_path, "w"))

        data_dirs = os.listdir(source)
        data_dir_pattern = re.compile("\d\d\d\d-\d\d-\d\d")
        for data_dir in data_dirs:
            if data_dir_pattern.match(data_dir) is None:
                continue
            current_dir = os.path.join(source, data_dir)
            for fm in feature_combiners:
                selected_dir = os.path.join(current_dir, fm.brand, fm.class_, "original")
                if not os.path.exists(selected_dir):
                    continue
                uid_dirs = os.listdir(selected_dir)
                for uid_dir in uid_dirs:
                    final_dir = os.path.join(selected_dir, uid_dir)
                    print(final_dir)
                    files = os.listdir(final_dir)
                    # if "picked.jpg" not in files:
                    #     self.pick(final_dir)
                    picked_image_path = self.pick(final_dir)
                    new_image_name = final_dir.replace("\\", "_")  # 记录图片原来是哪的，便于debug
                    new_image_path = os.path.join(images_target_dir, new_image_name + ".jpg")
                    shutil.copyfile(picked_image_path, new_image_path)

                    picked_image_dir, _ = os.path.split(picked_image_path)  # 通过picked_image_dir去数据库中找标签
                    original_labels_record = self.sql_manager.get_labels_by_path(picked_image_dir)
                    print("*****:", original_labels_record)
                    csv_line = [new_image_path, ]
                    for key in labels:
                        value = self.pick_value_from_labels_record(key, original_labels_record)
                        print(value)
                        csv_line.append(value)
                    csv_writer.writerow(csv_line)

    def pick(self, target_dir):
        if self.picker is None:
            self.picker = Picker(self.model_path)
        return self.picker.pick(work_space=target_dir)

    def pick_value_from_labels_record(self, key, original_record):
        if original_record is None:
            return ""
        original_record = json.loads(original_record)
        for pair in original_record:
            for k, v in pair.items():
                if k == key:
                    return v
        return ""
