# -*- coding: UTF-8 -*-
from sqlalchemy import and_, or_
from flask import Blueprint, render_template, url_for, redirect, request, flash, make_response
from flask_login import login_required, current_user
from application import app, db
import time, datetime, re, json
from models import Host, HostIp, HostOperationHistory, IpAddress, Device, User, Follow, DeviceIp, Rack, Datacenter, \
    Pool, PoolHost, Alarm
from models.host_load_ratio import HostLoadRatio
from models.host_load_daily import HostLoadDaily
from models.apply_host import Apply_host
from models.user_host import UserHost
from models.datacenter import Datacenter
from models.apply import Apply
from models.host_bastion_apply import HostBastionApply
from models.dns.dns_apply import DnsApply
from models.dns.dns_tasks import DnsTasks
from models.dns.dns_zone import DnsZone
from models.host_bastion_tasks import HostBastionTasks
from views.bastion import add_authority
from views.log import addlog
from views.functions import _set_used_ip, zabbix_rmhost, addmail, visible, responsejson
from config import DOMAIN
from pypages import Paginator
from tasks import host_device_changed
import xlwt, StringIO
from werkzeug.utils import secure_filename
from application import fujs
from models.user import Department


import xlrd
import os
from models import ip_address

host = Blueprint('host', __name__)
UPLOAD_FOLDER = 'static/upload'


@app.context_processor
def inject_fujs():
    return dict(fujs=fujs)

@host.route("/export_ip/<name>", methods=['POST', 'GET'])
@login_required
def export_ip(name):
    hosts = Host.query.all()
    jsonval = []
    if hosts:
        for host in hosts:
            host.ip = _get_ip(host.primary_ip_id)
            # host.type_name = _get_type_name(host.type)
            if (host.type_descri == name):
                jsonval.append(_get_ip(host.primary_ip_id))

    return app.response_class(json.dumps(jsonval), mimetype='application/json')

@host.route("/importinfo/<datas>", methods=['POST', 'GET'])
@login_required
def importinfo(datas):
    data= datas.split(',')
    return render_template('public/importinfo.html',datas=data)


@host.route("/importdb", methods=['POST', 'GET'])
@login_required
def importdb():
    try:
        f = request.files['fileToUpload']
        fname = secure_filename(f.filename)
        f.save(os.path.join(UPLOAD_FOLDER, 'host.xlsx'))
        BASE_DIR = (os.path.dirname(__file__))

        host_xlsx = os.path.join(UPLOAD_FOLDER, 'host.xlsx')
        data = xlrd.open_workbook(host_xlsx)
        table = data.sheets()[0]
        nrows = table.nrows
        message_date = []
        for i in range(nrows):
            if i == 0:
                continue
            row = table.row_values(i)
            print row
            hostname = row[0]
            is_virtual = 1
            type = 1
            note = row[5]
            ip_s = IpAddress.query.filter(IpAddress.ipv4 == row[3]).first()
            if not ip_s:
                print hostname + 'don not have ip: ' + row[3] + ";;;row:" + str(i)
                message_date.append(hostname + 'don not have ip: ' + row[3] + ";;;row:" + str(i))
                continue
            if ip_s.flag == 1:
                print hostname + ' ip: ' + row[3] + 'Occupyed' + ";;;row:" + str(i)
                message_date.append(hostname + ' ip: ' + row[3] + 'Occupyed' + ";;;row:" + str(i))
                continue
            primary_ip_id = ip_s.id
            net_ip_ids = row[4].split('+')
            net_name_ids = ['0']
            if not net_ip_ids:
                print hostname + 'net ip: ' + 'Error' + ";;;row:" + str(i)
                message_date.append(hostname + 'net ip: ' + 'Error' + ";;;row:" + str(i))
                continue
            # for ex_index in range(len(net_ip_ids)):
            #     net_name_ids.append(ex_index)
            isEx0Sameip = False
            for ip_n in net_ip_ids:
                if (ip_n == row[3]):
                    isEx0Sameip = True
            if not isEx0Sameip:
                print hostname + 'net ip: ' + 'not same ip' + ";;;row:" + str(i)
                message_date.append(hostname + 'net ip: ' + 'not same ip' + ";;;row:" + str(i))
                continue
            net_ip_ids_id = []
            for ip_s in net_ip_ids:
                ip_ns = IpAddress.query.filter(IpAddress.ipv4 == ip_s).first()
                if not ip_ns:
                    print hostname + 'don not have net ip: ' + ip_ns + ";;;row:" + str(i)
                    message_date.append(hostname + 'don not have net ip: ' + ip_ns + ";;;row:" + str(i))
                    continue
                if ip_ns.flag == 1:
                    print hostname + 'net ip: ' + ip_ns + 'Occupyed' + ";;;row:" + str(i)
                    message_date.append(hostname + 'don not have net ip: ' + ip_ns + ";;;row:" + str(i))
                    continue
            net_ip_ids_id.append(ip_ns.id)
            su_name = row[6]
            print su_name
            ip_s_su = IpAddress.query.filter(IpAddress.ipv4 == su_name).first()
            if not ip_s_su:
                print hostname + 'su ip: ' + su_name + 'not exist' + ";;;row:" + str(i)
                message_date.append(hostname + 'su ip: ' + su_name + 'not exist' + ";;;row:" + str(i))
                continue
            su_s = Host.query.filter(Host.primary_ip_id == ip_s_su.id, Host.is_virtual == 0).first()
            if not su_s:
                print hostname + 'su zhu: ' + su_name + 'not existed' + ";;;row:" + str(i)
                message_date.append(hostname + 'su zhu: ' + su_name + 'not existed' + ";;;row:" + str(i))
                continue
            parent_id = su_s.id
            cpu = row[7]
            memory = row[8]
            storage = row[9]
            device_id = 0
            status = 2
            hardware_info = {'cpu': cpu, 'memory': memory, 'storage': storage}
            data = {'hostname': hostname, 'is_virtual': is_virtual, 'type': type, 'note': note,
                    'primary_ip_id': primary_ip_id, 'search': '',
                    'net_ip_ids': net_ip_ids_id, 'parent_id': parent_id, 'device_id': device_id, 'status': status,
                    'hardware_info': hardware_info
                , 'net_name_ids': net_name_ids}

            _add_host(data)
        # if(message_date):
        #     html_show=''
        #     for m in message_date:
        #         html_show+="<li>"+m+"</li>"
        #     return (html_show)
        return app.response_class(json.dumps({'code': 1, 'msg': '', 'data': message_date}), mimetype='application/json')

    except Exception, e:
        print e
        return app.response_class(json.dumps({'code': 0, 'msg': '文件格式和内容不正确！', 'data': ''}),
                                  mimetype='application/json')

