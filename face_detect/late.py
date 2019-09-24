# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'late.ui'
#
# Created by: PyQt5 UI code generator 5.13.0
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Table(object):
    def setupUi(self, Table):
        Table.setFixedSize(549, 389)
        Table.setWindowFlags(QtCore.Qt.WindowCloseButtonHint)
        Table.setObjectName("Table")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/newPrefix/签到.jpeg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        Table.setWindowIcon(icon)
        self.frame = QtWidgets.QFrame(Table)
        self.frame.setGeometry(QtCore.QRect(140, 10, 361, 341))
        self.frame.setFrameShape(QtWidgets.QFrame.Box)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.tableWidget = QtWidgets.QTableWidget(self.frame)
        self.tableWidget.setGeometry(QtCore.QRect(20, 10, 321, 321))
        self.tableWidget.setObjectName("tableWidget")
        self.tableWidget.setColumnCount(3)
        self.tableWidget.setRowCount(0)
        item = QtWidgets.QTableWidgetItem()
        item.setTextAlignment(QtCore.Qt.AlignCenter)
        self.tableWidget.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(2, item)
        self.layoutWidget = QtWidgets.QWidget(Table)
        self.layoutWidget.setGeometry(QtCore.QRect(30, 30, 82, 291))
        self.layoutWidget.setObjectName("layoutWidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.layoutWidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.ShowBt = QtWidgets.QPushButton(self.layoutWidget)
        self.ShowBt.setObjectName("ShowBt")
        self.verticalLayout.addWidget(self.ShowBt)
        self.ResetBt = QtWidgets.QPushButton(self.layoutWidget)
        self.ResetBt.setObjectName("ResetBt")
        self.verticalLayout.addWidget(self.ResetBt)

        self.retranslateUi(Table)
        QtCore.QMetaObject.connectSlotsByName(Table)

    def retranslateUi(self, Table):
        _translate = QtCore.QCoreApplication.translate
        Table.setWindowTitle(_translate("Table", "签到表"))
        item = self.tableWidget.horizontalHeaderItem(0)
        item.setText(_translate("Table", "学号"))
        item = self.tableWidget.horizontalHeaderItem(1)
        item.setText(_translate("Table", "姓名"))
        item = self.tableWidget.horizontalHeaderItem(2)
        item.setText(_translate("Table", "状态"))
        self.ShowBt.setText(_translate("Table", "显示缺勤名单"))
        self.ResetBt.setText(_translate("Table", "重置"))
import icon.icon_rc
