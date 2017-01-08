# -*- coding: utf-8 -*-
from flask import Blueprint, render_template, request, redirect, url_for, flash, make_response
from flask_login import login_required,current_user
import json,re
from sqlalchemy import and_
from application import app,db,fujs
from config import ANSIBLE_BIZTEMP
from models.pool import Pool
from models.log import Log
from .log import addlog
from models.pool_host import PoolHost
from models.host import Host
from models.user import User
from models.tasks import Tasks
from models.follow import Follow
from models.alarm import Alarm
from models.pool_load_ratio import PoolLoadRatio
from models.pool_load_daily import PoolLoadDaily
from models.host_load_ratio import HostLoadRatio
from models.host_load_daily import HostLoadDaily
from views.host import _get_ip,_operation_log as _host_op_log
from views.user import userinfomapping
from views.commandbuild import CommandBuild
from views.functions import responsejson, addalarm, pool_color, host_status_mapping ,visible
from views.user import get_user_id
import time, datetime
from models.user import Department,DepartmentSchema

@app.context_processor
def inject_fujs():
    return dict(fujs=fujs)

pool = Blueprint('pool', __name__)

@pool.route("/",methods=['GET', 'POST'])
@login_required
def index():
    dp_id=1000
    if 'dep' in request.cookies:
        dp_id=request.cookies['dep']
    else:
        dep_id=1000
    show = visible()
    q = request.args.get("q",'')
    if q:
        kw = '%'+q+'%'
        if (int(dp_id)==1000):
            poollist=Pool.query.filter(and_(Pool.search.like(kw),Pool.deleted == Pool.DELETED_NO)).order_by(Pool.id.desc()).all()
        else:
            poollist=Pool.query.filter(and_(Pool.search.like(kw),Pool.deleted == Pool.DELETED_NO,Pool.department_id==int(dp_id) )).order_by(Pool.id.desc()).all()
    else:
        if (int(dp_id)==1000):
            poollist=Pool.query.filter(Pool.deleted == Pool.DELETED_NO ).order_by(Pool.id.desc()).all()
        else:
            poollist=Pool.query.filter(Pool.deleted == Pool.DELETED_NO ,Pool.department_id==int(dp_id)).order_by(Pool.id.desc()).all()
    if poollist:
        userids=find_userids(poollist)
        userlist={}
        if userids:
            userinfo=User.query.filter(User.id.in_(userids)).all()
            if userinfo:
                for item in userinfo:
                    userlist['uid_%s'%item.id]=item.cn_name
        departinfo=Department.query.all()
        departlist={}
        departlist['0']='unknow'
        if departinfo:
            for d in departinfo:
                departlist[str(d.id)]=d.name

        for poolinfo in poollist:
            poolinfo.team_owner_name=userlist['uid_%s'%poolinfo.team_owner]
            poolinfo.ops_owner_name=userlist['uid_%s'%poolinfo.ops_owner]
            poolinfo.biz_owner_name=userlist['uid_%s'%poolinfo.biz_owner]
            try:
                poolinfo.department=departlist[str(poolinfo.department_id)]
            except:
                 poolinfo.department=departlist['0']

    department_info=DepartmentSchema(many=True).dump(Department.query.all()).data

    return render_template("pool/index.html",poollist=poollist,show=show,q=q,department_info=department_info,dp_id=[dp_id])

@pool.route("/search_dp/<int:dp_id>",methods=['GET', 'POST'])
@login_required
def search_dp(dp_id):
    show = visible()
    q = request.args.get("q",'')
    if q:
        kw = '%'+q+'%'
        if (int(dp_id)==1000):
            poollist=Pool.query.filter(and_(Pool.search.like(kw),Pool.deleted == Pool.DELETED_NO)).order_by(Pool.id.desc()).all()
        else:
            poollist=Pool.query.filter(and_(Pool.search.like(kw),Pool.deleted == Pool.DELETED_NO,Pool.department_id==int(dp_id) )).order_by(Pool.id.desc()).all()
    else:
        if (int(dp_id)==1000):
            poollist=Pool.query.filter(Pool.deleted == Pool.DELETED_NO ).order_by(Pool.id.desc()).all()
        else:
            poollist=Pool.query.filter(Pool.deleted == Pool.DELETED_NO ,Pool.department_id==int(dp_id)).order_by(Pool.id.desc()).all()
    if poollist:
        userids=find_userids(poollist)
        userlist={}
        if userids:
            userinfo=User.query.filter(User.id.in_(userids)).all()
            if userinfo:
                for item in userinfo:
                    userlist['uid_%s'%item.id]=item.cn_name
        departinfo=Department.query.all()
        departlist={}
        departlist['0']='unknow'
        if departinfo:
            for d in departinfo:
                departlist[str(d.id)]=d.name

        for poolinfo in poollist:
            poolinfo.team_owner_name=userlist['uid_%s'%poolinfo.team_owner]
            poolinfo.ops_owner_name=userlist['uid_%s'%poolinfo.ops_owner]
            poolinfo.biz_owner_name=userlist['uid_%s'%poolinfo.biz_owner]
            poolinfo.department=departlist[str(poolinfo.department_id)]

    department_info=DepartmentSchema(many=True).dump(Department.query.all()).data

    return render_template("pool/index.html",poollist=poollist,show=show,q=q,department_info=department_info,dp_id=dep_id)

