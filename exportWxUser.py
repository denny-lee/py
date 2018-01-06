#!/usr/bin/env python
# _*_ coding: utf-8
import xlsxwriter
from pymongo import MongoClient
from datetime import datetime


pair={}
file=open('kvpair.txt')
while 1:
    line=file.readline()
    if not line:
        break
    pair[line.split(' - ')[0]] = line.split(' - ')[1].replace("\n", "")

file.close()
ids=[]
file = open('wxuserId.txt')
while 1:
    line = file.readline()
    if not line:
        break
    ids.append(line.replace("\n", ""))

file.close()

conn = MongoClient('172.16.2.148', 27017)
db = conn.get_database('express-admin')  #连接mydb数据库，没有则自动创建
# db.authenticate("express-admin-dev", "express-admin-dev")
# sms_set = db.get_collection('')    #使用test_set集合，没有则自动创建
# store_set = db.get_collection('WayBillSEntity')
store = db.get_collection('StoreEntity')
# userinfo = db.get_collection('TuboboUserEntity')
# startTime = datetime(2017, 11, 1)
# endTime = datetime(2017, 12, 9)

# for i in store_set.find({"inTime":{"$gte": startTime,"$lt": endTime}}):
#     if (i.get('normalUserId')):
#         userId=i['normalUserId']
#         storeId=i['belongStore'].id
#         pair[userId]=storeId
# for i in store_set.find({"inTime": {"$gte": endTime}}):
#     if (i.get('normalUserId')):
#         userId = i['normalUserId']
#         if (pair.get(userId)):
#             del pair[userId]

# workbook = xlsxwriter.Workbook('wxuser.xlsx')
# worksheet = workbook.add_worksheet()
# worksheet.write('A1', "用户名")
# worksheet.write('B1', "电话")
# worksheet.write('C1', "门店名")
# worksheet.write('D1', "门店城市")
index=0
count=0
for k,v in enumerate(ids):
    # print(k,'-',v)
    count=count+1
    s=store.find_one({"_id":pair[v]})
    # u=userinfo.find_one({"_id":k})
    if (s):
        # worksheet.write('A' + str(index + 2), u['nickName'])
        # worksheet.write('B' + str(index + 2), u['phone'])
        # worksheet.write('C' + str(index + 2), s['storeName'])
        # worksheet.write('D' + str(index + 2), s['city'])
        # print(u['nickName'],'\t',u['phone'],'\t',s['storeName'],'\t',s['city'])
        city=''
        if (s.get('city')):
            city=s['city']
        print(s['storeName'],'\t',city)
    else:
        print(pair[v])
    index=index+1
# workbook.close()
print(count)
conn.close()