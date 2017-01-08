# -*- coding: UTF-8 -*-
from flask import Blueprint, redirect, flash, request, render_template, url_for, jsonify, session, make_response
from flask_login import login_required, current_user
from application import db,app
from models.device_category import DeviceCategory
from models.device import Device
from models.remote_card import RemoteCard
from models.datacenter import Datacenter
from models.device_ip import DeviceIp
from models.ip_address import IpAddress
from models.rack import Rack
from models.supplier import Supplier
from models.host import Host
from models.device_operation_history import DeviceOperationHistory
from views.host import _user_name
from sqlalchemy import and_
from datetime import datetime, timedelta
from pypages import Paginator
from .log import addlog
from tasks import host_device_changed
from views.functions import visible
import json
import xlwt
import StringIO
from werkzeug.utils import secure_filename
from application import fujs
import os
import xlrd

device = Blueprint('device', __name__)

UPLOAD_FOLDER = 'static/upload'

@app.context_processor
def inject_fujs():
    return dict(fujs=fujs)

# device category part
@device.route('/category/')
@login_required
def category_list():
    show = visible()
    cates = DeviceCategory.query.filter(DeviceCategory.deleted == 0).order_by('id').all()
    return render_template('device/category/list.html', cates=cates,show=show)


@device.route('/category/add', methods=['POST', 'GET'])
@login_required
def category_add():
    if request.method != 'POST':
        flash('method not allowed')
        return redirect(url_for('device.category_list'))

    name = request.form['name']
    short = request.form['short_name']
    note = request.form['note']
    if not name:
        flash('Name is required')
        return redirect(url_for('device.category_list'))

    if not short:
        flash('Short name is required')
        return redirect(url_for('device.category_list'))

    cate = DeviceCategory.query.filter(DeviceCategory.deleted == 0, DeviceCategory.name == name).first()
    if cate is not None:
        flash('Category "%s" is already been used' % (cate.name))
        return redirect(url_for('device.category_list'))

    now = datetime.now()
    cate = DeviceCategory(name, short, note, now)
    db.session.add(cate)
    db.session.commit()
    flash('添加成功', 1)
    addlog('添加了设备类别: id:%d, name=%s' % (cate.id, cate.name))
    return redirect(url_for('device.category_list'))


@device.route('/category/modify/<int:id>', methods=['POST', 'GET'])
@login_required
def category_modify(id):
    if id <= 0:
        flash('Id must bigger than zero')
        return redirect(url_for('device.category_list'))

    cate = DeviceCategory.query.filter(DeviceCategory.deleted == 0, DeviceCategory.id == id).first()
    if cate is None:
        flash('category not found')
        return redirect(url_for('device.category_list'))

    if request.method == 'POST':
        name = request.form['name']
        short = request.form['short_name']
        note = request.form['note']
        if not name:
            flash('Name is required')
            return redirect(url_for('device.category_list'))
        if not short:
            flash('Short name is required')
            return redirect(url_for('device.category_list'))

        if cate.name != name:
            same_cate = DeviceCategory.query.filter(DeviceCategory.deleted == 0, DeviceCategory.name == name).first()
            if same_cate is not None:
                flash('Category "%s" is already been used' % (same_cate.name))
                return redirect(url_for('device.category_list'))

        log = []
        if cate.name != name:
            log.append('name:%s 更改为 %s' % (cate.name, name))
            cate.name = name

        if cate.note != note:
            log.append('note:%s 更改为 %s' % (cate.note, note))
            cate.note = note

        if cate.short_name != short:
            log.append('short_name:%s 更改为 %s' % (cate.short_name, short))
            cate.short_name = short

        if len(log) > 0:
            cate.updated = datetime.now()
            db.session.commit()
            flash('修改成功', 1)
            addlog('修改设备类别id=%d: %s' % (cate.id, ','.join(log)))

        return redirect(url_for('device.category_list'))

    return render_template('device/category/_modify_form.html', cate=cate)


@device.route('/category/delete/<int:id>', methods=['POST', 'GET'])
@login_required
def category_delete(id):
    if id <= 0:
        flash('Id must bigger than zero')
        return redirect(url_for('device.category_list'))
    if request.method != 'POST':
        flash('Method not allowed')
        return redirect(url_for('device.category_list'))

    cate = DeviceCategory.query.filter(DeviceCategory.deleted == 0, DeviceCategory.id == id).first()
    if cate is not None:
        num = Device.query.filter(Device.deleted == 0, Device.device_cat_id == id).count()
        if num > 0:
            flash('This category is still in use')
            return redirect(url_for('device.category_list'))

        cate.deleted = 1
        cate.updated = datetime.now()
        db.session.commit()
        flash('删除成功', 1)
        addlog('删除设备类别, id=%d, name=%s' % (cate.id, cate.name))

    return redirect(url_for('device.category_list'))


