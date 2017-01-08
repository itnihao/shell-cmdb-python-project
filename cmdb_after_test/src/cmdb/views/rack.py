# -*- coding: utf-8 -*-
from __future__ import division
from flask import Blueprint, render_template, request
from flask_login import login_required, current_user
from models.rack import Rack
from models.datacenter import Datacenter
from models.device import Device
from models.device_category import DeviceCategory
from models.supplier import Supplier
from models.host import Host
from models.follow import Follow
from views.host import _get_ip
from views.functions import responsejson
from .log import addlog
import json
from application import app, db
import datetime
import re, json
from views.functions import visible
from sqlalchemy import and_, or_

rack = Blueprint('rack', __name__)

@rack.route("/", methods = ['GET', 'POST'])
@rack.route("/page/<int:page>", methods = ['GET', 'POST'])
@login_required
def index():
    show = visible()
    rack_info = Rack.query.filter(Rack.deleted == 0).all()
    dc_info = Datacenter.query.filter(Datacenter.deleted == 0).all()
    dc_rack_info = []
    dc_rack_index = {}
    index_flag = 0
    for dc_item in dc_info:
        tmp_info = {'id':dc_item.id,'name':dc_item.name,'data':[],"status":'','auto_increment':1}
        if index_flag == 0:
            tmp_info['status'] = 'active'
        dc_rack_info.append(tmp_info)
        dc_rack_index[dc_item.id] = index_flag
        index_flag = index_flag +1

    for rack_item in rack_info:
        device_num = Device.query.filter(Device.rack_id == rack_item.id).count()
        is_followed = 0
        follow_info = Follow.query.filter(and_(Follow.type == 3,Follow.target_id == rack_item.id,Follow.uid == current_user.id)).first()
        if follow_info:
            is_followed = 1
        tmp_idx = dc_rack_index[rack_item.datacenter_id]
        tmp_info = {"name":rack_item.name, "id":rack_item.id,"height":rack_item.height,"content":rack_item.content,
                    "datacenter_id":rack_item.datacenter_id,"dc_name":dc_rack_info[tmp_idx]['name'],
                    'no':dc_rack_info[tmp_idx]['auto_increment'],'followed':is_followed, 'device_num':device_num}
        dc_rack_info[tmp_idx]['auto_increment'] +=1
        dc_rack_info[tmp_idx]['data'].append(tmp_info)

    return render_template("idc/rack.html", dc_rack_info = dc_rack_info, dc_info = dc_info,show=show)


@rack.route("/add", methods = ['GET', 'POST'])
@login_required
def add():
    logmsg=""
    code = 0
    msg = "添加机柜成功"
    if request.method == 'POST':
        name = request.form['name']
        height = request.form['height']
        content = request.form['content']
        dc_id = request.form['dc_id']
        if len(name) <= 0:
            code = 1
            msg = "请输入机柜名称"
            return responsejson(code, msg)
        if len(dc_id) <= 0 or int(dc_id) <= 0:
            code = 1
            msg = "请选择所属机房"
            return responsejson(code, msg)
        if len(height) <= 0:
            code = 1
            msg = "请输入机柜高度"
            return responsejson(code, msg)
        hasIn = Rack.query.filter(and_(Rack.datacenter_id == dc_id, Rack.name == name)).all()
        if hasIn:
            code = 1
            msg = "此机柜已存在"
            return responsejson(code, msg)
        racktarget = Rack(name = name, datacenter_id = dc_id, height = height, content = content)
        db.session.add(racktarget)
        db.session.commit()
        username = current_user.name
        logmsg = "用户%s添加机柜,机柜id:%s,机柜名称:%s"%(username,racktarget.id,name)
        addlog(logmsg,1)
    else:
        code = 1
        msg = "添加机柜失败"
    return responsejson(code, msg)

@rack.route("/detail/<int:id>",methods = ['GET','POST'])
@login_required
def showDetail(id):
    rack =Rack.query.filter(Rack.id == id).first()
    rack_name = rack.name
    idc = Datacenter.query.filter(Datacenter.id == rack.datacenter_id).first()
    idc_name = idc.name
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
    device = Device.query.filter(Device.rack_id == id).all()
    host_target = Host.query.filter(Host.deleted == Host.DELETED_NO)
    if device:
        device_id = []
        for item in device:
            device_id.append(item.id)
        hosts = host_target.filter(Host.device_id.in_(device_id)).all()
        apc_id = []
        if hosts:
            for item in hosts:
                if item.is_virtual == 0:
                    apc_id.append(item.id)
            hosts_info = host_target.filter(or_(Host.parent_id.in_(apc_id), Host.device_id.in_(device_id))).all()
            if hosts_info:
                for host in hosts_info:
                    host.ip = _get_ip(host.primary_ip_id)
    else:
        return render_template("idc/rack_detail.html", idc_name=idc_name, rack_name=rack_name)
    return render_template("idc/rack_detail.html",device=device, cate_names=cate_names, supp_names=supp_names,
                            rack_names=rack_names, rack_idc_names=rack_idc_names, datas=hosts_info, idc_name=idc_name, rack_name=rack_name)

@rack.route("/<int:id>", methods=['GET', 'POST'])
@login_required
def detail(id):
    jsonval = {}
    info = Rack.query.filter(Rack.id == id).first()
    if info:
        jsonval['id'] = info.id
        jsonval['name'] = info.name
        jsonval['height'] = info.height
        jsonval['datacenter_id'] = info.datacenter_id
        jsonval['content'] = info.content
    return app.response_class(json.dumps(jsonval), mimetype='application/json')

@rack.route("/modify/<int:id>", methods = ['GET', 'POST'])
@login_required
def modify(id):
    logmsg = ""
    code = 0
    msg = "修改机柜成功"
    intreg = re.compile('^\d*$')
    if not intreg.match(str(id)):
        code = 1
        msg = "修改机柜失败:id有问题"
        return responsejson(code,msg)
    info = Rack.query.filter(Rack.id == id).first()
    name = request.form['name']
    dc_id = request.form['dc_id']
    height = request.form['height']
    content = request.form['content']
    if info.name == name and info.datacenter_id == int(dc_id) and info.height == int(height) and info.content == content:
        return responsejson(code, "内容无修改")
    else:
        if info.name != name:
            logmsg = logmsg + "name:%s 更改为 %s"%(info.name,name) + ","
            info.name = name
        if info.height != int(height):
            if int(height) > 127:
                height = 127
            logmsg = logmsg+"height:%s 更改为 %s"%(info.height,height) + ","
            info.height = height
        if info.datacenter_id != int(dc_id):
            logmsg = logmsg + "datacenter_id:%s 更改为 %s"%(info.datacenter_id,dc_id) + ","
            info.datacenter_id = dc_id
        if info.content != content:
            logmsg = logmsg + "content:%s 更改为 %s"%(info.content,content) + ","
            info.content = content
        info.updated = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        db.session.commit()
        logmsg = "修改机柜信息,机柜id:%s,名称:%s,%s"%(info.id,info.name,logmsg)
        addlog(logmsg,1)
        return responsejson(code, msg)

@rack.route("/delete/<int:id>", methods=['GET', 'POST'])
@login_required
def delete(id):
    import re
    intreg = re.compile('^[1-9]\d*$')
    if intreg.match(str(id)):
        print 1
    info = Rack.query.filter(Rack.id == id).first()
    db.session.delete(info)
    db.session.commit()
    logmsg = "删除机房,机房id:%d"%(username,id)
    addlog(logmsg,1)
    return responsejson(0, "删除机柜成功")






