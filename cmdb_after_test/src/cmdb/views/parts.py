# -*- coding: utf-8 -*-

from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import login_required,current_user
from application import app, db
from models.stock_parts_model import StockPartsModel
from models.stock_parts import StockParts
from models.stock_history import StockHistory
from models.user import User
from models.device import Device
from models.host import Host
from models.device_operation_history import DeviceOperationHistory
from models.host_operation_history import HostOperationHistory
from models.device import Device
from views.log import addlog
from views.functions import responsejson
from views.device import update_mem_disk
from views.user import find_username
from views.host import device_id_find_host
from sqlalchemy import and_
import datetime
import json
import time

parts = Blueprint('parts', __name__)

@parts.route("/memory", methods=['GET', 'POST'])
@login_required
def memory():
    m_select = request.args.get('model_select',0)
    s_select = request.args.get('status_select',-1)
    mem_model = StockPartsModel.query.filter(StockPartsModel.type == StockPartsModel.TYPE_MEM).all()
    data = display(StockPartsModel.TYPE_MEM,m_select,s_select)
    return render_template("idc/parts/stock_parts.html",model=mem_model,data=data,type='mem',s_select=s_select,m_select=m_select)

@parts.route("/disk", methods=['GET', 'POST'])
@login_required
def disk():
    m_select = request.args.get('model_select',0)
    s_select = request.args.get('status_select',-1)
    disk_model = StockPartsModel.query.filter(StockPartsModel.type == StockPartsModel.TYPE_DISK).all()
    data = display(StockPartsModel.TYPE_DISK,m_select,s_select)
    return render_template("idc/parts/stock_parts.html",model=disk_model,data=data,type='disk',s_select=s_select,m_select=m_select)

def display(type,m_select,s_select):
    ids = []
    modellist = {}
    data = StockParts.query.filter(StockParts.type == type).order_by(StockParts.id.desc()).all()
    if int(s_select) != -1 and int(m_select) != 0:
        data = StockParts.query.filter(and_(StockParts.type == type,StockParts.status == int(s_select),StockParts.model_id == int(m_select))).order_by(StockParts.id.desc()).all()
    elif int(s_select) == -1 and int(m_select) != 0:
        data = StockParts.query.filter(and_(StockParts.type == type,StockParts.model_id == int(m_select))).order_by(StockParts.id.desc()).all()
    elif int(m_select) == 0 and int(s_select) != -1:
        data = StockParts.query.filter(and_(StockParts.type == type,StockParts.status == int(s_select))).order_by(StockParts.id.desc()).all()
    if data:
        for item in data:
            ids.append(item.model_id)
        info = StockPartsModel.query.filter(StockPartsModel.id.in_(ids)).all()
        if info:
            for item in info:
                modellist[item.id] = item.content
        if modellist:
            idx = 1
            for item in data:
                item.ts = time.mktime(time.strptime(str(item.created),'%Y-%m-%d %H:%M:%S'))
                item.model_select = modellist[item.model_id]
                params = item.model_select.split(" / ")
                if type == StockPartsModel.TYPE_MEM:
                    item.model = params[0]
                    item.storage = params[1]
                    item.frequency = params[2]
                else:
                    item.storage = params[0]
                    item.size = params[1]
                    item.interface = params[2]
                    item.speed = params[3]
                    item.if_rate = params[4]
                item.available = ava_cnt(item.status,item.id)
                item.idx = idx
                idx += 1
            return data

