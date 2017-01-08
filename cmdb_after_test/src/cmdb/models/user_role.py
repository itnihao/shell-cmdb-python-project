# -*- coding: utf-8 -*-

from sqlalchemy.schema import Column
from sqlalchemy.types import Integer,TIMESTAMP
from sqlalchemy import UniqueConstraint
from application import db
import datetime

class UserRole(db.Model):

    __tablename__ = "user_role"

    id              = Column(Integer, primary_key=True)
    user_id         = Column(Integer,nullable=False,index=True)
    role_id         = Column(Integer,nullable=False,server_default='0')
    created         = Column(TIMESTAMP, nullable=False,server_default='0000-00-00 00:00:00')
    updated         = Column(TIMESTAMP, nullable=False,server_default='0000-00-00 00:00:00')
    __table_args__ = (
        UniqueConstraint("user_id", "role_id"),
    )

    def __init__(self,user_id,role_id):
        self.user_id = user_id
        self.role_id = role_id
        self.created=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.updated = self.created
