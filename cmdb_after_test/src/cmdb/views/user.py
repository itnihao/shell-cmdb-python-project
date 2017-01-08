#-*- coding: UTF-8 -*-
from flask import Blueprint, redirect, json, request, make_response,render_template,flash,url_for
from flask_login import login_user, logout_user, login_required,current_user
from application import app, db
from models.follow import Follow
from models.host import Host
from models.user import User
from models.user_role import UserRole
from models.role_action import RoleAction
from models.role import Role
from models.action import Action
from sqlalchemy import or_,and_,desc
from models.pool import Pool
from models.ip_address import IpAddress
from models.alarm import Alarm
from models.sshkey import Sshkey
from models.rack import Rack
from models.datacenter import Datacenter
from models.host_bastion_apply import HostBastionApply
from models.host_bastion_tasks import HostBastionTasks
from models.sa.tickets_task import Tickets_Task
from models.user_host import UserHost
from models.pubkey_changed_queue import PubkeyChangedQueue
from models.dns.dns_apply import DnsApply
from models.dns.dns_zone import DnsZone
from views.functions import oa_interface,responsejson,visible
from pypages import Paginator
from models.apply import Apply
from models.apply_host import Apply_host
from models.apply_host_tasks import ApplyHostTasks
from views.functions import addmail as add_mail
from views.host import get_host_info

import urllib,urllib2,datetime
import tasks
import re
user = Blueprint('user', __name__)

@user.route('/login')
def login():
    try:
        code = request.args.get('code')
        if code is None:
            return _auth()
        else:
            token_url = app.config['AUTH_URL']+'/login/token'
            data = urllib.urlencode({'client_id': app.config['AUTH_ID'], 'client_secret': app.config['AUTH_SECRET'], 'code': code})
            req = urllib2.Request(token_url, data)
            response = urllib2.urlopen(req)
            access_token = response.read().split("&")[0].split("=")[1]
            req = urllib2.Request(app.config['AUTH_URL']+'/user')
            req.add_header('Authorization', 'bearer '+access_token)
            resource = urllib2.urlopen(req).read()
            auth_user = json.loads(resource)[0]
            user_info = User.query.filter(User.name == auth_user['username']).first()

            # ew_auth_user = oa_interface(auth_user['username'],superior=1)

            if user_info is None:
                new_auth_user = oa_interface(auth_user['username'],superior=1)
                superior_id = 0
                if new_auth_user['data']['superior']:
                    superior_name = new_auth_user['data']['superior']['domain_account']
                    superior_info = User.query.filter(User.name == superior_name).first()
                    if superior_info:
                        superior_id = superior_info.id

                user_info = insert_user_info(access_token,new_auth_user['data'],superior_id)
                init_user_role(new_auth_user['data']['user_id'])
            else:
                tasks.update_user_info.delay(user_info.id, auth_user, access_token)
            response = make_response(redirect('/'))
            secure_token = create_token(user_info.id, user_info.name, request.user_agent)
            secure_token = secure_token + 'QQ' + str(user_info.id)
            response.set_cookie('secure_token', value=secure_token, max_age=2592000)
            login_user(user_info)
        return response
    except Exception,e:
        print e.message

def insert_user_info(access_token,auth_user,superior_id=0):
    target = User('',auth_user['user_id'], auth_user['user_name'], auth_user['domain_account'], auth_user['user_code'],auth_user['office_mail'],
        auth_user['cellphone'], auth_user['job_status'],datetime.datetime.now(), datetime.datetime.now(),superior_id,
        auth_user['p_level'],auth_user['m_level'],auth_user['department_id'],auth_user['department_name'],auth_user['function_id'],
        auth_user['function_name'])
    db.session.add(target)
    db.session.commit()
    return target


def init_user_role(oauth_id):
     userid  = User.query.filter(User.oauth_id == int(oauth_id)).first()
     userrole = UserRole(user_id = userid.id,role_id = 2)
     db.session.add(userrole)
     db.session.commit()

@user.route('/logout')
@login_required
def logout():
    logout_user()
    response = make_response(redirect('/'))
    response.set_cookie('secure_token', '', 0)
    return response


@user.route("/search",methods=['GET', 'POST'])
@login_required
def search():
    jsonval=[]
    keyword=request.form['keyword']
    user_info = User.query.filter(and_(or_(User.cn_name.like('%'+keyword+'%'),User.name.like('%'+keyword+'%')),User.status==0)).all()
    if user_info:
        for item in user_info:
            jsonval.append([item.id,item.cn_name])
    return app.response_class(json.dumps(jsonval), mimetype='application/json')

def userinfomapping(userids):
    userlist={}
    if userids:
        userinfo=User.query.filter(User.id.in_(userids)).all()
        if userinfo:
            for item in userinfo:
                userlist['uid_%s'%item.id]=item.cn_name
    return userlist

def _auth():
    return redirect(app.config['AUTH_URL'] + "/login/authorize?client_id="+app.config['AUTH_ID'])


def create_token(id, user_name, user_agent):
    import hashlib
    m = hashlib.md5()
    m.update(str(id) + user_name + str(user_agent))
    return m.hexdigest()


def match_user_cookie(secure_cookie, user_agent):
    secure_user_id = secure_cookie.split('QQ')
    user = User.query.filter(User.id == secure_user_id[1]).first()
    if user:
        comb_cookie = create_token(user.id, user.name, user_agent)
        if comb_cookie == secure_user_id[0]:
            return user.id
    return None

