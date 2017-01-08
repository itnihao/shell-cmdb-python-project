# -*- coding: utf-8 -*-

from django.shortcuts import render
from django.http import HttpResponse
from django.core import serializers
from models import *
from apps.server_device import models as server_models
from apps.auth import models as auth_models
from public.APIViews import CoreView
from public.Exceptions import APIError
from public.Check import CheckParameters
from public.Syskeywords import db_code_mapping
import json
from datetime import datetime
from django.db.models import Q

import sys
reload(sys)
sys.setdefaultencoding('utf8')


class Cluster(CoreView):

    @CheckParameters(['token','q','busline','page_limit'])
    def post_list(self):
        """获取业务线对应集群列表"""
        q = self.parameters('q')
        busline = self.parameters('busline')
        page_limit = self.parameters('page_limit')
        if q is None:
            q = ''
        objs = TCluster.objects.filter(cluster_name__contains=q).order_by('cluster_id')[0:page_limit]
        vals = []
        for obj in objs:
            val = {'id':obj.cluster_id, 'text':obj.cluster_name}
            vals.append(val)
        return vals

    def get_adduser(self):
        cluster_user_id = self.create_id()
        user_name = self.parameters('user_name')
        cluster_id = self.parameters('cluster_id')
        is_admin = self.parameters('is_admin')
        op = self.parameters('op')
        kwargs = {'cluster_user_id':cluster_user_id, 'bsp_user_id':user_name, 'cluster_id':cluster_id, 'op_type':op, 'is_admin':is_admin}
        obj = TClusterUser(**kwargs)
        obj.save()

        return {'id':obj.cluster_user_id, 'name':obj.bsp_user_id}

    def get_addbusline(self):
        cluster_busline_id = self.create_id()
        cluster_id = self.parameters('cluster_id')
        busline_id = self.parameters('busline_id')

        kwargs = {'cluster_busline_id':cluster_busline_id, 'cluster_id':cluster_id, 'busline_id':busline_id}
        obj = TClusterBusline(**kwargs)
        obj.save()
        return {'id':obj.cluster_busline_id}

    def get_del(self):
        cluster_id = self.parameters('id')
        obj = TCluster.objects.get(cluster_id=cluster_id).delete()
        return {'id': cluster_id}


    def get_delbusline(self):
        cluster_busline_id = self.parameters('id')
        obj = TClusterBusline.objects.get(cluster_busline_id=cluster_busline_id).delete()
        return {'id':obj.cluster_busline_id}


    def get_add(self):
        cluster_name = str(self.parameters('cluster_name'))
        deploy_path = str(self.parameters('cluster_path'))
        cluster_id = self.create_id()
        cluster_type = 0;
        kwargs = {'cluster_id':cluster_id, 'deploy_path':deploy_path, 'cluster_name':cluster_name, 'cluster_type':cluster_type}
        obj = TCluster(**kwargs)
        obj.save()
        return {'id':obj.cluster_id, 'name': obj.cluster_name}

    def get_search(self):
        val =  self.parameters('value')
        objs = TCluster.objects.filter(cluster_name__contains=val).order_by('cluster_name')
        return serializers.serialize("json", objs)

    def post_savecluster(self):
        cluster_id = self.parameters('cluster_id')
        cluster_name = self.parameters('cluster_name')
        busline_id = self.parameters('busline_id')
        cluster_state = self.parameters('cluster_state')
        cluster_code = self.parameters('cluster_code')
        op_owner_id = self.parameters('op_owner')
        busline_owner_id = self.parameters('busline_owner')

        print cluster_name

        if not cluster_id:
            cluster_id = self.create_id()

        # print busline_owner_id
        # print cluster_id
        # print cluster_name
        # print busline_id
        # print int(cluster_state)
        # defaults_kwargs = {'cluster_id':cluster_id}
        # print defaults_kwargs

        try:
            cluster = TCluster.objects.filter(cluster_id=cluster_id)
            # print cluster
            if cluster.count()>0:
                # print 'qqqqqqqqq'
                cluster = cluster[0]
            else:
                b_o = TBspUser.objects.get(bsp_user_id=busline_owner_id)
                o_o = TBspUser.objects.get(bsp_user_id=op_owner_id)
                cluster = TCluster.objects.create(cluster_name=cluster_name,cluster_id=cluster_id,cluster_state=int(cluster_state),cluster_code=cluster_code,busline_owner=b_o,op_owner=o_o)
            # print cluster
            # print busline_id
            busline = TBusline.objects.get(busline_id=busline_id)
            # print busline
            # op_owner = TBspUser.objects.get(bsp_user_id=op_owner_id)
            # busline_owner = TBspUser.objects.get(bsp_user_id=busline_owner_id)
            # cluster.cluster_name = cluster_name
            cluster.busline_id = busline
            # cluster.busline_owner = busline_owner
            # cluster.op_owner = op_owner
            if not cluster.create_time:
                cluster.create_time = datetime.now()
            cluster.update_time = datetime.now()
            # print cluster_state
            cluster.cluster_state = int(cluster_state)
            cluster.cluster_code = cluster_code
            cluster.save();
            return True

        except Exception as e:
            return False;


    def post_getcluster(self):
        start = self.parameters('startnum')
        step = self.parameters('range')

        if not start:
            start = 0;
        if not step:
            step = 10;
        endnum = start+step

        clusters = TCluster.objects.all().order_by('-cluster_id')[start:endnum]
        print 'aaaaaaaaaaaaaaaaaaaa'
        print clusters
        print 'aaaaaaaaaaaaaaaaaaaa'
        data = []
        for obj in clusters:
            busline_owner = TBspUser.objects.get(bsp_user_id=obj.busline_owner_id)
            op_owner = TBspUser.objects.get(bsp_user_id=obj.op_owner_id)
            dic = {

                'cluster_id': obj.cluster_id,
                'cluster_name': obj.cluster_name,
                'cluster_code': obj.cluster_code,
                'busline_id': obj.busline_id.busline_id,
                'busline_owner': busline_owner.nickname,
                'op_owner': op_owner.nickname,
                'create_time': datetime.strftime(obj.create_time,'%Y-%m-%d'),
                'update_time': datetime.strftime(obj.update_time,'%Y-%m-%d'),
                'cluster_state': obj.cluster_state

            }
            data.append(dic)
        return data

    def post_getcurrentcluster(self):
        clusterid = self.parameters('clusterid')
        clusters = TCluster.objects.filter(cluster_id=clusterid)
        # print clusters
        data = []
        for obj in clusters:
            busline_owner = TBspUser.objects.get(bsp_user_id=obj.busline_owner_id)
            op_owner = TBspUser.objects.get(bsp_user_id=obj.op_owner_id)

            dic = {

                'cluster_id': obj.cluster_id,
                'cluster_name': obj.cluster_name,
                'busline_id': obj.busline_id.busline_id,
                'busline_name':obj.busline_id.busline_name,
                'busline_owner': busline_owner.nickname,
                'op_owner': op_owner.nickname,
                'cluster_code': obj.cluster_code,
                'create_time': datetime.strftime(obj.create_time,'%Y-%m-%d'),
                'update_time': datetime.strftime(obj.update_time,'%Y-%m-%d'),
                'cluster_state': obj.cluster_state

            }
            data.append(dic)
        # print data
        return data

    def post_clustersearchwithbusline(self):
        name = self.parameters('name')
        buslinename = self.parameters('busline')
        start = self.parameters('startnum')
        step = self.parameters('range')
        # print name,buslinename
        if not start:
            start = 0;
        if not step:
            step = 10;
        endnum = start+step

        cluster = [];
        if name or buslinename:
            if name and buslinename:
                busline = TBusline.objects.filter(busline_name__contains=buslinename)
                buslineid = [];
                if busline:
                    for obj in busline:
                        buslineid.append(obj.busline_id)
                    print buslineid
                cluster = TCluster.objects.filter(Q(cluster_code__contains=name)|Q(busline_id__in=buslineid)).order_by('-cluster_id')
            elif name:
                cluster = TCluster.objects.filter(cluster_code__contains=name).order_by('-cluster_id')
            elif buslinename:
                busline = TBusline.objects.filter(busline_name__contains=buslinename)
                buslineid = [];
                if busline:
                    for obj in busline:
                        buslineid.append(obj.busline_id)
                    print buslineid
                cluster = TCluster.objects.filter(busline_id__in=buslineid).order_by('-cluster_id')
        else:
            cluster = TCluster.objects.all().order_by('-cluster_id')

        # print cluster
        data = []
        data_count = cluster.count()
        for obj in cluster[start:endnum]:
            dic = {
                'data_count': data_count,
                'cluster_id': obj.cluster_id,
                'cluster_name': obj.cluster_name,
                'cluster_code': obj.cluster_code,
                # 'busline_id': obj.busline_id.busline_id,
                # 'busline_name':obj.busline_id.busline_name,
                # 'busline_owner': busline_owner.nickname,
                # 'op_owner': op_owner.nickname,
                'create_time': datetime.strftime(obj.create_time,'%Y-%m-%d'),
                'update_time': datetime.strftime(obj.update_time,'%Y-%m-%d'),
                'cluster_state': obj.cluster_state
            }

            busline = TBusline.objects.filter(busline_id=int(obj.busline_id_id))
            if busline:
                busline = busline[0]
                dic['busline_id'] = obj.busline_id.busline_id
                dic['busline_name'] = obj.busline_id.busline_name
            else:
                dic['busline_id'] = '未设置'
                dic['busline_name'] = '未设置'

            busline_owner = TBspUser.objects.filter(bsp_user_id=obj.busline_owner_id)
            if busline_owner:
                busline_owner = busline_owner[0]
                dic['busline_owner'] = busline_owner.nickname
            else:
                dic['busline_owner'] = '未设置'


            op_owner = TBspUser.objects.filter(bsp_user_id=obj.op_owner_id)
            if op_owner:
                op_owner = op_owner[0]
                dic['op_owner'] = op_owner.nickname
            else:
                dic['op_owner'] = '未设置'

            # print dic
            data.append(dic)
        return data

    def post_getclusteruser(self):
        # print 'aaaaaaaaaa'
        cluster_id = self.parameters('id')
        # print cluster_id
        clusterUser = TClusterUser.objects.filter(cluster_id=cluster_id)
        # print clusterUser
        data = []
        for obj in clusterUser:
            dic = {
                'cluster_user_id': obj.cluster_user_id,
                'cluster_name': obj.cluster.cluster_name,
                'cluster_id': obj.cluster.cluster_id,
                'bsp_user_name': obj.bsp_user.nickname,
                'bsp_user_account': obj.bsp_user.account,
                'bsp_user_id': obj.bsp_user.bsp_user_id,
                'role': obj.role,
                'state': obj.state,
                'add_time': datetime.strftime(obj.add_time,'%Y-%m-%d'),
                # 'effect_time':datetime.strftime(obj.start_time,'%Y-%m-%d'),
                # 'disabled_time':datetime.strftime(obj.end_time,'%Y-%m-%d'),
                }

            if obj.start_time:
                dic['effect_time'] = datetime.strftime(obj.start_time,'%Y-%m-%d')
            else:
                dic['effect_time'] = '未设置'

            if obj.end_time:
                dic['disabled_time'] = datetime.strftime(obj.end_time,'%Y-%m-%d')
            else:
                dic['disabled_time'] = '未设置'

            if obj.operation_user:
                dic['operation_user'] = obj.operation_user.nickname
            else:
                dic['operation_user'] = '未配置'

            if int(obj.role) == 0:
                dic['role_name'] = 'Root'
            elif int(obj.role) == 1:
                dic['role_name'] = 'Work'
            elif int(obj.role) == 2:
                dic['role_name'] = 'Readonly'
            else:
                dic['role_name'] = 'Default'
            data.append(dic)
            # print dic
        return data

    def post_clustersearchresult(self):
        clustername = self.parameters('searchCode')
        cluster = TCluster.objects.filter(cluster_name__startswith=clustername)
        data = []
        for obj in cluster:
            dic = {
                'cluster_name': obj.cluster_name,
                'cluster_id': obj.cluster_id
                }
            data.append(dic)
        return data

    def post_getclusterdata(self):
        cluster = TCluster.objects.all()
        data = []
        for obj in cluster:
            dic = {
                'cluster_name': obj.cluster_name,
                'cluster_id': obj.cluster_id
                }
            data.append(dic)
        return data

    def post_getuserdata(self):
        uname = self.parameters('uname')
        # print uname
        user = TBspUser.objects.filter(nickname__contains=uname)
        data = []
        for obj in user:
            dic = {
                'text': obj.nickname + ' : ' + '(' + obj.account + ')',
                'id': obj.bsp_user_id
                }
            data.append(dic)
        return data

    def post_saveclusteruserchange(self):
        clusteruserid = self.parameters('clusteruserid')
        clusterid = self.parameters('clusterid')
        role = self.parameters('role')
        # print clusterid
        clusterusers = TClusterUser.objects.filter(cluster_user_id=clusteruserid)
        if clusterusers.count()>0:
            # 有此条数据
            clusteruser = clusterusers[0]
            clusteruser.role = role
            cluster = TCluster.objects.get(cluster_id=clusterid)
            clusteruser.cluster = cluster
            clusteruser.add_time = datetime.now()
            clusteruser.save()

    def post_savenewclusteruser(self):
        clusteruserid = self.parameters('clusteruserid')
        clusterid = self.parameters('clusterid')
        role = self.parameters('role')
        userid = self.parameters('userid')
        startDate = self.parameters('startDate')
        endDate = self.parameters('endDate')
        op_user_name = self.parameters('operation_user')

        print startDate
        print endDate
        # print role
        clusteruser = TClusterUser.objects.create(cluster_user_id=self.create_id(),role=int(role),state=int('0'),add_time=datetime.now())
        cluster = TCluster.objects.filter(cluster_id=clusterid)
        if cluster:
            cluster = cluster[0]
            clusteruser.cluster = cluster
        bspuser = TBspUser.objects.filter(bsp_user_id=userid)
        if bspuser:
            bspuser = bspuser[0]
            clusteruser.bsp_user = bspuser
        op_user = TBspUser.objects.filter(account=op_user_name)
        if op_user:
            op_user = op_user[0]
            clusteruser.operation_user = op_user

        clusteruser.add_time = datetime.now()
        clusteruser.state = 0
        clusteruser.start_time=datetime.strptime(startDate,'%Y-%m-%d')
        clusteruser.end_time=datetime.strptime(endDate,'%Y-%m-%d')
        clusteruser.save()
        return True
        # try:
        #
        # except Exception as e:
        #     raise APIError(-3000)
        #     return False

    def post_getclusterusercluster(self):
        id = self.parameters('id')
        clusteruser = TClusterUser.objects.get(cluster_user_id=id)
        data = []
        dic = {
            'cluster_user_id':clusteruser.cluster_user_id,
            'clustername':clusteruser.cluster.cluster_name,
            'bsp_user_name':clusteruser.bsp_user.nickname,
            'role':clusteruser.role,
            'state':clusteruser.state
        }
        data.append(dic)
        return data

    def post_getbspuser(self):
        start = self.parameters('startnum')
        step = self.parameters('range')

        if not start:
            start = 0;
        if not step:
            step = 10;
        endnum = start+step

        bspusers = TBspUser.objects.all()[start:endnum]
        data = []
        for obj in bspusers:

            dic = {
                'id':obj.bsp_user_id,
                'text':obj.nickname,
                'name':obj.nickname,
                'account':obj.account,
                # 'org':org.org_name,
                # 'leader':leader.nickname,
            }
            group = auth_models.TUserGroup.objects.filter(user=obj.bsp_user_id)
            if group:
                group = group[0]
                dic['group'] = group.group.groupname
            else:
                dic['group'] = '未设置'

            bsporgid = obj.org_id
            org = TBspOrg.objects.filter(org_id=bsporgid)
            if org:
                org = org[0]
                dic['org'] = org.org_name
            else:
                dic['org'] = '未设置'

            leaderid = obj.leaders
            leader = TBspUser.objects.filter(bsp_user_id=leaderid)
            if leader:
                leader = leader[0]
                dic['leader'] = leader.nickname
            else:
                dic['leader'] = '未设置'

            data.append(dic)
        return data

    def post_searchbspuser(self):
        uname = self.parameters('uname')
        print uname
        if not uname:
            return;
        bspusers = TBspUser.objects.filter(nickname__contains=uname)
        # print bspusers
        data = []
        for obj in bspusers:

            dic = {
                'id':obj.bsp_user_id,
                'text':obj.nickname,
                'name':obj.nickname,
                'account':obj.account,
                # 'org':org.org_name,
                # 'leader':leader.nickname,
            }
            group = auth_models.TUserGroup.objects.filter(user=obj.bsp_user_id)
            if group:
                group = group[0]
                dic['group'] = group.group.groupname
            else:
                dic['group'] = '未设置'

            bsporgid = obj.org_id
            org = TBspOrg.objects.filter(org_id=bsporgid)
            if org:
                org = org[0]
                dic['org'] = org.org_name
            else:
                dic['org'] = '未设置'

            leaderid = obj.leaders
            leader = TBspUser.objects.filter(bsp_user_id=leaderid)
            if leader:
                leader = leader[0]
                dic['leader'] = leader.nickname
            else:
                dic['leader'] = '未设置'

            data.append(dic)
        return data

