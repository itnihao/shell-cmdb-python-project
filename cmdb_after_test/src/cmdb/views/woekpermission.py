# -*- coding: utf-8 -*-
from flask import Blueprint, render_template,request,redirect,url_for,flash,send_from_directory,jsonify
from flask_login import login_required, current_user
from application import app,db,celery,fujs
from models.ip_blacklist import IpBlacklist
from views.functions import responsejson
from datetime import datetime
from views.functions import visible
from work_permission.work_fun import *
from models.work_permission import *
from views.work_permission.work_fun import *
import json

@app.context_processor
def inject_fujs():
    return dict(fujs=fujs)

workpermission = Blueprint('workpermission', __name__)

@workpermission.route("/main",methods=['GET', 'POST'])
@login_required
def main():
    workShow=getWorkShow()
    roles=WorkRoleSchema(many=True).dump(WorkRole.query.all()).data

    return render_template("tools/workpermission/main.html",workShow=workShow,roles=roles)

@workpermission.route("/rolemanage",methods=['GET', 'POST'])
@login_required
def rolemanage():
    workShow=getWorkShow()
    roles=WorkRoleSchema(many=True).dump(WorkRole.query.all()).data

    return render_template("tools/workpermission/rolemanage.html",workShow=workShow,roles=roles)

@workpermission.route("/roleadd",methods=['GET', 'POST'])
@login_required
def roleadd():
    if request.method == 'POST':
        name=request.form['name']
        description=request.form['description']
        try:
            role_s=WorkRole.query.filter(WorkRole.name==name).first()
            if role_s:
                return responsejson(1,'name already existed!')
            dctarget=WorkRole(name=name,description=description)
            db.session.add(dctarget)
            db.session.commit()
            return responsejson(0,'')
        except Exception,e:
            return responsejson(1,'Add failed!')

@workpermission.route("/roledetail/<int:id>",methods=['GET', 'POST'])
@login_required
def roledetail(id):
    jsonval={}
    intreg=re.compile('^\d*$')
    if not intreg.match(str(id)):
        return app.response_class(json.dumps(jsonval), mimetype='application/json')
    info=WorkRole.query.filter(WorkRole.id==id).first()
    jsonval=WorkRoleSchema().dump(info).data
    return app.response_class(json.dumps(jsonval), mimetype='application/json')

@workpermission.route("/rolemodify/<int:id>",methods=['GET', 'POST'])
@login_required
def rolemodify(id):
    try:
        logmsg=""
        code=0
        intreg=re.compile('^\d*$')
        if not intreg.match(str(id)):
            return responsejson(1,'修改失败')

        info=WorkRole.query.filter(WorkRole.id==id).first()
        name=request.form['name']

        description=request.form['description']


        if info.name!=name:
            info.name=name

        if info.description!=description:
            info.description=description

        db.session.commit()
        return responsejson(0,'')
    except Exception,e:
        return responsejson(1,'修改失败')

@workpermission.route("/roledelete/<int:id>",methods=['GET', 'POST'])
@login_required
def roledelete(id):
    try:
        import re
        intreg=re.compile('^[1-9]\d*$')
        if not intreg.match(str(id)):
            return responsejson(1,"删除失败")
        info=WorkRole.query.filter(WorkRole.id==id).first()

        db.session.delete(info)
        db.session.commit()
        return responsejson(0,"删除成功")
    except Exception,e:
        return responsejson(1,"删除失败")