@user.route("/ucenter", methods=['GET', 'POST'])
@login_required
def ucenter():
    type = request.args.get("type","info")
    sshkey = Sshkey.query.filter(Sshkey.uid == current_user.id).all()
    userinfo = User.query.filter(User.id == current_user.id).first()
    str = userinfo.email
    email = str.replace(',','\n')
    return render_template("ucenter/ucenter.html", email=email, sshkey=sshkey, type=type)


@user.route("/ucenter/email/add", methods=['POST','GET'])
@login_required
def addemail():
    email = request.form['mail']
    email = email.replace('\r\n','\n').replace('\r','\n')
    strreg = re.compile('^(([a-zA-Z0-9_\.\-])+\@(([a-zA-Z0-9\-])+\.)+([a-zA-Z0-9]{2,4})+(\n)*)+$')
    if strreg.match(email):
        email = email.split('\n')
        mail = list(set(email))
        mail.sort(key=email.index)
        newemail = ",".join(mail)
        userinfo = User.query.filter(User.id == current_user.id).first()
        userinfo.email = newemail
        db.session.commit()
        flash("保存成功", 1)
        return redirect(url_for('user.ucenter'))
    else:
        msg = "邮箱有误，请重新输入"
        flash(msg, 0)
        return redirect(url_for('user.ucenter'))


@user.route("/ucenter/sshkey/add", methods=['POST'])
@login_required
def addkey():
    code = 0
    msg = "添加成功"
    if request.method == 'POST':
        name = request.form['name']
        key = request.form['content']
        if len(name) <= 0:
            code = 1
            msg = "请输入name"
            return responsejson(code, msg)
        if len(key) <= 0:
            code = 1
            msg = "请输入key"
            return responsejson(code, msg)
        key_parts = key.strip().split(None, 3)
        if len(key_parts) < 2:
            code = 1
            msg = "请输入合法key"
            return responsejson(code, msg)
        key_type = key_parts[0]
        if key_type not in ["ssh-rsa","ssh-dss"]:
            code = 1
            msg = "请输入合法key"
            return responsejson(code, msg)
        hasIn = Sshkey.query.filter(and_(Sshkey.name == name, Sshkey.key == key)).first()
        if hasIn:
            code = 1
            msg = "此key已存在"
            return responsejson(code, msg)
        sshkeytarget = Sshkey(current_user.id, name, key)
        db.session.add(sshkeytarget)
        db.session.commit()
        pubkeytarget = PubkeyChangedQueue(current_user.id)
        db.session.add(pubkeytarget)
        db.session.commit()
    else:
        code = 1
        msg = "添加失败"
    return responsejson(code, msg)

@user.route("/ucenter/sshkey/delete/<int:id>", methods=['POST'])
@login_required
def deletekey(id):
    deleteinfo = Sshkey.query.filter(Sshkey.id == id).first()
    if deleteinfo:
        db.session.delete(deleteinfo)
        db.session.commit()
        pubkeytarget = PubkeyChangedQueue(current_user.id)
        db.session.add(pubkeytarget)
        db.session.commit()
    return responsejson(0, "删除成功")

@user.route('/follow')
@login_required
def follow():
    #Finding hosts
    followdHost = db.session.query(Follow.id,Host).filter(and_(Follow.uid == current_user.id,Follow.target_id==Host.id, Follow.type==2)) .all();

    #Finding pool
    followdPool = db.session.query(Follow.id,Pool).filter(and_(Follow.uid == current_user.id,Follow.target_id==Pool.id, Follow.type==1)) .all();

    #Finding rack
    followdRack = db.session.query(Follow.id,Rack).filter(and_(Follow.uid == current_user.id,Follow.target_id==Rack.id, Follow.type==3)) .all();

    __host = [];
    __pool = [];
    __userID = [];
    __rack = [];
    #parsing pool data, extract own ids
    for x,v in followdPool:
        __userID.append(v.ops_owner);
        __userID.append(v.team_owner);
        __userID.append(v.biz_owner);
        v.fid = x;
        __pool.append(v);

    #sort user ids and fetching details from models
    __userID = {}.fromkeys(__userID).keys();
    userinfo=User.query.filter(User.id.in_(__userID)).all();

    __userHash = {};
    for x in userinfo:
        __userHash[x.id] = x.cn_name;

    #parsing host data
    for x,v in followdHost:
        v.fid = x;
        v.ipv4 = _get_ip( v.primary_ip_id )
        __host.append(v);

    num = 0
    for x,v in followdRack:
        info = Datacenter.query.filter(Datacenter.id == v.datacenter_id).first()
        if info:
            num +=1
            idc_name = info.name
            height   = v.height
            info = {'rack_name':v.name,'idc_name':idc_name,'height':height,'num':num,'id':v.id}
            __rack.append(info)

    return render_template("follow/follow_index_tpl.html",followdHost=__host,users=__userHash,followdPool=__pool,followdRack=__rack)

def _get_ip(id):
    ip_info = IpAddress.query.filter(IpAddress.id == id).first()
    return ip_info and ip_info.ipv4 or 0;



