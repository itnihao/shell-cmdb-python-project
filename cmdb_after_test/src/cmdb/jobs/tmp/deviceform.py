#-*- coding: UTF-8 -*-

from flask import make_response
from models.device import Device
import json
import xlwt
import StringIO

class DeviceForm:
    def run(self):
        head = ('id','型号')
        contents = []
        devices = Device.query.filter(Device.deleted == 0).all()
        for item in devices:
            if item.storage_extra:
                print(item.storage_extra)
                j_disks = json.loads(item.storage_extra)
                for j_disk in j_disks:
                    model = str(j_disk['capacity'])+' / '+str(j_disk['size'])+' / '+j_disk['interface']+' / '+str(j_disk['speed'])
                content = [item.id,model]
                contents.append(content)
        excel = ExportExcel()
        value = excel.exportexcel('Sheet1',head,contents)
        return make_response(value, 200, {'Content-type': 'application/vnd.ms-excel',
                                                   'Content-Disposition': 'attachment;filename="assets.xls"'})
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
        wb.save('/Users/angel/code/python/device.xls')
        value = sio.getvalue()
        return value