# device part
@device.route('/')
@login_required
def list():
    show = visible({'export':"/cmdb/device/export_get"})
    cates = DeviceCategory.query.filter(DeviceCategory.deleted == 0).all()
    cate_names = {}
    for cate in cates:
        cate_names[cate.id] = cate.name

    suppliers = Supplier.query.all()
    supp_names = {}
    for supp in suppliers:
        supp_names[supp.id] = supp.short_name

    idcs = Datacenter.query.filter(Datacenter.deleted == 0).all()
    idc_names = {}
    for idc in idcs:
        idc_names[idc.id] = idc.name

    racks = Rack.query.filter(Rack.deleted == 0).all()
    rack_names = {}
    rack_idc_names = {}
    idc_to_rack = {}
    for rack in racks:
        datacenter_id = rack.datacenter_id
        rack_names[rack.id] = rack.name
        rack_idc_names[rack.id] = idc_names[rack.datacenter_id]
        if datacenter_id not in idc_to_rack.keys():
            idc_to_rack[datacenter_id] = []
        idc_to_rack[datacenter_id].append({"id": rack.id,"name": rack.name})
    page = int(request.args.get('page',1))
    cate = int(request.args.get('cate',0))
    date = request.args.get('date','')
    idc  = int(request.args.get('idc',0))
    rack = int(request.args.get('rack',0))
    kw   = request.args.get('kw','').strip()
    status = request.args.get('status',0)
    cond = {1:cate,
            2:date,
            3:idc,
            4:rack,
            5:date,
            6:kw,
            7:status}
    page_size = 50
    url = ''
    condition = Device.query.filter(Device.deleted == 0)
    url = "cate=%d" % cate
    url = "%s&idc=%d&rack=%d" % (url,idc,rack)
    if cate != 0:
        condition = condition.filter(Device.device_cat_id == cate)
    if rack != 0:
        condition = condition.filter(Device.rack_id == rack)
    else:
        if idc != 0:
            rack_id = []
            for item in idc_to_rack[idc]:
                rack_id.append(item['id'])
            condition = condition.filter(Device.rack_id.in_(rack_id))
    if date:
        condition = condition.filter(Device.buy_time >= date)
        url = "%s&date=%s" % (url,date)
    if status:
        condition = condition.filter(Device.status == status)
        url = "%s&status=%s" % (url,status)
    if kw:
        url = "%s&kw=%s" % (url,kw)
        kw = '%'+kw+'%'
        condition = condition.filter(Device.search.like(kw))
    total_num = condition.count()
    if total_num > page_size:
        pager = Paginator(total_num, per_page=page_size, current=page, range_num=5)
    else:
        pager = False
    devs = condition.order_by(Device.id.desc()).offset((page - 1) * page_size).limit(page_size).all()
    extendinfo = {
        'total':total_num,
        'cur_total':len(devs)
    }
    status_info = Device.query.filter(Device.deleted == Device.DELETED_NO).all()
    status_ids = []
    status_name = {}
    if status_info:
        for item in status_info:
            if item.status not in status_ids:
                status_ids.append(item.status)
                status_name[item.status] = item.status_descri
    return render_template('device/list.html', devs=devs, cate_names=cate_names, supp_names=supp_names,
                           idc_names=idc_names, rack_names=rack_names, rack_idc_names=rack_idc_names,status_name=status_name,
                           pager=pager,cond=cond,url=url,idc_to_rack=json.dumps(idc_to_rack),show=show,extendinfo=extendinfo)

@device.route('/ajax_add', methods=['POST', 'GET'])
@login_required
def ajax_add():
    dev = Device()
    errors, net_list = load_form(dev)
    if len(errors) > 0:
        return jsonify({'errors': errors, 'code': 403})

    session.pop('_flashes', None)
    return jsonify({'id': dev.id, 'label': dev.device_label})


@device.route('/add', methods=['POST', 'GET'])
@login_required
def add():
    dev = Device()
    return update(dev, 'add')


@device.route('/modify/<int:id>', methods=['POST', 'GET'])
@login_required
def modify(id):
    dev = Device.query.filter(Device.deleted == 0, Device.id == id).first()
    if dev is None:
        return redirect(url_for('device.detail',id = dev.id))
    return update(dev, 'modify')

def update(dev, act):
    cates = DeviceCategory.query.filter(DeviceCategory.deleted == 0).all()
    suppliers = Supplier.query.all()
    idcs = Datacenter.query.filter(Datacenter.deleted == 0).all()
    idc_id = idcs[0].id
    racks = Rack.query.filter(Rack.deleted == 0).all()
    idc_racks = {}
    idc_ids = []
    for rack in racks:
        if rack.datacenter_id not in idc_racks.keys():
            idc_ids.append(rack.datacenter_id)
            idc_racks[rack.datacenter_id] = []

        if dev.rack_id == rack.id:
            idc_id = rack.datacenter_id

        idc_racks[rack.datacenter_id].append(rack)

    nets = DeviceIp.query.filter(DeviceIp.device_id == dev.id).all()
    net_list = {}
    for net in nets:
        ip = IpAddress.query.get(net.ip_address_id)
        if ip:
            net_list[ip.id] = {'ip_id': ip.id, 'net_name_id': int(net.net_name_id), 'ip': ip.ipv4, 'mac': net.mac}


    frame_cat = DeviceCategory.query.filter(and_(DeviceCategory.name == "机框",DeviceCategory.deleted == 0)).first()
    frames = Device.query.filter(Device.device_cat_id == frame_cat.id).all()
    frame_labels = []
    for frame in frames:
        frame_label = {}
        frame_label['id'] = frame.id
        frame_label['device_label'] = frame.device_label
        frame_labels.append(frame_label)

    errors = []
    if request.method == 'POST':
        idc_id = int(request.form['idc'])
        errors, net_list = load_form(dev)

        if len(errors) == 0:
            return redirect(url_for('device.detail',id = dev.id))

    return render_template(('device/%s.html' % (act)), dev=dev, frame_labels=frame_labels, cates=cates, net_names=Device.net_names(),
                           idcs=idcs, idc_racks=idc_racks, idc_id=idc_id, idc_ids=idc_ids,
                           suppliers=suppliers, nets=net_list, act=act, errors=errors)

