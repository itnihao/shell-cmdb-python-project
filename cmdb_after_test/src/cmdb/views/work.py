# -*- coding: utf-8 -*-
from flask import Blueprint, render_template,request,redirect,url_for,flash,send_from_directory,jsonify
from flask_login import login_required, current_user
from application import app,db,celery,fujs
from models.ip_blacklist import IpBlacklist
from views.functions import responsejson
from datetime import datetime
from views.functions import visible
from models.pool import Pool
from models.host import Host
from models.host_ip import HostIp
from models.ip_address import IpAddress
from models import Jobplat
from models.pool_host import PoolHost
from fabric.api import *
from sqlalchemy import and_
from fabric.state import output
import os,time
from models.pool import Pool
from pypages import Paginator
from config import DOMAIN
import re,commands,json,requests,pyhs2,datetime
import json as myjson
from sqlalchemy import extract,desc
from models.work import *
from models.user import Department,DepartmentSchema,User,UserSchema

from celery import Celery
# from ansible_work.ansible_playwork import get_pb
from work_permission.work_fun import permission_required
from work_permission.work_fun import *

@app.context_processor
def inject_fujs():
    return dict(fujs=fujs)

work = Blueprint('work', __name__)

@work.route("/workfilelist",methods=['GET', 'POST'])
@login_required
@permission_required
def workfilelist():
    department_q=Department.query.all()
    se=DepartmentSchema(many=True).dump(department_q)
    department=se.data

    worktype_q=WorkType.query.all()
    se=WorkTypeSchema(many=True).dump(worktype_q)
    worktype=se.data

    workfile_q=WorkFile.query.all()
    se=WorkFileSchema(many=True).dump(workfile_q)
    workfile=getWorkFilePre(se.data)

    workShow=getWorkShow()
    return render_template("tools/work/workfilelist.html",department=department,worktype=worktype,workfile=workfile,workShow=workShow)


@work.route("/workfileadd",methods=['GET', 'POST'])
@login_required
@permission_required
def workfileadd():
    if request.method == 'POST':
        name=request.form['name']
        path=request.form['path']
        filename=request.form['filename']
        dp_id=request.form['dp_id']
        type_id=request.form['type_id']
        description=request.form['description']
        try:
            work_s=WorkFile.query.filter(WorkFile.name==name).first()
            if work_s:
                return responsejson(1,'name already existed!')
            dctarget=WorkFile(name=name,path=path,filename=filename,department_id=int(dp_id),workType_id=int(type_id),description=description)
            db.session.add(dctarget)
            db.session.commit()
            return responsejson(0,'')
        except Exception,e:
            return responsejson(1,'Add failed!')

@work.route("/workfiledetail/<int:id>",methods=['GET', 'POST'])
@login_required
def workfiledetail(id):
    jsonval={}
    intreg=re.compile('^\d*$')
    if not intreg.match(str(id)):
        return app.response_class(json.dumps(jsonval), mimetype='application/json')
    info=WorkFile.query.filter(WorkFile.id==id).first()
    jsonval=WorkFileSchema().dump(info).data
    return app.response_class(json.dumps(jsonval), mimetype='application/json')

@work.route("/workfilemodify/<int:id>",methods=['GET', 'POST'])
@login_required
def workfilemodify(id):
    try:
        logmsg=""
        code=0
        intreg=re.compile('^\d*$')
        if not intreg.match(str(id)):
            return responsejson(1,'修改失败')

        info=WorkFile.query.filter(WorkFile.id==id).first()
        name=request.form['name']
        path=request.form['path']
        filename=request.form['filename']
        dp_id=request.form['dp_id']
        type_id=request.form['type_id']
        description=request.form['description']

        mo_dp=Department.query.filter(Department.id==int(dp_id)).first()
        if info.department.id!=mo_dp.id:
            info.department_id=int(dp_id)

        mo_type=WorkType.query.filter(WorkType.id==int(type_id)).first()
        if info.workType.id!=mo_type.id:
            info.workType_id=int(type_id)

        if info.name!=name:
            info.name=name

        if info.description!=description:
            info.description=description

        if info.path!=path:
            info.path=path

        if info.filename!=filename:
            info.filename=filename

        db.session.commit()
        return responsejson(0,'')
    except Exception,e:
        return responsejson(1,'修改失败')

