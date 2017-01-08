# -*- coding: utf-8 -*-
from flask_login import current_user,current_app
from flask import request,redirect,render_template
from models.work_permission import *
from functools import wraps
import re

def permission_required(func):
    @wraps(func)
    def decorated_view(*args, **kwargs):
        path=request.path
        if(kwargs):
            path=request.path[:request.path.rindex("/")]
        if checkPermission(path,current_user.id):
            return func(*args, **kwargs)
        elif not checkPermission(path,current_user.id):

            return render_template('error.html',status='权限错误',title='无相关权限')
        return func(*args, **kwargs)
    return decorated_view

def checkPermission(url,user_id):
    # work_role_id=getWorkRole(user_id)
    # if(work_role_id==0):
    #     return False
    # elif(work_role_id==1):
    #     return True
    # else:
    #    if getUrlRole(work_role_id,url):
    #        return True
    #    else:
    #        return False
    work_roles=getWorkRoles(user_id)
    if work_roles['ret']==0:
        return False
    elif work_roles['ret']==1:
        return True
    else:
        for work_role_id in work_roles['roles']:
             if getUrlRole(work_role_id,url):
                 return True
        return False

# 1-admin , 0-norole
def getWorkRole(user_id):
    role_map=UserWorkRolemap.query.filter(UserWorkRolemap.user_id==user_id).first()
    if not role_map:
        return 0
    else:
        return role_map.workrole_id

def getWorkRoles(user_id):
    role_admin=UserWorkRolemap.query.filter(UserWorkRolemap.user_id==user_id,UserWorkRolemap.workrole_id==1).first()
    if role_admin:
        return {'ret':1}
    role_map=UserWorkRolemap.query.filter(UserWorkRolemap.user_id==user_id).all()
    if not role_map:
        return {'ret':0}
    else:
        r_roles=[]
        for r in role_map:
            r_roles.append(r.workrole_id)
        return {'ret':2,'roles':r_roles}

def getUrlRole(worlrole_id,url):
    g_url=WorkUrl.query.filter(WorkUrl.url==url).first()
    if g_url:
        url_role=WorkRoleUrlmap.query.filter(WorkRoleUrlmap.url_id==g_url.id,WorkRoleUrlmap.work_role_id==worlrole_id).first()
        if url_role:
            return True
        else:
            return False
    else:
        return False

def getWorkShow():
    show_dict={}
    f_urls=WorkUrl.query.filter().all()
    for url in f_urls:
        show_dict.update({url.key:False})
    work_roles=getWorkRoles(current_user.id)
    if(work_roles['ret']==1):
       for key in show_dict:
           show_dict[key]=True
       return show_dict
    elif(work_roles['ret']==0):
       # for key in show_dict:
       #     show_dict[key]=False
       return show_dict
    else:
        for work_role_id in work_roles['roles']:
            url_roles=WorkRoleUrlmap.query.filter(WorkRoleUrlmap.work_role_id==work_role_id).all()
            for key in show_dict:
                for url_role in url_roles:
                    if url_role.url.key==key:
                        show_dict[key]=True
                        break
        return show_dict

def getWorkFilePre(source_data):
    work_roles=getWorkRoles(current_user.id)
    p_key='isPre'
    for w in source_data:
        w.update({p_key:False})
    if(work_roles['ret']==1):
        for w in source_data:
            w.update({p_key:True})
    elif(work_roles['ret']==0):
        for w in source_data:
            w.update({p_key:False})
    else:
        for work_role_id in work_roles['roles']:
            for w in source_data:
                # w.update({p_key:False})
                w_f=WorkFileRolemap.query.filter(WorkFileRolemap.role_id==work_role_id,WorkFileRolemap.workfile_id==w['id']).first()
                if(w_f):
                    w[p_key]=True
    return source_data

def getWorkTaskPre(source_data):
    work_roles=getWorkRoles(current_user.id)
    key_pre='isPre'
    key_delete='isDel'
    for w in source_data:
        w.update({key_pre:False,key_delete:False})
    if(work_roles['ret']==1):
        for w in source_data:
            w.update({key_pre:True,key_delete:True})
    elif(work_roles['ret']==0):
        for w in source_data:
            w.update({key_pre:False,key_delete:False})
    else:
        for work_role_id in work_roles['roles']:
            for w in source_data:
                # w.update({key_pre:False,key_delete:False})
                if w['template_id']==0 or (not w['template_id']):
                    w[key_pre]=True
                else:
                    w_f=WorkTaskRolemap.query.filter(WorkTaskRolemap.role_id==work_role_id,WorkTaskRolemap.task_id==w['template_id']).first()
                    if(w_f):
                        w[key_pre]=True
    return source_data

def getTaskTemplatePre(source_data):
    work_roles=getWorkRoles(current_user.id)
    key_pre='isPre'
    key_delete='isDel'
    for w in source_data:
        w.update({key_pre:False,key_delete:False})
    if(work_roles['ret']==1):
        for w in source_data:
            w.update({key_pre:True,key_delete:True})
    elif(work_roles['ret']==0):
        for w in source_data:
            w.update({key_pre:False,key_delete:False})
    else:
        for work_role_id in work_roles['roles']:
            for w in source_data:
                # w.update({key_pre:False,key_delete:False})
                w_f=WorkTaskRolemap.query.filter(WorkTaskRolemap.role_id==work_role_id,WorkTaskRolemap.task_id==w['id']).first()
                if(w_f):
                    w[key_pre]=True
    return source_data
