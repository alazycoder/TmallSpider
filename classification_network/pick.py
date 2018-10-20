from torch.autograd import Variable
import torch
from utils import pick_data_loader, get_model
import os


class Picker:
    def __init__(self, model_path):
        #load model
        self.model = get_model()
        self.model.load_state_dict(torch.load(model_path))
        self.model = self.model.cuda()

    def pick(self, work_space):
        data_loader = pick_data_loader(work_space)
        # data_loader 确保batch_size 足够大，一次load完所有的图片
        for imgs, files_path in data_loader:
            imgs = Variable(imgs.cuda())
            res = self.model(imgs)
            positive_score = res[:, 1]
            # file_num = res.size(0)
            # for i in range(file_num):
            #     _, file_name = os.path.split(files_path[i])
            #     print(file_name, positive_score[i].item())
            max_score, index = torch.max(positive_score, 0)
            print(max_score)
            # print(index, files_path[index])
            return files_path[index]



