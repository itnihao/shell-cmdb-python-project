# -*- coding: utf-8 -*-

from sqlalchemy.schema import Column,Index
from sqlalchemy.types import Integer, String, TIMESTAMP
from sqlalchemy.dialects.mysql import TINYINT, SMALLINT
from application import db
from flask_login import current_user
import datetime

class HostBastionApply(db.Model):

    __tablename__   = "host_bastion_apply"
    id              = Column(Integer,primary_key=True)
    uid             = Column(Integer,nullable=False)
    type            = Column(TINYINT(1),nullable=False) #host:1  pool:2
    host_id		    = Column(Integer,nullable=False)    #target_id(host/pool)
    role            = Column(TINYINT(1),nullable=False) #用户申请的权限,root:1,evans:2,readonly:3
    approve_uid     = Column(Integer,nullable=False) #当前审批人uid
    status          = Column(TINYINT(1),nullable=False) #申请状态 1:审批中,2:驳回,3:正在开通中,4:开通成功,5:开通失败
    days            = Column(SMALLINT,nullable=False) #申请有效期期限(单位:天)
    content         = Column(String(255),nullable=False)
    note            = Column(String(255),nullable=True)
    created         = Column(TIMESTAMP, nullable=False,server_default='0000-00-00 00:00:00')
    updated         = Column(TIMESTAMP, nullable=False,server_default='0000-00-00 00:00:00')
    __table_args__  = (Index('idx_uid_status', 'uid', 'status'),Index('idx_approve_uid','approve_uid'),)

    STATUS_APPROVING = 1
    STATUS_REJECT = 2
    STATUS_RUNNING = 3
    STATUS_SUCCESS = 4
    STATUS_FAIL = 5

    TYPE_HOST = 1
    TYPE_POOL = 2

    ROLE_ROOT = 1
    ROLE_EVANS = 2
    ROLE_READONLY = 3

    def __init__(self,uid,type,host_id,role,approve_uid,status,days,content,created=""):
        self.uid         = uid
        self.type        = type
        self.host_id     = host_id
        self.role        = role
        self.approve_uid = approve_uid
        self.status      = status
        self.days        = days
        self.content     = content
        if created:
            self.created = created
        else:
            self.created     = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.updated     = self.created


    @property
    def apply_status(self):
        if self.status == self.STATUS_APPROVING:
            return '审批中'
        elif self.status == self.STATUS_RUNNING :
            return '正在开通中'
        elif self.status == self.STATUS_SUCCESS:
            return  '开通成功'
        elif self.status == self.STATUS_REJECT:
            return '驳回'
        elif self.status == self.STATUS_FAIL:
            return '开通失败'

    @property
    def role_status(self):
        if self.role == self.ROLE_ROOT:
            return 'root'
        elif self.role == self.ROLE_EVANS:
            return 'evans'
        else:
            return 'readonly'
