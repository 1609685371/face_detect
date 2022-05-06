## 前言

一个基于MTCNN人脸检测和FaceNet进行人脸识别签到系统，作者某二本大学里的末流学生，写于2019/09/，python学习期间。
今年7月份开始接触python的，最近闲着无事就开始做了这个人脸识别的系统，一开始的话就想着简单的弄下，就去了[百度智能云](https://console.bce.baidu.com/)用的api接口实现的，写完以后我就想为什么我不自己写一个人脸识别签到，不去调用百度api接口，然后就诞生了这个程序。

## 先看下效果
![在这里插入图片描述](https://img02-xusong.taihe.com/979F839A-4A5A-4730-BCE0-E8B7FB28887D.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3UwMTEzMjUyMTM=,size_16,color_FFFFFF,t_70)
## 实现的功能

 - 点击开始进行实时人脸打开识别签到![在这里插入图片描述](https://img02-xusong.taihe.com/979F839A-4A5A-4730-BCE0-E8B7FB28887D.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3UwMTEzMjUyMTM=,size_16,color_FFFFFF,t_70)
 - 点击注册会跳到注册页面进行注册![在这里插入图片描述](https://img02-xusong.taihe.com/62DEF605-D945-43C0-A61F-9E4543E1867B.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3UwMTEzMjUyMTM=,size_16,color_FFFFFF,t_70)
 - 点击缺勤会打开缺勤窗口显示缺勤的表格![在这里插入图片描述](https://img02-xusong.taihe.com/EE24C860-2C6E-4A11-848C-6E4F6F16A51D.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3UwMTEzMjUyMTM=,size_16,color_FFFFFF,t_70)
 - 缺勤查询系统![在这里插入图片描述](https://img02-xusong.taihe.com/5E7D66DE-F51D-41B6-AF1B-F2C927EE23F6.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3UwMTEzMjUyMTM=,size_16,color_FFFFFF,t_70)
 - 缺勤查询系统，查询指定一天
 - ![在这里插入图片描述](https://img02-xusong.taihe.com/90F794C6-0D07-40BC-B234-49AEE1A13BAF.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3UwMTEzMjUyMTM=,size_16,color_FFFFFF,t_70)
 - 缺勤查询系统，查询指定范围
 - ![在这里插入图片描述](https://img02-xusong.taihe.com/7D663E68-8114-4920-AEAD-FCD663739A79.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3UwMTEzMjUyMTM=,size_16,color_FFFFFF,t_70)

## 开始准备
选用语言Python，时下入门机器学习成本最低、学习速度最快的语言，python搞网络爬虫也很靠谱。运用的技术有 opencv（摄像头、图片处理），numpy（图片数字化），os（文件的操作和处理），Pytorch（构建神经网络进行模型训练）。
## 页面的构建
我的UI页面是用pyqt写的，pyqt这块也不是很熟练，就稍微看了看教程，问了问同学，摸索着开始使用了，关于pyqt这块的话，不和大家多说了，大家可以看下这个链接[pyqt5、qtdesigner安装和环境设置](https://blog.csdn.net/weixin_43008870/article/details/85766035)，我的这个程序也是亏了博主的这篇博客，大爱![在这里插入图片描述](https://img-blog.csdnimg.cn/2019092419533616.png)
##  功能实现
这里我就长话短说，因为涉及的东西比较多，我就按照我的目录中的文件开始讲起![在这里插入图片描述](https://img02-xusong.taihe.com/59660CD8-418E-4811-84F8-A46C9F8590D6.png)
 - icon这个文件夹主要是存放UI页面的图标
 - detection文件夹是用来检测人脸区域的
 - face_db文件夹是存放的人脸库
 - save_model文件夹是之前保存的模型
 - ui文件夹是保存的页面文件
 - db.py用来建立连接数据库的对象
 - face_register.py文件向数据库进行插入用户数据
 - face_search.py文件是在进行签到时更新数据库中用户的状态，是签到了还是迟到了
 - manageMain.py是显示后台缺勤的
 - predictor.py是用来识别人脸的
 - user_log_late是将未出勤的用户写入数据库
 - main.py这个文件，基本上所有的执行代码就在这了，这里呢用到了pyqt的多线程QThread以及python的多线程threading，这俩稍微有点那么区别，但基本上实现都是相通的，为什么会用到多线程呢？这是因为在一开始进行注册拍照和模型训练的时候，我发现如果不启用多线程，前端的ui页面就会未响应，当模型训练完成以后才恢复正常，这样给用户带来的体验是极差的，所以尽量将ui展示页面和功能实现的代码分开，在显示页面的同时还能进行后台的运算。（~不知道这样说对不对，说错的还请大家指出来，小白虚心学习~）
## 代码部分
这里就放main.py文件的吧，其他的放了估计也太多![在这里插入图片描述](https://img-blog.csdnimg.cn/20190924203953898.gif)

```
# -*- coding: utf-8 -*-
# @File  : main.py
# @Author: CSD
# @Date  : 2019/9/7 0007 20:48
# @Software: PyCharm
import os
import sys
import threading
import time

import cv2
import qimage2ndarray
from PyQt5.QtCore import QTimer, Qt, QThread, pyqtSignal, pyqtSlot, QPoint
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QApplication, QMainWindow, QDialog, QAbstractItemView, QTableWidgetItem, QMessageBox

from Predictor import Predictor
from ui.mainWin import Ui_mainWin
from db import mysql_conn
from face_register import register_handler
from face_search import search_handler
from ui.late import Ui_Table
from ui.register import Ui_Register
from datetime import datetime


# 主窗口
class parentWindow(QMainWindow, Ui_mainWin):

    def __del__(self):
        try:
            self.camera.release()  # 释放资源
        except:
            return

    def __init__(self, parent=None):
        super(parentWindow, self).__init__(parent)
        self.setupUi(self)
        self.Timer = QTimer()  # 实例化一个类
        self.Timer.timeout.connect(self.TimerOutFun)  # 定时刷新
        self.flagThread = FlagThread()
        # 当获得循环完毕的信号时，停止计数
        self.flagThread.trigger.connect(self.fun_timer)
        self.name = 'test'

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

    # 开始按钮函数
    @pyqtSlot()
    def on_showBt_clicked(self):
        self.lateBt.setEnabled(True)
        self.PrepCamera()
        self.predictor = Predictor(mtcnn_model_path, mobilefacenet_model_path, face_db_path, threshold=0.5)
        self.Timer.start(1)  # 每隔1ms刷新一次
        self.timelb = time.perf_counter()
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
        boxes, names = self.predictor.recognition(self.Image)
        if boxes is not None:
            img = self.predictor.draw_face(self.Image, boxes, names)
            self.flagThread.get_name(names[0])
            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            qimg = qimage2ndarray.array2qimage(img)  # 调用array2qimage函数将其转为QImage格式
            self.dispLb.setPixmap(QPixmap(qimg))  # 再通过QPixmap函数转为QPixmap格式进行显示。
            self.dispLb.show()  # 图像显示

    # 帮助
    @pyqtSlot()
    def on_aboutBt_clicked(self):
        QMessageBox.information(self,
                                "关于",
                                "1.点击开始按钮播放视频流,进行签到\n"
                                "2.点击注册按钮可跳往注册窗口进行注册\n"
                                "3.点击缺勤按钮可查看缺勤学生名单，状态0代表缺勤\n"
                                "4.点击帮助按钮可查看帮助，同时关闭主窗口视频流,进行人脸注册",
                                QMessageBox.Close)

    # 关闭摄像头
    @pyqtSlot()
    def on_closeBt_clicked(self):
        try:
            self.camera.release()  # 释放资源
        except:
            return

    # 最小化
    @pyqtSlot()
    def on_pushButton_min_clicked(self):
        self.showMinimized()

    # 关闭程序
    @pyqtSlot()
    def on_pushButton_close_clicked(self):
        self.close()

    def mouseMoveEvent(self, e):  # 重写移动事件
        if self._tracking:
            self._endPos = e.pos() - self._startPos
            self.move(self.pos() + self._endPos)

    def mousePressEvent(self, e):
        if e.button() == Qt.LeftButton:
            self._startPos = QPoint(e.x(), e.y())
            self._tracking = True

    def mouseReleaseEvent(self, e):
        if e.button() == Qt.LeftButton:
            self._tracking = False
            self._startPos = None
            self._endPos = None


# 注册窗口
class childWindow(QDialog, Ui_Register):

    def __init__(self, parent=None):
        super(childWindow, self).__init__(parent)
        self.setupUi(self)
        self.photoBt.setEnabled(False)
        self.registerBt.setEnabled(False)
        self.photoThread = PhotoThread()
        # 当获得循环完毕的信号时，停止计数
        self.photoThread.trigger.connect(self.timeStop)
        self.Timer = QTimer()  # 实例化一个类
        self.Timer.timeout.connect(self.TimerOutFun)  # 定时刷新

    # 初始化摄像头并打开
    def PrepCamera(self):
        try:
            self.camera = cv2.VideoCapture(0)
            self.camera.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc('M', 'J', 'P', 'G'))
            self.MsgLb.clear()
            self.MsgLb.setText('请输入学号、姓名!')
        except Exception as e:
            self.MsgLb.clear()
            self.MsgLb.setText(str(e))

    # 开始按钮函数
    @pyqtSlot()
    def on_startBt_clicked(self):
        self.photoBt.setEnabled(True)
        self.registerBt.setEnabled(True)
        self.PrepCamera()
        self.Timer.start(1)  # 每隔1ms刷新一次
        self.timelb = time.perf_counter()

    # 注册模块
    @pyqtSlot()
    def on_registerBt_clicked(self):
        print('on_registerBt_clicked')
        Msg = register_handler(self.stu_id.text(), self.stu_name.text())
        self.MsgLb.setText(Msg)

    # 拍照按钮函数
    @pyqtSlot()
    def on_photoBt_clicked(self):
        print('on_photoBt_clicked')
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

    def timeStop(self, msg):
        self.MsgLb.setText(msg)

    @pyqtSlot()
    def on_minButton_clicked(self):
        # 最小化
        self.showMinimized()

    @pyqtSlot()
    def on_closeButton_clicked(self):
        # 关闭程序
        try:
            self.camera.release()
            self.close()
        except:
            self.close()

    def mouseMoveEvent(self, e):  # 重写移动事件
        if self._tracking:
            self._endPos = e.pos() - self._startPos
            self.move(self.pos() + self._endPos)

    def mousePressEvent(self, e):
        if e.button() == Qt.LeftButton:
            self._startPos = QPoint(e.x(), e.y())
            self._tracking = True

    def mouseReleaseEvent(self, e):
        if e.button() == Qt.LeftButton:
            self._tracking = False
            self._startPos = None
            self._endPos = None


# 缺勤窗口
class childWindow_late(QDialog, Ui_Table):
    def __init__(self, parent=None):
        super(childWindow_late, self).__init__(parent)
        self.setupUi(self)
        self.tableWidget.setEditTriggers(QAbstractItemView.NoEditTriggers)

    # 显示缺勤表格
    @pyqtSlot()
    def on_showBt_clicked(self):
        sql = 'select * from users where state=0'
        # print(sql)
        cursor = mysql_conn.cursor()
        cursor.execute(sql)
        results = cursor.fetchall()
        # print(results)
        if results:
            row = cursor.rowcount
            vol = len(results[0])
            self.tableWidget.setRowCount(row)
            self.tableWidget.setColumnCount(3)
            for i in range(row):
                for j in range(3):
                    temp_data = results[i][j + 1]  # 临时记录，不能直接插入表格
                    data = QTableWidgetItem(str(temp_data))  # 转换后可插入表格
                    data.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
                    self.tableWidget.setItem(i, j, data)

    # 最小化
    @pyqtSlot()
    def on_minButton_clicked(self):
        self.showMinimized()

    # 关闭程序
    @pyqtSlot()
    def on_closeButton_clicked(self):
        self.close()

    def mouseMoveEvent(self, e):  # 重写移动事件
        if self._tracking:
            self._endPos = e.pos() - self._startPos
            self.move(self.pos() + self._endPos)

    def mousePressEvent(self, e):
        if e.button() == Qt.LeftButton:
            self._startPos = QPoint(e.x(), e.y())
            self._tracking = True

    def mouseReleaseEvent(self, e):
        if e.button() == Qt.LeftButton:
            self._tracking = False
            self._startPos = None
            self._endPos = None


class PhotoThread(QThread, Ui_Register):
    trigger = pyqtSignal(str)

    def __int__(self):
        super(PhotoThread, self).__init__()

    def img(self, img, stu_name):
        self.image = img
        self.stu_name = stu_name

    def run(self):
        filepath = './face_db/'  # 路径拼接
        if not os.path.exists(filepath):  # 看是否需要创建路径
            os.makedirs(filepath)
        savePath = (filepath + "%s.jpg" % self.stu_name)
        cv2.imencode('.jpg', self.image, [cv2.IMWRITE_JPEG_QUALITY, 100])[1].tofile(savePath)  # 保存图片
        self.trigger.emit('图片采集完毕！')


class FlagThread(QThread):
    trigger = pyqtSignal(str)

    def __int__(self):
        super(FlagThread, self).__init__()

    def get_name(self, name=''):
        self.name = name

    def log_in(self):
        hour = datetime.utcnow().hour + 8
        hour = True
        if hour:
            if self.name != 'unknow':
                print(self.name)
                user_id, user_name, user_state = search_handler(self.name)
                if user_state == 1:
                    self.Msg = '%s %s 签到成功.' % (user_id, user_name)
                elif user_id is None:
                    self.Msg = '员工不存在'
            else:
                self.Msg = '请重新检测'
        else:
            self.Msg = '出勤迟到'

    def run(self):
        time.sleep(2)
        while True:
            self.get_name()
            timer = threading.Timer(2, self.log_in)  # 等待2s钟调用一次log_in() 函数
            timer.start()
            timer.join()
            self.trigger.emit(self.Msg)
            # if count == 20:
            #     break
            # print(self.Msg)


if __name__ == '__main__':
    try:
        mtcnn_model_path = 'save_model/mtcnn'
        mobilefacenet_model_path = 'save_model/mobilefacenet.pth'
        face_db_path = 'face_db'
        app = QApplication(sys.argv)
        ui = parentWindow()
        ui_child = childWindow()
        ui_child_late = childWindow_late()
        login_btn = ui.loginBt
        late_btn = ui.lateBt
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
    except:
        sys.exit(app.exec_())

```
## 总结
该项目的人脸识别部分是基于FaceNet实现的，另外程序不免费，需要的加qq1609685371，大佬绕道谢谢。
