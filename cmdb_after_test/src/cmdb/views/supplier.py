# -*- coding: utf-8 -*-
from flask import Blueprint, render_template, request
from flask_login import login_required, current_user
from models.supplier import Supplier
from models.log import Log
from views.functions import responsejson
from views.log import addlog
import json
from application import app,db
import datetime
import re,json,math
from views.functions import visible

supplier = Blueprint('supplier', __name__)

@supplier.route("/")
@login_required
def index():
    show = visible()
    supinfo=Supplier.query.order_by(Supplier.id).all()
    return render_template("idc/supplier.html",supinfo=supinfo,show=show)

@supplier.route("/add", methods=['GET', 'POST'])
@login_required
def add():
    code = 0
    msg = "添加供应商成功"
    if request.method == 'POST':
        name = request.form['name']
        short_name = request.form['short_name']
        content = request.form['content']
        if(len(name) <= 0):
            code=1
            msg="请输入供应商名称"
            return responsejson(code, msg)
        if(len(short_name) <= 0):
            code=1
            msg="请输入供应商名称"
            return responsejson(code, msg)
        hasIn=Supplier.query.filter(Supplier.name==name).first()
        if hasIn:
            code=1
            msg="此供应商已存在"
            return responsejson(code,msg)
        suptarget = Supplier(name=name,short_name=short_name, content=content)
        db.session.add(suptarget)
        db.session.commit()
        logmsg="添加供应商,供应商id:%s,供应商名称:%s"%(suptarget.id,name)
        addlog(logmsg,1)
    else:
        code = 1
        msg = "添加供应商失败"
    return responsejson(code, msg)

@supplier.route("/<int:id>", methods=['GET', 'POST'])
@login_required
def detail(id):
    jsonval = {}
    info = Supplier.query.filter(Supplier.id == id).first()
    if info:
        jsonval['id'] = info.id
        jsonval['name'] = info.name
        jsonval['short_name'] = info.short_name
        jsonval['content'] = info.content
    return app.response_class(json.dumps(jsonval), mimetype='application/json')

@supplier.route("/modify/<int:id>", methods=['GET', 'POST'])
@login_required
def modify(id):
    logmsg=""
    code=0
    msg="修改供应商成功"
    intreg=re.compile('^\d*$')
    if not intreg.match(str(id)):
        code=1
        msg="修改供应商失败:id有问题"
        return responsejson(code,msg)
    info = Supplier.query.filter(Supplier.id == id).first()
    name = request.form['name']
    short_name = request.form['short_name']
    content = request.form['content']

    if info.name == name and info.short_name == short_name and info.content == content:
        return responsejson(code, "内容无修改")
    else:
        if info.name!=name:
            logmsg=logmsg+"name:%s 更改为 %s"%(info.name,name)+","
            info.name=name
        if info.short_name!=short_name:
            logmsg=logmsg+"short_name:%s 更改为 %s"%(info.short_name,short_name)+","
            info.short_name=short_name
        if info.content!=content:
            logmsg=logmsg+"content:%s 更改为 %s"%(info.content,content)+","
            info.content=content
        info.updated=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        db.session.commit()
        logmsg="修改供应商信息,供应商id:%s,名称:%s, %s"%(info.id,info.name,logmsg)
        addlog(logmsg,1)
        return responsejson(code, msg)

