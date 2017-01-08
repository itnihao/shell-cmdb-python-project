# -*- coding: utf-8 -*-


from sqlalchemy.schema import Column
from sqlalchemy.types import Integer, String, Text, TIMESTAMP
from sqlalchemy.dialects.mysql import TINYINT
from application import db
import datetime


class Jobplat(db.Model):
    __tablename__ = "jobplat"


    id             = Column(Integer, primary_key=True)
    job_name       = Column(String(60), nullable=False)
    upload_type    = Column(TINYINT(1), nullable=False)     #  1:manual  2:local
    script_name    = Column(String(60), nullable=False)
    script_type    = Column(TINYINT(1), nullable=False)     #  1:shell   2:python   3:perl
    script_content = Column(Text, nullable=False)
    target_type    = Column(TINYINT(1), nullable=False)     #  1:主机      2:POOL
    target_id      = Column(String(255), nullable=False)    #  host_ids或者pool_id
    run_user       = Column(TINYINT(1), nullable=False)     #  1:root  2:evans
    status         = Column(TINYINT(1), nullable=False)     #  0:未执行  1:执行成功 2:执行失败
    created        = Column(TIMESTAMP, nullable=False,server_default='0000-00-00 00:00:00')
    updated        = Column(TIMESTAMP, nullable=False,server_default='0000-00-00 00:00:00')



    TYPE_SHELL = 1
    TYPE_PYTHON = 2
    TYPE_PERL = 3


    RUN_ROOT = 1
    RUN_EVANS = 2


    UPLOAD_MANUAL = 1
    UPLOAD_LOCAL = 2

    STATUS_FREE = 0
    STATUS_SUCCESS = 1
    STATUS_FAIL = 2


    def __init__(self,job_name,upload_type,script_name,script_type,script_content,target_type,target_id,run_user,status,created=""):
        self.job_name         = job_name
        self.upload_type      = upload_type
        self.script_name      = script_name
        self.script_type      = script_type
        self.script_content   = script_content
        self.target_type      = target_type
        self.target_id        = target_id
        self.run_user         = run_user
        self.status           = status
        if created:
            self.created = created
        else:
            self.created     = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.updated     = self.created

    @property
    def user_status(self):
        if self.run_user == self.RUN_ROOT:
            return 'root'
        elif self.run_user == self.RUN_EVANS:
            return 'evans'


    @property
    def scripts_type(self):
        if self.script_type == self.TYPE_SHELL:
            return 'shell'
        elif self.script_type == self.TYPE_PYTHON:
            return 'python'
        elif self.script_type == self.TYPE_PERL:
            return 'perl'

    @property
    def upload(self):
        if self.upload_type == self.UPLOAD_MANUAL:
            return '手动录入'
        elif self.upload_type == self.UPLOAD_LOCAL:
            return '本地上传'