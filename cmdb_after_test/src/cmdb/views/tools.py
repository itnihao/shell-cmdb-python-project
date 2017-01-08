# -*- coding: utf-8 -*-
from flask import Blueprint, render_template,request,redirect,url_for,flash,send_from_directory
from flask_login import login_required, current_user
from application import app,db
from models.ip_blacklist import IpBlacklist
from views.functions import responsejson
from datetime import datetime
from views.functions import visible
from models.pool import Pool
from models.host import Host
from models import Jobplat
from models.pool_host import PoolHost
from fabric.api import *
from sqlalchemy import and_
from fabric.state import output
from werkzeug.utils import secure_filename
import os
from models.pool import Pool
from pypages import Paginator
from config import DOMAIN
import re,commands,json,requests,pyhs2,datetime
from models import HostIp
from models import IpAddress
from work_permission.work_fun import *

env.user = 'root'
# env.password = ''
# env.key_filename = '/root/opt/Identity'
env.password = 'anjukeansible'
env.key_filename = '/root/.ssh/ansible_rsa'
env.warn_only = True
env.time_out = 100
env.skip_bad_hosts = True
env.abort_on_prompts = True
env.abort_exception = True
env.disable_known_hosts = True
env.colorize_errors = True

tools = Blueprint('tools', __name__)

class HiveClient:
    def __init__(self,db_host,user,database,password='',port=10000,authMechanism="PLAIN"):
        self.conn=pyhs2.connect(host=db_host,
                                port=port,
                                authMechanism=authMechanism,
                                user=user,
                                password=password,
                                database=database,
                                )

    def query(self,sql):
        with self.conn.cursor() as cursor:
            cursor.execute(sql)
            return cursor.fetch()

    def close(self):
        self.conn.close()


@tools.route("/jobplat",methods=['GET', 'POST'])
@login_required
def jobplat():
    workShow=getWorkShow()
    return render_template("tools/jobplat.html",workShow=workShow)

@tools.route("/jobplat/hostname/autocomplete", methods=['POST', 'GET'])
def hostname():
    q = request.form['q'] + '%'
    result = []
    hosts = Host.query.filter(Host.deleted == Host.DELETED_NO, Host.hostname.like(q)).limit(10).all()
    pools = Pool.query.filter(Pool.deleted == Pool.DELETED_NO, Pool.name.like(q)).limit(10).all()
    if hosts:
        for host in hosts:
            result.append([host.id, host.hostname, 1])
    if pools:
        for pool in pools:
            result.append([pool.id, pool.name, 2])
    return app.response_class(json.dumps(result), mimetype='application/json')


@tools.route("/jobplat/checkallow", methods=['POST', 'GET'])
def checkallow():
    code = 0
    msg = ""
    host_pool = request.form["host_pool"].strip()
    hosts_info  = Host.query.filter(Host.deleted == Host.DELETED_NO).all()
    pools_info = Pool.query.filter(Pool.deleted == Pool.DELETED_NO).all()
    hosts = []
    pools = []
    for item in hosts_info:
        hosts.append(item.hostname)
    for item in pools_info:
        pools.append(item.name)
    if host_pool not in hosts and host_pool not in pools:
        code = 1
        msg = "请选择提示的机器名或者pool"


    return responsejson(code,msg)

def wrap_run(run_func,host_list):
    ret = execute(run_func,hosts=host_list)
    return ret