@user.route('/actFollow',methods=['post','get'])
@login_required
def actFollow():
    #this method only accepts post
    target_type = request.form['type'].strip();
    target_id = request.form['id'];
    action_type = request.form['act']

    #validate posted data
    if '' == target_type.strip() or '' == target_id.strip() or int(target_id) <=0:
        return jsonRender(-111,'Parameter error');

    if action_type =='unfollow':
        unfollow(current_user.id,target_type,target_id)
        return jsonRender(data={"reload":1});

    followed  = Follow.query.filter(and_(Follow.uid == current_user.id, Follow.type == target_type, Follow.target_id ==target_id)).all()
    if followed :
        return jsonRender(-113,'您已经关注了当前信息,如要取消关注,可<a href="'+url_for('monitor.index')+'">进入关注列表</a>取消!');
    objFollow = Follow(target_type,target_id);
    db.session.add(objFollow);
    db.session.commit();

    return jsonRender(0,'操作已更新');


@user.route('/alarm')
@login_required
def alarm():
    #Finding hosts
    alarmHost = db.session.query(Alarm.id, Host).filter(and_(Alarm.uid == current_user.id, Alarm.target_id == Host.id, Alarm.type == 2)).all()

    #Finding pool
    alarmPool = db.session.query(Alarm.id, Pool).filter(and_(Alarm.uid == current_user.id, Alarm.target_id == Pool.id, Alarm.type == 1)).all()

    __host = []
    __pool = []
    __userID = []
    #parsing pool data, extract own ids
    for x, v in alarmPool:
        __userID.append(v.ops_owner)
        __userID.append(v.team_owner)
        __userID.append(v.biz_owner)
        v.fid = x
        __pool.append(v)

    #sort user ids and fetching details from models
    __userID = {}.fromkeys(__userID).keys()
    userinfo = User.query.filter(User.id.in_(__userID)).all()

    __userHash = {}
    for x in userinfo:
        __userHash[x.id] = x.cn_name

    #parsing host data
    for x, v in alarmHost:
        v.fid = x
        v.ipv4 = _get_ip(v.primary_ip_id)
        __host.append(v)
    return render_template("alarm/alarm.html", alarmHost=__host, users=__userHash, alarmPool=__pool)


@user.route('/mypapply')
@login_required
def mypapply():
    per_page = 50
    range_num = 10
    p = request.args.get('p',1)
    mypapply = HostBastionApply.query.filter(HostBastionApply.uid == current_user.id)
    sshkey_apply = mypapply.order_by(HostBastionApply.id.desc()).offset((int(p) - 1) * per_page).limit(per_page).all()
    total_num = mypapply.count()
    page = Paginator(total_num, per_page=per_page, current=p, range_num=range_num)
    apply_list = []
    i = 0
    from views.pool import get_pool_info
    for item in sshkey_apply:
        i += 1
        if item.type == HostBastionApply.TYPE_HOST:
            name = get_host_info(id=item.host_id).hostname
        else:
            name = get_pool_info(id=item.host_id).name
        apply_dict = {
            "type":item.type,
            "target_id": item.host_id,
            "name": name,
            "days":item.days,
            "content_all": item.content,
            "content_len": len(item.content),
            "content": item.content[:15],
            "created": item.created,
            "id": i,
            "role": item.role_status,
            "status": item.apply_status,
            "status_id":item.status,
            "note":item.note,
        }
        apply_list.append(apply_dict)
    return render_template("ucenter/myapply.html",info=apply_list,p=page,flag="mypapply")

@user.route('/myhapply')
@login_required
def myhapply():
    apply_list = []
    per_page = 50
    range_num = 10
    p = request.args.get('p',1)
    total_num = Apply.query.filter(Apply.uid == current_user.id).count()
    page = Paginator(total_num, per_page=per_page, current=p, range_num=range_num)
    apply = Apply.query.filter(Apply.uid == current_user.id).order_by(desc(Apply.id)).offset((int(p) - 1) * per_page).limit(per_page).all()
    i = 0
    if apply:
        for info in apply:
            i += 1
            host_type = info.type_desc
            idc =  info.idc_desc
            note=info.note
            pool_info = Pool.query.filter(Pool.id == info.pool_id).first()
            pool_name = pool_info.source_desc + pool_info.name
            pool_id = pool_info.id
            config_info = eval(info.template)
            os =  config_info['os']
            config = str(config_info['cpu'])+'核/'+str(config_info['mem'])+'G/'+str(config_info['disk'])+'G</br>'+ os
            apply_host_info = Apply_host.query.filter(and_(Apply_host.apply_id == info.id,Apply_host.status == 3)).all()
            hostinfo = []
            for item in apply_host_info:
                host_info = Host.query.filter(Host.id == item.host_id).first()
                tmp = host_info.hostname + '</br>'
                hostinfo.append({tmp:host_info.id})
            status = info.status_desc
            status_id = info.status
            num =  info.num
            date = info.created
            content = info.content
            apply_list.append({'id':i,'pool_id':pool_id,'status_id':status_id,'status':status,'type':host_type,
                               'host_info':hostinfo,'idc':idc,'pool':pool_name,
                               'config':config,'num':num,'date':date,'content':content,'note':note}),
    return render_template('ucenter/myapply.html',info=apply_list,p=page,flag='myhapply')

