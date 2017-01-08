import re
from sqlalchemy import and_
import json as myjson

from flask import Blueprint, render_template, request,json

from flask_login import login_required

from application import fujs,app
from models.puv import PUV
from sqlalchemy import and_
from views.functions import visible, responsejson
from views.log import addlog
from  models.puv import *

import  datetime


@app.context_processor
def inject_fujs():
    return dict(fujs=fujs)

puv = Blueprint('puv', __name__)

@puv.route("/index", methods=['POST', 'GET'])
@login_required
def index():
    # insert_time=datetime.datetime.strptime('20110212 02:00:00','%Y%m%d %H:%M:%S')
    # dctarget=PUV(hour='02',pv=1,pv_nospider=1,uv=1,
    #                      pv_uv=1,dataday='20110212',pv_nospider_m=1,pv_nospider_p=1,
    #                      uv_m=1,uv_p=1,time_f=insert_time)
    # db.session.add(dctarget)
    # db.session.commit()


    return render_template('puv/puv.html')

@puv.route("/getinit",methods=['GET', 'POST'])
@login_required
def getinit():
    now_time =datetime.datetime.now()
    yes_time = now_time + datetime.timedelta(days=-1)
    fday = yes_time.strftime('%Y%m%d')
    all_data=PUV.query.filter(PUV.dataday==fday).order_by(PUV.time_f).all()
    # pv, pv_nospider, pv_nospider_m, pv_nospider_p, uv, uv_m, uv_p, pv_uv, dataday, hour,time_f
    chart_data_s={'date':'','pv':0,'pv_nospider':0,'pv_nospider_m':0,'pv_nospider_p':0,'uv':0,'uv_m':0,'uv_p':0,'pv_uv':0}
    chart_data=[]
    for i in all_data:
        chart_data.append({'date':i.date_descri,'pv':i.pv,'pv_nospider':i.pv_nospider,'pv_nospider_m':i.pv_nospider_m,
                           'pv_nospider_p':i.pv_nospider_p,'uv':i.uv,'uv_m':i.uv_m,'uv_p':i.uv_p,'pv_uv':i.pv_uv,
                           'pv_u':i.pv_u,'pv_u_m':i.pv_u_m,'pv_u_p':i.pv_u_p,'pv_office':i.pv_office,'pv_office_m':i.pv_office_m,
                           'pv_office_p':i.pv_office_p,'pv_whitelist':i.pv_whitelist,'pv_whitelist_m':i.pv_whitelist_m,
                           'pv_whitelist_p':i.pv_whitelist_p,'request_time':i.request_time,'response_time':i.response_time})

    return_data={'data':chart_data}
    return app.response_class(json.dumps(return_data), mimetype='application/json')