@tools.route("/jobplat/runscripts",methods=['GET', 'POST'])
@login_required
def runscripts():
    url  = os.path.abspath('./templates/tools/jobplat/upload')
    if request.method == "GET":
        job_user = []
        job_user.append(int(Jobplat.RUN_ROOT))
        job_user.append(int(Jobplat.RUN_EVANS))
        workShow=getWorkShow()
        return render_template("tools/jobplat/runscripts.html",job_user=job_user,url=url,workShow=workShow)
    else:
        code = 0
        msg = ""
        data_r=json.loads(request.form['data'])
        run_user = data_r['run_user'].strip()
        job_name = data_r['job_name'].strip()
        upload_type = data_r['upload_type'].strip()
        script_type = data_r['script_type'].strip()
        script_name = data_r['script_name'].strip()
        script_content = data_r['script_content'].strip()
        input_list = data_r['input_list']
        host_list = []

        for h in input_list:

            host_list.append(h['ip'])

        # for item in input_list:
        #     item = eval(item)
        #     target_id = item['id']
        #     target_name = item['name']
        #     target_type = item['type']
        #     if int(target_type) == 2:
        #         info = db.session.query(Host,PoolHost,Host.hostname).filter(and_(PoolHost.pool_id == int(target_id),PoolHost.host_id == Host.id)).all()
        #         for hostname in info:
        #             ip_ss=db.session.query(HostIp,IpAddress,IpAddress.ipv4).filter(HostIp.host_id==int(hostname.id),HostIp.ip_address_id==IpAddress.id).first()
        #             if ip_ss:
        #                 host_list.append(ip_ss.ipv4)
        #             else:
        #                 host_list.append(hostname.hostname)
        #             # host_list.append(hostname.hostname)
        #     else:
        #         ip_s=db.session.query(HostIp,IpAddress,IpAddress.ipv4).filter(HostIp.host_id==int(target_id),HostIp.ip_address_id==IpAddress.id).first()
        #         if ip_s:
        #             host_list.append(ip_s.ipv4)
        #         else:
        #             host_list.append(target_name)



        def task_upload():
            # with settings(hide('running', 'stdout', 'stderr'), warn_only=True):
                local_dir = os.path.abspath('./templates/tools/jobplat/upload/%s'%script_name)
                remote_dir = '/tmp'
                return put(local_dir,remote_dir)

        def task_run():
            # with settings(hide('running', 'stdout', 'stderr'), warn_only=True):
                if int(script_type) == 1:
                    return run('/bin/bash /tmp/%s'%script_name)
                    return run('rm -rf /tmp/%s'%script_name)
                elif int(script_type) == 2:
                    return run('/usr/bin/python /tmp/%s'%script_name)
                    run('rm -rf /tmp/%s'%script_name)
                elif int(script_type) == 3:
                    return run('/usr/bin/perl /tmp/%s'%script_name)
                    return run('rm -rf /tmp/%s'%script_name)
        try:
        # for item in host_list:
            if int(upload_type) == 2:
                upload_ret = wrap_run(task_upload,host_list)
                run_ret = wrap_run(task_run,host_list)
            else:
                if int(script_type) == 1:
                    f = open(url + '/%s.sh'%job_name,'w')
                    script_name = "%s.sh"%job_name
                elif int(script_type) == 2:
                    f = open(url + '/%s.py'%job_name,'w')
                    script_name = "%s.py"%job_name
                elif int(script_type) == 3:
                    f = open(url + '/%s.pl'%job_name,'w')
                    script_name = "%s.pl"%job_name
                f.write(script_content)
                f.close()
                upload_ret = wrap_run(task_upload,host_list)
                run_ret = wrap_run(task_run,host_list)

            # upload = []
            # run1 = []
            upload = ''
            run1 = []

            issuccess_r=1
            for i in upload_ret:
                # upload.append({i:upload_ret[i]})
                # if(script_name not in upload_ret[i][0]):
                if (upload_ret[i]==False):
                    issuccess_r=1
                    # break
                else:
                    if not upload_ret[i].succeeded:
                       issuccess_r=2
                # upload=upload+"status:"+str(upload_ret[i].succeeded)+'\n'


            for j in run_ret:
                # run1.append({j:run_ret[j]})
                # if (run_ret[j] not in run1):
                if (run_ret[j]==False):
                    run_add={'info':'','host':'','success':0}
                    runx=''
                    runx+="host--------"+'\n'+j+'\n'
                    run_add['host']=j
                    runx=runx+'can not connect!'
                    run_add['info']=runx
                    run1.append(run_add)

                else:
                    if not (run_ret[j].succeeded):
                        issuccess_r=3
                    run_add={'info':'','host':'','success':0}
                    runx=''
                    runx+="host--------"+'\n'+j+'\n'
                    run_add['host']=j
                    runx=runx+"cmd--------"+'\n'+run_ret[j].command+"  in host "+j+":"+'\n'

                    runx=runx+"stdout-------"+'\n'+str(run_ret[j].stdout)+'\n'
                    if(run_ret[j].succeeded):
                        runx+='success!'+'\n'
                        run_add['success']=1
                    else:
                        runx+='failed!'+'\n'
                    runx+="===================="+'\n'
                    run_add['info']=runx
                    run1.append(run_add)
                    # run1 = run1.join("run "+run_ret[j].command+"  in host "+j+":" )
                    # run1 = run1.join("status:"+str(run_ret[j].succeeded))
                    # run1 = run1.join("stdout:"+str(run_ret[j].stdout))
                    # run1 = run1.join(run_ret[j])

            # print "==================="
            # print upload
            # print "--------------------"
            # print run1

            # data = [{'upload_message': upload, 'run_message': unicode( run1 , errors='ignore')}]
            data = [{'upload_message': upload, 'run_message': run1,'issuccess_r':issuccess_r}]


            target = Jobplat(job_name=job_name,upload_type=upload_type,script_name=script_name,script_type=script_type,script_content=script_content,target_type=1,target_id="",run_user=run_user,status=0)
            db.session.add(target)
            db.session.commit()

            return responsejson(code, msg, data)
        except Exception,e:
            print e.message

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in app.config['ALLOWED_EXTENSIONS']


