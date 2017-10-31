#!/usr/bin/env python
# _*_ coding: utf-8
import MySQLdb

conn=MySQLdb.connect(host='172.16.1.93',port=3306,user='liwtest',passwd='liwtest',db='weekreport',charset='utf8')

cursor=conn.cursor()

cursor.execute('select * from weekreport where removed=FALSE order by dep, name')
res=cursor.fetchall()
print(cursor.rowcount)
for row in res:
    print(row)
cursor.close()
conn.close()