def find_userids(poollist):
    userids = []
    for poolinfo in poollist:
        if poolinfo.ops_owner not in userids:
            userids.append(poolinfo.ops_owner)
        if poolinfo.team_owner not in userids:
            userids.append(poolinfo.team_owner)
        if poolinfo.biz_owner not in userids:
            userids.append(poolinfo.biz_owner)
    return userids

@pool.route("/add",methods=['GET', 'POST'])
@login_required
def add():
    return  pool_add('',type=1)


@pool.route("/<int:id>",methods=["GET","POST"])
@login_required
def pooldetail(id):
    poolinfo=Pool.query.filter(Pool.id==id).first()
    jsonval={}
    if poolinfo:
        userids=[str(poolinfo.ops_owner),str(poolinfo.team_owner),str(poolinfo.biz_owner)]
        userinfo=User.query.filter(User.id.in_(userids)).all()

        userlist={}
        if userinfo:
            for item in userinfo:
              userlist['uid_%s'%item.id]=item.cn_name

        departinfo=Department.query.all()
        departlist={}
        departlist['0']='unknow'
        if departinfo:
            for d in departinfo:
                departlist[str(d.id)]=d.name
        jsonval['id']=poolinfo.id
        jsonval['name']=poolinfo.name
        jsonval['byname']=poolinfo.byname
        jsonval['source']=poolinfo.source
        jsonval['content']=poolinfo.content
        jsonval['note']=poolinfo.note
        jsonval['ops_owner_id']=poolinfo.ops_owner
        jsonval['ops_owner']=userlist['uid_%s'%poolinfo.ops_owner]
        jsonval['team_owner_id']=poolinfo.team_owner
        jsonval['team_owner']=userlist['uid_%s'%poolinfo.team_owner]
        jsonval['biz_owner_id']=poolinfo.biz_owner
        jsonval['biz_owner']=userlist['uid_%s'%poolinfo.biz_owner]

        jsonval['department_id']=poolinfo.department_id
        jsonval['department']=poolinfo.department=departlist[str(poolinfo.department_id)]
    return app.response_class(json.dumps(jsonval), mimetype='application/json')

@pool.route("/modify/<int:id>",methods=["GET","POST"])
@login_required
def modify(id):
    logmsg=""
    code=0
    msg="修改pool成功"
    intreg=re.compile('^\d*$')
    if not intreg.match(str(id)):
        code=1
        msg="修改pool失败:id有问题"
        return responsejson(code,msg)
    info=Pool.query.filter(Pool.id==id).first()
    name=request.form['name'].strip()
    byname=request.form['byname'].strip()
    ops_owner=request.form['ops_owner'].strip()
    ops_owner_id=request.form['ops_owner_id'].strip()
    biz_owner=request.form['biz_owner'].strip()
    biz_owner_id=request.form['biz_owner_id'].strip()
    team_owner=request.form['team_owner'].strip()
    team_owner_id=request.form['team_owner_id'].strip()
    source=request.form['source'].strip()
    content=request.form['content'].strip()
    note=request.form['note'].strip()
    department_id=int(request.form['department_id'].strip())

    if info.name!=name:
        logmsg=logmsg+"name:%s 更改为 %s"%(info.name,name)+","
        info.name=name
    if info.byname!=byname:
        logmsg=logmsg+"byname:%s 更改为 %s"%(info.byname,byname)+","
        info.byname=byname
    if int(info.ops_owner)!=int(ops_owner_id):
        logmsg=logmsg+"ops_owner_id:%s 更改为 %s(%s)"%(info.ops_owner,ops_owner_id,ops_owner)+","
        info.ops_owner=ops_owner_id
    if int(info.biz_owner)!=int(biz_owner_id):
        logmsg=logmsg+"biz_owner_id:%s 更改为 %s(%s)"%(info.biz_owner,biz_owner_id,biz_owner)+","
        info.biz_owner=biz_owner_id
    if int(info.team_owner)!=int(team_owner_id):
        logmsg=logmsg+"team_owner_id:%s 更改为 %s(%s)"%(info.team_owner,team_owner_id,team_owner)+","
        info.team_owner=team_owner_id
    if int(info.source)!=int(source):
        logmsg=logmsg+"source:%s 更改为 %s"%(info.source,source)+","
        info.source=source
    if info.content!=content:
        logmsg=logmsg+"content:%s 更改为 %s"%(info.content,content)+","
        info.content=content
    if info.note!=note:
        logmsg=logmsg+"note:%s 更改为 %s"%(info.note,note)+","
        info.note=note
    if info.department_id!=department_id:
        logmsg=logmsg+"department_id:%s 更改为 %s"%(info.department_id,department_id)+","
        info.department_id=department_id

    if logmsg=="":
        msg="修改成功:pool没有任何修改"
        return responsejson(code,msg)
    else:
        info.updated=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        db.session.commit()
        logmsg="修改pool信息,id:%d %s"%(id,logmsg)
        addlog(logmsg,1)
        return responsejson(code,msg)