@user.route('/mydapply')
@login_required
def mydapply():
    per_page = 50
    range_num = 10
    p = request.args.get('p',1)
    uid = current_user.id
    office_domain = app.config.get("SELF_DOMAIN")
    zone_infos = DnsZone.query.all()
    zone_dic = {}
    for zone_item in zone_infos:
        zone_dic[zone_item.id] = zone_item

    #target = db.session.query(DnsApply,DnsZone.zone,User.cn_name).filter(and_(DnsApply.uid == current_user.id,DnsZone.id == DnsApply.zone_id,User.id == current_user.id,DnsApply.deleted == DnsApply.DELETED_NO))
    target = DnsApply.query.filter(and_(DnsApply.uid == uid,DnsApply.deleted == DnsApply.DELETED_NO))
    apply_info = target.order_by(DnsApply.id.desc()).offset((int(p) - 1) * per_page).limit(per_page).all()
    total_num = target.count()
    page = Paginator(total_num, per_page=per_page, current=p, range_num=range_num)
    apply_list = []
    applylists = []
    uids = []
    for item in apply_info:
        uids.append(item.uid)
        uids.append(item.approve_uid)
    user_mapping = get_user_info(uids=uids)
    if apply_info:
        for item in apply_info:
            tmp_uinfo = user_mapping[item.uid]
            tmp_approve_info = user_mapping[item.approve_uid]
            tmp_zone_info = zone_dic[item.zone_id]
            tmp_dns_info = {
                    'id': item.id,
                    'zone': tmp_zone_info.zone,
                    'applier_name': tmp_uinfo.cn_name,
                    'prefix': item.prefix,
                    'type': item.type_descri,
                    'ip_domain': item.value,
                    'content_part' : item.content[:15],
                    'content_len' : len(item.content),
                    'content': item.content,
                    'apply_time': item.updated,
                    'status_descri': item.status_descri,
                    'status': item.status,
                    'approver': tmp_approve_info.cn_name
            }
            if tmp_zone_info.zone == office_domain:
                applylists.append(tmp_dns_info)
            else:
                apply_list.append(tmp_dns_info)

        for item in apply_list:
            applylists.append(item)

    return render_template('ucenter/myapply.html',flag='mydapply',p=page,apply_list=applylists)

@user.route('/myhost')
@login_required
def myhost():
    myhost_info = db.session.query(Host.hostname,UserHost).filter(and_(UserHost.uid == current_user.id),UserHost.host_id == Host.id).all()
    myhost_list = []
    i = 0
    for item in myhost_info:
        i += 1
        myhost_dict = {
            "id": i,
            "host_id": item.UserHost.host_id,
            "hostname": item.hostname,
            "role": item.UserHost.role_status,
            "status": item.UserHost.myhost_status,
            "status_id": item.UserHost.status,
            "created": item.UserHost.created
        }
        myhost_list.append(myhost_dict)
    return render_template("host/list.html",myhost_list = myhost_list,flag='myhost')


@user.route('/actAlarm',methods=['post','get'])
@login_required
def actAlarm():
    target_type = request.form['type']
    target_id = request.form['id']
    action_type = request.form['act']

    if '' == target_type.strip() or '' == target_id.strip() or int(target_id) <= 0:
        return jsonRender(-111, 'Parameter error')

    if action_type == 'unalarm':
        unalarm(current_user.id,target_type,target_id)
        return jsonRender(data={"reload":1})
    alarmed = Alarm.query.filter(and_(Alarm.uid == current_user.id, Alarm.type == target_type, Alarm.target_id == target_id)).all()
    if alarmed:
        return jsonRender(-113, '您已经接警了当前信息')

    alarmtarget = Alarm(target_type, target_id, uid = current_user.id)
    db.session.add(alarmtarget)
    db.session.commit()

    return jsonRender(0, '操作已更新')

@user.route('/papproval',methods=['post','get'])
@login_required
def papproval():
    per_page = 50
    range_num = 10
    p = request.args.get('p',1)
    target = HostBastionApply.query.filter(HostBastionApply.approve_uid == current_user.id)
    total_num = target.count()
    page = Paginator(total_num, per_page=per_page, current=p, range_num=range_num)
    myapprovals = target.order_by(HostBastionApply.id.desc()).offset((int(p) - 1) * per_page).limit(per_page).all()
    approval_list = []
    idx = 1
    from views.pool import get_pool_info
    for myapproval in myapprovals:
        if myapproval.type == HostBastionApply.TYPE_HOST:
            name = get_host_info(id=myapproval.host_id).hostname
        else:
            name = get_pool_info(id=myapproval.host_id).name
        tmp = {
            'id':myapproval.id,
            'type':myapproval.type,
            'target_id':myapproval.host_id,
            'role':myapproval.role_status,
            'content':myapproval.content,
            'days':myapproval.days,
            'short_content':myapproval.content[:15],
            'status':myapproval.status,
            'hostid':myapproval.host_id,
            'name':name,
            'created':myapproval.created
        }
        if len(tmp['content'])>15:
            tmp['short_content'] += '...'

        user = User.query.filter(User.id == myapproval.uid).first()
        tmp['cn_name'] = user.cn_name
        tmp['idx'] = idx
        idx += 1
        approval_list.append(tmp)

    return render_template('ucenter/approval.html',info=approval_list,p=page,flag="papproval")