@host.route("/importdb_true", methods=['POST', 'GET'])
@login_required
def importdb_true():
    try:
        f = request.files['fileToUpload']
        fname = secure_filename(f.filename)
        f.save(os.path.join(UPLOAD_FOLDER, 'host_true.xlsx'))
        BASE_DIR = (os.path.dirname(__file__))

        host_xlsx = os.path.join(UPLOAD_FOLDER, 'host_true.xlsx')
        data = xlrd.open_workbook(host_xlsx)
        table = data.sheets()[0]
        nrows = table.nrows
        message_date = []
        for i in range(nrows):
            if i == 0:
                continue
            row = table.row_values(i)
            print row
            hostname = row[0]
            is_virtual = 1
            type = 1
            note = row[5]
            ip_s = IpAddress.query.filter(IpAddress.ipv4 == row[3]).first()
            if not ip_s:
                print hostname + 'don not have ip: ' + row[3] + ";;;row:" + str(i)
                message_date.append(hostname + 'don not have ip: ' + row[3] + ";;;row:" + str(i))
                continue
            if ip_s.flag == 1:
                print hostname + ' ip: ' + row[3] + 'Occupyed' + ";;;row:" + str(i)
                message_date.append(hostname + ' ip: ' + row[3] + 'Occupyed' + ";;;row:" + str(i))
                continue
            primary_ip_id = ip_s.id
            net_ip_ids = row[4].split('+')
            net_name_ids = ['0']
            if not net_ip_ids:
                print hostname + 'net ip: ' + 'Error' + ";;;row:" + str(i)
                message_date.append(hostname + 'net ip: ' + 'Error' + ";;;row:" + str(i))
                continue
            # for ex_index in range(len(net_ip_ids)):
            #     net_name_ids.append(ex_index)
            isEx0Sameip = False
            for ip_n in net_ip_ids:
                if (ip_n == row[3]):
                    isEx0Sameip = True
            if not isEx0Sameip:
                print hostname + 'net ip: ' + 'not same ip' + ";;;row:" + str(i)
                message_date.append(hostname + 'net ip: ' + 'not same ip' + ";;;row:" + str(i))
                continue
            net_ip_ids_id = []
            for ip_s in net_ip_ids:
                ip_ns = IpAddress.query.filter(IpAddress.ipv4 == ip_s).first()
                if not ip_ns:
                    print hostname + 'don not have net ip: ' + ip_ns + ";;;row:" + str(i)
                    message_date.append(hostname + 'don not have net ip: ' + ip_ns + ";;;row:" + str(i))
                    continue
                if ip_ns.flag == 1:
                    print hostname + 'net ip: ' + ip_ns + 'Occupyed' + ";;;row:" + str(i)
                    message_date.append(hostname + 'don not have net ip: ' + ip_ns + ";;;row:" + str(i))
                    continue
            net_ip_ids_id.append(ip_ns.id)

            device_ip=row[10]
            ips_ss=IpAddress.query.filter(IpAddress.ipv4 == device_ip).first()
            if (ips_ss):
                d_ip_s=DeviceIp.query.filter(DeviceIp.ip_address_id == ips_ss.id).first()
                if(d_ip_s):
                    device_id=d_ip_s.device_id
                else:
                    print 'device don not have net ip: ' + device_ip + ";;;row:" + str(i)
                    message_date.append('device don not have net ip: ' + device_ip + ";;;row:" + str(i))
                    continue
            else:
                print 'device don not have net ip: ' + device_ip + ";;;row:" + str(i)
                message_date.append('device don not have net ip: ' + device_ip + ";;;row:" + str(i))
                continue
            # su_name = row[6]
            # ip_s_su = IpAddress.query.filter(IpAddress.ipv4 == su_name).first()
            # if not ip_s_su:
            #     print hostname + 'su ip: ' + su_name + 'not exist' + ";;;row:" + str(i)
            #     message_date.append(hostname + 'su ip: ' + su_name + 'not exist' + ";;;row:" + str(i))
            #     continue
            # su_s = Host.query.filter(Host.primary_ip_id == ip_s_su.id, Host.is_virtual == 0).first()
            # if not su_s:
            #     print hostname + 'su zhu: ' + su_name + 'not existed' + ";;;row:" + str(i)
            #     message_date.append(hostname + 'su zhu: ' + su_name + 'not existed' + ";;;row:" + str(i))
            #     continue
            parent_id = 0
            cpu = row[7]
            memory = row[8]
            storage = row[9]
            # device_id = 0
            status = 2
            hardware_info = {'cpu': cpu, 'memory': memory, 'storage': storage}
            data = {'hostname': hostname, 'is_virtual': 0, 'type': type, 'note': note,
                    'primary_ip_id': primary_ip_id, 'search': '',
                    'net_ip_ids': net_ip_ids_id, 'parent_id': parent_id, 'device_id': device_id, 'status': status,
                    'hardware_info': hardware_info
                , 'net_name_ids': net_name_ids}

            _add_host(data)
        # if(message_date):
        #     html_show=''
        #     for m in message_date:
        #         html_show+="<li>"+m+"</li>"
        #     return (html_show)
        return app.response_class(json.dumps({'code': 1, 'msg': '', 'data': message_date}), mimetype='application/json')

    except Exception, e:
        print e
        return app.response_class(json.dumps({'code': 0, 'msg': '文件格式和内容不正确！', 'data': ''}),
                                  mimetype='application/json')

@host.route("/importpoolhost", methods=['POST', 'GET'])
@login_required
def importpoolhost():
    import_pool_host()
    return responsejson(1, 'Department add failed!')


class ExportExcel():
    def exportexcel(self, sheetname, head, content):
        wb = xlwt.Workbook(encoding='utf-8')
        ws = wb.add_sheet(sheetname)
        row = 1
        for column, name in enumerate(head):
            ws.write(0, column, name)
        for count, name in enumerate(content):
            for column, item in enumerate(name):
                ws.write(row, column, item)
            row += 1
        sio = StringIO.StringIO()
        wb.save(sio)
        value = sio.getvalue()
        return value


@host.route('/export/<exporthost>', methods=['GET', 'POST'])
@login_required
def host_excel(exporthost):
    # print exporthost
    head = ('id', '主机名称', 'IP', '类型', '虚机?', '状态', 'CPU', '内存', '硬盘')
    exporthost = exporthost[:-1]
    exporthost = exporthost[1:]
    sp_host = exporthost.split('],')
    id_list = []
    use_host = []

    for h in sp_host:
        temps = int(h.split(',')[0].replace('[', '').replace(']', '').replace('L', ''))
        id_list.append((temps))


    # use_host=request.form['hosts']

    uid = current_user.id
    sa_uids = app.config.get("SA_UIDS")

    hosts = Host.query.all()
    type_status_ids = Host.query.filter(Host.deleted == Host.DELETED_NO).distinct().all()
    type_ids = []
    status_ids = []
    type_name = {}
    status_name = {}
    contents = []
    if type_status_ids:
        for item in type_status_ids:
            if item.type not in type_ids:
                type_ids.append(item.type)
                type_name[item.type] = _get_type_name(item.type)

            if item.status not in status_ids:
                status_ids.append(item.status)
                tmp_status_name = _get_status_name(item.status)
                if tmp_status_name == "可使用":
                    if uid in sa_uids:
                        status_name[item.status] = tmp_status_name
                else:
                    status_name[item.status] = tmp_status_name
    if hosts:
        for host in hosts:
            host.ip = _get_ip(host.primary_ip_id)
            host.type_name = _get_type_name(host.type)
            for id_s in id_list:
                if (host.id == id_s):
                    contents.append(
                        [host.id, host.hostname, host.ip, host.type_name, host.virtual_descri, host.status_descri,
                         host.cpu_descri,
                         host.memory_descri, host.storage_descri])
                    break

    excel = ExportExcel()
    value = excel.exportexcel('Sheet1', head, contents)
    return make_response(value, 200, {'Content-type': 'application/vnd.ms-excel',
                                      'Content-Disposition': 'attachment;filename="hosts.xls"'})


@host.route('/export_all', methods=['GET', 'POST'])
@login_required
def export_all():
    # print exporthost
    head = ('id', '主机名称', 'IP', '类型', '虚机?', '状态', 'CPU', '内存', '硬盘','部门','Pool','运维负责人','pool负责人','业务负责人')

    # use_host=request.form['hosts']

    uid = current_user.id
    sa_uids = app.config.get("SA_UIDS")

    hosts = Host.query.all()
    type_status_ids = Host.query.filter(Host.deleted == Host.DELETED_NO).distinct().all()
    type_ids = []
    status_ids = []
    type_name = {}
    status_name = {}
    contents = []
    if type_status_ids:
        for item in type_status_ids:
            if item.type not in type_ids:
                type_ids.append(item.type)
                type_name[item.type] = _get_type_name(item.type)

            if item.status not in status_ids:
                status_ids.append(item.status)
                tmp_status_name = _get_status_name(item.status)
                if tmp_status_name == "可使用":
                    if uid in sa_uids:
                        status_name[item.status] = tmp_status_name
                else:
                    status_name[item.status] = tmp_status_name
    if hosts:
        for host in hosts:
            host.ip = _get_ip(host.primary_ip_id)
            host.type_name = _get_type_name(host.type)
            pool_name='unkonw'
            pool_ops='unkonw'
            pool_team='unkonw'
            pool_biz='unkonw'
            pool_s=PoolHost.query.filter(PoolHost.host_id==host.id).first()
            department_name='unkonw'
            if pool_s:
                pool=Pool.query.filter(Pool.id==pool_s.pool_id).first()
                if pool:
                    pool_name=pool.name
                    user_s=User.query.filter(User.id==pool.ops_owner).first()
                    if user_s:
                        pool_ops=user_s.cn_name

                    user_s1=User.query.filter(User.id==pool.team_owner).first()
                    if user_s1:
                        pool_team=user_s1.cn_name

                    user_s2=User.query.filter(User.id==pool.biz_owner).first()
                    if user_s2:
                        pool_biz=user_s2.cn_name
                if pool.department_id!=0:
                    department=Department.query.filter(Department.id==pool.department_id).first()
                    department_name=department.name

            contents.append(
                [host.id, host.hostname, host.ip, host.type_name, host.virtual_descri, host.status_descri,
                 host.cpu_descri,host.memory_descri, host.storage_descri,department_name,
                 pool_name,pool_ops,pool_team,pool_biz])

    excel = ExportExcel()
    value = excel.exportexcel('Sheet1', head, contents)
    return make_response(value, 200, {'Content-type': 'application/vnd.ms-excel',
                                      'Content-Disposition': 'attachment;filename="hosts.xls"'})

@host.route("/add", methods=['POST', 'GET'])
@login_required
def add():
    if request.method == 'POST':
        data = _get_data()
        _add_host(data)
        type = 'host'
        if 'type' in request.form:
            type = request.form['type']

        if type == "device":
            d_id = request.form['device_id']
            return redirect(url_for('device.detail', id=d_id))
        else:
            return redirect(url_for('host.index'))