@tools.route("/jobplat/runscripts/uploads",methods=['GET', 'POST'])
@login_required
def upload_file():
    filelist = []
    if request.method == 'POST':
        file = request.files['files[]']
        if file:
        #if file and allowed_file(file.filename):     #对上传文件进行格式过滤
            filename = secure_filename(file.filename)
            filelist.append(filename)
            url = os.path.abspath('./templates/tools/jobplat/upload/')
            file.save(os.path.join(url,filename))
#           return redirect(url_for('tools.uploaded_file',filename=filename))

    return filename

@tools.route("/jobplat/runscripts/uploads/<filename>")
@login_required
def uploaded_file(filename):
    url  = os.path.abspath('./templates/tools/jobplat/upload/')
    return send_from_directory(url,filename)


@tools.route("/jobplat/givefiles",methods=['GET', 'POST'])
@login_required
def givefiles():
    url  = os.path.abspath('./templates/tools/jobplat/upload')
    if request.method == 'GET':
        workShow=getWorkShow()
        return render_template("tools/jobplat/givefiles.html",workShow=workShow)
    else:
        code = 0
        msg = ""
        data_r=json.loads(request.form['data'])
        run_user = data_r['run_user'].strip()
        job_name = data_r['job_name'].strip()
        upload_type = data_r['upload_type'].strip()
        remote_dir = data_r['remote_dir'].strip()
        # limit_speed = data_r['limit_speed'].strip()
        file_list = data_r['filelist']
        filelist = json.dumps(file_list)
        input_list = data_r['input_list']

        remote_ip=data_r['remote_ip'].strip()
        remote_file=data_r['remote_file'].strip()


        host_list = []

        for h in input_list:
            host_list.append(h['ip'])

        # for item in input_list:
        #     item = eval(item)
        #     target_id = item['id']
        #     target_name = item['name']
        #     target_type = item['type']
        #     if int(target_type) == 2:
        #         info = db.session.query(Host,PoolHost,Host.hostname).filter(and_(PoolHost.pool_id == int(target_id),PoolHost.host_id == Host.id)).all()
        #         for hostname in info:
        #             ip_ss=db.session.query(HostIp,IpAddress,IpAddress.ipv4).filter(HostIp.host_id==int(hostname.id),HostIp.ip_address_id==IpAddress.id).first()
        #             if ip_ss:
        #                 host_list.append(ip_ss.ipv4)
        #             else:
        #                 host_list.append(hostname.hostname)
        #             # host_list.append(hostname.hostname)
        #     else:
        #         ip_s=db.session.query(HostIp,IpAddress,IpAddress.ipv4).filter(HostIp.host_id==int(target_id),HostIp.ip_address_id==IpAddress.id).first()
        #         if ip_s:
        #             host_list.append(ip_s.ipv4)
        #         else:
        #             host_list.append(target_name)

        # print "================"
        # print run_user,job_name,upload_type,remote_dir,limit_speed,filelist,host_list

        def task_upload1():
            r_info=[]
            for filename in file_list:
                if len(filename.split('\\'))>1:
                    filename=filename.split('\\')[-1]
                local_dir = os.path.abspath('%s/%s'%(url,filename))
                r_info.append(put(local_dir,remote_dir))
            return r_info

        def task_uplado2():
            filename=remote_file.split('/')[-1]
            local_dir = os.path.abspath('%s/%s'%(url,filename))
            return get(remote_file,local_dir)

        def task_uplado3():
            filename=remote_file.split('/')[-1]
            local_dir = os.path.abspath('%s/%s'%(url,filename))
            return put(local_dir,os.path.abspath('%s/%s'%(remote_dir,filename)))

        issuccess_r=1
        show_log=''
        if(upload_type=='2'):
            upload_ret=wrap_run(task_uplado2,[remote_ip])
            for u in upload_ret:
                if not upload_ret[u].succeeded:
                     issuccess_r=2
                     show_log+='download from '+remote_ip+'@'+remote_file+' failed'+'\n'
                else:
                    show_log+='download from '+remote_ip+'@'+remote_file+' success'+'\n'
            show_log+='======================'
            if (issuccess_r!=1):
                data={'issuccess_r': issuccess_r,'show_log':show_log}
                return responsejson(code, msg,data)
            upload_ret=wrap_run(task_uplado3,host_list)
            for u in upload_ret:
                show_log+='upload to '+u+'-------'+'\n'
                if not upload_ret[u].succeeded:
                     issuccess_r=2
                     show_log+='failed!'+'\n'
                else:
                     show_log+='success!'+'\n'

        # for item in host_list:
        else:
            upload_ret=wrap_run(task_upload1,host_list)

            for i in upload_ret:
                show_log+='upload to '+i+'-------'+'\n'
                for t in upload_ret[i]:
                    if not t.succeeded:
                        issuccess_r=2
                        show_log+='failed!'+'\n'
                    else:
                     show_log+='success!'+'\n'

            # upload.append({i:upload_ret[i]})
            # upload = upload.join(upload_ret[i])

        data={'issuccess_r': issuccess_r,'show_log':show_log}


        return responsejson(code, msg,data)