@user.route('/happroval',methods=['post','get'])
@login_required
def happroval():
    approver_uid = app.config.get("APPROVER")['host']
    superior_info = User.query.filter(User.superior_id == current_user.id).first()
    if not superior_info and approver_uid != current_user.id:
        return redirect(url_for('host.index'))
    per_page = 50
    range_num = 10
    p = request.args.get('p',1)
    total_num = Apply.query.count()
    apply = Apply.query.filter(and_(Apply.status == 1, Apply.approver_uid == current_user.id)).order_by(Apply.id.desc()).offset((int(p) - 1) * per_page).limit(per_page).all()
    if current_user.id == approver_uid:
        apply = Apply.query.order_by(Apply.id.desc()).offset((int(p) - 1) * per_page).limit(per_page).all()
    page = Paginator(total_num, per_page=per_page, current=p, range_num=range_num)
    apply_info = []
    if apply:
        lines = 0
        for info in apply:
            type_id = info.type
            id = info.id
            idc_id = info.idc
            username = User.query.filter(User.id == info.uid).first().cn_name
            host_type = info.type_desc
            idc = info.idc_desc
            pool_info = Pool.query.filter(Pool.id == info.pool_id).first()
            config_info = eval(info.template)
            os =  config_info['os']
            config = str(config_info['cpu'])+'核/'+str(config_info['mem'])+'G/'+str(config_info['disk'])+'G</br>'+ os
            cpu = config_info['cpu']
            mem = config_info['mem']
            disk = config_info['disk']
            pool_id = pool_info.id
            status = info.status
            num =  info.num
            date = info.created
            content = info.content
            short_content = info.content[:33]
            pool_name = pool_info.source_desc + str(pool_info.name)
            content_len = len(info.content)
            approver_id=info.approver_uid
            note=info.note
            lines += 1
            apply_info.append({'id':id,'idc_id':idc_id,'cpu':cpu,'mem':mem,'disk':disk,'pool_id':pool_id,'status':status,'type_id':type_id,'name':username,'type':host_type,'idc':idc,
                               'config':config,'num':num,'date':date,'short_content':short_content,'content_len':content_len,'lines':lines,
                               'pool_name':pool_name,'content':content,'approver_id':approver_id,'note':note})
    return render_template('ucenter/approval.html',info=apply_info,flag="happroval",p=page,current_user_id=current_user.id)

@user.route('/msg',methods=['get','post'])
@login_required
def msg():
    from views.sa.dns import find_self_domain
    remote_addr = request.remote_addr
    uid = current_user.id
    find_self_domain(remote_addr,current_user.name)
    bastion_count = HostBastionApply.query.filter(and_(HostBastionApply.status == HostBastionApply.STATUS_APPROVING, HostBastionApply.approve_uid == uid)).count()
    host_count = Apply.query.filter(and_(Apply.uid == uid,Apply.status == Apply.STATUS_APPROVING)).count()
    if current_user.is_sa:
        sa_ticket_count = Tickets_Task.query.filter(and_(Tickets_Task.manage_uid == uid, Tickets_Task.status == Tickets_Task.STATUS_OPEN)).count()
    else:
        sa_ticket_count = 0
    data={
        'bastion':bastion_count,
        'host':host_count,
        'ticket_count':sa_ticket_count
    }
    return responsejson(code=0,msg="success",data=data)

@user.route('/add_bastiontasks/<int:id>',methods=['post','get'])
@login_required
def add_bastiontasks(id):
    from views.bastion import all_task
    code = 0
    msg = "任务添加成功"
    flag = request.form['flag']
    item = HostBastionApply.query.filter(HostBastionApply.id == id).first()
    if flag == '1':
        approver_uid = app.config.get("APPROVER")['host']
        if item.role == 1: #root
            if current_user.id != approver_uid:
                item.approve_uid = approver_uid
                db.session.commit()
                return responsejson(code, msg)

        item.status = HostBastionApply.STATUS_RUNNING
        db.session.commit()
        all_task(item)
    else:
        item.status = HostBastionApply.STATUS_REJECT
        db.session.commit()
    return responsejson(code, msg)

@user.route('/reject_apply/',methods=['post','get'])
@login_required
def reject_apply():
    code=0
    msg="操作成功"
    apply_id=request.form['id']
    note=request.form['note']
    apply_info=Apply.query.filter(Apply.id == apply_id).first()
    apply_info.status = Apply.STATUS_REJECT
    apply_info.note=note
    db.session.commit()
    userinfo = User.query.filter(User.id == apply_info.uid).first()
    subject = "[主机申请]申请主机被驳回"
    config = eval(apply_info.template)
    configure = "%d核/%dG/%dG" %(config['cpu'],config['mem'],config['disk'])
    content =  '您申请的主机(配置:%s)被<fonts style="color: red;">驳回</fonts> 原因:%s' %(configure,apply_info.note)
    add_mail(userinfo.email, subject, content)
    if request.referrer:
        return redirect(request.referrer)
    else:
        return redirect(url_for('user.happroval'))

@user.route('/reject_bastion_apply/',methods=['post','get'])
@login_required
def reject_bastion_apply():
    note = request.form['note']
    id=request.form['id']
    item = HostBastionApply.query.filter(HostBastionApply.id == id).first()
    item.status = HostBastionApply.STATUS_REJECT
    item.note=note
    db.session.commit()
    userinfo = User.query.filter(User.id == item.uid).first()
    host = Host.query.filter(Host.id == item.host_id).first()
    subject = "[权限申请]申请权限被驳回"
    content =  '您申请的主机(%s)权限被<fonts style="color: red;">驳回</fonts> 原因:%s' %(host.hostname,item.note)
    add_mail(userinfo.email, subject, content)
    if request.referrer:
        return redirect(request.referrer)
    else:
        return redirect(url_for('user.papproval'))