@device.route("/import_remote_card",methods=['POST','GET'])
@login_required
def import_remote_card():
    try:
        f = request.files['fileToUpload']
        f.save(os.path.join(UPLOAD_FOLDER, 'remote_card.xlsx'))
        host_xlsx = os.path.join(UPLOAD_FOLDER, 'remote_card.xlsx')
        if os.path.isfile(host_xlsx):
            data = xlrd.open_workbook(host_xlsx)
            os.remove(host_xlsx)
            table = data.sheets()[0]
            nrows = table.nrows
            for i in range(nrows):
                if i == 0:
                    continue
                row = table.row_values(i)
                ip = IpAddress.query.filter(IpAddress.ipv4 == row[0]).first()
                if not ip:
                    print "Can't find the IP :%s"%row[0]
                    continue
                remotecard = RemoteCard.query.filter(RemoteCard.ip_id == ip.id).first()
                if remotecard:
                    # print "This IP is exits :%s"%row[0]
                    remotecard.user = row[1]
                    remotecard.password = row[2]
                    db.session.commit()
                    continue
                remotecard_target = RemoteCard(ip.id,row[1],row[2])
                db.session.add(remotecard_target)
                db.session.commit()
            return app.response_class(json.dumps({'code': 1, 'msg': ''}), mimetype='application/json')
        return app.response_class(json.dumps({'code': 0, 'msg': '文件上传失败！'}), mimetype='application/json')
    except Exception, e:
        print e
        if os.path.isfile(host_xlsx):
            os.remove(host_xlsx)
        return app.response_class(json.dumps({'code': 0, 'msg': '文件格式和内容不正确！'}),mimetype='application/json')



