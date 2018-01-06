#!/usr/bin/env python
# _*_ coding: utf-8

# createDate: 2018.01.06
# Author: wittli


import xlsxwriter
from pymongo import MongoClient
from datetime import datetime
from tkinter import *


class Application(Frame):
    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.pack()
        self.e = StringVar()
        self.dbname = StringVar()
        self.outputName = StringVar()
        self.startDateStr = StringVar()
        self.createWidgets()

    def createWidgets(self):
        self.helloLabel = Label(self, text='请填写库地址和库名，入库时间条件，及输出文件名，再点按钮，导出可能比较慢，请等待!')
        self.helloLabel.pack()

        self.helloLabel = Label(self, text='库地址：')
        self.helloLabel.pack()
        self.enter = Entry(self, textvariable=self.e)
        self.e.set("172.16.2.148")
        self.enter.pack()
        self.helloLabel1 = Label(self, text='库名：')
        self.helloLabel1.pack()
        self.enter = Entry(self, textvariable=self.dbname)
        self.dbname.set("express-admin")
        self.enter.pack()
        self.helloLabel2 = Label(self, text='输出文件名：')
        self.helloLabel2.pack()
        self.enter = Entry(self, textvariable=self.outputName)
        self.outputName.set("微信报表")
        self.enter.pack()
        self.helloLabel3 = Label(self, text='起始日期：')
        self.helloLabel3.pack()
        self.enter = Entry(self, textvariable=self.startDateStr)
        self.startDateStr.set("2017-11-01")
        self.enter.pack()

        self.quitButton = Button(self, text='Rock', command=self.rokeAndRoll)
        self.quitButton.pack()

    def rokeAndRoll(self):
        print(self.e.get())
        ret = self.realJob(self.e.get(), self.dbname.get(), self.outputName.get(), self.startDateStr.get())
        if (ret > 0):
            self.quit()
        else:
            print('参数错误')

    def realJob(self, ip, dbname, outputName, startDateStr):
        if (not ip or not dbname or not outputName or not startDateStr):
            return 0
        if (not outputName.endswith(".xlsx")):
            outputName = outputName + ".xlsx"
        pair = {}
        file = open('kvcache.txt', 'w')

        conn = MongoClient(ip, 27017)
        db = conn.get_database(dbname)

        waybill_coll = db.get_collection('WayBillSEntity')
        store_coll = db.get_collection('StoreEntity')
        wxuser_coll = db.get_collection('TuboboUserEntity')

        workbook = xlsxwriter.Workbook(outputName)
        worksheet = workbook.add_worksheet()
        bold = workbook.add_format({'bold': True, 'align': 'center', 'valign': 'vcenter'})
        worksheet.write('A1', "门店名", bold)
        worksheet.write('B1', "用户数", bold)

        index = 1
        count = 0
        errCount = 0

        startTime = datetime.strptime(startDateStr, "%Y-%m-%d")
        if (not startTime):
            startTime = datetime(2017, 11, 1)

        pipline = [
            {"$match": {"inTime": {"$gte": startTime}}},
            {"$sort": {"inTime": -1}},
            {"$group": {"_id": "$normalUserId",
                        "store": {"$first": "$belongStore"}
                        }
             },
            {"$match": {"_id": {"$nin": ['', None]}}}
            # ,
            # {"allowDiskUse": True}
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

        file = open('kvcache.txt', 'r')
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
        return 1

app = Application()
# 设置窗口标题:
app.master.title('导出小工具')
# 主消息循环:
app.mainloop()




