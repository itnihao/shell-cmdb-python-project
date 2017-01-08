# -*- coding: utf-8 -*-


from sqlalchemy.schema import Column
from sqlalchemy.types import Integer, String, Text, TIMESTAMP
from sqlalchemy.dialects.mysql import TINYINT,SMALLINT
from application import db
import datetime


class Host(db.Model):
    __tablename__ = "host"

    id              = Column(Integer, primary_key=True)
    hostname        = Column(String(25),nullable=False,index=True)
    primary_ip_id   = Column(Integer, nullable=False,index=True)
    type            = Column(TINYINT(2),nullable=False,index=True)
    is_virtual      = Column(TINYINT(1),nullable=False,index=True)
    parent_id       = Column(Integer, nullable=False)
    device_id       = Column(Integer, nullable=False)
    status          = Column(TINYINT(1), nullable=False,index=True)
    cpu             = Column(TINYINT(3),nullable=False,index=True)
    memory          = Column(SMALLINT,nullable=False,index=True)
    storage         = Column(Integer,nullable=False,index=True)
    note            = Column(String(255),nullable=False)
    deleted         = Column(TINYINT(1),nullable=False,index=True,server_default='0')
    search          = Column(Text, nullable=False)
    created         = Column(TIMESTAMP, nullable=False,server_default='0000-00-00 00:00:00')
    updated         = Column(TIMESTAMP, nullable=False,server_default='0000-00-00 00:00:00')


    TYPE_APP = 1
    TYPE_APC = 2
    TYPE_DB = 3
    TYPE_HADOOP=4

    DELETED_NO = 0
    DELETED_YES = 1

    IS_VIRTUAL_NO = 0
    IS_VIRTUAL_YES = 1

    STATUS_START=1  #裸机
    STATUS_READY=2  #可使用
    STATUS_ASSIGNED=3 #在pool 已分配
    STATUS_ONLINE=4  #上LB  已上线
    STATUS_OFFLINE=5  #已下线


    def __init__(self, hostname, primary_ip_id, type, is_virtual, parent_id, device_id, status, cpu, memory, storage, note, deleted=0, search=""):
        self.hostname      = hostname
        self.primary_ip_id = primary_ip_id
        self.type          = type
        self.is_virtual    = is_virtual
        self.parent_id     = parent_id
        self.device_id     = device_id
        self.status        = status
        self.cpu           = cpu
        self.memory        = memory
        self.storage       = storage
        self.note          = note
        self.deleted       = deleted
        self.search        = search
        self.created       =datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.updated       =self.created

    @property
    def status_descri(self):
        if self.status == self.STATUS_START:
           return  '初始化'
        elif self.status == self.STATUS_READY:
           return  '可使用'
        elif self.status==self.STATUS_ASSIGNED:
           return '已分配'
        elif self.status==self.STATUS_ONLINE:
           return '已上线'
        elif self.status==self.STATUS_OFFLINE:
           return '已下线'
        else :
           return  '未知'

    @property
    def virtual_descri(self):
        if self.is_virtual==1:
            return '是'
        else :
            return '否'

    @property
    def type_descri(self):
        if self.type==self.TYPE_APP:
            return 'APP'
        elif self.type==self.TYPE_APC:
            return 'APC'
        elif self.type==self.TYPE_DB:
            return 'DB'
        elif self.type==self.TYPE_HADOOP:
            return 'HADOOP'
        else:
            return 'other'

    @property
    def cpu_descri(self):
        if self.cpu == 0:
            return '未知'
        else:
            return '%sCore'%self.cpu

    @property
    def memory_descri(self):
        if self.memory == 0:
            return '未知'
        else:
            return '%sG'%self.memory

    @property
    def storage_descri(self):
        if self.storage == 0:
            return '未知'
        else:
            if self.storage >=1000:
                return '%sT'% int(self.storage/1000)
            else:
                return '%sG'%self.storage

    @property
    def detail_vir_desc(self):
        if self.is_virtual==1:
            return '(虚拟机)'
        else :
            return ''

    @property
    def cpu_info(self):
        if self.cpu !=0:
            return "%d" %self.cpu
        else:
            return "未知"

    @property
    def memory_info(self):
        if self.memory !=0:
            return "%dG" %self.memory
        else:
            return "未知"

    @property
    def storage_info(self):
        if self.storage !=0:
            return "%dG" %self.storage
        else:
            return "未知"

    @property
    def note_info(self):
        if self.note:
            return self.note
        else:
            return "未知"