@device.route("/import_device", methods=['POST', 'GET'])
@login_required
def import_device():
    try:
        f = request.files['fileToUpload']
        f.save(os.path.join(UPLOAD_FOLDER, 'device.xlsx'))
        host_xlsx = os.path.join(UPLOAD_FOLDER, 'device.xlsx')
        # if os.path.isfile(host_xlsx):
        #     os.remove(host_xlsx)
        data = xlrd.open_workbook(host_xlsx)
        table = data.sheets()[0]
        nrows = table.nrows
        message_date = []
        for i in range(nrows):
            if i == 0:
                continue
            row = table.row_values(i)
            print row
            dev = Device()
            cat = row[0]
            if cat:
                cate=DeviceCategory.query.filter(DeviceCategory.name == cat).first()
                if cate:
                    dev.device_cat_id = cate.id
                else:
                    message_date.append('设备类型'+row[0] + 'don not exist! ' + ";;;row:" + str(i))
                    continue
            else:
                message_date.append('设备类型'+ 'is null! ' + ";;;row:" + str(i))
                continue

            supplier=row[1]
            if supplier:
                supplier_s=Supplier.query.filter(Supplier.name==supplier).first()
                if supplier_s:
                    dev.supplier_id = supplier_s.id
                else:
                    message_date.append('供应商'+row[0] + 'don not exist! ' + ";;;row:" + str(i))
                    continue
            else:
               message_date.append('供应商'+ 'is null! ' + ";;;row:" + str(i))
               continue

            sn=row[2]
            if sn:
                dev.sn=sn
            else:
               message_date.append('序列号'+ 'is null! ' + ";;;row:" + str(i))
               continue

            model=row[3]
            if model:
                dev.model=model
            else:
               message_date.append('设备型号'+ 'is null! ' + ";;;row:" + str(i))
               continue

            buy_time=row[4]
            if buy_time:
                try:
                    dev.buy_time = dev.buy_time.strptime(buy_time, "%m/%d/%Y")
                except:
                    message_date.append('购买时间'+ '格式错误! ' + ";;;row:" + str(i))
                    continue
            else:
               message_date.append('购买时间'+ 'is null! ' + ";;;row:" + str(i))
               continue

            term = int(row[5]) if row[5] else 0
            if term>0:

                dev.elapsed_time = dev.buy_time + timedelta(days=term * 365)
            else:
               message_date.append('保修期'+ 'is null! ' + ";;;row:" + str(i))
               continue

            price = float(row[6]) if row[6] else 0
            if price > 0:
                v = round(price * 100)
                v1 = str(dev.price_rmb())
                dev.price = v

            else:
                dev.price = 0

            rack=row[7]
            if rack:
                rack_s=Rack.query.filter(Rack.name==rack).first()
                if rack_s:
                    dev.rack_id = rack_s.id
                else:
                    message_date.append('机柜'+row[0] + 'don not exist! ' + ";;;row:" + str(i))
                    continue
            else:
                message_date.append('机柜'+ 'is null! ' + ";;;row:" + str(i))
                continue

            rack_offset=int(row[8])
            if rack_offset:
                dev.rack_offset=rack_offset

            rack_unit=int(row[9])
            if rack_unit:
                dev.rack_unit=rack_unit

            memory=row[10]
            if memory:
                extra = []
                extra.append(str(memory))
                dev.memory = float(memory)
                dev.memory_extra = ' '.join(extra)
            else:
                message_date.append('内存'+ 'is null! ' + ";;;row:" + str(i))
                continue

            cpu=row[11]
            if cpu:
                try:
                    cpu_nums = []
                    cpu_models = []
                    cpus=cpu.split(',')
                    for c in cpus:
                        cpu_nums.append('' if c.split('#')[0]=='null' else c.split('#')[0])
                        cpu_models.append('' if c.split('#')[1]=='null' else c.split('#')[1])
                        num = 0
                    extra = []
                    if len(cpu_nums) > 0:
                        index = 0
                        while index < len(cpu_nums):
                            n = 0
                            if cpu_nums[index]:
                                n = int(cpu_nums[index])
                            if n > 0:
                                extra.append({'num': n, 'model': cpu_models[index]})
                                num += n
                            index += 1

                    if num > 0:
                        dev.cpu = num
                        dev.cpu_extra = json.dumps(extra)
                    else:
                        message_date.append('CPU信息填写错误'+ ";;;row:" + str(i))
                        continue

                except:
                   message_date.append('CPU'+ '格式错误! ' + ";;;row:" + str(i))
                   continue
            else:
                message_date.append('CPU'+ 'is null! ' + ";;;row:" + str(i))
                continue

            disk_s=row[12]
            if disk_s:
                try:
                    disks=disk_s.split(',')
                    disk_cap = []
                    disk_speed = []
                    disk_inter = []
                    disk_size = []
                    disk_count = []
                    disk_type=[]

                    for d in disks:
                        disk_cap.append('' if d.split('#')[0]=='null' else d.split('#')[0])
                        disk_speed.append(0)
                        disk_inter.append('' if d.split('#')[2]=='null' else d.split('#')[2])
                        disk_size.append('' if d.split('#')[3]=='null' else d.split('#')[3])
                        disk_count.append('' if d.split('#')[4]=='null' else d.split('#')[4])
                        disk_type.append('' if d.split('#')[1]=='null' else d.split('#')[1])

                    disk = []
                    num = 0
                    if len(disk_cap) > 0:
                        index = 0
                        while index < len(disk_cap):
                            cap = 0
                            if disk_cap[index]:
                                cap = int(disk_cap[index])
                            if cap > 0:
                                if disk_speed[index]:
                                    speed = int(disk_speed[index])
                                else:
                                    speed = 0
                                if disk_type[index]:
                                    type_s = int(disk_type[index])
                                else:
                                    speed = 100
                                inter = disk_inter[index]
                                if disk_size[index]:
                                    size = float(disk_size[index])
                                else:
                                    size = 0
                                if disk_count[index]:
                                    count = int(disk_count[index])
                                else:
                                    count = 1

                                num += cap * count
                                disk.append({
                                    'capacity': cap,
                                    'speed': speed,
                                    'interface': inter,
                                    'size': size,
                                    'count': count,
                                    'type':type_s
                                })
                            index += 1
                    if num > 0:
                        dev.storage = num
                        dev.storage_extra = json.dumps(disk)
                    else:
                        message_date.append('disk'+ '格式错误! ' + ";;;row:" + str(i))
                        continue
                except:
                    message_date.append('disk'+ '格式错误! ' + ";;;row:" + str(i))
                    continue
            else:
                message_date.append('disk'+ 'is null! ' + ";;;row:" + str(i))
                continue


            ip_net=row[13]
            if ip_net:
                try:
                    ips=ip_net.split(',')
                    net_ip_ids = []
                    net_names = []
                    net_ips = []
                    net_macs = []
                    net_list = {}

                    isIpture=True
                    for i_index in ips:
                        ip_add=i_index.split('#')[0]
                        ip_ns = IpAddress.query.filter(IpAddress.ipv4 == ip_add).first()
                        if not ip_ns:
                            print  'don not have net ip: ' + ip_add + ";;;row:" + str(i)
                            message_date.append( 'don not have net ip: ' + ip_add + ";;;row:" + str(i))
                            isIpture=False
                            break
                        if ip_ns.flag == 1:
                            print 'net ip: ' + ip_add + 'Occupyed' + ";;;row:" + str(i)
                            message_date.append('net ip: ' + ip_add + 'Occupyed' + ";;;row:" + str(i))
                            isIpture=False
                            break
                        net_ips.append(ip_add)
                        net_ip_ids.append(ip_ns.id)
                        net_names.append('0')
                        net_macs.append('' if i_index.split('#')[1]=='null' else i_index.split('#')[1])

                    if not isIpture:
                        continue

                    if len(net_ip_ids) > 0:
                        index = 0
                        while index < len(net_ip_ids):
                            ip_id = int(net_ip_ids[index] or 0)
                            if ip_id == 0:
                                index += 1
                                continue

                            ip = net_ips[index]
                            name_id = -1
                            if net_names[index]:
                                name_id = int(net_names[index])

                            if name_id > len(Device.net_names()):
                                index += 1
                                continue

                            mac = net_macs[index]
                            index += 1
                            net_list[ip_id] = {'ip_id': ip_id, 'net_name_id': name_id, 'ip': ip, 'mac': mac}

                except:
                   message_date.append('ip'+ '格式错误! ' + ";;;row:" + str(i))
                   continue
            else:
               message_date.append('ip'+ 'is null! ' + ";;;row:" + str(i))
               continue


            dev.updated = datetime.now()
            dev.content = row[14]
            dev.created = datetime.now()
            db.session.add(dev)
            db.session.commit()
            rack = Rack.query.filter(Rack.id == dev.rack_id).limit(1).first()

            idc_i=row[15]

            idc = Datacenter.query.filter(Datacenter.name == idc_i).first()
            if (not idc):
                message_date.append('ip'+ '机房找不到! ' + ";;;row:" + str(i))
                continue
            cate = DeviceCategory.query.filter(DeviceCategory.id == dev.device_cat_id).limit(1).first()
            if not dev.device_label:
                dev.device_label = idc.idc_label + '-' + cate.short_name + '-' + str(dev.id + 1000)


            if dev.update_nets(net_list):
                print ''

            db.session.commit()
        return app.response_class(json.dumps({'code': 1, 'msg': '', 'data': message_date}), mimetype='application/json')

    except Exception, e:
        print e
        return app.response_class(json.dumps({'code': 0, 'msg': '文件格式和内容不正确！', 'data': ''}),
                                  mimetype='application/json')