@work.route("/workfiledelete/<int:id>",methods=['GET', 'POST'])
@login_required
def workfiledelete(id):
    try:
        import re
        intreg=re.compile('^[1-9]\d*$')
        if not intreg.match(str(id)):
            return responsejson(1,"删除失败")
        info=WorkFile.query.filter(WorkFile.id==id).first()

        db.session.delete(info)
        db.session.commit()
        return responsejson(0,"删除成功")
    except Exception,e:
        return responsejson(1,"删除失败")

@work.route("/newwork",methods=['GET', 'POST'])
@login_required
@permission_required
def newwork():

    #
    # dctarget=WorkFile(name='test1',path='/root',filename='test.yaml',description='',workType_id=1,department_id=5)
    # db.session.add(dctarget)
    # db.session.commit()
    workShow=getWorkShow()
    return render_template("tools/work/newwork.html",workShow=workShow)

@work.route("/gethost",methods=['GET', 'POST'])
@login_required
def gethost():
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
                all_pool_host=PoolHost.query.filter(PoolHost.pool_id==p.id).all()
                if all_pool_host:
                    p_add['tags'][0]=str(len(all_pool_host))
                    for ph in all_pool_host:
                        host_f=Host.query.filter(Host.id==ph.host_id).first()
                        if host_f:
                            ip_add=''
                            host_ip=HostIp.query.filter(HostIp.host_id==host_f.id).first()
                            if host_ip:
                                ip_s=IpAddress.query.filter(IpAddress.id==host_ip.ip_address_id).first()
                                if ip_s:
                                    ip_add=ip_s.ipv4

                            p_add['nodes'].append({'id':host_f.id,'text': host_f.hostname+'@'+ip_add,'href': '#'+host_f.hostname,'nodes':[],
                                                   'ip':ip_add,'level':3,'poolname':p.name,"depname":d.name,'name':host_f.hostname})
                    d_add['nodes'].append(p_add)
         jsonval.append(d_add)


     return app.response_class(json.dumps(jsonval), mimetype='application/json')

@work.route("/getscript",methods=['GET', 'POST'])
@login_required
def getscript():
     jsonval=[]
     all_dep=Department.query.all()
     work_files=WorkFile.query.all()

     work_files_filter=[]
     work_roles=getWorkRoles(current_user.id)
     if work_roles['ret']==1:
         work_files_filter=work_files
     elif work_roles['ret']==0:
         work_files_filter=[]
     else:
         for work_role_id in work_roles['roles']:
             for w in work_files:
                 w_f=WorkFileRolemap.query.filter(WorkFileRolemap.role_id==work_role_id,WorkFileRolemap.workfile_id==w.id).first()
                 if(w_f):
                     isExist=False
                     for x in work_files_filter:

                         if x.workfile_id==w.id:
                             isExist=True
                             break
                     if not isExist:
                        work_files_filter.append(w)

     jsonval=[]
     for d in all_dep:
         d_add={'id':d.id,'text': d.name,'href': '#'+d.name,'tags': ['0'],'nodes':[],'level':1}
         for w in work_files_filter:
             if (w.department_id==d.id):
                 d_add['nodes'].append({'id':w.id,'text': w.name,'href': '#'+w.name,'tags': ['0'],'path':w.path,'filename':w.filename,'nodes':[],'level':2})
         d_add['tags'][0]=str(len(d_add['nodes']))
         jsonval.append(d_add)

     return app.response_class(json.dumps(jsonval), mimetype='application/json')