@pool.route("/ratio",methods=["GET","POST"])
def poolratios():
    pool_ids = request.form['ids'] or ''
    ids_list = [0]
    if pool_ids:
        tmp_ids_list = pool_ids.split(",")
        for tmp_id in tmp_ids_list:
            tmp_id = int(tmp_id)
            if tmp_id>0:
               ids_list.append(tmp_id)
    #poollist = Pool.query.all()
    today = datetime.date.today()
    begin_time = str(today)+' 00:00:00'
    begin_timestamps = time.mktime(time.strptime(begin_time,'%Y-%m-%d %H:%M:%S'))
    #多减600就是10分钟,为了就是取两个10分钟弥补当前10分钟可能正在计算
    tmp_step = (time.time()-begin_timestamps-600)/600
    hour = '%02d'%int(tmp_step/6)
    minitus = (int(tmp_step%6))*10
    minitus = '%02d'%minitus
    begin_time = str(today)+' %s:%s:00'%(hour,minitus)
    end_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    pools_load = PoolLoadRatio.query.filter(and_(PoolLoadRatio.pool_id.in_(ids_list),PoolLoadRatio.created.between(begin_time,end_time))).order_by(PoolLoadRatio.id.asc()).all()
    pools_load_list = {}
    if pools_load:
        for pool_load in pools_load:
            tmp_pool_id = pool_load.pool_id
            tmp_dic_key = 'poolload_%d'%tmp_pool_id
            pools_load_list[tmp_dic_key] = [int(pool_load.ratio * 100),pool_load.created.strftime('%Y-%m-%d %H:%M'),'']
            pools_load_list[tmp_dic_key][2] = ['%s'%pool_color(pools_load_list[tmp_dic_key][0])]

    code=0
    msg="成功"
    return responsejson(code,msg,[pools_load_list])

