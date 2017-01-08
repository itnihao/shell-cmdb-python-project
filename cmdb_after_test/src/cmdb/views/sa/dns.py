# -*- coding: utf-8 -*-
from flask import Blueprint, render_template, request, redirect, url_for,Flask,make_response
from flask_login import login_required, current_user
from application import app, db
from models.dns.dns_zone import DnsZone
from models.dns.dns_history import DnsHistory
from models.dns.dns_apply import DnsApply
from models.dns.dns_apply import get_type
from models.dns.dns_tasks import DnsTasks
from models.dns.cdn import Cdn
from models.dns.cdn_details import CdnDetails
from models.user import User
from pypages import Paginator
from views.functions import responsejson,addmail
from views.user import userinfomapping
from sqlalchemy import and_
import json,re,datetime,time
from apis.paramikolib import ParamikoLib
from configure.cdn import Cdn_List
from config import DOMAIN
from threading import Thread

dns = Blueprint('dns', __name__)

@dns.route("/")
@login_required
def index():
    zone_id = request.args.get('zone',0)
    p = request.args.get('p',1)
    q = request.args.get("q",'')
    per_page = 50
    range_num = 10
    zone = {}
    zoneinfo = DnsZone.query.all()
    for item in zoneinfo:
        zone[item.id] = item.zone
    url = ''
    applyinfo = DnsApply.query.filter(DnsApply.deleted == DnsApply.DELETED_NO)
    if int(zone_id) != 0:
        applyinfo = applyinfo.filter(DnsApply.zone_id == zone_id)
        url = '%s&zone=%d'%(url,int(zone_id))
    if q:
        url = '%s&q=%s' %(url,q.strip())
        kw = '%'+q+'%'
        applyinfo = applyinfo.filter(DnsApply.prefix.like(kw))
    total_num = applyinfo.count()
    page = Paginator(total_num, per_page=per_page, current=p, range_num=range_num)
    apply = applyinfo.order_by(DnsApply.id.desc()).offset((int(p) - 1) * per_page).limit(per_page).all()
    extendinfo = {
        'total':total_num,
        'cur_total':len(apply)
    }
    if apply:
        for item in apply:
            try:
                item.domain = item.prefix+'.'+zone[item.zone_id]
            except:
                print item.id
    zone_info = DnsZone.query.all()
    return render_template('/sa/dns/list.html',zone_id=zone_id,url=url,data=apply,p=page,extendinfo=extendinfo,zone_info=zone_info)

@dns.route("/delete/<int:id>",methods = ['GET', 'POST'])
@login_required
def delete(id):
    intreg = re.compile('^[1-9]\d*$')
    if not intreg.match(str(id)):
        print "删除域名失败!"
        return responsejson(1,"删除域名失败!")
    apply_info = DnsApply.query.filter(DnsApply.id == id).first()
    apply_info.status = DnsApply.STATUS_RUNNING
    db.session.commit()
    thr = Thread(target=del_dns,args=[id,current_user.cn_name])
    thr.start()
    return responsejson(0,"")

@dns.route("/task/my/",methods = ['GET', 'POST'])
@login_required
def task_my():
    p = request.args.get('p',1)
    per_page = 50
    range_num = 10
    zone = {}
    zoneinfo = DnsZone.query.all()
    for item in zoneinfo:
        zone[item.id] = item.zone
    uids = []
    apply_info = DnsApply.query.filter(DnsApply.approve_uid == current_user.id,DnsApply.deleted == DnsApply.DELETED_NO)
    total_num = apply_info.count()
    page = Paginator(total_num, per_page=per_page, current=p, range_num=range_num)
    apply = apply_info.order_by(DnsApply.id.desc()).offset((int(p) - 1) * per_page).limit(per_page).all()
    extendinfo = {
        'total':total_num,
        'cur_total':len(apply)
    }
    for item in apply:
        uids.append(item.uid)
    userlist = userinfomapping(uids)
    idx = 1
    for item in apply:
        item.domain = item.prefix + '.' + zone[item.zone_id]
        item.cn_name = userlist['uid_%s'%item.uid]
        item.idx = idx
        item.content_part = item.content[:15]
        item.content_len = len(item.content)
        idx += 1
    return render_template("/sa/dns/task.html",p=page,data=apply,extendinfo=extendinfo)