class ClusterServer(CoreView):

    @CheckParameters(['token','busline_id','server_items'])
    def post_addclusterbulineserver(self):
        """添加服务器业务线关系"""
        try:
            busline_id = self.parameters('busline_id')
            server_ids = self.parameters('server_items')
        except:
            raise APIError(-1002)

        busline_obj=TBusline.objects.filter(busline_id=busline_id)[0]
        for server in server_ids:
            resource_pool_server_obj = TResourcePoolServer.objects.filter(server_id=server)[0]
            error_row=[]
            try:
                resource_pool_server_obj.busline_id = busline_obj
                resource_pool_server_obj.save()
                message=u'服务器分配到%s业务线' % busline_obj.busline_id
                self.setlog(asset=server, context=message)
            except:
                error_row.append(server)
                continue

        return {'error_row':error_row,'cluster_name':busline_obj.busline_name}



    @CheckParameters(['token','cluster_id','server_items'])
    def post_addclusterserver(self):
        """添加服务器集群关系"""
        try:
            cluster_id = self.parameters('cluster_id')
            server_ids = self.parameters('server_items')
        except:
            raise APIError(-1002)

        busline_ids=TResourcePoolServer.objects.filter(server_id__in=server_ids).values('busline_id').distinct()
        cluster_ids=TCluster.objects.filter(cluster_id=cluster_id)[0]
        if len(busline_ids) != 1:
            return {'error_row':[server_ids],'cluster_name':server_ids}
        try:
            if int(busline_ids[0]['busline_id']) != int(cluster_ids.busline_id.busline_id):
                return {'error_row':[u"分配集群与业务线"],'cluster_name':server_ids}
        except:
                return {'error_row':[u"分配集群与业务线"],'cluster_name':server_ids}
        for server in server_ids:
            defaults_kwargs = {
                'cluster_server_id': self.create_id(),
                'cluster_id': TCluster.objects.filter(cluster_id=cluster_id)[0],
                'server_id': server_models.TServer.objects.filter(server_id=server)[0],
                }

            kwargs = {'cluster_id':defaults_kwargs['cluster_id'],
                       'server_id':defaults_kwargs['server_id'],
                       'defaults':defaults_kwargs}

            error_row=[]
            try:
                data_obj, created = TClusterServer.objects.get_or_create(**kwargs)
                if not created:
                    del defaults_kwargs['cluster_server_id']
                    data_obj.cluster_id=defaults_kwargs['cluster_id']
                    data_obj.server_id=defaults_kwargs['server_id']
                    data_obj.__dict__.update(**defaults_kwargs)
                    data_obj.save()
                resource_pool_server_obj = TResourcePoolServer.objects.filter(server_id=server)[0]
                resource_pool_server_obj.delete()
                message=u'添加服务器到%s集群' % defaults_kwargs['cluster_id']
                self.setlog(asset=defaults_kwargs['server_id'].asset_id, context=message)
            except:
                error_row.append(defaults_kwargs['server_id'].server_host_name)
                continue

        return {'error_row':error_row,'cluster_name':defaults_kwargs['cluster_id'].cluster_name}

    @CheckParameters(['token','cluster_id','server_items'])
    def post_delclusterserver(self):
        """释放服务器集群关系"""
        try:
            cluster_id = self.parameters('cluster_id')
            server_ids = self.parameters('server_items')
        except:
            raise APIError(-1002)

        for server in server_ids:
            error_row=[]
            try:
                resource_pool_server_obj = TResourcePoolServer.objects.filter(server_id=server)[0]
                resource_pool_server_obj.delete()
                server_obj = server_models.TServer.objects.filter(server_id=server)[0]
                server_obj.server_operation_status=1
                server_obj.save()
                message = u'从资源池%s中释放资源' % cluster_id
                self.setlog(asset=server_obj.asset_id, context=message)
            except:
                error_row.append(server_obj.server_host_name)
                continue

        return {'error_row':error_row}


