import os
import shutil


class Porter:
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


Porter().file_collect(r"E:\tmall\2018-10-19", r"E:\tmall\temp")
