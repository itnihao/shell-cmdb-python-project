# -*- coding: utf-8 -*-
from flask_login import current_user
from sqlalchemy.schema import Column, Index
from sqlalchemy.types import Integer, TIMESTAMP, String
from sqlalchemy.dialects.mysql import TINYINT
from application import db
import datetime


class StockHistory(db.Model):
    __tablename__ = "stock_history"

    id        = Column(Integer, primary_key=True)
    target_id = Column(Integer,nullable=False)            #对应关系表中id
    device_id = Column(Integer,nullable=False,default=0)  #默认0，重新购买的为0 机器归还重新入库的关联设备id
    num       = Column(Integer,nullable=False)            #入库数量
    status    = Column(TINYINT,nullable=False) #状态：0 采购，1 报废
    type      = Column(TINYINT,nullable=False) #动作：0 入库，1 出库
    content   = Column(String(255),nullable=False)        #备注
    uid       = Column(Integer,nullable=False)
    created   = Column(TIMESTAMP, nullable=False,server_default='0000-00-00 00:00:00')
    updated   = Column(TIMESTAMP, nullable=False,server_default='0000-00-00 00:00:00')
    __table_args__  = (Index('idx_status_type', 'status', 'type'),)

    STATUS_BUY = 0
    STATUS_DISCARD = 1

    TYPE_IN = 0
    TYPE_OUT = 1


    def __init__(self, target_id=0, device_id=0, num=0, status=0, type=0,uid =0, content='',created=''):
        self.target_id = target_id
        self.device_id = device_id
        self.num = num
        self.status = status
        self.type = type
        self.content = content
        self.uid = uid
        if created == '' or created == 'NULL':
            self.created = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        else:
            self.created = created
        self.updated = self.created

    @property
    def status_descri(self):
        if self.status == self.STATUS_BUY:
            return '采购入库'
        else:
            return '报废入库'
