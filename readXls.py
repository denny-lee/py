#!/usr/bin/env python
# _*_ coding: utf-8
from openpyxl import load_workbook

wb = load_workbook("bizResultCode.xlsx")

sheet = wb.get_sheet_by_name("Sheet1")

for i in sheet["A"]:
    if i.value:
        print(i.value)

wb.close()