def load_form(dev):
    errors = []
    log = []
    log_data = {}
    is_add = False if dev.id > 0 else True
    value = request.form['device-cate']
    if value:
        if dev.device_cat_id != int(value) and not is_add:
            cates = DeviceCategory.query.filter(DeviceCategory.deleted == 0).all()
            cate_names = {}
            for cate in cates:
                cate_names[cate.id] = cate.name
                if cate.name == "机框":
                    frame = cate
            if dev.device_cat_id == frame.id:
                devices = Device.query.filter(and_(Device.deleted ==0,Device.frame_id == dev.id)).all()
                for device_info in devices:
                    device_info.frame_id = 0
                    db.session.commit()
                log_data['device_cat_id'] = '设备分类 从' + cate_names[dev.device_cat_id] + '更改为' + cate_names[int(value)]+ ",已清除原机框下所有设备记录。"
            else:
                log_data['device_cat_id'] = '设备分类 从' + cate_names[dev.device_cat_id] + '更改为' + cate_names[int(value)]
        dev.device_cat_id = int(value)
    else:
        errors.append("没有选择设备类型")

    value = request.form['supplier']
    if value:
        if dev.supplier_id != int(value) and not is_add:
            suppliers = Supplier.query.all()
            supp_names = {}
            for supp in suppliers:
                supp_names[supp.id] = supp.short_name
            log_data['supplier_id'] = '设备供应商 从' + supp_names[dev.supplier_id] + '更改为' + supp_names[int(value)]
        dev.supplier_id = int(value)
    else:
        errors.append("没有选择供应商")

    value = request.form['sn']
    if value:
        if dev.sn != value and not is_add:
            log_data['sn'] = '设备序列号 从' + str(dev.sn) + '更改为' + str(value)
        dev.sn = value
    else:
        # errors.append("没有填写序列号")
        dev.sn = ""

    value = request.form['model']
    if value:
        if dev.model != value and not is_add:
            log_data['model'] = '设备型号 从' + str(dev.model) + '更改为' + str(value)
        dev.model = value
    else:
        errors.append("没有填写设备型号")

    value = request.form['buy-time']
    if value:
        v = dev.buy_time.strftime('%m/%d/%Y')
        if v != value:
            dev.buy_time = dev.buy_time.strptime(value, "%m/%d/%Y")
            if not is_add:
                log_data['buy_time'] = '购买时间 从' + str(v) + '更改为' + str(value)
    else:
        errors.append("没有填写购买时间")

    value = int(request.form['service-term']) if request.form['service-term'] else 0
    if value > 0:
        if dev.elapsed_time:
            v = dev.elapsed_time.strftime('%m/%d/%Y')
        else:
            v = ''

        if dev.service_term() != value:
            dev.elapsed_time = dev.buy_time + timedelta(days=value * 365)
            if not is_add:
                log_data['elapsed_time'] = '过保时间 从' + str() + '更改为' + str(dev.elapsed_time.strftime('%m/%d/%Y'))
    else:
        errors.append("没有填写保修期")

    value = float(request.form['price']) if request.form['price'] else 0
    if value > 0:
        v = round(value * 100)
        v1 = str(dev.price_rmb())
        if dev.price != v:
            dev.price = v
            if not is_add:
                log_data['price'] = '价格 从' + str(v1) + '更改为' + str(dev.price_rmb())
    else:
        dev.price = 0
        #errors.append("没有填写价格")

    value = int(request.form['rack']) if request.form['rack'] else 0
    if value > 0:
        if dev.rack_id != value and not is_add:
            racks = Rack.query.all()
            rack_names = {}
            for rack in racks:
                rack_names[rack.id] = rack.name
            if dev.rack_id == 0:
                log_data['rack_id'] = '机柜 从 未知 更改为' + rack_names[int(value)]
            else:
                log_data['rack_id'] = '机柜 从' + rack_names[dev.rack_id] + '更改为' + rack_names[int(value)]
        dev.rack_id = value
    else:
        errors.append("没有选择机柜")

    value = int(request.form['rack-offset']) if request.form['rack-offset'] else 0
    if dev.rack_offset != value:
        if not is_add:
            log_data['rack_offset'] = '机柜内位置 从' + str(dev.rack_offset) + '更改为' + str(value)
        dev.rack_offset = value

    value = int(request.form['rack-unit']) if request.form['rack-unit'] else 0
    if dev.rack_unit != value:
        if not is_add:
            log_data['rack_unit'] = '机柜高度 从' + str(dev.rack_unit) + '更改为' + str(value)
        dev.rack_unit = value

    value = int(request.form['frame-droplist'])
    if dev.frame_id != value:
        if not is_add:
            log_data['frame_unit'] = '机框 从' + str(dev.frame_id) + '更改为' + str(value)
        dev.frame_id = value

    value = request.form['memory']
    if value:
        sizes = value.split()
        total = 0
        extra = []
        for size in sizes:
            s = float(size)
            total += s
            extra.append(str(s))

        if dev.memory != total and not is_add:
            log_data['memory'] = '内存 从' + str(dev.memory) + '更改为' + str(total)
        dev.memory = total
        dev.memory_extra = ' '.join(extra)

    if dev.memory <= 0:
        errors.append('内存不能为零')

    cpu_nums = request.form.getlist('cpu-num[]')
    cpu_models = request.form.getlist('cpu-model[]')
    num = 0
    extra = []
    if len(cpu_nums) > 0:
        i = 0
        while i < len(cpu_nums):
            n = 0
            if cpu_nums[i]:
                n = int(cpu_nums[i])
            if n > 0:
                extra.append({'num': n, 'model': cpu_models[i]})
                num += n
            i += 1

    if num > 0:
        if dev.cpu != num and not is_add:
            log_data['cpu'] = 'cpu 从' + str(dev.cpu) + '更改为' + str(num)
        dev.cpu = num
        dev.cpu_extra = json.dumps(extra)
    else:
        errors.append('CPU信息填写错误')

    disk_cap = request.form.getlist('disk-capacity[]')
    disk_speed = request.form.getlist('disk-speed[]')
    disk_inter = request.form.getlist('disk-inter[]')
    disk_size = request.form.getlist('disk-size[]')
    disk_count = request.form.getlist('disk-count[]')
    disk_type=request.form.getlist('disk-type[]')
    disk = []
    num = 0
    if len(disk_cap) > 0:
        i = 0
        while i < len(disk_cap):
            cap = 0
            if disk_cap[i]:
                cap = int(disk_cap[i])
            if cap > 0:
                if disk_speed[i]:
                    speed = int(disk_speed[i])
                else:
                    speed = 0
                inter = disk_inter[i]
                if disk_size[i]:
                    size = float(disk_size[i])
                else:
                    size = 0
                if disk_count[i]:
                    count = int(disk_count[i])
                else:
                    count = 1
                if disk_type[i]:
                    type_add=int(disk_type[i])
                else:
                    type_add=100

                num += cap * count
                disk.append({
                    'capacity': cap,
                    'speed': speed,
                    'interface': inter,
                    'size': size,
                    'count': count,
                    'type':type_add
                })
            i += 1
    if num > 0:
        if dev.storage != num:
            log_data['storage'] = '硬盘 从' + str(dev.storage) + '更改为' + str(num)
        dev.storage = num
        dev.storage_extra = json.dumps(disk)

    dev.updated = datetime.now()
    dev.content = request.form['content']
    if dev.id <= 0 and len(errors) == 0:
        dev.created = datetime.now()
        db.session.add(dev)
        db.session.commit()
        flash('添加成功', 1)
        log = json.dumps({'create': '添加一台设备'}, ensure_ascii=False, separators=(',', ':')).encode('utf8')
        _operation_log(dev.id, current_user.id, log)

    net_ip_ids = request.form.getlist('net-ip-id[]')
    net_names = request.form.getlist('net-name[]')
    net_ips = request.form.getlist('net-ip[]')
    net_macs = request.form.getlist('net-mac[]')
    net_list = {}
    if len(net_ip_ids) > 0:
        i = 0
        while i < len(net_ip_ids):
            ip_id = int(net_ip_ids[i] or 0)
            if ip_id == 0:
                i += 1
                continue

            ip = net_ips[i]
            name_id = -1
            if net_names[i]:
                name_id = int(net_names[i])

            if name_id > len(Device.net_names()):
                i += 1
                continue

            mac = net_macs[i]
            i += 1
            net_list[ip_id] = {'ip_id': ip_id, 'net_name_id': name_id, 'ip': ip, 'mac': mac}

    if len(errors) == 0:
        rack = Rack.query.filter(Rack.id == dev.rack_id).limit(1).first()
        idc = Datacenter.query.filter(Datacenter.id == rack.datacenter_id).limit(1).first()
        cate = DeviceCategory.query.filter(DeviceCategory.id == dev.device_cat_id).limit(1).first()
        if not dev.device_label:
            dev.device_label = idc.idc_label + '-' + cate.short_name + '-' + str(dev.id + 1000)
            host_device_changed.delay(dev.id, 2, 1)

        if dev.update_nets(net_list):
            log_data['net'] = '网卡信息有变更'

        db.session.commit()
        if not is_add and len(log_data) > 0:
            dev.created = datetime.now()
            dev.updated = datetime.now()
            host_device_changed.delay(dev.id, 2, 2)
            flash('修改成功', 1)
            if log_data:
                log = json.dumps(log_data, ensure_ascii=False, separators=(',', ':')).encode('utf8')
                _operation_log(dev.id, current_user.id, log)
    return errors, net_list