@celery.task(bind=True)
def long_task(self,jobinfo,job_id):
    """ Let's do it a bit cleaner """

    # verb = ['Starting up', 'Booting', 'Repairing', 'Loading', 'Checking']
    # adjective = ['master', 'radiant', 'silent', 'harmonic', 'fast']
    # noun = ['solar array', 'particle reshaper', 'cosmic ray', 'orbiter', 'bit']
    # message = ''
    # total = random.randint(10, 50)
    # for i in range(total):
    #     if not message or random.random() < 0.25:
    #         message = '{0} {1} {2}...'.format(random.choice(verb),
    #                                           random.choice(adjective),
    #                                           random.choice(noun))
    #     self.update_state(state='PROGRESS',
    #                       meta={'current': i, 'total': total,
    #                             'status': message})
    #     time.sleep(1)
    # return {'current': 100, 'total': 100, 'status': 'Task completed!',
    #         'result': 42}
    task_f=WorkTask.query.filter(WorkTask.id==job_id).first()
    self.logs = []
    try:
        for job in jobinfo:
            for script in job['scripts']:
                script_s=WorkFile.query.filter(WorkFile.id==int(script)).first()

                r = get_pb(self,job['machines'],script_s.path,script_s.name,job_id).run()

                self.logs.append("finish")
                self.logs.append(str(r))

                self.update_state(state='PROGRESS', meta={'msg': [str(r),"finish"+script_s.name]})
                # return self.logs


        self.update_state(state='MYFINSHIED', meta={'msg': self.logs})

        # return self.logs
        # upgrade_taks_log(task_f.task_id,"finish")
        for lg in self.logs:
            upgrade_taks_log(task_f.task_id,str(lg))

        r_state=1
        for (d,x) in r.items():
            if x['failures']>0:
                r_state=0
                break
            if x['unreachable']>0:
                r_state=0
                break
        task_f.state=r_state
        db.session.commit()
        return {'status': self.logs,'state':'MYFINSHIED'}
    except Exception,e:
        self.update_state(state='Error', meta={'msg': [str(e.message)]})
        upgrade_taks_log(task_f.task_id,str(e.message))
        task_f.state=0
        db.session.commit()
        # return self.logs
        return {'status': [str(e.message)],'state':'Error'}

    # message='running'
    # for i in range(0,10):
    #     time.sleep(5)
    #     t = str(time.clock())
    #     print i
    #     self.update_state(state='PROGRESS',
    #                       meta={'current': i,
    #                             'status': message})
    #     time.sleep(1)
    # return {'current': 100, 'status': 'SUCCESS'}


@work.route('/startwork',methods=['GET', 'POST'])
@login_required
def startwork():

    job_info=myjson.loads(request.form.get('job_info'))
    job_name=request.form.get('job_name')

    job=WorkTask()
    ISOTIMEFORMAT='%Y-%m-%d %X'
    job.start_time=time.strftime(ISOTIMEFORMAT, time.localtime( time.time()))
    job.info_ext=myjson.dumps(job_info)
    job.user_id=current_user.id
    job.template_id=0
    w_f= WorkTaskTemplate.query.filter(WorkTaskTemplate.name==job_name).first()
    if w_f:
        job.template_id=w_f.id

    job.name=str(job_name)+'@'+str(job.start_time)
    job.log='start task: '+job.name+'@'
    job.task_id='0'
    job.state=2

    db.session.add(job)
    db.session.commit()

    task = long_task.apply_async(args=[job_info,job.id])
    job.task_id=task.id
    db.session.commit()
    # task.wait()
    return jsonify({}), 202, {'Location': url_for('work.taskstatus',task_id=task.id)}

@work.route('/savework',methods=['GET', 'POST'])
@login_required
def savework():
    try:
        job_info=myjson.loads(request.form.get('job_info'))
        job_name=request.form.get('job_name')

        job_s=WorkTaskTemplate.query.filter(WorkTaskTemplate.name==job_name).first()

        if job_s:
           return app.response_class(json.dumps({'state':2}), mimetype='application/json')

        job=WorkTaskTemplate()
        ISOTIMEFORMAT='%Y-%m-%d %X'
        job.update_time=time.strftime(ISOTIMEFORMAT, time.localtime( time.time()))
        job.info_ext=myjson.dumps(job_info)
        job.user_id=current_user.id
        job.name=str(job_name)
        db.session.add(job)
        db.session.commit()
        return app.response_class(json.dumps({'state':1}), mimetype='application/json')
    except:
        return app.response_class(json.dumps({'state':0}), mimetype='application/json')


