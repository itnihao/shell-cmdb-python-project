# -*- coding: utf-8 -*-

from sqlalchemy.schema import Column, Index
from sqlalchemy.types import Integer, TIMESTAMP
from sqlalchemy.dialects.mysql import TINYINT
from application import db
from flask_login import current_user
import datetime

class PubkeyChangedQueue(db.Model):

    __tablename__   = "pubkey_changed_queue"
    id              = Column(Integer,primary_key=True)
    uid             = Column(Integer,nullable=False)
    bastion_host_flag  = Column(TINYINT(1),nullable=False,index=True) #堡垒机是否跑了,默认0 ，1表示执行了
    my_host_flag    = Column(TINYINT(1),nullable=False,index=True) #我的主机是否同步 默认0,1表示执行了
    created         = Column(TIMESTAMP, nullable=False,server_default='0000-00-00 00:00:00')
    updated         = Column(TIMESTAMP, nullable=False,server_default='0000-00-00 00:00:00')




    def __init__(self,uid):
        self.uid         = uid
        self.bastion_host_flag     = 0
        self.my_host_flag          = 0
        self.created     = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.updated     = self.created