@device.route('/autocomplete', methods=['POST', 'GET'])
@login_required
def autocomplete():
    jsonval = []
    q = '%' + request.form['q'] + '%'
    device_info = Device.query.filter(and_(Device.deleted == 0,Device.model.like(q))).group_by(Device.model).limit(10).all()
    if device_info:
        for item in device_info:
            jsonval.append(item.model)
    return app.response_class(json.dumps(jsonval), mimetype='application/json')

@device.route('/<int:id>', methods=['POST', 'GET'])
@login_required
def detail(id):
    dev = Device.query.filter(Device.deleted == 0, Device.id == id).first()
    if dev is None:
        return redirect(url_for('device.category_list'))
    return detail_list(dev)

def detail_list(dev):
    show = visible({'host_add':"/cmdb/host/add_post"})
    cate = DeviceCategory.query.filter(DeviceCategory.deleted == 0, DeviceCategory.id == dev.device_cat_id).first()
    supplier = Supplier.query.filter(Supplier.id == dev.supplier_id).first()
    if dev.rack_id:
        rack = Rack.query.filter(Rack.deleted == 0, Rack.id == dev.rack_id).first()
        idc = Datacenter.query.filter(Datacenter.id == rack.datacenter_id).first()
    else:
        rack = 0
        idc = 0
    hosts_info = []
    device_infos = []
    if cate.name == "服务器":
        hosts = Host.query.filter(and_(Host.device_id == dev.id,Host.deleted == Host.DELETED_NO)).all()
        if hosts:
            for host in hosts:
                ip = IpAddress.query.filter(IpAddress.id == host.primary_ip_id).first()
                if ip:
                    ip_add = ip.ipv4
                else:
                    ip_add = "未知"
                if host.deleted !=1:
                    status = host.status_descri
                else:
                    status = "已删除"
                hosts_list = {'id': host.id, 'name': host.hostname,'ip': ip_add,'vir':host.virtual_descri,
                          'type':host.type_descri,'status':status,'cpu':host.cpu_descri,'mem':host.memory_descri,'sto':host.storage_descri}
                hosts_info.append(hosts_list)
                vm_hosts = Host.query.filter(and_(Host.parent_id == host.id,Host.deleted == Host.DELETED_NO)).all()
                if vm_hosts:
                    for vm_host in vm_hosts:
                        ip = IpAddress.query.filter(IpAddress.id == vm_host.primary_ip_id).first()
                        if ip:
                            ip_add = ip.ipv4
                        else:
                            ip_add = "未知"
                        if vm_host.deleted !=1:
                            status = vm_host.status_descri
                        else:
                            status = "已删除"
                        hosts_list = {'id': vm_host.id,'name': vm_host.hostname,'ip': ip_add,'vir':vm_host.virtual_descri,
                                    'type':vm_host.type_descri,'status':status,'cpu':vm_host.cpu_descri,'mem':vm_host.memory_descri,'sto':vm_host.storage_descri}
                        hosts_info.append(hosts_list)
    elif cate.name == "机框":
        devices = Device.query.filter(and_(Device.deleted == 0,Device.frame_id == dev.id)).all()
        for device in devices:
            device_info = {}
            device_info['id'] = device.id
            device_info['device_label'] = device.device_label
            dev_cate = DeviceCategory.query.filter(DeviceCategory.id == Device.id).first()
            device_info['cat_name'] = dev_cate.name
            rack= Rack.query.filter(Rack.deleted == 0, Rack.id == dev.rack_id).first()
            idc= Datacenter.query.filter(Datacenter.id == rack.datacenter_id).first()
            device_info['rack'] = idc.idc_label + "/" + rack.name
            supplier = Supplier.query.filter(Supplier.id == device.supplier_id).first()
            device_info['supplier'] = supplier.short_name
            device_info['model'] = device.model
            device_info['cpu'] = device.cpu
            device_info['memory'] = str(device.memory)+"G"
            device_info['storage'] = str(device.storage/1000)+"T"
            device_infos.append(device_info)

    nets = DeviceIp.query.filter(DeviceIp.device_id == dev.id).all()
    net_info = []
    for net in nets:
        ip = IpAddress.query.get(net.ip_address_id)
        if ip:
            if net.net_name_id == 0:
                remotecard = RemoteCard.query.filter(RemoteCard.ip_id == net.ip_address_id).first()
                username = password = ""
                if remotecard:
                    username = remotecard.user.strip()
                    password = remotecard.password.strip()
                list = {'net_name': "远控卡", 'ip': ip.ipv4, 'mac': net.mac, 'user': username, 'pass': password}
            else:
                list = {'net_name': "IP", 'ip': ip.ipv4, 'mac': net.mac}
            net_info.append(list)
    nets_ip = list_3array(net_info)
    cpu_info = {}
    for cpu in dev.cpu_list():
        if cpu['num'] == 0:
            cpu_num = "未知"
        else:
            cpu_num = cpu['num']
        if cpu['model']:
            cpu_model = cpu['model']
        else:
            cpu_model = "未知"
        cpu_info = {"cpu_num": cpu_num,"cpu_model": cpu_model}
    disks = []
    disk_info ={}
    for disk in dev.storage_list():
        if disk['capacity']:
            disk_cap = disk['capacity']
        else:
            disk_cap = "未知"
        if disk['speed']:
            disk_speed = disk['speed']
        else:
            disk_speed = "未知"
        if disk['interface']:
            disk_inter = disk['interface']
        else:
            disk_inter = "未知"
        disk_counter = 1
        if 'count' in disk:
            disk_counter = disk['count']
        if 'type' in disk:
            disk_type=disk['type']
            if disk_type==100 or disk_type=='100':
                disk_type='未知'
        else:
            disk_type='未知'

        disk_info = {'cap':disk_cap,'speed':disk_speed,'inter':disk_inter,'counter':disk_counter,'type':disk_type}
        disks.append(disk_info)
    history = DeviceOperationHistory.query.filter(DeviceOperationHistory.device_id == dev.id).order_by(DeviceOperationHistory.id.desc()).limit(5).all()
    if history:
        for item in history:
            item.username = _user_name(item.uid)
            tmp = json.loads(item.content)
            item.content = "; ".join(tmp.values())

    dev.history = history
    return render_template('device/detail.html', dev=dev, cate=cate, idc=idc,  rack=rack,
                           supplier=supplier, nets_ip=nets_ip, hosts_info=hosts_info,device_infos=device_infos, cpu_info=cpu_info, disks=disks,show=show)