@pool.route("/detail/<int:id>",methods=["GET","POST"])
@login_required
def detail(id):
    show = visible({'host_add':"/cmdb/pool/host/add_post",'host_delete':"/cmdb/pool/host/delete_post"})
    pool_host_list=[]
    alarmUids = []
    poolinfo=Pool.query.filter(Pool.id==id).first()
    if not poolinfo:
        redirect(url_for('pool.index'))
    flag = 0
    if "DB" in pool.name:
        flag = 1
    userids=[]
    if poolinfo.ops_owner not in userids:
        if poolinfo.ops_owner not in userids:
            userids.append(poolinfo.ops_owner)
        if poolinfo.team_owner not in userids:
            userids.append(poolinfo.team_owner)
        if poolinfo.biz_owner not in userids:
            userids.append(poolinfo.biz_owner)
    AlarmInFo = Alarm.query.filter(and_(Alarm.type == Alarm.TYPE_POOL,Alarm.target_id == id)).all()
    if AlarmInFo:
        for item_alarm in AlarmInFo:
            if item_alarm.uid not in alarmUids:
                userids.append(item_alarm.uid)
                alarmUids.append(item_alarm.uid)

    userlist=userinfomapping(userids)
    poolinfo.team_owner_name=userlist['uid_%s'%poolinfo.team_owner]
    poolinfo.ops_owner_name=userlist['uid_%s'%poolinfo.ops_owner]
    poolinfo.biz_owner_name=userlist['uid_%s'%poolinfo.biz_owner]

    departinfo=Department.query.all()
    departlist={}
    departlist['0']='unknow'
    if departinfo:
        for d in departinfo:
            departlist[str(d.id)]=d.name

    poolinfo.department=departlist[str(poolinfo.department_id)]

    alarmusers = ""
    if alarmUids:
        for item_uid in alarmUids:
            alarmusers += '%s,'%userlist['uid_%s'%item_uid]
    alarmusers = alarmusers[0:-1]

    hasFollowed=Follow.query.filter(Follow.type == Follow.TYPE_POOL,Follow.uid == current_user.id,Follow.target_id == poolinfo.id).first()
    if hasFollowed:
        poolinfo.followed = 1
    else:
        poolinfo.followed = 0
    hasAlarmed = Alarm.query.filter(Alarm.type == Alarm.TYPE_POOL, Alarm.uid == current_user.id, Alarm.target_id == poolinfo.id).first()
    if hasAlarmed:
        poolinfo.alarmed = 1
    else:
        poolinfo.alarmed = 0

    poolhostlist=PoolHost.query.filter(PoolHost.pool_id==id).all()
    tmphostids=[]

    pool_lbs = {}
    if poolhostlist:
        for item in poolhostlist:
            tmphostids.append(str(item.host_id))
            tmp_pool_key = 'pool_id_%s'%item.pool_id
            if tmp_pool_key not in pool_lbs:
                pool_lbs[tmp_pool_key] = 0
            pool_lbs[tmp_pool_key] += int(item.weight)

    today = datetime.date.today()
    yesterday = today - datetime.timedelta(days=1)
    begin_time = str(today)+' 00:00:00'
    begin_timestamps = time.mktime(time.strptime(begin_time,'%Y-%m-%d %H:%M:%S'))
    #多减600就是10分钟,为了就是取两个10分钟弥补当前10分钟可能正在计算
    tmp_step = (time.time()-begin_timestamps-600)/600
    hour = '%02d'%int(tmp_step/6)
    minitus = (int(tmp_step%6))*10
    minitus = '%02d'%minitus
    begin_time_current = str(today)+' %s:%s:00'%(hour,minitus)
    now_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    yesterday = str(yesterday)+' 00:00:00'
    pool_loads = PoolLoadRatio.query.filter(and_(PoolLoadRatio.pool_id == id,PoolLoadRatio.created.between(begin_time_current,now_time))).order_by(PoolLoadRatio.id.asc()).all() or 0
    pool_load_time = '未知'
    current_pool_load = 0
    if pool_loads:
        for pool_load in pool_loads:
            pool_load_time = pool_load.created.strftime('%Y-%m-%d %H:%M')
            current_pool_load = pool_load.ratio * 100


    max_pool_load = PoolLoadRatio.query.filter(and_(PoolLoadRatio.pool_id == id,PoolLoadRatio.created.between(begin_time,now_time)))\
                         .order_by(PoolLoadRatio.ratio.desc()).limit(1).first() or 0

    max_pool_load_time = '未知'
    if max_pool_load:
        max_pool_load_time = max_pool_load.created.strftime('%Y-%m-%d %H:%M')
        max_pool_load = max_pool_load.ratio * 100
    max_host_load = HostLoadRatio.query.filter(and_(HostLoadRatio.host_id.in_(tmphostids),HostLoadRatio.created.between(begin_time,now_time)))\
                        .order_by(HostLoadRatio.ratio.desc()).limit(1).first() or 0
    max_host_load_time = '未知'

    if max_host_load:
        max_host_load_time = max_host_load.created.strftime('%Y-%m-%d %H:%M')
        max_host_load = max_host_load.ratio * 100

    yes_pool_load = PoolLoadDaily.query.filter(and_(PoolLoadDaily.pool_id == id,PoolLoadDaily.created == yesterday)).first() or 0
    if yes_pool_load:
        yes_pool_load = yes_pool_load.ratio * 100
    yes_host_load = HostLoadDaily.query.filter(and_(HostLoadDaily.host_id.in_(tmphostids),HostLoadDaily.created == yesterday)).first()  or 0
    if yes_host_load:
        yes_host_load = yes_host_load.ratio * 100

    load = {
        'pool_load':[int(current_pool_load),pool_load_time],
        'max_pool_load':[int(max_pool_load),max_pool_load_time],
        'max_host_load':[int(max_host_load),max_host_load_time],
        'yes_pool_load':int(yes_pool_load),
        'yes_host_load':int(yes_host_load)
    }
    if tmphostids:
        hostlist=Host.query.filter(Host.id.in_(tmphostids)).order_by(Host.id.asc()).all()
        host_loads_list = HostLoadRatio.query.filter(and_(HostLoadRatio.host_id.in_(tmphostids),HostLoadRatio.created.between(begin_time_current,now_time)))\
                                    .order_by(HostLoadRatio.id.asc()).all()
        host_loads = {}
        for item_host_load in host_loads_list:
            tmp_host_load_key = 'host_%s'%item_host_load.host_id
            host_loads[tmp_host_load_key] = [item_host_load.ratio,item_host_load.created.strftime('%Y-%m-%d %H:%M')]

        host_mapping = {}
        if hostlist:
            host_idx = 1
            for item in hostlist:
                tmp_mapping_key = 'host_%s'%item.id
                tmp_mapping_item = {}
                tmp_mapping_item['host_id'] = item.id
                tmp_mapping_item['hostname'] = item.hostname
                tmp_mapping_item['cpu'] = item.cpu_descri
                tmp_mapping_item['memory'] = item.memory_descri
                tmp_mapping_item['storage'] = item.storage_descri
                tmp_host_load_key ='host_%s'%item.id
                if  tmp_host_load_key in host_loads:
                    tmp_ratio = int(host_loads[tmp_host_load_key][0]*100)
                    tmp_mapping_item['load'] = '%s%%'%tmp_ratio
                    tmp_mapping_item['updatetime']  = host_loads[tmp_host_load_key][1]
                else:
                    tmp_mapping_item['load'] = '--'
                    tmp_mapping_item['updatetime']  = '未知'
                host_mapping[tmp_mapping_key] = tmp_mapping_item

            for item in poolhostlist:
                tmp_host_info = host_mapping['host_%s'%item.host_id]
                tmp={'id' : item.id,}
                tmp['hostname'] = tmp_host_info['hostname']
                tmp['host_id'] = tmp_host_info['host_id']
                tmp['cpu'] = tmp_host_info['cpu']
                tmp['memory'] = tmp_host_info['memory']
                tmp['storage'] = tmp_host_info['storage']
                tmp['weight'] = item.weight
                tmp['port'] = item.port
                tmp['pool_id'] = item.pool_id
                tmp['load'] = tmp_host_info['load']
                tmp['updatetime']  = tmp_host_info['updatetime']
                tmp['idx'] = host_idx
                tmp_pool_key = 'pool_id_%s'%tmp['pool_id']
                if tmp_pool_key in pool_lbs:
                    tmp_host_lb_ratio = "%.f%%"%(float(tmp['weight'])/float(pool_lbs[tmp_pool_key])*100)
                    tmp['weight_ratio'] = tmp_host_lb_ratio
                host_idx += 1
                pool_host_list.append(tmp)
    return render_template("pool/detail.html",pool_host_list=pool_host_list, poolinfo=poolinfo, show=show, load = load, alarmusers = alarmusers,flag=flag)


@pool.route("/delete/<int:id>",methods=["GET","POST"])
@login_required
def pooldelete(id):
    ans = _pooldelete(id)
    return  responsejson(ans['code'],ans['msg'])