class ClusterUser(CoreView):
	def get_deluser(self):
		bsp_user_id = self.parameters('user_id')
		cluster_id = self.parameters('cluster_id')
		clusteruser = TClusterUser.objects.get(cluster__cluster_id=cluster_id,bsp_user__id=bsp_user_id).delete()
		return {'id':bsp_user_id}


class Dpt(CoreView):

    def get_adddpt(self):

        try:
            dpt_level = self.parameters('dpt_level')
            dpt_name = self.parameters('dpt_name')
            dpt_pid = int(self.parameters('dpt_pid'))
            dpt_desc = self.parameters('dpt_desc')

            dpt = TDpt()
            if dpt_pid != 0:
                pdpt = TDpt.objects.get(dpt_id=dpt_pid)
                if int(pdpt.is_leaf) == 1:
                    pdpt.is_leaf = 0
                    pdpt.save()
                dpt.dpt_p = pdpt
            dpt.dpt_id = self.create_id()
            dpt.dpt_level = dpt_level
            dpt.dpt_name =  dpt_name
            dpt.dpt_desc = dpt_desc
            dpt.save()


        except:
            raise APIError(-3000)

        return {'id':dpt.dpt_id, 'name':dpt.dpt_name}



    def get_listdpt(self):

        dpt_id = self.parameters('id')
        try:
            if dpt_id is None or str(dpt_id) == '0':
                objs = TDpt.objects.filter(dpt_level=1)
            else:
                objs = TDpt.objects.filter(dpt_p_id=dpt_id)

        except:
            raise APIError(-3000)

        return serializers.serialize("json", objs)


    def get_del(self):
        dpt_id =  int(self.parameters('id'))
        dpt = TDpt.objects.get(dpt_id=dpt_id).delete()
        return {"id":dpt_id}


    def get_listlevel(self):
        dpt_id = self.parameters('id')
        tag = int(self.parameters('tag'))
        if tag == 1:
            objs = TDpt.objects.filter(dpt_id=dpt_id)
        else:
            objs = TDpt.objects.filter(dpt_p_id=dpt_id)
        return serializers.serialize('json', objs)

    def get_search(self):
        dpt_val =  self.parameters('value')
        objs = TDpt.objects.filter(dpt_name__contains=dpt_val).order_by('dpt_name')
        return serializers.serialize("json", objs)

