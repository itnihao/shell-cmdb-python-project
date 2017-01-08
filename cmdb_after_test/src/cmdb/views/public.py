#-*- coding: UTF-8 -*-
import json,time
from flask import Blueprint, render_template, request, url_for, make_response
from flask_login import login_required,current_user
from sqlalchemy import or_,and_,desc
from models.sa.tickets import Tickets
from models.sa.tickets_task import Tickets_Task
from models.sa.tickets_category import Tickets_Category
from models.device import Device
from models.host import Host
from models.pool import Pool
from models.pool_host import PoolHost
from models.apply import Apply
from models.user import User
from models.user_host import UserHost
from models.host_bastion_apply import HostBastionApply
from views.user import get_user_info
from views.host import get_host_info
from application import app, db
from apis.zabbixAPI import ZABBIX_API

public = Blueprint('public', __name__)

@public.route("/")
@login_required
def index():
    device_count = Device.query.filter(Device.deleted == Device.DELETED_NO).count()
    host_count = Host.query.filter(Host.deleted == Host.DELETED_NO).count()
    pool_count = Pool.query.filter(Pool.deleted == Pool.DELETED_NO).count()
    applying_info = [] #申请
    approving_info = [] #任务
    cat_dic = {} # task分类
    entrance = [] #常见入口
    triggers = []
    #申请进度:主机申请,权限申请,工单需求
    uid = current_user.id
    tickets_info =  Tickets.query.filter(and_(Tickets.uid == uid,Tickets.status == Tickets.STATUS_OPEN)).order_by(Tickets.id.desc()).all()
    cat_list = Tickets_Category.query.all()
    if cat_list:
        for cat_item in cat_list:
            cat_dic[cat_item.id] = cat_item

    if tickets_info:
        tickets_id = []
        tickets_tasks_dic = {}
        for tickets_item in tickets_info:
            tickets_id.append(tickets_item.id)
        tickets_tasks_info = Tickets_Task.query.filter(Tickets_Task.tickets_id.in_(tickets_id)).all()
        for tickets_tasks_item in tickets_tasks_info:
            tmp_tickets_id = tickets_tasks_item.tickets_id
            if tmp_tickets_id not in tickets_tasks_dic:
                tickets_tasks_dic[tmp_tickets_id] = []
            tickets_tasks_dic[tmp_tickets_id].append(tickets_tasks_item.tickets_cat_id)

        for tickets_item in tickets_info:
            tickets_item.cat_name = ''
            tickets_item.process_status = 'info' if tickets_item.status == 1 else 'success'
            if tickets_item.id in tickets_tasks_dic:
                for tmp_tickets_cat_id in tickets_tasks_dic[tickets_item.id]:
                    tmp_cat_dic = cat_dic[tmp_tickets_cat_id]
                    tmp_cat_name = tmp_cat_dic.name if  tmp_cat_dic.name == tmp_cat_dic.label else '%s-%s'%(tmp_cat_dic.label,tmp_cat_dic.name)
                    tickets_item.cat_name += tmp_cat_name + ","
                tickets_item.cat_name = tickets_item.cat_name[:-1]
            applying_info.append({
                'type':'[工单]',
                'desc':'分类:%s'%tickets_item.cat_name,
                'process':tickets_item.status_desc,
                'href':url_for('tickets.detail',id = tickets_item.id)
            })

    bastion_apply_info = HostBastionApply.query.filter(
        and_(HostBastionApply.uid == uid,HostBastionApply.status.in_([HostBastionApply.STATUS_APPROVING,HostBastionApply.STATUS_RUNNING])))\
        .all()
    if bastion_apply_info:
        host_ids = []
        for bastion_apply_item in bastion_apply_info:
            host_ids.append(bastion_apply_item.host_id)
            hosts_info_mapping = get_host_info(ids = host_ids)
        for bastion_apply_item in bastion_apply_info:
            approvings=[]
            if bastion_apply_item.status==HostBastionApply.STATUS_APPROVING:
                approver_system_id=app.config.get("APPROVER")['host']
                if approver_system_id!=bastion_apply_item.approve_uid:
                    approving_cnname=User.query.filter(User.id==bastion_apply_item.approve_uid).first().cn_name
                    approving={'approve_name':approving_cnname,'status':'审批中'}
                    approvings.append(approving)
                    approving_cnname=User.query.filter(User.id==approver_system_id).first().cn_name
                    approving={'approve_name':approving_cnname,'status':'待审批'}
                    approvings.append(approving)
                else:
                    superior_id=User.query.filter(User.id==bastion_apply_item.uid).first().superior_id
                    user_superior=User.query.filter(User.id==superior_id).first()
                    if user_superior.id != approver_system_id:
                        approving={'approve_name':user_superior.cn_name,'status':'已审批'}
                        approvings.append(approving)
                    approving_cnname=User.query.filter(User.id==approver_system_id).first().cn_name
                    approving={'approve_name':approving_cnname,'status':'审批中'}
                    approvings.append(approving)
            applying_info.append({
                'type':'[权限申请]',
                'desc':'主机名:%s 用户:%s'%(hosts_info_mapping[bastion_apply_item.host_id].hostname,bastion_apply_item.role_status),
                'process':bastion_apply_item.apply_status,
                'href':url_for('user.mypapply'),
                'approvings':approvings
            })

    host_apply_info = Apply.query.filter(and_(Apply.uid == uid,Apply.status.in_([Apply.STATUS_APPROVING,Apply.STATUS_RUNNING]))).all()
    if host_apply_info:
        approver_uid = app.config.get("APPROVER")['host']
        for host_apply_item in host_apply_info:
            approvings=[]
            if host_apply_item.status==Apply.STATUS_APPROVING:
                approver_system_id=app.config.get("APPROVER")['host']
                if approver_system_id!=host_apply_item.approver_uid:
                    approving_cnname=User.query.filter(User.id==host_apply_item.approver_uid).first().cn_name
                    approving={'approve_name':approving_cnname,'status':'审批中'}
                    approvings.append(approving)
                    approving_cnname=User.query.filter(User.id==approver_system_id).first().cn_name
                    approving={'approve_name':approving_cnname,'status':'待审批'}
                    approvings.append(approving)
                else:
                    superior_id=User.query.filter(User.id==host_apply_item.uid).first().superior_id
                    user_superior=User.query.filter(User.id==superior_id).first()
                    if user_superior.id != approver_system_id:
                        approving={'approve_name':user_superior.cn_name,'status':'已审批'}
                        approvings.append(approving)
                    approving_cnname=User.query.filter(User.id==approver_system_id).first().cn_name
                    approving={'approve_name':approving_cnname,'status':'审批中'}
                    approvings.append(approving)
            tmp_desc = eval(host_apply_item.template)
            applying_info.append({
                'type':'[主机申请]',
                'desc':'%s核/%sG/%sG/%s'%(str(tmp_desc['cpu']),str(tmp_desc['mem']),str(tmp_desc['disk']),str(tmp_desc['os'])),
                'process':host_apply_item.status_desc,
                'href':url_for('user.myhapply'),
                'approvings':approvings
            })

    #我的审批 权限审批 和 主机审批, SA任务
    bastion_approve_info = HostBastionApply.query.filter(
        and_(HostBastionApply.approve_uid == uid,HostBastionApply.status == HostBastionApply.STATUS_APPROVING))\
        .all()
    if bastion_approve_info:
        host_ids = []
        for bastion_approve_item in bastion_approve_info:
            host_ids.append(bastion_approve_item.host_id)
            hosts_info_mapping = get_host_info(ids = host_ids)
        for bastion_approve_item in bastion_approve_info:
            approvings=[]
            if bastion_approve_item.status==HostBastionApply.STATUS_APPROVING:
                approver_system_id=app.config.get("APPROVER")['host']
                if approver_system_id!=bastion_approve_item.approve_uid:
                    approving_cnname=User.query.filter(User.id==bastion_approve_item.approve_uid).first().cn_name
                    approving={'approve_name':approving_cnname,'status':'审批中'}
                    approvings.append(approving)
                    approving_cnname=User.query.filter(User.id==approver_system_id).first().cn_name
                    approving={'approve_name':approving_cnname,'status':'待审批'}
                    approvings.append(approving)
                else:
                    superior_id=User.query.filter(User.id==bastion_approve_item.uid).first().superior_id
                    user_superior=User.query.filter(User.id==superior_id).first()
                    if user_superior.id != approver_system_id:
                        approving={'approve_name':user_superior.cn_name,'status':'已审批'}
                        approvings.append(approving)
                    approving_cnname=User.query.filter(User.id==approver_system_id).first().cn_name
                    approving={'approve_name':approving_cnname,'status':'审批中'}
                    approvings.append(approving)
            approving_info.append({
                'type':'[权限申请]',
                'desc':'主机名:%s 用户:%s'%(hosts_info_mapping[bastion_approve_item.host_id].hostname,bastion_approve_item.role_status),
                'process':bastion_approve_item.apply_status,
                'href':url_for('user.papproval'),
                'approvings':approvings
            })
    host_approve_info = Apply.query.filter(and_(Apply.approver_uid == uid,Apply.status == Apply.STATUS_APPROVING)).all()
    if host_approve_info:
        for host_approve_item in host_approve_info:
            tmp_desc = eval(host_approve_item.template)
            approvings=[]
            if host_approve_item.status==Apply.STATUS_APPROVING:
                approver_system_id=app.config.get("APPROVER")['host']
                if approver_system_id!=host_approve_item.approver_uid:
                    approving_cnname=User.query.filter(User.id==host_approve_item.approver_uid).first().cn_name
                    approving={'approve_name':approving_cnname,'status':'审批中'}
                    approvings.append(approving)
                    approving_cnname=User.query.filter(User.id==approver_system_id).first().cn_name
                    approving={'approve_name':approving_cnname,'status':'待审批'}
                    approvings.append(approving)
                else:
                    superior_id=User.query.filter(User.id==host_approve_item.uid).first().superior_id
                    user_superior=User.query.filter(User.id==superior_id).first()
                    if user_superior.id != approver_system_id:
                        approving={'approve_name':user_superior.cn_name,'status':'已审批'}
                        approvings.append(approving)
                    approving_cnname=User.query.filter(User.id==approver_system_id).first().cn_name
                    approving={'approve_name':approving_cnname,'status':'审批中'}
                    approvings.append(approving)
            approving_info.append({
                'type':'[主机申请]',
                'desc':'%s核/%sG/%sG/%s'%(str(tmp_desc['cpu']),str(tmp_desc['mem']),str(tmp_desc['disk']),str(tmp_desc['os'])),
                'process':host_approve_item.status_desc,
                'href':url_for('user.happroval'),
                'approvings':approvings
            })
    tickets_tasks_handle_info = Tickets_Task.query.filter(and_(Tickets_Task.manage_uid == uid, Tickets_Task.status == Tickets_Task.STATUS_OPEN)).all()
    if tickets_tasks_handle_info:
        for tickets_tasks_handle_item in tickets_tasks_handle_info:
            tmp_cat_dic = cat_dic[tickets_tasks_handle_item.tickets_cat_id]
            tmp_cat_name = tmp_cat_dic.name if  tmp_cat_dic.name == tmp_cat_dic.label else '%s-%s'%(tmp_cat_dic.label,tmp_cat_dic.name)
            approving_info.append({
                'type':'[工单]',
                'desc':tmp_cat_name,
                'title': tickets_tasks_handle_item.content,
                'process':tickets_tasks_handle_item.status_desc,
                'href':url_for('tickets.detail',id = tickets_tasks_handle_item.tickets_id)
            })
    #常见入口
    tmp_entrance = {'desc':'我想找运维做事情','href':url_for('tickets.add'),'type':'提工单'}
    entrance.append(tmp_entrance)
    tmp_entrance = {'desc':'我想登录线上机器','href':url_for('bastion.index',id = 0),'type':'申请权限'}
    entrance.append(tmp_entrance)
    tmp_entrance = {'desc':'我想申请主机','href':url_for('host.apply',id = 0),'type':'申请主机'}
    entrance.append(tmp_entrance)
    tmp_entrance = {'desc':'我要申请域名','href':url_for('dns.apply'),'type':'申请域名'}
    entrance.append(tmp_entrance)

    extend = {
        'host_count': host_count if host_count else 0,
        'device_count': device_count if device_count else 0,
        'pool_count': pool_count if pool_count else 0,
        'applying_info':applying_info,
        'approving_info':approving_info,
        'entrance':entrance
        # 'triggers':datas
    }
    return render_template("index/public.html",extend = extend, count = len)

