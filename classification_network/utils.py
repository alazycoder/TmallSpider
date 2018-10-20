from torch.utils.data import DataLoader
from torchvision.datasets import ImageFolder
from torchvision import transforms
import torchvision.models as models
import torch.utils.data as data
import torch.nn as nn
import os
from PIL import Image


def get_transform():
    my_transform = transforms.Compose([transforms.Resize((224, 224)), transforms.ToTensor()])
    return my_transform


def train_data_loader(image_dir):
    # image_dir下有多个文件夹，每个文件夹代表一类
    my_transform = get_transform()
    my_dataset = ImageFolder(image_dir, transform=my_transform)
    my_data_loader = DataLoader(dataset=my_dataset, batch_size=64, shuffle=True)
    return my_data_loader


def pick_data_loader(root):
    dataset = PickDataSet(root)
    data_loader = data.DataLoader(dataset, batch_size=64)  # 因为待分类的文件夹都比较小，64保证能一次load完。
    return data_loader


def get_model():
    model = models.resnet101()
    model.fc = nn.Linear(2048, 2)
    return model


class PickDataSet(data.Dataset):
    def __init__(self, root):
        self.root = root
        self.image_files = os.listdir(root)
        self.transform = get_transform()

    def __len__(self):
        return len(self.image_files)

    def __getitem__(self, index):
        image_path = os.path.join(self.root, self.image_files[index])
        img = Image.open(image_path)
        img = img.convert('RGB')
        return self.transform(img), image_path