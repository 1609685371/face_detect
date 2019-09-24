# -*- coding: utf-8 -*-
# @File  : face_register.py
# @Author: CSD
# @Date  : 2019/9/8 0008 9:05
# @Software: PyCharm

from db import mysql_conn

'''
    
'''
def register_handler(stu_id, stu_name):

    ret = stu_id.isdigit()
    if ret:
        cursor = mysql_conn.cursor()
        user_id = stu_id
        user_name = stu_name
        user_state = 0
        try:
            sql = "insert into users(user_id, user_name, state) values ('%s', '%s', %s)" % (
                user_id, user_name, user_state)
            cursor.execute(sql)
            mysql_conn.commit()
            Msg = user_id + ' ' + user_name + '注册成功'
            return Msg
        except:
            mysql_conn.rollback()
            Msg = user_id + ' ' + user_name + '注册失败'
            return Msg
    else:
        return '请输入正确的学号'