class Org(CoreView):

    # http://10.48.180.9:3000/api/idc/getidcinfoall/?token=431071e111a707ab44d20992e404f788
    def get_listorg_bak(self):
        org_id = self.parameters('id')
        try:
            if str(org_id) == '0':
                objs = TOrg.objects.filter(org_level=1)
            else:
                objs = TOrg.objects.filter(org_bsp_pid=self.parameters('id'))
        except:
            raise APIError(-3000)

        return serializers.serialize("json", objs)
        # for obj in objs:
        #     return serializers.serialize("json", obj.get_name())


            # data_dic   = {"for-sale":{"text":"For Sale", "type":"folder"}, "vehicles":{"text":"Vehicles", "type":"folder"}, "services":{"text":"Personals", "type":"item"}};
        # for key in objs:
        #     return serializers.serialize("json",key)
        #     data[obj.org_bsp_id] = {"text": obj.org_name, "type":"folder"}
        data = serializers.serialize("json", objs)
        return data

    def get_listorg(self):
        org_id = self.parameters('id')

        try:
            if str(org_id) == '0':
                objs = TOrg.objects.filter(org_level=1)
                return serializers.serialize("json", objs)
            else:
                objs = TOrg.objects.filter(org_p_id=org_id)
        except:
            raise APIError(-3000)
        return serializers.serialize("json", objs)



    def get_org(self):
        try:
            obj = TOrg.objects.filter(org_id=self.parameters('org_id'))
        except:
            raise APIError(-3000)
        data = serializers.serialize("json", obj)
        return data


    def get_addorg(self):
        try:
            obj = TOrg.objects.filter(org_id=self.url_parameters('org_id'))
        except:
            raise APIError(-3000)
        data = serializers.serialize("json", obj)
        return data

