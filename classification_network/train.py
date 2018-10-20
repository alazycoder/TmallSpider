import torch.optim as optim
from torch.autograd import Variable
import torch.nn as nn
import torch
from visdom import Visdom
import os
from datetime import date
from utils import train_data_loader, get_model

# visdom
viz = Visdom(env='tmall_classifier')

# data
my_data_loader = train_data_loader(r"E:\tmall\train_data")

# model
model = get_model()
model = model.cuda()

# loss
my_loss = nn.CrossEntropyLoss()

# optim
lr = 1e-3
optimizer = optim.Adam(model.parameters(), lr=lr)

# train
epochs = 6
today = str(date.today())
for epoch in range(epochs):
    win = None
    loss_sum = 0
    batch_num = 0
    for batch_index, (x, y) in enumerate(my_data_loader):
        optimizer.zero_grad()
        inputs = Variable(x.cuda())
        targets = Variable(y.cuda())
        outputs = model(inputs)
        loss = my_loss(outputs, targets)
        loss.backward()
        optimizer.step()
        # print('epoch: ' + str(epoch + 1) + ',batch: ' + str(batch_index + 1) + ',loss: ' + str(loss.item()))
        loss_sum = loss.item()
        batch_num += 1
        # 画loss曲线
        if win:
            win = viz.line(Y=torch.Tensor([loss.item()]), X=torch.Tensor([batch_index]), win=win, update='append')
        else:
            win = viz.line(Y=torch.Tensor([loss.item()]), X=torch.Tensor([batch_index]))
    print("epoch %d, loss %.4f" % (epoch, loss_sum/batch_num))
    # 保存model
    model_dir = "./models/%s" % today
    if not os.path.exists(model_dir):
        os.makedirs(model_dir)
    torch.save(model.state_dict(), os.path.join(model_dir, str(epoch)+".pkl"))
