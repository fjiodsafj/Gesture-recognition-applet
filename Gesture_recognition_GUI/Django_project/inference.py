# -*- coding: utf-8 -*- #
import cv2
# -----------------------------------------------------------------------
# File Name:    inference.py
# Version:      ver1_0
# Created:      2024/06/17
# Description:  本文件定义了用于在模型应用端进行推理，返回模型输出的流程
#               ★★★请在空白处填写适当的语句，将模型推理应用流程补充完整★★★
# -----------------------------------------------------------------------

import torch
from torchvision.transforms import ToTensor
import matplotlib.pyplot as plt
from PIL import Image


def inference(image_path, model, device):
    """定义模型推理应用的流程。
    :param image_path: 输入图片的路径
    :param model: 训练好的模型
    :param device: 模型推理使用的设备，即使用哪一块CPU、GPU进行模型推理
    """
    # 将模型置为评估（测试）模式
    model.eval()
    image = Image.open(image_path)  # 打开图像文件
    # 图片预处理
    image = image.resize((64, 64), Image.LANCZOS)
    new_image = Image.new('RGB', (64, 64), (0, 0, 0))
    for channel in range(24):
        new_image.paste(image, (0, 0, 64, 64))

    # START----------------------------------------------------------

    plt.imshow(new_image)
    plt.axis('off')  # 关闭坐标轴
    plt.show()
    transform = ToTensor()  # 定义图像转换器
    image_tensor = transform(new_image).unsqueeze(0).to(device)  # 将图像转换为张量，并移动到设备上

    with torch.no_grad():
        output = model(image_tensor)  # 对图像进行推理
        _, predicted = torch.max(output, 1)  # 获取预测结果
        print(f"Predicted class index: {predicted.item()}")  # 打印预测类别索引
    # END------------------------------------------------------------


if __name__ == "__main__":
    # 指定图片路径
    image_path = "./images/test/signs/img_0063.png"
    #image_path = "test_image1.jpg"

    # 加载训练好的模型
    model = torch.load('./models/model.pkl')
    if torch.cuda.is_available():
        device = torch.device("cuda")
    else:
        device = torch.device("cpu")
    model.to(device)

    # 显示图片，输出预测结果
    inference(image_path, model, device)
