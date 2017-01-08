# -*- coding: utf-8 -*-

from sqlalchemy.schema import Column
from sqlalchemy.types import Integer, String, TIMESTAMP
from application import db
import datetime

class Role(db.Model):

    __tablename__ = "role"

    id              = Column(Integer, primary_key=True)
    name            = Column(String(60), nullable=False,index=True)
    created         = Column(TIMESTAMP, nullable=False,server_default='0000-00-00 00:00:00')
    updated         = Column(TIMESTAMP, nullable=False,server_default='0000-00-00 00:00:00')


    def __init__(self,name,updated):
        self.name = name
        self.created=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.updated = updated