class OrgDpt(CoreView):

    def get_addassocorg(self):
        org_item = self.parameters('item')
        dpt_id  = self.parameters('dpt_id')
        # delete assoc dpt
        TOrgDpt.objects.filter(dpt_id=dpt_id).delete()
        org_item = org_item.split(',')
        objs = TOrg.objects.filter(org_name__in=org_item)
        exists_objs = []
        for obj in objs:
            if obj.org_name in exists_objs:
                continue
            org_dpt_id = self.create_id()
            dpt = TDpt.objects.get(dpt_id=dpt_id)
            org_id = obj.org_id
            org = TOrg.objects.get(org_id=org_id)
            orgdpt = TOrgDpt()
            orgdpt.org_dpt_id = org_dpt_id
            orgdpt.org = org
            orgdpt.dpt = dpt
            orgdpt.save()
            exists_objs.append(obj.org_name)

        data = serializers.serialize("json",objs)
        return data


    def get_del(self):
        dptorg_id = self.parameters('id')
        orgdpt = TOrgDpt.objects.get(org_dpt_id=dptorg_id).delete()
        return {'id':dptorg_id}

    # zhangli

    def get_assocorg(self):
        org_item = self.parameters('item')
        dpt_id  = self.parameters('dpt_id')
        org_item = org_item.split(',')
        objs = TOrg.objects.filter(org_name__in=org_item)
        for obj in objs:
            org_dpt_id = self.create_id()
            dpt = TDpt.objects.get(dpt_id=dpt_id)
            org_id = obj.org_id
            org = TOrg.objects.get(org_id=org_id)
            orgdpt = TOrgDpt()
            orgdpt.org_dpt_id = org_dpt_id
            orgdpt.org = org
            orgdpt.dpt = dpt
            orgdpt.save()
        data = serializers.serialize("json",objs)
        return data


class UserBsp(CoreView):

    def get_listuser(self):
        page_limit = self.parameters('page_limit')
        q = self.parameters('q')
        if q is None:
            q = ''
        objs = TUserBsp.objects.filter(account__contains=q).order_by('account')[0:page_limit]
        vals = []

        for obj in objs:
            val = {'id':obj.id, 'text':obj.account}
            vals.append(val)
        return vals

    def get_adduser(self):
        dpt_user_id = self.create_id()
        user_name = self.parameters('user_name')
        dpt_id = self.parameters('dpt_id')
        is_admin = self.parameters('is_admin')
        op = self.parameters('op')
        kwargs = {'dpt_user_id':dpt_user_id, 'bsp_user_id':user_name, 'dpt_id':dpt_id, 'op_type':op, 'is_admin':is_admin}
        obj = TUserBsp(**kwargs)
        obj.save()

        return {'id':obj.dpt_user_id, 'name':obj.bsp_user_id}

class DptUser(CoreView):
     def get_adduser(self):
        dpt_user_id = self.create_id()
        user_name = self.parameters('user_name')
        dpt_id = self.parameters('dpt_id')
        is_admin = self.parameters('is_admin')
        op = self.parameters('op')
        kwargs = {'dpt_user_id':dpt_user_id, 'bsp_user_id':user_name, 'dpt_id':dpt_id, 'op_type':op, 'is_admin':is_admin}
        TDptUser.objects.filter(bsp_user_id=user_name).delete()
        obj = TDptUser(**kwargs)
        obj.save()
        return {'id':obj.dpt_user_id}



     def get_deluser(self):
         id = self.parameters('id')
         dptuser = TDptUser.objects.get(dpt_user_id=id).delete()
         return {'id':id}