@pool.route("/host/search",methods=["GET","POST"])
@login_required
def hostsearch():
    from sqlalchemy import text
    jsonval=[]
    kw=request.form['keyword']
    if kw:
        kw="%"+kw+"%"
        sql="SELECT a.id,a.hostname from host as a ,ip_address as b where a.primary_ip_id =b.id and (a.hostname like '%"+kw+"%' or b.ipv4 like '"+kw+"')"
        sql=text(sql)
        hostlist=db.engine.execute(sql)
        app.logger.debug(hostlist)
        if hostlist:
            for item in hostlist:
                jsonval.append([item.id,item.hostname])
    return app.response_class(json.dumps(jsonval), mimetype='application/json')


@pool.route("/host/pick/<id>",methods=['POST','GET'])
@login_required
def pickhost(id):
    intreg=re.compile('^[1-9]\d*$')
    if not intreg.match(id):
        return redirect(url_for('pool.index'))
    poolinfo=Pool.query.filter(Pool.id==id).first()
    if not poolinfo:
        return redirect(url_for('pool.index'))
    poolhost = PoolHost.query.filter(PoolHost.pool_id == id).all()
    hostids = [0]
    if pooldetail:
        for item_poolhost in poolhost:
            hostids.append(item_poolhost.host_id)
    #hostlist=Host.query.filter(and_(Host.status==Host.STATUS_READY,Host.deleted == Host.DELETED_NO)).all()
    hostlist=Host.query.filter(and_(Host.deleted == Host.DELETED_NO,Host.id.notin_(hostids))).all()
    if hostlist:
        for host in hostlist:
            host.ip = _get_ip(host.primary_ip_id)
    return render_template("pool/pickhost.html",hostlist=hostlist,poolinfo=poolinfo)


@pool.route("/host/add",methods=['POST'])
@login_required
def hostadd():
    code=0
    msg="为pool添加主机成功"
    host_ids=request.form['host_ids']
    pool_id=request.form['pool_id']
    intreg=re.compile('^[1-9]\d*$')
    host_ids=host_ids.split(",")
    if len(host_ids)<=0:
        code=1
        msg="操作提示:为pool添加主机失败,主机编号格式不对"
        return responsejson(code,msg)
    if not intreg.match(pool_id):
        code=1
        msg="操作提示:为pool添加主机失败,pool编号格式不对"
        return responsejson(code,msg)
    poolinfo=Pool.query.filter(Pool.id==pool_id).first()
    if not poolinfo:
        code=1
        msg="操作提示:为pool添加主机失败,pool不存在"
        return responsejson(code,msg)
    logmsg=""
    for host_id in host_ids:
        hostinfo=Host.query.filter(Host.id==host_id).first()
        if not hostinfo:
            continue
        hasIn=PoolHost.query.filter(and_(PoolHost.pool_id==pool_id,PoolHost.host_id==host_id)).all()
        if hasIn:
            continue

        poolhosttarget=PoolHost(pool_id,host_id)
        db.session.add(poolhosttarget)
        db.session.commit()
        log_data = {}
        log_data['pooladd'] = "添加主机入POOL,<a href='/cmdb/pool/detail/%s'>%s</a>"%(poolinfo.id,poolinfo.name)
        uid = 0
        if current_user:
            uid = current_user.id
        log = json.dumps(log_data, ensure_ascii=False, separators=(',', ':')).encode('utf8')
        _host_op_log(hostinfo.id,uid,log)

        tmp_host_status = Host.STATUS_ASSIGNED
        if poolinfo.source > 0:
            tmp_host_status = Host.STATUS_ONLINE

        if int(tmp_host_status) > int(hostinfo.status):
            log_data = {}
            log_data['status'] = '主机状态:从 %s 更改为 %s '%(host_status_mapping(hostinfo.status),host_status_mapping(tmp_host_status))
            hostinfo.status = tmp_host_status
            db.session.commit()
            log = json.dumps(log_data, ensure_ascii=False, separators=(',', ':')).encode('utf8')
            _host_op_log(hostinfo.id,uid,log)

        logmsg="%s,主机编号:%s  name:%s"%(logmsg,host_id,hostinfo.hostname)

    if logmsg:
        logmsg=" 在%s添加主机%s"%(poolinfo.name,logmsg)
        addlog(logmsg,1)
    else:
        code=1
        msg="操作提示:没有添加任何主机(所选主机已经添加了)"
    return responsejson(code,msg)

@pool.route("/check_pool_host",methods=['POST','GET'])
@login_required
def check_host_pool():
    data = {'hostid':int(request.form['hostid']),'poolid':int(request.form['poolid'])}
    ans = _check_host_pool(data,type = 2)
    return responsejson(ans['code'],ans['msg'],ans['data'])


@pool.route("/host/delete",methods=['POST'])
@login_required
def hostdelete():
    data = {'pool_id':request.form['pid'],'id':request.form['id']}
    ans =  _host_delete(data)
    return responsejson(ans['code'],ans['msg'])

