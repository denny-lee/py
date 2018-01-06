#!/usr/bin/env python
# _*_ coding: utf-8
from openpyxl import load_workbook
from datetime import datetime

wb = load_workbook("store1.xlsx")

sheet = wb.get_sheet_by_name("Sheet1")

idx=0
count=0
for i in sheet["A"]:
    if i.value:
        id=i.value[11:43]
        flag=sheet["F"]
        if (flag[idx].value)=='N':
            print('"'+id+'",')
            count=count+1
        idx=idx+1
print(count)
wb.close()