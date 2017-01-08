# -*- coding: utf-8 -*-

from sqlalchemy.schema import Column, Index
from sqlalchemy.types import Integer, String, Text, TIMESTAMP,DateTime,VARCHAR,BLOB
from sqlalchemy.dialects.mysql import TINYINT
from application import app
from application import db
from models.dns.dns_zone import DnsZone
from marshmallow import Schema,fields, ValidationError, pre_load
from models.user import Department,DepartmentSchema,User,UserSchema
from models.work import *
from models.pool import Pool,PoolSchema

class WorkRole(db.Model):
    __tablename__ = 'work_role'

    id = Column(Integer, primary_key=True)
    name = Column(String(40), nullable=False, index=True)
    description=Column(String(50), nullable=True, index=True)

class UserWorkRolemap(db.Model):
    _tablename__ = "user_worktask_map"

    id = db.Column(db.Integer, primary_key=True)
    user=db.relationship(User ,backref='UserWorkRolemaps')
    workrole=db.relationship(WorkRole ,backref='UserWorkRolemaps')
    user_id=db.Column(db.Integer, db.ForeignKey(User.id,ondelete='CASCADE'), nullable=False)
    workrole_id=db.Column(db.Integer, db.ForeignKey(WorkRole.id,ondelete='CASCADE'), nullable=False)

class WorkTaskRolemap(db.Model):
    _tablename__ = "worktask_role_map"

    id = db.Column(db.Integer, primary_key=True)
    role=db.relationship(WorkRole ,backref='WorkTaskRolemaps')
    task=db.relationship(WorkTaskTemplate ,backref='WorkTaskRolemaps')
    role_id=db.Column(db.Integer, db.ForeignKey(WorkRole.id,ondelete='CASCADE'), nullable=False)
    task_id=db.Column(db.Integer, db.ForeignKey(WorkTaskTemplate.id,ondelete='CASCADE'), nullable=False)

class WorkFileRolemap(db.Model):
    _tablename__ = "workfile_role_map"

    id = db.Column(db.Integer, primary_key=True)
    role=db.relationship(WorkRole ,backref='WorkFileRolemaps')
    workfile=db.relationship(WorkFile ,backref='WorkFileRolemaps')
    role_id=db.Column(db.Integer, db.ForeignKey(WorkRole.id,ondelete='CASCADE'), nullable=False)
    workfile_id=db.Column(db.Integer, db.ForeignKey(WorkFile.id,ondelete='CASCADE'), nullable=False)

class WorkPoolRolemap(db.Model):
    _tablename__ = "workpool_role_map"

    id = db.Column(db.Integer, primary_key=True)
    pool=db.relationship(Pool ,backref='WorkPoolRolemaps')
    role=db.relationship(WorkRole ,backref='WorkPoolRolemaps')

    role_id=db.Column(db.Integer, db.ForeignKey(WorkRole.id,ondelete='CASCADE'), nullable=False)
    pool_id=db.Column(db.Integer, db.ForeignKey(Pool.id,ondelete='CASCADE'), nullable=False)

class WorkUrl(db.Model):
    __tablename__ = 'work_url'

    id = Column(Integer, primary_key=True)
    url = Column(String(200), nullable=False, index=True)
    key=Column(String(50), nullable=True, index=True)
    type=Column(Integer,nullable=True) #1 page 2 operate 3 else
    description=Column(String(50), nullable=True, index=True)

class WorkRoleUrlmap(db.Model):
    _tablename__ = "workrole_url_map"

    id = db.Column(db.Integer, primary_key=True)
    work_role=db.relationship(WorkRole ,backref='WorkRoleUrlmaps')
    url=db.relationship(WorkUrl ,backref='WorkRoleUrlmaps')
    work_role_id=db.Column(db.Integer, db.ForeignKey(WorkRole.id,ondelete='CASCADE'), nullable=False)
    url_id=db.Column(db.Integer, db.ForeignKey(WorkUrl.id,ondelete='CASCADE'), nullable=False)

class WorkUrlSchema(Schema):
    class Meta:
        fields = ('id', 'url','key','type', 'description')

class WorkRoleSchema(Schema):
    class Meta:
        fields = ('id', 'name', 'description')

class UserWorkRolemapSchema(Schema):
    class Meta:
        fields = ('id', 'user_id', 'workrole_id','user','workrole')

    user=fields.Nested(UserSchema)
    workrole=fields.Nested(WorkRoleSchema)

class WorkPoolRolemapSchema(Schema):
    class Meta:
        fields = ('id', 'role_id', 'pool_id','pool','role')

    role=fields.Nested(WorkRoleSchema)
    pool=fields.Nested(PoolSchema)

class WorkFileRolemapSchema(Schema):
    class Meta:
        fields = ('id', 'role_id', 'workfile_id','workfile','role')

    role=fields.Nested(WorkRoleSchema)
    workfile=fields.Nested(WorkFileSchema)

class WorkTaskRolemapSchema(Schema):
    class Meta:
        fields = ('id', 'role_id', 'task_id','task','role')

    role=fields.Nested(WorkRoleSchema)
    task=fields.Nested(WorkTaskTemplateSchema)

class WorkRoleUrlmapSchema(Schema):
    class Meta:
        fields = ('id', 'work_role_id', 'url_id','url','work_role')

    url=fields.Nested(WorkUrlSchema)
    work_role=fields.Nested(WorkRoleSchema)