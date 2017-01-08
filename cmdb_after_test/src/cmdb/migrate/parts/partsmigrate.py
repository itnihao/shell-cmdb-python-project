# -*- coding: utf-8 -*-
from sqlalchemy import *
from config import PARTS_MIGRATE_DATABASE_URI
from models.stock_parts_model import StockPartsModel
from models.stock_parts import StockParts
from models.stock_history import StockHistory
from models.host import Host

from application import app, db
import hashlib

class PartsMigrate:
    def run(self):
        print '--------start-----'
        self.separator = ' / '
        self.humanmapping = {
            'db20-008':'app00-002',
            'apcbak20-002':'apc20-003',
            'apcbak20-003':'apc20-004',
            'App20-007':'apcbak20-004',
            'APP20-006':'apc20-004',
            'App-080':'App10-080',
            '2102310KCS10E5000852':'opsbak10-013',
            '2102310KCS10E5000851':'opsbak10-012',
            '2102310KCS10E5000855':'apc10-020',
            '2102310KCS10E5001491':'apc10-021',
            'OFFICE-LB00-002':'LB00-002'
        }
        db.engine.execute("truncate table stock_parts")
        db.engine.execute("truncate table stock_history")
        self.disk()
        self.mem()
        print '--------end-----'

    def disk(self):
        model_dic = {}
        model_lists = StockPartsModel.query.filter(StockPartsModel.type == StockPartsModel.TYPE_DISK).all()
        for item in model_lists:
            md5_item = hashlib.md5(item.content).hexdigest()
            model_dic[md5_item] = item.id

        engine = create_engine(PARTS_MIGRATE_DATABASE_URI, encoding='utf-8',echo=False)
        connection = engine.connect()
        result = connection.execute("select *  from Hdisk") #采购
        for row in result:
            if int(row[3]) >= 1000:
                    tmp_row3 = '%dT'%int(int(row[3])/1000)
            else:
                tmp_row3 = '%sG'%row[3]
            item = '%s#%s英寸#%s#%s#%sGb/s'%(tmp_row3,row[2],row[4],row[5],row[7])
            item = item.replace("#",self.separator)
            md5_item = hashlib.md5(item).hexdigest()
            tmp_model_id = model_dic[md5_item]
            tmp_count  =  row[1]
            tmp_hdisk_id = row[0]
            target = StockParts(type=StockParts.TYPE_DISK, model_id = tmp_model_id, num = tmp_count,status = 0)
            db.session.add(target)
            db.session.commit()
            tmp_target_id = target.id
            histarget = StockHistory(target_id = tmp_target_id,num=tmp_count,created = row[9])
            db.session.add(histarget)
            db.session.commit()
            sql = "select *  from Hdisk_USED where hdisk_id = %d"%tmp_hdisk_id
            tmp_result = connection.execute(sql)
            for tmp_row in tmp_result:
                tmp_hostname = tmp_row[2]
                tmp_device_id = self.get_deviceinfo(tmp_hostname)
                if tmp_device_id == 0:
                    print '--------采购硬盘:hostname:%s,device_id:%s-------------'%(tmp_hostname,tmp_device_id)
                    histarget = StockHistory(target_id = tmp_target_id,num=tmp_row[3],device_id=0,type=1,content=tmp_hostname,created = tmp_row[10])
                    db.session.add(histarget)
                    db.session.commit()
                    continue
                histarget = StockHistory(target_id = tmp_target_id,num=tmp_row[3],device_id=tmp_device_id,type =1,created = tmp_row[10])
                db.session.add(histarget)
                db.session.commit()

        result = connection.execute("select *  from Hdisk_used") #报废
        for row in result:
            item = '%s#%s#%s#%s#3Gb/s'%(row[5].replace("TB","T"),row[3],row[4],row[6].replace("转/分",""))
            item = item.replace("#",self.separator)
            md5_item = hashlib.md5(item).hexdigest()
            tmp_model_id = model_dic[md5_item]
            tmp_count  =  row[2]
            hasIn = StockParts.query.filter(and_(StockParts.model_id == tmp_model_id,StockParts.status == 1, StockParts.type == StockParts.TYPE_DISK,)).first()
            if hasIn:
                tmp_target_id = hasIn.id
                hasIn.num = tmp_count + hasIn.num
                db.session.commit()
            else:
                target = StockParts(type=StockParts.TYPE_DISK, model_id = tmp_model_id, num = tmp_count,status = 1)
                db.session.add(target)
                db.session.commit()
                tmp_target_id = target.id
            tmp_hostname = row[1]
            tmp_device_id = self.get_deviceinfo(tmp_hostname)
            if tmp_device_id == 0:
                print '--------报废硬盘:hostname:%s,device_id:%s-------------'%(tmp_hostname,tmp_device_id)
                histarget = StockHistory(target_id = tmp_target_id,num=tmp_count,device_id=0,type=0,status = 1,content=tmp_hostname,created = row[7])
                db.session.add(histarget)
                db.session.commit()
                continue
            histarget = StockHistory(target_id = tmp_target_id,num=tmp_count,device_id = tmp_device_id,status = 1,type = 0,created = row[7])
            db.session.add(histarget)
            db.session.commit()

        connection.close()

    def mem(self):
        model_dic = {}
        model_lists = StockPartsModel.query.filter(StockPartsModel.type == StockPartsModel.TYPE_MEM).all()
        for item in model_lists:
            md5_item = hashlib.md5(item.content).hexdigest()
            model_dic[md5_item] = item.id

        engine = create_engine(PARTS_MIGRATE_DATABASE_URI, encoding='utf-8',echo=False)
        connection = engine.connect()
        result = connection.execute("select *  from Memory") #采购
        for row in result:#硬盘：容量/尺寸/接口/转速/接口速率
            item = '%s#%s#%s'%(row[3],row[4],row[5])
            item = item.replace("#",self.separator)
            md5_item = hashlib.md5(item).hexdigest()
            tmp_model_id = model_dic[md5_item]
            tmp_count  =  row[2]
            hasIn = StockParts.query.filter(and_(StockParts.type==StockParts.TYPE_MEM,StockParts.model_id == tmp_model_id,StockParts.status == 0)).first()
            if hasIn:
                tmp_target_id = hasIn.id
                hasIn.num = tmp_count + hasIn.num
                db.session.commit()
            else:
                target = StockParts(type=StockParts.TYPE_MEM, model_id = tmp_model_id, num = tmp_count,status = 0)
                db.session.add(target)
                db.session.commit()
                tmp_target_id = target.id
            histarget = StockHistory(target_id = tmp_target_id,num=tmp_count,created = row[9])
            db.session.add(histarget)
            db.session.commit()
            if hasIn:
                pass
            else:
                sql = "select *  from Memory_used where Type = '%s' and Capacity = '%s' and Frequency = '%s'"%(row[3],row[4],row[5])
                tmp_result = connection.execute(sql)
                for tmp_row in tmp_result:
                    tmp_hostname = tmp_row[6]
                    tmp_device_id = self.get_deviceinfo(tmp_hostname)
                    if tmp_device_id == 0:
                        print '--------采购内存:hostname:%s,device_id:%s-------------'%(tmp_hostname,tmp_device_id)
                        histarget = StockHistory(target_id = tmp_target_id,num=tmp_row[2],device_id=0,type=1,content=tmp_hostname,created = row[9])
                        db.session.add(histarget)
                        db.session.commit()
                        continue
                    histarget = StockHistory(target_id = tmp_target_id,num=tmp_row[2],device_id=tmp_device_id,type =1,created=row[9])
                    db.session.add(histarget)
                    db.session.commit()



    def get_deviceinfo(self,hostname):
        if hostname in self.humanmapping:
            hostname = self.humanmapping[hostname]
        device_id = 0
        info = Host.query.filter(Host.hostname == hostname).first()
        if info:
            if info.is_virtual:
                parent_info = Host.query.filter(Host.id == info.parent_id).first()
                if parent_info:
                    device_id = parent_info.device_id
            else:
                device_id = info.device_id
        return device_id