# -*- coding: utf-8 -*-

from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import login_required, current_user
from application import app, db
from models.dns.dns_zone import DnsZone
from models.dns.dns_history import DnsHistory
from models.dns.dns_apply import DnsApply
from views.functions import responsejson
from views.user import get_user_info,userinfomapping
from dns import add_dns_history
import json,re

dns_category = Blueprint('dns_category', __name__)

@dns_category.route("/")
@login_required
def index():
    cat_list = DnsZone.query.order_by(DnsZone.type.desc()).all()
    uids = []
    for item in cat_list:
        uids.append(item.uid)
    user_mapping = get_user_info(uids = uids)
    idx = 1
    for item in cat_list:
        item.idx = idx
        item.content_part = item.content[:15]
        item.content_len = len(item.content)
        item.approve_name = user_mapping[item.uid].cn_name
        idx += 1
    return render_template('/sa/dns/category/list.html',data=cat_list)

@dns_category.route("/add",methods = ['GET', 'POST'])
@login_required
def add():
    code = 0
    msg = "添加成功"
    zone = request.form['zone']
    display = int(request.form['display'])
    type = int(request.form['type'])
    content = request.form['content']
    approve_uid = request.form['approve_uid']
    if len(zone) <= 0:
        code = 1
        msg = "请输入zone名称"
        return responsejson(code, msg)
    if type < 0:
        code = 1
        msg = "请选择使用范围"
        return responsejson(code, msg)
    hasIn = DnsZone.query.filter(and_(DnsZone.zone == zone,DnsZone.type == type,DnsZone.display == display)).first()
    if hasIn:
        code = 1
        msg = "此zone名称已存在"
        return responsejson(code, msg)
    else:
        zone_target = DnsZone(uid=approve_uid,zone=zone,type=type,display=display,content=content)
        db.session.add(zone_target)
        db.session.commit()
    return responsejson(code, msg)

@dns_category.route("/modify/<int:id>",methods = ['GET', 'POST'])
@login_required
def modify(id):
    code = 0
    msg = "修改成功"
    zone = request.form['zone']
    display = int(request.form['display'])
    type = int(request.form['type'])
    content = request.form['content']
    approve_uid = int(request.form['approve_uid'])
    zone_info = DnsZone.query.filter(DnsZone.id == id).first()
    if zone_info:
        if zone != zone_info.zone:
            zone_info.zone = zone
        if display != zone_info.display:
            zone_info.display = display
        if type != zone_info.type:
            zone_info.type = type
        if content != zone_info.content:
            zone_info.content = content
        if approve_uid != zone_info.uid:
            zone_info.uid = approve_uid
        db.session.commit()
    else:
        code = 1
        msg = "修改失败"
    return responsejson(code,msg)


@dns_category.route("/delete/<int:id>",methods = ['GET', 'POST'])
@login_required
def delete(id):
    code = 0
    msg = "删除成功"
    intreg = re.compile('^[1-9]\d*$')
    if not intreg.match(str(id)):
        code = 1
        msg = "删除失败"
        return responsejson(code,msg)

    zone_info = DnsZone.query.filter(DnsZone.id == id).first()
    db.session.delete(zone_info)
    apply_infos = DnsApply.query.filter(DnsApply.zone_id == id).all()
    for apply_info in apply_infos:
        apply_info.deleted = DnsApply.DELETED_YES
        content = '用户：%s删除域名:%s.%s'%(current_user.cn_name,apply_info.prefix,zone_info.zone)
        add_dns_history(id,DnsHistory.STATUS_DELETE,content)
    db.session.commit()
    return responsejson(code,msg)


@dns_category.route("/get/<int:id>", methods=['GET', 'POST'])
@login_required
def dns_cat_info(id):
    info = DnsZone.query.filter(DnsZone.id == id).first()
    jsonval = {}
    if info:
        jsonval['id'] = info.id
        jsonval['zone'] = info.zone
        jsonval['display'] = info.display
        jsonval['type'] = info.type
        jsonval['content'] = info.content
        jsonval['approve_uid'] = info.uid
        jsonval['approval'] = userinfomapping([info.uid])['uid_%s'%info.uid]
    return app.response_class(json.dumps(jsonval), mimetype='application/json')