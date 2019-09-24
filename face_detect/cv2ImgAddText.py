# coding=utf-8
# cv2解决绘制中文乱码

import cv2
import numpy
from PIL import Image, ImageDraw, ImageFont


def cv2ImgAddText(img, text, left, top, textColor=(0, 0, 255), textSize=30):
    if (isinstance(img, numpy.ndarray)):  # 判断是否OpenCV图片类型
        img = Image.fromarray(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
    # 创建一个可以在给定图像上绘图的对象
    draw = ImageDraw.Draw(img)
    # 字体的格式
    fontStyle = ImageFont.truetype(
        "微软雅黑Bold.ttf", textSize, encoding="utf-8")
    # 绘制文本
    draw.text((left, top), text, textColor, font=fontStyle)
    # 转换回OpenCV格式
    return cv2.cvtColor(numpy.asarray(img), cv2.COLOR_RGB2BGR)


if __name__ == '__main__':
    img = cv2ImgAddText(cv2.imread('0.jpg'), "大家好，我是片天边的云彩", 10, 65, (0, 0, 139), 20)
    cv2.imshow('show', img)
    if cv2.waitKey(100000) & 0xFF == ord('q'):
        cv2.destroyAllWindows()   

