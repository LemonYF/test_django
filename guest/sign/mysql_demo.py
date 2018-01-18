#!/usr/bin/env python3
# -*- coding: utf-8 -*-

""" a test module """

__author__ = 'YF'

from pymysql import cursors, connect

# 连接数据库
conn = connect(host='127.0.0.1', user='root', password='', charset='utf8mb4', db='guest',
               cursorclass=cursors.DictCursor)
try:
    with conn.cursor() as cursor:
        sql = 'INSERT INTO sign_guest (realname, phone, email, sign, event_id, create_time) VALUES ("Tom",13161868699,"yefan1@lenovo.com",0,1,NOW());'
        cursor.execute(sql)
    conn.commit()

    with conn.cursor() as cursor:
        sql = "SELECT realname,phone,email,sign FROM sign_guest WHERE phone=%s"
        cursor.execute(sql, '13161868699')
        result = cursor.fetchone()
        # result1 = cursor.fetchall()
        print(result)
        # print(result1)
finally:
    conn.close()
