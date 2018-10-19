from torch.utils.data import DataLoader
from torchvision.datasets import ImageFolder
import torchvision.models as models
import torch.nn as nn
from MyTransform import MyTransform

my_dataset = ImageFolder(r"E:\tmall\train_data", transform=MyTransform())
my_data_loader = DataLoader(dataset=my_dataset, batch_size=1, shuffle=True)

model = models.resnet101()
# 修改为二分类
model.fc = nn.Linear(2048, 2)


for x, y in my_data_loader:
    break