@user.route('/add_applyhosttasks/<int:id>',methods=['post','get'])
@login_required
def add_applyhosttasks(id):
    code = 0
    msg = "任务添加成功"
    flag = request.form['flag']
    info = Apply.query.filter(Apply.id == id).first()
    config = eval(info.template)
    configure = "%d核/%dG/%dG" %(config['cpu'],config['mem'],config['disk'])
    approver_uid = app.config.get("APPROVER")['host']
    if info.approver_uid == current_user.id:
        if flag == '1':
            if current_user.id == approver_uid:
                info.status = Apply.STATUS_RUNNING
                db.session.commit()
                target_add = ApplyHostTasks(info.uid,info.id,info.pool_id,info.type,info.idc,info.num,info.template,0)
                db.session.add(target_add)
                db.session.commit()
            else:
                info.approver_uid=approver_uid
                db.session.commit()
        else:
            info.status = Apply.STATUS_REJECT
            db.session.commit()
            userinfo = User.query.filter(User.id == info.uid).first()
            subject = "[主机申请]申请主机被驳回"
            content =  '您申请的主机(配置:%s)被<fonts style="color: red;">驳回</fonts>' %configure
            add_mail(userinfo.email, subject, content)
    else:
        code = 1
        msg = "没有权限操作"
    return responsejson(code, msg)


@user.route("/permission/userrole",methods=['post','get'])
@login_required
def permission():
    roles = Role.query.all()
    role_user = []
    index = []
    for role in roles:
        info = {'roleid':role.id,'name':role.name,'users':[]}
        index.append(role.id)
        role_user.append(info)
    for i in range(0,len(index)):
        # qiqi 修复不显示权限用户的bug
        userroles = db.session.query(UserRole.user_id,User).filter\
            (and_(UserRole.role_id == index[i],UserRole.user_id == User.id,User.status == 0)).all()
        if userroles:
            for item in userroles:
                username = User.query.filter(User.id == item.user_id).first()
                if username:
                    info = {'id':username.id,'name':username.cn_name}
                    role_user[i]['users'].append(info)
    return render_template('permission/userrole.html',role_users=role_user)

@user.route("/permission/userrole/autocomplete", methods=['POST', 'GET'])
def username():
    name = request.form['name'].strip() + '%'
    roleid = int(request.form['roleid'].strip(),0)
    roleids = []
    result = []
    if re.match(r'([A-Za-z])+',name):
        users = User.query.filter(and_(User.name.like(name),User.status == 0)).all()
        for user in users:
            user_roles = UserRole.query.filter(UserRole.user_id == user.id).all()
            if user_roles:
                for user_role in user_roles:
                    roleids.append(user_role.role_id)
                if roleid not in roleids:
                    result.append([user.id,user.name])
            else:
                result.append([user.id,user.name])
    else:
        users = User.query.filter(and_(User.cn_name.like(name),User.status == 0)).all()
        for user in users:
            user_roles = UserRole.query.filter(UserRole.user_id == user.id).all()
            if user_roles:
                for user_role in user_roles:
                    roleids.append(user_role.role_id)
                if roleid not in roleids:
                    result.append([user.id,user.cn_name])
            else:
                result.append([user.id,user.cn_name])
    return app.response_class(json.dumps(result), mimetype='application/json')

@user.route('/permission/userrole/add',methods=['POST','GET'])
@login_required
def add():
    if request.method == 'POST':
        userid = int(request.form['userid'].strip())
        roleid = int(request.form['roleid'].strip())
        if userid and roleid:
            userrole = UserRole(user_id=userid,role_id=roleid)
            db.session.add(userrole)
            db.session.commit()

    return responsejson('0',"成功")

@user.route('/permission/userrole/delete',methods=['POST','GET'])
@login_required
def delete():
    if request.method == 'POST':
        userid = int(request.form['userid'].strip())
        roleid = int(request.form['roleid'].strip())
        if userid and roleid:
            userrole = UserRole.query.filter(and_(UserRole.user_id == userid,UserRole.role_id == roleid)).first()
            if userrole:
                db.session.delete(userrole)
                db.session.commit()
    return responsejson('0',"成功")

@user.route('/permission/role',methods=['post','get'])
@login_required
def role():
    roles = Role.query.all()
    return render_template('permission/role.html',roles=roles)

@user.route('/permission/role/add',methods=['POST','GET'])
@login_required
def roleadd():
    if request.method == 'POST':
        rolename = request.form['role'].strip()
        info = Role.query.filter(Role.name == rolename).first()
        if info:
            return responsejson(1,"角色已存在")
        updated  = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        role = Role(name=rolename,updated=updated)
        db.session.add(role)
        db.session.commit()
        return  responsejson('0',"添加成功")
    return  responsejson('1',"操作不允许")

@user.route('/permission/role/delete/<int:id>',methods=['POST','GET'])
@login_required
def roledelte(id):
    if id == 1 or id == 2:
        flash('初始化角色，不允许删除',0)
        return  responsejson('1',"")
    role = Role.query.filter(Role.id == id).first()
    code = 0
    if role:
        code = 1
        db.session.delete(role)
        db.session.commit()
    userroles =UserRole.query.filter(UserRole.role_id == id).all()
    if userroles:
        for userrole in userroles:
            db.session.delete(userrole)
            db.session.commit()
    if code:
        flash('删除成功',code)
    else:
        flash('删除失败',code)
    return  responsejson('1',"")