@parts.route("/<int:id>", methods=['GET'])
@login_required
def history_detail(id):
    data = {
        "info":None,
        'history':None
    }
    info = StockParts.query.filter(StockParts.id == id).first()
    if not info:
        return redirect(url_for("parts.memory"))
    model_id = info.model_id
    type_descri = info.type_descri
    model_info = StockPartsModel.query.filter(StockPartsModel.id == model_id).first()
    info.model_desc = model_info.content
    info.available = ava_cnt(info.status,info.id)
    data['info'] = info
    #历史记录
    history_info = StockHistory.query.filter(StockHistory.target_id == id).order_by(StockHistory.id.desc()).all()
    history_list = []
    device_ids = []
    uids = []
    if history_info:
        for item in history_info:
            device_ids.append(item.device_id)
            uids.append(item.uid)
        device_host_dic = get_device_host_info(device_ids,'all')
        user_dic = find_username(uids)
        tmp_device_label = ""
        for item in history_info:
            tmp_uname = user_dic[item.uid]
            tmp_content = '%s %s'%(item.created,tmp_uname)
            if item.type == 1:
                tmp_hostname = ''
                tmp_device_host_info = device_host_dic[item.device_id]
                if item.device_id == 0:
                    tmp_content = '%s %s 为%s添加%s %s个'%(item.created,tmp_uname,item.content,type_descri,item.num)
                else:
                    if tmp_device_host_info['device']:
                        tmp_device_label = tmp_device_host_info['device'].device_label
                    if tmp_device_host_info['host']:
                        tmp_hostname = tmp_device_host_info['host'].hostname
                        tmp_content = '%s 为%s(%s)添加%s %s个'%(tmp_content,tmp_device_label,tmp_hostname,type_descri,item.num)
            else:
                if item.status == 1:
                    tmp_hostname = ''
                    tmp_device_host_info = device_host_dic[item.device_id]
                    if item.device_id == 0:
                        tmp_content = '%s %s 从%s报废%s %s个'%(item.created,tmp_uname,item.content,type_descri,item.num)

                    else:
                        if tmp_device_host_info['device']:
                            tmp_device_label = tmp_device_host_info['device'].device_label
                        if tmp_device_host_info['host']:
                            tmp_hostname = tmp_device_host_info['host'].hostname
                            tmp_content = '%s 从%s(%s)报废%s %s个'%(tmp_content,tmp_device_label,tmp_hostname,type_descri,item.num)
                else:
                    tmp_content = '%s 采购%s %s个'%(tmp_content,type_descri,item.num)
            history_list.append(tmp_content)
        data['history'] = history_list

    return render_template("idc/parts/detail.html",data = data)

def cnt(id,type):
    cnt = 0
    info = StockHistory.query.filter(and_(StockHistory.target_id == id,StockHistory.type == type)).all()
    for data in info:
        cnt += data.num
    return cnt

def ava_cnt(status,id):
    ava_num = 0
    if status == StockParts.STATUS_BUY:
        in_cnt = cnt(id,StockHistory.TYPE_IN)
        out_cnt = cnt(id,StockHistory.TYPE_OUT)
        ava_num = int(in_cnt)-int(out_cnt)
    return ava_num

@parts.route("/add_parts", methods=['GET', 'POST'])
@login_required
def add_parts():
    code = 0
    msg = "添加成功"
    name = "内存"
    action = "添加"
    type = request.form['type']
    model = int(request.form['model'])
    num = int(request.form['num'])
    content = request.form['content']
    m_id = int(request.form['m_id'])
    d_id = int(request.form['d_id'])
    status = int(request.form['status'])
    btn = int(request.form['btn'])
    h_id = 0
    total_num = num
    updated = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    if btn == 1:#添加
        _has_in(type,num,updated,d_id,h_id,name,action,model,total_num,status,content)
        return responsejson(code,msg)

    if btn == 2:#报废
        action = "报废"
        h_id = find_h_id(d_id)
        _has_in(type,num,updated,d_id,h_id,name,action,model,total_num,status,content)
        return responsejson(code,msg)

    if btn == 3:#出库
        h_id = find_h_id(d_id)
        info = StockParts.query.filter(StockParts.id == m_id).first()
        _history_update(info,m_id,d_id,h_id,name,num,action,type,content,btn)
        return responsejson(code,msg)

    if btn == 4:#入库
        _type_in_discard(m_id,d_id,h_id,name,num,updated,action,type,content,btn)
        return responsejson(code,msg)

    if btn == 5:#报废m_id!=0
        action = "报废"
        h_id = find_h_id(d_id)
        _type_in_discard(m_id,d_id,h_id,name,num,updated,action,type,content,btn)
        return responsejson(code,msg)

def find_h_id(d_id):
    host_info = device_id_find_host(d_id)
    if host_info:
        h_id = host_info.id
        return h_id

