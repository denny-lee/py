#!/usr/bin/env python
# _*_ coding: utf-8
import xlsxwriter
import MySQLdb

conn=MySQLdb.connect(host='172.16.1.93',port=3306,user='liwtest',passwd='liwtest',db='weekreport',charset='utf8')

cursor=conn.cursor()

cursor.execute('select * from weekreport where removed=FALSE order by dep, name')
res=cursor.fetchall()
print(cursor.rowcount)

workbook = xlsxwriter.Workbook('hello.xlsx')
worksheet = workbook.add_worksheet()
bold = workbook.add_format({'bold': True, 'align': 'center', 'valign': 'vcenter'})
center = workbook.add_format({'align': 'center', 'valign': 'vcenter'})

for index,row in enumerate(res):
    dep=row[1]
    emp=row[2]
    key1='本周关键进展'
    key2='问题、风险'
    key3='下周计划'
    key4='心得'
    v1=row[3]
    v2=row[4]
    v3=row[5]
    v4=row[6]
    worksheet.write('C'+str(index*4+1), key1)
    worksheet.write('D'+str(index*4+1), v1)
    worksheet.write('C' + str(index*4 + 2), key2)
    worksheet.write('D' + str(index*4 + 2), v2)
    worksheet.write('C' + str(index*4 + 3), key3)
    worksheet.write('D' + str(index*4 + 3), v3)
    worksheet.write('C' + str(index*4 + 4), key4)
    worksheet.write('D' + str(index*4 + 4), v4)
    worksheet.merge_range('B'+str(index*4+1)+':B'+str(index*4+4), dep, center)
    worksheet.merge_range('A'+str(index*4+1)+':A'+str(index*4+4), emp, center)
cursor.close()
conn.close()
workbook.close()



