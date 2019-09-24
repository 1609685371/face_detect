# -*- coding: utf-8 -*-
# @File  : face_search.py
# @Author: CSD
# @Date  : 2019/9/6 0006 12:49
# @Software: PyCharm
from db import mysql_conn


def search_handler(dirname=''):
    cursor = mysql_conn.cursor()
    try:
            sql_update = "update  users set state = 1 where user_name='%s'" % dirname
            cursor.execute(sql_update)
            mysql_conn.commit()
            sql = "select * from users where user_name='%s'" % dirname
            cursor.execute(sql)
            results = cursor.fetchall()
            if results:
                for ret in results:
                    user_id = ret[1]
                    user_name = ret[2]
                    user_state = ret[3]
                    return user_id, user_name, user_state
            else:
                return None, None, None
    except:
        mysql_conn.rollback()
