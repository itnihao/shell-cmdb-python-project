# coding=utf-8
__author__ = 'qiqi'

import xlwt,StringIO

class ExportExcel():
    def exportexcel(self,sheetname,head,content):
        wb = xlwt.Workbook(encoding='utf-8')
        ws = wb.add_sheet(sheetname)
        row = 1
        for column,name in enumerate(head):
            ws.write(0, column, name)
        for count,name in enumerate(content):
            for column,item in enumerate(name):
                ws.write(row, column, item)
            row += 1
        sio = StringIO.StringIO()
        wb.save(sio)
        value = sio.getvalue()
        return value

    def exportexcel_stream(self,sheetname,head,content):
        wb = xlwt.Workbook(encoding='utf-8')
        ws = wb.add_sheet(sheetname)
        row = 1
        for column,name in enumerate(head):
            ws.write(0, column, name)
        for count,name in enumerate(content):
            for column,item in enumerate(name):
                ws.write(row, column, item)
            row += 1
        sio = StringIO.StringIO()
        wb.save(sio)
        # value = sio.getvalue()
        return wb
