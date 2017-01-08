# -*- coding: utf-8 -*-
# author:郭威
# email: apanly@163.com
# QQ:364054110
from sqlalchemy.schema import Column, Index
from sqlalchemy import or_
from sqlalchemy.types import Integer, String, Text, TIMESTAMP,VARCHAR
from sqlalchemy.dialects.mysql import TINYINT
from application import app
from application import db
from models.dns.dns_zone import DnsZone
from marshmallow import Schema,fields, ValidationError, pre_load
from models.pool import Pool

class User(db.Model):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True)
    oauth_token = Column(String(40), nullable=False, index=True)
    oauth_id = Column(Integer, nullable=False, index=True)
    cn_name = Column(String(50), nullable=False,index=True)
    name = Column(String(50), nullable=False, index=True)
    employee_id = Column(String(10), nullable=False)
    email = Column(String(255), nullable=False)
    mobile = Column(String(11), nullable=False)
    superior_id = Column(Integer,nullable=False)
    p_level = Column(TINYINT(2),nullable=False)
    m_level = Column(TINYINT(2),nullable=False)
    department_id = Column(Integer,nullable=False)
    department_name = Column(String(50),nullable=False)
    function_id = Column(Integer,nullable=False,server_default='0')
    function_name = Column(String(50),nullable=False)
    status = Column(TINYINT(2),nullable=False,index=False,server_default='0')
    created = Column(TIMESTAMP, nullable=False,server_default='0000-00-00 00:00:00')
    updated = Column(TIMESTAMP, nullable=False,server_default='0000-00-00 00:00:00')

    def __init__(self, oauth_token, oauth_id,cn_name,name, employee_id, email, mobile,
                 status,created, updated,superior_id,p_level,m_level,department_id,department_name,function_id,function_name):
        self.oauth_token = oauth_token
        self.oauth_id = oauth_id
        self.cn_name=cn_name
        self.name = name
        self.employee_id = employee_id
        self.email = email
        self.mobile = mobile
        self.status = status
        self.created = created
        self.updated = updated
        self.superior_id = superior_id
        self.p_level = p_level
        self.m_level = m_level
        self.department_id = department_id
        self.department_name = department_name
        self.function_id = function_id
        self.function_name = function_name


    def get_id(self):
        return self.id


    def is_authenticated(self):
        return True


    def is_active(self):
        return True


    def is_anonymous(self):
        return False

    # @property
    # def is_user(self):
    #     if self.identity=='user':
    #         return True
    #     else:
    #         return False

    @property
    def is_admin(self):
        from sqlalchemy import and_
        from user_role import UserRole
        from role import Role
        roleinfo = Role.query.filter(Role.name=="超级管理员").first()
        if roleinfo:
            userrole = UserRole.query.filter(and_(UserRole.user_id == self.id,UserRole.role_id == roleinfo.id)).first()
            if userrole:
                return True
        return False

    @property
    def href_button(self):
        from views.functions import visible
        href_buton = {'datacenter':"/cmdb/datacenter_get",'rack':"/cmdb/rack_get",'supplier':"/cmdb/supplier_get",
                  'ip':'/cmdb/ip_get','device_cat':'/cmdb/device/category_get','device':'/cmdb/device_get',
                  'host':'/cmdb/host_get','pool':'/cmdb/pool_get','blacklist':'/cmdb/tools/blacklist_get',
                  'log':'/cmdb/bastion/apply_get','parts':'/cmdb/parts/memory_get','publish':'/cmdb/tools/publish_get',
                  'ldap':'/cmdb/ldapgroup_get','ldapdep':'/cmdb/ldapgroup/deplist_get','ldapgroup':'/cmdb/ldapgroup/grouplist_get',
                    'ldapsudo':'/cmdb/ldapgroup/sudolist_get','ldapsudouser':'/cmdb/ldapgroup/sudouser_get'}
        public_show = visible(href_buton)
        return public_show

    @property
    def hasAuthority(self):
        if 7 <= self.p_level < 99 or 4 <= self.m_level < 99:
            return True
        else:
            return False

    @property
    def host_approvaler(self):
        approver_uid = app.config.get("APPROVER")['host']
        if approver_uid == self.id:
            return True
        superior_info = User.query.filter(User.superior_id == self.id).first()
        if superior_info:
            return True
        else:
            return False

    @property
    def dns_approvaler(self):
        count = DnsZone.query.filter(self.id == DnsZone.uid).count()
        if count > 0:
            return True
        else:
            return False

    @property
    def is_sa(self):
        if self.department_id == 160:
            return True
        else:
            return False

    @property
    def identity(self):
        usergroup_info=Usergroupmap.query.filter_by(user_id=self.id).first()
        if usergroup_info:
            group_id=usergroup_info.group_id
            group_info=Group.query.filter_by(id=group_id).first()
            if group_info:
                department_id=group_info.department_id
                department_info=Department.query.filter_by(id=department_id).first()
                if department_id==5 and (self.id==department_info.leader_uid or self.id==department_info.bleader_uid):
                    return 'leader_ops'
                if self.id==department_info.leader_uid or self.id==department_info.bleader_uid:
                    return 'leader'
                if department_id==5:   #ops成员
                    return 'ops'
                else:
                    return 'user'
            else:
                return 'noGroup'
    @property
    def user_list(self):
        department_info=Department.query.filter(or_(Department.leader_uid==self.id,Department.bleader_uid==self.id)).first()
        if department_info:
            department_id=department_info.id
            group_info=Group.query.filter_by(department_id=department_id).all()
            if group_info:
                groupid_list=[]
                for item in group_info:
                    groupid_list.append(item.id)
                user_info= Usergroupmap.query.filter(Usergroupmap.group_id.in_(groupid_list)).all()
                userid_list=[]
                for item in user_info:
                    userid_list.append(item.user_id)
                return userid_list