@dns.route("/task/add/<int:id>",methods = ['GET', 'POST'])
@login_required
def add_task(id):
    flag = request.form['flag']
    item = DnsApply.query.filter(and_(DnsApply.deleted == 0,DnsApply.id == id)).first()
    item.status = DnsApply.STATUS_RUNNING
    db.session.commit()
    thr = Thread(target=add_dns,args=[id,flag,current_user.cn_name])
    thr.start()
    return responsejson(0,"")

def add_dns(id,flag,cn_name):
    with app.app_context():
        item = DnsApply.query.filter(and_(DnsApply.deleted == 0,DnsApply.id == id)).first()
        if item:
            zone_info = DnsZone.query.filter(DnsZone.id == item.zone_id).first()
            user_info = User.query.filter(User.id == item.uid).first()
            if flag == '1':
                dns_info = get_dns_info(zone_info.type)
                par = ParamikoLib(dns_info['host'])
                new_value = item.value
                if item.type == DnsApply.TYPE_CNAME:
                    new_value = item.value+ '.'
                dns_record = '%s\t%s\t%s'%(item.prefix,item.type_descri,new_value)

                if zone_info.type == DnsZone.TYPE_IDC_OUT:
                    dns_file = dns_info['file_dir'] + '/default/' + zone_info.zone + '.default'
                else:
                    dns_file = dns_info['file_dir'] + '/' + zone_info.zone

                #检测是否存在
                par.execute("sed -n '/^\s*%s\s*%s\s*%s\s*$/p' %s"%(item.prefix,item.type_descri,new_value,dns_file))
                stdout = par.get_stdout()
                if stdout == "":
                    #备份文件
                    par.execute('\cp -f %s %s.bak'%(dns_file,dns_file))
                    #添加记录
                    par.execute('tail -1 %s'%dns_file)
                    stdout = par.get_stdout()
                    #为避免追加文本到同一行，所以添加一个空行
                    if stdout != '':
                        par.execute("echo '' >> %s"%(dns_file))
                    par.execute('echo %s >> %s'%(dns_record,dns_file))
                    #检测是否修改成功
                    par.execute("sed -n '/^\s*%s\s*%s\s*%s\s*$/p' %s"%(item.prefix,item.type_descri,new_value,dns_file))
                    stdout = par.get_stdout()
                    if stdout != "":
                        #删除空行
                        par.execute("sed -i '/^\s*$/d' %s"%(dns_file))
                        timestamp = str(int(time.time()))
                        #替换时间
                        par.execute("sed -i 's/[0-9]\{10\}\( *; *[S,s]erial\)/%s\\1/g' %s"%(timestamp,dns_file))
                        par.execute("/usr/sbin/named-checkzone %s %s"%(zone_info.zone,dns_file))
                        stdout = par.get_stdout()
                        if stdout[-2:] == "OK":
                            par.execute('/usr/sbin/rndc reload')
                            stdout = par.get_stdout()
                            if stdout == 'server reload successful':
                                item.status = DnsApply.STATUS_SUCCESS
                                db.session.commit()
                                print "DNS添加成功！"
                                content = '用户：%s通过%s的域名申请，域名:%s.%s'%(cn_name,user_info.cn_name,item.prefix,zone_info.zone)
                                add_dns_history(id,DnsHistory.STATUS_DELETE,content)
                                return
                    #还原文件
                    par.execute('\cp -f %s.bak %s'%(dns_file,dns_file))
                    print "DNS配置错误！"
                else:
                    print "DNS记录已存在！"
                item.status = DnsApply.STATUS_FAIL
            else:
                item.status = DnsApply.STATUS_REJECT
                item.deleted = 1
                print "DNS申请被拒绝！"
                content = '用户：%s驳回%s的域名申请，域名:%s.%s'%(cn_name,user_info.cn_name,item.prefix,zone_info.zone)
                add_dns_history(id,DnsHistory.STATUS_REJECT,content)
        else:
            print "未找到DNS前缀！"
            item.status = DnsApply.STATUS_FAIL
        db.session.commit()