def _type_in_discard(m_id,d_id,h_id,name,num,updated,action,type,content,btn):
    info = StockParts.query.filter(StockParts.id == m_id).first()
    info.num = info.num + num
    info.updated = updated
    db.session.commit()
    _history_update(info,m_id,d_id,h_id,name,num,action,type,content,btn)

def _history_update(info,m_id,d_id,h_id,name,num,action,type,content,btn):
    operation = "+"
    type_in_out = StockHistory.TYPE_IN
    if btn == 3:
        type_in_out = StockHistory.TYPE_OUT
    model_info = StockPartsModel.query.filter(StockPartsModel.id == info.model_id).first()
    history_target = StockHistory(target_id=m_id,device_id=d_id,num=num,status=info.status,type=type_in_out,uid=current_user.id,content=content)
    _operation_log(model_info, name, num, action, d_id, h_id, current_user.id)
    db.session.add(history_target)
    db.session.commit()
    if action == '报废':
        operation = "-"
    if btn != 4:
        update_mem_disk(type,model_info.content,d_id,h_id,num,operation)

def _has_in(type,num,updated,d_id,h_id,name,action,model,total_num,status,content):
    model_info = StockPartsModel.query.filter(StockPartsModel.id == model).first()
    _operation_log(model_info, name, num, action, d_id, h_id, current_user.id)
    if type == "mem":
        stockparts_type = 1
    else:
        stockparts_type = 2
    hasIn = StockParts.query.filter(and_(StockParts.type == stockparts_type,StockParts.model_id == model,StockParts.status == status)).first()
    if hasIn:
        hasIn.num = hasIn.num + num
        hasIn.updated = updated
        db.session.commit()
        history_target = StockHistory(target_id=hasIn.id,device_id=d_id,num=num,status=hasIn.status,type=StockHistory.TYPE_IN,uid=current_user.id,content=content)
    else:
        parts_target = StockParts(type=stockparts_type,model_id=model,num=total_num,status=status)
        db.session.add(parts_target)
        db.session.commit()
        history_target = StockHistory(target_id=parts_target.id,device_id=d_id,num=num,status=status,type=StockHistory.TYPE_IN,uid=current_user.id,content=content)
    db.session.add(history_target)
    db.session.commit()
    if action == "报废":
        operation = "-"
        update_mem_disk(type,model_info.content,d_id,h_id,num,operation)

def _operation_log(model_info, name, num, action, device_id, host_id, uid):
    if model_info.type == 2:
        name = "硬盘"
    log = json.dumps({'create': '%s%s，型号:%s，数量:%s'%(action,name,model_info.content,num)}, ensure_ascii=False, separators=(',', ':')).encode('utf8')
    if device_id != 0:
        device_log = DeviceOperationHistory(device_id, uid, log)
        db.session.add(device_log)
    if host_id != 0:
        host_log = HostOperationHistory(host_id, uid, log)
        db.session.add(host_log)
    db.session.commit()

@parts.route("/autocomplete",methods=['GET', 'POST'])
@login_required
def autocomplete():
    jsonval = []
    keyword = '%' + request.form['keyword'] + '%'
    host_info = Host.query.filter(and_(Host.search.like(keyword),Host.deleted == 0,Host.device_id > 0)).limit(10).all()
    if host_info:
        for item in host_info:
            jsonval.append([item.device_id,item.hostname])
    return app.response_class(json.dumps(jsonval), mimetype='application/json')

@parts.route("/model/memory", methods=['GET', 'POST'])
@login_required
def model_memory():
    data = {'model':[],'storage':[],'frequency':[]}
    parts_target = StockPartsModel()
    model = parts_target.memory_desc()
    model_list = dis_modellist(data,StockPartsModel.TYPE_MEM,model)
    return render_template("idc/parts/model_list.html",data=data,flag="mem",model_list=model_list)

@parts.route("/model/disk", methods=['GET', 'POST'])
@login_required
def model_disk():
    data = {'size':[],'storage':[],'interface':[],'speed':[],'if_rate':[]}
    parts_target = StockPartsModel()
    model = parts_target.disk_desc()
    model_list = dis_modellist(data,StockPartsModel.TYPE_DISK,model)
    return render_template("idc/parts/model_list.html",data=data,flag="disk",model_list=model_list)

