# -*- coding: utf-8 -*-

from django.shortcuts import render
from django.http import HttpResponse
from django.core import serializers
from models import *
from apps.dpt import models as dpt_models
from apps.server_device import models as server_models
from public.APIViews import CoreView
from public.Exceptions import APIError
from public.Check import CheckParameters
from public.Syskeywords import db_code_mapping
import json
from datetime import datetime

class Permission(CoreView):

    def post_getgroupwithuser(self):
        try:
            user = dpt_models.TBspUser.objects.filter(account=self.parameters('user')).exclude(delete_status=db_code_mapping['delete'])
            group = TUserGroup.objects.filter(user=user)[0]
            return group.group.groupname
        except:
            raise APIError(-3000)

    def post_getusergroup(self):
        try:
            groupid = self.parameters('groupid')
            usergroups = TUserGroup.objects.filter(group=groupid)
            data = []
            for obj in usergroups:
                user = dpt_models.TBspUser.objects.get(bsp_user_id=obj.user_id)
                dic = {
                    'id':user.bsp_user_id,
                    'text':user.nickname,
                    'name':user.nickname,
                    'account':user.account,
                    # 'org':org.org_name,
                    # 'leader':leader.nickname,
                    # 'group':'group.group.groupname'
                }
                leaderid = user.leaders
                leader = dpt_models.TBspUser.objects.filter(bsp_user_id=leaderid)
                if leader:
                    leader = leader[0]
                    dic['leader'] = leader.nickname
                else:
                    dic['leader'] = '未设置'

                bsporgid = user.org_id
                org = dpt_models.TBspOrg.objects.filter(org_id=bsporgid)
                if org:
                    org = org[0]
                    dic['org'] = org.org_name
                else:
                    dic['org'] = '未设置'

                group = TUserGroup.objects.filter(user=user.bsp_user_id)
                if group:
                    group = group[0]
                    dic['group'] = group.group.groupname
                else:
                    dic['group'] = '未设置'

                data.append(dic)
            return data
        except:
            raise APIError(-3000)


    def post_addusertogroup(self):
        try:
            user = dpt_models.TBspUser.objects.filter(account=self.parameters('user')).exclude(delete_status=db_code_mapping['delete'])[0]
            group = TGroup.objects.filter(groupname=self.parameters('groupname')).exclude(delete_status=db_code_mapping['delete'])[0]
            d = {
                'ugid': self.create_id(),
                'user': user,
                'group': group
                }
            kwargs = {'user': user, 'defaults': d}
            obj, created = TUserGroup.objects.exclude(delete_status=db_code_mapping['delete']).get_or_create(**kwargs)
            if not created:
                del d['ugid']
                obj.group = group
                obj.__dict__.update(**d)
                obj.save()
        except:
            raise APIError(-3000)


    def post_getallgroups(self):
        try:
            groups = TGroup.objects.all()
            print groups
            data = []
            for obj in groups:
                dic = {

                    'id':obj.groupid,
                    'text':obj.groupname,
                    'delete_status':obj.delete_status

                }
                data.append(dic)

            return data
        except Exception as e:
            raise APIError(-3000)


    def post_saveusergroup(self):
        userid = self.parameters('userid')
        groupid = self.parameters('groupid')
        try:
            user = dpt_models.TBspUser.objects.get(bsp_user_id=userid)
            group = TGroup.objects.get(groupid=groupid)
            usergroup = TUserGroup.objects.filter(user=userid)
            if not usergroup:
                usergroupid = self.create_id()
                usergroup = TUserGroup.objects.create(ugid=usergroupid)
                usergroup.user = user
                usergroup.delete_status = 0
            else:
                usergroup = usergroup[0]

            usergroup.group = group
            usergroup.save()
        except Exception as e:
            raise

    def post_searchuser(self):
        name = self.parameters('name')
        account = self.parameters('account')

        result = [];
        if name and account:
            names = name.split(',')
            accounts = account.split(',')
            result = dpt_models.TBspUser.objects.filter(nickname__in=names).filter(account__in=accounts)
        else:
            if account:
                accounts = account.split(',')
                result = dpt_models.TBspUser.objects.filter(account__in=accounts)
            if name:
                names = name.split(',')
                result = dpt_models.TBspUser.objects.filter(nickname__in=names)

        print result

        data = [];
        for obj in result:
            dic = {

                'id':obj.bsp_user_id,
                'name':obj.nickname,
                'text':obj.nickname,
                'account':obj.account,
                # 'org':org.org_name,
                # 'leader':leader.nickname,
                # 'group':'group.group.groupname'

            }

            group = TUserGroup.objects.filter(user=obj.bsp_user_id)
            if group:
                group = group[0]
                dic['group'] = group.group.groupname
            else:
                dic['group'] = '未设置'

            bsporgid = obj.org_id
            org = dpt_models.TBspOrg.objects.filter(org_id=bsporgid)
            if org:
                org = org[0]
                dic['org'] = org.org_name
            else:
                dic['org'] = '未设置'

            leaderid = obj.leaders
            leader = dpt_models.TBspUser.objects.filter(bsp_user_id=leaderid)
            if leader:
                leader = leader[0]
                dic['leader'] = leader.nickname
            else:
                dic['leader'] = '未设置'

            data.append(dic)
        return data

    def post_getallrolelist(self):
        try:
            roleList = TRole.objects.all()
            data = [];
            for obj in roleList:
                dic = {
                    'text':obj.rolename,
                    'id':obj.roleid
                }
                data.append(dic)
            return data
        except Exception as e:
            raise APIError(-3000)

    def post_getroleforgroup(self):
        groupid = self.parameters('id')
        try:
            g_r = TGroupRole.objects.get(group=groupid)
            role = TRole.objects.get(roleid=g_r.role_id)
            result = [{

                'id':role.roleid,
                'name':role.rolename

            }]
            return result
        except Exception as e:
            raise APIError(-3000)

    def post_savegrouprolechange(self):
        try:
            groupid = self.parameters('groupid')
            groupname = self.parameters('groupname')
            roleid = self.parameters('roleid')

            role = TRole.objects.get(roleid=roleid)
            g_r = [];
            if groupid:
                g_r = TGroupRole.objects.get(group=groupid)
            else:
                group = TGroup.objects.create(groupid=self.create_id())
                group.groupname = groupname
                group.save()
                g_r = TGroupRole.objects.create(grid=self.create_id())
                g_r.group = group

            g_r.role = role
            g_r.save()
        except Exception as e:
            raise APIError(-3000)

    def post_findmodelsforrole(self):
        roleid = self.parameters('roleid')
        models = TRoleModularPermissionsType.objects.filter(role=roleid)
        data = []
        for model in models:
            dic = {

                'modelid':model.modular_id,
                'modelname':model.modular.modularname,
                'permission':model.permission.permission,
                'rolename':model.role.rolename,
            }

            data.append(dic)
        return data

    def post_getallmodels(self):
        models = TModular.objects.all()
        data = []
        for obj in models:
            dic = {

                'id':obj.mid,
                'text':obj.modularname,

            }
            data.append(dic)
        return data

    def post_findoperationinmodel(self):
            modelid = self.parameters('modelid')
            isall = self.parameters('isall')
            mos = TModularOperation.objects.filter(modular=modelid)
            data = []
            for mo in mos:
                dic = {

                    'name':mo.operation.name,
                    'key':mo.operation.key,
                    'uri':mo.operation.uri,
                    # buttonid
                    'http_method':mo.operation.http_method,
                    'permission':[],
                    # delete_status
                    'modelname':mo.modular.modularname,

                }
                ops = TOperation.objects.filter(name=mo.operation.name)
                for op in ops:
                    pDic = {
                        'permissionid':op.permission_id,
                        'permissionname':op.permission.permission,
                        'permission_status':op.permission_status
                    }
                    dic['permission'].append(pDic)

                data.append(dic)

            return data

    def post_getallpermission(self):

        p = TPermissionsType.objects.all()
        data = []
        for obj in p:
            dic = {
                'id':obj.ptid,
                'text':obj.permission,
            }
            data.append(dic)
        return data

    def post_updataorinsertrolemodularpermissiontype(self):
        roleid = self.parameters('roleid')
        rolename = self.parameters('rolename')
        if not roleid:
            roleid = self.create_id()
        modularPermissions = self.parameters('modularPermissions')
        for m_p in modularPermissions:
            modularid = m_p['modelid'];
            permissionid = m_p['permissionid'];
            p = TPermissionsType.objects.filter(ptid=permissionid)[0]
            result = TRoleModularPermissionsType.objects.filter(role=roleid, modular=modularid)
            if result:
                rmpt = result[0]
                rmpt.permission = p
                print p.permission
                rmpt.save()
            else:
                role = TRole.objects.filter(roleid=roleid)
                # print '11111'
                if not role:
                    role = TRole.objects.create(roleid=roleid)
                    # print '22222'
                    role.rolename=rolename
                    role.save()
                else:
                    role = role[0]

                modular = TModular.objects.get(mid=modularid)
                result = TRoleModularPermissionsType.objects.create(rmptid=self.create_id(), role=role, modular=modular)
                result.permission = p
                result.save()
