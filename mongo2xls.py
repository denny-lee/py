#!/usr/bin/env python
# _*_ coding: utf-8
# import xlsxwriter
from pymongo import MongoClient

conn=MongoClient("127.0.0.1", 27017)

db=conn.learn
waybill= db.waybill

# workbook = xlsxwriter.Workbook('hello.xlsx')
# worksheet = workbook.add_worksheet()
# bold = workbook.add_format({'bold': True, 'align': 'center', 'valign': 'vcenter'})
# center = workbook.add_format({'align': 'center', 'valign': 'vcenter'})
pipline=[
    {"$sort":{"createDate":-1}},
    {
        "$group":{
            "_id":"$userId",
            "store":{"$first":"$storeId"}
        }
    }
]
for i in waybill.aggregate(pipline):
    print(i['_id'])
    # dep=row[1]
    # emp=row[2]
    # key1='本周关键进展'
    # key2='问题、风险'
    # key3='下周计划'
    # key4='心得'
    # v1=row[3]
    # v2=row[4]
    # v3=row[5]
    # v4=row[6]
    # worksheet.write('C'+str(index*4+1), key1)
    # worksheet.write('D'+str(index*4+1), v1)
    # worksheet.write('C' + str(index*4 + 2), key2)
    # worksheet.write('D' + str(index*4 + 2), v2)
    # worksheet.write('C' + str(index*4 + 3), key3)
    # worksheet.write('D' + str(index*4 + 3), v3)
    # worksheet.write('C' + str(index*4 + 4), key4)
    # worksheet.write('D' + str(index*4 + 4), v4)

conn.close()
# workbook.close()