@work.route('/taskstatus/<task_id>',methods=['GET', 'POST'])
@login_required
def taskstatus(task_id):
    # task = long_task.AsyncResult(task_id)
    # print task.state
    # if task.state == 'PENDING':
    #     response = {
    #         'state': task.state,source_data
    #         # 'current': 0,
    #         # 'total': 1,
    #         'status': 'Pending...'
    #     }
    # elif task.state != 'FAILURE':
    #     response = {
    #         'state': task.state,
    #         # 'current': task.info.get('current', 0),
    #         # 'total': task.info.get('total', 1),
    #         # 'status': task.info.get('status', '')
    #     }
    #     # if 'result' in task.info:
    #     #     response['result'] = task.info['result']
    # else:
    #     # something went wrong in the background job
    #     response = {
    #         'state': task.state,
    #         # 'current': task.info['current'],
    #         # 'total': 1,
    #         # 'status': str(task.info),
    #     }
    # return jsonify(response)

    task = long_task.AsyncResult(task_id)
    # print task.info
    if task.state == 'PENDING':
        response = {
            'state': task.state,
            'status': 'Pending...'
        }
    elif task.state != 'FAILURE':
        response = {
            'state': task.state,
            'status': task.info
        }
        if 'result' in task.info:
            response['result'] = task.info['result']
        if 'state' in task.info:
            response['state']='MYFINSHIED'
        # if 'msg' in response['status']:
        #     for m_add in response['status']['msg']:
        #         upgrade_taks_log(task_id,m_add)
    else:
        # something went wrong in the background job
        response = {
            'state': task.state,
            'status': task.info,  # this is the exception raised
        }
        for m_add in response['status']['msg']:
            upgrade_taks_log(task_id,m_add)

    return jsonify(response)


@work.route('/history',methods=['GET', 'POST'])
@login_required
@permission_required
def history():
    all_count=WorkTask.query.count()
    current_page=1
    all_page=1
    lastpage_count=0
    if all_count>10:
        all_page=all_count/10
        if (all_count%10)>0:
            all_page+=1
            lastpage_count=all_count%10

        history_s= WorkTask.query.order_by(desc(WorkTask.id)).all()[0:10]
    else:
        history_s=WorkTask.query.order_by(desc(WorkTask.id)).all()
    history_r=WorkTaskSchema(many=True).dump(history_s).data
    for h in history_r:
        info_ext=myjson.loads(h['info_ext'])
        # h.update({'step_count':len(info_ext)})
        h['step_count']=len(info_ext)
        del h['log']
        del h['info_ext']

    history_r=getWorkTaskPre(history_r)

    workShow=getWorkShow()
    return render_template("tools/work/jobhistory.html",history=history_r,current_page=current_page,all_page=all_page,workShow=workShow)