@device.route('/frame_add_services', methods=['POST', 'GET'])
@login_required
def frame_add_services():
    if request.method == 'GET':
        device_cat = DeviceCategory.query.filter(DeviceCategory.name == "服务器").first()
        device_services = Device.query.filter(and_(Device.deleted == 0,Device.frame_id == 0,Device.device_cat_id == device_cat.id)).all()
        services = []
        for service in device_services:
            services.append(service.device_label)
        return app.response_class(json.dumps(services), mimetype='application/json')
    else :
        frame_id = int(request.form['now_id'])
        device_name = request.form['device_name']
        if frame_id > 0 and device_name != "":
            devices = Device.query.filter(and_(Device.deleted == 0,Device.device_label == device_name)).all()
            for device in devices:
                device.frame_id = frame_id
                db.session.commit()
        return redirect(url_for('device.detail',id=frame_id))

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

@device.route('/history/<int:id>', methods=['POST', 'GET'])
@login_required
def history(id):
    info = Device.query.filter(Device.id == id ).first()
    history = DeviceOperationHistory.query.filter(DeviceOperationHistory.device_id == id).order_by(DeviceOperationHistory.id.desc()).all()
    if history:
        for item in history:
            item.username = _user_name(item.uid)
            tmp = json.loads(item.content)
            item.content = "; ".join(tmp.values())
    return render_template("device/history.html",info = info,data=history)