class BusLine(CoreView):

     @CheckParameters(['token', 'q', 'page_limit'])
     def post_list(self):
         """业务线列表"""
         page_limit = self.parameters('page_limit')
         q = self.parameters('q')
         if q is None:
            q = ''
         objs = TBusline.objects.filter(busline_name__contains=q).order_by('busline_id')[0:page_limit]
         vals = []
         for obj in objs:
            val = {'id':obj.busline_id, 'text':obj.busline_name}
            vals.append(val)
         return vals


     def get_delbusline(self):
         id = self.parameters('id')
         dptuser = TBusline.objects.get(busline_id=id).delete()
         return {'id':id}

     def get_del(self):
         id = self.parameters('id')
         dptuser = TBusline.objects.get(busline_id=id).delete()
         return {'id':id}

     def get_assocdpt(self):
        dpt_item = self.parameters('item')
        busline_id  = self.parameters('busline_id')
        dpt_item = dpt_item.split(',')
        objs = TDpt.objects.filter(dpt_name__in=dpt_item)

        # delete assoc dpt
        # TBuslineDpt.objects.filter()
        for obj in objs:
            busline_dpt_id = self.create_id()
            dpt_id = obj.dpt_id
            kwargs = {'busline_dpt_id':busline_dpt_id, 'dpt_id':dpt_id, 'busline_id':busline_id}
            buslinedpt = TBuslineDpt(**kwargs)
            buslinedpt.save()
        data = serializers.serialize("json",objs)
        return data

     @CheckParameters(['token','busline_name','busline_code','desc'])
     def post_add(self):
         name = self.parameters('busline_name')
         code = self.parameters('busline_code')
         desc = self.parameters('desc')
         busline_id = self.create_id()
         kwargs = {'busline_id':busline_id, 'busline_code':code, 'busline_name':name, 'description':desc}
         obj = TBusline(**kwargs)
         obj.save()
         return {'id':busline_id, 'code':code}

     def get_search(self):
        value =  self.parameters('value')
        objs = TBusline.objects.filter(busline_name__contains=value).order_by('busline_name')
        return serializers.serialize("json", objs)

    #  @CheckParameters(['token','level'])
     def post_buslineinfo(self):

        start = self.parameters('startnum')
        step = self.parameters('range')
        level = self.parameters('level')
        parentID = self.parameters('parentID')

        # print start
        # print step
        if not start:
            start = 0;
        if not step:
            step = 10;
        endnum = int(start)+int(step)
        if not level:
            level = 1;

        data = []
        busline_objects = TBusline.objects.filter(busline_level=level)
        if parentID:
            busline_objects = busline_objects.filter(parent=parentID)
        busline_objects = busline_objects

        data_count = busline_objects.count()
        for obj in busline_objects[start:endnum]:

            owner_op = TBspUser.objects.filter(bsp_user_id=obj.owner_op_id)
            owner_biz = TBspUser.objects.filter(bsp_user_id=obj.owner_biz_id)

            dic = {
                'data_count': data_count,
                'busline_id': obj.busline_id,
                'busline_code': obj.busline_code,
                'busline_name': obj.busline_name,
                # 'owner_op': owner_op.nickname,
                # 'owner_op_id': owner_op.bsp_user_id,
                # 'owner_biz': owner_biz.nickname,
                # 'owner_biz_id': owner_biz.bsp_user_id,
                'busline_level': obj.busline_level,
                # 'is_leaf': obj.is_leaf,
                # 'fullpath': obj.fullpath,
                'description': obj.description,
                # 'state': obj.state,
                'bsp_org_id': obj.bsp_org_id,
                'bsp_org_name': obj.bsp_org.org_name,
                'parent_id': obj.parent_id,
                # 'parent_name': obj.parent.busline_name,

            }
            if int(obj.is_leaf) == 0:
                dic['is_leaf'] = '否'
            elif int(obj.is_leaf) == 1:
                dic['is_leaf'] = '是'
            else:
                dic['is_leaf'] = obj.is_leaf

            if int(obj.state) == 0:
                dic['state'] = '正常'
            elif int(obj.state) == 1:
                dic['state'] = '禁用'
            else:
                dic['state'] = obj.state


            thefullpath = obj.fullpath.split(',')
            finalfullpath = []
            print thefullpath
            for fp in thefullpath:
                # print 'aaaaaaaaaaaaaaaa'
                p = TBusline.objects.filter(busline_id=int(fp))
                if p:
                    p = p[0]
                    finalfullpath.append(p.busline_name)

            dic['fullpath'] = ','.join(finalfullpath)


            parent = TBusline.objects.filter(busline_id=obj.parent_id)
            if parent:
                # print 'bbbbbbbbbbbbbbbbbb'
                parent = parent[0]
                dic['parent_name'] = parent.busline_name
            else:
                dic['parent_name'] = '未设置'

            if owner_op:
                # print 'cccccccccccccccccc'
                owner_op = owner_op[0]
                dic['owner_op'] = owner_op.nickname
                dic['owner_op_id'] = owner_op.bsp_user_id
            else:
                dic['owner_op'] = ''
                dic['owner_op_id'] = ''

            if owner_biz:
                # print 'dddddddddddddddddddd'
                owner_biz = owner_biz[0]
                dic['owner_biz'] = owner_biz.nickname
                dic['owner_biz_id'] = owner_biz.bsp_user_id
            else:
                dic['owner_biz'] = ''
                dic['owner_biz_id'] = ''

            if obj.bsp_org_id:
                bsporg = TBspOrg.objects.get(org_id=obj.bsp_org_id)
                dic['bsp_org_name'] = bsporg.org_name
            else:
                dic['bsp_org_name'] = ''
            data.append(dic)
        # try:
        #
        # except Exception as e:
        #     raise APIError(-3000)
        #
        return data

     def post_allbuslinelist(self):
         uname = self.parameters('uname')
         buslines = TBusline.objects.filter(busline_name__contains=uname)
         data = []
         for obj in buslines:
             dic = {
                'text':obj.busline_name,
                'id':obj.busline_id,
                'fullpath':obj.fullpath
             }
             data.append(dic)
         return data


     def post_getbsporgtree(self):

         try:
             parentID = self.parameters('bol_id')
            #  print parentID
             if parentID:
                 bsp_obj_all = TBspOrg.objects.filter(parent_id_id=parentID)
             else:
                 bsp_obj_all = TBspOrg.objects.filter(org_level=1)

             data = []
             for obj in bsp_obj_all:
                #  print obj
                 d = {

                    'org_id': obj.org_id,
                    'org_level': obj.org_level,
                    'org_name': obj.org_name,
                    'parent_id': obj.parent_id_id

                 }
                #  print d
                 data.append(d)
         except Exception as e:
             raise
         return data

     def post_getallbsporgtree(self):
         uname = self.parameters('uname')
         bsporgs = TBspOrg.objects.filter(org_name__contains=uname)
         data = []
         for bsporg in bsporgs:
             dic = {
                'text':bsporg.org_name,
                'id':bsporg.org_id
             }
             data.append(dic)
         return data

     @CheckParameters(['buslineid', 'linkbsporgid'])
     def post_linkbsporg(self):
         buslineid = self.parameters('buslineid')
         linkid = self.parameters('linkbsporgid')
        #  print buslineid
        #  print linkid
         try:
             obj = TBusline.objects.filter(busline_id=buslineid)
             for v in obj:
                 bsp = TBspOrg.objects.filter(org_id=linkid)[0]
                 v.bsp_org=bsp
                 v.save()
         except Exception as e:
             raise false


     def post_savebusline(self):

         input_id = self.parameters('busline_id')
         input_code = self.parameters('busline_code')
         input_name = self.parameters('busline_name')
        #  input_op = self.parameters('input_op')
        #  input_manager = self.parameters('input_manager')
         input_level = 0
         input_desc = self.parameters('description')
         input_state = self.parameters('state')
         input_parent = self.parameters('parent_id')
         input_bsp = self.parameters('bsp_org_id')
         op_owner_id = self.parameters('owner_op_id')
         busline_owner_id = self.parameters('owner_biz_id')

         if not input_id:
             input_id = 0
         if not input_parent:
             input_parent = 0

         parent = TBusline.objects.filter(busline_id=input_parent)
         if parent:
             parent = parent[0]
         else:
             return False

         bsp = TBspOrg.objects.filter(org_id=input_bsp)
         if bsp:
             bsp = bsp[0]
         else:
             return False

         op_owner = TBspUser.objects.filter(bsp_user_id=op_owner_id)
         if op_owner:
             op_owner = op_owner[0]
         else:
             return False

         busline_owner = TBspUser.objects.filter(bsp_user_id=busline_owner_id)
         if busline_owner:
             busline_owner = busline_owner[0]
         else:
             return False

         busline = TBusline.objects.filter(busline_id=input_id)
         if busline:
             busline = busline[0]
         else:
             busline = TBusline.objects.create(parent=parent,bsp_org=bsp,owner_op=op_owner,owner_biz=busline_owner)

        #  修改父业务线的是否是叶子节点的记录
         parent.is_leaf = 0
         input_level = int(parent.busline_level) + 1
        #  print input_level
         parent.save()
        #  print busline
        #  print input_level
        #  print op_owner_id
        #  print busline_owner_id

         busline.busline_code = input_code
         busline.busline_name = input_name
         busline.owner_op = op_owner #input_op
         busline.owner_biz = busline_owner #input_manager
         busline.busline_level = int(input_level)
         busline.description = input_desc
         busline.state = int(input_state)
         busline.parent = parent
        #  print 'aaaaaaaaaaaaaa'
        #  print parent.fullpath
        #  print 'aaaaaaaaaaaaaa'
         if int(parent.fullpath) == 0:
             busline.fullpath = str(parent.busline_id) + ',' + str(busline.busline_id)
         else:
             busline.fullpath = str(parent.fullpath) + ',' + str(busline.busline_id)

         busline.is_leaf = 1
         busline.bsp_org = bsp
         busline.save()

         return True
        #  try:
        #
        #  except Exception as e:
        #      raise APIError(-3000)

        #  print input_id
        #  print input_code
        #  print input_name
        #  print input_op
        #  print input_manager
        #  print input_level
        #  print input_desc
        #  print input_state
        #  print input_parent
        #  print input_bsp
        #  try:
         #
        #  except Exception as e:
        #      raise APIError(-3000)


     def post_allbuslines(self):

         try:
             data = []
             buslines = TBusline.objects.all()
             for obj in buslines:
                 dic = {
                     'busline_id': obj.busline_id,
                    #  'busline_code': obj.busline_code,
                     'busline_name': obj.busline_name,
                    #  'owner_op': obj.owner_op,
                    #  'owner_biz': obj.owner_biz,
                     'busline_level': obj.busline_level,
                    #  'is_leaf': obj.is_leaf,
                    #  'fullpath': obj.fullpath,
                    #  'description': obj.description,
                    #  'state': obj.state,
                    #  'bsp_org_id': obj.bsp_org_id,
                     'parent_id': obj.parent_id,
                     }
                 data.append(dic)

         except Exception as e:
             raise APIError(-3000)

         return data

     def post_buslineswithlevelandpid(self):

         level = self.parameters('level')
         pid = self.parameters('pid')
         if not level:
             level = 1

         c_level = level + 1

         try:
             data = []
             print level
             buslines = TBusline.objects.filter(busline_level=level)
             print buslines
             if pid:
                 print pid
                 buslines = buslines.filter(parent=pid)
             for obj in buslines:
                 dic = {
                     'id': obj.busline_id,
                     'text': obj.busline_name,
                     'level': obj.busline_level,
                     'is_leaf': obj.is_leaf,
                     'parentID': obj.parent_id,
                    #  'nodes':[],
                     }
                 children = TBusline.objects.filter(busline_level=c_level).filter(parent=dic['id'])
                #  print children.count()
                 if children.count() > 0:
                     dic['nodes'] = [];
                 data.append(dic)
         except Exception as e:
             raise APIError(-3000)

         print data
         return data

     def post_allbsporg(self):
        #  try:
        #      data = []
        #      bsporgs = TBspOrg.objects.all()
        #      for obj in bsporgs:
        #          dic = {
        #              'org_id': obj.org_id,
        #              'org_name': obj.org_name,
        #              'org_level': obj.org_level,
        #              'parent_id': obj.parent_id
        #              }
        #          data.append(dic)
         #
        #  except Exception as e:
        #      raise APIError(-3000)

         data = []
         bsporgs = TBspOrg.objects.all()
         for obj in bsporgs:
             dic = {
                 'org_id': obj.org_id,
                 'org_name': obj.org_name,
                 'org_level': obj.org_level,
                 'parent_id': obj.parent_id_id
                 }
             data.append(dic)

         return data

     def post_bsporgwithlevelandpid(self):
         level = self.parameters('level')
         pid = self.parameters('pid')
         if not level:
             level = 1
         c_level = int(level) + 1
         data = []
         bsporgs = TBspOrg.objects.filter(org_level=level)
         if pid:
             bsporgs = bsporgs.filter(parent_id=pid)

         for obj in bsporgs:
             dic = {
                 'id': obj.org_id,
                 'text': obj.org_name,
                 'level': obj.org_level,
                 'parentID': obj.parent_id_id
                 }

             children = TBspOrg.objects.filter(org_level=c_level).filter(parent_id=dic['id'])
            #  print children.count()
             if children.count() > 0:
                 dic['nodes'] = [];

             data.append(dic)

         return data

     def post_getclickbusline(self):
         try:
             data = []
             buslineid = self.parameters('currentID')
             busline_obj = TBusline.objects.filter(busline_id=buslineid)
             for obj in busline_obj:
                 dic = {
                    'busline_id': obj.busline_id,
                    # 'busline_code': obj.busline_code,
                    'busline_name': obj.busline_name,
                    # 'owner_op': obj.owner_op,
                    # 'owner_biz': obj.owner_biz,
                    'busline_level': obj.busline_level,
                    # 'is_leaf': obj.is_leaf,
                    'fullpath': obj.fullpath,
                    # 'description': obj.description,
                    # 'state': obj.state,
                    # 'bsp_org_id': obj.bsp_org_id,
                    'parent_id': obj.parent_id,
                 }
             data.append(dic)
         except Exception as e:
             raise APIError(-3000)
         return data

     def post_getclickbsporg(self):
         try:
             data = []
             bsporgid = self.parameters('currentID')
             bsporg_obj = TBspOrg.objects.filter(org_id=bsporgid)
             for obj in bsporg_obj:
                 dic = {
                    'org_id': obj.org_id,
                    'org_name': obj.org_name,
                    'org_level': obj.org_level,
                    'parent_id': obj.parent_id_id
                 }
                 data.append(dic)
         except Exception as e:
             raise
         return data
    #  @CheckParameters(['bl_id'])
    #  def post_nextlevelbusline(self):
    #      try:
    #          bl_id = self.parameters('bl_id')
    #          data = []
    #          current = TBusline.objects.filter(busline_id = bl_id)[0]
    #         #  此处需要等parent属性关联完成之后，进行修改。暂时如下处理。
    #          nextLevel = current.busline_level+1
    #          result = TBusline.objects.filter(busline_level = nextLevel)
    #          for obj in result:
    #              dic = {
    #                 'busline_id':obj.busline_id,
    #                 'busline_code':obj.busline_code,
    #                 'busline_name':obj.busline_name,
    #                 'owner_op':obj.owner_op,
    #                 'owner_biz':obj.owner_biz,
    #                 'busline_level':obj.busline_level,
    #                 'is_leaf':obj.is_leaf,
    #                 'fullpath':obj.fullpath,
    #                 'description':obj.description,
    #                 'state':obj.state,
    #                 # 'bsp_org_id':obj.bsp_org_id.org_id,
    #                 # 'parent_id':obj.parent_id.busline_id
    #                 'bsp_org_id':nextLevel,
    #                 'parent_id':nextLevel
    #              }
    #              data.append(dic)
    #      except Exception as e:
    #          raise APIError(-3000)
     #
    #      return data

    #  @CheckParameters(['id'])
    #  def get_buslinedetail(self):
    #      try:
    #          data = []
    #          busline_detail = TBusline.objects.filter(busline_id=self.parameters('id'))
    #          for obj in busline_detail:
    #              dic = {
    #                  'busline_id':obj.busline_id,
    #                  'busline_code':obj.busline_code,
    #                  'busline_name':obj.busline_name,
    #                  'owner_op':obj.owner_op,
    #                  'owner_biz':obj.owner_biz,
    #                  'busline_level':obj.busline_level,
    #                  'is_leaf':obj.is_leaf,
    #                  'fullpath':obj.fullpath,
    #                  'description':obj.description,
    #                  'state':obj.state,
    #                 #  'bsp_org_id':obj.bsp_org_id.org_id,
    #                  # 'parent_id':obj.parent_id.busline_id
    #                  'bsp_org_id':'obj.bsp_org_id.org_id',
    #                  'parent_id':'obj.parent_id.busline_id'
     #
    #              }
    #              data.append(dic)
    #      except Exception as e:
    #          raise APIError(-3000)
     #
    #      return data

     def post_searchbuslineinfo(self):

         names = self.parameters('name').split(',')
         ops = self.parameters('op').split(',')
         managers = self.parameters('manager').split(',')

         print names, ops, managers

         opids = [];
         opdatas = TBspOrg.objects.filter(org_name__in=ops)
         for obj in opdatas:
             opids.append(obj.org_id)

         buslineids = [];
         buslinedatas = TBspUser.objects.filter(nickname__in=managers)
         for obj in buslinedatas:
             buslineids.append(obj.bsp_user_id)

         busline_obj = TBusline.objects.filter(
                 Q(busline_name__in=names)
                | Q(bsp_org__in=opids)
                | Q(owner_op__in=buslineids)
                )
        #  print busline_obj
         data = []
         for obj in busline_obj:
             dic = {
                 'busline_id':obj.busline_id,
                 'busline_code':obj.busline_code,
                 'busline_name':obj.busline_name,
                 'owner_op':obj.owner_op.nickname,
                 'owner_biz':obj.owner_biz.nickname,
                 'owner_op_id':obj.owner_op_id,
                 'owner_biz_id':obj.owner_biz_id,
                 'busline_level':obj.busline_level,
                 'is_leaf':obj.is_leaf,
                 'fullpath':obj.fullpath,
                 'description':obj.description,
                 'state':obj.state,
                 'bsp_org_id':obj.bsp_org_id,
                 'bsp_org_name':obj.bsp_org.org_name,
                 'parent_id':obj.parent_id,
                #  'parent_name': obj.parent.busline_name,
             }

             parent = TBusline.objects.filter(busline_id=obj.parent_id)
             if parent:
                 parent = parent[0]
                 dic['parent_name'] = parent.busline_name
             else:
                 dic['parent_name'] = '未设置'

             data.append(dic)

        #  try:
        #
         #
        #  except:
        #      raise APIError(-3000)

         return data