@puv.route("/compare",methods=['GET', 'POST'])
@login_required
def compare():
    if request.method == 'POST':
        s_date=myjson.loads(request.form.get('sdate'))
        try:
            chart_data=''
            c1=''
            c2=''
            c3=''
            if s_date['source']:
                firsttime = datetime.datetime.strptime(s_date['source']['f'],'%Y-%m-%d')
                endtime = datetime.datetime.strptime(s_date['source']['l'],'%Y-%m-%d')
                endtime=endtime+datetime.timedelta(hours=23)
                chart_data = get_puv_data(firsttime,endtime)
                if (not chart_data):
                    return app.response_class(json.dumps({'data':'','c1':'','c2':'','c3':'','code':0}), mimetype='application/json')
                if not chart_data:
                    return app.response_class(json.dumps({'data':'','c1':'','c2':'','c3':'','code':0}), mimetype='application/json')
            if s_date['c1']:
                firsttime = datetime.datetime.strptime(s_date['c1']['f'],'%Y-%m-%d')
                endtime = datetime.datetime.strptime(s_date['c1']['l'],'%Y-%m-%d')
                endtime=endtime+datetime.timedelta(hours=23)
                c1 = get_puv_data(firsttime,endtime)
                if (not c1) or(len(c1)!=len(chart_data)):
                    return app.response_class(json.dumps({'data':'','c1':'','c2':'','c3':'','code':0}), mimetype='application/json')
                for i in range(0,len(chart_data)):
                    c1[i]['date']=chart_data[i]['date']
            if s_date['c2']:
                firsttime = datetime.datetime.strptime(s_date['c2']['f'],'%Y-%m-%d')
                endtime = datetime.datetime.strptime(s_date['c2']['l'],'%Y-%m-%d')
                endtime=endtime+datetime.timedelta(hours=23)
                c2 = get_puv_data(firsttime,endtime)
                if (not c2) or(len(c2)!=len(chart_data)):
                    return app.response_class(json.dumps({'data':'','c1':'','c2':'','c3':'','code':0}), mimetype='application/json')
                for i in range(0,len(chart_data)-1):
                    c2[i]['date']=chart_data[i]['date']
            if s_date['c3']:
                firsttime = datetime.datetime.strptime(s_date['c3']['f'],'%Y-%m-%d')
                endtime = datetime.datetime.strptime(s_date['c3']['l'],'%Y-%m-%d')
                endtime=endtime+datetime.timedelta(hours=23)
                c3 = get_puv_data(firsttime,endtime)
                if (not c3) or(len(c3)!=len(chart_data)):
                    return app.response_class(json.dumps({'data':'','c1':'','c2':'','c3':'','code':0}), mimetype='application/json')
                for i in range(0,len(chart_data)-1):
                    c3[i]['date']=chart_data[i]['date']
            return_data={'data':chart_data,'c1':c1,'c2':c2,'c3':c3,'code':1}
            return app.response_class(json.dumps(return_data), mimetype='application/json')
        except Exception,e:
            return app.response_class(json.dumps({'data':'','c1':'','c2':'','c3':'','code':0}), mimetype='application/json')

@puv.route("/get_puv/<dates>", methods=['POST', 'GET'])
@login_required
def get_puv(dates):
    if not dates :
        return render_template('error.html',status = 404,title = 'unknown error',msg = 'Can\'t find the page!')

    times = dates.split("&", 1)
    if len(times) < 2 :
        return render_template('error.html',status = 404,title = 'unknown error',msg = 'Can\'t find the page!')

    firsttime = datetime.datetime.strptime(times[0],'%Y-%m-%d')
    endtime = datetime.datetime.strptime(times[1],'%Y-%m-%d')
    endtime=endtime+datetime.timedelta(hours=23)
    chart_data = get_puv_data(firsttime,endtime)
    # chart_95=[]
    # for c_d in  chart_data

    return_data={'data':chart_data}

    return app.response_class(json.dumps(return_data), mimetype='application/json')


def get_puv_data(firsttime,endtime):
    if firsttime and endtime:
        if(firsttime==endtime):
            fday = endtime.strftime('%Y%m%d')
            datas = PUV.query.filter(PUV.dataday == fday).order_by(PUV.time_f).all()
        else:
            datas = PUV.query.filter(and_(PUV.time_f >= firsttime,PUV.time_f <= endtime)).order_by(PUV.time_f).all()
        chart_data = []

        for i in datas:
            # print data.date_descri
            chart_data.append({'date':i.date_descri,'pv':i.pv,'pv_nospider':i.pv_nospider,'pv_nospider_m':i.pv_nospider_m,
                           'pv_nospider_p':i.pv_nospider_p,'uv':i.uv,'uv_m':i.uv_m,'uv_p':i.uv_p,'pv_uv':i.pv_uv,
                           'pv_u':i.pv_u,'pv_u_m':i.pv_u_m,'pv_u_p':i.pv_u_p,'pv_office':i.pv_office,'pv_office_m':i.pv_office_m,
                           'pv_office_p':i.pv_office_p,'pv_whitelist':i.pv_whitelist,'pv_whitelist_m':i.pv_whitelist_m,
                           'pv_whitelist_p':i.pv_whitelist_p,'request_time':int(i.request_time),'response_time':int(i.response_time)})

        return chart_data