@tools.route("/blacklist",methods=['GET', 'POST'])
@login_required
def blacklist():
    show = visible({'push':'/cmdb/tools/blacklist/push_get'})
    ip_blacklist = IpBlacklist.query.filter(IpBlacklist.deleted == 0).all()
    lb10_idx = 1
    lb20_idx = 2
    ip_info = []
    ip_item = {'status':'active', 'type':'1', 'name':'LB-10', 'data':[]}
    ip_info.append(ip_item)
    ip_item = {'status':'','type':'2', 'name':'LB-20', 'data':[]}
    ip_info.append(ip_item)
    for item in ip_blacklist:
        tmp_info = {
            'id': item.id,
            'ip_address': item.ip_address,
            'type':item.type,
            'content':item.content,
            'created':item.created
        }
        if item.type == lb10_idx:
            ip_info[0]['data'].append(tmp_info)
        elif item.type == lb20_idx:
            ip_info[1]['data'].append(tmp_info)
    return render_template("tools/blacklist.html", ip_info=ip_info,show=show)


@tools.route("/blacklist/add",methods=['POST'])
@login_required
def blacklist_add():
    code = 0
    msg = "添加ip成功"
    if request.method == 'POST':
        ip = request.form['ip']
        lb = request.form['lb']
        content = request.form['content']
        if len(ip) <= 0:
            code = 1
            msg = "请填写需要屏蔽的ip或者ip段"
            return responsejson(code,msg)
        tmpip = ip.split(".")
        if len(tmpip) != 4:
            code = 1
            msg = "请填写有效的ip或者ip段"
            return responsejson(code, msg)
        intreg = re.compile('^\d*$')
        if not intreg.match(tmpip[0]) or int(tmpip[0]) < 0 or int(tmpip[0]) > 256:
            code = 1
            msg = "操作提示:第一段不对,请填写有效的ip或者ip段"
            return responsejson(code, msg)
        if not intreg.match(tmpip[1]) or int(tmpip[1]) < 0 or int(tmpip[1]) > 256:
            code = 1
            msg = "操作提示:第二段不对,请填写有效的ip或者ip段"
            return responsejson(code, msg)
        if not intreg.match(tmpip[2]) or int(tmpip[2]) < 0 or int(tmpip[2]) > 256:
            code = 1
            msg = "操作提示:第三段不对,请填写有效的ip或者ip段"
            return responsejson(code, msg)
        if '/' in ip:
            tmp = tmpip[3].split('/')
            if not intreg.match(tmp[0]) or int(tmp[0]) < 0 or int(tmp[0]) > 256 or not intreg.match(tmp[1]) or int(tmp[1]) < 0 or int(tmp[1]) > 32:
                code = 1
                msg = "操作提示:第四段不对,请填写有效的ip或者ip段"
                return responsejson(code, msg)
        else:
            if not intreg.match(tmpip[3]) or not tmpip[3] or int(tmpip[3]) < 0 or int(tmpip[3]) > 256:
                code = 1
                msg = "操作提示:第四段不对,请填写有效的ip或者ip段"
                return responsejson(code,msg)
        if len(lb) <= 0 or int(lb) <= 0:
            code = 1
            msg = "请选择需要生效的机器"
            return responsejson(code, msg)
        hasIn = IpBlacklist.query.filter(IpBlacklist.ip_address == ip).all()
        if hasIn:
            code = 1
            msg = "此ip已存在"
            return responsejson(code, msg)
        user_id = current_user.id
        iptarget = IpBlacklist(ip_address=ip, type=lb, content=content, user_id=user_id)
        db.session.add(iptarget)
        db.session.commit()
    else:
        code = 1
        msg = "添加ip失败"
    return responsejson(code, msg)


