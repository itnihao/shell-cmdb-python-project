# -*- coding: utf-8 -*-

from sqlalchemy.schema import Column
from sqlalchemy.types import Integer, String, TIMESTAMP
from application import db
import datetime

class Action(db.Model):

    __tablename__ = "action"

    id              = Column(Integer, primary_key=True)
    url             = Column(String(60), nullable=False,index=True)
    content         = Column(String(255), nullable=False,server_default='')
    method          = Column(String(25), nullable=False)
    tag             = Column(String(25), nullable=False,index=True)
    created         = Column(TIMESTAMP, nullable=False,server_default='0000-00-00 00:00:00')
    updated         = Column(TIMESTAMP, nullable=False,server_default='0000-00-00 00:00:00')


    def __init__(self,url,content,method,tag):
        self.url     = url
        self.content = content
        self.method  = method
        self.tag     = tag
        self.created = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.updated = self.created