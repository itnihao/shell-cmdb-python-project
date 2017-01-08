# -*- coding: utf-8 -*-

from sqlalchemy.schema import Column, Index
from sqlalchemy.types import Integer, TIMESTAMP, String,TEXT
from sqlalchemy.dialects.mysql import TINYINT
from application import db
from flask_login import current_user
import datetime

class MailQueue(db.Model):

    __tablename__   = "mail_queue"
    id              = Column(Integer,primary_key=True)
    email           = Column(String(255),nullable=False)
    subject         = Column(String(255),nullable=False)
    content         = Column(TEXT,nullable=False)
    status          = Column(TINYINT(1),nullable=False) #状态默认值0,0:未运行,1:执行成功 2:执行失败
    created         = Column(TIMESTAMP, nullable=False,server_default='0000-00-00 00:00:00')
    updated         = Column(TIMESTAMP, nullable=False,server_default='0000-00-00 00:00:00')
    __table_args__  = (Index('idx_status','status'),)

    STATUS_FREE = 0
    STATUS_SUCCESS = 1
    STATUS_FAIL = 2

    def __init__(self,email,subject,content,status):
        self.email       = email
        self.subject     = subject
        self.content     = content
        self.status      = status
        self.created     = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.updated     = self.created