@pool.route("/ratio/download",methods=['POST','GET'])
@login_required
def ratio_download():
    from models.device import Device
    from models.supplier import Supplier
    from models.rack import Rack
    from models.datacenter import Datacenter
    from models.pool import Pool
    from models.pool_host import PoolHost
    from models.host import Host
    from views.device import ExportExcel
    type= request.args.get("type","host")
    if type == "host":
        suppliers_dic = {}
        dc_rack_dic = {}
        device_dic = {}
        host_dic = {}
        pool_dic = {}
        host_pool_dic = {}
        suppliers_list = Supplier.query.all()
        suppliers_dic[0] = '未知'
        for item in suppliers_list:
            suppliers_dic[item.id] = item.short_name

        dc_rack_list = db.session.query(Rack.id,Rack.name,Datacenter.name).filter(Rack.datacenter_id == Datacenter.id).all()
        dc_rack_dic[0] = '未知'
        for item in dc_rack_list:
            dc_rack_dic[item[0]] = "%s/%s"%(item[2],item[1])

        device_list = Device.query.filter(Device.deleted == 0).all()
        device_dic[0] = {
            'device_label':'未知',
            'supply':'未知',
            'model':'未知',
            'dc_rack':'未知',
            'dt':'未知',
            'cpu':'未知',
            'memory':'未知',
            'storage':'未知',
        }
        for item in device_list:
            device_dic[item.id] = {
                'device_label':item.device_label,
                'supply':suppliers_dic[item.supplier_id],
                'model':item.model,
                'dc_rack':dc_rack_dic[item.rack_id],
                'dt':item.buy_time.strftime('%Y-%m-%d'),
                'cpu':item.cpu,
                'memory':item.memory,
                'storage':item.storage
            }

        pool_list = Pool.query.all()
        for item in pool_list:
            pool_dic[item.id] = item.name

        host_pool_list = PoolHost.query.filter(PoolHost.pool_id>0).all()
        tmp_max = 0
        for item in host_pool_list:
            tmp_host_id = item.host_id
            tmp_pool_id = item.pool_id
            if tmp_host_id not in host_pool_dic:
                 host_pool_dic[tmp_host_id] = []
            host_pool_dic[tmp_host_id].append('%s'%pool_dic[tmp_pool_id])
            if len(host_pool_dic[tmp_host_id])>tmp_max:
                tmp_max = len(host_pool_dic[tmp_host_id])


        host_list = Host.query.filter(Host.deleted == Host.DELETED_NO).all()
        for item in host_list:
            host_dic[item.id] = [item.device_id,item.parent_id,item.type,item.hostname]

        days15 = calHostRatio(15)
        days7 = calHostRatio(7)

        contents = []
        for item_host_id,item_content in host_dic.items():
            device_id = item_content[0]
            if item_content[1]>0:
                device_id = host_dic[item_content[1]][0]

            tmp_deivce_info = device_dic[device_id]
            tmp_pool = ['未知']
            if item_host_id in host_pool_dic:
                tmp_pool = host_pool_dic[item_host_id]
            tmp_day15 = 0
            if item_host_id in days15:
                tmp_day15 = days15[item_host_id]
            tmp_day7 = 0
            if item_host_id in days7:
                tmp_day7 = days7[item_host_id]

            content = [
                item_content[3],
                tmp_deivce_info['device_label'],
                tmp_deivce_info['dc_rack'],
                tmp_deivce_info['supply'],
                tmp_deivce_info['model'],
                tmp_deivce_info['cpu'],
                tmp_deivce_info['memory'],
                tmp_deivce_info['storage'],
                tmp_deivce_info['dt'],
                '%d'%int(float('%.2f'%(tmp_day7/7))*100),
                '%d'%int(float('%.2f'%(tmp_day15/15))*100),
                ",".join(tmp_pool)
            ]
            contents.append(content)


        head = ('主机名','资产编号','机房/机柜','品牌','型号','CPU','内存','硬盘','购买时间','7','15','pool')
        excel = ExportExcel()
        value = excel.exportexcel('Sheet1',head,contents)
        return make_response(value, 200, {'Content-type': 'application/vnd.ms-excel',
                                                   'Content-Disposition': 'attachment;filename="host.xls"'})
    elif type == "pool":
        days15 = calPoolRatio(15)
        days7 = calPoolRatio(7)
        days1 = calPoolRatio(1)
        pool_lists = Pool.query.all()
        head = ('POOL名称','来源','昨日满载率','7天平均满载率','15天平均满载率')
        excel = ExportExcel()
        contents = []
        for item_pool in pool_lists:
            tmp_pool_name = item_pool.name
            tmp_pool_id = item_pool.id
            tmp_day15 = 0
            if tmp_pool_id in days15:
                tmp_day15 = days15[tmp_pool_id]
            tmp_day7 = 0
            if tmp_pool_id in days7:
                tmp_day7 = days7[tmp_pool_id]
            tmp_day1 = 0
            if tmp_pool_id in days1:
                tmp_day1 = days1[tmp_pool_id]
            content = [
                tmp_pool_name,
                item_pool.source_desc,
                '%d'%int(float('%.2f'%(tmp_day1/1))*100),
                '%d'%int(float('%.2f'%(tmp_day7/7))*100),
                '%d'%int(float('%.2f'%(tmp_day15/15))*100)
            ]
            contents.append(content)
        value = excel.exportexcel('Sheet1',head,contents)
        return make_response(value, 200, {'Content-type': 'application/vnd.ms-excel',
                                                   'Content-Disposition': 'attachment;filename="pool.xls"'})
def calHostRatio(pre_days):
    import datetime
    from models.host_load_daily import HostLoadDaily
    end_date = datetime.date.today() - datetime.timedelta(days=1)
    from_date = datetime.date.today() - datetime.timedelta(days=(pre_days))
    end_date = '%s 00:00:00'%end_date
    from_date = '%s 00:00:00'%from_date
    host_loads_list = HostLoadDaily.query.filter(HostLoadDaily.created.between(from_date,end_date)).all()
    host_loads_dic = {}
    for item in  host_loads_list:
        tmp_host_id = item.host_id
        if tmp_host_id not in host_loads_dic:
            host_loads_dic[tmp_host_id] = 0
        host_loads_dic[tmp_host_id] += item.ratio

    return host_loads_dic