def del_dns(id,cn_name):
    with app.app_context():
        apply_info = DnsApply.query.filter(DnsApply.id == id).first()
        zone_info = DnsZone.query.filter(DnsZone.id == apply_info.zone_id).first()
        dns_info = get_dns_info(zone_info.type)
        par = ParamikoLib(dns_info['host'])

        if zone_info.type == DnsZone.TYPE_IDC_OUT:
            dns_file = dns_info['file_dir'] + '/default/' + zone_info.zone + '.default'
        else:
            dns_file = dns_info['file_dir'] + '/' + zone_info.zone

        #备份文件
        par.execute('\cp -f %s %s.bak'%(dns_file,dns_file))
        #删除记录
        par.execute("sed -i '/^\s*%s\s*/d' %s"%(apply_info.prefix,dns_file))
        #检测是否修改成功
        par.execute("sed -n '/^\s*%s\s*/p' %s"%(apply_info.prefix,dns_file))
        stdout = par.get_stdout()
        if stdout == "":
            #删除空行
            par.execute("sed -i '/^\s*$/d' %s"%(dns_file))
            #替换时间
            timestamp = str(int(time.time()))
            par.execute("sed -i 's/[0-9]\{10\}\( *; *[S,s]erial\)/%s\\1/g' %s"%(timestamp,dns_file))
            par.execute("/usr/sbin/named-checkzone %s %s"%(zone_info.zone,dns_file))
            stdout = par.get_stdout()
            if stdout[-2:] == "OK":
                par.execute('/usr/sbin/rndc reload')
                stdout = par.get_stdout()
                if stdout == 'server reload successful':
                    apply_info.deleted = DnsApply.DELETED_YES
                    apply_info.status = DnsApply.STATUS_SUCCESS
                    db.session.commit()
                    content = '用户：%s删除域名:%s.%s'%(cn_name,apply_info.prefix,zone_info.zone)
                    add_dns_history(id,DnsHistory.STATUS_DELETE,content)
                    return
        #还原文件
        par.execute('\cp -f %s.bak %s'%(dns_file,dns_file))
        print "删除域名失败!"
        apply_info.status = DnsApply.STATUS_SUCCESS
        db.session.commit()

def modify_dns(id,new_type,new_value,ip_updated,cn_name):
    with app.app_context():
        apply_info = DnsApply.query.filter(and_(DnsApply.id == id,DnsApply.deleted == 0)).first()
        zone_info = DnsZone.query.filter(DnsZone.id == apply_info.zone_id).first()
        dns_info = get_dns_info(zone_info.type)
        par = ParamikoLib(dns_info['host'])
        old_value = apply_info.value
        if zone_info.type == DnsZone.TYPE_IDC_OUT:
            dns_file = dns_info['file_dir'] + '/default/' + zone_info.zone + '.default'
        else:
            dns_file = dns_info['file_dir'] + '/' + zone_info.zone
        type_name = get_type(new_type)
        if type_name != "A":
            new_fqdn_value = new_value + '.'
        else:
            new_fqdn_value = new_value

        if apply_info.type_descri != "A":
            old_value = old_value + '.'

        #备份文件
        par.execute('\cp -f %s %s.bak'%(dns_file,dns_file))
        #修改记录
        par.execute("sed -i 's/\(^\s*%s\s*\)%s\s*%s\s*$/\\1%s\t%s/g' %s"%(apply_info.prefix,apply_info.type_descri,old_value,type_name,new_fqdn_value,dns_file))
        #检测是否修改成功
        par.execute("sed -n '/^\s*%s\s*%s\s*%s\s*$/p' %s"%(apply_info.prefix,type_name,new_fqdn_value,dns_file))
        stdout = par.get_stdout()
        if stdout != "":
            #删除空行
            par.execute("sed -i '/^\s*$/d' %s"%(dns_file))
            #替换时间
            timestamp = str(int(time.time()))
            par.execute("sed -i 's/[0-9]\{10\}\(\s*;\s*[S,s]erial\)/%s\\1/g' %s"%(timestamp,dns_file))
            par.execute("/usr/sbin/named-checkzone %s %s"%(zone_info.zone,dns_file))
            stdout = par.get_stdout()
            if stdout[-2:] == "OK":
                par.execute('/usr/sbin/rndc reload')
                stdout = par.get_stdout()
                if stdout == 'server reload successful':
                    changeMsg = ''
                    if apply_info.value != new_value:
                        changeMsg = '用户：%s,将value 从 %s 更改为 %s'%(cn_name,apply_info.value,new_value)
                        apply_info.value = new_value
                    if apply_info.type != new_type:
                        if len(changeMsg) > 1:
                            changeMsg = '%s,将type 从 %s 更改为 %s'%(changeMsg,apply_info.type,type_name)
                        else:
                            changeMsg = '用户：%s,将type 从 %s 更改为 %s'%(cn_name,apply_info.type,type_name)
                        apply_info.type = new_type
                    apply_info.ip_updated = ip_updated
                    apply_info.status = DnsApply.STATUS_SUCCESS
                    db.session.commit()
                    if len(changeMsg) > 1:
                        add_dns_history(id,DnsHistory.STATUS_PASS,content = changeMsg)
                    return
        #还原文件
        par.execute('\cp -f %s.bak %s'%(dns_file,dns_file))
        print "DNS修改失败！"
        apply_info.status = DnsApply.STATUS_SUCCESS
        db.session.commit()


