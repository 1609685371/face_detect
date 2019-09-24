# -*- coding: utf-8 -*-
# @File  : test_1.py
# @Author: CSD
# @Date  : 2019/9/20 0020 20:25
# @Software: PyCharm

# 1 数据采集、灰度处理
import captureface
from captureface import CaptureFace
import matplotlib.pyplot as plt
picture = CaptureFace(
    imgdir='./test_img/',  # 采集到的图片存放位置
    grayfacedir='./small_img_gray'  # 灰度处理后的图片存放位置
)
# 1.1 调用摄像头采集
picture.captureface(someone='chenshidong',
                    waitkey=100,  # (MS)
                    picturenum=100)
# 1.2 处理
picture.facetogray(someone='chenshidong', waitkey=100, size=64)

# 2 读取文件
from sklearn.model_selection import train_test_split
from getimgdata import GetImgData
path = './small_img_gray'  # 灰度图路径
imgs, labels, number_name = GetImgData(dir=path).readimg()
x_train, x_test, y_train, y_test = train_test_split(imgs, labels, test_size=0.2)

# 3 模型训练
from cnn_net import CnnNet
import numpy as np

# 3.1 创建类
cnnNet = CnnNet(modelfile='./temp/train-model',
                imgs=x_train, labels=y_train)
# 3.2 模型训练
cnnNet.cnnTrain(maxiter=1000,  # 最大迭代次数
                accu=0.9,)  # 指定正确率（499次之后）
# # 3.3 模型测试
# cnnNet2 = CnnNet(modelfile='./temp/train-model')
# pre, pro = cnnNet2.predict(test_x=x_test)
# # pre:预测结果
# # pro:概率矩阵
# acc_test = sum(np.argmax(y_test, axis=1) == pre)/len(pre)
# print(acc_test)
# # 4 调用摄像头测试
#
# import cv2
#
# size = 64  # 图片大小,与facetogray的size参数大小一致
# threshold = 0.98  # 阈值
# waitkey = 1  # 摄像头两次抓拍图像的时间间隔
# # 调用摄像头
# capture = cv2.VideoCapture(0)
# while True:
#     ret, img = capture.read()  # 按帧数读取视频的图片
#     k = cv2.waitKey(1)
#     if k == 27 & 0xff:
#         capture.release()
#         break
#     # 截取人脸
#     results = captureface.detect_face(img)  # 对图片进行人脸检测，即找到图片中人脸的位置
#     if results is not ():  # 判断图片中有无人脸
#         faceboxes = results  # 提取人脸位置信息
#         for (x, y, w, h) in faceboxes:
#             face = img[y:y+h, x:x+w]
#             # 灰度处理
#             face = cv2.cvtColor(face, cv2.COLOR_BGR2GRAY)
#             plt.imshow(face, cmap='gray')
#             # 图片大小处理
#             face = cv2.resize(face, (size, size))
#             # 图片格式处理
#             face = face.reshape([1, size, size, 1])
#             from cnn_net import CnnNet
#             cnnNet = CnnNet(modelfile='./temp/train-model')
#             res, pre = cnnNet.predict(test_x=face)
#             print(pre)
#             name = number_name[res[0]]
#             cv2.putText(img,  # 图片
#                         name,  # 文字
#                         (int(x), int(y-20)),  # 文字位置
#                         cv2.FONT_HERSHEY_SIMPLEX,  # 字体
#                         1,  # 字体大小
#                         (0, 255, 0),  # 颜色
#                         2)  # 字体粗细
#             cv2.rectangle(img,
#                           (int(x), int(y)),  # 左上角坐标
#                           (int(x+w), int(y+h)),  # 右下角坐标
#                           (255, 0, 0),  # 颜色
#                           3)  # 线宽
#             cv2.imshow('image', img)


