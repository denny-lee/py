#!/usr/bin/env python
# _*_ coding: utf-8
import xlrd

wb = xlrd.open_workbook("/home/jgz/Downloads/个护鞋包选品官说.xls")

sheet = wb.sheet_by_index(0)
print(sheet.nrows)
for i in range(sheet.nrows):
    print(sheet.cell(i,1).value)