def dis_modellist(data,type,model):
    for k,v in data.items():
        evaluation(k,model,data)
    model_list = StockPartsModel.query.filter(StockPartsModel.type == type).order_by(StockPartsModel.id.desc()).all()
    idx = 1
    for item in model_list:
        params = item.content
        params = params.split(" / ")
        if type == StockPartsModel.TYPE_MEM:
            item.model = params[0]
            item.storage = params[1]
            item.frequency = params[2]
        else:
            item.storage = params[0]
            item.size = params[1]
            item.interface = params[2]
            item.speed = params[3]
            item.if_rate = params[4]
        item.idx = idx
        idx += 1
    return model_list

def evaluation(key,dic1,dic2):
    dic = sorted(dic1[key].iteritems(),key=lambda d:d[0])
    for k,v in dic:
        dic2[key].append(v)

@parts.route("/add_model", methods=['GET', 'POST'])
@login_required
def add_model():
    code = 0
    msg = "添加型号成功"
    type = request.form['type']
    if type == "mem":
        model = request.form['model']
        storage = request.form['storage']
        frequency = request.form['frequency']
        content = model+' / '+storage+' / '+frequency
        target = StockPartsModel(type=StockPartsModel.TYPE_MEM,content=content)
    elif type == "disk":
        storage = request.form['storage']
        size = request.form['size']
        interface = request.form['in_fc']
        speed = request.form['speed']
        if_rate = request.form['if_rate']
        content = storage+' / '+size+' / '+interface+' / '+speed+' / '+if_rate
        target = StockPartsModel(type=StockPartsModel.TYPE_DISK,content=content)
    else:
        return responsejson(1,"添加失败")
    hasIn = StockPartsModel.query.filter(StockPartsModel.type == target.type,StockPartsModel.content == content).first()
    if hasIn:
        return responsejson(1,"该型号已存在")
    db.session.add(target)
    db.session.commit()
    logmsg = "添加新型号,id:%d,%s"%(target.id,target.content)
    addlog(logmsg,1)
    return responsejson(code,msg)

@parts.route("/modify_model/<int:id>", methods=['GET', 'POST'])
@login_required
def modify_model(id):
    code = 0
    info = StockPartsModel.query.filter(StockPartsModel.id == id).first()
    type = request.form['type']
    if type == "mem":
        model = request.form['model']
        storage = request.form['storage']
        frequency = request.form['frequency']
        content = model+' / '+storage+' / '+frequency
    elif type == "disk":
        storage = request.form['storage']
        size = request.form['size']
        interface = request.form['in_fc']
        speed = request.form['speed']
        if_rate = request.form['if_rate']
        content = storage+' / '+size+' / '+interface+' / '+speed+' / '+if_rate
    else:
        content = ""
    if content == info.content:
        return responsejson(code, "内容无修改")
    hasIn = StockPartsModel.query.filter(StockPartsModel.type == info.type,StockPartsModel.content == content).first()
    if hasIn:
        return responsejson(1,"该型号已存在")
    info.content = content
    info.updated = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    db.session.commit()
    logmsg = "修改型号,id:%d,%s"%(info.id,info.content)
    addlog(logmsg,1)
    return responsejson(code, "修改成功")

@parts.route("/model/<int:id>", methods=['GET', 'POST'])
@login_required
def detail(id):
    jsonval = {}
    info = StockPartsModel.query.filter(StockPartsModel.id == id).first()
    if info:
        jsonval['id'] = info.id
        content = info.content.split(" / ")
        jsonval['type'] = info.type
        if info.type == 1:
            jsonval['model'] = content[0]
            jsonval['storage'] = content[1]
            jsonval['frequency'] = content[2]
        else:
            jsonval['storage'] = content[0]
            jsonval['size'] = content[1]
            jsonval['interface'] = content[2]
            jsonval['speed'] = content[3]
            jsonval['if_rate'] = content[4]
    return app.response_class(json.dumps(jsonval), mimetype='application/json')

@parts.route("/in_history_memory", methods=['GET', 'POST'])
@login_required
def in_history_memory():
    m_select = request.args.get('model_select',0)
    s_select = request.args.get('status_select',-1)
    flag = 'in'
    mem_model = StockPartsModel.query.filter(StockPartsModel.type == StockPartsModel.TYPE_MEM).all()
    data = display_format(StockParts.TYPE_MEM,flag)
    return render_template("idc/parts/history.html", model=mem_model,data=data, flag=flag, type="mem",s_select=s_select,m_select=m_select)

