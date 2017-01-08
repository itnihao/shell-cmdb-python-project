# -*- coding: utf-8 -*-

from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import login_required, current_user
from application import app, db
from models.host import Host
from models.device import Device
from models.pool import Pool
from views.functions import responsejson
from config import DOMAIN
from sqlalchemy import and_
import re, json

pmz_search = Blueprint('pmz_search', __name__)


@pmz_search.route("/", methods=['GET', 'POST'])
@login_required
def index():
    q = request.form['q']
    size = int(request.form['size'])
    if q:
        kw = '%'+q+'%'
        all_dic = {}
        poolnum = Pool.query.filter(Pool.search.like(kw)).count()
        all_dic['pool'] = {'size': poolnum, 'data': [], 'url': ""}

        if 0 < poolnum <= size:
            data = []
            poollist = Pool.query.filter(Pool.search.like(kw)).all()
            if poollist:
                for pool in poollist:
                    tmp_content = '%s%s'%(pool.source_desc,pool.name)
                    tmp_url = url_for('pool.detail',id=pool.id)
                    data.append([tmp_content,tmp_url])
                all_dic['pool']['data'] = data
                url = url_for('pool.index') + '?q=' + q
                all_dic['pool']['url'] = url
        elif poolnum > size:
            url = url_for('pool.index') + '?q=' + q
            all_dic['pool']['url'] = url

        hostnum = int(Host.query.filter(and_(Host.search.like(kw),Host.deleted == 0)).count())
        all_dic['host'] = {'size': hostnum, 'data': [], 'url': ""}
        if 0 < hostnum <= size:
            data = []
            hostlist = Host.query.filter(and_(Host.search.like(kw),Host.deleted == 0)).all()
            if hostlist:
                for host in hostlist:
                    tmp_content = host.hostname
                    tmp_url = url_for('host.host_detail',id=host.id)
                    data.append([tmp_content,tmp_url])
                all_dic['host']['data'] = data
                url = url_for('host.index') + '?q=' + q + '&status=0&type=0'
                all_dic['host']['url'] = url
        elif hostnum > size:
            url = url_for('host.index') + '?q=' + q + '&status=0&type=0'
            all_dic['host']['url'] = url

        devicenum = Device.query.filter(and_(Device.search.like(kw),Device.deleted == 0)).count()
        all_dic['device'] = {'size':devicenum, 'data': [], 'url': ""}
        if 0 < devicenum <= size:
            data = []
            devicelist = Device.query.filter(and_(Device.search.like(kw),Device.deleted == 0)).all()
            if devicelist:
                for device in devicelist:
                    tmp_content = device.device_label
                    tmp_url = url_for('device.detail',id=device.id)
                    data.append([tmp_content,tmp_url])
                all_dic['device']['data'] = data
                url = url_for('device.list') + '?cate=0&idc=0&rack=0&date=&kw=' + q
                all_dic['device']['url'] = url
        elif devicenum > size:
            url = url_for('device.list') + '?cate=0&idc=0&rack=0&date=&kw=' + q
            all_dic['device']['url'] = url

        return responsejson(0,msg = "success",data = all_dic)