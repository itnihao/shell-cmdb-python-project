# -*- coding: utf-8 -*-

from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import login_required, current_user
from application import app, db
from sqlalchemy import or_,and_,desc
from views.functions import responsejson
from views.user import get_user_info
from models.sa.tickets_category import Tickets_Category

tickets_category = Blueprint('tickets_category', __name__)

@tickets_category.route("/")
@login_required
def index():
    if not current_user.is_sa:
        return redirect("/")
    cat_list = Tickets_Category.query.all()
    uids = []
    for item in cat_list:
        uids.append(item.manage_uid)
    user_mapping = get_user_info(uids = uids)
    idx = 1
    for item in cat_list:
        item.idx = idx
        item.manage_cname = user_mapping[item.manage_uid].cn_name
        idx += 1
    return render_template("/sa/tickets/category/list.html",data = cat_list)

@tickets_category.route("/add",methods=['POST'])
@login_required
def add():
    if not current_user.is_sa:
        return redirect("/")
    code = 0
    msg  = '添加成功'
    name = request.form['name'].strip()
    label = request.form['label'].strip()
    manage_uid = int(request.form['manage_uid'].strip())
    template = request.form['template'].strip()
    if len(name) < 2:
        code = 1
        msg = '请输入分类名称'
        return responsejson(code, msg)
    if len(label) < 2:
        code = 1
        msg = '请输入分类名称'
        return responsejson(code, msg)
    if manage_uid < 0:
        code = 1
        msg = '请输入此分类工单处理人'
        return responsejson(code, msg)
    manage_info = get_user_info(id = manage_uid)
    if not manage_info:
        code = 1
        msg = '工单处理人非法'
        return responsejson(code, msg)
    has_in = Tickets_Category.query.filter(and_(Tickets_Category.name == name,Tickets_Category.label == label )).first()
    if has_in:
        code = 1
        msg = '此分类已经存在'
        return responsejson(code, msg)
    target = Tickets_Category(name = name,label = label,manage_uid = manage_uid, template = template)
    db.session.add(target)
    db.session.commit()
    return responsejson(code, msg)

@tickets_category.route("/<int:id>",methods=['POST'])
@login_required
def detail(id):
    if not current_user.is_sa:
        return redirect("/")
    code = 0
    msg  = '添加成功'
    ticket_cat_info = Tickets_Category.query.filter(Tickets_Category.id == id).first()
    if not ticket_cat_info:
        code = 1
        msg = '此分类不存在'
    data = {}
    data['id'] = ticket_cat_info.id
    data['name'] = ticket_cat_info.name
    data['label'] = ticket_cat_info.label
    data['template'] = ticket_cat_info.template
    data['manage_uid'] = ticket_cat_info.manage_uid
    data['manage_cname'] =  get_user_info(id = ticket_cat_info.manage_uid).cn_name
    return responsejson(code, msg, data)


@tickets_category.route("/mod",methods=['POST'])
@login_required
def mod():
    if not current_user.is_sa:
        return redirect("/")
    code = 0
    msg  = '修改成功'
    name = request.form['name'].strip()
    label = request.form['label'].strip()
    manage_uid = int(request.form['manage_uid'].strip())
    template = request.form['template'].strip()
    if len(name) < 2:
        code = 1
        msg = '请输入分类名称'
        return responsejson(code, msg)
    if len(label) < 2:
        code = 1
        msg = '请输入分类名称'
        return responsejson(code, msg)
    if manage_uid < 0:
        code = 1
        msg = '请输入此分类工单处理人'
        return responsejson(code, msg)
    manage_info = get_user_info(id = manage_uid)
    if not manage_info:
        code = 1
        msg = '工单处理人非法'
        return responsejson(code, msg)
    ticket_cat_info  = Tickets_Category.query.filter(and_(Tickets_Category.name == name,Tickets_Category.label == label )).first()
    if not ticket_cat_info:
        code = 1
        msg = '此分类不存在'
        return responsejson(code, msg)
    ticket_cat_info.name = name
    ticket_cat_info.label = label
    ticket_cat_info.template = template
    ticket_cat_info.manage_uid = manage_uid
    db.session.commit()
    return responsejson(code, msg)

