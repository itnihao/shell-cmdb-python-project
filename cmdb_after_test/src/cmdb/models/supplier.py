# -*- coding: utf-8 -*-
from sqlalchemy.schema import Column
from sqlalchemy.types import Integer, String, Text, TIMESTAMP
from application import db
from sqlalchemy.dialects.mysql import TINYINT
import datetime
from jinja2 import Markup

class Supplier(db.Model):
    __tablename__ = "supplier"

    id      = Column(Integer, primary_key=True)
    name    = Column(String(30),nullable=False)
    short_name  = Column(String(20),nullable=False)
    content = Column(Text,nullable=False)
    created = Column(TIMESTAMP, nullable=False,server_default='0000-00-00 00:00:00')
    updated = Column(TIMESTAMP, nullable=False,server_default='0000-00-00 00:00:00')


    def __init__(self, name=name, short_name=short_name,content=content):
        self.name = name
        self.short_name = short_name
        self.content = content
        self.created = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.updated = self.created
    @property
    def content_nr2br(self):
        return Markup(self.content.replace("\n","<br>"))