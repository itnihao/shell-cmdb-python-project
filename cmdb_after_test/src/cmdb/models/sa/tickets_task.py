# -*- coding: utf-8 -*-
from sqlalchemy.schema import Column, Index
from sqlalchemy.types import Integer, TIMESTAMP, Text
from sqlalchemy.dialects.mysql import TINYINT
from application import db
import datetime

class Tickets_Task(db.Model):
    __tablename__ = "tickets_task"
    id          = Column(Integer, primary_key=True)
    uid         = Column(Integer, nullable=False)
    manage_uid  = Column(Integer, nullable=False)
    tickets_id  = Column(Integer, nullable=False)
    tickets_cat_id = Column(Integer, nullable=False)
    status      = Column(TINYINT(1),nullable=False)
    deleted     = Column(TINYINT(1),nullable=False)
    content     = Column(Text, nullable=False)
    created     = Column(TIMESTAMP, nullable=False,server_default='0000-00-00 00:00:00')
    updated     = Column(TIMESTAMP, nullable=False,server_default='0000-00-00 00:00:00')
    __table_args__  = (Index('idx_tickets_id_tickets_cat_id', 'tickets_id', 'tickets_cat_id'),)

    STATUS_CLOSED = 2
    STATUS_OPEN = 1
    DELETED_YES = 1
    DELETED_NO = 0

    def __init__(self,uid = 0, manage_uid = 0 , tickets_id = 0, tickets_cat_id = 0, status = 1, content = '', created = ''):
        self.uid  = uid
        self.manage_uid = manage_uid,
        self.tickets_id = tickets_id
        self.tickets_cat_id = tickets_cat_id
        self.status = status
        self.deleted = self.DELETED_NO
        self.content = content
        if created:
            self.created = created
        else:
            self.created = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.updated = self.created

    @property
    def status_desc(self):
        desc = '处理中'
        if self.status == 2:
            desc = '已关闭'
        return desc