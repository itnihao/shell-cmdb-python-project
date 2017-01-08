# -*- coding: utf-8 -*-

from django.shortcuts import render
from django.http import HttpResponse
from django.core import serializers
from models import *
from apps.server_device import models as server_models
from apps.dpt import models as dpt_models
from public.APIViews import CoreView
from public.Exceptions import APIError
from public.Check import CheckParameters
import json
from datetime import datetime
from public.Syskeywords import db_code_mapping
from public.File import handle_uploaded_file


class Idc(CoreView):

    @CheckParameters(['token'])
    def post_getidcinfoall(self):
        try:
            idc_obj = TIdc.objects.all().exclude(delete_status=db_code_mapping['delete'])
        except:
            raise APIError(-3000)
        data = serializers.serialize("json", idc_obj)
        return data

    @CheckParameters(['token','type_id','cpu_type','mem_type','disk_type'])
    def post_getrackbufferbyidc(self):
        idc_id=rack_id=position_id=None
        try:
            id_value=str(self.parameters('type_id')).split('_')
            if len(id_value) == 1:
                idc_id=id_value[0]
                data_type="idc"
            elif len(id_value) == 2:
                idc_id,rack_id=id_value
                data_type="rack"
            else:
                idc_id,rack_id,position_id=id_value
                data_type="position"
        except:
            raise APIError(-1001)

        try:
            server_objs=server_models.TServer.objects.filter(
                    server_operation_status=1,
                    server_health_status=0,
                    asset_id__position_id__rack_id__idc_id=idc_id,
                    ).exclude(delete_status=db_code_mapping['delete'])
        except:
            raise APIError(-3000)

        kwarg = {}
        data=[]
        if self.parameters('cpu_type'):
            kwarg['cpu_capacity']=self.parameters('cpu_type')
        if self.parameters('mem_type'):
            kwarg['memory_capacity']=self.parameters('mem_type')
        if self.parameters('disk_type'):
            kwarg['disk_capacity']=self.parameters('disk_type')
        for server_obj in server_objs:
            accessorys=server_obj.asset_id.trealaccessory_set.filter(
                    **kwarg
                )
            for accessory in accessorys:
                if idc_id and (not rack_id) and (not position_id):
                    data.append({"sn":accessory.sn.asset_sn,
                        "position_num":accessory.sn.position_id.position_num,
                        "rack_code":accessory.sn.position_id.rack_id.rack_code})
                    continue
                if rack_id and (accessory.sn.position_id.rack_id.rack_code == rack_id) and not position_id:
                    data.append({"sn":accessory.sn.asset_sn,
                        "position_num":accessory.sn.position_id.position_num,
                        "rack_code":accessory.sn.position_id.rack_id.rack_code})
                    continue
                if (accessory.sn.position_id.rack_id.rack_code == rack_id) and (accessory.sn.position_id.position_num == int(position_id)):
                    data.append({"sn":accessory.sn.asset_sn,
                        "position_num":accessory.sn.position_id.position_num,
                        "rack_code":accessory.sn.position_id.rack_id.rack_code})
                    continue

        return [{"data_type":data_type},data]

