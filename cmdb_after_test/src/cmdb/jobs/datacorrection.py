# -*- coding: utf-8 -*-
from application import db
from models.host_load_ratio import HostLoadRatio
import json
import getopt, sys

class DataCorrection:
    def run(self):
        param= None
        opts, args = getopt.getopt(sys.argv[1:], "hm:p:")
        for op, mod in opts:
            if op == "-p":
                param = mod
        self.data_correction(param)

    def data_correction(self,page):
        page = int(page)
        if page<=0:
            page = 1

        tmp_max_id = 415541
        pageSize = 1000
        from_index=(page-1)*pageSize
        tmp =  HostLoadRatio.query.filter(HostLoadRatio.id<=tmp_max_id).offset(from_index).limit(pageSize).all()
        if tmp:
            for item in tmp:
                id = item.id
                print 'id:%s'%(id)
                item.ratio = self.calratio(item.content)
                db.session.commit()



    def calratio(self,content):
        items = json.loads(content)
        b = 'cpu_1'
        a = float(items[b])
        if float(items['disk_used'])> a :
            b = 'disk_used'
            a = float(items[b])

        if float(items['mem_used'])> a :
            b = 'mem_used'
            a = float(items[b])

        if float(items['net'])> a :
            b = 'net'
            a = float(items[b])

        if float(items['iowait'])> a :
            b = 'iowait'
            a = float(items[b])

        tmp_ratio = 0.0
        for k,v in items.items():
            if k!= b:
                tmp_ratio += float(v)*0.05

        tmp_ratio += a*0.8
        tmp_ratio = float('%.2f'%tmp_ratio)
        return tmp_ratio