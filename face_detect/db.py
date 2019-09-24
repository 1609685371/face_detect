# -*- coding: utf-8 -*-
# @File  : db.py
# @Author: CSD
# @Date  : 2019/9/7 0007 16:00
# @Software: PyCharm
import pymysql

# 连接数据库
try:
    mysql_conn = pymysql.Connection(
        host='localhost',  # 主机地址
        port=3306,  # 端口号
        user='root',  # 登录用户名
        password='123456',  # 登录密码
        database='face_course',  # 连接的数据库名称
        charset='utf8',  # utf-8的编码
    )
except:
    mysql_conn = None