@host.route("/modify", methods=['POST', 'GET'])
@login_required
def modify():
    if request.method == 'POST':
        data = _get_data()
        if data['host_id'] > 0:
            status = _modify_host(data['host_id'], data)
        if request.referrer:
            return redirect(request.referrer)
        else:
            return redirect(url_for('host.index'))


@host.route("/delete/<int:id>", methods=['POST'])
@login_required
def delete(id):
    code = 0
    msg = "删除成功"
    if request.method == 'POST':
        host_info = Host.query.filter(Host.id == id).first()
        if not __delete_host(host_info):
            code = 1
            msg = "删除失败(不存在此主机)"
    else:
        code = 1
        msg = "删除失败(不存在此主机)"
    return responsejson(code, msg)


@host.route("/apply/add", methods=['POST', 'GET'])
@login_required
def apply():
    approver_uid = app.config.get("APPROVER")['host']
    approver = User.query.filter(User.id == approver_uid).first().cn_name
    approver_name_info = User.query.filter(User.id == current_user.superior_id).first()
    if approver_name_info:
        approver = approver_name_info.cn_name
        approver_uid = approver_name_info.id

    if request.method == "GET":
        idc_info = Datacenter.query.filter(Datacenter.name != 'Office').all()
        apply = Apply()
        host_type = apply.host_type_desc()
        os_type_info = apply.os_type_desc()
        os_type = dict(os_type_info)['ubuntu']
        pool_info = Pool.query.all()
        return render_template("host/apply.html", idc_info=idc_info, pool_info=pool_info, host_type=dict(host_type),
                               os_type=os_type, approver=approver)
    else:
        code = 0
        msg = ""
        uid = current_user.id
        cpu = int(request.form['cpu'].strip())
        mem = int(request.form['mem'].strip())
        disk = int(request.form['disk'].strip())
        idc = int(request.form['idc'].strip())
        pool_id = int(request.form['pool_id'].strip())
        num = int(request.form['num'].strip())
        os = request.form['os'].strip()
        content = request.form['content'].strip()
        template = {'cpu': cpu, 'mem': mem, 'disk': disk, 'os': os}
        type = int(request.form['host_type'].strip())
        target = Apply(uid=uid, approver_uid=approver_uid, pool_id=pool_id, type=type, idc=idc, num=num,
                       content=content,
                       template=str(template))
        db.session.add(target)
        db.session.commit()
        return responsejson(code, msg)


@host.route("/apply", methods=['POST', 'GET'])
@login_required
def host_apply():
    per_page = 50
    range_num = 10
    p = request.args.get('p', 1)
    target = db.session.query(User.cn_name, Pool, Apply).filter(and_(User.id == Apply.uid, Pool.id == Apply.pool_id))
    if target:
        total_num = target.count()
        page = Paginator(total_num, per_page=per_page, current=p, range_num=range_num)
        target_info = target.order_by(Apply.id.desc()).offset((int(p) - 1) * per_page).limit(per_page).all()
        apply_host = []

    for item in target_info:
        apply_info = {}
        apply_info['id'] = item.Apply.id
        apply_info['applier_name'] = item.cn_name
        if item.Pool.source_desc:
            apply_info['pool_name'] = item.Pool.source_desc + item.Pool.name
        else:
            apply_info['pool_name'] = item.Pool.name
        apply_info['pool_id'] = item.Pool.id
        apply_info['pool_len'] = len(item.Pool.name)
        apply_info['idc_name'] = item.Apply.idc_desc
        apply_info['host_type'] = item.Apply.type_desc
        apply_info['cpu'] = eval(item.Apply.template)['cpu']
        apply_info['mem'] = eval(item.Apply.template)['mem']
        apply_info['disk'] = eval(item.Apply.template)['disk']
        apply_info['os'] = eval(item.Apply.template)['os']
        apply_info['num'] = item.Apply.num
        host_apply_info = Apply_host.query.filter(
            and_(Apply_host.apply_id == item.Apply.id, Apply_host.status == Apply_host.ACTIVE)).all()
        hostinfo = []
        for a in host_apply_info:
            host_info = Host.query.filter(Host.id == a.host_id).first()
            tmp = host_info.hostname + '</br>'
            hostinfo.append({tmp: host_info.id})
        apply_info['host_info'] = hostinfo
        apply_info['content'] = item.Apply.content
        apply_info['created'] = item.Apply.created
        apply_info['status'] = item.Apply.status_desc
        apply_info['status_id'] = item.Apply.status
        apply_host.append(apply_info)

    return render_template("bastion/apply.html", flag="host_apply", p=page, apply_host=apply_host)


@host.route("/", methods=['POST', 'GET'])
@login_required
def index():
    show = visible()
    uid = current_user.id
    sa_uids = app.config.get("SA_UIDS")
    per_page = 50
    range_num = 10
    p = request.args.get('p', 1)
    rack_id = request.args.get('rack_id', 0)
    q = request.args.get("q", '')
    type = request.args.get('type', 0)
    status = request.args.get('status', 0)
    host_target = Host.query.filter(Host.deleted == Host.DELETED_NO)
    url = ''
    if int(type) != 0:
        host_target = host_target.filter(Host.type == type)
        url = '%s&type=%d' % (url, int(type))
    if int(status) != 0:
        host_target = host_target.filter(Host.status == status)
        url = '%s&status=%d' % (url, int(status))
    if q:
        url = '%s&q=%s' % (url, q.strip())
        kw = '%' + q + '%'
        host_target = host_target.filter(Host.search.like(kw))

    if int(rack_id) != 0:
        device = Device.query.filter(Device.rack_id == rack_id).all()
        if device:
            device_id = []
            for item in device:
                device_id.append(item.id)
            hosts = Host.query.filter(Host.device_id.in_(device_id)).all()
            apc_id = []
            if hosts:
                for item in hosts:
                    if item.is_virtual == 0:
                        apc_id.append(item.id)
                host_target = host_target.filter(or_(Host.parent_id.in_(apc_id), Host.device_id.in_(device_id)))
        url = '%s&rack_id=%d' % (url, int(rack_id))
    total_num = host_target.count()
    page = Paginator(total_num, per_page=per_page, current=p, range_num=range_num)
    hosts = host_target.order_by(Host.id.desc()).offset((int(p) - 1) * per_page).limit(per_page).all()
    type_status_ids = Host.query.filter(Host.deleted == Host.DELETED_NO).distinct().all()
    type_ids = []
    status_ids = []
    type_name = {}
    status_name = {}
    if type_status_ids:
        for item in type_status_ids:
            if item.type not in type_ids:
                type_ids.append(item.type)
                type_name[item.type] = _get_type_name(item.type)

            if item.status not in status_ids:
                status_ids.append(item.status)
                tmp_status_name = _get_status_name(item.status)
                if tmp_status_name == "可使用":
                    if uid in sa_uids:
                        status_name[item.status] = tmp_status_name
                else:
                    status_name[item.status] = tmp_status_name
    export_host = []
    if hosts:
        for host in hosts:
            host.ip = _get_ip(host.primary_ip_id)
            host.type_name = _get_type_name(host.type)
            export_host.append(
                [host.id, host.hostname, host.ip, host.type_name, host.virtual_descri, host.status_descri,
                 host.cpu_descri,
                 host.memory_descri, host.storage_descri])

    extendinfo = {
        'total': total_num,
        'cur_total': len(hosts),
        'show_special': True if uid in sa_uids else False
    }
    return render_template("host/list.html", datas=hosts, p=page, q=q, url=url, type=type, status=status,
                           type_name=type_name, status_name=status_name, rack_id=rack_id,
                           show=show, flag='hostlist', extendinfo=extendinfo, export_host=export_host)


def _get_data():
    host_id = int((request.form['host_id']), 0)
    is_virtual = int(request.form['is_virtual'])
    data = {}
    data['host_id'] = host_id
    if is_virtual == 0:
        # 实体机
        data['is_virtual'] = 0
        data['type'] = request.form['host_type']
        data['parent_id'] = 0
        data['device_id'] = request.form['device_id']  # _get_device_id(request.form['remote_ip_id'])
    else:
        # 虚机
        data['is_virtual'] = 1
        data['type'] = Host.TYPE_APP
        data['parent_id'] = request.form['entity_host_id']
        data['device_id'] = 0
    data['hostname'] = request.form['hostname']
    data['primary_ip_id'] = request.form['primary_ip_id']
    data['status'] = Host.STATUS_READY
    data['note'] = request.form['note']
    data['search'] = ""
    data['net_name_ids'] = {}
    data['net_ip_ids'] = {}
    if request.form.getlist('net_name_id[]'):
        data['net_name_ids'] = request.form.getlist('net_name_id[]')
        data['net_ip_ids'] = request.form.getlist('net_ip_id[]')
    data['hardware_info'] = _get_hardware_info()
    if not data['hostname']:
        flash('请输入主机名')
        return redirect(url_for('host.index'))
    if int(data['primary_ip_id']) == 0:
        flash('请输入ip地址')
        return redirect(url_for('host.index'))
    if is_virtual == 1 and int(data['parent_id']) == 0:
        flash('请输入宿主机名称')
        return redirect(url_for('host.index'))
    if data['net_ip_ids']:
        for ip_id in data['net_ip_ids']:
            if int(ip_id) == 0:
                flash('请输入网卡ip')
                return redirect(url_for('host.index'))
    return data


