# -*- coding: utf-8 -*-

from sqlalchemy.schema import Column, Index
from sqlalchemy.types import Integer, TIMESTAMP
from sqlalchemy.dialects.mysql import TINYINT
from application import db
from flask_login import current_user
import datetime

class HostBastionTasks(db.Model):

    __tablename__   = "host_bastion_tasks"
    id              = Column(Integer,primary_key=True)
    apply_id        = Column(Integer,nullable=False)
    uid             = Column(Integer,nullable=False)
    host_id		    = Column(Integer,nullable=False)
    role            = Column(TINYINT(1),nullable=False) #用户申请的权限,root:1,evans:2,readonly:3
    type            = Column(TINYINT(1),nullable=False) #类型:默认值1,1:新增  2:删除
    status          = Column(TINYINT(1),nullable=False) #状态默认值0,0:未运行,1:执行成功 2:执行失败
    exec_time       = Column(TIMESTAMP, nullable=False,server_default='0000-00-00 00:00:00')
    created         = Column(TIMESTAMP, nullable=False,server_default='0000-00-00 00:00:00')
    updated         = Column(TIMESTAMP, nullable=False,server_default='0000-00-00 00:00:00')
    __table_args__  = (Index('idx_status','status'),)

    STATUS_FREE = 0
    STATUS_SUCCESS = 1
    STATUS_FAIL = 2

    TYPE_ADD = 1
    TYPE_DELETE = 2


    def __init__(self,apply_id,uid,host_id,role,type,status,exec_time):
        self.apply_id    = apply_id
        self.uid         = uid
        self.host_id     = host_id
        self.role        = role
        self.type        = type
        self.status      = status
        self.exec_time   = exec_time
        self.created     = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.updated     = self.created

