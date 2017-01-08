# coding=utf-8
__author__ = 'qiqi'
'''
  此job用来同步ldap信息与数据库信息，方便跳板机登陆，一天跑一次
'''

from apis.ldap.ldap_api import *
from models.user import *

class SyncLdap:
    ldapObj = LDAPMgmt(LDAP_HOST_URL, LDAP_BASE_DN, LDAP_ROOT_DN, LDAP_ROOT_PW)

    def run(self):
        print "=======start========"
        self.sync_dep()
        self.sync_group()
        self.sync_user()
        self.sync_user_group()
        print "=======end========="

    def sync_dep(self):
        deps = Department.query.all()
        if deps:
            for dep in deps:
                dep_name = dep.name
                res = self.ldapObj.list("ou=%s"%dep_name)
                if not res:
                    self.ldapObj.addDepart(dep_name)
                    print "Ldap新增部门%s!"%dep_name

    def sync_group(self):
        groups = Group.query.all()
        if groups:
            for group in groups:
                res = self.ldapObj.list("cn=%s"%group.ldap_id)
                if not res:
                    dep = Department.query.filter(Department.id == group.department_id).first()
                    if dep:
                        self.ldapObj.addGroup(dep.name,group.name)
                        print "%s下新增组%s!"%(dep.name,group.name)

    def sync_user(self):
        users = User.query.all()
        if users:
            for user in users:
                if user.name == "" or user.name == "系统":
                    break
                res = self.ldapObj.list("uid=%s"%user.name)
                if not res:
                    self.ldapObj.addUser(user.name,user.oauth_id)
                    print "新增用户：%s"%user.name

    def sync_user_group(self):
        groups = Group.query.all()
        if groups:
            for group in groups:
                ldap_group = self.ldapObj.list("cn=%s"%group.ldap_id)
                if ldap_group:
                    dep = Department.query.filter(Department.id == group.department_id).first()
                    user_groups = Usergroupmap.query.filter(Usergroupmap.group_id == group.id).all()
                    if user_groups:
                        for user_group in user_groups:
                            user = User.query.filter(User.id == user_group.user_id).first()
                            if user:
                                user.name = user.name.encode("utf-8")
                                if not user.name in ldap_group[0][1]['memberUid']:
                                    res = self.ldapObj.addUser2Group(user.name,group.name,dep.name)
                                    if res == 0:
                                        print "添加 %s 用户到 %s 组失败！"%(user.name,group.name)
                                    else:
                                        print "添加 %s 用户到 %s 组！"%(user.name,group.name)