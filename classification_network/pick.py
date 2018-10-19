from torch.autograd import Variable
import torch
from utils import pick_data_loader, get_model


class Picker:
    def __init__(self, model_path):
        #load model
        self.model = get_model()
        self.model.load_state_dict(torch.load(model_path))
        self.model = self.model.cuda()
        self.data_loader = pick_data_loader("test")

    def pick(self, work_space):
        data_loader = pick_data_loader(work_space)
        for img in data_loader:
            print(img.size())
            img = Variable(img.cuda())
            res = self.model(img)
            print(res.size())
            print(res)