@user.route('/permission/role/<int:id>',methods=['POST','GET'])
@login_required
def roledetail(id):
    info = Role.query.filter(Role.id == id).first()
    role = {}
    if info:
        role['name'] = info.name
        role['flag'] = info.id
    return app.response_class(json.dumps(role), mimetype = 'application/json')

@user.route('/permission/role/update',methods=['POST','GET'])
@login_required
def roleupdate():
    roleid = int(request.form['roleid'].strip())
    name   = request.form['role'].strip()
    info = Role.query.filter(Role.name == name).first()
    if info:
        return responsejson(1,"角色已存在")
    else:
        role = Role.query.filter(Role.id == roleid).first()
        role.name = name
        db.session.commit();
        return responsejson(0,"修改成功")

    return app.response_class(json.dumps(role), mimetype = 'application/json')

@user.route('/permission/url',methods=['post','get'])
@login_required
def urllist():
    lists = Action.query.all()
    urllist = []
    flag = 1
    if lists:
        for item in lists:
            info = {'id':item.id,'url':item.url,'tag':item.tag,'content':item.content,'method':item.method,'flag':flag }
            flag +=1
            urllist.append(info)
        return render_template('permission/addurl.html',lists=urllist)

@user.route('/permission/url/add',methods=['POST','GET'])
@login_required
def urladd():
    if request.method == 'POST':
        url = request.form['url'].strip()
        key = int(request.form['method'].strip(),0)
        method = ['','post','get','delete']
        tag = request.form['tag'].strip()
        content = request.form['content'].strip()
        info = Action.query.filter(and_(Action.url == url,Action.method == method[key])).first()
        if info:
            return responsejson(1,"URL已存在")
        action = Action(url=url,content=content,method=method[key],tag=tag)
        db.session.add(action)
        db.session.commit()
        return  responsejson('0',"添加成功")
    return  responsejson('1',"操作不允许")

@user.route('/permission/url/<int:id>',methods=['POST','GET'])
@login_required
def urldetail(id):
    info = Action.query.filter(Action.id == id).first()
    action = {}
    method = ['','post','get','delete']
    if info:
        action['url'] = info.url
        action['tag'] = info.tag
        action['method'] = method.index(info.method)
        action['content'] = info.content
        action['type'] = info.id
    return app.response_class(json.dumps(action), mimetype = 'application/json')

@user.route('/permission/url/delete/<int:id>',methods=['POST','GET'])
@login_required
def urldelte(id):
    action = Action.query.filter(Action.id == id).first()
    code = 0
    if role:
        code = 1
        db.session.delete(action)
        db.session.commit()
    roleactions =RoleAction.query.filter(RoleAction.action_id == id).all()
    if roleactions:
        for roleaction in roleactions:
            db.session.delete(roleaction)
            db.session.commit()
    if code:
        flash('删除成功',code)
    else:
        flash('删除失败',code)
 
    return  responsejson('1',"")

@user.route('/permission/url/modify',methods=['POST','GET'])
@login_required
def urlupdate():
    if request.method == 'POST':
        id  = int(request.form['id'].strip(),0)
        url = request.form['url'].strip()
        key = int(request.form['method'].strip(),0)
        tag = request.form['tag'].strip()
        content = request.form['content'].strip()
        method = ['','post','get','delete']
        info = Action.query.filter(and_(Action.url == url,Action.tag == tag,Action.content == content,Action.method == method[key])).first()
        if info:
           return  responsejson('0',"内容无修改")
        action = Action.query.filter(Action.id == id).first()
        if action:
            action.url = url
            action.tag = tag
            action.method = method[key]
            action.content = content
            db.session.commit()
        return  responsejson('0',"修改成功")
    return responsejson(1,'操作不允许')

@user.route('/permission/role-action',methods=['post','get'])
@login_required
def roleaction():
    actions = Action.query.all()
    roleid  = int(request.args.get('roleid').strip(),0)
    role = Role.query.filter(Role.id == roleid).first()
    tab  = []
    tag = []
    adminid = getadminid()
    for item in actions:
        if item.tag not in tag:
            info = {'tag':item.tag,'data':[],'roleid':roleid,'adminid':adminid}
            tab.append(info)
            tag.append(item.tag)
    for i in range(len(tag)):
        for item in actions:
            if tag[i] == item.tag:
                role_actions = RoleAction.query.filter(RoleAction.action_id == item.id).all()
                roleids = []
                if role_actions:
                    for role_action in role_actions:
                        roleids.append(role_action.role_id)
                info = {'content':item.content,'actionid':item.id,"roleids":roleids}
                tab[i]['data'].append(info)
    for item in tab:
        item['data']=list_3array(item['data'])

    return render_template('permission/role-action.html',tab=tab,role=role)

@user.route('/permission/role-action/update',methods=['POST','GET'])
@login_required
def roleactionupdate():
    if request.method == 'POST':
        adminid = getadminid()
        roleid =  int(request.form['roleid'].strip(),0)
        if roleid != adminid:
            actionids = request.form.getlist('actionid')
            roleaction = RoleAction.query.filter(RoleAction.role_id == roleid).all()
            role_actionids = []
            if roleaction:
                for item in roleaction:
                    role_actionids.append(item.action_id)
            intactionids = []
            if actionids:
                for item in actionids:
                    intactionids.append(int(item.strip()))
            add = list(set(intactionids) - set(role_actionids))
            remove = list(set(role_actionids) - set(intactionids))
            if add:
                for actionid in add:
                    roleaction = RoleAction(role_id=roleid,action_id=actionid)
                    db.session.add(roleaction)
                    db.session.commit()
            if remove:
                for actionid in remove:
                    roleaction = RoleAction.query.filter(and_(RoleAction.role_id == roleid,RoleAction.action_id == actionid )).first()
                    if roleaction:
                        db.session.delete(roleaction)
                        db.session.commit()
        return redirect(url_for('user.role'))

