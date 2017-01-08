# -*- coding: utf-8 -*-

from sqlalchemy.schema import Column
from sqlalchemy.types import Integer, TIMESTAMP, Text, String
from sqlalchemy.dialects.mysql import TINYINT
from application import db
import datetime

class Tickets_Category(db.Model):
    __tablename__ = "tickets_category"

    id = Column(Integer, primary_key=True)
    manage_uid = Column(Integer, nullable=False,index=True)
    name = Column(String(50), nullable=False)
    label = Column(String(50), nullable=False)
    template = Column(Text, nullable=False)
    created = Column(TIMESTAMP, nullable=False,server_default='0000-00-00 00:00:00')
    updated = Column(TIMESTAMP, nullable=False,server_default='0000-00-00 00:00:00')


    def __init__(self, manage_uid=0, name="", label="", template="",created=""):
        self.manage_uid = manage_uid
        self.name = name
        self.label = label
        self.template = template
        if created:
            self.created = created
        else:
            self.created = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.updated = self.created