# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.http import HttpResponse
from django.core import serializers
from models import *
from django.db.models import Q
from apps.dpt import models as dpt_models
from apps.idc import models as idc_models
from apps.ips import models as ip_models
from apps.accessory import models as accessory_models
from public.APIViews import CoreView
from public.Exceptions import APIError
from public.Check import CheckParameters
from public.Syskeywords import db_code_mapping
from datetime import datetime
import json
from public.File import handle_uploaded_file
import urllib, urllib2

class Server(CoreView):

    @CheckParameters(['producer_name','device_type','sn','cpu_capacity','memory_capacity','net_card_capacity','disk_capacity','cpu_info','memory_info','net_card_info','disk_info','server_device_type_name'])
    def post_createserver(self):

        try:
            #厂商表
            if self.parameters('producer_name') and self.parameters('device_type'):
                defaults_kwargs = {
                    'device_producer_type_id':self.create_id(),
                    'producer_name':self.parameters('producer_name'),
                    'device_type':self.parameters('device_type'),
                }
                kwargs = {
                    'producer_name':self.parameters('producer_name'),
                    'device_type':self.parameters('device_type'),
                    'defaults':defaults_kwargs
                }
                #print defaults_kwargs, kwargs
                data_obj, created = TDeviceProducerType.objects.exclude(delete_status=db_code_mapping['delete']).get_or_create(**kwargs)
                if not created:
                    del defaults_kwargs['device_producer_type_id']
                    data_obj.__dict__.update(**defaults_kwargs)
                    data_obj.save()

            #OS表
            if self.parameters('os_type_name') and self.parameters('os_type_version') and self.parameters('os_kernerl_version'):
                defaults_kwargs = {
                    'os_type_id':self.create_id(),
                    'os_type_name':self.parameters('os_type_name'),
                    'os_type_version':self.parameters('os_type_version'),
                    'os_kernerl_version':self.parameters('os_kernerl_version'),
                }
                kwargs = {
                    'os_type_name':self.parameters('os_type_name'),
                    'os_type_version':self.parameters('os_type_version'),
                    'os_kernerl_version':self.parameters('os_kernerl_version'),
                    'defaults':defaults_kwargs,
                }
                print 'os'
                #print defaults_kwargs, kwargs
                data_obj, created = TOsType.objects.exclude(delete_status=db_code_mapping['delete']).get_or_create(**kwargs)
                if not created:
                    del defaults_kwargs['os_type_id']
                    data_obj.__dict__.update(**defaults_kwargs)
                    data_obj.save()

            #服务器类型表
            if self.parameters('producer_name') and self.parameters('device_type') and self.parameters('server_device_type_name'):
                defaults_kwargs = {
                    'server_type_id':self.create_id(),
                    'device_producer_id':TDeviceProducerType.objects.filter(
                        producer_name=self.parameters('producer_name'),
                        device_type=self.parameters('device_type'),
                        ).exclude(delete_status=db_code_mapping['delete'])[0],
                    'server_device_type_name':self.parameters('server_device_type_name'),
                #'server_hight':self.parameters('server_hight'),
                }
                kwargs = {
                    'server_device_type_name':self.parameters('server_device_type_name'),
                #'server_hight':self.parameters('server_hight'),
                    'defaults':defaults_kwargs
                }
                print 'server_type'
                #print defaults_kwargs, kwargs
                data_obj, created = TServerDeviceType.objects.exclude(delete_status=db_code_mapping['delete']).get_or_create(**kwargs)
                if not created:
                    del defaults_kwargs['server_type_id']
                    data_obj.device_producer_id = defaults_kwargs['device_producer_id']
                    data_obj.__dict__.update(**defaults_kwargs)
                    data_obj.save()


            #IP
            if self.parameters('inip'):
                sn_obj = TAsset.objects.filter(asset_sn=self.parameters('sn'))[0]
                defaults_kwargs = {
                    'ip_id':self.create_id(),
                    #'sn':sn_obj,
                    'ip':self.parameters('inip'),
                    'gateway':self.parameters('ingateway'),
                    'mask':self.parameters('inmask'),
                    'ip_type':0,
                    'mac': self.parameters('inmac'),
                }
                kwargs = {'ip':self.parameters('inip'),'defaults':defaults_kwargs}
                print 'ip'
                #print defaults_kwargs, kwargs
                data_obj, created = ip_models.TRealIp.objects.exclude(delete_status=db_code_mapping['delete']).get_or_create(**kwargs)
                if not created:
                    del defaults_kwargs['ip_id']
                    data_obj.__dict__.update(**defaults_kwargs)
                    data_obj.save()


                #server_obj = server_models.TAsset.objects.filter(asset_sn=self.parameters('sn')).exclude(delete_status=db_code_mapping['delete'])[0]
                #ip_obj is data_obj
                defaults_kwargs = {
                    'assetip_id': self.create_id(),
                    'ip': data_obj,
                    'asset': sn_obj
                }
                kwargs = {'ip': data_obj, 'asset': sn_obj, 'defaults': defaults_kwargs}
                data_obj, created = ip_models.TAssetIp.objects.exclude(delete_status=db_code_mapping['delete']).get_or_create(**kwargs)
                if not created:
                    del defaults_kwargs['assetip_id']
                    data_obj.__dict__.update(**defaults_kwargs)
                    data_obj.save()
            """
            if self.parameters('outip'):
                defaults_kwargs = {
                    'ip_id':self.create_id(),
                    'sn':sn_obj,
                    'ip':self.parameters('outip'),
                    'gateway':self.parameters('outgateway'),
                    'mask':self.parameters('outmask'),
                    'ip_type':TRealIp.IP_TYPE_MAPPING['外网'],
                    'mac': self.parameters('outmac'),
                    }
                kwargs = {'sn':sn_obj,'ip':self.parameters('outip'),'defaults':defaults_kwargs}
                data_obj, created = TRealIp.objects.exclude(delete_status=db_code_mapping['delete']).get_or_create(**kwargs)
                if not created:
                    del defaults_kwargs['ip_id']
                    data_obj.__dict__.update(**defaults_kwargs)
                    data_obj.save()
            """

            #配件表
            defaults_kwargs = {
                'accessory_id':self.create_id(),
                'cpu_capacity':self.parameters('cpu_capacity'),
                'sn':TAsset.objects.filter(asset_sn=self.parameters('sn'))[0],
                'memory_capacity':self.parameters('memory_capacity'),
                'net_card_capacity':self.parameters('net_card_capacity'),
                'disk_capacity':self.parameters('disk_capacity'),
                'cpu_info':self.parameters('cpu_info'),
                'memory_info':self.parameters('memory_info'),
                'disk_info':self.parameters('disk_info'),
                'net_card_info':self.parameters('net_card_info'),
            }
            kwargs = {'sn':TAsset.objects.filter(asset_sn=self.parameters('sn'))[0],
                    'defaults':defaults_kwargs}
            #print defaults_kwargs, kwargs
            data_obj, created = accessory_models.TRealaccessory.objects.exclude(delete_status=db_code_mapping['delete']).get_or_create(**kwargs)
            if not created:
                del defaults_kwargs['accessory_id']
                data_obj.__dict__.update(**defaults_kwargs)
                data_obj.save()

            #服务器表
            #print TOsType.objects.filter(os_type_name=self.parameters('os_type_name'),os_type_version=self.parameters('os_type_version'),os_kernerl_version=self.parameters('os_kernerl_version'),)[0].os_type_id
            defaults_kwargs = {
                'server_id':self.create_id(),
                #'server_health_status':TServer.SERVER_HEALTH_STATUS_MAPPING[self.parameters('server_health_status')],
                #'server_run_status':TServer.SERVER_RUN_STATUS_MAPPING[self.parameters('server_run_status')],
                'server_operation_status':1, #装机流程统一为未交付
                #'server_comment':table.row_values(i)[14],
                'asset_id':TAsset.objects.filter(asset_sn=self.parameters('sn'))[0],
                'server_host_name':self.parameters('server_host_name'),
                'os_type_id':TOsType.objects.filter(
                    os_type_name=self.parameters('os_type_name'),
                    os_type_version=self.parameters('os_type_version'),
                    os_kernerl_version=self.parameters('os_kernerl_version'),
                    )[0],
                'server_device_type_id':TServerDeviceType.objects.filter(
                    server_device_type_name=self.parameters('server_device_type_name'))[0],
                    }
            kwargs = {
                'asset_id':TAsset.objects.filter(asset_sn=self.parameters('sn'))[0],
                #'server_host_name':self.parameters('server_host_name'),
                'defaults':defaults_kwargs
            }
            #print defaults_kwargs, kwargs
            data_obj, created = TServer.objects.exclude(delete_status=db_code_mapping['delete']).get_or_create(**kwargs)
            if not created:
                del defaults_kwargs['server_id']
                data_obj.os_type_id = defaults_kwargs['os_type_id']
                data_obj.server_device_type_id = defaults_kwargs['server_device_type_id']
                data_obj.__dict__.update(**defaults_kwargs)
                data_obj.save()

        except:
            raise APIError(-3000)


    @CheckParameters(['pk'])
    def post_getserverdetailedinfo(self):
        '''
        获取服务器详细信息
        '''
        try:
            data = []
            server_obj = TServer.objects.filter(server_id=self.parameters('pk')).exclude(delete_status=db_code_mapping['delete'])
            data_count=server_obj.count()

            for i in server_obj:
                d = {
                    'data_count': data_count,
                    'pk': i.asset_id.asset_id,
                    'sn': i.asset_id.asset_sn,
                    'position': '',
                    'inip': ','.join([j.ip.ip for j in ip_models.TAssetIp.objects.filter(asset=i.asset_id) if int(j.ip.ip_type) is 0]),
                    'in_mask': ','.join([j.ip.mask for j in ip_models.TAssetIp.objects.filter(asset=i.asset_id) if int(j.ip.ip_type) is 0]),
                    'outip': ','.join([j.ip.ip for j in ip_models.TAssetIp.objects.filter(asset=i.asset_id) if int(j.ip.ip_type) is 1]),
                    'out_mask': ','.join([j.ip.mask for j in ip_models.TAssetIp.objects.filter(asset=i.asset_id) if int(j.ip.ip_type) is 1]),
                    'bmcip': ','.join([j.ip.ip for j in ip_models.TAssetIp.objects.filter(asset=i.asset_id) if int(j.ip.ip_type) is 2]),
                    'mac': ','.join([j.ip.mac for j in ip_models.TAssetIp.objects.filter(asset=i.asset_id) if int(j.ip.ip_type) is 0]),
                    'server_type': i.server_device_type_id.server_device_type_name,
                    'os': '-'.join([i.os_type_id.os_type_name, i.os_type_id.os_type_version]),
                    'cpu_info': ','.join([j.cpu_info for j in i.asset_id.trealaccessory_set.all()]),
                    'disk_info': ','.join([j.disk_info for j in i.asset_id.trealaccessory_set.all()]),
                    'producer': i.server_device_type_id.device_producer_id.producer_name,
                    'las_time': i.asset_id.asset_last_update_time.strftime("%Y-%m-%d %H:%M:%S"),
                    'device_type': i.get_server_type_display(),
                    'run_status': i.get_server_run_status_display(),
                    'memory_info': ','.join([j.memory_info for j in i.asset_id.trealaccessory_set.all()]),
                    'net_card': ','.join([j.net_card_info for j in i.asset_id.trealaccessory_set.all()]),
                    #'asset_warranty_due_time': i.asset_id.asset_warranty_due_time.strftime("%Y-%m-%d"),
                    #'asset_on_shelf_time': i.asset_id.asset_on_shelf_time.strftime("%Y-%m-%d")
                }

                if (i.server_type != TServer.SERVER_TYPE_MAPPING[u'虚拟机']):
                    d['position'] = '-'.join([str(i.asset_id.position_id.rack_id.rack_name),str(i.asset_id.position_id.rack_id.rack_code),str(i.asset_id.position_id.position_num)])
                else:
                    d['domain0'] = '-'.join(i.asset_id.asset_num.split('-')[0:2])
                if i.asset_id.asset_warranty_due_time:
                    d['asset_warranty_due_time'] = i.asset_id.asset_warranty_due_time.strftime("%Y-%m-%d")
                else:
                    d['asset_warranty_due_time'] = ''
                if i.asset_id.asset_on_shelf_time:
                    d['asset_on_shelf_time'] = i.asset_id.asset_on_shelf_time.strftime("%Y-%m-%d")
                else:
                    d['asset_on_shelf_time'] = ''
                if i.server_operation_status == 0:
                    d['op_user'] = list(set([ii.cluster_id.op_owner.account for ii in dpt_models.TClusterServer.objects.filter(
                                                server_id=i.server_id)
                                            ]))
                    d['op_user_phone'] = list(set([ii.cluster_id.op_owner.mobile for ii in dpt_models.TClusterServer.objects.filter(
                                                server_id=i.server_id)
                                            ]))
                    d['busline'] = list(set([ii.cluster_id.busline_id.busline_name for ii in dpt_models.TClusterServer.objects.filter(
                                                server_id=i.server_id)
                                            ]))
                    d['buline_user'] = list(set([ii.cluster_id.busline_owner.account for ii in dpt_models.TClusterServer.objects.filter(
                                                server_id=i.server_id)
                                            ]))
                    d['buline_user_name'] = list(set([ii.cluster_id.busline_owner.nickname for ii in dpt_models.TClusterServer.objects.filter(
                                                server_id=i.server_id)
                                            ]))
                    d['buline_user_phone'] = list(set([ii.cluster_id.busline_owner.mobile for ii in dpt_models.TClusterServer.objects.filter(
                                                server_id=i.server_id)
                                            ]))
                    d['op_user_name'] = list(set([ii.cluster_id.op_owner.nickname for ii in dpt_models.TClusterServer.objects.filter(
                                                server_id=i.server_id)
                                            ]))
                else:
                    d['buline_user_name'] = 'NULL'
                    d['op_user_name'] = 'NULL'
                    d['op_user'] = 'NULL'
                    d['op_user_phone'] = 'NULL'
                    d['busline'] = 'NULL'
                    d['buline_user_phone'] = 'NULL'
                    d['buline_user'] = 'NULL'
                data.append(d)

        except:
            raise APIError(-3000)
        return data

    @CheckParameters(['token','startnum','range','inip','outip','bmcip','assetsn','assetno','cluster','servermodel','servertype','incservertype'])
    def post_searchserverinfo(self):
        '''
        按条件搜索数据
        '''
        try:
            inips = self.parameters('inip').replace('\n',',').split(',')
            outips = self.parameters('outip').replace('\n',',').split(',')
            bmcips = self.parameters('bmcip').replace('\n',',').split(',')
            assetsns = self.parameters('assetsn').replace('\n',',').split(',')
            assetnos = self.parameters('assetno').replace('\n',',').split(',')
            clusters = self.parameters('cluster')
            incservertype=self.parameters('incservertype')
            servertype=self.parameters('servertype')
            servermodel=self.parameters('servermodel')
            startnum = self.parameters('startnum')
            rangeid = self.parameters('range')
        except:
            raise APIError(-3000)

        if not startnum:
            startnum = 0
        if not rangeid:
            rangeid = 10
        endnum = startnum+rangeid

        query = Q()
        if inips != [u'']:
            query = query | Q(
                asset_id__tassetip__ip__ip__in=inips,
                asset_id__tassetip__ip__ip_type=ip_models.TRealIp.IP_TYPE_MAPPING[u'内网']
            )
        if bmcips != [u'']:
            query = query | Q(
                    asset_id__tassetip__ip__ip__in=bmcips,
                    asset_id__tassetip__ip__ip_type=ip_models.TRealIp.IP_TYPE_MAPPING[u'管理网']
                    )
        if outips != [u'']:
            query = query | Q(
                    asset_id__tassetip__ip__ip__in=outips,
                    asset_id__tassetip__ip__ip_type=ip_models.TRealIp.IP_TYPE_MAPPING[u'外网']
                    )
        if assetsns != [u'']:
            query = query | Q(
                    asset_id__asset_sn__in=assetsns
                    )
        if assetnos != [u'']:
            query = query | Q(
                    asset_id__asset_num__in=assetnos
                    )
        if clusters:
            query = query | Q(
                    server_device__cluster_id__cluster_name__contains=clusters
                    )

        if query == Q():
            server_obj = TServer.objects.all().exclude(delete_status=db_code_mapping['delete'])
        else:
            server_obj = TServer.objects.filter(
                    query
                    ).exclude(delete_status=db_code_mapping['delete']).distinct()

        if incservertype:
            server_obj=server_obj.filter(inc_server_type_id__inc_server_type_name=incservertype)
        if servertype:
            server_obj=server_obj.filter(server_type=servertype)
        if servermodel:
            server_obj=server_obj.filter(server_device_type_id__device_producer_id__producer_name__contains=servermodel)
        data=[]
        data_count=server_obj.count()
        for i in server_obj[startnum:endnum]:
            info = {
                    'data_count': data_count,
                    'pk': i.server_id,
                    'sn': i.asset_id.asset_sn,
                    'num': i.asset_id.asset_num,
                    'inip': ','.join(
                        [ii.ip.ip for ii in ip_models.TAssetIp.objects.filter(
                                                asset_id=i.asset_id.asset_id,
                                                ip_id__ip_type=ip_models.TRealIp.IP_TYPE_MAPPING[u'内网'])
                        ]),
                    'outip': ','.join(
                        [ii.ip.ip for ii in ip_models.TAssetIp.objects.filter(
                                                asset_id=i.asset_id.asset_id,
                                                ip_id__ip_type=ip_models.TRealIp.IP_TYPE_MAPPING[u'外网'])
                        ]),
                    'bmcip': ','.join(
                        [ii.ip.ip for ii in ip_models.TAssetIp.objects.filter(
                                                asset_id=i.asset_id.asset_id,
                                                ip_id__ip_type=ip_models.TRealIp.IP_TYPE_MAPPING[u'管理网'])
                        ]),
                    'mac': ','.join(
                        [ii.ip.mac for ii in ip_models.TAssetIp.objects.filter(
                                                asset_id=i.asset_id.asset_id,
                                                ip_id__ip_type=ip_models.TRealIp.IP_TYPE_MAPPING[u'内网'])
                        ]),
                    'clusters': ','.join(
                        [ii.cluster_id.cluster_name for ii in dpt_models.TClusterServer.objects.filter(
                                                server_id=i.server_id)
                        ]),
                    'server_type': i.server_device_type_id.server_device_type_name,
                    'os': '-'.join([i.os_type_id.os_type_name, i.os_type_id.os_type_version]),
                    #'cpu': ','.join([j.cpu_capacity for j in i.asset_id.trealaccessory_set.all()]),
                    #'disk': ','.join([j.disk_capacity for j in i.asset_id.trealaccessory_set.all()]),
                    'inc_type': i.inc_server_type_id.inc_server_type_name,
                    'producer': i.server_device_type_id.device_producer_id.producer_name,
                    'las_time': i.asset_id.asset_last_update_time.strftime("%Y-%m-%d %H:%M:%S"),
                    'device_type': i.get_server_type_display(),
                    'run_status': i.get_server_run_status_display(),
                    'server_health_status': i.server_health_status,
                    'server_operation_status':i.server_operation_status,
                    'host_name':i.server_host_name
                    }
            if (i.server_type != TServer.SERVER_TYPE_MAPPING[u'虚拟机']):
                info['position']='-'.join([str(i.asset_id.position_id.rack_id.rack_name),str(i.asset_id.position_id.rack_id.rack_code),str(i.asset_id.position_id.position_num)])
            else:
                info['position']=''
            data.append(info)

        return data


    @CheckParameters(['token','startnum','range'])
    def post_getrepair(self):
        try:
            startnum = self.parameters('startnum')
            rangeid = self.parameters('range')
            data = []
            endnum = startnum + rangeid
            server_obj = TServer.objects.filter(server_health_status=1).exclude(delete_status=db_code_mapping['delete']).exclude(server_type=2)
            for i in server_obj[startnum:endnum]:
                #print TServerRepair.objects.filter(asset_id = i.asset_id)
                d = {
                    'pk': i.server_id,
                    'sn': i.asset_id.asset_sn,
                    'position': '-'.join([str(i.asset_id.position_id.rack_id.rack_name),str(i.asset_id.position_id.rack_id.rack_code),str(i.asset_id.position_id.position_num)]),
                    'inip': ','.join([j.ip.ip for j in ip_models.TAssetIp.objects.filter(asset=i.asset_id) if int(j.ip.ip_type) is 0]),
                            #'outip': ','.join([j.ip for j in i.asset_id.trealip_set.filter(ip_type=1)]),
                            #'bmcip': ','.join([j.ip for j in i.asset_id.trealip_set.filter(ip_type=2)]),
                            #'mac': ','.join([j.mac for j in i.asset_id.trealip_set.filter(ip_type=0)]),
                    'server_type': i.server_device_type_id.server_device_type_name,
                            #'os': '-'.join([i.os_type_id.os_type_name, i.os_type_id.os_type_version]),
                            #'cpu': ','.join([j.cpu_capacity for j in i.asset_id.trealaccessory_set.all()]),
                            #'disk': ','.join([j.disk_capacity for j in i.asset_id.trealaccessory_set.all()]),
                    'producer': i.server_device_type_id.device_producer_id.producer_name,
                            #'las_time': i.asset_id.asset_last_update_time.strftime("%Y-%m-%d %H:%M:%S"),
                    'device_type': i.get_server_type_display(),
                    'server_health_status': i.server_health_status,
                    'count': TServerRepair.objects.filter(asset_id = i.asset_id).count()
                            #'run_status': i.get_server_run_status_display()
                            }
                data.append(d)
        except:
            raise APIError(-3000)

        return data


    @CheckParameters(['token', 'flag', 'hostname'])
    def post_monitor(self):
        try:
            sn = self.parameters('hostname')
            asset = TAsset.objects.filter(asset_sn=sn)
            asset_ip_obj = ip_models.TAssetIp.objects.filter(asset=asset)
            ip =  ','.join([j.ip.ip for j in ip_models.TAssetIp.objects.filter(asset=asset) if int(j.ip.ip_type) is 0])
            dic = {'close': 'host_disable', 'open': 'host_enable'}
            url = 'http://58mm.58corp.com/zconfig/api/host_ad/'
            action = dic[self.parameters('flag')]
        #hostname = self.parameters('hostname')
            hostname = '10.126.85.221'
            data = {'action':action, 'hostname':hostname}
            data = json.dumps(data)
            req = urllib2.Request(url, data)
            response = urllib2.urlopen(req)
            page = response.read()
            self.setlog(asset=asset[0].assetip_id, context=u'监控人工下掉')
            return page
        except:
            raise APIError(-3000)

    @CheckParameters(['sn','step'])
    def post_updaterepairstep(self):
        try:
            repair_obj = TServerRepair.objects.filter(asset_id__asset_sn=self.parameters('sn'), repair_status=1)[0]
            repair_obj.repair_status = self.parameters('step')
            repair_obj.save()
            if self.parameters('step') == -1:
                obj = TServer.objects.filter(asset_id__asset_sn=self.parameters('sn'))[0]
                obj.server_health_status = 0
                repair_obj.repair_end_time = datetime.now()
                repair_obj.save()
                obj.save()

        except:
            raise APIError(-3000)


    @CheckParameters(['sn', 'context'])
    def post_createrepair(self):
        try:
            defaults_kwargs = {
                'server_repair_id': self.create_id(),
                'asset_id': TAsset.objects.filter(asset_sn=self.parameters('sn'))[0],
                'repair_start_time': datetime.now(),
                'repair_context': self.parameters('context'),
                'repair_status': 1,
                'repair_user': dpt_models.TBspUser.objects.filter(account=self.request.session['username'])[0],
            }
            obj = TServerRepair(**defaults_kwargs)
            obj.save()

            server_obj = TServer.objects.filter(asset_id__asset_sn=self.parameters('sn'))[0]
            server_obj.server_health_status = 1
            server_obj.save()
            #self.setlog(asset=obj.asset_id, context='create repair list')
            #add repair pool
            defaults_kwargs = {
                'resource_pool_server_id': self.create_id(),
                'resource_pool_id': dpt_models.TResourcePool.objects.filter(resource_pool_name='报修服务器')[0],
                'server_id': server_obj,
                'add_time': datetime.now(),
                'bsp_user_id': dpt_models.TBspUser.objects.filter(account=self.request.session['username'])[0]
            }
            if dpt_models.TResourcePoolServer.objects.filter(server_id=server_obj):
                pass
            else:
                obj = dpt_models.TResourcePoolServer(**defaults_kwargs)
                obj.save()

            self.setlog(asset=server_obj.asset_id, context='create repair list')
        except:
            raise APIError(-3000)

    @CheckParameters(['sn'])
    def post_getrepairinfo(self):
        try:
            data = []
            server_obj = TServer.objects.filter(asset_id__asset_sn=self.parameters('sn')).exclude(delete_status=db_code_mapping['delete'])
            asset = server_obj[0].asset_id
            repair_info = TServerRepair.objects.filter(asset_id=asset, repair_status=-1)
            for i in repair_info:
                d = {
                    'repair_end_time': i.repair_end_time.strftime("%Y-%m-%d %H:%M:%S"),
                    #'user': i.repair_user.nickname,
                    'context': i.repair_context
                }
                data.append(d)
                #print i.repair_start_time.strftime("%Y-%m-%d %H:%M:%S")
                #print i.repair_end_time.strftime("%Y-%m-%d %H:%M:%S")
                #print i.repair_user.repair_user.nickname
                #print i.repair_context
            #repair_info = TServerRepair.objects.filter()
        except:
            raise APIError(-3000)
        return data


    @CheckParameters(['token','resource_pool_id'])
    def post_getresoursepoolserver(self):
        '''
        获取资源池信息
        '''
        try:
            data = []
            resourcepoolserver_obj = dpt_models.TResourcePoolServer.objects.filter(resource_pool_id=self.parameters('resource_pool_id'))
            for i in resourcepoolserver_obj:
                d = {
                    'pk': i.server_id.server_id,
                    'server_sn': i.server_id.asset_id.asset_sn,
                    'server_inip': ','.join(
                        [ii.ip.ip for ii in ip_models.TAssetIp.objects.filter(
                                                asset_id=i.server_id.asset_id,
                                                ip_id__ip_type=ip_models.TRealIp.IP_TYPE_MAPPING[u'内网'])
                        ]),
                    'server_type': i.server_id.get_server_type_display(),
                    'os_type':i.server_id.os_type_id.os_type_version,
                    'cpu': ','.join([j.cpu_capacity for j in i.server_id.asset_id.trealaccessory_set.all()]),
                    'disk': ','.join([j.disk_capacity for j in i.server_id.asset_id.trealaccessory_set.all()])
                }
                if not i.busline_id:
                    d['buline'] = u'未分配'
                else:
                    d['buline'] = i.busline_id.busline_name
                data.append(d)
        except:
            raise APIError(-3000)
        return data

    @CheckParameters(['token'])
    def post_getresoursepool(self):
        try:
            data = []
            pool = dpt_models.TResourcePool.objects.all()
            for i in pool:
                #print i.resource_pool_id, i.resource_pool_name, i.description, i.create_time.strftime("%Y-%m-%d %H:%M:%S"), i.creater_id.nickname
                d = {
                    'pk': i.resource_pool_id,
                    'resource_pool_name': i.resource_pool_name,
                    'description': i.description,
                    'create_time': i.create_time.strftime("%Y-%m-%d"),
                    'creater_id': i.creater_id.nickname
                }
                data.append(d)

        except:
            raise APIError(-3000)
        return data


    @CheckParameters(['pool_name', 'description', 'token'])
    def post_createresoursepool(self):
        #print self.create_id()
        try:
            defaults_kwargs = {
            #'resource_pool_id': self.create_id(),
                'resource_pool_name': self.parameters('pool_name'),
                'description': self.parameters('description'),
                'create_time': datetime.now(),
                'state': 0,
                'creater_id': dpt_models.TBspUser.objects.filter(bsp_user_id='201103251403475eca8a86')[0]
                }
                #print defaults_kwargs
            obj = dpt_models.TResourcePool(**defaults_kwargs)
            obj.save()
        except:
            raise APIError(-3000)

    @CheckParameters(['pk','pool_name','token'])
    def post_addservertopool(self):
        try:
            server_obj = TServer.objects.filter(server_id=self.parameters('pk'))[0]

            defaults_kwargs = {
                'resource_pool_server_id': self.create_id(),
                'resource_pool_id': dpt_models.TResourcePool.objects.filter(resource_pool_id=self.parameters('pool_name'))[0],
                'server_id': server_obj,
                'add_time': datetime.now(),
                'bsp_user_id': dpt_models.TBspUser.objects.filter(bsp_user_id='201103251403475eca8a86')[0]
            }
            if dpt_models.TResourcePoolServer.objects.filter(server_id=server_obj):
                server_obj.server_operation_status=0
                server_obj.save()
            else:
                obj = dpt_models.TResourcePoolServer(**defaults_kwargs)
                obj.save()
                server_obj.server_operation_status=0
                server_obj.save()
            message=u'分配到资源池%s' % self.parameters('pool_name')
            self.setlog(asset=server_obj.asset_id, context=message)
        except:
            raise APIError(-3000)

    def post_getbaseresource(self):
        type = int(self.parameters('type'))
        data = [];
        # server_device_tincservertype          0       TIncServerType
        # server_device_tserverdevicetype       1       TServerDeviceType
        # server_device_tdeviceproducertype     2       TDeviceProducerType
        # server_device_tostype                 3       TOsType
        if type==0:
            result = TIncServerType.objects.all()
            for obj in result:
                dic = {

                    'id':obj.inc_server_type_id,
                    'name':obj.inc_server_code,
                    'code':obj.inc_server_type_name,
                    'status':obj.delete_status

                    }
                data.append(dic)

        elif type==1:
            result = TServerDeviceType.objects.all()
            for obj in result:

                deviceproduce = TDeviceProducerType.objects.get(device_producer_type_id=obj.device_producer_id_id)
                # print deviceproduce
                dic = {

                    'id':obj.server_type_id,
                    'code':obj.server_device_type_name,
                    'name':obj.server_hight,
                    'status':obj.delete_status,
                    'other':deviceproduce.producer_name,

                    }
                data.append(dic)

        elif type==2:
            result = TDeviceProducerType.objects.all()
            for obj in result:

                dic = {

                    'id':obj.device_producer_type_id,
                    'code':obj.producer_name,
                    'name':obj.device_type,
                    'status':obj.delete_status

                    }
                data.append(dic)

        elif type==3:
            result = TOsType.objects.all()
            for obj in result:

                dic = {

                    'id':obj.os_type_id,
                    'name':obj.os_type_name,
                    'code':obj.os_type_version,
                    'status':obj.delete_status,
                    'other':obj.os_kernerl_version

                    }
                data.append(dic)

        else:
            pass

        return data


    def post_savebaseresourcechange(self):
        type = int(self.parameters('type'))
        selectid = self.parameters('id')
        code = self.parameters('code')
        name = self.parameters('name')
        other = self.parameters('other')

        if type==0:

            result = None;
            if selectid:
                result = TIncServerType.objects.get(inc_server_type_id=selectid)
            else:
                selectid = self.create_id()
                result = TIncServerType.objects.create(inc_server_type_id=selectid, delete_status=0)


            result.inc_server_code = name
            result.inc_server_type_name = code
            result.delete_status = 0
            result.save()

        elif type==1:

            result = None;
            if selectid:
                result = TServerDeviceType.objects.get(server_type_id=selectid)
            else:
                selectid = self.create_id()
                result = TServerDeviceType.objects.create(server_type_id=selectid)

            deviceproduce = TDeviceProducerType.objects.get(device_producer_type_id=other)

            result.device_producer_id = deviceproduce
            result.server_device_type_name = code
            result.server_hight = name
            result.delete_status = 0
            result.save()

        elif type==2:

            result = None;
            if selectid:
                result = TDeviceProducerType.objects.get(device_producer_type_id=selectid)
            else:
                selectid = self.create_id()
                result = TDeviceProducerType.objects.create(device_producer_type_id=selectid)

            result.producer_name = code
            result.device_type = name
            result.delete_status = 0
            result.save()

        elif type==3:

            result = None;
            if selectid:
                result = TOsType.objects.get(os_type_id=selectid)
            else:
                selectid = self.create_id()
                result = TOsType.objects.create(os_type_id=selectid)

            result.os_type_name = name
            result.os_type_version = code
            result.delete_status = 0
            result.os_kernerl_version = other
            result.save()

        else:
            pass


    def post_getproducerdata(self):

        deviceproduces = TDeviceProducerType.objects.all()
        data = []
        for obj in deviceproduces:
            dic = {

                'id': obj.device_producer_type_id,
                'text': obj.producer_name

            }
            data.append(dic)
        return data

