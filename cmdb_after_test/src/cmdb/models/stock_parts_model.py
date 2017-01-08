# -*- coding: utf-8 -*-
from sqlalchemy.schema import Column
from sqlalchemy.types import Integer, String, TIMESTAMP
from application import db
from sqlalchemy.dialects.mysql import TINYINT
import datetime


class StockPartsModel(db.Model):
    __tablename__ = "stock_parts_model"

    id      = Column(Integer, primary_key=True)
    type    = Column(TINYINT,nullable=False,index=True) #type=1 内存 type=2 硬盘
    content = Column(String(255),nullable=False) #型号详情
    created = Column(TIMESTAMP, nullable=False,server_default='0000-00-00 00:00:00')
    updated = Column(TIMESTAMP, nullable=False,server_default='0000-00-00 00:00:00')

    TYPE_MEM = 1
    TYPE_DISK = 2


    def __init__(self, type=0, content=''):
        self.type = type
        self.content = content
        self.created = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.updated = self.created


    def memory_desc(self):
        desc = {}
        desc['model'] = {'0':'DDR1','1':'DDR2','2':'DDR3'}  #类型
        desc['storage'] = {'0':'512M','1':'1G','2':'2G','3':'4G','4':'8G','5':'16G'}  #容量
        desc['frequency'] = {'0':'2100R','1':'5300F','2':'8500E','3':'8500R','4':'10600R'}  #工作频率
        return desc

    def disk_desc(self):
        desc = {}
        desc['size'] = {'0':'1.8英寸','1':'2.5英寸','2':'3.5英寸','3':'5.25英寸'}  #尺寸
        desc['storage'] = {'0':'146G','1':'300G','2':'480G','3':'500G','4':'600G','5':'800G','6':'1T','7':'2T'}  #容量
        desc['interface'] = {'0':'SAS','1':'SATA','2':'HDD','3':'PCIE','4':'SSD'}  #接口
        desc['speed'] = {'0':'4500','1':'5400','2':'7200','3':'10000','4':'15000'}  #转速
        desc['if_rate'] = {'0':'3Gb/s','1':'6Gb/s','2':'12Gb/s','3':'40Gb/s'}  #接口速率
        return desc
