# -*- coding: utf-8 -*-

from sqlalchemy.schema import Column, Index
from sqlalchemy.types import Integer, TIMESTAMP
from sqlalchemy.dialects.mysql import TINYINT
from application import db
from flask_login import current_user
import datetime

class UserHost(db.Model):

    __tablename__   = "user_host"
    id              = Column(Integer,primary_key=True)
    uid             = Column(Integer,nullable=False)
    host_id		    = Column(Integer,nullable=False)
    role            = Column(TINYINT(1),nullable=False) #用户申请的权限,root:1,evans:2,readonly:3
    status          = Column(TINYINT(1),nullable=False) #status 默认1 1:有效,2表示过期
    created         = Column(TIMESTAMP, nullable=False,server_default='0000-00-00 00:00:00')
    updated         = Column(TIMESTAMP, nullable=False,server_default='0000-00-00 00:00:00')
    __table_args__  = (Index('idx_uid_host_role','uid','host_id','role'),)


    STATUS_VALID = 1
    STATUS_OVERDUE = 2


    ROLE_ROOT = 1
    ROLE_EVANS = 2
    ROLE_READONLY = 3


    def __init__(self,uid,host_id,role,status,created=""):
        self.uid         = uid
        self.host_id     = host_id
        self.role        = role
        self.status      = status
        if created:
            self.created = created
        else:
            self.created     = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.updated     = self.created


    @property
    def myhost_status(self):
        if self.status == self.STATUS_OVERDUE:
            return '过期'
        else:
            return  '有效'


    @property
    def role_status(self):
        if self.role == self.ROLE_ROOT:
            return 'root'
        elif self.role == self.ROLE_EVANS:
            return 'evans'
        else:
            return 'readonly'