class Logger(CoreView):

    @CheckParameters(['server_pk', 'token'])
    def post_serverlog(self):
        """日志查询"""
        server_log_obj = AssetLog.objects.filter(asset_id=self.parameters('server_pk'))
        data=[]
        for i in server_log_obj:
            info = {
                    'pk': i.logid,
                    'num': i.asset_id.asset_num,
                    'las_time': i.update_time.strftime("%Y-%m-%d %H:%M:%S"),
                    'context': i.context,
                    'auther': ""
                    }
            data.append(info)
        return data


class Upload(CoreView):

    def post_serverasset(self):
        try:
            file_name = self.request.FILES['title'].name.split('.')[-1]
        except:
            raise APIError(-1002)
        if 'title' in self.request.FILES and (file_name == 'xlsx'):
            data = handle_uploaded_file(self.request.FILES['title'])
            """server表中第0个sheet为服务器表+资产表+OS表+厂商表"""
            table = data.sheets()[0]
            error_row=[]
            for i in xrange(1,table.nrows):
                try:
                    defaults_kwargs = {
                        'asset_id':self.create_id(),
                        'asset_sn':table.row_values(i)[0],
                        'asset_num':table.row_values(i)[1],
                        'asset_status':TAsset.ASSET_STATUS_MAPPING[table.row_values(i)[6]],
                        'device_type':TAsset.DEVICE_TYPE_MAPPING[table.row_values(i)[8]],
                        'asset_operator_org_id':table.row_values(i)[9],
                        'asset_comment':table.row_values(i)[10],
                    }
                    if table.row_values(i)[2]:
                        defaults_kwargs['asset_warranty_due_time'] = datetime.strptime(table.row_values(i)[2],'%Y-%m-%d')
                    if table.row_values(i)[3]:
                        defaults_kwargs['asset_receipt_time'] = datetime.strptime(table.row_values(i)[3],'%Y-%m-%d')
                    if table.row_values(i)[4]:
                        defaults_kwargs['asset_on_shelf_time'] = datetime.strptime(table.row_values(i)[4],'%Y-%m-%d')
                    if table.row_values(i)[5]:
                        defaults_kwargs['asset_off_shelf_time'] = datetime.strptime(table.row_values(i)[5],'%Y-%m-%d')
                    if table.row_values(i)[7] and (table.row_values(i)[23] != u'虚拟机'):
                        defaults_kwargs['position_id'] = idc_models.TPosition.objects.filter( \
                                                    position_num=int(table.row_values(i)[7].split('-')[2]),\
                                                    rack_id__rack_code=table.row_values(i)[7].split('-')[1],\
                                                    rack_id__rack_name=table.row_values(i)[7].split('-')[0]\
                                                    ).exclude(delete_status=db_code_mapping['delete'])[0]
                except:
                    error_row.append(i+1)
                    continue

                kwargs = {'asset_sn':table.row_values(i)[0],
                        'asset_num':table.row_values(i)[1],
                        'device_type':TAsset.DEVICE_TYPE_MAPPING[table.row_values(i)[8]],
                        'defaults':defaults_kwargs}

                try:
                    data_obj, created = TAsset.objects.exclude(delete_status=db_code_mapping['delete']).get_or_create(**kwargs)
                    if not created:
                        del defaults_kwargs['asset_id']
                        if table.row_values(i)[7]:
                            data_obj.position_id=defaults_kwargs['position_id']
                        data_obj.__dict__.update(**defaults_kwargs)
                        data_obj.save()
                except:
                    error_row.append(i+1)
                    continue

            """厂商表"""
            for i in xrange(1,table.nrows):
                try:
                    defaults_kwargs = {
                        'device_producer_type_id':self.create_id(),
                        'producer_name':table.row_values(i)[21],
                        'device_type':TDeviceProducerType.DEVICE_TYPE_MAPPING[table.row_values(i)[22]],
                    }
                except:
                    error_row.append(i)
                    continue

                kwargs = {
                        'producer_name':table.row_values(i)[21],
                        'device_type':TDeviceProducerType.DEVICE_TYPE_MAPPING[table.row_values(i)[22]],
                        'defaults':defaults_kwargs
                        }
                try:
                    data_obj, created = TDeviceProducerType.objects.exclude(delete_status=db_code_mapping['delete']).get_or_create(**kwargs)
                    if not created:
                        del defaults_kwargs['device_producer_type_id']
                        data_obj.__dict__.update(**defaults_kwargs)
                        data_obj.save()
                except:
                    error_row.append(i)
                    continue

            """OS表"""
            for i in xrange(1,table.nrows):
                try:
                    defaults_kwargs = {
                        'os_type_id':self.create_id(),
                        'os_type_name':table.row_values(i)[17],
                        'os_type_version':table.row_values(i)[18],
                        'os_kernerl_version':table.row_values(i)[16],
                    }
                except:
                    error_row.append(i)
                    continue

                kwargs = {'os_type_name':table.row_values(i)[17],
                        'os_type_version':table.row_values(i)[18],
                        'os_kernerl_version':table.row_values(i)[16],
                        'defaults':defaults_kwargs}

                try:
                    data_obj, created = TOsType.objects.exclude(delete_status=db_code_mapping['delete']).get_or_create(**kwargs)
                    if not created:
                        del defaults_kwargs['os_type_id']
                        data_obj.__dict__.update(**defaults_kwargs)
                        data_obj.save()
                except:
                    error_row.append(i)
                    continue

            """服务器类型表"""
            for i in xrange(1,table.nrows):
                try:
                    defaults_kwargs = {
                        'server_type_id':self.create_id(),
                        'device_producer_id':TDeviceProducerType.objects.filter(
                            producer_name=table.row_values(i)[21],
                            device_type=TDeviceProducerType.DEVICE_TYPE_MAPPING[table.row_values(i)[22]],
                            ).exclude(delete_status=db_code_mapping['delete'])[0],
                        'server_device_type_name':table.row_values(i)[19],
                        'server_hight':table.row_values(i)[20],
                    }
                except:
                    error_row.append(i)
                    continue

                kwargs = {'server_device_type_name':table.row_values(i)[19],
                        'server_hight':table.row_values(i)[20],
                        'defaults':defaults_kwargs}

                try:
                    data_obj, created = TServerDeviceType.objects.exclude(delete_status=db_code_mapping['delete']).get_or_create(**kwargs)
                    if not created:
                        del defaults_kwargs['server_type_id']
                        data_obj.__dict__.update(**defaults_kwargs)
                        data_obj.save()
                except:
                    error_row.append(i)
                    continue

            """服务器表"""
            for i in xrange(1,table.nrows):
                try:
                    defaults_kwargs = {
                        'server_id':self.create_id(),
                        'server_health_status':TServer.SERVER_HEALTH_STATUS_MAPPING[table.row_values(i)[11]],
                        'server_run_status':TServer.SERVER_RUN_STATUS_MAPPING[table.row_values(i)[12]],
                        'server_operation_status':TServer.SERVER_OPERATION_STATUS_MAPPING[table.row_values(i)[13]],
                        'server_comment':table.row_values(i)[14],
                        'server_host_name':table.row_values(i)[15],
                        'asset_id':TAsset.objects.filter(asset_num=table.row_values(i)[1])[0],
                        'os_type_id':TOsType.objects.filter(
                               os_type_name=table.row_values(i)[17],
                               os_type_version=table.row_values(i)[18],
                               os_kernerl_version=table.row_values(i)[16],
                            )[0],
                        'server_device_type_id':TServerDeviceType.objects.filter(
                            server_device_type_name=table.row_values(i)[19],
                            server_hight=table.row_values(i)[20],
                            )[0],
                    }
                    if table.row_values(i)[23]:
                        defaults_kwargs['server_type']=TServer.SERVER_TYPE_MAPPING[table.row_values(i)[23]]
                    if table.row_values(i)[26]:
                        defaults_kwargs['inc_server_type_id']=TIncServerType.objects.filter(inc_server_type_name=table.row_values(i)[26])[0]
                except:
                    error_row.append(i)
                    continue

                kwargs = {'server_host_name':table.row_values(i)[15],
                        'defaults':defaults_kwargs}

                try:
                    data_obj, created = TServer.objects.exclude(delete_status=db_code_mapping['delete']).get_or_create(**kwargs)
                    if not created:
                        del defaults_kwargs['server_id']
                        data_obj.asset_id=defaults_kwargs['asset_id']
                        data_obj.os_type_id=defaults_kwargs['os_type_id']
                        data_obj.server_device_type_id=defaults_kwargs['server_device_type_id']
                        data_obj.inc_server_type_id=defaults_kwargs['inc_server_type_id']
                        data_obj.__dict__.update(**defaults_kwargs)
                        data_obj.save()
                except:
                    error_row.append(i)
                    continue

            """选型关系表"""
            for i in xrange(1,table.nrows):
                try:
                    defaults_kwargs = {
                        'server_selection_id':self.create_id(),
                        'inc_server_type':TIncServerType.objects.filter(inc_server_type_name=table.row_values(i)[26])[0],
                        'server_device_type':TServerDeviceType.objects.filter(
                                server_device_type_name=table.row_values(i)[19])[0]
                        }
                except:
                    error_row.append(i)
                    continue

                kwargs = {'inc_server_type':TIncServerType.objects.filter(inc_server_type_name=table.row_values(i)[26])[0],
                          'server_device_type':TServerDeviceType.objects.filter(
                                                server_device_type_name=table.row_values(i)[19],
                                            )[0],
                          'defaults':defaults_kwargs}
                try:
                    data_obj, created = TServerSelection.objects.exclude(delete_status=db_code_mapping['delete']).get_or_create(**kwargs)
                    if not created:
                        del defaults_kwargs['server_selection_id']
                        data_obj.inc_server_type=defaults_kwargs['inc_server_type']
                        data_obj.server_device_type=defaults_kwargs['server_device_type']
                        data_obj.__dict__.update(**defaults_kwargs)
                        data_obj.save()
                except:
                    error_row.append(i)
                    continue

            if error_row:
                raise APIError(-1, error_row)
            else:
                raise APIError(0, u"上传成功!")
        else:
            raise APIError(-1, u"文件非法!")
