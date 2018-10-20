import os
import shutil
import re

from classification_network.pick import Picker


class FeatureCombiner:
    def __init__(self, brand=None, class_=None):
        self.brand = brand
        self.class_ = class_


class Porter:
    def __init__(self, model_path=None):
        self.picker = None
        self.model_path = model_path

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
                    picked_image = self.pick(final_dir)
                    image_name = final_dir.replace("\\", "_")
                    # print(picked_image)
                    shutil.copyfile(picked_image, os.path.join(images_target_dir, image_name + ".jpg"))
        # todo label

    def pick(self, target_dir):
        if self.picker is None:
            self.picker = Picker(self.model_path)
        return self.picker.pick(work_space=target_dir)

feature_combiners=[]
feature_combiners.append(FeatureCombiner(brand="handuyishe", class_=u"T恤"))
feature_combiners.append(FeatureCombiner(brand="hm", class_=u"衬衫"))

porter = Porter(model_path=r"D:\python_project\TmallSpider\classification_network\models\2018-10-21\4.pkl")
porter.file_picker(target_dir=r"E:\tamll_picked", feature_combiners=feature_combiners)