def _add_host(data):
    hasIn = Host.query.filter(Host.hostname == data['hostname']).first()
    if hasIn:
        flash('此主机名已存在')
        return redirect(url_for('host.index'))
    host = Host(data['hostname'], data['primary_ip_id'], data['type'], data['is_virtual'], data['parent_id'],
                data['device_id'], data['status'], data['hardware_info']['cpu'],
                data['hardware_info']['memory'], data['hardware_info']['storage'], data['note'], search=data['search'])
    db.session.add(host)
    db.session.commit()

    _set_used_ip(data['primary_ip_id'], IpAddress.FLAG_USED, IpAddress.TYPE_HOST, host.id)
    if data['primary_ip_id']:
        if '0' not in data['net_name_ids']:
            _add_host_ip(host.id, 0, data['primary_ip_id'])

    if data['net_ip_ids']:
        _add_net_ip(host.id, data['net_ip_ids'], data['net_name_ids'])

    log = json.dumps({'create': '创建一台主机'}, ensure_ascii=False, separators=(',', ':')).encode('utf8')
    _operation_log(host.id, current_user.id, log)
    # 添加设备日志
    uid = 0
    if current_user:
        uid = current_user.id
    log_data = {}
    log_data['host_add'] = "添加主机(主机名:<a href='/cmdb/host/%s'>%s</a>,主机ID:<a href='/cmdb/host/%s'>%s</a>)" % (
    host.id, host.hostname, host.id, host.id)
    log = json.dumps(log_data, ensure_ascii=False, separators=(',', ':')).encode('utf8')
    if int(data['is_virtual']) == 1:
        parent_host_info = Host.query.filter(Host.id == data['parent_id']).first()
        data['device_id'] = parent_host_info.device_id

    from views.device import _operation_log as _device_op_log
    _device_op_log(data['device_id'], uid, log)

    host_device_changed.delay(host.id, 1, 1)


def import_host():
    try:
        BASE_DIR = (os.path.dirname(__file__))
        host_xlsx = os.path.join(BASE_DIR, 'host1.xlsx')
        data = xlrd.open_workbook(host_xlsx)
        table = data.sheets()[0]
        nrows = table.nrows
        for i in range(nrows):
            if i == 0:
                continue
            row = table.row_values(i)
            print row
            hostname = row[0]
            is_virtual = 1
            type = 1
            note = row[5]
            ip_s = IpAddress.query.filter(IpAddress.ipv4 == row[3]).first()
            if not ip_s:
                print hostname + 'don not have ip: ' + row[3] + ";;;row:" + str(i)
                continue
            if ip_s.flag == 1:
                print hostname + ' ip: ' + row[3] + 'Occupyed' + ";;;row:" + str(i)
                continue
            primary_ip_id = ip_s.id
            net_ip_ids = row[4].split('+')
            net_name_ids = ['0']
            if not net_ip_ids:
                print hostname + 'net ip: ' + 'Error' + ";;;row:" + str(i)
                continue
            # for ex_index in range(len(net_ip_ids)):
            #     net_name_ids.append(ex_index)
            isEx0Sameip = False
            for ip_n in net_ip_ids:
                if (ip_n == row[3]):
                    isEx0Sameip = True
            if not isEx0Sameip:
                print hostname + 'net ip: ' + 'not same ip' + ";;;row:" + str(i)
                continue
            net_ip_ids_id = []
            for ip_s in net_ip_ids:
                ip_ns = IpAddress.query.filter(IpAddress.ipv4 == ip_s).first()
                if not ip_ns:
                    print hostname + 'don not have net ip: ' + ip_ns + ";;;row:" + str(i)
                    continue
                if ip_ns.flag == 1:
                    print hostname + 'net ip: ' + ip_ns + 'Occupyed' + ";;;row:" + str(i)
                    continue
            net_ip_ids_id.append(ip_ns.id)
            su_name = row[6]
            ip_s_su = IpAddress.query.filter(IpAddress.ipv4 == su_name).first()
            if not ip_s_su:
                print hostname + 'su ip: ' + su_name + 'not exist' + ";;;row:" + str(i)
                continue
            su_s = Host.query.filter(Host.primary_ip_id == ip_s_su.id, Host.is_virtual == 0).first()
            if not su_s:
                print hostname + 'su zhu: ' + su_name + 'not existed' + ";;;row:" + str(i)
                continue
            parent_id = su_s.id
            cpu = row[7]
            memory = row[8]
            storage = row[9]
            device_id = 0
            status = 2
            hardware_info = {'cpu': cpu, 'memory': memory, 'storage': storage}
            data = {'hostname': hostname, 'is_virtual': is_virtual, 'type': type, 'note': note,
                    'primary_ip_id': primary_ip_id, 'search': '',
                    'net_ip_ids': net_ip_ids_id, 'parent_id': parent_id, 'device_id': device_id, 'status': status,
                    'hardware_info': hardware_info
                , 'net_name_ids': net_name_ids}

            _add_host(data)
        return True
    except Exception, e:
        print e


def import_pool_host():
    try:
        BASE_DIR = (os.path.dirname(__file__))
        host_xlsx = os.path.join(BASE_DIR, 'hostpool1.xlsx')
        data = xlrd.open_workbook(host_xlsx)
        table = data.sheets()[0]
        nrows = table.nrows
        host_ids = ''
        pool_id = ''
        for i in range(nrows):
            host_ids = ''
            if i == 0:
                continue
            row = table.row_values(i)
            pool_name = row[0]
            host_ip_list = row[1].split(',')
            pool_s = Pool.query.filter(Pool.name == pool_name).first()
            if not pool_s:
                print pool_name + 'not existed' + ";;;row:" + str(i)
                continue
            pool_id = pool_s.id
            for host_each_ip in host_ip_list:
                ip_s = IpAddress.query.filter(IpAddress.ipv4 == host_each_ip).first()
                if not ip_s:
                    print pool_name + ": ip :" + host_each_ip + 'not existed' + ";;;row:" + str(i)
                    continue
                host_ip_s = HostIp.query.filter(HostIp.ip_address_id == ip_s.id).first()
                if not host_ip_s:
                    print pool_name + ": ip :" + host_each_ip + 'host not existed' + ";;;row:" + str(i)
                    continue
                host_ids += str(host_ip_s.host_id) + ','
            hostadd(host_ids[:-1], str(pool_id))

        return True
    except Exception, e:
        print e


def hostadd(host_ids_f, pool_id):
    try:
        from views.pool import *
        code = 0
        msg = "为pool添加主机成功"

        intreg = re.compile('^[1-9]\d*$')
        host_ids = host_ids_f.split(",")
        if len(host_ids) <= 0:
            code = 1
            print "操作提示:为pool添加主机失败,主机编号格式不对"
            return responsejson(code, msg)
        if not intreg.match(pool_id):
            code = 1
            print "操作提示:为pool添加主机失败,pool编号格式不对"
            return responsejson(code, msg)
        poolinfo = Pool.query.filter(Pool.id == pool_id).first()
        if not poolinfo:
            code = 1
            print "操作提示:为pool添加主机失败,pool不存在"
            return responsejson(code, msg)
        logmsg = ""
        for host_id in host_ids:
            hostinfo = Host.query.filter(Host.id == host_id).first()
            if not hostinfo:
                continue
            hasIn = PoolHost.query.filter(and_(PoolHost.pool_id == pool_id, PoolHost.host_id == host_id)).all()
            if hasIn:
                continue

            poolhosttarget = PoolHost(pool_id, host_id)
            db.session.add(poolhosttarget)
            db.session.commit()
            log_data = {}
            log_data['pooladd'] = "添加主机入POOL,<a href='/cmdb/pool/detail/%s'>%s</a>" % (poolinfo.id, poolinfo.name)
            uid = 0
            if current_user:
                uid = current_user.id
            log = json.dumps(log_data, ensure_ascii=False, separators=(',', ':')).encode('utf8')
            # _host_op_log(hostinfo.id,uid,log)

            tmp_host_status = Host.STATUS_ASSIGNED
            if poolinfo.source > 0:
                tmp_host_status = Host.STATUS_ONLINE

            if int(tmp_host_status) > int(hostinfo.status):
                log_data = {}
                log_data['status'] = '主机状态:从 %s 更改为 %s ' % (
                host_status_mapping(hostinfo.status), host_status_mapping(tmp_host_status))
                hostinfo.status = tmp_host_status
                db.session.commit()
                log = json.dumps(log_data, ensure_ascii=False, separators=(',', ':')).encode('utf8')
                # _host_op_log(hostinfo.id,uid,log)

            logmsg = "%s,主机编号:%s  name:%s" % (logmsg, host_id, hostinfo.hostname)

        if logmsg:
            logmsg = " 在%s添加主机%s" % (poolinfo.name, logmsg)
            addlog(logmsg, 1)
        else:
            code = 1
            msg = "操作提示:没有添加任何主机(所选主机已经添加了)"
        return responsejson(code, msg)
    except Exception, e:
        print e


