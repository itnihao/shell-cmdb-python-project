# -*- coding: utf-8 -*-

from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import login_required, current_user
from application import app, db
from models.host import Host
from models.user import User
from models.host_bastion_apply import HostBastionApply
from models.user_host import UserHost
from models.host_bastion_tasks import HostBastionTasks
from models.sshkey import Sshkey
from models.pool import Pool
from models.pool_host import PoolHost
from views.functions import addmail
from config import DOMAIN
from sqlalchemy import and_
from pypages import Paginator
import re, json
import datetime
import urllib

bastion = Blueprint('bastion', __name__)


@bastion.route("/<int:id>", methods = ['GET', 'POST'])
@login_required
def index(id=0):
    type = int(request.args.get('type',0))
    target_id = 0
    target_name = ""
    if type == 1:
        host = Host.query.filter(Host.id == id).first()
        if host:
            target_name = host.hostname
            target_id = host.id
    elif type == 2:
        pool = Pool.query.filter(Pool.id == id).first()
        if pool:
            target_name = pool.name
            target_id = pool.id

    approval_dic = {'uid':0} #默认不需要审批
    if 7 <= current_user.p_level < 99 or 4 <= current_user.m_level < 99:
        pass
    else: #需要审批
        approval = __get_superior(current_user.id,type)
        approval_dic['uid'] = approval.id
        approval_dic['name'] = approval.cn_name

    department = current_user.department_id
    haskey = 0
    pub_key = Sshkey.query.filter(Sshkey.uid == current_user.id).all()
    if pub_key:
        haskey = 1
    root_approver_uid = app.config.get("APPROVER")['host']
    tipmsg = ''
    if root_approver_uid:
        approver_info = User.query.filter(User.id == root_approver_uid).first()
        approver_info=__get_superior(current_user.id)
        if approver_info:
            tipmsg = "PS:root权限需要%s审批,审核通过后1-2分钟开通"%approver_info.cn_name
    extend_info = {
        'type':type,
        'hostname':target_name,
        'host_id':target_id,
        'department':department,
        'haskey':haskey,
        'tipmsg':tipmsg
    }
    return render_template('/bastion/index.html',approval=approval_dic, extend_info=extend_info )

@bastion.route("/apply",methods=['POST','GET'])
@login_required
def allapply():
    from views.pool import get_pool_info
    from views.host import get_host_info
    per_page = 50
    range_num = 10
    p = request.args.get('p',1)
    target = HostBastionApply.query.filter()
    total_num = target.count()
    page = Paginator(total_num, per_page=per_page, current=p, range_num=range_num)
    target_info = target.order_by(HostBastionApply.id.desc()).offset((int(p) - 1) * per_page).limit(per_page).all()
    apply_list = []
    for item in target_info:
        if item.type == HostBastionApply.TYPE_HOST:
            name = get_host_info(id=item.host_id).hostname
        else:
            name = get_pool_info(id=item.host_id).name
        cn_name = User.query.filter(User.id == item.uid).first().cn_name
        apply_dict = {
            "type":item.type,
            "target_id":item.host_id,
            "name": name,
            "days": item.days,
            "content_all": item.content,
            "content_len": len(item.content),
            "content": item.content[:15],
            "created": item.created,
            "id": item.id,
            "role": item.role_status,
            "status": item.apply_status,
            "status_id":item.status,
            "cn_name": cn_name
        }
        apply_list.append(apply_dict)
    return render_template("/bastion/apply.html", apply_list=apply_list, p=page)

def __get_superior(user_id,roles=0):
    if roles == 1:
        approval_root_uid = app.config.get("APPROVER")['host']
        user=User.query.filter(User.id == approval_root_uid).first()
        return user
    user = User.query.filter(User.id == user_id).first()
    if user:
        if 7 <= user.p_level < 99 or 4 <= user.m_level < 99:
            return user
        else :
            user=User.query.filter(User.id == user.superior_id).first()
            if user.p_level<6 and user.m_level<4:
                return __get_superior(0,1)
            return user

@bastion.route("/tokeninput", methods=['POST', 'GET'])
def hostname():
    ignoreHosts = ['ajk_login']
    is_ops = 0
    if current_user.department_id == 160:
        is_ops = 1
    arg = '%'+request.args.get('q')+'%'
    result = []
    if current_user.department_id == 160 or current_user.department_id == 562:
        hosts = Host.query.filter(and_(Host.search.like(arg),Host.deleted == Host.DELETED_NO)).limit(10).all()
        pools = Pool.query.filter(and_(Pool.search.like(arg),Pool.deleted == Pool.DELETED_NO)).limit(10).all()
    else:
        hosts = Host.query.filter(and_(Host.search.like(arg),Host.hostname.notlike("db%"),Host.deleted == Host.DELETED_NO)).limit(10).all()
        pools = Pool.query.filter(and_(Pool.search.like(arg),Pool.name != 'DB',Pool.deleted == Pool.DELETED_NO)).limit(10).all()
    if hosts:
        for host in hosts:
            tmp_hostname = host.hostname
            if tmp_hostname in ignoreHosts:
                continue
            if not is_ops:
                m = re.match('^(lb|apc)',tmp_hostname.lower())
                if m:
                    continue

            result.append({"id":host.id, "name":host.hostname,"type":HostBastionApply.TYPE_HOST})
    if pools:
        for pool in pools:
            result.append({"id":pool.id, "name":pool.name,"type":HostBastionApply.TYPE_POOL})

    return app.response_class(json.dumps(result), mimetype='application/json')


