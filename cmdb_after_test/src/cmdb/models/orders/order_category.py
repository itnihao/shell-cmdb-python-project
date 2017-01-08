# -*- coding: utf-8 -*-
from application import db
from sqlalchemy.schema import Column
from sqlalchemy.types import Integer, String,Text ,TIMESTAMP
from sqlalchemy.dialects.mysql import TINYINT
import datetime


class Order_Category(db.Model):
    __tablename__ = "order_category"

    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    type_id = Column(Integer,nullable=False)
    uid = Column(Integer,nullable=False)
    dec = Column(Text,nullable=False)
    deleted = Column(TINYINT(1), nullable=False)
    created     = Column(TIMESTAMP, nullable=False,server_default='0000-00-00 00:00:00')
    updated     = Column(TIMESTAMP, nullable=False,server_default='0000-00-00 00:00:00')


    def __init__(self, name="", type_id=0, uid=0, dec="",deleted=0 ,created="", updated=""):
        self.name=name
        self.type_id=type_id
        self.uid=uid
        self.dec=dec
        self.deleted=deleted
        if created:
            self.created = created
        else:
            self.created = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.updated = updated