def _modify_host(host_id, data):
    host = Host.query.filter(Host.id == host_id).first()
    log_data = {}
    if host:
        if str(data['primary_ip_id']) != str(host.primary_ip_id):
            _set_used_ip(host.primary_ip_id)
            _set_used_ip(data['primary_ip_id'], IpAddress.FLAG_USED, IpAddress.TYPE_HOST, host_id)
            log_data['primary_ip_id'] = '主机主IP 从ID' + str(host.primary_ip_id) + '更改为' + str(data['primary_ip_id'])
            host.primary_ip_id = data['primary_ip_id']

        if str(host.hostname) != str(data['hostname']):
            hasIn = Host.query.filter(Host.hostname == data['hostname']).all()
            if hasIn:
                flash('此主机名已存在')
                return redirect(url_for('host.index'))
            log_data['hostname'] = '主机名称 从' + str(host.hostname) + '更改为' + str(data['hostname'])
            host.hostname = data['hostname']

        if str(host.type) != str(data['type']) and str(host.is_virtual) == '0':
            # log_data['type'] = '主机类型 从' + str(_get_type_name(host.type)) + '更改为' + str(_get_type_name(data['type']))
            log_data['type'] = '主机类型 从' + str(host.type) + '更改为' + str(data['type'])
            host.type = data['type']

        if str(host.is_virtual) != str(data['is_virtual']):
            host.is_virtual = data['is_virtual']

        if str(host.parent_id) != str(data['parent_id']) and str(host.is_virtual) == '1':
            log_data['parent_id'] = 'parent_id ' + str(host.parent_id) + '更改为' + str(data['parent_id'])
            host.parent_id = data['parent_id']

        if str(host.device_id) != str(data['device_id']) and str(host.is_virtual) == '0':
            log_data['device_id'] = '设备ID 从' + str(host.device_id) + '更改为' + str(data['device_id'])
            host.device_id = data['device_id']

        if str(host.note) != str(data['note']):
            log_data['note'] = '备注 从' + str(host.note) + '更改为' + str(data['note'])
            host.note = data['note']

        # host.status = data['status']
        db.session.add(host)
        # dns_zone_info = DnsZone.query.filter(DnsZone.zone == "i.ajkdns.com").first()
        # zone_id = dns_zone_info.id
        # dns_apply_info = DnsApply.query.filter(and_(DnsApply.prefix == "update",DnsApply.zone_id==zone_id)).first()
        # dns_apply_id = dns_apply_info.id
        # dns_task_target = DnsTasks(dns_apply_id=dns_apply_id, type=1, status=0)
        # db.session.add(dns_task_target)
        # db.session.commit()

        origin_ip_id = []
        now_ip_id = []
        host_ips = HostIp.query.filter(HostIp.host_id == host_id).all()
        if host_ips:
            for host_ip in host_ips:
                origin_ip_id.append(str(host_ip.ip_address_id))
        for x in data['net_ip_ids']:
            now_ip_id.append(x.encode('UTF8'))

        del_ip_ids = list((set(origin_ip_id) - (set(origin_ip_id) & set(now_ip_id))))
        _modify_net_ip(host_id, del_ip_ids, data['net_ip_ids'], data['net_name_ids'])
        notchanged = True
        if log_data:
            log = json.dumps(log_data, ensure_ascii=False, separators=(',', ':')).encode('utf8')
            _operation_log(host.id, current_user.id, log)
            notchanged = False
        host_device_changed.delay(host.id, 1, 2)
        return notchanged


def __delete_host(host_info):
    if host_info and host_info.deleted == Host.DELETED_NO:
        host_id = host_info.id
        # 如果是虚拟机 从opennebula中删除
        if host_info.is_virtual == Host.IS_VIRTUAL_YES:
            import requests
            APC_URL = "http://apc10-001.i.ajkdns.com:4567"
            APC_AUTH = "Basic b25lYWRtaW46YTEyZTJjMzU0ZDQxZDdlMmI2ZDlkZGNiZWUzZjY5NDk5OWQ0MTkyNw=="
            vm_id = 0
            virtual_host_info = Apply_host.query.filter(Apply_host.host_id == host_id).first()
            if virtual_host_info:
                vm_id = virtual_host_info.vm_id
            if vm_id > 0:
                APC_URL = "%s/compute/%d" % (APC_URL, int(vm_id))
                requests.delete(APC_URL, headers={'Authorization': APC_AUTH})
        host_info.deleted = 1
        _set_used_ip(host_info.primary_ip_id)
        db.session.commit()
        hostip_info = HostIp.query.filter(HostIp.host_id == host_id).all()
        if hostip_info:
            for item in hostip_info:
                _set_used_ip(item.ip_address_id)
                db.session.commit()
            HostIp.query.filter(HostIp.host_id == host_id).delete()
            db.session.commit()
        Alarm.query.filter(and_(Alarm.target_id == host_id, Alarm.type == Alarm.TYPE_HOST)).delete()
        Follow.query.filter(and_(Follow.target_id == host_id, Follow.type == Follow.TYPE_HOST)).delete()
        PoolHost.query.filter(and_(PoolHost.host_id == host_id)).delete()
        zabbix_rmhost(host_info.hostname)
        log = json.dumps({'create': '删除一台主机(API)'}, ensure_ascii=False, separators=(',', ':')).encode('utf8')
        __host_operation_log(host_info.id, current_user.id, log)
        ##删除主机在设备中添加删除日志
        device_id = 0
        if host_info.is_virtual == 1:
            parentinfo = Host.query.filter(Host.id == host_info.parent_id).first()
            if parentinfo:
                device_id = parentinfo.device_id
        else:
            device_id = host_info.device_id
        if device_id > 0:
            log_msg = '删除主机(主机名:<a href="/cmdb/host/%s">%s</a>,主机ID:<a href="/cmdb/host/%s">%s</a>)' % (
            host_id, host_info.hostname, host_id, host_id)
            log = json.dumps({'del_host': log_msg}, ensure_ascii=False, separators=(',', ':')).encode('utf8')
            from views.device import _operation_log as __device_operation_log
            __device_operation_log(device_id, current_user.id, log)
        host_device_changed.delay(host_id, 1, 3)
        return True
    else:
        return False


def _add_net_ip(host_id, net_ip_ids, net_name_ids):
    if net_ip_ids:
        for net_ip_id in net_ip_ids:
            _add_host_ip(host_id, net_name_ids[net_ip_ids.index(net_ip_id)], net_ip_id)

    return True


def _add_host_ip(host_id, net_name_id, net_ip_id):
    host_ip_obj = HostIp(host_id, net_name_id, net_ip_id)
    db.session.add(host_ip_obj)
    db.session.commit()
    _set_used_ip(net_ip_id, IpAddress.FLAG_USED, IpAddress.TYPE_HOST, host_id)
    host_device_changed.delay(host_id, 1, 2)


def _modify_net_ip(host_id, del_ip_ids, net_ip_ids, net_name_ids):
    log_data = {}

    # del
    if del_ip_ids:
        for net_ip_id in del_ip_ids:
            _set_used_ip(net_ip_id)
            ip = _get_ip(net_ip_id)
            log_data['net_del_ip_id_' + str(net_ip_id)] = '删除ip: ' + str(ip)
        HostIp.query.filter(and_(HostIp.host_id == host_id, HostIp.ip_address_id.in_(del_ip_ids))).delete(
            synchronize_session='fetch')
        db.session.commit()

    # new
    if net_ip_ids:

        for net_ip_id in net_ip_ids:
            current_host_ip = HostIp.query.filter(and_(HostIp.host_id == host_id,
                                                       HostIp.ip_address_id == net_ip_id)).first()
            if current_host_ip:
                if str(current_host_ip.net_name_id) != net_name_ids[net_ip_ids.index(net_ip_id)]:
                    current_host_ip.net_name_id = net_name_ids[net_ip_ids.index(net_ip_id)]
                    db.session.add(current_host_ip)
                    db.session.commit()
            else:
                _add_host_ip(host_id, net_name_ids[net_ip_ids.index(net_ip_id)], net_ip_id)
                ip = _get_ip(net_ip_id)
                log_data['net_add_ip_id_' + str(net_ip_id)] = '添加ip:' + str(ip)

    if log_data:
        log = json.dumps(log_data, ensure_ascii=False, separators=(',', ':')).encode('utf8')
        _operation_log(host_id, current_user.id, log)

    return True