def get_dns_info(type):
    template_name = "office"
    if type == 1:
        template_name = 'outer'
    elif type == 2:
        template_name = 'inner'
    return app.config.get('DNS')[template_name]


@dns.route("/apply", methods=['POST', 'GET'])
@login_required
def apply():
    if request.method == "GET":
        zone_id = request.args.get('zone','0')
        pre_domain = request.args.get('pre_domain','')
        ip_domain = request.args.get('ip_domain','')
        content = request.args.get('content','')
        params = {'zone_id':zone_id,
                 'pre_domain':pre_domain,
                 'ip_domain':ip_domain,
                 'content':content}
        approval = ""
        approve_uid = []
        zone_type = {}
        zone_info = DnsZone.query.filter(DnsZone.display == DnsZone.DISPLAY_YES).order_by(DnsZone.type.desc()).all()
        zone_list = []
        for item in zone_info:
            zone_data = {}
            zone_data['id'] = item.id
            zone_data['type'] = item.type
            zone_data['zone'] = item.zone
            zone_list.append(zone_data)
            if not zone_type.has_key(item.type_descri):
                zone_type[item.type_descri] = item.type
            if item.id == int(zone_id):
                approve_uid.append(item.uid)
                approval = userinfomapping(approve_uid)['uid_%s'%item.uid]
        return render_template("dns/apply.html",params=params,zone_info=zone_list,approval=approval,zone_type=zone_type,flag="dns_apply")
    else:
        code = 0
        msg = ""
        pre_domain = request.form['pre_domain']
        zone_id = int(request.form['zone'])
        type = request.form['type']
        uid = current_user.id
        ip_domain = request.form['ip_domain']
        content = request.form['content']
        ip_updated = request.form['ip_updated']
        approve_uid = 0
        zone_info = DnsZone.query.filter(DnsZone.id == zone_id).first()
        if zone_info:
            approve_uid = zone_info.uid
        apply_info = DnsApply.query.filter(and_(DnsApply.prefix == pre_domain,DnsApply.zone_id == zone_id,DnsApply.deleted == DnsApply.DELETED_NO)).all()
        if not apply_info:
            apply_target = DnsApply(prefix=pre_domain,zone_id=zone_id, type=type, value=ip_domain, uid=uid, approve_uid=approve_uid, content=content, priority=0, status=DnsApply.STATUS_APPROVING,deleted=DnsApply.DELETED_NO,ip_updated=ip_updated)
            db.session.add(apply_target)
            db.session.commit()
            user_info = User.query.filter(User.id == uid).first()
            approval = User.query.filter(User.id == approve_uid).first()
            subject = "【域名申请】 " + user_info.cn_name + ' 申请域名，待审批'
            content = user_info.cn_name + '申请域名：' + pre_domain + '.' + zone_info.zone + '<br/><a href=' + DOMAIN + url_for('dns.task_my') + '>点击此处</a>进行审批'
            addmail(approval.email, subject, content)
        else:
            code = 1
            msg = "此域名已经存在,请申请其他域名"
        return responsejson(code, msg)

