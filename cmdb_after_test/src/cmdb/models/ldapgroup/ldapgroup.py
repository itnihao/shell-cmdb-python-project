from flask import url_for
from application import db,app
from flask_sqlalchemy import SQLAlchemy
# from flask_marshmallow import Marshmallow
from marshmallow import Schema,fields, ValidationError, pre_load
from  models import User

def dump_datetime(value):
    """Deserialize datetime object into string form for JSON processing."""
    if value is None:
        return None
    return [value.strftime("%Y-%m-%d"), value.strftime("%H:%M:%S")]

# ma = Marshmallow(app)


# class Department(db.Model):
#     _tablename__ = "department"
#
#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String(255))
#     description=db.Column(db.String(255))
#
# class Group(db.Model):
#     _tablename__ = "group"
#
#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String(255))
#     description=db.Column(db.String(255))
#     ldap_id=db.Column(db.String(255))
#     department=db.relationship('Department', backref='groups')
#     department_id=db.Column(db.Integer, db.ForeignKey('department.id'))
#
# class Usergroupmap(db.Model):
#     _tablename__ = "usergroupmap"
#
#     id = db.Column(db.Integer, primary_key=True)
#     user=db.relationship('User', backref='Usergroupmaps')
#     group=db.relationship('Group', backref='Usergroupmaps')
#     user_id=db.Column(db.Integer, db.ForeignKey('User.id'))
#     group_id=db.Column(db.Integer, db.ForeignKey('Group.id'))
#     # @property
    # def url(self):
    #     return url_for('book', id=self.id)

# class UserSchema(Schema):
#     id=fields.Int(dump_only=True)
#     oauth_token = fields.Str()
#     oauth_id = fields.Int()
#     cn_name = fields.Str()
#     name = fields.Str()
#     employee_id = fields.Str()
#     email = fields.Str()
#     mobile = fields.Str()
#     superior_id = fields.Int()
#     p_level = fields.Int()
#     m_level = fields.Int()
#     department_id = fields.Int()
#     department_name = fields.Str()
#     function_id = fields.Int()
#     function_name = fields.Str()
#     status = fields.Int()
#     created = fields.Time
#     updated = fields.Time
#
# class DepartmentSchema(Schema):
#     id=fields.Int(dump_only=True)
#     name = fields.Str()
#     description= fields.Str()
#
# class GroupSchema(Schema):
#     id=fields.Int(dump_only=True)
#     name = fields.Str()
#     description= fields.Str()
#     ldap_id=fields.Int()
#     department_id=fields.Int()
#     group=fields.Nested(DepartmentSchema)
#
# class Usergroupmapchema(Schema):
#     id=fields.Int(dump_only=True)
#     user=fields.Nested(UserSchema)
#     group=fields.Nested(GroupSchema)
#     user_id=fields.Int()
#     group_id=fields.Int()