class Department(db.Model):
    _tablename__ = "department"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    description=db.Column(db.String(255))
    leader_uid=db.Column(db.Integer,db.ForeignKey(User.id,ondelete='CASCADE'), nullable=False)
    bleader_uid=db.Column(db.Integer,db.ForeignKey(User.id,ondelete='CASCADE'), nullable=False)
    group=db.relationship('Group',backref='departments',cascade='all,delete')
    workFile=db.relationship('WorkFile',backref='departments',cascade='all,delete')


class Sudo(db.Model):
    _tablename__ = "sudo"

    id = db.Column(db.Integer, primary_key=True)
    cmd = db.Column(db.String(255))
    description=db.Column(db.String(255))
    sudousermap=db.relationship('Sudousermap',backref='Sudousermaps',cascade='all,delete')
    sudogroupmap=db.relationship('Sudogroupmap',backref='Sudogroupmaps',cascade='all,delete')

class Group(db.Model):
    _tablename__ = "group"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    description=db.Column(db.String(255))
    ldap_id=db.Column(db.String(255))
    department=db.relationship(Department, backref='groups')
    department_id=db.Column(db.Integer, db.ForeignKey(Department.id,ondelete='CASCADE'), nullable=False)
    usergroupmap=db.relationship('Usergroupmap',backref='Usergroupmaps',cascade='all,delete')
    sudogroupmap=db.relationship('Sudogroupmap',backref='Sudogroupmaps2',cascade='all,delete')

class Sudousermap(db.Model):
    _tablename__ = "sudousermap"

    id = db.Column(db.Integer, primary_key=True)
    user=db.relationship(User ,backref='Sudousermaps')
    sudo=db.relationship(Sudo ,backref='Sudousermaps')
    user_id=db.Column(db.Integer, db.ForeignKey(User.id,ondelete='CASCADE'), nullable=False)
    sudo_id=db.Column(db.Integer, db.ForeignKey(Sudo.id,ondelete='CASCADE'), nullable=False)

class Userpoolmap(db.Model):
    _tablename__ = "userpoolmap"

    id = db.Column(db.Integer, primary_key=True)
    user=db.relationship(User ,backref='Userpoolmapmaps')
    pool=db.relationship(Pool ,backref='Userpoolmapmaps')
    user_id=db.Column(db.Integer, db.ForeignKey(User.id,ondelete='CASCADE'), nullable=False)
    pool_id=db.Column(db.Integer, db.ForeignKey(Pool.id,ondelete='CASCADE'), nullable=False)

class Sudogroupmap(db.Model):
    _tablename__ = "sudogroupmap"

    id = db.Column(db.Integer, primary_key=True)
    group=db.relationship(Group ,backref='Sudogroupmaps')
    sudo=db.relationship(Sudo ,backref='Sudogroupmaps')
    group_id=db.Column(db.Integer, db.ForeignKey(Group.id,ondelete='CASCADE'), nullable=False)
    sudo_id=db.Column(db.Integer, db.ForeignKey(Sudo.id,ondelete='CASCADE'), nullable=False)

class Usergroupmap(db.Model):
    _tablename__ = "usergroupmap"

    id = db.Column(db.Integer, primary_key=True)
    user=db.relationship(User ,backref='Usergroupmaps')
    group=db.relationship(Group, backref='Usergroupmaps')
    user_id=db.Column(db.Integer, db.ForeignKey(User.id,ondelete='CASCADE'), nullable=False)
    group_id=db.Column(db.Integer, db.ForeignKey(Group.id,ondelete='CASCADE'), nullable=False)
    # @property

class UserSchema(Schema):
    id=fields.Int(dump_only=True)
    oauth_token = fields.Str()
    oauth_id = fields.Int()
    cn_name = fields.Str()
    name = fields.Str()
    employee_id = fields.Str()
    email = fields.Str()
    mobile = fields.Str()
    superior_id = fields.Int()
    p_level = fields.Int()
    m_level = fields.Int()
    department_id = fields.Int()
    department_name = fields.Str()
    function_id = fields.Int()
    function_name = fields.Str()
    status = fields.Int()
    created = fields.Time()
    updated = fields.Time()

class SudoSchema(Schema):
    id=fields.Int(dump_only=True)
    cmd = fields.Str()
    description= fields.Str()

class DepartmentSchema(Schema):
    id=fields.Int(dump_only=True)
    name = fields.Str()
    description= fields.Str()

class GroupSchema(Schema):
    id=fields.Int(dump_only=True)
    name = fields.Str()
    description= fields.Str()
    ldap_id=fields.Int()
    department_id=fields.Int()
    department=fields.Nested(DepartmentSchema)

class SudousermapSchema(Schema):
    id=fields.Int(dump_only=True)
    user=fields.Nested(UserSchema)
    sudo=fields.Nested(SudoSchema)
    user_id=fields.Int()
    sudo_id=fields.Int()

class SudogroupmapSchema(Schema):
    id=fields.Int(dump_only=True)
    group=fields.Nested(GroupSchema)
    sudo=fields.Nested(SudoSchema)
    group_id=fields.Int()
    sudo_id=fields.Int()

class UsergroupmapSchema(Schema):
    id=fields.Int(dump_only=True)
    user=fields.Nested(UserSchema)
    group=fields.Nested(GroupSchema)
    user_id=fields.Int()
    group_id=fields.Int()

