#!/usr/bin/env python
# _*_ coding: utf-8
from openpyxl import load_workbook
from datetime import datetime

wb = load_workbook("store1.xlsx")

sheet = wb.get_sheet_by_name("Sheet1")

arr1=[]
arr2=[]
arr3=[]
arr4=[]
arr5=[]
arr6=[]
arr7=[]
arr8=[]
arr9=[]
arr10=[]
ch=","
for i in sheet["A"]:
    if i.value:
        id=i.value[0:44]+" }"
        arr1.append(id)
for i in sheet["B"]:
    if i.value:
        prv=i.value+"省"
        arr2.append(prv)

for i in sheet["C"]:
    if i.value:
        city=i.value+"市"
        arr3.append(city)
for i in sheet["D"]:
    if i.value:
        dis=i.value
        arr4.append(dis)
for i in sheet["E"]:
    if i.value and len(i.value) > 3:
        lon=i.value
        idx=str(lon).index(ch)
        lenth=len(lon)
        arr5.append(str(lon)[0:idx])
        arr6.append(str(lon)[idx+1:lenth])
for i in sheet["G"]:
    if i.value:
        d=i.value
        year=str(d).split(" ")
        timeStr=year[0]+"T"+year[1]+".000+8"
        arr7.append(timeStr)

for i in sheet["H"]:
    if i.value:
        zCode=i.value
        zc=str(zCode).split(",")
        arr8.append(zc[0])
        arr9.append(zc[1])
        arr10.append(zc[2][0:6])

index=0
for i in arr1:
    code='db.getCollection("StoreEntity").update('+arr1[index]+',{"$set":{"province": "'+arr2[index]+'","provinceCode":"'+arr8[index]+'","city":"'+arr3[index]+'","cityCode":"'+arr9[index]+'","district":"'+arr4[index]+'","districtCode":"'+arr10[index]+'","longitude":'+arr5[index]+',"latitude":'+arr6[index]+',"createDate":ISODate("'+arr7[index]+'")}})'
    print(code)
    index=index+1
wb.close()