@dns.route("/switch_cdn",methods=['GET','POST'])
@login_required
def switch_cdn():
    zone_id = request.args.get('zone','0')
    pre_domain = request.args.get('pre_domain','')
    ip_domain = request.args.get('ip_domain','')
    content = request.args.get('content','')
    params = {'zone_id':zone_id,
             'pre_domain':pre_domain,
             'ip_domain':ip_domain,
             'content':content}
    zone_info = DnsZone.query.filter(DnsZone.type == DnsZone.TYPE_CDN).order_by(DnsZone.type.desc()).all()
    zone_list = []
    for item in zone_info:
        zone_data = {}
        zone_data['id'] = item.id
        zone_data['zone'] = item.zone
        dns_applys = DnsApply.query.filter(DnsApply.zone_id == item.id).all()
        cdn_infos = []
        for cdn in dns_applys:
            cdn_infos.append(cdn.prefix)
        zone_data['prefix'] = cdn_infos
        zone_list.append(zone_data)
    return render_template("dns/apply.html",params=params,zone_info=zone_list,flag="switch_cdn")

@dns.route("/<int:id>",methods=['GET', 'POST'])
@login_required
def detail(id):
    jsonval = {}
    apply_info = DnsApply.query.filter(DnsApply.id == id).first()
    zone_info = DnsZone.query.filter(DnsZone.id == apply_info.zone_id).first()
    remote_addr = request.remote_addr
    if apply_info:
        jsonval = {
            'prefix': apply_info.prefix,
            'value': apply_info.value,
            'zone': zone_info.zone,
            'type': apply_info.type,
            'content': apply_info.content,
            'remote_addr':remote_addr,
            'ip_updated': apply_info.ip_updated,
        }
    return app.response_class(json.dumps(jsonval), mimetype='application/json')

@dns.route("/modify/<int:id>", methods=['POST', 'GET'])
@login_required
def modify(id):
    dns_value = request.form['dns_value']
    type = int(request.form['type'])
    ip_updated = int(request.form['ip_updated'])
    item = DnsApply.query.filter(and_(DnsApply.deleted == 0,DnsApply.id == id)).first()
    if item.status != 4:
        item.value = dns_value
        item.type = type
        item.ip_updated = ip_updated
        db.session.commit()
        return responsejson(0,"修改成功！")
    if item.status == 3:
        return responsejson(1,"域名已经在添加中，请稍后再试！")
    item.status = DnsApply.STATUS_RUNNING
    db.session.commit()
    thr = Thread(target=modify_dns,args=[id,type,dns_value,ip_updated,current_user.cn_name])
    thr.start()
    return responsejson(0,"")

def add_dns_task(id,type,status):
    task_target = DnsTasks(dns_apply_id=id,type=type,status=status)
    db.session.add(task_target)
    db.session.commit()

def add_dns_history(id,status,content = ''):
    history_target = DnsHistory(id,status,content = content)
    db.session.add(history_target)
    db.session.commit()

def find_self_domain(ip,prefix):
    zone_name = app.config.get('SELF_DOMAIN')
    zone_info = DnsZone.query.filter(DnsZone.zone == zone_name).first()
    if zone_info:
        approve_uid = zone_info.uid
        zone_id = zone_info.id
        if '_' in prefix:
            prefix = prefix.replace('_','-')
        info = DnsApply.query.filter(and_(DnsApply.zone_id == zone_id,DnsApply.prefix == prefix)).first()
        if not info:
            apply_target = DnsApply(prefix=prefix, zone_id=zone_id, type=DnsApply.TYPE_A, value=ip, uid=current_user.id, approve_uid=approve_uid, content="自用域名", priority=0, status=DnsApply.STATUS_SUCCESS,deleted=DnsApply.DELETED_NO,ip_updated=0)
            db.session.add(apply_target)
            db.session.commit()
            add_dns_task(apply_target.id,zone_info.type,DnsTasks.STATUS_FREE)
        else:
            today = str(datetime.date.today())+" 00:00:00"
            today = datetime.datetime.strptime(today,'%Y-%m-%d %H:%M:%S')
            if info.updated < today:
                if info.value != ip:
                    add_dns_task(info.id,zone_info.type,DnsTasks.STATUS_FREE)
                if info.ip_updated == 0:
                    info.value = ip
                    info.updated = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    db.session.commit()

