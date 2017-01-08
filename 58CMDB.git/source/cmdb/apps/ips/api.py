# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.http import HttpResponse
from django.core import serializers
from models import *
from django.db.models import Q
from public.APIViews import CoreView
from public.Exceptions import APIError
from public.Check import CheckParameters
import json
from datetime import datetime
from public.File import handle_uploaded_file
from apps.server_device import models as server_models
from public.Syskeywords import db_code_mapping

class Ip(CoreView):

    @CheckParameters(['token','ip','iptype','assetsn','startnum','range'])
    def post_searchipinfo(self):
        '''
        按条件搜索IP数据
        '''
        try:
            ips = self.parameters('ip').split(',')
            iptype = self.parameters('iptype')
            assetsns = self.parameters('assetsn').split(',')
            startnum = self.parameters('startnum')
            rangeid = self.parameters('range')
            if not iptype:
                iptype = [0,1,2]
        except:
            raise APIError(-3000)

        if not startnum:
            startnum = 0
        if not rangeid:
            rangeid = 10
        endnum = startnum+rangeid

        query = Q()
        if ips != [u'']:
            query = query | Q(
                    ip__ip__in=ips,
                    ip__ip_type__in=iptype
                )
        if assetsns != [u'']:
            query = query | Q(
                    asset__asset_num__in=assetsns,
                    ip__ip_type__in=iptype
                )
        if query == Q():
            ip_obj = TAssetIp.objects.all().exclude(delete_status=db_code_mapping['delete'])
        else:
            ip_obj = TAssetIp.objects.filter(
                    query
                    ).exclude(delete_status=db_code_mapping['delete']).distinct()

        data=[]
        for i in ip_obj[startnum:endnum]:
            info = {
                'pk':i.asset.asset_id,
                'sn':i.asset.asset_sn,
                'ip':i.ip.ip,
                'gateway':i.ip.gateway,
                'mask':i.ip.mask,
                'ip_type':i.ip.get_ip_type_display(),
                'mac':i.ip.mac
                }
            data.append(info)
        return data

class Upload(CoreView):

    def post_ip(self):
        try:
            file_name = self.request.FILES['title'].name.split('.')[-1]
        except:
            raise APIError(-1002)
        if 'title' in self.request.FILES and (file_name == 'xlsx'):
            data = handle_uploaded_file(self.request.FILES['title'])
            """server表中第2个sheet为ip表"""
            table = data.sheets()[1]
            error_row=[]
            for i in xrange(1,table.nrows):
                try:
                    #obj = server_models.TAsset.objects.filter(asset_num=table.row_values(i)[0]).exclude(delete_status=db_code_mapping['delete'])[0]
                    defaults_kwargs = {
                        'ip_id':self.create_id(),
                        'ip':table.row_values(i)[1],
                        'gateway':table.row_values(i)[2],
                        'mask':table.row_values(i)[4],
                        'ip_type':TRealIp.IP_TYPE_MAPPING[table.row_values(i)[5]],
                        'mac': table.row_values(i)[3],
                        }
                except:
                    error_row.append(i)
                    continue

                kwargs = {'ip':table.row_values(i)[1],'ip_type':TRealIp.IP_TYPE_MAPPING[table.row_values(i)[5]], 'defaults':defaults_kwargs}
                try:
                    data_obj, created = TRealIp.objects.exclude(delete_status=db_code_mapping['delete']).get_or_create(**kwargs)
                    if not created:
                        del defaults_kwargs['ip_id']
                        data_obj.__dict__.update(**defaults_kwargs)
                        data_obj.save()
                except:
                    error_row.append(i)
                    continue

                try:
                    server_obj = server_models.TAsset.objects.filter(asset_num=table.row_values(i)[0]).exclude(delete_status=db_code_mapping['delete'])[0]
                    #ip_obj is data_obj
                    defaults_kwargs = {
                        'assetip_id': self.create_id(),
                        'ip': data_obj,
                        'asset': server_obj
                    }
                    kwargs = {'ip': data_obj, 'asset': server_obj, 'defaults': defaults_kwargs}
                    data_obj, created = TAssetIp.objects.exclude(delete_status=db_code_mapping['delete']).get_or_create(**kwargs)
                    if not created:
                        del defaults_kwargs['assetip_id']
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
