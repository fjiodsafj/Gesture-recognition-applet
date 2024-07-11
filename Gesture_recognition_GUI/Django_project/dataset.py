# -*- coding: utf-8 -*- #

# -----------------------------------------------------------------------
# File Name:    dataset.py
# Version:      ver1_0
# Created:      2024/06/17
# Description:  本文件定义了CustomDataset类，用于实现手势数据集的加载
# -----------------------------------------------------------------------

from torch.utils.data import Dataset
from torchvision.transforms import ToTensor, Lambda
from PIL import Image


class CustomDataset(Dataset):
    """自定义图像数据集类，用于对训练数据集进行操作。
    继承Dataset类，重写__init__、__len__、__getitem__三个方法，用于实现相关功能。
    """

    def __init__(self, annotations_file, img_dir, transform):
        # 按行读取数据标注文件，去掉结尾的\n，并根据空格分割为图片访问地址和类别标签
        with open(annotations_file, "r") as f:
            self.labels = [line.strip('\n').split(" ") for line in f.readlines()]
        self.img_dir = img_dir  # 训练样本所在的目录
        self.transform = transform()  # 需应用的图像变换方法
        self.target_transform = Lambda(lambda y: int(y))  # 标签转换方法

    def __len__(self):
        return len(self.labels)

    def __getitem__(self, idx):
        """使数据集可以使用下标索引，当调用本方法时，返回一个数据样本
        """
        image = Image.open(self.labels[idx][0])
        label = self.labels[idx][1]
        if self.transform:
            image = self.transform(image)
        if self.target_transform:
            label = self.target_transform(label)

        return image, label


if __name__ == "__main__":
    # 测试
    c = CustomDataset('./images/train.txt', './images/train', ToTensor)  # 实例化
    for label in c.labels:
        print(label)  # 打印所有训练数据的文件名及标注信息
    print(len(c))  # 打印数据集长度，测试__len__方法
    print(c[10])  # 测试__getitem__方法
