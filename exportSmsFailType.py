#!/usr/bin/env python
# _*_ coding: utf-8
import xlsxwriter
from pymongo import MongoClient
from datetime import datetime

conn = MongoClient('172.16.2.148', 27017)
db = conn.get_database('express-admin')  #连接mydb数据库，没有则自动创建
sms_set = db.get_collection('AliSmsRecordEntity')    #使用test_set集合，没有则自动创建
startTime = datetime(2017, 11, 1)
endTime = datetime(2017, 11, 8)

count = sms_set.find({"storeId":{"$ne":""},"createDate":{"$gte": startTime,"$lte": endTime}}).count()
print(count)

workbook = xlsxwriter.Workbook('sms_3.xlsx')
worksheet = workbook.add_worksheet()
worksheet.write('A1', "错误信息")
worksheet.write('B1', "发生次数")
index=0
subMsgCount={}
msgCount={}
for i in sms_set.find({"storeId":{"$ne":""},"createDate":{"$gte": startTime,"$lte": endTime}}).skip(0).limit(40000):
    # if i.get("taobaoResponseSubMsg"):
    #     subMsg=i['taobaoResponseSubMsg']
    #     if subMsg in subMsgCount:
    #         subMsgCount[subMsg] = subMsgCount[subMsg] + 1
    #     else:
    #         subMsgCount[subMsg] = 1
    if i.get("bizResultCode"):
        msg = i['bizResultCode']
        if msg in msgCount:
            msgCount[msg] = msgCount[msg] + 1
        else:
            msgCount[msg] = 1
            # elif i.get("taobaoResponseMsg"):
    #     msg = i['taobaoResponseMsg']
    #     count = msgCount[msg]
    #     if count:
    #         msgCount[msg] = msgCount[msg]+1
    #     else:
    #         msgCount[msg] = 1

for k,v in msgCount.items():
    worksheet.write('A'+str(index+2), k)
    worksheet.write('B'+str(index+2), v)
    index=index+1

#
# bold = workbook.add_format({'bold': True, 'align': 'center', 'valign': 'vcenter'})
# center = workbook.add_format({'align': 'center', 'valign': 'vcenter'})
#
# worksheet.merge_range('A1:G1', u'标题', bold)
# worksheet.merge_range('A2:A10', 'Helle Kitty', center)
#
workbook.close()

conn.close()