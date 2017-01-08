# -*- coding: utf-8 -*-

from sqlalchemy.schema import Column
from sqlalchemy.types import Integer,TIMESTAMP,SMALLINT
from application import db
from flask_login import current_user
import datetime
class Alarm(db.Model):

    __tablename__ = "alarm"

    id              = Column(Integer, primary_key=True)
    uid             = Column(Integer, nullable=False,index=True)
    type            = Column(SMALLINT,nullable=False,index=True)
    target_id       = Column(Integer,nullable=False,index=True)
    created         = Column(TIMESTAMP, nullable=False,server_default='0000-00-00 00:00:00')
    updated         = Column(TIMESTAMP, nullable=False,server_default='0000-00-00 00:00:00')

    TYPE_HOST = 2
    TYPE_POOL = 1

    def __init__(self, type, target_id, uid = 0):
        self.uid = uid
        self.type = type
        self.target_id = target_id
        self.created = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.updated = self.created