@user.route("/tickets")
@login_required
def tickets():
    from models.sa.tickets import Tickets
    from models.sa.tickets_task import Tickets_Task
    from models.sa.tickets_category import Tickets_Category
    p = request.args.get('p',1)
    per_page = 50
    range_num = 10
    uid = current_user.id
    cat_dic = {}
    uids = []
    tickets_id = []
    tickets_tasks_dic = {}
    idx = 1
    cat_list = Tickets_Category.query.all()
    if cat_list:
        for cat_item in cat_list:
            cat_dic[cat_item.id] = cat_item
    target = Tickets.query.filter(Tickets.uid == uid)
    total_num = target.count()
    page = Paginator(total_num, per_page=per_page, current=p, range_num=range_num)
    tickets_info = target.order_by(Tickets.id.desc()).offset((int(p) - 1) * per_page).limit(per_page).all()
    for tickets_item in tickets_info:
        tickets_id.append(tickets_item.id)

    tickets_tasks_info = Tickets_Task.query.filter(Tickets_Task.tickets_id.in_(tickets_id)).all()

    for tickets_tasks_item in tickets_tasks_info:
        tmp_tickets_id = tickets_tasks_item.tickets_id
        if tmp_tickets_id not in tickets_tasks_dic:
            tickets_tasks_dic[tmp_tickets_id] = []

        tickets_tasks_dic[tmp_tickets_id].append({
            'tickets_cat_id':tickets_tasks_item.tickets_cat_id,
            'manage_uid':tickets_tasks_item.manage_uid,
            'content':tickets_tasks_item.content
        })
        uids.append(tickets_tasks_item.manage_uid)

    user_mapping = get_user_info(uids = uids)
    for tickets_item in tickets_info:
        tickets_item.idx = idx
        tickets_item.cat_name = ''
        tickets_item.content = ''
        tickets_item.manage_name = ''
        idx += 1
        if tickets_item.id in tickets_tasks_dic:
            for tmp_tickets_tasks_item in tickets_tasks_dic[tickets_item.id]:
                tmp_cat_dic = cat_dic[tmp_tickets_tasks_item['tickets_cat_id']]
                tmp_user_info = user_mapping[tmp_tickets_tasks_item['manage_uid']]
                tmp_cat_name = tmp_cat_dic.name if  tmp_cat_dic.name == tmp_cat_dic.label else '%s-%s'%(tmp_cat_dic.label,tmp_cat_dic.name)
                tickets_item.cat_name += tmp_cat_name + ","
                tickets_item.manage_name += tmp_user_info.cn_name + ","
                tickets_item.content += '<br/>分类:'+ tmp_cat_name  + '&nbsp;&nbsp;简述:' +tmp_tickets_tasks_item['content'] + "<br/>"
            tickets_item.cat_name = tickets_item.cat_name[:-1]
            tickets_item.manage_name = tickets_item.manage_name[:-1]

    extend = {
        'total':total_num,
        'cur_total':len(tickets_info)
    }
    return render_template("ucenter/tickets.html",tickets = tickets_info ,p = page, extend = extend)

def  getadminid():
    role = Role.query.filter(Role.name == "超级管理员").first()
    return role.id

def list_3array(arr):
    lenth = len(arr)
    lines = int( (lenth+2)/3 )
    tmp = []
    array3 = []
    for i in range(lines):
        for j in range(i*3,(i+1)*3):
            if j <= lenth-1:
                tmp.append(arr[j])
        array3.append(tmp)
        tmp=[]
    return array3

# def responsejson(code,msg):
#     return app.response_class(json.dumps({'code':code,'msg':msg}), mimetype='application/json')

def jsonRender(code=0,msg='操作已更新',data=[]):
    return json.dumps({'code': code, 'msg': msg,'data':data})

def unalarm(uid,target_type,target_id):
    Alarm.query.filter(and_(Alarm.uid == uid, Alarm.type == target_type, Alarm.target_id == target_id)).delete()
    db.session.commit()

def unfollow(uid,type,id):
    Follow.query.filter(and_(Follow.uid == uid, Follow.type == type, Follow.target_id == id)).delete()
    db.session.commit()

def get_user_id(username=""):
    info = User.query.filter(User.name == username).first()
    if info:
        return  info.id
    else:
        return 0

def find_username(uids):
    userlist = {}
    if uids:
        userinfo = User.query.filter(User.id.in_(uids)).all()
        if userinfo:
            for item in userinfo:
                userlist[item.id] = item.cn_name
    return userlist

def get_user_info(**kwargs):
    if 'id' in kwargs:
        return User.query.filter(User.id == kwargs['id']).first()
    elif 'uids' in kwargs:
        userlist = {}
        userinfo = User.query.filter(User.id.in_(kwargs['uids'])).all()
        if userinfo:
            for item in userinfo:
                userlist[item.id] = item
        return userlist
    return None