# BusLineUser
class BusLineUser(CoreView):
     def get_adduser(self):
        busline_user_id = self.create_id()
        user_name = self.parameters('user_name')
        busline_id = self.parameters('busline_id')
        is_admin = self.parameters('is_admin')
        op = self.parameters('op')
        kwargs = {'busline_user_id':busline_user_id, 'bsp_user_id':user_name, 'busline_id':busline_id, 'op_type':op, 'is_admin':is_admin}
        obj = TBuslineUser(**kwargs)
        obj.save()
        return {'id':obj.busline_user_id}


     def get_deluser(self):
         id = self.parameters('id')
         dptuser = TBuslineUser.objects.get(busline_user_id=id).delete()
         return {'id':id}

class BuslineServer(CoreView):
    @CheckParameters(['token','server_items','busline_id'])
    def post_addbuslinserver(self):
        try:
            server_sns=str(self.parameters('server_items')).split(',')
            busline_obj=TBusline.objects.filter(busline_id=self.parameters('busline_id'))[0]
        except:
            raise APIError(-3000)

        error_row=[]
        for server in server_sns:
            try:
                server_obj=server_models.TServer.objects.filter(asset_id__asset_sn=server)[0]
                defaults_kwargs = {
                    'busline_server_id':self.create_id(),
                    'busline':busline_obj,
                    'server':server_obj
                    }
                kwargs = {'busline':busline_obj,
                        'server':server_obj,
                        'defaults':defaults_kwargs
                        }
                data_obj, created = TBuslineServer.objects.get_or_create(**kwargs)
                if not created:
                    del defaults_kwargs['busline_server_id']
                    data_obj.server = defaults_kwargs['server']
                    data_obj.busline = defaults_kwargs['busline']
                    data_obj.__dict__.update(**defaults_kwargs)
                    data_obj.save()
                    server_obj.server_operation_status=0
                    server_obj.save()

            except:
                error_row.append(server)
                continue
        return error_row