@tools.route("/blacklist/delete/<int:id>", methods=['POST'])
@login_required
def blacklist_delete(id):
    info = IpBlacklist.query.filter(IpBlacklist.id == id).first()
    if info:
        info.deleted = 1
        info.updated = datetime.now()
        db.session.commit()
        return responsejson(0, "删除机柜成功")


@tools.route("/blacklist/push", methods=['POST'])
@login_required
def blacklist_push():
    return

@tools.route("/lblog",methods=['POST','GET'])
@login_required
def lblog():
    if request.method == 'POST':
        # print request.form.keys
        starttime = request.form['starttime']
        endtime = request.form['endtime']
    return render_template("tools/lblog.html",flag='query')

def hive_custom_search(starttime,endtime):

    pass

@tools.route("/lbip",methods=['POST','GET'])
@login_required
def lbip():
    """
    hive_client=HiveClient(db_host='10.10.8.164',user='hdfs',database='alog')
    now=datetime.datetime.now()
    time=now.strftime("%Y-%m-%d %H:%M:%S")
    sql = 'select count(*) as count,remote_addr,sum(bytes_sent) from d_20150722 where hour=15 and min=30 group by remote_addr sort by count desc limit 20'
    result=hive_client.query(sql)
    result.sort()
    ret_data = []
    for i in result:
        ret_data.append({'ip':i[1],'count':i[0],'flow':i[2]})
    hive_client.close()

    """

    ret_data=[]
    ret_data.append({'ip':'114.80.230.212','count':14797,'flow':20})
    ret_data.append({'ip':'125.39.17.90','count':13326,'flow':30})
    ret_data.append({'ip':'114.80.230.211','count':11927,'flow':40})
    ret_data.append({'ip':'10.10.3.93','count':9855,'flow':25})
    ret_data.append({'ip':'10.10.3.92','count':9836,'flow':49})
    ret_data.append({'ip':'10.10.3.91','count':9746,'flow':78})
    ret_data.append({'ip':'211.151.3.6','count':7151,'flow':38})

    return render_template("tools/lbip.html",flag='ip',ret=ret_data)