class ExportExcel():
    def exportexcel(self,sheetname,head,content):
        wb = xlwt.Workbook(encoding='utf-8')
        ws = wb.add_sheet(sheetname)
        row = 1
        for column,name in enumerate(head):
            ws.write(0, column, name)
        for count,name in enumerate(content):
            for column,item in enumerate(name):
                ws.write(row, column, item)
            row += 1
        sio = StringIO.StringIO()
        wb.save(sio)
        value = sio.getvalue()
        return value

@device.route('/export', methods=['GET'])
@login_required
def device_excel():
    head = ('id','资产编号','资产类型','机房/机柜','品牌','型号','CPU','内存','硬盘','名称','购买时间','类型','状态','序列号')

    cates = DeviceCategory.query.filter(DeviceCategory.deleted == 0).all()
    cate_names = {}
    for cate in cates:
        cate_names[cate.id] = cate.name
        cate_names[0] = ""

    idcs = Datacenter.query.filter(Datacenter.deleted == 0).all()
    idc_names = {}
    for idc in idcs:
        idc_names[idc.id] = idc.name
        idc_names[0] = ""

    suppliers = Supplier.query.all()
    supp_names = {}
    for supp in suppliers:
        supp_names[supp.id] = supp.short_name
        supp_names[0] = ""

    racks = Rack.query.filter(Rack.deleted == 0).all()
    rack_names = {}
    rack_idc_names = {}
    for rack in racks:
        rack_names[rack.id] = rack.name
        rack_idc_names[rack.id] = idc_names[rack.datacenter_id]
        rack_names[0] = ""
        rack_idc_names[0] = ""

    contents = []
    devices = Device.query.filter(Device.deleted == 0).all()
    for item in devices:
        hostname = ""
        type = ""
        status = ""
        dev_label = item.device_label
        host = Host.query.filter(Host.device_id == item.id).first()
        if host:
            hostname = host.hostname
            type = host.type_descri
            status = host.status_descri
        content = [item.id,dev_label,cate_names[item.device_cat_id],"%s/%s"%(rack_idc_names[item.rack_id],rack_names[item.rack_id]),supp_names[item.supplier_id],item.model_descri,item.cpu_info(),item.memory_info(),item.storage_info(),hostname,item.buy_time.strftime('%Y-%m-%d'),type,status,item.sn]
        contents.append(content)

    excel = ExportExcel()
    value = excel.exportexcel('Sheet1',head,contents)
    return make_response(value, 200, {'Content-type': 'application/vnd.ms-excel',
                                               'Content-Disposition': 'attachment;filename="assets.xls"'})


@device.route('/qrcode/<label>', methods=['POST', 'GET'])
def qrcode(label):
    return label

def _operation_log(device_id, uid, content):
    opt_log = DeviceOperationHistory(device_id, uid, content)
    db.session.add(opt_log)
    db.session.commit()

def update_mem_disk(type,content,d_id,h_id,num,operation):
    param = content.split(" / ")
    device_info = Device.query.filter(Device.id == d_id).first()
    if device_info:
        if type == "mem":
            storage = param[1]
            add = int(storage[:-1])
            if storage[-1] == "M":
                add = add/1000
            if operation == "+":
                device_info.memory = device_info.memory + add*num
            else:
                device_info.memory = device_info.memory - add*num
            device_info.memory_extra = device_info.memory
        else:
            storage = param[0]
            add = int(storage[:-1])
            if storage[-1] == "T":
                add = add*1000
            if operation == "+":
                device_info.storage = device_info.storage + add*num
            else:
                device_info.storage = device_info.storage - add*num
            size = param[1][:-2]
            interface = param[2]
            speed = param[3]
            flag = 0
            if device_info.storage_extra:
                j_disks = json.loads(device_info.storage_extra)
                for j_disk in j_disks:
                    if 'name' in j_disk:
                        disk = append_list(add,speed,interface,size,num)
                    else:
                        if add == j_disk['capacity'] and size == j_disk['size'] and interface == j_disk['interface'] and speed == j_disk['speed']:
                            flag = 1
                            if operation == "+":
                                j_disk['count'] = j_disk['count'] + num
                            else:
                                j_disk['count'] = j_disk['count'] - num
                        if j_disk['count'] != 0:
                            disk = append_list(j_disk['capacity'],j_disk['speed'],j_disk['interface'],j_disk['size'],j_disk['count'])
            if operation == "+" and flag == 0:
                disk = append_list(add,speed,interface,size,num)
            device_info.storage_extra = json.dumps(disk)
        db.session.commit()

def append_list(capacity,speed,interface,size,count):
    disk = []
    disk.append({
                'capacity': capacity,
                'speed': speed,
                'interface': interface,
                'size': size,
                'count': count
            })
    return disk