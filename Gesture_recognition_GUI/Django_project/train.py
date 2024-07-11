# -*- coding: utf-8 -*- #

# -----------------------------------------------------------------------
# File Name:    train.py
# Version:      ver1_0
# Created:      2024/06/17
# Description:  本文件定义了模型的训练流程
#               ★★★请在空白处填写适当的语句，将模型训练流程补充完整★★★
# -----------------------------------------------------------------------

import torch
from torch import nn
from torchvision.transforms import ToTensor
from torch.utils.data import DataLoader
from dataset import CustomDataset
from model import CustomNet


def train_loop(epoch, dataloader, model, loss_fn, optimizer, device):
    """定义训练流程。
    :param epoch: 定义训练的总轮次
    :param dataloader: 数据加载器
    :param model: 模型，需在model.py文件中定义好
    :param loss_fn: 损失函数
    :param optimizer: 优化器
    :param device: 训练设备，即使用哪一块CPU、GPU进行训练
    """
    # 将模型置为训练模式
    model.train()

    # START----------------------------------------------------------
    for i in range(epoch):
        total_loss = 0
        for batch_idx, (data, target) in enumerate(dataloader):
            # 将数据移到设备上
            data, target = data.to(device), target.to(device)
            # 梯度清零
            optimizer.zero_grad()
            # 前向传播
            output = model(data)
            # 计算损失
            loss = loss_fn(output, target)
            # 反向传播
            loss.backward()
            # 更新权重
            optimizer.step()
            # 打印训练信息
            total_loss += loss.item()
        ave_loss = total_loss/len(dataloader)
        print(f"Epoch {i + 1}/{epoch}, Loss: {ave_loss:.4f}")
    # END------------------------------------------------------------

    # 保存模型
    torch.save(model, './models/model.pkl')


if __name__ == "__main__":
    # 定义模型超参数
    BATCH_SIZE = 32
    LEARNING_RATE = 1e-3
    EPOCH = 1000

    # 模型实例化
    model = CustomNet()
    if torch.cuda.is_available():
        device = torch.device("cuda")
    else:
        device = torch.device("cpu")
    print("using {} device.".format(device))
    model.to(device)

    # 训练数据加载器
    train_dataloader = DataLoader(CustomDataset('./images/train.txt', './images/train', ToTensor),
                                  batch_size=BATCH_SIZE)
    # 损失函数
    loss_fn = nn.CrossEntropyLoss()
    # 学习率和优化器
    optimizer = torch.optim.SGD(model.parameters(), lr=LEARNING_RATE)
    # 调用训练方法
    train_loop(EPOCH, train_dataloader, model, loss_fn, optimizer, device)
