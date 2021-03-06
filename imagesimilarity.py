# -*- coding: utf-8 -*-
"""ImageSimilarity.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1xE1Qi-nznlqv7nfj_y6LIYtwiVkfRebi
"""

## GPU 설정

import torch

print(torch.cuda.is_available())
print(torch.cuda.device_count())

cuda = torch.device('cuda')

## 저작권이 이미 인정된 data

## data에 대해 다 device를 cuda로 설정
# a = torch.tensor([1.,2.]).cuda()

## 입력으로 들어온 data

## url -> image data

import cv2
#from google.colab.patches import cv2_imshow
import numpy as np
import urllib.request
from PIL import Image

def url_to_image(url):
  resp = urllib.request.urlretrieve(url, "image.png")
  #image = np.asarray(bytearray(resp.read()), dtype="uint8")
  #image = cv2.imdecode(image, cv2.IMREAD_COLOR)
  image = Image.open("image.png")

  return image

## example data
import torchvision
import torchvision.transforms as transforms

# 원래 Normalize는 R,G,B의 평균값으로 함
transform = transforms.Compose([
                                transforms.Resize((224,224)),
                                transforms.ToTensor(),
                                transforms.Normalize((0.5,0.5,0.5), (0.5,0.5,0.5))
])

'''
trainset = torchvision.datasets.ImageFolder(root = '이미지 파일이 들어있는 폴더의 상위경로', 
					transform = trans)
'''

img_url = "https://www.sjpost.co.kr/news/photo/202007/53199_48342_4214.jpg"
img = url_to_image(img_url)
img = transform(img)
img = img.cuda()

## VGG-16 model - image 특징 정보만 가져오기

import torchvision.models as models
import torch.nn as nn
from torchsummary import summary

vgg16 = models.vgg16(pretrained = True) # 사전에 훈련된 모델
New_vgg16 = nn.Sequential(*(list(vgg16.children())[0:1]))

New_vgg16 = New_vgg16.cuda()
New_vgg16

# example data result

result = New_vgg16(img.unsqueeze(0)) # img 3 x 224 x 224에서 하나의 dimension을 올려줌

# result의 size -> 1 x 512 x 7 x 7 
result = result.view(-1, 512 * 7* 7)

result = result.cpu()

result = result.detach().numpy()

result

def vgg16_array(img):
  result = New_vgg16(img.unsqueeze(0))
  result = result.view(-1, 512 * 7* 7)

  ## numpy array로 반환
  return result.cpu().detach().numpy().T

## Image Similarity 측정

def consine_sim(img1, img2):

  output1 = vgg16_array(img1)
  output2 = vgg16_array(img2)

  return dot(output1, output2) / (norm(output1)*norm(output2))



## 결과를 Server에



















