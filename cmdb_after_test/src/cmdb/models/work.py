# -*- coding: utf-8 -*-
from sqlalchemy.schema import Column, Index
from sqlalchemy.types import Integer, String, Text, TIMESTAMP,DateTime,VARCHAR,BLOB
from sqlalchemy.dialects.mysql import TINYINT
from application import app
from application import db
from models.dns.dns_zone import DnsZone
from marshmallow import Schema,fields, ValidationError, pre_load
from user import Department,DepartmentSchema,User,UserSchema



class WorkType(db.Model):
    __tablename__ = 'work_type'

    id = Column(Integer, primary_key=True)
    name = Column(String(40), nullable=False, index=True)
    description=Column(String(50), nullable=True, index=True)

class WorkFile(db.Model):
    __tablename__ = 'work_file'

    id = Column(Integer, primary_key=True)
    name = Column(String(40), nullable=False, index=True)
    filename= Column(String(40), nullable=False, index=True)
    path=Column(String(50), nullable=False, index=True)
    description=Column(String(50), nullable=True, index=True)
    department=db.relationship(Department, backref='workFiles')
    department_id=db.Column(db.Integer, db.ForeignKey(Department.id,ondelete='CASCADE',onupdate='CASCADE'), nullable=False)
    workType=db.relationship(WorkType, backref='WorkFiles')
    workType_id=db.Column(db.Integer, db.ForeignKey(WorkType.id,ondelete='CASCADE',onupdate='CASCADE'), nullable=False)

class WorkTaskTemplate(db.Model):
    __tablename__ = 'work_task_template'
    id = Column(Integer, primary_key=True)
    name = Column(String(40), nullable=False, index=True)
    update_time= Column(DateTime, nullable=True)
    user=db.relationship(User ,backref='TaskTemplateusermaps')
    user_id=db.Column(db.Integer, db.ForeignKey(User.id,ondelete='CASCADE'), nullable=False)
    info_ext=Column(VARCHAR(65532), nullable=False, index=True)

class WorkTask(db.Model):
    __tablename__ = 'work_task'
    id = Column(Integer, primary_key=True)
    name = Column(String(40), nullable=False, index=True)
    log= Column(VARCHAR(65532), nullable=False, index=True)
    state=Column(db.Integer) #0-失败 1-成功 2-正在执行
    scripts_ext=Column(String(255), nullable=True, index=True)
    machines_ext=Column(String(255), nullable=True, index=True)
    start_time= Column(DateTime, nullable=True)
    end_time= Column(DateTime, nullable=True)
    user=db.relationship(User ,backref='WorkTaskusermaps')
    user_id=db.Column(db.Integer, db.ForeignKey(User.id,ondelete='CASCADE'), nullable=False)
    info_ext=Column(VARCHAR(65532), nullable=False, index=True)
    task_id=Column(String(40), nullable=False, index=True)

    template_id=db.Column(db.Integer)


class WorkTypeSchema(Schema):
    id=fields.Int(dump_only=True)
    name = fields.Str()
    description= fields.Str()

class WorkFileSchema(Schema):
    id=fields.Int(dump_only=True)
    name = fields.Str()
    description= fields.Str()
    filename=fields.Str()
    path=fields.Str()
    workType_id=fields.Int()
    workType=fields.Nested(WorkTypeSchema)
    department_id=fields.Int()
    department=fields.Nested(DepartmentSchema)

class WorkTaskSchema(Schema):
    class Meta:
        fields = ('id', 'name', 'log', 'state', 'scripts_ext', 'machines_ext', 'start_time', 'end_time','user_id', 'info_ext', 'task_id','user','template_id')

    # id=fields.Int(dump_only=True)
    # name = fields.Str()
    # log= fields.Str()
    # state=fields.Int() #0-失败 1-成功 2-正在执行
    # scripts_ext=fields.Str()
    # machines_ext=fields.Str()
    start_time= fields.DateTime(format='%Y-%m-%d %H:%M:%S')
    end_time= fields.DateTime(format='%Y-%m-%d %H:%M:%S')
    user=fields.Nested(UserSchema)
    # user_id=fields.Int()
    # info_ext=fields.Str()
    # task_id=fields.Str()

class WorkTaskTemplateSchema(Schema):
    class Meta:
        fields = ('id', 'name', 'update_time','user_id', 'info_ext','user')
    update_time= fields.DateTime(format='%Y-%m-%d %H:%M:%S')
    user=fields.Nested(UserSchema)