@public.route("/get_zabbix_triggers",methods=["GET","POST"])
@login_required
def get_zabbix_triggers():
    try:
        zabbix = ZABBIX_API()
        if zabbix.connect():
            triggers = zabbix.get_triggers()
            datas = []
            cur_time = int(time.time())
            for trigger in triggers:
                data = {}
                # data['hostname'] = trigger['hostname'].strip().replace('web','').replace('ops','').replace('kvm','').replace('hd','').replace('db','')
                data['hostname'] = trigger['hostname'].strip()
                n = data['hostname'].index("tjtx")
                data['hostname'] = data['hostname'][n:]
                data['description'] = trigger['description'].replace('{HOST.NAME}',data['hostname'])
                data['url'] = trigger['url']
                longer = cur_time - int(trigger['lastchange'])
                day = int(longer / 86400)
                hour = int((longer % 86400) / 3600)
                min = int((longer % 86400) % 3600) / 60
                if day != 0:
                    data['longer'] = '%d天 %d时 %d分'%(day,hour,min)
                elif hour != 0:
                    data['longer'] = '%d时 %d分'%(hour,min)
                else:
                    data['longer'] = '%d分'%(min)
                host = Host.query.filter(Host.hostname == data['hostname']).first()
                if not host:
                    print 'Can\'t canvert hostname: %s'% trigger['hostname']
                    continue
                pool_host = PoolHost.query.filter(PoolHost.host_id == host.id).first()
                pool = Pool.query.filter(Pool.id == pool_host.pool_id).first()
                user = User.query.filter(User.id == pool.ops_owner).first()
                data['pool'] = pool.name
                data['user'] = user.cn_name
                data['host_id'] = host.id
                data['pool_id'] = pool.id
                datas.append(data)
            zabbix.disconnect()
    except:
        return make_response(json.dumps([]))
    return make_response(json.dumps(datas))


@public.route("/list")
@login_required
def list():
    return "列表页需要认证"