def _get_ip_id(ip):
    ip_info = IpAddress.query.filter(IpAddress.ipv4 == ip).first()
    if ip_info:
        return ip_info.id
    return 0


def _get_ip(id):
    ip_info = IpAddress.query.filter(IpAddress.id == id).first()
    if ip_info:
        return ip_info.ipv4
    return 0


def _get_device_id(remote_control_ip_id):
    device = Device.query.filter(Device.primary_ip_id == remote_control_ip_id).first()
    if device:
        return device.id
    return 0


def _get_remote_ip_and_id(device_id):
    device = Device.query.filter(Device.id == device_id).first()
    if device:
        # ip = _get_ip(device.primary_ip_id)
        return [device.id, device.device_label]
    return ['', '']


def _get_hardware_info():
    hardware_info = {}
    hardware_info['cpu'] = 0
    hardware_info['memory'] = 0
    hardware_info['storage'] = 0
    return hardware_info


def _get_type_name(type):
    type = int(type)
    if type == Host.TYPE_APC:
        type_name = 'APC'
    elif type == Host.TYPE_APP:
        type_name = 'APP'
    elif type == Host.TYPE_DB:
        type_name = 'DB'
    elif type == Host.TYPE_HADOOP:
        type_name = 'HADOOP'
    else:
        type_name = 'Other'
    return type_name


def _get_status_name(status):
    status = int(status)
    if status == Host.STATUS_START:
        status_name = '裸机'
    elif status == Host.STATUS_READY:
        status_name = '可使用'
    elif status == Host.STATUS_ASSIGNED:
        status_name = '已分配'
    elif status == Host.STATUS_ONLINE:
        status_name = '已上线'
    elif status == Host.STATUS_OFFLINE:
        status_name = '已下线'
    else:
        status_name = '未知'
    return status_name


def _operation_log(host_id, uid, content):
    opt_log = HostOperationHistory(host_id, uid, content)
    db.session.add(opt_log)
    db.session.commit()


def __host_operation_log(host_id, uid, content):
    _operation_log(host_id, uid, content)


def _user_name(uid):
    user = User.query.filter(User.id == uid).first()
    if user:
        return user.cn_name
    return ''


@host.route("/<int:id>", methods=['GET', 'POST'])
@login_required
def host_detail(id):
    show = visible({'host_modify': "/cmdb/host/modify_post"})
    host = Host.query.filter(Host.id == id).first()
    if not host:
        return redirect(url_for('error.index'))

    flag = 0
    if "db" in host.hostname:
        flag = 1
    # device = {'id':0,'device_label':" ",'sn':"未知",'model':"未知",'buy_time':"未知"}
    device = None
    ip = []
    if host.deleted != 1:
        status = host.status_descri
    else:
        status = "已删除"
    if host and host.is_virtual == 0:
        if host.device_id > 0:
            device = Device.query.filter(Device.id == host.device_id).first()
    else:
        parent_host = Host.query.filter(Host.id == host.parent_id).first()
        if parent_host and parent_host.device_id > 0:
            device = Device.query.filter(Device.id == parent_host.device_id).first()
    if device:
        dev_ip = DeviceIp.query.filter(and_(DeviceIp.device_id == device.id, DeviceIp.net_name_id == 0)).all()
        for item in dev_ip:
            dev_ip_add_list = IpAddress.query.filter(IpAddress.id == item.ip_address_id).first()
            ip.append({'name': "远控卡", 'ip': dev_ip_add_list.ipv4})

    ip_list = HostIp.query.filter(HostIp.host_id == id).order_by(HostIp.net_name_id).all()
    if ip_list:
        for val in ip_list:
            ip_ans = IpAddress.query.filter(IpAddress.id == val.ip_address_id).first()
            if val.type == 99:
                list = {'name': "eth%d" % val.net_name_id, 'ip': ip_ans.ipv4}
            else:
                list = {'name': "eth%d:%d" % (val.net_name_id, val.type), 'ip': ip_ans.ipv4}
            ip.append(list)
    lenth = len(ip)
    lines = int((lenth + 2) / 3)
    tmp_ip = []
    type_ip = []
    for i in range(lines):
        for j in range(i * 3, (i + 1) * 3):
            if j <= lenth - 1:
                tmp_ip.append(ip[j])
        type_ip.append(tmp_ip)
        tmp_ip = []
    host.device = device
    rack_info = {'rack_id': 0, 'name': "未知"}
    if device and device.rack_id != 0:
        rack = Rack.query.filter(Rack.id == device.rack_id).first()
        idc = Datacenter.query.filter(Datacenter.id == rack.datacenter_id).first()
        rack_info = {'datacenter_id': rack.datacenter_id, 'rack_id': rack.id, 'idc': idc.name, 'name': rack.name}

    hasFollowed = Follow.query.filter(Follow.type == Follow.TYPE_HOST, Follow.uid == current_user.id,
                                      Follow.target_id == host.id).first()
    if hasFollowed:
        host.followed = 1
    else:
        host.followed = 0

    hasAlarmed = Alarm.query.filter(Alarm.type == Alarm.TYPE_HOST, Alarm.uid == current_user.id,
                                    Alarm.target_id == host.id).first()
    if hasAlarmed:
        host.alarmed = 1
    else:
        host.alarmed = 0

    history = HostOperationHistory.query.filter(HostOperationHistory.host_id == id).order_by(
        HostOperationHistory.id.desc()).limit(5).all()
    if history:
        for item in history:
            item.username = _user_name(item.uid)
            tmp = json.loads(item.content)
            item.content = "; ".join(tmp.values())

    userids = []
    userlist = {}
    alarmUids = []
    poollist = Pool.query.filter(and_(PoolHost.host_id == id, Pool.id == PoolHost.pool_id)).all()
    if poollist:
        for poolinfo in poollist:
            if poolinfo.ops_owner not in userids:
                userids.append(poolinfo.ops_owner)
                alarmUids.append(poolinfo.ops_owner)
            if poolinfo.team_owner not in userids:
                userids.append(poolinfo.team_owner)
                alarmUids.append(poolinfo.team_owner)
            if poolinfo.biz_owner not in userids:
                userids.append(poolinfo.biz_owner)
                alarmUids.append(poolinfo.biz_owner)

    AlarmInFo = Alarm.query.filter(and_(Alarm.type == Alarm.TYPE_HOST, Alarm.target_id == id)).all()
    if AlarmInFo:
        for item_alarm in AlarmInFo:
            if item_alarm.uid not in alarmUids:
                userids.append(item_alarm.uid)
                alarmUids.append(item_alarm.uid)

    roles_userid = []
    bastion_users = {
        'root': '',
        'evans': '',
        'readonly': ''
    }
    users = UserHost.query.filter(and_(UserHost.host_id == id, UserHost.status == UserHost.STATUS_VALID)).all()
    if users:
        for item_user in users:
            tmp_role = 3
            if item_user.role == UserHost.ROLE_ROOT:
                tmp_role = 1
            elif item_user.role == UserHost.ROLE_EVANS:
                tmp_role = 2
            roles_userid.append([item_user.uid, tmp_role])
            userids.append(item_user.uid)

    if userids:
        userinfo = User.query.filter(User.id.in_(userids)).all()
        if userinfo:
            for item in userinfo:
                userlist['uid_%s' % item.id] = item.cn_name

    if poollist:
        for poolinfo in poollist:
            poolinfo.team_owner_name = userlist['uid_%s' % poolinfo.team_owner]
            poolinfo.ops_owner_name = userlist['uid_%s' % poolinfo.ops_owner]
            poolinfo.biz_owner_name = userlist['uid_%s' % poolinfo.biz_owner]

    for tmp_user in roles_userid:
        tmp_username = userlist['uid_%s' % tmp_user[0]]
        tmp_role = tmp_user[1]
        if tmp_role == 1:
            bastion_users['root'] += '%s,' % tmp_username
        elif tmp_role == 2:
            bastion_users['evans'] += '%s,' % tmp_username
        elif tmp_role == 3:
            bastion_users['readonly'] += '%s,' % tmp_username

    bastion_users['root'] = bastion_users['root'][0:-1]
    bastion_users['evans'] = bastion_users['evans'][0:-1]
    bastion_users['readonly'] = bastion_users['readonly'][0:-1]

    alarmusers = ""

    if alarmUids:
        for item_uid in alarmUids:
            alarmusers += '%s,' % userlist['uid_%s' % item_uid]

    alarmusers = alarmusers[0:-1]
    # 满载率
    host.history = history
    host.rack_info = rack_info
    host.pools = poollist
    today = datetime.date.today()
    begin_time = str(today) + ' 00:00:00'
    begin_timestamps = time.mktime(time.strptime(begin_time, '%Y-%m-%d %H:%M:%S'))
    # 多减600就是10分钟,为了就是取两个10分钟弥补当前10分钟可能正在计算
    tmp_step = (time.time() - begin_timestamps - 600) / 600
    hour = '%02d' % int(tmp_step / 6)
    minitus = (int(tmp_step % 6)) * 10
    minitus = '%02d' % minitus
    begin_time_current = str(today) + ' %s:%s:00' % (hour, minitus)
    end_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    host_load_time = "未知"
    current_load = 0
    host_load_infos = HostLoadRatio.query.filter(
        and_(HostLoadRatio.host_id == id, HostLoadRatio.created.between(begin_time_current, end_time))).order_by(
        HostLoadRatio.id.asc()).all() or 0
    if host_load_infos:
        for host_load_info in host_load_infos:
            current_load = host_load_info.ratio * 100
            host_load_time = host_load_info.created.strftime('%Y-%m-%d %H:%M')

    yesterday = today - datetime.timedelta(days=1)
    yesterday = str(yesterday) + ' 00:00:00'
    now_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    host_maxcurrent_ration = HostLoadRatio.query.filter(
        and_(HostLoadRatio.host_id == id, HostLoadRatio.created.between(begin_time, now_time))) \
                                 .order_by(HostLoadRatio.ratio.desc()).limit(1).first() or 0
    if host_maxcurrent_ration:
        max_load = host_maxcurrent_ration.ratio * 100
        max_load_time = host_maxcurrent_ration.created.strftime('%Y-%m-%d %H:%M')
    else:
        max_load = 0
        max_load_time = "未知"
    host_maxyes_ration = HostLoadDaily.query.filter(
        and_(HostLoadDaily.host_id == id, HostLoadDaily.created == yesterday)).first() or 0
    if host_maxyes_ration:
        yes_max_load = host_maxyes_ration.ratio * 100
        yes_load_time = ""
    else:
        yes_max_load = 0
        yes_load_time = "未知"
    load = {
        'host_load': [int(current_load), host_load_time],
        'max_host_load': [int(max_load), max_load_time],
        'yes_host_load': [int(yes_max_load), yes_load_time],
        'id': id
    }
    host.len = len(host.note_info)
    host.short = host.note_info[:17]
    return render_template("host/detail.html", flag=flag, data=host, ip=type_ip, lines=lines, lenth=lenth,
                           status=status, load=load, bastion_users=bastion_users, alarmusers=alarmusers, show=show)


