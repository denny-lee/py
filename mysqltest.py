#!/usr/bin/env python
# _*_ coding: utf-8
import MySQLdb

conn=MySQLdb.connect(host='172.16.1.181',port=3306,user='tubobo_admin',passwd='tubobo_admin',db='tubobo_admin',charset='utf8')

cursor=conn.cursor()

cursor.execute('select * from sys_user')
res=cursor.fetchmany(5)
print(cursor.rowcount)
for row in res:
    print(row)
cursor.close()
conn.close()