class Upload(CoreView):

    def post_idc(self):
        try:
            file_name = self.request.FILES['title'].name.split('.')[1]
        except:
            raise APIError(-1002)
        if 'title' in self.request.FILES and (file_name == 'xlsx'):
            data = handle_uploaded_file(self.request.FILES['title'])
            """idc表中第0个sheet为idc表"""
            table = data.sheets()[0]
            error_row=[]
            for i in xrange(1,table.nrows):
                defaults_kwargs = {
                   'idc_id':self.create_id(),
                   'idc_region':table.row_values(i)[0],
                   'idc_zone':table.row_values(i)[1],
                   'idc_campus':table.row_values(i)[2],
                   'idc_name':table.row_values(i)[3],
                   'idc_address':table.row_values(i)[4],
                   'idc_supplier':table.row_values(i)[5],
                   'idc_resource_type': TIdc.IDC_RESOURCE_TYPE_MAPPING[table.row_values(i)[6]],
                   'idc_phone':table.row_values(i)[9],
                   'idc_fax':table.row_values(i)[10],
                   'idc_email':table.row_values(i)[11],
                   'idc_owner_master_id':dpt_models.TBspUser.objects.filter(account=table.row_values(i)[12])[0],
                   'idc_owner_backup_id':dpt_models.TBspUser.objects.filter(account=table.row_values(i)[13])[0],
                   'idc_contacts':table.row_values(i)[14],
                }

                if table.row_values(i)[7]:
                    defaults_kwargs['idc_enable_time']=datetime.strptime(table.row_values(i)[7],'%Y-%m-%d'),
                if table.row_values(i)[8]:
                    defaults_kwargs['idc_due_time']=datetime.strptime(table.row_values(i)[8],'%Y-%m-%d'),

                kwargs = {'idc_name':table.row_values(i)[3], 'defaults':defaults_kwargs}

                try:
                    data_obj, created = TIdc.objects.exclude(delete_status=db_code_mapping['delete']).get_or_create(**kwargs)
                    if not created:
                        del defaults_kwargs['idc_id']
                        data_obj.idc_owner_master_id=defaults_kwargs['idc_owner_master_id']
                        data_obj.idc_owner_backup_id=defaults_kwargs['idc_owner_backup_id']
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

    def post_rack(self):
        try:
            file_name = self.request.FILES['title'].name.split('.')[1]
        except:
            raise APIError(-1002)
        if 'title' in self.request.FILES and (file_name == 'xlsx'):
            data = handle_uploaded_file(self.request.FILES['title'])
            """idc表中第2个sheet为rack表"""
            table = data.sheets()[1]
            error_row=[]
            for i in xrange(1,table.nrows):
                try:
                    defaults_kwargs = {
                        'rack_id':self.create_id(),
                        'idc_id':TIdc.objects.filter(idc_name=table.row_values(i)[0]).exclude(delete_status=db_code_mapping['delete'])[0],
                        'rack_name':table.row_values(i)[1],
                        'rack_code':table.row_values(i)[2],
                        'rack_depth':int(table.row_values(i)[3]),
                        'rack_height':int(table.row_values(i)[4]),
                        'rack_width':int(table.row_values(i)[5]),
                        'rack_spec_height': table.row_values(i)[6],
                        'rack_energy_type':TRack.RACK_ENERGY_TYPE_MAPPING[table.row_values(i)[7]],
                        'rack_power_max':int(table.row_values(i)[8]),
                        'rack_power_rating':int(table.row_values(i)[9]),
                        'rack_virtualization':TRack.FLAG_MAPPING[table.row_values(i)[10]],
                        'rack_extranet':TRack.FLAG_MAPPING[table.row_values(i)[11]],
                        }
                except:
                    error_row.append(i)
                    continue

                kwargs = {'rack_name':table.row_values(i)[1],'rack_code':table.row_values(i)[2], 'defaults':defaults_kwargs}
                try:
                    data_obj, created = TRack.objects.exclude(delete_status=db_code_mapping['delete']).get_or_create(**kwargs)
                    if not created:
                        del defaults_kwargs['rack_id']
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

    def post_position(self):
        try:
            file_name = self.request.FILES['title'].name.split('.')[1]
        except:
            raise APIError(-1002)
        if 'title' in self.request.FILES and (file_name == 'xlsx'):
            data = handle_uploaded_file(self.request.FILES['title'])
            """idc表中第3个sheet为position表"""
            table = data.sheets()[2]
            error_row=[]
            for i in xrange(1,table.nrows):
                try:
                    rack_obj = TRack.objects.filter(
                            rack_name=table.row_values(i)[0].split('-')[0],
                            rack_code=table.row_values(i)[0].split('-')[1])\
                            .exclude(delete_status=db_code_mapping['delete'])[0]
                    defaults_kwargs = {
                        'position_id':self.create_id(),
                        'rack_id':rack_obj,
                        'position_num':int(table.row_values(i)[1]),
                        'position_spec_height':table.row_values(i)[2],
                        'position_status':TPosition.POSITION_STATUS_MAPPING[table.row_values(i)[3]],
                        'start_spec_height':int(table.row_values(i)[4]),
                        'position_comment': table.row_values(i)[5],
                        }
                except:
                    error_row.append(i)
                    continue

                kwargs = {'position_num':int(table.row_values(i)[1]),'rack_id':rack_obj, 'defaults':defaults_kwargs}
                try:
                    data_obj, created = TPosition.objects.exclude(delete_status=db_code_mapping['delete']).get_or_create(**kwargs)
                    if not created:
                        del defaults_kwargs['position_id']
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
