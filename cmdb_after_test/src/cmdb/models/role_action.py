# -*- coding: utf-8 -*-

from sqlalchemy.schema import Column
from sqlalchemy.types import Integer, TIMESTAMP
from sqlalchemy import UniqueConstraint
from application import db
import datetime

class RoleAction(db.Model):

    __tablename__ = "role_action"

    id              = Column(Integer, primary_key=True)
    action_id       = Column(Integer, nullable=False)
    role_id         = Column(Integer, nullable=False)
    created         = Column(TIMESTAMP, nullable=False,server_default='0000-00-00 00:00:00')
    updated         = Column(TIMESTAMP, nullable=False,server_default='0000-00-00 00:00:00')
    __table_args__ = (
        UniqueConstraint("action_id", "role_id"),
    )


    def __init__(self,action_id,role_id):
        self.action_id = action_id
        self.role_id   = role_id
        self.created   = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.updated   = self.created