@parts.route("/in_history_disk", methods=['GET', 'POST'])
@login_required
def in_history_disk():
    m_select = request.args.get('model_select',0)
    s_select = request.args.get('status_select',-1)
    flag = 'in'
    disk_model = StockPartsModel.query.filter(StockPartsModel.type == StockPartsModel.TYPE_DISK).all()
    data = display_format(StockParts.TYPE_DISK,flag)
    return render_template("idc/parts/history.html", model=disk_model, data=data, flag=flag, type="disk",s_select=s_select,m_select=m_select)

@parts.route("/out_history_memory", methods=['GET', 'POST'])
@login_required
def out_history_memory():
    m_select = request.args.get('model_select',0)
    s_select = request.args.get('status_select',-1)
    flag = 'out'
    mem_model = StockPartsModel.query.filter(StockPartsModel.type == StockPartsModel.TYPE_MEM).all()
    data = display_format(StockParts.TYPE_MEM,flag)
    return render_template("idc/parts/history.html", model=mem_model, data=data, flag=flag, type="mem",s_select=s_select,m_select=m_select)

@parts.route("/out_history_disk", methods=['GET', 'POST'])
@login_required
def out_history_disk():
    m_select = request.args.get('model_select',0)
    s_select = request.args.get('status_select',-1)
    flag = 'out'
    disk_model = StockPartsModel.query.filter(StockPartsModel.type == StockPartsModel.TYPE_DISK).all()
    data = display_format(StockParts.TYPE_DISK,flag)
    return render_template("idc/parts/history.html", model=disk_model, data=data, flag=flag, type="disk",s_select=s_select,m_select=m_select)