@workpermission.route("/getroleall/<int:id>",methods=['GET', 'POST'])
@login_required
@permission_required
def getroleall(id):

    current_role=WorkRoleSchema().dump(WorkRole.query.filter(WorkRole.id==id).first()).data
    roles=WorkRoleSchema(many=True).dump(WorkRole.query.all()).data
    workShow=getWorkShow()

    userroles=UserWorkRolemapSchema(many=True).dump(UserWorkRolemap.query.filter(UserWorkRolemap.workrole_id==id).all()).data
    poolroles=WorkPoolRolemapSchema(many=True).dump(WorkPoolRolemap.query.filter(WorkPoolRolemap.role_id==id).all()).data
    scriptroles=WorkFileRolemapSchema(many=True).dump(WorkFileRolemap.query.filter(WorkFileRolemap.role_id==id).all()).data
    taskroles=WorkTaskRolemapSchema(many=True).dump(WorkTaskRolemap.query.filter(WorkTaskRolemap.role_id==id).all()).data
    oproles=WorkRoleUrlmapSchema(many=True).dump(WorkRoleUrlmap.query.filter(WorkRoleUrlmap.work_role_id==id).all()).data

    departinfo=Department.query.all()
    departlist={}
    departlist['0']='unknow'
    if departinfo:
        for d in departinfo:
            departlist[str(d.id)]=d.name
    for pool in poolroles:
        try:
            pool['pool']['department']=departlist[str( pool['pool']['department_id'])]
        except:
            pool['pool']['department']=departlist['0']


    return render_template("tools/workpermission/roledetail.html",workShow=workShow,current_role=current_role,
                           roles=roles,userroles=userroles,poolroles=poolroles,scriptroles=scriptroles,taskroles=taskroles,oproles=oproles)

@workpermission.route("/getuser",methods=['GET', 'POST'])
@login_required
def getuser():
     jsonval=[]
     all_dep=Department.query.all()
     # all_dep=DepartmentSchema(many=True).dump(all_dep).data

     jsonval=[]
     for d in all_dep:
         d_add={'id':d.id,'text': d.name,'href': '#'+d.name,'tags': ['0'],'nodes':[],'level':1}
         for w in d.group:
             g_add=({'id':w.id,'text': w.name,'href': '#'+w.name,'tags': ['0'],'nodes':[],'level':2})
             for u in w.Usergroupmaps:
                 u_add={'id':u.user.id,'text': u.user.cn_name+'@'+u.user.name,'href': '#'+u.user.name,'tags': ['0'],'nodes':[],'level':3}
                 g_add['nodes'].append(u_add)
             g_add['tags'][0]=str(len(g_add['nodes']))
             d_add['nodes'].append(g_add)


         d_add['tags'][0]=str(len(d_add['nodes']))
         jsonval.append(d_add)

     return app.response_class(json.dumps(jsonval), mimetype='application/json')

@workpermission.route("/adduserrole/<int:id>",methods=['GET', 'POST'])
@login_required
def adduserrole(id):
    import copy
    jsonval={'code':0,'data':''}
    try:
        user_info=json.loads(request.form.get('user_info'))
        d = {}
        for i in user_info:
            d.setdefault(i['id'], 0)
            d[i['id']] += 1
        at = copy.copy(user_info)
        for i in at:
            if d[i['id']] > 1:
                user_info.remove(i)
        u_r_f=UserWorkRolemap.query.filter(UserWorkRolemap.workrole_id==id).all()

        u_ids=[]
        for u in u_r_f:
            u_ids.append(u.user_id)
        for a_u in user_info:
            if not (a_u['id'] in u_ids):
                dctarget=UserWorkRolemap(user_id=a_u['id'],workrole_id=id)
                db.session.add(dctarget)
                db.session.commit()
        data_r=UserWorkRolemapSchema(many=True).dump(UserWorkRolemap.query.filter(UserWorkRolemap.workrole_id==id).all()).data
        jsonval['data']=data_r
        jsonval['code']=1
        return app.response_class(json.dumps(jsonval), mimetype='application/json')
    except:
        return app.response_class(json.dumps(jsonval), mimetype='application/json')

@workpermission.route("/userdelete/<int:id>",methods=['GET', 'POST'])
@login_required
def userdelete(id):
    try:
        import re
        intreg=re.compile('^[1-9]\d*$')
        if not intreg.match(str(id)):
            return responsejson(0,"删除失败")
        info=UserWorkRolemap.query.filter(UserWorkRolemap.id==id).first()

        db.session.delete(info)
        db.session.commit()
        return responsejson(1,"删除成功")
    except Exception,e:
        return responsejson(0,"删除失败")