@host.route("/history/<int:id>", methods=['GET', 'POST'])
@login_required
def history(id):
    info = Host.query.filter(Host.id == id).first()
    history = HostOperationHistory.query.filter(HostOperationHistory.host_id == id).order_by(
        HostOperationHistory.id.desc()).all()
    if history:
        for item in history:
            item.username = _user_name(item.uid)
            tmp = json.loads(item.content)
            item.content = "; ".join(tmp.values())
    return render_template("host/history.html", info=info, data=history)


@host.route("/get/<int:id>", methods=['GET', 'POST'])
@login_required
def host_info(id):
    info = Host.query.filter(Host.id == id).first()
    jsonval = {}
    if info:
        jsonval['id'] = info.id
        jsonval['is_virtual'] = info.is_virtual
        jsonval['type'] = info.type
        jsonval['hostname'] = info.hostname
        jsonval['primary_ip_id'] = info.primary_ip_id
        jsonval['primary_ip'] = _get_ip(info.primary_ip_id)
        jsonval['status'] = info.status
        jsonval['note'] = info.note

        if info.is_virtual == 0:
            device_info = _get_remote_ip_and_id(info.device_id)
            jsonval['device_id'] = device_info[0]
            jsonval['remote_ip'] = device_info[1]
        else:
            jsonval['entity_host_id'] = info.parent_id
            parent_info = Host.query.filter(Host.id == info.parent_id).first()
            jsonval['entity_host_name'] = ''
            if parent_info:
                jsonval['entity_host_name'] = parent_info.hostname
        host_ips = HostIp.query.filter(HostIp.host_id == info.id).all()
        if host_ips:
            net_ips = {}
            for host_ip in host_ips:
                ip = _get_ip(host_ip.ip_address_id)
                net_ips[host_ips.index(host_ip)] = {'net_name_id': host_ip.net_name_id, 'ip': ip,
                                                    'ip_address_id': host_ip.ip_address_id}
            jsonval['net_ip'] = net_ips

    return app.response_class(json.dumps(jsonval), mimetype='application/json')


@host.route("/hostip/autocomplete", methods=['POST', 'GET'])
def host_ip():
    q = request.form['q'] + '%'
    result = []
    ip_list = IpAddress.query.filter(IpAddress.flag == IpAddress.FLAG_AVAILABLE, IpAddress.ipv4.like(q)).limit(12).all()
    if ip_list:
        for item in ip_list:
            result.append([item.id, item.ipv4])
    return app.response_class(json.dumps(result), mimetype='application/json')


@host.route("/device/autocomplete", methods=['POST', 'GET'])
def device_info_autocomplete():
    q = '%' + request.form['q'] + '%'
    result = []
    ip_id_list = []

    device_list = Device.query.filter(Device.search.like(q)).all()

    for device in device_list:
        result.append([device.id, device.device_label])

    return app.response_class(json.dumps(result), mimetype='application/json')


@host.route("/entityname/autocomplete", methods=['POST', 'GET'])
def entity_host_name():
    q = request.form['q'] + '%'
    result = []
    hosts = Host.query.filter(Host.type == Host.TYPE_APC, Host.hostname.like(q)).all()
    if hosts:
        for item in hosts:
            result.append([item.id, item.hostname])
    return app.response_class(json.dumps(result), mimetype='application/json')


@host.route("/hostname/autocomplete", methods=['POST', 'GET'])
def host_name_match():
    q = request.form['q']
    result = get_host_name(q)
    return app.response_class(json.dumps(result), mimetype='application/json')


def get_host_name(q):
    result = []
    q = q + '%'
    select_hosts = []
    hosts = Host.query.filter(Host.hostname.like(str(q))).order_by(Host.hostname.desc()).limit(5).all()
    if hosts:
        for host in hosts:
            select_hosts.append(host.hostname)
        select_hosts = sorted(select_hosts)
    if select_hosts:
        name = select_hosts.pop().split("-")
        name_num = ("%03d" % (int(name[1]) + 1))
        next_name = name[0] + '-' + str(name_num)
        result.append([0, next_name])
    return result


