#!/usr/bin/env python
# _*_ coding: utf-8
import xlsxwriter

workbook = xlsxwriter.Workbook('hello.xlsx')
worksheet = workbook.add_worksheet()

bold = workbook.add_format({'bold': True, 'align': 'center', 'valign': 'vcenter'})
center = workbook.add_format({'align': 'center', 'valign': 'vcenter'})

worksheet.merge_range('A1:G1', u'标题', bold)
worksheet.merge_range('A2:A10', 'Helle Kitty', center)

workbook.close()