@work.route('/searchpage',methods=['GET', 'POST'])
@login_required
def searchpage():
    current_page=int(request.form.get('current_page'))
    search=myjson.loads(request.form.get('search'))
    history_f=WorkTask.query.order_by(desc(WorkTask.id)).filter()

    if search['jobname']:
        history_f=history_f.filter(WorkTask.name.contains('%'+str(search['jobname'])+'%'))

    if search['state']:
        if int(search['state'])!=100:
            history_f=history_f.filter(WorkTask.state==int(search['state']))

    if search['starttime']:
        starttime = datetime.datetime.strptime(search['starttime'],'%Y-%m-%d')
        history_f=history_f.filter(extract('year',WorkTask.start_time)==starttime.year,
                                   extract('month',WorkTask.start_time)==starttime.month,extract('day',WorkTask.start_time)==starttime.day)

    if search['endtime']:
        starttime = datetime.datetime.strptime(search['endtime'],'%Y-%m-%d')
        history_f=history_f.filter(extract('year',WorkTask.end_time)==starttime.year,
                                   extract('month',WorkTask.end_time)==starttime.month,extract('day',WorkTask.end_time)==starttime.day)

    if search['user']:
        history_f=history_f.join(User.WorkTaskusermaps).filter(User.cn_name.contains('%'+str(search['user'])+'%'))

    if not history_f:
        history_f=WorkTask.query.order_by(desc(WorkTask.id)).all()
        all_count=WorkTask.query.count()
    else:
        history_f=history_f.all()
        all_count=len(history_f)
    all_page=int(request.form.get('all_page'))

    all_page_s=1
    lastpage_count=0
    if all_count>10:
        all_page_s=all_count/10
        if (all_count%10)>0:
            all_page_s+=1
            lastpage_count=all_count%10
    if(all_page_s>current_page):
        history_s=history_f[(current_page-1)*10:current_page*10]
    elif(all_page==current_page):

        history_s=history_f[(current_page-1)*10:]

    history_r=WorkTaskSchema(many=True).dump(history_s).data
    for h in history_r:
        info_ext=myjson.loads(h['info_ext'])
        # h.update({'step_count':len(info_ext)})
        h['step_count']=len(info_ext)

    history_r=getWorkTaskPre(history_r)

    return app.response_class(json.dumps({'info':history_r,'current_page':current_page,'all_page':all_page_s}), mimetype='application/json')

@work.route('/jobtemplate',methods=['GET', 'POST'])
@login_required
@permission_required
def jobtemplate():
    all_count=WorkTaskTemplate.query.count()
    current_page=1
    all_page=1
    lastpage_count=0
    if all_count>10:
        all_page=all_count/10
        if (all_count%10)>0:
            all_page+=1
            lastpage_count=all_count%10

        history_s= WorkTaskTemplate.query.order_by(desc(WorkTaskTemplate.id)).all()[0:10]
    else:
        history_s=WorkTaskTemplate.query.order_by(desc(WorkTaskTemplate.id)).all()
    history_r=WorkTaskTemplateSchema(many=True).dump(history_s).data
    for h in history_r:

        info_ext=myjson.loads(h['info_ext'])
        # h.update({'step_count':len(info_ext)})
        h['step_count']=len(info_ext)
        # del h['log']
        del h['info_ext']
    history_r=getTaskTemplatePre(history_r)
    workShow=getWorkShow()
    return render_template("tools/work/jobtemplate.html",history=history_r,current_page=current_page,all_page=all_page,workShow=workShow)

@work.route('/searchtemplatepage',methods=['GET', 'POST'])
@login_required
def searchtemplatepage():
    current_page=int(request.form.get('current_page'))
    search=myjson.loads(request.form.get('search'))
    history_f=WorkTaskTemplate.query.order_by(desc(WorkTaskTemplate.id)).filter()

    if search['jobname']:
        history_f=history_f.filter(WorkTaskTemplate.name.contains('%'+str(search['jobname'])+'%'))

    # if search['state']:
    #     if int(search['state'])!=100:
    #         history_f=history_f.filter(WorkTask.state==int(search['state']))

    # if search['starttime']:
    #     starttime = datetime.datetime.strptime(search['starttime'],'%Y-%m-%d')
    #     history_f=history_f.filter(extract('year',WorkTask.start_time)==starttime.year,
    #                                extract('month',WorkTask.start_time)==starttime.month,extract('day',WorkTask.start_time)==starttime.day)
    #
    # if search['endtime']:
    #     starttime = datetime.datetime.strptime(search['endtime'],'%Y-%m-%d')
    #     history_f=history_f.filter(extract('year',WorkTask.end_time)==starttime.year,
    #                                extract('month',WorkTask.end_time)==starttime.month,extract('day',WorkTask.end_time)==starttime.day)

    if search['user']:
        history_f=history_f.join(User.TaskTemplateusermaps).filter(User.cn_name.contains('%'+str(search['user'])+'%'))

    if not history_f:
        history_f=WorkTaskTemplate.query.order_by(desc(WorkTask.id)).all()
        all_count=WorkTaskTemplate.query.count()
    else:
        history_f=history_f.all()
        all_count=len(history_f)
    all_page=int(request.form.get('all_page'))

    all_page_s=1
    lastpage_count=0
    if all_count>10:
        all_page_s=all_count/10
        if (all_count%10)>0:
            all_page_s+=1
            lastpage_count=all_count%10
    if(all_page_s>current_page):
        history_s=history_f[(current_page-1)*10:current_page*10]
    elif(all_page==current_page):

        history_s=history_f[(current_page-1)*10:]

    history_r=WorkTaskTemplateSchema(many=True).dump(history_s).data
    for h in history_r:
        info_ext=myjson.loads(h['info_ext'])
        # h.update({'step_count':len(info_ext)})
        h['step_count']=len(info_ext)
    history_r=getTaskTemplatePre(history_r)
    return app.response_class(json.dumps({'info':history_r,'current_page':current_page,'all_page':all_page_s}), mimetype='application/json')