@host.route("/allocate", methods=['POST', 'GET'])
def allocate():
    if request.method == 'GET':
        pool_id = request.args.get('pool_id', 0)
        apply_id = request.args.get('apply_id', 0)
        cpu = request.args.get('cpu', 0)
        mem = request.args.get('mem', 0)
        disk = request.args.get('disk', 0)
        idc = int(request.args.get('idc', 1))
        not_used_info = []
        data = ""
        all_not_used_info = Host.query.filter(
            and_(Host.status == Host.STATUS_READY, Host.is_virtual == 0, Host.cpu >= cpu, Host.memory >= mem,
                 Host.storage >= disk)).all()
        apply_info = Apply.query.filter(Apply.id == apply_id).first()
        user_name = User.query.filter(User.id == apply_info.uid).first().cn_name
        config_info = eval(apply_info.template)
        pool_info = Pool.query.filter(Pool.id == pool_id).first()
        content_len = len(apply_info.content)
        short_content = apply_info.content[:18]
        if pool_info:
            pool_name = pool_info.source_desc + str(pool_info.name)
        else:
            pool_name = "未知"
        content = {'name': user_name, 'num': apply_info.num, 'cpu': config_info['cpu'], 'mem': config_info['mem'],
                   'disk': config_info['disk'], 'pool_name': pool_name, 'desc': apply_info.content, 'len': content_len,
                   'short': short_content}
        for item in all_not_used_info:
            device_info = Device.query.filter(Device.id == item.device_id).first()
            rack_info = Rack.query.filter(Rack.id == device_info.rack_id).first()
            idcinfo = Datacenter.query.filter(Datacenter.id == rack_info.datacenter_id).first()
            if rack_info.datacenter_id == idc:
                idc_info = idcinfo.name + '/' + rack_info.name
                not_used_info.append({'hostname': item.hostname, 'id': item.id, 'cpu': item.cpu, 'mem': item.memory,
                                      'disk': item.storage,
                                      'idc': idc, 'idc_info': idc_info, 'rack_id': rack_info.id})
        if not_used_info:
            code = 1
            msg = "success"
            data = not_used_info
        else:
            code = 0
            msg = "没有可用的主机资源"

        # update by qiqi approve bug
        if (current_user.id == apply_info.approver_uid):
            config = eval(apply_info.template)
            approver_uid = app.config.get("APPROVER")['host']
            if (approver_uid == apply_info.approver_uid):
                return render_template("host/allocate.html", code=code, num=apply_info.num, msg=msg, data=data,
                                       content=content, pool_id=pool_id, apply_id=apply_id)
            else:
                apply_info = Apply.query.filter(Apply.id == apply_id).first()
                apply_info.approver_uid = approver_uid
                db.session.commit()
                if request.referrer:
                    return redirect(request.referrer)
                else:
                    return redirect(url_for('user.happroval'))
        else:

            return redirect(url_for('host.index'))

    elif request.method == 'POST':
        code = 0
        msg = "分配主机成功"
        host_ids = request.form['host_ids']
        pool_id = request.form['pool_id']
        apply_id = request.form['apply_id']
        intreg = re.compile('^[1-9]\d*$')
        host_ids = host_ids.split(",")
        if len(host_ids) <= 0:
            code = 1
            msg = "操作提示:分配主机失败,主机编号格式不对"
            return responsejson(code, msg)
        if not intreg.match(pool_id):
            code = 1
            msg = "操作提示:分配主机失败,pool编号格式不对"
            return responsejson(code, msg)
        pool_info = Pool.query.filter(Pool.id == pool_id).first()
        hostinfos = []
        apply_info = Apply.query.filter(Apply.id == apply_id).first()
        user_info = User.query.filter(User.id == apply_info.uid).first()
        config = eval(apply_info.template)
        approver_uid = app.config.get("APPROVER")['host']
        for host_id in host_ids:
            host_info = Host.query.filter(Host.id == host_id).first()
            ip_info = IpAddress.query.filter(IpAddress.id == host_info.primary_ip_id).first()
            if ip_info:
                ipv4 = ip_info.ipv4
            else:
                ipv4 = ""
            tmp_info = {'name': host_info.hostname, 'id': host_info.id, 'ip': ipv4, 'cpu': host_info.cpu,
                        'mem': host_info.memory, 'disk': host_info.storage}
            hostinfos.append(tmp_info)
            hasIn = PoolHost.query.filter(and_(PoolHost.pool_id == pool_id, PoolHost.host_id == host_id)).all()
            if hasIn:
                continue
            poolhosttarget = PoolHost(pool_id, host_id)
            db.session.add(poolhosttarget)
            host_info.status = Host.STATUS_ASSIGNED
            db.session.commit()
            target = Apply_host(apply_id=apply_info.id, host_id=host_info.id, status=Apply_host.ACTIVE)
            db.session.add(target)
            db.session.commit()
            logmsg = "主机编号:%s  name:%s　状态:可使用=>已分配  Pool:%s" % (host_id, host_info.hostname, pool_info.name)
            addlog(logmsg, 1)
            log_data = {}
            log_data['status'] = '状态 从 可使用 更改为 已分配(申请人: %s 申请id:%s cpu:%score mem: %sG storage: %sG pool: %s)' % (
            user_info.cn_name,
            apply_info.id, config['cpu'], config['mem'], config['disk'], pool_info.name)
            content = json.dumps(log_data, ensure_ascii=False, separators=(',', ':')).encode('utf8')
            _operation_log(host_id, approver_uid, content)
        apply_info.status = Apply.STATUS_SUCCESS
        db.session.commit()
        reciver = user_info.email
        subject = "[主机申请] 您申请的%s台主机开通成功" % apply_info.num
        needs = "申请配置: %s核/%sG/%sG<br>" % (config['cpu'], config['mem'], config['disk'])
        content = "您申请的%s台的主机开通成功<br>实际%s" % (str(apply_info.num), needs)
        type = HostBastionApply.TYPE_HOST
        for info in hostinfos:
            configure = "分配配置: %s核/%sG/%sG<br>" % (info['cpu'], info['mem'], info['disk'])
            content += "主机名:<a href='" + str(DOMAIN) + '/cmdb/host/%s' % info['id'] + "'>" + info['name'] + "</a>" + \
                       "  IP:<a href='" + str(DOMAIN) + "/cmdb/host/%s" % (info['id']) + "'>" + info['ip'] + \
                       "</a>  配置:%s <br>" % (configure)
            add_authority(apply_info.uid, type, info['id'], HostBastionApply.ROLE_ROOT, approver_uid,
                          HostBastionApply.STATUS_RUNNING, 30, "申请主机开通权限")
        addmail(reciver, subject, content)
        return responsejson(code, msg)


def __get_ip_info(ip):
    ip_info = IpAddress.query.filter(IpAddress.ipv4 == ip).first()
    if ip_info:
        return ip_info
    return False


def __add_net(id=0, net_name_id=0, ip_address_id=0, type=99, content=''):
    ret = True
    host_info = Host.query.filter(Host.id == id).first()
    if not host_info:
        ret = False
    else:
        host_ip_info = HostIp(id, net_name_id, ip_address_id, type=type, content=content)
        db.session.add(host_ip_info)
        db.session.commit()
        _set_used_ip(ip_address_id, IpAddress.FLAG_USED, IpAddress.TYPE_HOST, id)
    return ret


def __delete_net(id=0, net_name_id=0, ip_address_id=0, type=99):
    ret = True
    host_info = Host.query.filter(Host.id == id).first()
    if not host_info:
        ret = False
    else:
        host_ip_info = HostIp.query.filter(
            and_(HostIp.host_id == id, HostIp.net_name_id == net_name_id, HostIp.ip_address_id == ip_address_id,
                 HostIp.type == type)).first()
        if host_ip_info:
            db.session.delete(host_ip_info)
            db.session.commit()
            _set_used_ip(ip_address_id, IpAddress.FLAG_AVAILABLE, 0, 0)
        else:
            ret = False
    return ret


def device_id_find_host(device_id):
    host_info = Host.query.filter(Host.device_id == device_id).first()
    if host_info:
        return host_info


@host.route("/ratio", methods=["GET", "POST"])
def poolratios():
    host_ids = request.form['ids'] or ''
    ids_list = [0]
    if host_ids:
        tmp_ids_list = host_ids.split(",")
        for tmp_id in tmp_ids_list:
            tmp_id = int(tmp_id)
            if tmp_id > 0:
                ids_list.append(tmp_id)
    today = datetime.date.today()
    begin_time = str(today) + ' 00:00:00'
    begin_timestamps = time.mktime(time.strptime(begin_time, '%Y-%m-%d %H:%M:%S'))
    # 多减600就是10分钟,为了就是取两个10分钟弥补当前10分钟可能正在计算
    tmp_step = (time.time() - begin_timestamps - 600) / 600
    hour = '%02d' % int(tmp_step / 6)
    minitus = (int(tmp_step % 6)) * 10
    minitus = '%02d' % minitus
    begin_time = str(today) + ' %s:%s:00' % (hour, minitus)
    end_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    hosts_load = HostLoadRatio.query.filter(
        and_(HostLoadRatio.host_id.in_(ids_list), HostLoadRatio.created.between(begin_time, end_time))).order_by(
        HostLoadRatio.id.asc()).all()
    hosts_load_list = {}
    if hosts_load:
        for item_host_load in hosts_load:
            tmp_host_id = item_host_load.host_id
            tmp_dic_key = 'hostload_%d' % tmp_host_id
            hosts_load_list[tmp_dic_key] = [int(item_host_load.ratio * 100),
                                            item_host_load.created.strftime('%Y-%m-%d %H:%M')]

    code = 0
    msg = "成功"
    return responsejson(code, msg, [hosts_load_list])


@host.route("/ip/<params>", methods=['GET', 'POST'])
@login_required
def detail(params):
    if params:
        ip_info = IpAddress.query.filter(
            and_(IpAddress.ipv4 == str(params), IpAddress.type == IpAddress.TYPE_HOST)).first()
        if ip_info:
            host_id = ip_info.target_id
            return redirect(url_for('host.host_detail', id=host_id))
        else:
            return render_template("error.html", status=404, msg='Not Found')


def get_hostinfo(id):
    host_info = Host.query.filter(Host.id == id).first()
    if host_info:
        return host_info


def get_host_info(**kwargs):
    if 'id' in kwargs:
        return Host.query.filter(Host.id == kwargs['id']).first()
    elif 'ids' in kwargs:
        hosts_dic = {}
        hosts_info = Host.query.filter(Host.id.in_(kwargs['ids'])).all()
        if hosts_info:
            for item in hosts_info:
                hosts_dic[item.id] = item
        return hosts_dic
