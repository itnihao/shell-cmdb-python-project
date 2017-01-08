# -*- coding: utf-8 -*-
from sqlalchemy.schema import Column
from sqlalchemy.types import Integer, TIMESTAMP, Text
from sqlalchemy.dialects.mysql import TINYINT
from application import db
import datetime

class Order_Comments(db.Model):
    __tablename__ = "order_comments"
    id          = Column(Integer, primary_key=True)
    uid         = Column(Integer, nullable=False)
    order_id  = Column(Integer, nullable=False)
    content     = Column(Text, nullable=False)
    created     = Column(TIMESTAMP, nullable=False,server_default='0000-00-00 00:00:00')
    updated     = Column(TIMESTAMP, nullable=False,server_default='0000-00-00 00:00:00')

    def __init__(self,uid = 0 , order_id = 0, content = '', created = ''):
        self.uid = uid
        self.order_id = order_id
        self.content = content
        if created:
            self.created = created
        else:
            self.created = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.updated = self.created