@work.route("/showlog/<int:id>",methods=['GET', 'POST'])
@login_required
def showlog(id):
    task_f=WorkTask.query.filter(WorkTask.id==int(id)).first()
    task_r=WorkTaskSchema().dump(task_f).data
    logs=[]
    if task_f:
        logs=task_f.log.split('@')

    workShow=getWorkShow()
    return render_template("tools/work/log.html",task=task_r,logs=logs,workShow=workShow)

@work.route("/rerun/<int:id>",methods=['GET', 'POST'])
@login_required
def rerun(id):
    task_f=WorkTask.query.filter(WorkTask.id==int(id)).first()
    task_r=WorkTaskSchema().dump(task_f).data

    workShow=getWorkShow()
    return render_template("tools/work/rerun.html",task=task_r,workShow=workShow)

@work.route("/edittask/<int:id>",methods=['GET', 'POST'])
@login_required
def edittask(id):
    task_f=WorkTask.query.filter(WorkTask.id==int(id)).first()
    task_r=WorkTaskSchema().dump(task_f).data
    task_r['json_ext']=''
    task_r['name_ext']=''
    if task_r:
        task_r['json_ext']=myjson.loads(task_r['info_ext'])
        task_r['name_ext']=task_r['name'].split('@')[0]
        for i in task_r['json_ext']:
            i['machine_count']=len(i['machines'])
            i['script_count']=len(i['scripts'])
            i['scripts_ext']=[]
            i['machines_ext']=[]
            for s in i['scripts']:
                script=WorkFileSchema().dump(WorkFile.query.filter(WorkFile.id==int(s)).first()).data
                if script:
                    script['exist']=1
                    i['scripts_ext'].append(script)
                else:
                    script['exist']=0

            for m in i['machines']:
                machine={}
                host=Host.query.filter(Host.id==int(m['id'])).first()
                machine['exist']=1
                if host:
                    machine['ip']=m['ip']
                    machine['id']=host.id

                    machine['hostname']=host.hostname
                    poolhost=PoolHost.query.filter(PoolHost.host_id==host.id).first()
                    if poolhost:
                        pool=Pool.query.filter(Pool.id==poolhost.pool_id).first()
                        if pool:
                            machine['pool']=pool.name
                            dep=Department.query.filter(Department.id==pool.department_id).first()
                            if dep:
                                machine['dep']=dep.name
                            else:
                                machine['exist']=0
                        else:
                            machine['exist']=0
                    else:
                        machine['exist']=0


                    # i['machines_ext'].append(machine)
                else:
                    machine['exist']=0
                i['machines_ext'].append(machine)


    workShow=getWorkShow()
    return render_template("tools/work/editwork.html",task=task_r,workShow=workShow)

