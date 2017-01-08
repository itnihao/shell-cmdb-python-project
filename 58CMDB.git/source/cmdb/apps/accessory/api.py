# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.http import HttpResponse
from django.core import serializers
from models import *
from apps.server_device import models as server_models
from public.APIViews import CoreView
from public.Exceptions import APIError
from public.Check import CheckParameters
import json
from datetime import datetime
from public.Syskeywords import db_code_mapping
from public.File import handle_uploaded_file

class Upload(CoreView):

    def post_accessory(self):
        try:
            file_name = self.request.FILES['title'].name.split('.')[-1]
        except:
            raise APIError(-1002)
        if 'title' in self.request.FILES and (file_name == 'xlsx'):
            data = handle_uploaded_file(self.request.FILES['title'])
            """server表中第3个sheet为配件表"""
            table = data.sheets()[2]
            error_row=[]
            for i in xrange(1,table.nrows):
                try:
                    defaults_kwargs = {
                        'accessory_id':self.create_id(),
                        'cpu_capacity':table.row_values(i)[1],
                        'asset_num':server_models.TAsset.objects.filter(asset_num=table.row_values(i)[0]).exclude(delete_status=db_code_mapping['delete'])[0],
                        'memory_capacity':table.row_values(i)[4],
                        'net_card_capacity':table.row_values(i)[2],
                        'disk_capacity':table.row_values(i)[3],
                        'cpu_info':table.row_values(i)[5],
                        'memory_info':table.row_values(i)[8],
                        'disk_info':table.row_values(i)[7],
                        'net_card_info':table.row_values(i)[6],
                    }
                except:
                    error_row.append(i)
                    continue

                kwargs = {'asset_num':server_models.TAsset.objects.filter(asset_num=table.row_values(i)[0]).exclude(delete_status=db_code_mapping['delete'])[0],
                        'defaults':defaults_kwargs}
                try:
                    data_obj, created = TRealaccessory.objects.exclude(delete_status=db_code_mapping['delete']).get_or_create(**kwargs)
                    if not created:
                        del defaults_kwargs['accessory_id']
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