@workpermission.route("/getpool",methods=['GET', 'POST'])
@login_required
def getpool():
     jsonval=[]
     all_dep=Department.query.all()
     work_role_id=getWorkRole(current_user.id)
     dep_filter=''
     if work_role_id==1:
         dep_filter=Pool.query.filter()
     elif work_role_id==0:
         dep_filter=''
     else:
         w_f=WorkPoolRolemap.query.filter(WorkPoolRolemap.role_id==work_role_id).all()
         if(w_f):
             list_r=[]
             for w in w_f:
                 list_r.append(w.pool_id)
                 dep_filter=Pool.query.filter(Pool.id.in_(list_r))

     for d in all_dep:
         d_add={'id':d.id,'text': d.name,'href': '#'+d.name,'tags': ['0'],'nodes':[],'level':1}
         all_pool=''
         if dep_filter:
            all_pool=dep_filter.filter(Pool.department_id==d.id).all()
         if all_pool:
             d_add['tags'][0]=str(len(all_pool))
             for p in all_pool:
                # d_add['nodes'].append({'id':d.id,'text': p.name,'href': '#'+p.name,'tags': ['0'],'nodes':[]})
                p_add=({'id':p.id,'text': p.name,'href': '#'+p.name,'tags': ['0'],'nodes':[],'state': { 'expanded': False,},'level':2})

                d_add['nodes'].append(p_add)
         jsonval.append(d_add)


     return app.response_class(json.dumps(jsonval), mimetype='application/json')

@workpermission.route("/addpoolrole/<int:id>",methods=['GET', 'POST'])
@login_required
def addpoolrole(id):
    import copy
    jsonval={'code':0,'data':''}
    try:
        pool_info=json.loads(request.form.get('pool_info'))

        p_r_f=WorkPoolRolemap.query.filter(WorkPoolRolemap.role_id==id).all()

        u_ids=[]
        for p in p_r_f:
            u_ids.append(p.pool_id)
        for a_u in pool_info:
            if not (a_u['id'] in u_ids):
                dctarget=WorkPoolRolemap(pool_id=a_u['id'],role_id=id)
                db.session.add(dctarget)
                db.session.commit()
        data_r=WorkPoolRolemapSchema(many=True).dump(WorkPoolRolemap.query.filter(WorkPoolRolemap.role_id==id).all()).data
        departinfo=Department.query.all()
        departlist={}
        departlist['0']='unknow'
        if departinfo:
            for d in departinfo:
                departlist[str(d.id)]=d.name
        for pool in data_r:
            try:
                pool['pool']['department']=departlist[str( pool['pool']['department_id'])]
            except:
                pool['pool']['department']=departlist['0']

        jsonval['data']=data_r
        jsonval['code']=1
        return app.response_class(json.dumps(jsonval), mimetype='application/json')
    except Exception,e:
        return app.response_class(json.dumps(jsonval), mimetype='application/json')

@workpermission.route("/pooldelete/<int:id>",methods=['GET', 'POST'])
@login_required
def pooldelete(id):
    try:
        import re
        intreg=re.compile('^[1-9]\d*$')
        if not intreg.match(str(id)):
            return responsejson(0,"删除失败")
        info=WorkPoolRolemap.query.filter(WorkPoolRolemap.id==id).first()

        db.session.delete(info)
        db.session.commit()
        return responsejson(1,"删除成功")
    except Exception,e:
        return responsejson(0,"删除失败")

@workpermission.route("/addscriptrole/<int:id>",methods=['GET', 'POST'])
@login_required
def addscriptrole(id):
    import copy
    jsonval={'code':0,'data':''}
    try:
        script_info=json.loads(request.form.get('script_info'))

        u_r_f=WorkFileRolemap.query.filter(UserWorkRolemap.workrole_id==id).all()

        u_ids=[]
        for u in u_r_f:
            u_ids.append(u.workfile_id)
        for a_u in script_info:
            if not (a_u['id'] in u_ids):
                dctarget=WorkFileRolemap(workfile_id=a_u['id'],role_id=id)
                db.session.add(dctarget)
                db.session.commit()
        data_r=WorkFileRolemapSchema(many=True).dump(WorkFileRolemap.query.filter(WorkFileRolemap.role_id==id).all()).data
        jsonval['data']=data_r
        jsonval['code']=1
        return app.response_class(json.dumps(jsonval), mimetype='application/json')
    except:
        return app.response_class(json.dumps(jsonval), mimetype='application/json')

