# -*- coding: utf-8 -*-
from sqlalchemy.schema import Column
from sqlalchemy.types import Integer, String, TIMESTAMP
from sqlalchemy.dialects.mysql import TINYINT
from application import db
import datetime

class Apply(db.Model):
    __tablename__ = "apply"

    id              = Column(Integer, primary_key=True)
    uid             = Column(Integer, nullable=False)
    approver_uid    = Column(Integer, nullable=False,index=True)
    pool_id         = Column(Integer, nullable=False)
    type            = Column(TINYINT(1), nullable=False)
    idc             = Column(TINYINT(1), nullable=False)
    num             = Column(Integer, nullable=False)
    template        = Column(String(255), nullable=False)
    content         = Column(String(255), nullable=False)
    note         = Column(String(255), nullable=True)
    status          = Column(TINYINT(1), nullable=False)
    created         = Column(TIMESTAMP, nullable=False,server_default='0000-00-00 00:00:00')
    updated         = Column(TIMESTAMP, nullable=False,server_default='0000-00-00 00:00:00')

    def __init__(self, uid=0, approver_uid=0, pool_id=0, type=1, idc=1, num=1, template="", content="", note="",status=1, created=""):
        self.uid = uid
        self.approver_uid = approver_uid
        self.pool_id = pool_id
        self.type = type
        self.idc = idc
        self.num = num
        self.template = template
        self.content = content
        self.status = status
        self.note=note
        if created:
            self.created = created
        else:
            self.created = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.updated = self.created


    STATUS_APPROVING = 1
    STATUS_REJECT = 2
    STATUS_RUNNING = 3
    STATUS_SUCCESS = 4
    STATUS_FAIL = 5

    @property
    def type_desc(self):
        if self.type == 1:
            desc = "物理机"
        elif self.type == 2:
            desc = "虚拟机"
        return desc


    @property
    def idc_desc(self):
        desc = ''
        if self.idc == 1:
            desc = "IDC10"
        elif self.idc == 3:
            desc = "IDC20"
        return desc

    @property
    def status_desc(self):
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


    def host_type_desc(self):              #主机类型
        desc = {'1': "物理机",'2': "虚拟机"}
        return desc

    def os_type_desc(self):               #机房
        desc = {}
        desc['ubuntu']=["ubuntu-12.04", "ubuntu-14.04"]
        desc['centos']=["centos-5.5", "centos6.5", "centos7.0"]
        return desc
