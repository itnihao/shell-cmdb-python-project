# -*- coding: utf-8 -*-
from sqlalchemy import *
from config import PARTS_MIGRATE_DATABASE_URI
from models.stock_parts_model import StockPartsModel
from application import app, db
import hashlib

class ModelMigrate:
    def run(self):
        db.engine.execute("truncate table stock_parts_model")
        engine = create_engine(PARTS_MIGRATE_DATABASE_URI, encoding='utf-8',echo=True)
        connection = engine.connect()
        result = connection.execute("select *  from Hdisk")
        md5items = []
        separator = ' / '
        if result:
            #硬盘：容量/尺寸/接口/转速/接口速率
            items = []
            for row in result:
                if int(row[3]) >= 1000:
                    tmp_row3 = '%dT'%int(int(row[3])/1000)
                else:
                    tmp_row3 = '%sG'%row[3]
                item = '%s#%s英寸#%s#%s#%sGb/s'%(tmp_row3,row[2],row[4],row[5],row[7])
                item = item.replace("#",separator)
                md5_item = hashlib.md5(item).hexdigest()
                if md5_item not in md5items:
                    md5items.append(md5_item)
                    items.append(item)

            if items:
                for item in items:
                    print item
                    target = StockPartsModel(type = StockPartsModel.TYPE_DISK,content = item)
                    db.session.add(target)
                    db.session.commit()

        result = connection.execute("select *  from Hdisk_used")
        if result:
            #硬盘：容量/尺寸/接口/转速/接口速率
            items = []
            for row in result:
                item = '%s#%s#%s#%s#3Gb/s'%(row[5].replace("TB","T"),row[3],row[4],row[6].replace("转/分",""))
                item = item.replace("#",separator)
                md5_item = hashlib.md5(item).hexdigest()
                if md5_item not in md5items:
                    md5items.append(md5_item)
                    items.append(item)

            if items:
                for item in items:
                    print item
                    target = StockPartsModel(type = StockPartsModel.TYPE_DISK,content = item)
                    db.session.add(target)
                    db.session.commit()


        result = connection.execute("select *  from Memory")
        md5items = []
        if result:
            items = []
            for row in result:
                item = '%s#%s#%s'%(row[3],row[4],row[5])
                item = item.replace("#",separator)
                md5_item = hashlib.md5(item).hexdigest()
                if md5_item not in md5items:
                    md5items.append(md5_item)
                    items.append(item)

            if items:
                for item in items:
                    print item
                    target = StockPartsModel(type = StockPartsModel.TYPE_MEM,content = item)
                    db.session.add(target)
                    db.session.commit()


        result = connection.execute("select *  from Memory_used")
        if result:
            items = []
            for row in result:
                item = '%s#%s#%s'%(row[3],row[4],row[5])
                item = item.replace("#",separator)
                md5_item = hashlib.md5(item).hexdigest()
                if md5_item not in md5items:
                    md5items.append(md5_item)
                    items.append(item)

            if items:
                for item in items:
                    print item
                    target = StockPartsModel(type = StockPartsModel.TYPE_MEM,content = item)
                    db.session.add(target)
                    db.session.commit()
        connection.close()