@work.route("/edittemplatetask/<int:id>",methods=['GET', 'POST'])
@login_required
def edittemplatetask(id):
    task_f=WorkTaskTemplate.query.filter(WorkTaskTemplate.id==int(id)).first()
    task_r=WorkTaskTemplateSchema().dump(task_f).data
    task_r['json_ext']=''
    task_r['name_ext']=''
    if task_r:
        task_r['json_ext']=myjson.loads(task_r['info_ext'])
        task_r['name_ext']=task_r['name'].split('@')[0]
        for i in task_r['json_ext']:
            i['machine_count']=len(i['machines'])
            i['script_count']=len(i['scripts'])
            i['scripts_ext']=[]
            i['machines_ext']=[]
            for s in i['scripts']:
                script=WorkFileSchema().dump(WorkFile.query.filter(WorkFile.id==int(s)).first()).data
                if script:
                    script['exist']=1
                    i['scripts_ext'].append(script)
                else:
                    script['exist']=0

            for m in i['machines']:
                machine={}
                host=Host.query.filter(Host.id==int(m['id'])).first()
                machine['exist']=1
                if host:
                    machine['ip']=m['ip']
                    machine['id']=host.id

                    machine['hostname']=host.hostname
                    poolhost=PoolHost.query.filter(PoolHost.host_id==host.id).first()
                    if poolhost:
                        pool=Pool.query.filter(Pool.id==poolhost.pool_id).first()
                        if pool:
                            machine['pool']=pool.name
                            dep=Department.query.filter(Department.id==pool.department_id).first()
                            if dep:
                                machine['dep']=dep.name
                            else:
                                machine['exist']=0
                        else:
                            machine['exist']=0
                    else:
                        machine['exist']=0


                    # i['machines_ext'].append(machine)
                else:
                    machine['exist']=0
                i['machines_ext'].append(machine)


    workShow=getWorkShow()
    return render_template("tools/work/editwork.html",task=task_r,workShow=workShow)

@work.route("/worktaskdelete/<int:id>",methods=['GET', 'POST'])
@login_required
def worktaskdelete(id):
    try:
        import re
        intreg=re.compile('^[1-9]\d*$')
        if not intreg.match(str(id)):
            return responsejson(1,"删除失败")
        info=WorkTask.query.filter(WorkTask.id==id).first()

        db.session.delete(info)
        db.session.commit()
        return responsejson(0,"删除成功")
    except Exception,e:
        return responsejson(1,"删除失败")

@work.route("/worktemplatedelete/<int:id>",methods=['GET', 'POST'])
@login_required
def worktemplatedelete(id):
    try:
        import re
        intreg=re.compile('^[1-9]\d*$')
        if not intreg.match(str(id)):
            return responsejson(1,"删除失败")
        info=WorkTaskTemplate.query.filter(WorkTaskTemplate.id==id).first()

        db.session.delete(info)
        db.session.commit()
        return responsejson(0,"删除成功")
    except Exception,e:
        return responsejson(1,"删除失败")

def upgrade_taks_log(task_id,log):
    task_f=WorkTask.query.filter(WorkTask.task_id==task_id).first()
    if task_f:
        task_f.log+=log+'@'
        ISOTIMEFORMAT='%Y-%m-%d %X'
        task_f.end_time=time.strftime(ISOTIMEFORMAT, time.localtime( time.time()))
        db.session.commit()

def upgrade_taks_log_byid(id,log):
    task_f=WorkTask.query.filter(WorkTask.id==id).first()
    if task_f:
        task_f.log+=log+'@'
        ISOTIMEFORMAT='%Y-%m-%d %X'
        task_f.end_time=time.strftime(ISOTIMEFORMAT, time.localtime( time.time()))
        db.session.commit()

def upgrade_job_state(id,state):
    task_f=WorkTask.query.filter(WorkTask.id==id).first()
    if task_f:
        task_f.state=state
        db.session.commit()

@work.route('/mytest',methods=['GET', 'POST'])
@login_required
@permission_required
def mytest():
    return render_template('error.html',status='test',title='test')

@work.route('/test/<int:id>',methods=['GET', 'POST'])
@login_required
@permission_required
def test(id):
    return render_template('error.html',status='test',title='test')