@dns.route("/zone_cdn",methods = ["GET","POST"])
@login_required
def zone_cdn():
    host = app.config.get('DNS')['outer']['host']
    if request.method == "GET":
        area = request.args.get('area','')
        dn = request.args.get('dn','')
        prefix = request.args.get('prefix','')
        file_path = get_cdn_file_path(area,dn)
        par = ParamikoLib(host)
        now_cdn = get_now_cdn(par,file_path,prefix)
        now_pro = get_pro(now_cdn,prefix,dn)
        return app.response_class(json.dumps({'pro':now_pro}), mimetype='application/json')
    else:
        isOk = False
        area = request.form['area']
        dn = request.form['dn']
        prefix = request.form['prefix']
        now_pro = request.form['now_pro']
        new_pro = request.form['new_pro']
        new_pro2 = get_pro(change_cdn(prefix,dn,area,now_pro),prefix,dn)
        if new_pro == new_pro2:
            isOk = True
        else:
            isOk = False

        # file_path = get_cdn_file_path(area,dn)
        # now_cdn = get_now_cdn(par,file_path,prefix)
        # if new_pro != '':
        #     args = ''
        #     for cdn in Cdn_List[new_pro]:
        #         fqdn = prefix + '.' + dn + '.' + cdn + '.'
        #         if fqdn != now_cdn:
        #             args = args + ' ' + fqdn + '$\|'
        #     args = args[:-2]
        #     timestamp = str(int(time.time()))
        #     par = ParamikoLib(host)
        #     par.execute("sed -i '/^%s /s/^[^ *;]/;&/' %s"%(prefix,file_path))
        #     print "sed '/ %s/s/^ *;//' %s"%(args,file_path)
        #
        #     par.execute("sed -i '/%s/s/^ *;//' %s"%(args,file_path))
        #     par.execute("sed -i 's/[0-9]\{10\}\( *; Serial\)/%s\\1/g' %s"%(timestamp,file_path))
        #
        #     par.execute("/usr/sbin/named-checkconf %s"%app.config.get('DNS_CONF'))
        #     error1 = par.get_stdout()
        #     if error1 == '':
        #         par.execute("/usr/sbin/named-checkzone %s %s"%(dn,file_path))
        #         error2 = par.get_stdout()
        #         if error2[-2:] == "OK":
                    # par.execute('/usr/sbin/rndc reload')
        return app.response_class(json.dumps({"isOk":isOk,"pro":new_pro}), mimetype='application/json')

def change_cdn(prefix,dn,area,now_pro):
    host = app.config.get('DNS')['outer']['host']
    file_path = get_cdn_file_path(area,dn)
    # now_cdn = get_now_cdn(par,file_path,prefix)
    if now_pro == 'tencent':
        new_pro = 'dnion'
    else:
        new_pro = 'tencent'

    args = ''
    for cdn in Cdn_List[new_pro]:
        fqdn = prefix + '.' + dn + '.' + cdn + '.'
        args = args + ' ' + fqdn + '$\|'
    args = args[:-2]
    timestamp = str(int(time.time()))
    par = ParamikoLib(host)
    #全部注释
    par.execute("sed -i '/^%s /s/^[^ *;]/;&/' %s"%(prefix,file_path))
    # print "sed '/ %s/s/^ *;//' %s"%(args,file_path)
    #取消注释
    par.execute("sed -i '/%s/s/^ *;//' %s"%(args,file_path))
    #替换时间
    par.execute("sed -i 's/[0-9]\{10\}\( *; Serial\)/%s\\1/g' %s"%(timestamp,file_path))

    par.execute("/usr/sbin/named-checkconf %s"%app.config.get('DNS_CONF'))
    error1 = par.get_stdout()
    now_cdn = ""
    if error1 == '':
        par.execute("/usr/sbin/named-checkzone %s %s"%(dn,file_path))
        error2 = par.get_stdout()
        if error2[-2:] == "OK":
            par.execute('/usr/sbin/rndc reload')
            stdout = par.get_stdout()
            if stdout == 'server reload successful':
                now_cdn = get_now_cdn(par,file_path,prefix)
    return now_cdn

def get_cdn_file_path(area,dn):
    dir = app.config.get('DNS')['outer']['file_dir']
    file_path = dir + '/' + area + '/cdn/' + dn + '.' + area
    return file_path

def get_now_cdn(par,file_path,prefix):
    cdn = ''
    command = "cat %s | grep 'CNAME' | grep ^%s | grep -v ';' |awk '{print $4}'"%(file_path,prefix)
    par.execute(command)
    fqdn = par.get_stdout()
    return fqdn