def calPoolRatio(pre_days):
    import datetime
    from models.pool_load_daily import PoolLoadDaily
    end_date = datetime.date.today() - datetime.timedelta(days=1)
    from_date = datetime.date.today() - datetime.timedelta(days=(pre_days))
    end_date = '%s 00:00:00'%end_date
    from_date = '%s 00:00:00'%from_date
    pool_loads_list = PoolLoadDaily.query.filter(PoolLoadDaily.created.between(from_date,end_date)).all()
    pool_loads_dic = {}
    for item in  pool_loads_list:
        tmp_pool_id = item.pool_id
        if tmp_pool_id not in pool_loads_dic:
            pool_loads_dic[tmp_pool_id] = 0
        pool_loads_dic[tmp_pool_id] += item.ratio

    return pool_loads_dic



def get_ansible_passwd():
    filetarget = open('%s/password'%ANSIBLE_BIZTEMP, 'r')
    content=filetarget.read()
    filetarget.close()
    return content

def pool_add(data="",type=0):
    code=0
    msg="添加pool成功"
    if type == 0:
        ops_user = "vincentguo"
        ops_owner_id = get_user_id(ops_user)
        team_owner_id = 0
        biz_owner_id = 0
        name = data['name']
        byname = data['byname']
        source = data['source']
        note=""
        content=""
    else:
        name=request.form['name'].strip()
        byname=request.form['byname'].strip()
        ops_owner=request.form['ops_owner'].strip()
        ops_owner_id=request.form['ops_owner_id'].strip()
        biz_owner=request.form['biz_owner'].strip()
        biz_owner_id=request.form['biz_owner_id'].strip()
        team_owner=request.form['team_owner'].strip()
        team_owner_id=request.form['team_owner_id'].strip()
        source=request.form['source'].strip()
        content=request.form['content'].strip()
        note=request.form['note'].strip()
        department_id=int(request.form['department_id'].strip())
        if len(name)<=0:
            code=1
            msg="请输入pool名称"
        if len(ops_owner)<=0 or len(ops_owner_id)<=0:
            code=1
            msg="请输入ops负责人"
            return responsejson(code,msg)
        if len(team_owner)<=0 or len(team_owner_id)<=0:
            code=1
            msg="请输入pool负责人"
            return responsejson(code,msg)
        if len(biz_owner)<=0 or len(biz_owner_id)<=0:
            code=1
            msg="请输入业务负责人"
            return responsejson(code,msg)
        if len(content)<=0:
            code=1
            msg="请输入pool业务描述"
            return responsejson(code,msg)

    pooldetail=Pool.query.filter(and_(Pool.name==name,Pool.byname == byname, Pool.source == source)).first()
    if pooldetail:
        if type == 0:
            return {'code':code,'msg':msg}
        else:
            code=1
            msg="pool名称已经存在"
            return responsejson(code,msg)
    pooltarget=Pool(name,ops_owner_id,team_owner_id,biz_owner_id,note=note,content=content, byname = byname, source = source,department_id=department_id)
    db.session.add(pooltarget)
    db.session.commit()
    addalarm(ops_owner_id, Alarm.TYPE_POOL, pooltarget.id)
    addalarm(biz_owner_id, Alarm.TYPE_POOL, pooltarget.id)
    addalarm(team_owner_id, Alarm.TYPE_POOL, pooltarget.id)
    logmsg=" 添加pool,id : %d,name : %s"%(pooltarget.id,name)
    addlog(logmsg,7)
    if type == 0:
        return {'code':code,'msg':msg}
    else:
        return responsejson(code, msg)

def get_pool_id(pool_name="",type=""):
    if pool_name and type:
        Pool_info = Pool.query.filter(and_(Pool.name == pool_name,Pool.source == type)).first()
        if Pool_info :
            return Pool_info.id
        else:
            return 0

def get_pool_host_id(pool_id="",host_id=""):
    ans = PoolHost.query.filter(and_(PoolHost.host_id == host_id,PoolHost.pool_id == pool_id)).first()
    return  ans.id


