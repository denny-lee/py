#!/usr/bin/env python
# _*_ coding: utf-8

# createDate: 2018.01.06
# Author: wittli

import xlsxwriter
from pymongo import MongoClient
from datetime import datetime

pair={}
file=open('kvcache.txt', 'w')

# 开发库
# conn = MongoClient('mongo01.ops.com', 27017)
# db = conn.get_database('express-admin-dev')
# db.authenticate("express-admin-dev", "express-admin-dev")

conn = MongoClient('172.16.2.148', 27017)
db = conn.get_database('express-admin')

waybill_coll = db.get_collection('WayBillSEntity')
store_coll = db.get_collection('StoreEntity')
wxuser_coll = db.get_collection('TuboboUserEntity')

workbook = xlsxwriter.Workbook('wxuser.xlsx')
worksheet = workbook.add_worksheet()
bold = workbook.add_format({'bold': True, 'align': 'center', 'valign': 'vcenter'})
worksheet.write('A1', "门店名", bold)
worksheet.write('B1', "用户数", bold)

index=1
count=0
errCount=0

startTime = datetime(2017, 11, 1)

pipline=[
    {"$match":{"inTime":{"$gte": startTime}}},
    { "$sort": { "inTime": -1 } },
    {"$group":{"_id":"$normalUserId",
            "store":{"$first":"$belongStore"}
        }
    },
    {"$match":{"_id":{"$nin":['', None]}}}
]
for i in waybill_coll.aggregate(pipline, allowDiskUse=True):
    if (i.get("_id") and i.get("store")):
        line = i["_id"] + "\t" + i["store"].id;
        file.write(line + "\n")
        count = count + 1
    else:
        errCount = errCount + 1

file.flush()
file.close()

file=open('kvcache.txt', 'r')
while 1:
    line = file.readline()
    if not line:
        break
    userId, storeId = line.replace("\n", "").split("\t")

    if (pair.get(storeId)):
        num = pair[storeId]
        pair[storeId] = num + 1
    else:
        pair[storeId] = 1


for k, v in pair.items():
    index = index + 1
    store = store_coll.find_one({"_id": k})
    if (store):
        worksheet.write('A' + str(index), store["storeName"])
        worksheet.write('B' + str(index), v)
    else:
        worksheet.write('A' + str(index), k)
        worksheet.write('B' + str(index), v)

wxuserCount = wxuser_coll.count({})
index = index + 1
worksheet.write('A' + str(index), '总用户', bold)
worksheet.write('B' + str(index), wxuserCount)

file.close()
conn.close()

print(count)
print(errCount)
workbook.close()
