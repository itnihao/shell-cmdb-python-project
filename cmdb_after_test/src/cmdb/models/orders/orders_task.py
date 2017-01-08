# -*- coding: utf-8 -*-
from sqlalchemy.schema import Column, Index
from sqlalchemy.types import Integer, TIMESTAMP, Text
from sqlalchemy.dialects.mysql import TINYINT
from application import db
from models.user import User
from models.orders.orders import Orders
import datetime

class Orders_Task(db.Model):
    __tablename__ = "orders_task"
    id          = Column(Integer, primary_key=True)
    tickets_id  = Column(Integer, db.ForeignKey(Orders.id,ondelete='CASCADE'),nullable=False)
    uid         = Column(Integer, db.ForeignKey(User.id,ondelete='CASCADE'),nullable=False)
    operation   = Column(Text, nullable=False)
    created     = Column(TIMESTAMP,nullable=False,server_default='0000-00-00 00:00:00')
    updated     = Column(TIMESTAMP, nullable=False,server_default='0000-00-00 00:00:00')


    def __init__(self,uid=0, tickets_id=0,  operation='', created='', updated=''):
        self.uid  = uid
        self.tickets_id = tickets_id
        self.operation = operation
        if created:
            self.created = created
        else:
            self.created = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.updated =  self.created