def modify_pool_host(data,type=1):
    if data:
        code = 1
        msg = "success"
        pool_id = get_pool_id(data['pool_name'],data['source'])
        pool_host_info = PoolHost.query.filter(and_(PoolHost.pool_id == pool_id,PoolHost.host_id == data['host_id'])).first()
        host_info = Host.query.filter(Host.id == data['host_id']).first()
        host_name = host_info.hostname
        if type == 1:
            pool_host_info.port = data['port']
            pool_host_info.weight = data['weight']
            db.session.add(pool_host_info)
            db.session.commit()
            logmsg = "修改pool:%s,%s,weight:%s.port:%s"%(data['pool_name'],host_name,data['weight'],data['port'])
            addlog(logmsg,1)
        if type == 2:
            info = PoolHost(pool_id,data['host_id'],data['weight'],data['port'],data['source'])
            db.session.add(info)
            db.session.commit()
            logmsg=",主机编号:%s  name:%s"%(data['host_id'],host_name)
            logmsg=" 在%s添加主机%s"%(data['pool_name'],logmsg)
            addlog(logmsg,1)
            log_data = {}
            log_data['pooladd'] = "添加主机入POOL,<a href='/cmdb/pool/detail/%s'>%s</a>"%(pool_id,data['pool_name'])
            uid = 0
            if current_user:
                uid = current_user.id
            log = json.dumps(log_data, ensure_ascii=False, separators=(',', ':')).encode('utf8')
            _host_op_log(host_info.id,uid,log)
            #修改主机状态
            tmp_host_status = Host.STATUS_ASSIGNED
            if int(data['source']) > 0:
                host_info.status = Host.STATUS_ONLINE
            if int(host_info.status) < int(tmp_host_status):
                log_data = {}
                log_data['status'] = '主机状态:从 %s 更改为 %s '%(host_status_mapping(host_info.status),host_status_mapping(tmp_host_status))
                host_info.status = tmp_host_status
                db.session.commit()
                log = json.dumps(log_data, ensure_ascii=False, separators=(',', ':')).encode('utf8')
                _host_op_log(host_info.id,uid,log)

        res = {'code':code,'msg':msg}
        return  res

def _host_delete(data=""):
    code = 0
    msg="移除主机成功"
    id = str(data['id'])
    pool_id = str(data['pool_id'])
    intreg=re.compile('^[1-9]\d*$')
    if not intreg.match(id) or not intreg.match(pool_id):
        code=1
        msg="操作提示:移除主机失败"
    info=PoolHost.query.filter(and_(PoolHost.id==id,PoolHost.pool_id==pool_id)).first()
    if info :
        hostinfo=Host.query.filter(Host.id==info.host_id).first()
        db.session.delete(info)
        db.session.commit()
        logmsg="删除pool主机,pool_id:%s,host_id:%s name:%s"%(pool_id,info.host_id,hostinfo.hostname)
        addlog(logmsg,1)

        log_data = {}
        log_data['remove'] = "从<a href='/cmdb/pool/detail/%s'>POOL</a>移除主机"%pool_id
        uid = 0
        if current_user:
            uid = current_user.id
        log = json.dumps(log_data, ensure_ascii=False, separators=(',', ':')).encode('utf8')
        _host_op_log(hostinfo.id,uid,log)

        if hostinfo:#修改主机状态
            other_pool_info = PoolHost.query.filter(PoolHost.host_id == info.host_id).all()
            other_pool_ids = []
            for item in other_pool_info:
                other_pool_ids.append(item.pool_id)
            tmp_count = Pool.query.filter(and_(Pool.id.in_(other_pool_ids),Pool.source>0)).count()
            tmp_host_status = Host.STATUS_ASSIGNED
            if tmp_count>0:
                tmp_host_status =  Host.STATUS_ONLINE
            if int(hostinfo.status) != int(tmp_host_status):
                log_data = {}
                log_data['status'] = '主机状态:从 %s 更改为 %s '%(host_status_mapping(hostinfo.status),host_status_mapping(tmp_host_status))
                hostinfo.status = tmp_host_status
                db.session.commit()
                uid = 0
                if current_user:
                    uid = current_user.id
                log = json.dumps(log_data, ensure_ascii=False, separators=(',', ':')).encode('utf8')
                _host_op_log(hostinfo.id,uid,log)

    res = {'code':code,'msg':msg}
    return  res

def _check_host_pool(info,type = 1):#type 1=>job 2=>web
    code = 1
    msg = "success"
    hostid = info['hostid']
    poolid = info['poolid']
    pool_host = PoolHost.query.filter(PoolHost.host_id == hostid).all()
    hostname = Host.query.filter(Host.id == hostid).first().hostname
    num = len(pool_host)
    if num > 1:
        data = ""
    else:
        if type == 1:
            code = 0
            msg = "host only in one pool"
            data = ""
        elif type == 2:
            data = [hostname]
            pool_info = []
            all_pool_info = Pool.query.filter(Pool.deleted == Pool.DELETED_NO ).all()
            for item in all_pool_info:
                if item.id != poolid:
                    info = str(item.id) + '_'+ item.name+ item.source_desc
                    pool_info.append(info)
            code = 0
            msg = "host only in one pool"
            data.append(pool_info)
    res = {'code':code,'msg':msg,'data':data}
    return res

def _pooldelete(id):
    code=0
    msg="删除成功"
    intreg=re.compile('^[1-9]\d*$')
    if not intreg.match(str(id)):
        code=1
        msg="删除失败"
        return responsejson(code,msg)
    poolinfo=Pool.query.filter(Pool.id==id).first()
    if poolinfo:
        rows=PoolHost.query.filter(PoolHost.pool_id==id).count()
        if rows == 0:
            poolinfo.deleted = Pool.DELETED_YES
            db.session.commit()
            logmsg="删除pool信息,name:%s,id:%d"%(poolinfo.name,id)
            addlog(logmsg,1)
        else:
            code=1
            msg="删除失败,此pool下有关联的主机,请先移除主机"
    res = {'code':code,'msg':msg}
    return res

def get_pool_info(**kwargs):
    if 'id' in kwargs:
        return Pool.query.filter(Pool.id == kwargs['id']).first()
    elif 'ids' in kwargs:
        pools_dic = {}
        pools_info = Pool.query.filter(Pool.id.in_(kwargs['ids'])).all()
        if pools_info:
            for item in pools_info:
                pools_dic[item.id] = item
        return pools_dic
