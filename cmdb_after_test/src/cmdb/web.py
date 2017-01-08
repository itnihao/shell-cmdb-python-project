# -*- coding: utf-8 -*-

from application import app,db
from flask import redirect, url_for, request, make_response
from flask_login import LoginManager, login_user, current_user
import re

COOKIE_KEY_SECURE_TOKEN = 'secure_token'
login_manager = LoginManager()
login_manager.init_app(app)
from models.user import User
from models.action import Action
from models.user_role import UserRole
from models.role_action import RoleAction
from sqlalchemy import and_
from views.user import match_user_cookie
from views.functions import responsejson

@login_manager.user_loader
def load_user(id):
    return User.query.filter(User.id == id).first()

'''
  关于用户权限这块 可以做的更好些，以请求的path为准，赋予权限，path 也分post,get,delete三种权限
  例如 path:/cmdb/host/add  method:post/get/delete
'''
@app.before_request
def before_request():
    method = request.method.lower()
    path = request.path
    if not current_user.is_authenticated():
        return
    if current_user.is_admin:
        return
    ignorepath = app.config.get("IGNOREPATH")
    pattern = re.compile('%s'%ignorepath)
    if pattern.match(path):
        return
    pattern1 = re.compile(r'(.*)(/\d+$)')
    if pattern1.match(path):
        path = pattern1.match(path).group(1)
    if path[-1] == "/":
        path = path[0:-1]
    action = Action.query.filter(and_(Action.url == path,Action.method == method)).first()
    if action:
        have_privilege = 1
        userrole = UserRole.query.filter(UserRole.user_id == current_user.id).all()
        user_role_id = []
        if userrole:
            for item in userrole:
                user_role_id.append(item.role_id)
        roleaction = RoleAction.query.filter(RoleAction.action_id == action.id).all()
        role_action_id = []
        if roleaction:
            for item in roleaction:
                role_action_id.append(item.role_id)
        for role_id in user_role_id:
            if role_id in role_action_id:
                have_privilege = 0
        if have_privilege:
            if request.is_xhr:
                return responsejson(-1, '没有权限')
            else:
                return  redirect(url_for('error.index'))
    return
    #return  redirect(url_for('error.index')) #这块有bug,查看的连接都没有

@app.after_request
def after_request(response):
    release_info = app.config.get("RELEASE_INFO")
    if release_info and 'path' in release_info:
        import os
        path = release_info['path']
        if os.path.exists(path):
            fp = open(path)
            release_num = fp.readline()
            release_num = str(release_num).replace("\r","").replace("\n","").replace("\r\n","")
            fp.close()
            response.headers.set('CMDB_RELEASE', release_num)
    return response

@app.errorhandler(404) #捕获应用的异常
def error_404(e):
    return error_server(e)

@app.errorhandler(500) #捕获应用的异常
def error_404(e):
    return error_server(e)

@app.errorhandler(502) #捕获应用的异常
def error_404(e):
    return error_server(e)

def error_server(e):
    from flask import render_template
    return render_template("error.html",status = e.code, title = e.name)


@login_manager.unauthorized_handler
def unauthorized():
    secure = request.cookies.get(COOKIE_KEY_SECURE_TOKEN)
    if secure:
        user_id = match_user_cookie(secure, request.user_agent)
        if user_id:
            user_info=load_user(user_id)
            if user_info:
                login_user(user_info)
                url = request.path
                if request.args:
                    param = ""
                    for k,v in request.args.items():
                        param +="%s=%s&"%(k,v)
                    url +="?"+param
                return redirect(url or '/')
    return redirect(url_for('user.login'))

from apis import *
from views import *

MODULES = (
    (public, ''),
    (device, '/cmdb/device'),
    (server, '/cmdb/server'),
    (user, '/user'),
    (datacenter, '/cmdb/datacenter'),
    (ip, '/cmdb/ip'),
    (log, '/cmdb/log'),
    (rack, '/cmdb/rack'),
    (supplier, '/cmdb/supplier'),
    (pool, '/cmdb/pool'),
    (host, '/cmdb/host'),
    (monitor, '/monitor'),
    (logger, '/logger'),
    (tickets,'/sa/tickets'),
    (tickets_category,'/sa/tickets/category'),
    (orders,'/cmdb/orders'),
    (dns_category,'/sa/dns/category'),
    (dns,'/sa/dns'),
    (error,   '/error'),
    (tools, '/cmdb/tools'),
    (bastion, '/cmdb/bastion'),
    (pmz_search, '/cmdb/pmz_search'),
    (parts, '/cmdb/parts'),
    (apipublic, '/api'),
    (apihost, '/api/cmdb/host'),
    (apiuser, '/api/user'),
    (apialarm, '/api/cmdb/alarm'),
    (apipool, '/api/cmdb/pool'),
    (apiremotecard, '/api/cmdb/remotecard'),
    (ldapgroup, '/cmdb/ldapgroup'),
    (puv, '/cmdb/puv'),
    # (ansible, '/cmdb/ansible'),
    (work, '/cmdb/work'),
    (workpermission,'/cmdb/workpermission')
)


def setting_modules(app, modules):
    """ 注册Blueprint模块 """
    for module, url_prefix in modules:
        app.register_blueprint(module, url_prefix=url_prefix)

setting_modules(app, MODULES)