@workpermission.route("/scriptdelete/<int:id>",methods=['GET', 'POST'])
@login_required
def scriptdelete(id):
    try:
        import re
        intreg=re.compile('^[1-9]\d*$')
        if not intreg.match(str(id)):
            return responsejson(0,"删除失败")
        info=WorkFileRolemap.query.filter(WorkFileRolemap.id==id).first()

        db.session.delete(info)
        db.session.commit()
        return responsejson(1,"删除成功")
    except Exception,e:
        return responsejson(0,"删除失败")


@workpermission.route("/getjob",methods=['GET', 'POST'])
@login_required
def getjob():
     jsonval=[]
     all_jobs=WorkTaskTemplate.query.all()

     for d in all_jobs:
         d_add={'id':d.id,'text': d.name,'href': '#'+d.name,'tags': '','nodes':[],'level':1}
         jsonval.append(d_add)


     return app.response_class(json.dumps(jsonval), mimetype='application/json')

@workpermission.route("/addjobrole/<int:id>",methods=['GET', 'POST'])
@login_required
def addjobrole(id):
    jsonval={'code':0,'data':''}
    try:
        job_info=json.loads(request.form.get('job_info'))

        u_r_f=WorkTaskRolemap.query.filter(WorkTaskRolemap.role_id==id).all()

        u_ids=[]
        for u in u_r_f:
            u_ids.append(u.task_id)
        for a_u in job_info:
            if not (a_u['id'] in u_ids):
                dctarget=WorkTaskRolemap(task_id=a_u['id'],role_id=id)
                db.session.add(dctarget)
                db.session.commit()
        data_r=WorkTaskRolemapSchema(many=True).dump(WorkTaskRolemap.query.filter(WorkTaskRolemap.role_id==id).all()).data
        jsonval['data']=data_r
        jsonval['code']=1
        return app.response_class(json.dumps(jsonval), mimetype='application/json')
    except:
        return app.response_class(json.dumps(jsonval), mimetype='application/json')

@workpermission.route("/jobdelete/<int:id>",methods=['GET', 'POST'])
@login_required
def jobdelete(id):
    try:
        import re
        intreg=re.compile('^[1-9]\d*$')
        if not intreg.match(str(id)):
            return responsejson(0,"删除失败")
        info=WorkTaskRolemap.query.filter(WorkTaskRolemap.id==id).first()

        db.session.delete(info)
        db.session.commit()
        return responsejson(1,"删除成功")
    except Exception,e:
        return responsejson(0,"删除失败")

@workpermission.route("/getop",methods=['GET', 'POST'])
@login_required
def getop():
     jsonval=[]
     all_jobs=WorkUrl.query.all()

     for d in all_jobs:
         d_add={'id':d.id,'text': d.description,'href': '#'+d.description,'tags': '','nodes':[],'level':1}
         jsonval.append(d_add)


     return app.response_class(json.dumps(jsonval), mimetype='application/json')

@workpermission.route("/addoprole/<int:id>",methods=['GET', 'POST'])
@login_required
def addoprole(id):
    jsonval={'code':0,'data':''}
    try:
        op_info=json.loads(request.form.get('op_info'))

        u_r_f=WorkRoleUrlmap.query.filter(WorkRoleUrlmap.work_role_id==id).all()

        u_ids=[]
        for u in u_r_f:
            u_ids.append(u.url_id)
        for a_u in op_info:
            if not (a_u['id'] in u_ids):
                dctarget=WorkRoleUrlmap(url_id=a_u['id'],work_role_id=id)
                db.session.add(dctarget)
                db.session.commit()
        data_r=WorkRoleUrlmapSchema(many=True).dump(WorkRoleUrlmap.query.filter(WorkRoleUrlmap.work_role_id==id).all()).data
        jsonval['data']=data_r
        jsonval['code']=1
        return app.response_class(json.dumps(jsonval), mimetype='application/json')
    except:
        return app.response_class(json.dumps(jsonval), mimetype='application/json')

@workpermission.route("/opdelete/<int:id>",methods=['GET', 'POST'])
@login_required
def opdelete(id):
    try:
        import re
        intreg=re.compile('^[1-9]\d*$')
        if not intreg.match(str(id)):
            return responsejson(0,"删除失败")
        info=WorkRoleUrlmap.query.filter(WorkRoleUrlmap.id==id).first()

        db.session.delete(info)
        db.session.commit()
        return responsejson(1,"删除成功")
    except Exception,e:
        return responsejson(0,"删除失败")