def get_pro(now_cdn,prefix,dn):
    for cdns in Cdn_List:
        for c in Cdn_List[cdns]:
            test_fqdn = prefix + '.' + dn + '.' + c + '.'
            if now_cdn == test_fqdn:
                return cdns
    return ''

def get_cdn(now_cdn,prefix,dn):
    for cdns in Cdn_List:
        for c in Cdn_List[cdns]:
            test_fqdn = prefix + '.' + dn + '.' + c + '.'
            if now_cdn == test_fqdn:
                return c
    return ''


# def get_now_cdns(area):
#     zones = DnsZone.query.filter(DnsZone.type == DnsZone.TYPE_CDN).all()
#     zones_info = {}
#     for zone in zones:
#         file_path = get_cdn_file_path(area,zone.zone)
#         prefixs = DnsApply.query.filter(DnsApply.zone_id == zone.id).all()
#         par = ParamikoLib(app.config.get('DNS')['outer']['host'])
#         zone_info = {}
#         for prefix in prefixs:
#             now_cdn = get_now_cdn(par,file_path,prefix.prefix)
#             cdn_name = get_pro(now_cdn,prefix.prefix,zone.zone)
#             zone_info[prefix.prefix] = cdn_name
#         zones_info[zone.zone] = zone_info
#     return zones_info


@dns.route('/cdn_list',methods = ['GET','POST'])
@login_required
def cdn_list():
    if request.method == "GET":
        cdndetails = CdnDetails.query
        prefix = request.args.get('pre_zone','')
        if prefix != '':
            cdndetails = cdndetails.filter(CdnDetails.prefix == prefix)
        cdndetails.all()
        cdnlists = []
        for cdndetail in cdndetails:
            cdnlist = {}
            cdnlist["id"] = int(cdndetail.id)
            cdnlist["prefix"] = str(cdndetail.prefix)
            cdnlist["area"] = cdndetail.area
            cdnlist["area_descri"] = cdndetail.area_descri
            dnszone = DnsZone.query.filter(DnsZone.id==cdndetail.zone_id).first()
            cdnlist["zone"] = str(dnszone.zone)
            cdn = Cdn.query.filter(Cdn.id==cdndetail.cdn_id).first()
            cdnlist["cdn"] = str(cdn.cdn)
            cdnlist["cdn_name"] = cdn.cdn_descri_name
            cdnlist["updated"] = cdndetail.updated.strftime('%Y-%m-%d %H:%M:%S')
            cdnlists.append(cdnlist)
        return render_template("dns/apply.html",cdn_lists=cdnlists,flag="cdn_list")
    else:
        id = request.form["id"]
        cdndetail = CdnDetails.query.filter(CdnDetails.id == id).first()
        zone = DnsZone.query.filter(DnsZone.id == cdndetail.zone_id).first()
        cdn = Cdn.query.filter(Cdn.id == cdndetail.cdn_id).first()
        now_cdn = change_cdn(cdndetail.prefix,zone.zone,cdndetail.area_descri_pinyin,cdn.cdn_name)
        new_zone = get_cdn(now_cdn,cdndetail.prefix,zone.zone)
        new_cdn = Cdn.query.filter(Cdn.cdn == new_zone).first()
        cdndetail.cdn_id = new_cdn.id
        cdndetail.updated = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        db.session.commit()
        return app.response_class(json.dumps({"isOk":True}), mimetype='application/json')

@dns.route('/cdn_export/<cdnlists>', methods=['GET','POST'])
@login_required
def cdn_export(cdnlists):
    from views.publics.excel import ExportExcel
    from views.functions import formatJsonStr
    head = ('前缀','域名','CDN','厂商','地区','更新时间')
    cdnlists = formatJsonStr(cdnlists)
    print cdnlists
    cdnlists = json.loads(cdnlists)
    contents = []
    for cdnlist in cdnlists:
        # print cdnlist['prefix']
        contents.append([cdnlist['prefix'],cdnlist['zone'],cdnlist['cdn'],cdnlist['cdn_name'],cdnlist['area_descri'],cdnlist['updated']])
    excel = ExportExcel()
    value = excel.exportexcel('Sheet1',head,contents)
    return make_response(value, 200, {'Content-type': 'application/vnd.ms-excel','Content-Disposition': 'attachment;filename="cdns.xls"'})