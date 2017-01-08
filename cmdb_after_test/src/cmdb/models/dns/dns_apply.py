# -*- coding: utf-8 -*-

from sqlalchemy.schema import Column
from sqlalchemy.dialects.mysql import TINYINT
from sqlalchemy.types import Integer, String, TIMESTAMP
from application import db
import datetime

class DnsApply(db.Model):

    __tablename__ = "dns_apply"

    id              = Column(Integer, primary_key=True)
    prefix          = Column(String(50), nullable=False)
    zone_id         = Column(Integer, nullable=False) #域名后缀 对应域名表中id
    type            = Column(TINYINT, nullable=False) #记录类型 1：A记录，2：CNAME 3：MX 4：TXT
    value           = Column(String(50), nullable=False)
    uid             = Column(Integer, nullable=False)
    approve_uid     = Column(Integer, nullable=False)
    content         = Column(String(255), nullable=False)
    priority        = Column(TINYINT, nullable=False) #MX记录优先级 冗余字段
    status          = Column(TINYINT, nullable=False) #申请状态 1:审批中,2:驳回,3:正在开通中,4:开通成功,5:开通失败
    deleted         = Column(TINYINT, nullable=False)# 0：正常，1:已删除
    created         = Column(TIMESTAMP, nullable=False,server_default='0000-00-00 00:00:00')
    updated         = Column(TIMESTAMP, nullable=False,server_default='0000-00-00 00:00:00')
    ip_updated      = Column(TINYINT, nullable=False)

    DELETED_NO = 0
    DELETED_YES = 1

    TYPE_A = 1
    TYPE_CNAME = 2
    TYPE_MX = 3
    TYPE_TXT = 4

    STATUS_APPROVING = 1
    STATUS_REJECT = 2
    STATUS_RUNNING = 3
    STATUS_SUCCESS = 4
    STATUS_FAIL = 5

    def __init__(self,prefix,zone_id,type,value,uid,approve_uid,content,priority,status,deleted,ip_updated):
        self.prefix  = prefix
        self.zone_id = zone_id
        self.type    = type
        self.value   = value
        self.uid     = uid
        self.approve_uid = approve_uid
        self.content = content
        self.priority= priority
        self.status  = status
        self.deleted = deleted
        self.created = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.updated = self.created
        self.ip_updated = ip_updated

    @property
    def status_descri(self):
        if self.status==1:
            return '审批中'
        elif self.status==2:
            return '驳回'
        elif self.status==3:
            return '正在开通中'
        elif self.status==4:
            return '开通成功'
        else:
            return '失败'

    @property
    def type_descri(self):
        if self.type==1:
            return 'A'
        elif self.type==2:
            return 'CNAME'
        elif self.type==3:
            return 'MX'
        elif self.type==4:
            return 'TXT'
        else:
            return '未知'

def get_type(type):
    if type==1:
        return 'A'
    elif type==2:
        return 'CNAME'
    elif type==3:
        return 'MX'
    elif type==4:
        return 'TXT'
    else:
        return '未知'

def get_type_num(type):
    if type=='A':
        return 1
    elif type=='CNAME':
        return 2
    elif type=='MX':
        return 3
    elif type=='TXT':
        return 4
    else:
        return 0