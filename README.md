## 前言

一个基于opencv人脸识别和TensorFlow进行模型训练的人脸实时签到系统，作者某二本大学里的末流学生，写于2019/09/，python学习期间。
今年7月份开始接触python的，最近闲着无事就开始做了这个人脸识别的系统，一开始的话就想着简单的弄下，就去了[百度智能云](https://console.bce.baidu.com/)用的api接口实现的，写完以后我就想为什么我不自己写一个人脸识别签到，不去调用百度api接口，然后就诞生了这个程序。

## 先看下效果
![在这里插入图片描述](https://img-blog.csdnimg.cn/20190924192838913.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3UwMTEzMjUyMTM=,size_16,color_FFFFFF,t_70)
## 实现的功能

 - 点击开始进行实时人脸打开识别签到![在这里插入图片描述](https://img-blog.csdnimg.cn/20190924194026776.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3UwMTEzMjUyMTM=,size_16,color_FFFFFF,t_70)
 - 点击注册会跳到注册页面进行注册![在这里插入图片描述](https://img-blog.csdnimg.cn/20190924194041906.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3UwMTEzMjUyMTM=,size_16,color_FFFFFF,t_70)
 - 点击缺勤会打开缺勤窗口显示缺勤的表格![在这里插入图片描述](https://img-blog.csdnimg.cn/20190924194203588.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3UwMTEzMjUyMTM=,size_16,color_FFFFFF,t_70)
## 开始准备
选用语言Python，时下入门机器学习成本最低、学习速度最快的语言，python搞网络爬虫也很靠谱。运用的技术有 opencv（摄像头、图片处理），numpy（图片数字化），os（文件的操作和处理），TensorFlow（构建神经网络进行模型训练）。
## 页面的构建
我的UI页面是用pyqt写的，pyqt这块也不是很熟练，就稍微看了看教程，问了问同学，摸索着开始使用了，关于pyqt这块的话，不和大家多说了，大家可以看下这个链接[pyqt5、qtdesigner安装和环境设置](https://blog.csdn.net/weixin_43008870/article/details/85766035)，我的这个程序也是亏了博主的这篇博客，大爱![在这里插入图片描述](https://img-blog.csdnimg.cn/2019092419533616.png)
##  功能实现
这里我就长话短说，因为涉及的东西比较多，我就按照我的目录中的文件开始讲起![在这里插入图片描述](https://img-blog.csdnimg.cn/20190924200121378.png)
 - icon这个文件夹主要是存放UI页面的图标
 - small_img_gray文件夹是用来存放注册时转换的灰度图，就是你在注册的时候点击拍照以后，程序会在一段时间内拍下100张照片进行保存，然后再将保存的照片转换为灰度图进行往后的模型训练。
 - temp文件夹用来保存训练的模型
 - test_img用来保存注册时拍下的100张照片，对了忘了说，test_img文件夹和small_img_gray文件夹下都是以人名为命名的文件夹，每个人名文件夹下保存着100张照片![在这里插入图片描述](https://img-blog.csdnimg.cn/20190924200611303.png)
 - captureface.py这个文件功能是
1.用于某个人的图片采集和图片中人脸检测及灰度处理
2.通过电脑摄像头实时拍照，并按类别进行存储
3.把获取的图片中的人脸检测裁剪出来，并做灰度处理后分类存储，这里用到了后边的getimgdata.py文件
 - cnn_net.py是用来构建cnn神经网络结构，以及模型训练和模型预测
 - cv2ImgAddText.py，关于这个文件，大家前边看到的我人脸上边有个方框和人名是吧，但是在做这一步的时候我发现，opencv自带的puttext方法不能输出中文，只能输出英文，很生气，中国汉字文化博大精深~源远流长 为什么不能输出汉字？？但是咱也不能怪人家开发人员可能人家没考虑的，所以这个文件就是将汉字进行输出的
 - db.py用来建立连接数据库的对象
 - face_register.py文件向数据库进行插入用户数据
 - face_search.py文件是在进行签到时更新数据库中用户的状态，是签到了还是迟到了
 - getimgdata.py文件包含4个方法，主要功能就是将用户的照片进行分类存储
 - haarcascade_frontalface_default.xml文件是级联分类器文件，是opencv进行人脸识别的文件，具体还有[其他的分类器](https://github.com/opencv/opencv/tree/master/data/haarcascades)，像识别眼睛嘴巴还有微笑什么的
 - late.py和late.ui这两个文件我拿一起说，主要是因为late.py是由late.ui文件进行编译得到的，当你看完上边页面部分的构建你就会明白了，后边的Mainwindow.py和Mainwindow.ui以及register.py和register.ui同理，都是页面的代码文件
 - 微软雅黑Bold.ttf就是人脸识别的时候方框上边的名字字体，默认的我嫌它的字体比较细，所以网上找了个加粗的，大家也可以用别的字体，这个无所谓
 - 最后就是main.py这个文件了，基本上所有的执行代码就在这了，这里呢用到了pyqt的多线程QThread以及python的多线程threading，这俩稍微有点那么区别，但基本上实现都是相通的，为什么会用到多线程呢？这是因为在一开始进行注册拍照和模型训练的时候，我发现如果不启用多线程，前端的ui页面就会未响应，当模型训练完成以后才恢复正常，这样给用户带来的体验是极差的，所以尽量将ui展示页面和功能实现的代码分开，在显示页面的同时还能进行后台的运算。（~不知道这样说对不对，说错的还请大家指出来，小白虚心学习~）
## 代码部分
这里就放main.py文件的吧，其他的放了估计也太多![在这里插入图片描述](https://img-blog.csdnimg.cn/20190924203953898.gif)

```
# -*- coding: utf-8 -*-
# @File  : main.py
# @Author: CSD
# @Date  : 2019/9/7 0007 20:48
# @Software: PyCharm
import gc
import os
import sys
import time
import cv2
import qimage2ndarray
from PyQt5.QtCore import QTimer, Qt, QThread, pyqtSignal
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QApplication, QMainWindow, QDialog, QAbstractItemView, QTableWidgetItem, QMessageBox
from Mainwindow import Ui_MainWindow
from db import mysql_conn
from face_register import register_handler
from face_search import search_handler
from late import Ui_Table
from register import Ui_Register
from cnn_net import CnnNet
from sklearn.model_selection import train_test_split
import numpy as np
from getimgdata import GetImgData
import captureface
from captureface import CaptureFace
import threading
from cv2ImgAddText import cv2ImgAddText
imgs, labels, number_name = GetImgData().readimg()  # 读取数据
train_x, test_x, train_y, test_y = train_test_split(imgs, labels, test_size=0.1, random_state=10)  # 训练集测试集数据划分
cnnnet = CnnNet()  # 调用CNN算法类


# 主窗口
class parentWindow(QMainWindow, Ui_MainWindow):

    def __del__(self):
        try:
            self.camera.release()  # 释放资源
        except:
            return

    def __init__(self, parent=None):
        super(parentWindow, self).__init__(parent)
        self.setupUi(self)
        self.Latebt.setEnabled(False)
        # self.PrepCamera()
        self.CallBackFunctions()
        self.Timer = QTimer()  # 实例化一个类
        self.Timer.timeout.connect(self.TimerOutFun)  # 定时刷新
        self.flagThread = FlagThread()
        # 当获得循环完毕的信号时，停止计数
        self.flagThread.trigger.connect(self.fun_timer)

    # 初始化摄像头
    def PrepCamera(self):
        try:
            self.camera = cv2.VideoCapture(0)
            self.camera.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc('M', 'J', 'P', 'G'))
            self.MsgTE.clear()
            self.MsgTE.append('摄像头已连接！')
        except Exception as e:
            self.MsgTE.clear()
            self.MsgTE.append(str(e))

    # 回调函数
    def CallBackFunctions(self):
        self.Showbt.clicked.connect(self.StartCamera)
        self.About.clicked.connect(self.about)

    # 开始按钮函数
    def StartCamera(self):
        self.Showbt.setEnabled(False)
        self.Loginbt.setEnabled(False)
        self.Latebt.setEnabled(True)
        self.PrepCamera()
        self.Timer.start(1)  # 每隔1ms刷新一次
        self.timelb = time.clock()
        self.flagThread.start()

    # 从摄像头读取图像
    def TimerOutFun(self):
        success, img = self.camera.read()
        if success:
            self.Image = img
            self.DispImg()
        else:
            self.MsgTE.clear()
            self.MsgTE.setPlainText('摄像头读取图像已暂停！')

    def fun_timer(self, flag):
        self.MsgTE.setPlainText(flag)

    # 检测人脸、色彩空间及格式转换
    def DispImg(self):
        results = captureface.detect_face(self.Image)
        if results is not ():
            faceboxes = results  # 提取人脸位置信息
            for (x, y, w, h) in faceboxes:
                face = self.Image[y:y + h, x:x + w]  # 截取图片中的人脸图像
                face = cv2.cvtColor(face, cv2.COLOR_BGR2GRAY)  # 转为灰度图片
                face = cv2.resize(face, (64, 64))  # 压缩成指定大小
                face = face.reshape([1, 64, 64, 1])
                cnnNet = CnnNet(modelfile='./temp/train-model')  # 注意这步很关键，起到了重置计算图的作用，否则多次导入训练好的计算图会出现tensor重复的问题
                res, pre = cnnNet.predict(test_x=face)  # 调用已训练好的模型进行预测
                if np.max(pre) < 0.8:  # 通过调整阈值为threshold，当返回数组最大值小于threshold是即视为unknown
                    self.name = "unknown"
                else:
                    self.name = number_name[res[0]]
                    self.flagThread.get_name(self.name)

                # cv2.putText(self.Image, self.name, (int(x), int(y) - 20), cv2.FONT_HERSHEY_SIMPLEX, 1, 255, 2)
                cv2.rectangle(self.Image, (int(x), int(y)), (int(x + w), int(y + h)), (255, 0, 0), 3)  # 将name显示出来
                img = cv2ImgAddText(self.Image, self.name, int(x+25), int(y-50))
                img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
                qimg = qimage2ndarray.array2qimage(img)  # 调用array2qimage函数将其转为QImage格式
                self.DispLb.setPixmap(QPixmap(qimg))  # 再通过QPixmap函数转为QPixmap格式进行显示。
                self.DispLb.show()  # 图像显示
                gc.collect()

        else:
            img = cv2.cvtColor(self.Image, cv2.COLOR_BGR2RGB)
            qimg = qimage2ndarray.array2qimage(img)  # 调用array2qimage函数将其转为QImage格式
            self.DispLb.setPixmap(QPixmap(qimg))  # 再通过QPixmap函数转为QPixmap格式进行显示。
            self.DispLb.show()  # 图像显示

    # 帮助
    def about(self):
        reply = QMessageBox.information(self,
                                        "关于",
                                        "1.点击开始按钮播放视频流,进行签到\n"
                                        "2.点击注册按钮可跳往注册窗口进行注册\n"
                                        "3.点击缺勤按钮可查看缺勤学生名单，状态0代表缺勤\n"
                                        "4.点击帮助按钮可查看帮助，同时关闭主窗口视频流,进行人脸注册",
                                        QMessageBox.Close)

        try:
            self.camera.release()  # 释放资源
            self.Showbt.setEnabled(True)
            self.Loginbt.setEnabled(True)
        except:
            return


# 注册窗口
class childWindow(QDialog, Ui_Register):

    def __init__(self, parent=None):
        super(childWindow, self).__init__(parent)
        self.setupUi(self)
        self.PhotoBt.setEnabled(False)
        self.RegisterBt.setEnabled(False)
        # self.PrepCamera()
        self.CallBackFunctions()
        self.workThread = WorkThread()
        self.photoThread = PhotoThread()
        # 当获得循环完毕的信号时，停止计数
        self.workThread.trigger.connect(self.timeStop)
        self.photoThread.trigger.connect(self.runover)
        self.Timer = QTimer()  # 实例化一个类
        self.Timer.timeout.connect(self.TimerOutFun)  # 定时刷新

    # 初始化摄像头并打开
    def PrepCamera(self):
        try:
            self.camera = cv2.VideoCapture(0)
            self.MsgLb.clear()
            self.MsgLb.setText('请输入学号、姓名,点击拍照!')
        except Exception as e:
            self.MsgLb.clear()
            self.MsgLb.setText(str(e))

    # 回调函数
    def CallBackFunctions(self):
        self.PhotoBt.clicked.connect(self.PhotoCamera)
        self.StartBt.clicked.connect(self.StartCamera)
        self.RegisterBt.clicked.connect(self.RegisterCamera)
        self.ModelBt.clicked.connect(self.ModelTrain)

    # 开始按钮函数
    def StartCamera(self):
        self.PhotoBt.setEnabled(True)
        self.RegisterBt.setEnabled(True)
        self.PrepCamera()
        self.Timer.start(1)  # 每隔1ms刷新一次
        self.timelb = time.clock()

    # 注册
    def RegisterCamera(self):
        Msg = register_handler(self.stu_id.text(), self.stu_name.text())
        self.MsgLb.setText(Msg)

    # 拍照按钮函数
    def PhotoCamera(self):
        if self.stu_id.text().isdigit():
            self.RecordCamera()  # 保存照片
            self.stu_id.clear()
            self.stu_name.clear()
        else:
            self.MsgLb.setText('请检查学号是否正确')

    # 从摄像头读取图像
    def TimerOutFun(self):
        success, img = self.camera.read()
        if success:
            self.Image = img
            self.DispImg()
        else:
            self.MsgLb.clear()
            self.MsgLb.setText('摄像头读取图像已暂停！')

    # 色彩空间及格式转换
    def DispImg(self):
        img = cv2.cvtColor(self.Image, cv2.COLOR_BGR2RGB)
        qimg = qimage2ndarray.array2qimage(img)  # 调用array2qimage函数将其转为QImage格式
        self.ShowLb.setPixmap(QPixmap(qimg))  # 再通过QPixmap函数转为QPixmap格式进行显示。
        self.ShowLb.show()  # 图像显示

    # 采集照片
    def RecordCamera(self):
        self.MsgLb.setText('正在采集图片')
        self.photoThread.img(self.Image, self.stu_name.text())
        self.photoThread.start()

    def runover(self, msg, i):
        self.MsgLb.setText(msg)
        self.progressBar.setValue(i)

    # 模型训练
    def ModelTrain(self):
        self.MsgLb.setText('请等待一段时间进行模型训练!')
        self.workThread.start()

    def timeStop(self, msg, i):
        self.MsgLb.setText(msg)
        self.progressBar.setValue(i)

    def closeEvent(self, event):
        self.camera.release()


# 缺勤窗口
class childWindow_late(QDialog, Ui_Table):
    def __init__(self, parent=None):
        super(childWindow_late, self).__init__(parent)
        self.setupUi(self)
        self.CallBackFunctions()
        self.tableWidget.setEditTriggers(QAbstractItemView.NoEditTriggers)

    # 回调函数
    def CallBackFunctions(self):
        self.ResetBt.clicked.connect(self.ResetTable)
        self.ShowBt.clicked.connect(self.ShowTable)

    # 显示缺勤表格
    def ShowTable(self):
        sql = 'select * from users where state=0'
        print(sql)
        cursor = mysql_conn.cursor()
        cursor.execute(sql)
        results = cursor.fetchall()
        print(results)
        if results:
            row = cursor.rowcount
            vol = len(results[0])
            self.tableWidget.setRowCount(row)
            self.tableWidget.setColumnCount(3)
            for i in range(row):
                for j in range(3):
                    temp_data = results[i][j + 1]  # 临时记录，不能直接插入表格
                    print(temp_data)
                    data = QTableWidgetItem(str(temp_data))  # 转换后可插入表格
                    data.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
                    self.tableWidget.setItem(i, j, data)

    # 重置
    def ResetTable(self):
        reply = QMessageBox.question(self,
                                     "消息",
                                     "重置后所有的学生的状态将更改为0，是否修改？",
                                     QMessageBox.Yes | QMessageBox.No)
        if reply == QMessageBox.Yes:
            sql = 'update  users set state = 0'
            print(sql)
            cursor = mysql_conn.cursor()
            cursor.execute(sql)
            mysql_conn.commit()
        else:
            return


class WorkThread(QThread):
    trigger = pyqtSignal(str, int)

    def __int__(self):
        super(WorkThread, self).__init__()

    def run(self):
        time.sleep(2)
        path = './small_img_gray'  # 灰度图路径
        imgs, labels, number_name = GetImgData(dir=path).readimg()
        x_train, x_test, y_train, y_test = train_test_split(imgs, labels, test_size=0.2)

        cnnNet = CnnNet(modelfile='./temp/train-model',
                        imgs=x_train, labels=y_train)

        train_class = cnnNet.cnnTrain(maxiter=1000,  # 最大迭代次数
                                      accu=0.99, )  # 指定正确率（499次之后）
        for index, out in enumerate(train_class):
            # 循环完毕后发出信号
            self.trigger.emit(out, index * 10)
        self.trigger.emit("训练完成", 100)

    def kill_thread(self):
        self.terminate()


class PhotoThread(QThread, Ui_Register):
    trigger = pyqtSignal(str, int)

    def __int__(self):
        super(PhotoThread, self).__init__()

    def img(self, img, stu_name):
        self.Image = img
        self.stu_name = stu_name

    def run(self):
        filepath = os.path.join('./test_img/', self.stu_name)  # 路径拼接
        if not os.path.exists(filepath):  # 看是否需要创建路径
            os.makedirs(filepath)
        for i in range(100):  # 开始拍照
            savePath = (filepath + "/%d.jpg" % i)
            cv2.imencode('.jpg', self.Image, [cv2.IMWRITE_JPEG_QUALITY, 100])[1].tofile(savePath)  # 保存图片
            # 无法写入中文 搜了搜发现OpenCV的imwrite不支持 所以换成了cv2.imencode
            # picturepath = os.path.join(filepath, str(i)) + '.jpg'  # 图片的完整路径名  无法读取中文路径
            # cv2.imwrite(picturepath, self.Image, [cv2.IMWRITE_JPEG_QUALITY, 100])  # 将图片写入指定d路径
            self.trigger.emit('正在采集图片~', i)
        picture = CaptureFace(
            imgdir='./test_img/',  # 采集到的图片存放位置
            grayfacedir='./small_img_gray'  # 灰度处理后的图片存放位置
        )
        picture.facetogray(someone=self.stu_name, waitkey=100, size=64)
        self.trigger.emit('图片采集完毕！点击注册', 100)


class FlagThread(QThread):
    trigger = pyqtSignal(str)

    def __int__(self):
        super(FlagThread, self).__init__()

    def get_name(self, name=''):
        self.name = name

    def log_in(self):
        if self.name != '':
            user_id, user_name, user_state = search_handler(self.name)
            if user_state == 1:
                self.Msg = '%s %s 签到成功.' % (user_id, user_name)
            elif user_id is None:
                self.Msg = '签到失败'
        else:
            self.Msg = '未检测到人脸'

    def run(self):
        time.sleep(2)
        while True:
            self.get_name()
            timer = threading.Timer(2, self.log_in)  # 等待5s钟调用一次fun_timer() 函数
            timer.start()
            timer.join()
            self.trigger.emit(self.Msg)
            print(self.Msg)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ui = parentWindow()
    ui_child = childWindow()
    ui_child_late = childWindow_late()
    login_btn = ui.Loginbt
    late_btn = ui.Latebt
    login_btn.clicked.connect(ui_child.show)
    late_btn.clicked.connect(ui_child_late.show)
    if mysql_conn is None:
        QMessageBox.warning(ui,
                            "警告",
                            "请先联网，以便进行操作",
                            QMessageBox.Close)
        sys.exit(app.exec_())
    else:
        ui.show()
        sys.exit(app.exec_())

```
## 总结
这个我自己搭建出的人脸识别系统是具有自己学习能力的，你给它喂的数据越多，它就可以识别越多的人而且准确度会不断提高，希望大家可以自己测试和研究。
