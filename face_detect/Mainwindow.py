# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'Mainwindow.ui'
#
# Created by: PyQt5 UI code generator 5.13.0
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(796, 652)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/newPrefix/签到.jpeg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        MainWindow.setWindowIcon(icon)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName("gridLayout")
        self.frame_3 = QtWidgets.QFrame(self.centralwidget)
        self.frame_3.setMinimumSize(QtCore.QSize(0, 0))
        self.frame_3.setMaximumSize(QtCore.QSize(16777215, 60))
        self.frame_3.setFrameShape(QtWidgets.QFrame.Box)
        self.frame_3.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_3.setObjectName("frame_3")
        self.MsgTE = QtWidgets.QTextEdit(self.frame_3)
        self.MsgTE.setEnabled(True)
        self.MsgTE.setGeometry(QtCore.QRect(10, 10, 751, 41))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(15)
        font.setBold(True)
        font.setWeight(75)
        self.MsgTE.setFont(font)
        self.MsgTE.setTabletTracking(True)
        self.MsgTE.setUndoRedoEnabled(True)
        self.MsgTE.setObjectName("MsgTE")
        self.gridLayout.addWidget(self.frame_3, 1, 0, 1, 2)
        self.DispFm = QtWidgets.QFrame(self.centralwidget)
        self.DispFm.setMinimumSize(QtCore.QSize(600, 0))
        self.DispFm.setMaximumSize(QtCore.QSize(400, 16777215))
        self.DispFm.setFrameShape(QtWidgets.QFrame.Box)
        self.DispFm.setFrameShadow(QtWidgets.QFrame.Raised)
        self.DispFm.setObjectName("DispFm")
        self.DispLb = QtWidgets.QLabel(self.DispFm)
        self.DispLb.setGeometry(QtCore.QRect(10, 10, 581, 501))
        self.DispLb.setText("")
        self.DispLb.setPixmap(QtGui.QPixmap(":/newPrefix/title.jpg"))
        self.DispLb.setObjectName("DispLb")
        self.gridLayout.addWidget(self.DispFm, 0, 0, 1, 1)
        self.SettingsFm = QtWidgets.QFrame(self.centralwidget)
        self.SettingsFm.setFrameShape(QtWidgets.QFrame.Box)
        self.SettingsFm.setFrameShadow(QtWidgets.QFrame.Raised)
        self.SettingsFm.setObjectName("SettingsFm")
        self.layoutWidget = QtWidgets.QWidget(self.SettingsFm)
        self.layoutWidget.setGeometry(QtCore.QRect(50, 20, 77, 471))
        self.layoutWidget.setObjectName("layoutWidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.layoutWidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.Showbt = QtWidgets.QPushButton(self.layoutWidget)
        self.Showbt.setObjectName("Showbt")
        self.verticalLayout.addWidget(self.Showbt)
        self.Loginbt = QtWidgets.QPushButton(self.layoutWidget)
        self.Loginbt.setObjectName("Loginbt")
        self.verticalLayout.addWidget(self.Loginbt)
        self.Latebt = QtWidgets.QPushButton(self.layoutWidget)
        self.Latebt.setObjectName("Latebt")
        self.verticalLayout.addWidget(self.Latebt)
        self.About = QtWidgets.QPushButton(self.layoutWidget)
        self.About.setObjectName("About")
        self.verticalLayout.addWidget(self.About)
        self.gridLayout.addWidget(self.SettingsFm, 0, 1, 1, 1)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 796, 23))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "人脸识别签到"))
        self.MsgTE.setHtml(_translate("MainWindow", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'Arial\'; font-size:15pt; font-weight:600; font-style:normal;\">\n"
"<p align=\"center\" style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-family:\'微软雅黑\';\"><br /></p></body></html>"))
        self.Showbt.setText(_translate("MainWindow", "开始"))
        self.Loginbt.setText(_translate("MainWindow", "注册"))
        self.Latebt.setText(_translate("MainWindow", "缺勤名单"))
        self.About.setText(_translate("MainWindow", "帮助"))
import icon.icon_rc
