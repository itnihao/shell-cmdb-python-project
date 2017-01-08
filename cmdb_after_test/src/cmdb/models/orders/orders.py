# -*- coding: utf-8 -*-
from sqlalchemy.schema import Column
from sqlalchemy.types import Integer, TIMESTAMP,Text,VARCHAR
from sqlalchemy.dialects.mysql import TINYINT
from application import db
from models.orders.order_category import Order_Category
from models.user import User
import datetime

class Orders(db.Model):
    __tablename__ = "orders"
    id              = Column(Integer, primary_key=True)
    category_id     = db.Column(db.Integer,db.ForeignKey(Order_Category.id,ondelete='CASCADE'), nullable=False)
    applier_uid     = db.Column(db.Integer,db.ForeignKey(User.id,ondelete='CASCADE'), nullable=False)
    approver_uid    = db.Column(db.Integer,db.ForeignKey(User.id,ondelete='CASCADE'), nullable=False)
    title           = db.Column(VARCHAR(255),nullable=False)
    content         = db.Column(db.Text) #cont_info
    status          = Column(TINYINT(1),nullable=False)
    level           = Column(TINYINT(1),nullable=False)
    deleted         = Column(TINYINT(1),nullable=False)
    created         = Column(TIMESTAMP, nullable=False,server_default='0000-00-00 00:00:00')
    updated         = Column(TIMESTAMP, nullable=False,server_default='0000-00-00 00:00:00')

    def __init__(self, category_id=0, applier_uid=0,approver_uid=0, title="",content="", level=0, status=0, deleted=0, created="", updated=""):
        self.category_id =  category_id
        self.applier_uid = applier_uid
        self.approver_uid = approver_uid
        self.title = title
        self.content = content
        self.level = level
        self.status = status
        self.deleted=deleted
        if created:
            self.created = created
        else:
            self.created = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.updated = self.created

    @property
    def status_desc(self):
        desc = ''
        if self.status == 0:
            desc = '待认领'
        elif  self.status == 1:
            desc = '评估中'
        elif self.status==2:
             desc = 'ops待认领'
        elif  self.status == 3:
            desc = '处理中'
        elif  self.status == 4:
            desc = '完成'
        elif self.status == 5:
            desc = "驳回"
        return desc

    @property
    def level_desc(self):
        desc = ''
        if self.level == 0:
            desc = '默认'
        elif self.level == 1:
            desc = '中'
        elif  self.level == 2:
            desc = '高'
        return desc