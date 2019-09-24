import os
import cv2
import numpy as np

from getimgdata import GetImgData

getdata = GetImgData()  # 图片获取类

"""
此脚本用于某个人的图片采集和图片中人脸检测及灰度处理
1.captureface：通过电脑摄像头实时拍照，并按类别进行存储
2.facetogray：把获取的图片中的人脸检测裁剪出来，并做灰度处理后分类存储
"""


def detect_face(img):
    clf = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
    # 找到符合xml文件里描述的特征区域
    objects = clf.detectMultiScale(img)
    return objects


class CaptureFace:
    def __init__(self, imgdir='./test_img/', grayfacedir='./test_img_gray'):
        """
        :param imgdir: 采集到的图片的存放路径
        :param grayfacedir: 处理后的图片（人脸灰度图）的存放路径
        """
        self.imgdir = imgdir
        self.grayfacedir = grayfacedir

    def facetogray(self, someone='', size=64, waitkey=100):
        """
        将指定文件夹中的所有图片转为灰度图，并保存至指定位置
        :param someone: 某人姓名，即要处理的图片文件夹
        :param size: 将图片压缩的纬度大小
        :param waitkey: 延迟时长（ms）
        :return: 处理后的灰度图
        """
        imgnames = getdata.getimgnames(path=os.path.join(self.imgdir, someone))  # 获取指定文件夹中的所有jpg图片名称
        n = len(imgnames)  # 图片张数
        newpath = os.path.join(self.grayfacedir, someone)  # 处理后的灰度图的存放路径
        if not os.path.exists(newpath):  # 看是否需要创建路径
            os.makedirs(newpath)
        for i in range(n):  # 开始对每张图片进行灰度处理
            # img = cv2.imread(imgnames[i])  # 读入图片 无法读取中文路径
            img = cv2.imdecode(np.fromfile(imgnames[i], dtype=np.uint8), -1)
            results = detect_face(img)  # 对图片进行人脸检测，即找到图片中人脸的位置
            if results is not ():  # 判断图片中有无人脸
                faceboxes = results  # 提取人脸位置信息
                for (x, y, w, h) in faceboxes:
                    face = img[y:y + h, x:x + w]  # 截取图片中的人脸图像
                    face_gray = cv2.cvtColor(face, cv2.COLOR_BGR2GRAY)  # 转为灰度图片
                    face_gray = cv2.resize(face_gray, (size, size))  # 压缩成指定大小
                    # cv2.imwrite(newpath + '/' + str(i) + '.jpg', face_gray)  # 保存检测出的人脸图片 无法读取中文路径
                    savePath = (newpath + "/%d.jpg" % i)
                    cv2.imencode('.jpg', face_gray)[1].tofile(savePath)
            else:
                print('未检测到人脸')