@bastion.route("/addbastion", methods=['POST', 'GET'])
def addbastion():
    from views.pool import get_pool_info
    from views.host import get_host_info
    host_ids = request.form.getlist('host_id[]')
    pool_ids = request.form.getlist('pool_id[]')
    roles = request.form['roles']
    days = request.form['days']
    content = request.form['content']
    id = request.form['host_id']
    if len(host_ids) <= 0 and len(pool_ids) <= 0:
        msg = urllib.urlencode({'msg':1})
        return redirect(url_for('bastion.index',id=id)+'?'+msg)
    if len(roles) <= 0:
        msg = urllib.urlencode({'msg':2})
        return redirect(url_for('bastion.index',id=id)+'?'+msg)
    if len(days) <= 0:
        msg = urllib.urlencode({'msg':3})
        return redirect(url_for('bastion.index',id=id)+'?'+msg)
    if len(content) <= 0:
        msg = urllib.urlencode({'msg':4})
        return redirect(url_for('bastion.index',id=id)+'?'+msg)
    approval = __get_superior(current_user.id,int(roles))
    approval_uid = approval.id
    approval_root_uid = app.config.get("APPROVER")['host']

    if approval_uid == current_user.id: #免审
        if int(roles) == 1 and int(current_user.id) != approval_root_uid: #root
            #approval_uid = approval_root_uid
            status = HostBastionApply.STATUS_APPROVING
        else:
            status = HostBastionApply.STATUS_RUNNING
    else:
        status = HostBastionApply.STATUS_APPROVING
    names = []
    for pool_id in pool_ids:
        apply_pool_target = HostBastionApply(current_user.id,HostBastionApply.TYPE_POOL,pool_id,roles,approval_uid,status,days,content)
        db.session.add(apply_pool_target)
        db.session.commit()
        if status == HostBastionApply.STATUS_RUNNING:
            all_task(apply_pool_target)
        names.append(get_pool_info(id=pool_id).name)
    hostnames = []
    for host_id in host_ids:
        hasIn = UserHost.query.filter(and_(UserHost.uid == current_user.id,UserHost.host_id == host_id,UserHost.role == roles,UserHost.status == UserHost.STATUS_VALID)).first()
        if hasIn:
            if len(host_ids) == 1:
                msg = urllib.urlencode({'msg':5})
                return redirect(url_for('bastion.index',id=id)+'?'+msg)
            else:
                continue
        apply_host_target = HostBastionApply(current_user.id,HostBastionApply.TYPE_HOST,host_id,roles,approval_uid,status,days,content)
        db.session.add(apply_host_target)
        db.session.commit()

        if status == HostBastionApply.STATUS_RUNNING:
            all_task(apply_host_target)

        names.append(get_host_info(id=host_id).hostname)

    if approval_uid != current_user.id:

        userinfo = User.query.filter(User.id == approval_uid).first()
        applier = User.query.filter(User.id == current_user.id).first()
        subject = "【堡垒机权限】 " + applier.cn_name + ' 申请堡垒机权限，待审批'
        names = ",".join(names)
        content = applier.cn_name + '申请堡垒机权限，名称为：' + names + '<br/><a href=' + DOMAIN + url_for('user.papproval') + '>点击此处</a>进行审批'
        addmail(userinfo.email, subject, content)

    return redirect(url_for('user.mypapply'))

def add_authority(uid,type,host_id,role,approve_uid,status,time,content):
    apply_target = HostBastionApply(uid,type,host_id,role,approve_uid,status,time,content)
    db.session.add(apply_target)
    db.session.commit()
    all_task(apply_target)

def all_task(apply_target):
    add_exec_time = datetime.datetime.now()
    delete_exec_time = add_exec_time + datetime.timedelta(days=apply_target.days)
    if apply_target.type == HostBastionApply.TYPE_HOST:
        add_task(apply_target.id,apply_target.uid,apply_target.host_id,apply_target.role,HostBastionTasks.TYPE_ADD,HostBastionTasks.STATUS_FREE,add_exec_time,delete_exec_time)

    elif apply_target.type == HostBastionApply.TYPE_POOL:
        poolhost = PoolHost.query.filter(PoolHost.pool_id == apply_target.host_id).all()
        for item in poolhost:
            add_task(apply_target.id,apply_target.uid,item.host_id,apply_target.role,HostBastionTasks.TYPE_ADD,HostBastionTasks.STATUS_FREE,add_exec_time,delete_exec_time)

def add_task(apply_target_id,uid,host_id,role,type,status,add_exec_time,delete_exec_time):
    userhost = UserHost.query.filter(and_(UserHost.host_id == host_id,UserHost.uid == uid,UserHost.role == role,UserHost.status == UserHost.STATUS_VALID)).first()
    if not userhost:
        target_add = HostBastionTasks(apply_target_id,uid,host_id,role,HostBastionTasks.TYPE_ADD,HostBastionTasks.STATUS_FREE,add_exec_time)
        db.session.add(target_add)
    hasIn = HostBastionTasks.query.filter(and_(HostBastionTasks.uid == uid,HostBastionTasks.host_id == host_id,HostBastionTasks.role == role,HostBastionTasks.type == HostBastionTasks.TYPE_DELETE)).first()
    if hasIn:
        if hasIn.exec_time < delete_exec_time:
            hasIn.exec_time = delete_exec_time
    else:
        target_delete = HostBastionTasks(apply_target_id,uid,host_id,role,HostBastionTasks.TYPE_DELETE,HostBastionTasks.STATUS_FREE,delete_exec_time)
        db.session.add(target_delete)
    db.session.commit()