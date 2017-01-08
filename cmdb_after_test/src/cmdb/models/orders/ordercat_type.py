# -*- coding: utf-8 -*-
from application import db
from sqlalchemy.schema import Column
from sqlalchemy.dialects.mysql import TINYINT
from sqlalchemy.types import Integer, String, TIMESTAMP
import datetime

class Ordercat_Type(db.Model):
    __tablename__ = "ordercat_type"
    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    deleted = Column(TINYINT(1), nullable=False)
    created     = Column(TIMESTAMP, nullable=False,server_default='0000-00-00 00:00:00')
    updated     = Column(TIMESTAMP, nullable=False,server_default='0000-00-00 00:00:00')


    def __init__(self, name="" ,deleted=0,created="",updated=""):
        self.name=name
        self.deleted=deleted
        if created:
            self.created = created
        else:
            self.created = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.updated = self.updated
