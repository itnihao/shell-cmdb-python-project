# -*- coding: utf-8 -*-


from sqlalchemy.schema import Column
from sqlalchemy.types import Integer, String, Text, TIMESTAMP
from sqlalchemy.dialects.mysql import TINYINT
from application import db
import datetime
from marshmallow import Schema,fields, ValidationError, pre_load
# from models.user import Department

class Pool(db.Model):
    __tablename__ = "pool"

    id         = Column(Integer, primary_key=True)
    name       = Column(String(40),nullable=False)
    byname     = Column(String(40),nullable=False)
    ops_owner  = Column(Integer,nullable=False)
    team_owner = Column(Integer,nullable=False)
    biz_owner  = Column(Integer,nullable=False)
    content    = Column(String(255),nullable=False)
    note       = Column(Text,nullable=False)
    auto_chooses = Column(String(255),nullable=False)
    deleted    = Column(TINYINT(1),nullable=False,index=True,server_default='0')
    source     = Column(TINYINT(3), nullable=True)
    search     = Column(Text, nullable=False)
    created    = Column(TIMESTAMP, nullable=False,server_default='0000-00-00 00:00:00')
    updated    = Column(TIMESTAMP, nullable=False,server_default='0000-00-00 00:00:00')


    # department=db.relationship('Department', backref='pools')
    department_id=db.Column(db.Integer)

    DELETED_NO = 0
    DELETED_YES = 1
    department=''

    def __init__(self,name,ops_owner,team_owner,biz_owner,note=note,content=content,auto_chooses='',byname='',source=0,search='',department_id=0):
        self.name       = name
        self.byname       = byname
        self.ops_owner  = ops_owner
        self.team_owner = team_owner
        self.biz_owner  = biz_owner
        self.content    = content
        self.note       = note
        self.auto_chooses = auto_chooses
        self.source = source
        if search!='':
            self.search = search
        self.created    = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.updated    = self.created
        # self.department=department
        self.department_id=department_id

    @property
    def source_desc(self):
        desc = ''
        if self.source == 1:
            desc = "KFS"
        elif self.source == 2:
            desc = "USER"
        elif self.source == 3:
            desc = "BROKER"
        elif self.source == 4:
            desc = "OTHER"
        elif self.source == 5:
            desc = "PUBLIC"
        elif self.source == 6:
            desc = "BI"
        elif self.source == 7:
            desc = "OPS"
        elif self.source == 8:
            desc = "INNER"
        elif self.source == 9:
            desc = "DB"

        return desc

class PoolSchema(Schema):
    class Meta:
        fields = ('id', 'name', 'ops_owner','team_owner', 'biz_owner', 'department_id','department')
