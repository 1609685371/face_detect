# -*- coding: utf-8 -*-
# @File  : main.py
# @Author: CSD
# @Date  : 2019/9/7 0007 20:48
# @Software: PyCharm
import gc
import os

os.environ["CUDA_VISIBLE_DEVICES"] = "-1"
import sys

if hasattr(sys, 'frozen'):
    os.environ['PATH'] = sys._MEIPASS + ";" + os.environ['PATH']
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
        self.PrepCamera()
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
        # self.PrepCamera()
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
