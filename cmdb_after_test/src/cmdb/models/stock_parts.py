# -*- coding: utf-8 -*-
from sqlalchemy.schema import Column
from sqlalchemy.types import Integer, String, TIMESTAMP
from application import db
from sqlalchemy.dialects.mysql import TINYINT
import datetime


class StockParts(db.Model):
    __tablename__ = "stock_parts"

    id       = Column(Integer, primary_key=True)
    type     = Column(TINYINT,nullable=False,index=True) #type=1 内存 type=2 硬盘
    model_id = Column(Integer,nullable=False,index=True) #对应型号表中id
    num      = Column(Integer,nullable=False)            #库存总数
    status   = Column(TINYINT,nullable=False,index=True) #状态：0 采购，1 报废
    created  = Column(TIMESTAMP, nullable=False,server_default='0000-00-00 00:00:00')
    updated  = Column(TIMESTAMP, nullable=False,server_default='0000-00-00 00:00:00')

    TYPE_MEM = 1
    TYPE_DISK = 2

    STATUS_BUY = 0
    STATUS_DISCARD = 1


    def __init__(self, type=0, model_id=0, num=0, status=0):
        self.type = type
        self.model_id = model_id
        self.num = num
        self.status = status
        self.created = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.updated = self.created

    @property
    def status_descri(self):
        if self.status == self.STATUS_BUY:
            return '采购入库'
        else:
            return '报废入库'

    @property
    def type_descri(self):
        if self.type == 1:
            return '内存'
        elif self.type == 2:
            return '硬盘'