@tools.route("/load_data",methods=['POST','GET'])
@login_required
def load_data():
    """
    hive_client=HiveClient(db_host='10.10.8.164',user='hdfs',database='alog')
    now=datetime.datetime.now()
    time=now.strftime("%Y-%m-%d %H:%M:%S")
    sql = 'select min, count(*),count(case when http_code>499  then http_code else null end ) as error_code_count,sum(bytes_sent/1024/1024/1024) as flow from d_%s%s%s where hour=%s group by min' \
    % (now.strftime("%Y"),now.strftime("%m"),now.strftime("%d"),now.strftime("%H"))
    result=hive_client.query(sql)
    result.sort()
    ret_data = []
    ret_data.append({'name':'querycount','data':[]})
    ret_data.append({'name':'errorcount','data':[]})
    ret_data.append({'name':'flow','data':[]})
    ret_categories = []
    count=0
    for i in result:
        prefix=now.strftime("%Y-%m-%d %H")
        ret_categories.append("%s:%s" % (prefix,i[0]))
        ret_data[0]['data'].append(float(i[1]))
        ret_data[1]['data'].append(float(i[2]))
        ret_data[2]['data'].append(float(i[3]))
        count+=1
    hive_client.close()
    step=count/5

    """
    count=0
    count_all=40

    ret_data = []
    ret_categories = []
    ret_data.append({'name':'querycount','data':[]})
    ret_data.append({'name':'errorcount','data':[]})
    ret_data.append({'name':'flow G','data':[]})
    now=datetime.datetime.now()
    while(count<count_all):
        prefix=now.strftime("%Y-%m-%d %H")
        ret_categories.append("%s:%s" % (prefix,count))
        ret_data[0]['data'].append(count)
        ret_data[1]['data'].append(count)
        ret_data[2]['data'].append(count)
        count+=1
    step=count_all/10


    colors = ["#00b9d9", "#f0ca4d"]
    msg="成功"
    title=['querycount','error code','flow (G)']
    resp_data = {
        'data':ret_data,
        'categories':ret_categories,
        'step':step,
        'title':title,
        'unit':1,
        'type':'spline',
        'colors':colors
    }
    response =  {'code':0,'data':resp_data,'msg':msg}
    return  app.response_class(json.dumps(response), mimetype='application/json')

@tools.route("/publish", methods=['POST','GET'])
@login_required
def publish():

    return render_template("tools/publish.html")

@tools.route("/check", methods=['POST','GET'])
@login_required
def check():
    if request.method == 'POST':
        value = request.form['value']
        if value in ['ga','beta']:
            msg = action_ga_beta(value)
        elif value == "api":
            allhosts = get_msg("http://ops.corp.anjuke.com/api/cmdb/host")
            hostinfo = get_msg("http://ops.corp.anjuke.com/api/cmdb/host/hostname:app10-001")
            allpools = get_msg("http://ops.corp.anjuke.com/api/cmdb/pool?random=1&access_token=2658243290a3858c332fac195766c4bc")
            pool_host = get_msg("http://ops.corp.anjuke.com/api/cmdb/pool/pool_id:1?random=1&access_token=2658243290a3858c332fac195766c4bc")
            user_email = get_msg("http://ops.corp.anjuke.com/api/user/hostname:app10-001")
            msg = allhosts+'\n'+hostinfo+'\n'+allpools+'\n'+pool_host+'\n'+user_email+'\n'
        else:
            return app.response_class(json.dumps("提交出错"), mimetype='application/json')
        return app.response_class(json.dumps(msg), mimetype='application/json')

def action_ga_beta(type):
    import time
    release_yw = int(time.strftime('%Y%W',time.localtime(time.time())))+1
    release_ga = '%s00'%release_yw
    release_ga = find_next_release(release_ga)
    return publish_release(release_ga, type)

def find_next_release(release):
    import os
    path = "/home/www/release/%s"%release
    if os.path.exists(path):
        return find_next_release(str(int(release)+1))
    else:
        return str(release)

def publish_release(release_num, release_type):
    cmd = [
        "cd /home/www/release",
        "git clone git@gitlab.corp.anjuke.com:_infra/cmdb.git %s"%release_num,
        "/bin/cp /home/www/config/src_config_%s.py /home/www/release/%s/src/cmdb/config.py"%(release_type,release_num),
        "mkdir /home/www/release/%s/src/cmdb/static/asset"%release_num,
        "mkdir /home/www/release/%s/src/cmdb/static/.webassets-cache"%release_num,
        "/bin/chmod -R 777 /home/www/release/%s/src/cmdb/static/asset"%release_num,
        "/bin/chmod -R 777 /home/www/release/%s/src/cmdb/static/.webassets-cache"%release_num,
        "/bin/echo '%s' > /home/www/config/RELEASE_VERSION_%s"%(release_num, release_type.upper())
    ]
    if release_type == "ga":
        cmd.append("/usr/bin/supervisorctl restart cmdb")
    else:
        cmd.append("/usr/bin/supervisorctl restart cmdb_branch")
    msg_cmd = "\r\n".join(cmd)
    msg =  commands.getstatusoutput(" && ".join(cmd))
    return '%s\r\n%s'%(msg_cmd,msg)

def get_msg(url):
    r = requests.get(url)
    msg = "status_code:"+str(r.status_code)+"   url:"+url
    return msg