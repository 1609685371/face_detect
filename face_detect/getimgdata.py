import os
import re
import cv2
import numpy as np


class GetImgData:
    """
    将图片数据处理成ndarry数据
    """

    def __init__(self, dir='./small_img_gray'):
        self.dir = dir  # 该文件夹中有多个子文件夹，每个子文件夹名为一个人名，里面是这个人的多张人脸照片

    def onehot(self, numlist):
        """
        将输入的数字列表转为独热编码的形式
        :param numlist: 数字列表
        :return: 列表中数字的独热编码形式
        """
        b = np.zeros([len(numlist), max(numlist) + 1])  # 构建全零数组，行数为数字个数，列为数字最大值加一
        b[np.arange(len(numlist)), numlist] = 1  # 利用数组的索引方式进行赋值
        return b.tolist()

    def getimgnames(self, path=None):
        """
        获取指定文件夹中的JPG图片名称（含路径）
        :param path: 指定文件夹
        :return: path中的所有JPG图片名称（含路径，例如：./path/image1.jpg）
        """
        imgnames = []
        filenames = os.listdir(path)  # 获取path中的所有文件名
        for i in filenames:
            if re.findall('^\\d+\\.jpg$', i) != []:  # 在所有文件名中找出JPG图片名称
                imgnames.append(os.path.join(path, i))  # 将图片名称和路径合并、保存
        return imgnames

    def getfileandlabels(self):
        """
        获取self.dir中每个文件（人名）的独热编码及每个文件（人名）对应的标签（数字）
        :param self.dir: 指定路径，该路径中包含多个文件夹，每个文件夹为一个人的多张照片，文件名为人名
        :return: 返回两个值
        1. 文件名（人名）与其类别的独热编码，如：('./face_image_gray/hebo', [1.0, 0.0, 0.0, 0.0, 0.0, 0.0])
        2. 数字标签和文件名（人名）的对应关系，如：{0:'hebo', 1:'hexianbin'}
        """
        dir = self.dir
        dictdir = {name: os.path.join(dir, name) for name in os.listdir(dir) \
                   if os.path.isdir(os.path.join(dir, name))}  # 获取dir中的文件名和路径
        namelist, pathlist = dictdir.keys(), dictdir.values()  # namelist:文件名，pathlist:文件路径
        indexlist = list(range(len(namelist)))  # 将文件名转为数字标签
        return list(zip(pathlist, self.onehot(indexlist))), dict(zip(indexlist, namelist))

    def readimg(self):
        """
        读取dir中所有图片，将图片数据转为数组，并保存相应标签
        :param dir: 文件夹路径
        :return: 返回三部分的数据
        x: 图片像素数据
        y: 图片标签（0,1,2,3,4,5,...）
        number_name: 数字标签和人名的对应关系（字典）
        """
        imgs = []  # 图片像素数据
        labels = []  # 图片标签
        dir_labels, number_name = self.getfileandlabels()  # 获取文件名（人名）的独热编码和标签信息
        for dirname, label in dir_labels:  # 依次访问各文件名（人名）及对应的独热编码
            for imgname in self.getimgnames(dirname):  # 访问某文件名（人名）下的所有图片
                #img = cv2.imread(imgname)[:, :, 0:1]  # 读取图片(灰度图),并取其中一个通道的值，但请注意要保持其维度(三维)不变
                img = cv2.imdecode(np.fromfile(imgname, dtype=np.uint8), -1)
                img = cv2.cvtColor(img, cv2.COLOR_GRAY2RGB)[:, :, 0:1]
                imgs.append(img)  # 存贮图片像素数据
                labels.append(label)  # 存贮图片标签数据
        x = np.array(imgs, dtype='float32') / 255  # 将图片像素数据转为数组并归一化
        y = np.array(labels, dtype='float32')  # 将标签数据转为数组
        return x, y, number_name


if __name__ == '__main__':
    print('=========hello')
    myData = GetImgData()
    x, y, number_name = myData.readimg()
    print(x.shape,y.shape,number_name)
