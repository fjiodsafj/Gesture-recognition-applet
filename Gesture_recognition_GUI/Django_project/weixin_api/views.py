from django.http import HttpResponse
from django.http import JsonResponse

from rest_framework.views import APIView
from rest_framework.response import Response
import base64

import torch.nn as nn
import torch
from PIL import Image
from torchvision import transforms
from torchvision.transforms import ToTensor

# Create your views here.
# 手势识别微信小程序
# cd Django_project # 进入Django_project目录
# python manage.py runserver # 启动django服务


device = torch.device('cuda')
transform = transforms.Compose([
    transforms.Resize(256),
    transforms.CenterCrop(224),
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.485, 0.456, 0.406],
                         std=[0.229, 0.224, 0.225])
])


def hello(request):
    model_path = 'models/model.pkl'  # 训练模型的相对路径
    image_path = 'test.jpg'  # 生成图片的相对路径
    model = torch.load(model_path)
    model.eval()
    model = model.to(device)

    if request.method == "POST":
        image_base64 = request.POST.get("image_base64", default='110')
        print(image_base64)
        if len(image_base64) % 2 != 0:
            image_base64 += "="
        with open('test.jpg', 'wb') as f:
            f.write(base64.b64decode(image_base64))
        f.close()
        torch.no_grad()  # 不计算梯度
        image = Image.open(image_path)  # 打开图像文件
        # 图片预处理
        image = image.resize((64, 64), Image.LANCZOS)
        new_image = Image.new('RGB', (64, 64), (0, 0, 0))
        for channel in range(24):
            new_image.paste(image, (0, 0, 64, 64))

        transform = ToTensor()  # 定义图像转换器
        image_tensor = transform(new_image).unsqueeze(0).to(device)  # 将图像转换为张量，并移动到设备上

        with torch.no_grad():
            output = model(image_tensor)  # 对图像进行推理
            _, predicted = torch.max(output, 1)  # 获取预测结果
            print(f"Predicted class index: {predicted.item()}")  # 打印预测类别索引
        print(predicted.item())
        print('load model ok')
        return HttpResponse(predicted.item())
