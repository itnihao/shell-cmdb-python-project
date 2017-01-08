# -*- coding: utf-8 -*-
from application import app, db
from pynginxconfig import NginxConfig
from models.user import User
from models.host import Host
from models.host_ip import HostIp
from models.pool import Pool as modelpool
from models.pool_host import PoolHost
from views.host import _get_ip_id,_get_ip
from sqlalchemy import or_, and_
import hashlib , datetime , re ,getopt,sys
from views.pool import pool_add
from views.pool import get_pool_host_id,get_pool_id,_host_delete,modify_pool_host,_pooldelete,_check_host_pool


class Pool:
    def run(self):
        param= None
        opts, args = getopt.getopt(sys.argv[1:], "hm:p:")
        for op, mod in opts:
            if op == "-p":
                param = mod

        if param == "init":
            self.init()
        elif param == "build_search":
            self.build_search()
        elif param == "check":
            self.check_equ()
        elif param == "ratio":
            self.send_ratio()



    def init(self):
        filenames = ['ngx_conf_lb_external','ngx_conf_lb_internal','ngx_conf_lb20_external']
        #filenames = ['ngx_conf_lb_external']
        path = app.config.get('NGINX_PATH')
        nc = NginxConfig()
        pools = {}
        idx = 1
        i=0
        for item_filename in filenames:
            nc.loadf('%s%s/conf.d/upstream.config'%(path,item_filename))
            markdown_content = ''
            for data in nc.data:
                name = data['param']
                idx_name ='%s_%s'%(name,idx)
                if idx_name not in pools.keys():
                    pools[idx_name]={'name':name,'type':idx,'hosts':[]}
                #markdown_content +=name+'\n'
                for a in data['value']:
                    if a[0] == "server":
                        port = ""
                        weight = 1
                        host_id = 0
                        intreg=re.compile('\d+\.\d+\.\d+\.\d+')
                        tmp1 = a[1].split()[0]
                        server = tmp1.split(":")[0]
                        if not intreg.match(server):
                            name = server.split(".")[0]
                            info = Host.query.filter(Host.hostname == name).first()
                            server = '0'
                            if info:
                                server = _get_ip(info.primary_ip_id)
                        ip_id = _get_ip_id(server)
                        if ip_id:
                            hostname = '此ip(%s)无主机'%ip_id
                            hostipinfo = HostIp.query.filter(HostIp.ip_address_id==ip_id).first()
                            if hostipinfo:
                                hostinfo = Host.query.filter(and_(Host.id == hostipinfo.host_id,Host.deleted==Host.DELETED_NO)).first()
                                if hostinfo:
                                    hostname = hostinfo.hostname
                                    host_id = hostinfo.id

                        elif not intreg.match(server):
                            hostname = server.split(".")[0]
                        else:
                            hostname = "查不到此ip"
                        port = tmp1.split(":")[1]
                        if "weight" in a[1]:
                            tmp2 = a[1].split()[1]
                            weight = tmp2.split("=")[1]
                        tmp_content = '* %s   %s:%s   %s '%(hostname,server,port,weight)+'\n'
                        #markdown_content += markdown_content+tmp_content
                        pools[idx_name]['hosts'].append({
                            'id':host_id,
                            'host_name':hostname,
                            'weight':weight,
                            'port':port
                        })
                i+=1
            # f = file('%s%s.md'%(path,item_filename),'a')
            # f.write(markdown_content)
            # f.close()
            idx += 1
        if pools:#进行初始化插入数据库操作
            db.engine.execute("truncate table pool")
            db.engine.execute("truncate table pool_host")
            for idx_name in pools:
                poolinfo = pools[idx_name]
                name = poolinfo['name']
                type = poolinfo['type']
                pooltarget = modelpool(name.replace("upstream-",""),0,0,0,note='',content='',byname=name,source = type)
                db.session.add(pooltarget)
                db.session.commit()
                pool_id = pooltarget.id
                if poolinfo['hosts']:
                    for item_host in poolinfo['hosts']:
                        host_id = item_host['id']
                        poolhostinfo = PoolHost.query.filter(and_(PoolHost.pool_id == pool_id,PoolHost.host_id == host_id)).first()
                        if poolhostinfo:
                            print '-------------------------'
                            print pool_id
                            print host_id
                            print '-------------------------'
                        else:
                            pool_host_target = PoolHost(pool_id,host_id,weight=item_host['weight'],port=item_host['port'])
                            db.session.add(pool_host_target)
                            db.session.commit()


    def build_search(self):
        special_seg = '#@#'
        poollist = modelpool.query.filter(modelpool.deleted == modelpool.DELETED_NO).all()
        for item_pool in poollist:
            userids=[]
            userlist={}
            userids.append(item_pool.ops_owner)
            userids.append(item_pool.team_owner)
            userids.append(item_pool.biz_owner)
            if userids:
                userinfo=User.query.filter(User.id.in_(userids)).all()
                if userinfo:
                    for item in userinfo:
                        userlist['uid_%s'%item.id]=[item.cn_name,item.name]
            search_content = item_pool.name+special_seg+item_pool.content+special_seg
            tmpuser = userlist['uid_%s'%item_pool.ops_owner]
            search_content = search_content+tmpuser[0]+special_seg+tmpuser[1]+special_seg
            tmpuser = userlist['uid_%s'%item_pool.team_owner]
            search_content = search_content+tmpuser[0]+special_seg+tmpuser[1]+special_seg
            tmpuser = userlist['uid_%s'%item_pool.biz_owner]
            search_content = search_content+tmpuser[0]+special_seg+tmpuser[1]+special_seg
            item_pool.search = search_content
            db.session.commit()

    def check_equ(self):
        filenames = ['ngx_conf_lb_external','ngx_conf_lb_internal','ngx_conf_lb20_external']
        self.git_refresh(filenames)
        path = app.config.get('NGINX_PATH')
        nc = NginxConfig()
        pools = {}
        idx = 1
        i=0
        for item_filename in filenames:
            nc.loadf('%s%s/conf.d/upstream.config'%(path,item_filename))
            for data in nc.data:
                name = data['param']
                idx_name ='%s_%s'%(name,idx)
                if idx_name not in pools.keys():
                    pools[idx_name]={'name':name,'type':idx,'hosts':[]}
                for a in data['value']:
                    if a[0] == "server":
                        port = ""
                        weight = 1
                        host_id = 0
                        intreg=re.compile('\d+\.\d+\.\d+\.\d+')
                        tmp1 = a[1].split()[0]
                        server = tmp1.split(":")[0]
                        if not intreg.match(server):
                            name = server.split(".")[0]
                            info = Host.query.filter(Host.hostname == name).first()
                            server = '0'
                            if info:
                                server = _get_ip(info.primary_ip_id)
                        ip_id = _get_ip_id(server)
                        if ip_id:
                            hostname = '此ip(%s,%s)无主机'%(ip_id,server)
                            hostipinfo = HostIp.query.filter(HostIp.ip_address_id==ip_id).first()
                            if hostipinfo:
                                hostinfo = Host.query.filter(and_(Host.id == hostipinfo.host_id,Host.deleted==Host.DELETED_NO)).first()
                                if hostinfo:
                                    hostname = hostinfo.hostname
                                    host_id = hostinfo.id

                        elif not intreg.match(server):
                            hostname = server.split(".")[0]
                        else:
                            hostname = "查不到此ip"
                        port = tmp1.split(":")[1]
                        if "weight" in a[1]:
                            tmp2 = a[1].split()[1]
                            weight = tmp2.split("=")[1]
                        pools[idx_name]['hosts'].append({
                            'id':host_id,
                            'host_name':hostname,
                            'weight':weight,
                            'port':port
                        })
                i+=1
            idx += 1
        nginx_pools = pools
        cmdb_pools = {}
        pool_list = modelpool.query.filter(and_(modelpool.source>0,modelpool.deleted == modelpool.DELETED_NO)).all()
        if pool_list:
            for pool_item in pool_list:
                idx_name ='%s_%s'%(pool_item.byname,pool_item.source)
                if idx_name not in cmdb_pools.keys():
                    cmdb_pools[idx_name]={'name':pool_item.byname,'type':pool_item.source,'hosts':[]}
                pool_hosts = PoolHost.query.filter(PoolHost.pool_id == pool_item.id).all()
                if pool_hosts:#以CMDB的数据为基准,进行对比
                    for item_pool_host in pool_hosts:
                        host_id = item_pool_host.host_id
                        hostinfo = Host.query.filter(Host.id == host_id).first()
                        if hostinfo:
                            cmdb_pools[idx_name]['hosts'].append({
                                'id':host_id,
                                'host_name':hostinfo.hostname,
                                'weight':item_pool_host.weight,
                                'port':item_pool_host.port
                            })
                        else:
                            print '------Host_ID:%s------'%host_id
        print '-----start compare--------'
        mail_messages = {
            'add':[],
            'mod':[],
            'delete':[]
        }
        #先以nginx为基准，对比
        if nginx_pools:
            for nginx_item_name,nginx_item_val in nginx_pools.items():
                tmp_name = nginx_item_val['name']
                if nginx_item_name in cmdb_pools:
                    tmp_mail_item = {
                        'name':tmp_name.replace("upstream-",""),
                        'byname':tmp_name,
                        'source':nginx_item_val['type'],
                        'tips':[]
                    }
                    tmp_cmdb_hosts = {}
                    tmp_nginx_hosts = {}
                    for tmp_host in nginx_item_val['hosts']:
                        tmp_nginx_key = 'host_%s_%s'%(tmp_host['id'],tmp_host['port'])
                        tmp_nginx_hosts[tmp_nginx_key] = [tmp_host['weight'],tmp_host['port'],tmp_host['id'],tmp_host['host_name']]
                    for tmp_host in cmdb_pools[nginx_item_name]['hosts']:
                        tmp_cmdb_key = 'host_%s_%s'%(tmp_host['id'],tmp_host['port'])
                        tmp_cmdb_hosts[tmp_cmdb_key] = [tmp_host['weight'],tmp_host['port'],tmp_host['id'],tmp_host['host_name']]

                    for tmp_host_key,tmp_host_val in tmp_nginx_hosts.items():
                        if tmp_cmdb_hosts.has_key(tmp_host_key):
                            if str(tmp_host_val[1]) != str(tmp_cmdb_hosts[tmp_host_key][1]) or str(tmp_host_val[0]) != str(tmp_cmdb_hosts[tmp_host_key][0]):
                                tmp_host_info = {'act':'mod','id':tmp_host_val[2],'hostname':tmp_host_val[3],'weight_old':tmp_cmdb_hosts[tmp_host_key][0],'weight_new':tmp_host_val[0],'port_old':tmp_cmdb_hosts[tmp_host_key][1],'port_new':tmp_host_val[1]}
                                tmp_mail_item['tips'].append(tmp_host_info)
                        else:
                            if tmp_host_val[2] != 0:
                                tmp_host_info = {'act':'add','id':tmp_host_val[2],'hostname':tmp_host_val[3],'weight_old':0,'weight_new':tmp_host_val[0],'port_old':0,'port_new':tmp_host_val[1]}
                                tmp_mail_item['tips'].append(tmp_host_info)
                            else:
                                tmp_host_info = {'act':'default','id':0,'hostname':'nginx中有但cmdb中没有此主机','weight_old':0,'weight_new':0,'port_old':0,'port_new':0}
                                tmp_mail_item['tips'].append(tmp_host_info)

                    for tmp_host_key,tmp_host_val in tmp_cmdb_hosts.items():
                        if tmp_nginx_hosts.has_key(tmp_host_key):
                            pass
                        else:
                            tmp_host_info = {'act':'delete','id':tmp_host_val[2],'hostname':tmp_host_val[3],'weight_old':0,'weight_new':0,'port_old':0,'port_new':0}
                            tmp_mail_item['tips'].append(tmp_host_info)
                    if len(tmp_mail_item['tips'])>0:
                        mail_messages['mod'].append(tmp_mail_item)
                else:
                    tmp_mail_item = {
                        'name':tmp_name.replace("upstream-",""),
                        'byname':tmp_name,
                        'source':nginx_item_val['type'],
                        'tips':[]
                    }
                    for tmp_host in nginx_item_val['hosts']:
                        tmp_host_info = {'act':'add','id':tmp_host['id'],'hostname':tmp_host['host_name'],'weight_old':0,'weight_new':tmp_host['weight'],'port_old':0,'port_new':tmp_host['port']}
                        tmp_mail_item['tips'].append(tmp_host_info)
                    if len(tmp_mail_item['tips'])>0:
                        mail_messages['add'].append(tmp_mail_item)

        #以CMDB为基准，对比
        if cmdb_pools:
            for cmdb_item_name,cmdb_item_val in cmdb_pools.items():
                tmp_name = cmdb_item_val['name']
                if cmdb_item_name not in nginx_pools:
                    tmp_mail_item = {
                        'name':tmp_name.replace("upstream-",""),
                        'byname':tmp_name,
                        'source':cmdb_item_val['type'],
                        'tips':[]
                    }
                    for host_info in  cmdb_item_val['hosts']:
                        tmp_host_info = {'act':'delete','id':host_info['id'],'hostname':host_info['host_name'],'weight_old':0,'weight_new':0,'port_old':0,'port_new':0}
                        tmp_mail_item['tips'].append(tmp_host_info)
                    if len(tmp_mail_item['tips'])>0:
                        mail_messages['delete'].append(tmp_mail_item)
        head = ['POOL名称','POOL昵称','来源','操作','描述']
        bodys = []
        if len(mail_messages['add']) > 0:#新增加pool
            for item in mail_messages['add']:
                ret = pool_add( data = {'name':item['name'],'byname':item['byname'],'source':item['source']},type = 0)
                tmp_body = [item['name'],item['byname'],self.source_desc(item['source']),'新增','']
                if ret['code'] == 0: #开始添加主机了
                    for host_item in item['tips']:
                        if host_item['act'] == "add":
                            modify_pool_host({'pool_name':item['name'],'weight':host_item['weight_new'],'port':host_item['port_new'],'host_id':host_item['id'],'source':item['source']},2)
                            tmp_body[4] += "增加主机(ID:%s,Hostname:%s,weight:%s,port:%s)<br/>"%(host_item['id'],host_item['hostname'],host_item['weight_new'],host_item['port_new'])
                else:
                    tmp_body[4] = "新增POOL失败"
                bodys.append(tmp_body)

        if len(mail_messages['mod']) > 0:#修改pool
            for item in mail_messages['mod']:
                tmp_body = [item['name'],item['byname'],self.source_desc(item['source']),'修改','']
                for host_item in item['tips']:
                    if host_item['act'] == "mod":
                        modify_pool_host({'pool_name':item['name'],'weight':host_item['weight_new'],'port':host_item['port_new'],'host_id':host_item['id'],'source':item['source']},1)
                        tmp_body[4] += "修改主机(ID:%s,Hostname:%s)(weight:%s=>%s,port:%s=>%s)<br/>"%(host_item['id'],host_item['hostname'],host_item['weight_old'],host_item['weight_new'],host_item['port_old'],host_item['port_new'])
                    elif host_item['act'] == "add":
                        modify_pool_host({'pool_name':item['name'],'weight':host_item['weight_new'],'port':host_item['port_new'],'host_id':host_item['id'],'source':item['source']},2)
                        tmp_body[4] += "增加主机(ID:%s,Hostname:%s,weight:%s,port:%s)<br/>"%(host_item['id'],host_item['hostname'],host_item['weight_new'],host_item['port_new'])
                    elif host_item['act'] == "delete":
                        pool_id =  get_pool_id(item['name'],item['source'])
                        host_id =  host_item['id']
                        pool_host_id = get_pool_host_id(pool_id,host_id)
                        ret = _check_host_pool({'hostid':host_id,'poolid':pool_id})
                        if ret['code'] == 1:
                            _host_delete({'id':pool_host_id,'pool_id':pool_id})
                            tmp_body[4] += "删除主机(ID:%s,Hostname:%s)<br/>"%(host_item['id'],host_item['hostname'])
                        else:
                            tmp_msg = "删除主机(ID:%s,Hostname:%s),失败:只在一个POOL<br/>"%(host_item['id'],host_item['hostname'])
                            tmp_body[4] += self.wrap_msg(color = 'red',msg = tmp_msg )
                bodys.append(tmp_body)


        if len(mail_messages['delete']) > 0: #删除pool
            for item in mail_messages['delete']:
                tmp_body = [item['name'],item['byname'],self.source_desc(item['source']),'删除','']
                flag = 0
                pool_id =  get_pool_id(item['name'],item['source'])
                for host_item in item['tips']:
                    if host_item['act'] == "delete":
                        host_id =  host_item['id']
                        pool_host_id = get_pool_host_id(pool_id,host_id)
                        ret = _check_host_pool({'hostid':host_id,'poolid':pool_id})
                        if ret['code'] == 1:
                            _host_delete({'id':pool_host_id,'pool_id':pool_id})
                            tmp_body[4] += "删除主机(ID:%s,Hostname:%s)<br/>"%(host_item['id'],host_item['hostname'])
                        else:
                            flag += 1
                            tmp_msg = "删除主机(ID:%s,Hostname:%s),失败:只在一个POOL<br/>"%(host_item['id'],host_item['hostname'])
                            tmp_body[4] += self.wrap_msg(color = 'red',msg = tmp_msg )

                if flag == 0:
                    _pooldelete(pool_id)
                    tmp_body[4] = "%s%s"%("删除POOL成功<br/>",tmp_body[4])
                else:
                    tmp_body[4] = "%s%s"%("删除POOL失败<br/>",tmp_body[4])

        print '---------开始发邮件-------------'
        if len(bodys) > 0:
            from views.functions import addmail
            from flask import render_template
            import datetime
            subject = "[POOL核对]%s核对结果"%datetime.datetime.now().strftime("%Y-%m-%d")
            receiver = app.config.get("MAIL_TO")['ops_email']
            content = render_template('jobs/ratio.html',head = head,bodys = bodys,avghead = [],avgbodys = [])
            addmail(receiver, subject, content)
        else:
            print '没有改动'
        print('-------邮件发送结束------')

    def git_refresh(self,filenames):
        print '---------start  git refresh-----------'
        import os, commands
        path = app.config.get('NGINX_PATH')
        for item_filename in filenames:
            tmp_path = "%s%s"%(path,item_filename)
            command = "cd %s;git fetch --all;git rebase origin/master"%tmp_path
            print '------------------------'
            print command
            status , msg = commands.getstatusoutput(command)
            print msg
            if 'CONFLICT' in msg:
                git_repo_url = "git@gitlab.corp.anjuke.com:_infra/%s.git"%(item_filename)
                command = "cd %s;rm -rf %s;git clone %s"%(path,item_filename,git_repo_url)
                print command
                status , msg = commands.getstatusoutput(command)
                print msg

        print '---------end  git refresh-----------'


    def send_ratio(self):
        from flask import render_template
        from models.pool import Pool
        from views.functions import addmail

        Job_poolids = [181,177,159,143]
        DB_poolids = [148]
        Job_poolnum = 0
        DB_poolnum = 0
        Web_poolnum = 0
        predays = 7
        ratios =  self.calPoolRatio(predays)
        pool_lists = Pool.query.filter(Pool.deleted == Pool.DELETED_NO).all()
        head = ['POOL名称','来源']
        avghead = ['POOL名称']
        avgjob = {}
        avgdb = {}
        avgweb = {}
        tmp_avg_dt = []
        for i in range(predays,0,-1):
            dt = datetime.date.today() - datetime.timedelta(days=(i))
            dt = dt.strftime('%Y-%m-%d')
            head.append(dt)
            avghead.append(dt)
            tmp_avg_dt.append(dt)
            avgjob[dt] = 0
            avgdb[dt] = 0
            avgweb[dt] = 0

        head.append('%s天平均'%predays)

        bodys = []
        avgbodys = []

        for item_pool in pool_lists:
            item_tr = []
            tmp_pool_id = item_pool.id
            item_tr.append(item_pool.name)
            item_tr.append(item_pool.source_desc)
            tmp_total = 0
            for i in range(predays,0,-1):
                tmp_ratio = 0
                dt = datetime.date.today() - datetime.timedelta(days=(i))
                dt = dt.strftime('%Y-%m-%d')
                if tmp_pool_id in ratios:
                    if dt in ratios[tmp_pool_id]:
                        tmp_ratio = ratios[tmp_pool_id][dt]
                        item_tr.append(int(float(tmp_ratio)*100))
                    else:
                        item_tr.append('未知')
                else:
                    item_tr.append('未知')
                if tmp_pool_id in Job_poolids:
                    avgjob[dt] += tmp_ratio
                elif tmp_pool_id in DB_poolids:
                    avgdb[dt] += tmp_ratio
                elif item_pool.source >0:
                    avgweb[dt] += tmp_ratio

                tmp_total += tmp_ratio

            if tmp_pool_id in Job_poolids:
                Job_poolnum += 1
            elif tmp_pool_id in DB_poolids:
                DB_poolnum += 1
            elif item_pool.source >0:
                Web_poolnum += 1

            tmp_pool_avg = int(float('%.2f'%(tmp_total/predays))*100)
            item_tr.append('%d'%tmp_pool_avg)

            bodys.append(item_tr)

        tmpbody = []
        tmpbody.append("Job")
        for tmp_dt in tmp_avg_dt:
            tmp_ratio = avgjob[tmp_dt]
            tmpbody.append(int(float('%.2f'%(tmp_ratio/Job_poolnum))*100))
        avgbodys.append(tmpbody)

        tmpbody = []
        tmpbody.append("Web")
        for tmp_dt in tmp_avg_dt:
            tmp_ratio = avgweb[tmp_dt]
            tmpbody.append(int(float('%.2f'%(tmp_ratio/Web_poolnum))*100))

        avgbodys.append(tmpbody)

        tmpbody = []
        tmpbody.append("DB")
        for tmp_dt in tmp_avg_dt:
            tmp_ratio = avgdb[tmp_dt]
            tmpbody.append(int(float('%.2f'%(tmp_ratio/DB_poolnum))*100))

        avgbodys.append(tmpbody)

        mail_content = render_template('jobs/ratio.html',head = head,bodys = bodys,avghead = avghead,avgbodys = avgbodys)

        email = app.config.get("MAIL_TO")['ops_email']
        subject = "满载率报表"
        addmail(email, subject, mail_content)

    def calPoolRatio(self,pre_days):
        from models.pool_load_daily import PoolLoadDaily
        end_date = datetime.date.today() - datetime.timedelta(days=1)
        from_date = datetime.date.today() - datetime.timedelta(days=(pre_days))
        end_date = '%s 00:00:00'%end_date
        from_date = '%s 00:00:00'%from_date
        pool_loads_list = PoolLoadDaily.query.filter(PoolLoadDaily.created.between(from_date,end_date)).all()
        pool_loads_dic = {}
        for item in  pool_loads_list:
            tmp_pool_id = item.pool_id
            if tmp_pool_id not in pool_loads_dic:
                pool_loads_dic[tmp_pool_id] = {}

            pool_loads_dic[tmp_pool_id][item.created.strftime('%Y-%m-%d')] = item.ratio

        return pool_loads_dic

    def source_desc(self,source):
        desc = ''
        if source == 1:
            desc = "LB10(外部)"
        elif source == 2:
            desc = "LB10(内部)"
        elif source == 3:
            desc = "LB20(外部)"
        return desc

    def wrap_msg(self,color = 'red',msg = ''):
        return "<fonts color='%s'>%s</fonts>"%(color,msg)
