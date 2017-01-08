# -*- coding: utf-8 -*-
from flask import Blueprint, render_template,request,url_for
from flask_login import login_required
from flask_login import current_user
from application import app,db
from models.follow import Follow
from models.host import Host
from models.user import User
from models.pool import Pool
from models.rack import Rack
from models.datacenter import Datacenter
from models.pool_host import PoolHost
from models  import IpAddress
from views.functions import responsejson
from sqlalchemy import and_
from views.monitor.index import _get_rack_host
import urllib2;
from urllib2 import URLError;
import json;
import time;
import re;
import redis;

#Api url of zabbix (Writren by robanlee)
logger = Blueprint('logger', __name__)



'''
Default route of logger
@author Robanlee@gmail.com
@return html
'''
@logger.route("/")
@login_required
def index():
    '''
    PoolID is not required
    '''
    settings = {"nav":"logger"};
    host_name = request.args.get('host_name') or None;
    pool_id = request.args.get('pool_id') or None;
    rack_id = request.args.get('rack_id') or None;
    auto = request.args.get('auto') or None;
    host_name_in_pool = "";
    hosts = []
    if pool_id:
        hosts = db.session.query(Host).filter(and_(PoolHost.pool_id==pool_id,PoolHost.host_id==Host.id)).all()
    if rack_id:
        hosts = _get_rack_host(rack_id)
    for x in hosts:
        host_name_in_pool += ","+ x.hostname;
    host_name_in_pool = host_name_in_pool.lstrip(",")
    followdHost = db.session.query(Host).filter(and_(Follow.target_id==Host.id, Follow.type==2, Follow.uid==current_user.id)).all()

    return render_template("logger/logger_index_tpl.html",settings=settings,host_name=host_name,followdHost=followdHost,auto=auto,host_name_in_pool=host_name_in_pool)

@logger.route("/pools",methods=['POST','GET'])
@login_required
def get_follow_pools():
    code = 0
    msg = "成功"
    uid=current_user.id
    followdPools = Follow.query.filter(and_(Follow.uid==uid, Follow.type==1)).all()
    poolids=[]
    data=[]
    if followdPools:
        for item in followdPools:
            poolids.append(item.target_id)
    if poolids:
        poolinfos=Pool.query.filter(Pool.id.in_(poolids)).all()
        if poolinfos:
            for item in poolinfos:
                data.append({'id':item.id,'name':item.name})
    return responsejson(code,msg,data)

@logger.route("/racks",methods=['POST','GET'])
@login_required
def get_follow_racks():
    code = 0
    msg = "成功"
    uid=current_user.id
    followdracks = Follow.query.filter(and_(Follow.uid==uid, Follow.type==3)).all()
    data=[]
    if followdracks:
        for item in followdracks:
            rack = Rack.query.filter(Rack.id == item.target_id).first()
            idcinfo = Datacenter.query.filter(Datacenter.id == rack.datacenter_id).first()
            if idcinfo:
                idcname = idcinfo.name
                info = {'id':item.target_id,'rackname':rack.name,'idcname':idcname}
                data.append(info)
    return responsejson(code,msg,data)



