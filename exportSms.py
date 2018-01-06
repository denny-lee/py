#!/usr/bin/env python
# _*_ coding: utf-8
import xlsxwriter
from pymongo import MongoClient
from datetime import datetime

conn = MongoClient('172.16.2.148', 27017)
db = conn.get_database('express-admin')  #连接mydb数据库，没有则自动创建
sms_set = db.get_collection('AliSmsRecordEntity')    #使用test_set集合，没有则自动创建
store_set = db.get_collection('StoreEntity')
startTime = datetime(2017, 11, 1)
endTime = datetime(2017, 11, 8)

count = sms_set.find({"storeId":{"$ne":""},"createDate":{"$gte": startTime,"$lte": endTime}}).count()
print(count)
workbook = xlsxwriter.Workbook('sms_2.xlsx')
worksheet = workbook.add_worksheet()
worksheet.write('A1', "aliSmsId")
worksheet.write('B1', "类型")
worksheet.write('C1', "结果")
worksheet.write('D1', "电话")
worksheet.write('E1', "参数")
worksheet.write('F1', "创建时间")
worksheet.write('G1', "错误信息")
worksheet.write('H1', "门店名")
index=0
for i in sms_set.find({"storeId":{"$ne":""},"createDate":{"$gte": startTime,"$lte": endTime}}).skip(80000).limit(40000):
    if i.get("storeId"):
        temId=i['storeId']
        if temId:
            storeName=store_set.find({"_id":temId})[0]['storeName']

    if i.get("aliSmsId"):
        aliSmsId=i['aliSmsId']

    if i.get("smsType"):
        smsType=i['smsType']
    if i.get("smsStatus"):
        smsStatus=i['smsStatus']
    if i.get("phone"):
        phone=i['phone']
    if i.get("jsonParams"):
        jsonParams=i['jsonParams']
    if i.get("createDate"):
        createDate=i['createDate']
    if i.get("taobaoResponseMsg"):
        taobaoResponseMsg=i['taobaoResponseMsg']
    else:
        taobaoResponseMsg=''

    worksheet.write('A'+str(index+2), aliSmsId)
    worksheet.write('B'+str(index+2), smsType)
    worksheet.write('C'+str(index+2), smsStatus)
    worksheet.write('D'+str(index+2), phone)
    worksheet.write('E'+str(index+2), jsonParams)
    worksheet.write('F'+str(index+2), createDate)
    worksheet.write('G'+str(index+2), taobaoResponseMsg)
    worksheet.write('H'+str(index+2), storeName)
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