def display_format(type,action):
    m_select = request.args.get('model_select',0)
    s_select = request.args.get('status_select',-1)
    parts_models_ids = []
    parts_ids = []
    parts_dic = {}
    parts_list = StockParts.query.filter(StockParts.type == type).all()
    for item in parts_list:
        parts_dic[item.id] = item.model_id
        parts_models_ids.append(item.model_id)
        parts_ids.append(item.id)

    parts_models_dic = {}
    parts_models_list = StockPartsModel.query.filter(and_(StockPartsModel.type == type,StockPartsModel.id.in_(parts_models_ids))).all()

    for item in parts_models_list:
        params = item.content
        params = params.split(" / ")
        if type == StockPartsModel.TYPE_MEM:
            parts_models_dic["model_%s"%item.id] = params[0]
            parts_models_dic["storage_%s"%item.id] = params[1]
            parts_models_dic["frequency_%s"%item.id] = params[2]
        else:
            parts_models_dic["storage_%s"%item.id] = params[0]
            parts_models_dic["size_%s"%item.id] = params[1]
            parts_models_dic["interface_%s"%item.id] = params[2]
            parts_models_dic["speed_%s"%item.id] = params[3]
            parts_models_dic["if_rate_%s"%item.id] = params[4]
    parts_mem_dic = []
    histype = StockHistory.TYPE_OUT
    if action == "in":
        histype = StockHistory.TYPE_IN

    if int(m_select):
        parts_ids = []
        parts_dic = {}
        target = StockParts.query.filter(and_(StockParts.type == type,StockParts.model_id == int(m_select))).all()
        for item in target:
            parts_dic[item.id] = item.model_id
            parts_ids.append(item.id)

    parts_his_list = StockHistory.query.filter(and_(StockHistory.type == histype,StockHistory.target_id.in_(parts_ids))).order_by(StockHistory.id.desc()).all()
    if int(s_select) != -1 and int(m_select) != 0:
        parts_his_list = StockHistory.query.filter(and_(StockHistory.type == histype,StockHistory.target_id.in_(parts_ids),StockHistory.status == int(s_select))).order_by(StockHistory.id.desc()).all()
    elif int(s_select) == -1 and int(m_select) != 0:
        parts_his_list = StockHistory.query.filter(and_(StockHistory.type == histype,StockHistory.target_id.in_(parts_ids))).order_by(StockHistory.id.desc()).all()
    elif int(m_select) == 0 and int(s_select) != -1:
        parts_his_list = StockHistory.query.filter(and_(StockHistory.type == histype,StockHistory.status == int(s_select)),StockHistory.target_id.in_(parts_ids)).order_by(StockHistory.id.desc()).all()
    parts_device_ids = []
    parts_uids = []
    for item in parts_his_list:
        parts_device_ids.append(item.device_id)
        parts_uids.append(item.uid)

    parts_uids_dic = find_username(parts_uids)
    parts_device_dic = get_device_host_info(parts_device_ids,action)
    idx = 1
    for item in parts_his_list:
        tmp_device_host_info = parts_device_dic[item.device_id]
        tmp_device_label = '未知'
        tmp_device_id = 0
        if tmp_device_host_info['device']:
            tmp_device_id = tmp_device_host_info['device'].id
            tmp_device_label = tmp_device_host_info['device'].device_label
        tmp_hostname = '未知'
        tmp_host_id = 0
        if tmp_device_host_info['host']:
            tmp_host_id = tmp_device_host_info['host'].id
            tmp_hostname = tmp_device_host_info['host'].hostname

        if (item.status==0 and item.type==1 and item.device_id==0) or (item.status==1 and item.type==0 and item.device_id==0):
            tmp_hostname = item.content
            tmp_device_label = "--"
            tmp_device_id = 0
            tmp_host_id= 0
        tmp_cnt = item.num
        tmp_dt = item.created
        tmp_stamp = time.mktime(time.strptime(str(tmp_dt),'%Y-%m-%d %H:%M:%S'))
        tmp_persion = parts_uids_dic[item.uid]
        if type == StockPartsModel.TYPE_MEM:
            parts_mem_dic.append({
                'target_id':item.target_id,
                'model':parts_models_dic["model_%s"%parts_dic[item.target_id]],
                'mem_storage':parts_models_dic["storage_%s"%parts_dic[item.target_id]],
                'frequency':parts_models_dic["frequency_%s"%parts_dic[item.target_id]],
                'disk_storage':parts_models_dic["storage_%s"%parts_dic[item.target_id]],
                'device_label':tmp_device_label,
                'device_id':tmp_device_id,
                'hostname':tmp_hostname,
                'host_id':tmp_host_id,
                'cnt':tmp_cnt,
                'dt':tmp_dt,
                'ts':tmp_stamp,
                'person':tmp_persion,
                'content':'',
                'status':item.status_descri,
                'idx':idx,
                'flag':item.status,
                'type':item.type
            })
        else:
            parts_mem_dic.append({
                'target_id':item.target_id,
                'disk_storage':parts_models_dic["storage_%s"%parts_dic[item.target_id]],
                'size':parts_models_dic["size_%s"%parts_dic[item.target_id]],
                'interface':parts_models_dic["interface_%s"%parts_dic[item.target_id]],
                'speed':parts_models_dic["speed_%s"%parts_dic[item.target_id]],
                'if_rate':parts_models_dic["if_rate_%s"%parts_dic[item.target_id]],
                'device_label':tmp_device_label,
                'device_id':tmp_device_id,
                'hostname':tmp_hostname,
                'host_id':tmp_host_id,
                'cnt':tmp_cnt,
                'dt':tmp_dt,
                'ts':tmp_stamp,
                'person':tmp_persion,
                'content':'',
                'status':item.status_descri,
                'idx':idx,
                'flag':item.status,
                'type':item.type
            })
        idx += 1
    return parts_mem_dic

def get_device_host_info(device_ids,action):
    returnval = {}
    returnval[0] = {
            'device':None,
            'host':None
    }
    device_info_lists = Device.query.filter(and_(Device.id.in_(device_ids),Device.deleted == 0)).all()
    if device_info_lists:
        for item in device_info_lists:
            tmp = {
                'device':item,
                'host':None
            }
            returnval[item.id] = tmp

    host_info_lists = Host.query.filter(and_(Host.device_id.in_(device_ids),Host.deleted == 0)).all()
    if host_info_lists:
        for item in host_info_lists:
            returnval[item.device_id]['host'] = item
    return returnval


