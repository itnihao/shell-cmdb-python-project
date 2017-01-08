from django.shortcuts import render
from django.http import HttpResponse
from django.core import serializers
from models import *
from public.APIViews import CoreView
from public.Exceptions import APIError
from public.Check import CheckParameters
import json
from datetime import datetime
from public.Syskeywords import db_code_mapping


class NetDevice(CoreView):
    '''
    NetDevice action class;
    '''
    def get_getnetdeviceinfobyid(self):
        '''
        Get request return NetDevice by id;
        error code -3000
        '''
        try:
            net_device_obj = TNetDevice.objects.filter(net_device_id=self.url_parameters('id')).exclude(delete_status=db_code_mapping['delete'])
        except:
            raise APIError(-3000)
        data = serializers.serialize("json", net_device_obj)
        return data

    @CheckParameters(['id'])
    def post_delnetdeviceinfobyid(self):
        try:
            net_device_obj = TNetDevice.objects.filter(net_device_id=self.parameters('id')).exclude(delete_status=db_code_mapping['delete'])[0]
            net_device_obj.delete_status = db_code_mapping['delete']
            net_device_obj.save()
        except:
            raise APIError(-3000)
        return {'id':net_device_obj.net_device_id}


    @CheckParameters(['net_device_name','asset','device_level','t_net_devicecol'])
    def post_addnetdevice(self):
        '''
        Post request add NetDevice;
        decorator CheckParameters for check json header
        '''
        try:
            kwargs = {
                    'net_device_id':self.create_id(),
                    'net_device_name':self.parameters('net_device_name'),
                    'asset':TAsset.objects.filter(asset_id=self.parameters('asset'))[0],
                    'device_level':self.parameters('device_level'),
                    't_net_devicecol':self.parameters('t_net_devicecol'),
                    }
            obj = TNetDevice(**kwargs)
            obj.save()
        except:
            raise APIError(-3000)
        return {'id':obj.net_device_id}


    @CheckParameters(['id','net_device_name','asset','device_level','t_net_devicecol'])
    def post_updatenetdeviceinfobyid(self):
        try:
            net_device_obj = TNetDevice.objects.filter(net_device_id=self.url_parameters('id')).exclude(delete_status=db_code_mapping['delete'])
            kwargs = {
                    'net_device_name':self.parameters('net_device_name'),
                    'asset':TAsset.objects.filter(asset_id=self.parameters('asset'))[0],
                    'device_level':self.parameters('device_level'),
                    't_net_devicecol':self.parameters('t_net_devicecol'),
                    }
            net_device_obj.update(**kwargs)
        except:
            raise APIError(-3000)
        return {'id':net_device_obj.net_device_id}

class IdcModule(CoreView):
    '''
    IdcModule action class;
    '''
    def get_getidcmoduleinfobyid(self):
        '''
        Get request return IdcModule by id;
        error code -3000
        '''
        try:
            module_obj = TIdcModule.objects.filter(module_id=self.url_parameters('id')).exclude(delete_status=db_code_mapping['delete'])
        except:
            raise APIError(-3000)
        data = serializers.serialize("json", module_obj)
        return data

    @CheckParameters(['id'])
    def post_delidcmoduleinfobyid(self):
        try:
            module_obj = TIdcModule.objects.filter(module_id=self.parameters('id')).exclude(delete_status=db_code_mapping['delete'])[0]
            module_obj.delete_status = db_code_mapping['delete']
            module_obj.save()
        except:
            raise APIError(-3000)
        return {'id':module_obj.module_id}


    @CheckParameters(['module_name'])
    def post_addidcmodule(self):
        '''
        Post request add IdcModule;
        decorator CheckParameters for check json header
        '''
        try:
            kwargs = {
                    'module_id':self.create_id(),
                    'module_name':self.parameters('module_name'),
                    }
            obj = TIdcModule(**kwargs)
            obj.save()
        except:
            raise APIError(-3000)
        return {'id':obj.module_id}


    @CheckParameters(['id','module_name'])
    def post_updateidcmoduleinfobyid(self):
        try:
            module_obj = TIdcModule.objects.filter(module_id=self.url_parameters('id')).exclude(delete_status=db_code_mapping['delete'])
            kwargs = {
                     'module_name':self.parameters('module_name'),
                    }
            module_obj.update(**kwargs)
        except:
            raise APIError(-3000)
        return {'id':module_obj.module_id}

class NicPort(CoreView):
    '''
    NicPort action class;
    '''
    def get_getnicportinfobyid(self):
        '''
        Get request return NicPort by id;
        error code -3000
        '''
        try:
            nic_port_obj = TNicPort.objects.filter(nic_port_id=self.url_parameters('id')).exclude(delete_status=db_code_mapping['delete'])
        except:
            raise APIError(-3000)
        data = serializers.serialize("json", nic_port_obj)
        return data

    @CheckParameters(['id'])
    def post_delnicportinfobyid(self):
        try:
            nic_port_obj = TNicPort.objects.filter(nic_port_id=self.parameters('id')).exclude(delete_status=db_code_mapping['delete'])[0]
            nic_port_obj.delete_status = db_code_mapping['delete']
            nic_port_obj.save()
        except:
            raise APIError(-3000)
        return {'id':nic_port_obj.nic_port_id}


    @CheckParameters(['nic_port_name','nic_port_speed','nic_port_transfer_medium','nic_port_bandwidth','nic_port_mode','nic_port_link_type','asset','nic_port_num','nic_port_level','nic_port_planned_position'])
    def post_addnicport(self):
        '''
        Post request add NicPort;
        decorator CheckParameters for check json header
        '''
        try:
            kwargs = {
                    'nic_port_id':self.create_id(),
                    'nic_port_name':self.parameters('nic_port_name'),
                    'nic_port_speed':self.parameters('nic_port_speed'),
                    'nic_port_transfer_medium':self.parameters('nic_port_transfer_medium'),
                    'nic_port_bandwidth':self.parameters('nic_port_bandwidth'),
                    'nic_port_mode':self.parameters('nic_port_mode'),
                    'nic_port_link_type':self.parameters('nic_port_link_type'),
                    'asset':TAsset.objects.filter(asset_id=self.parameters('asset'))[0],
                    'nic_port_num':self.parameters('nic_port_num'),
                    'nic_port_level':self.parameters('nic_port_level'),
                    'nic_port_planned_position':TPosition.objects.filter(position_id=self.parameters('nic_port_planned_position'))[0],
                    }
            obj = TNicPort(**kwargs)
            obj.save()
        except:
            raise APIError(-3000)
        return {'id':obj.nic_port_id}


    @CheckParameters(['id','nic_port_name','nic_port_speed','nic_port_transfer_medium','nic_port_bandwidth','nic_port_mode','nic_port_link_type','asset','nic_port_num','nic_port_level','nic_port_planned_position'])
    def post_updatenicportinfobyid(self):
        try:
            nic_port_obj = TNicPort.objects.filter(nic_port_id=self.url_parameters('id')).exclude(delete_status=db_code_mapping['delete'])
            kwargs = {
                    'nic_port_name':self.parameters('nic_port_name'),
                    'nic_port_speed':self.parameters('nic_port_speed'),
                    'nic_port_transfer_medium':self.parameters('nic_port_transfer_medium'),
                    'nic_port_bandwidth':self.parameters('nic_port_bandwidth'),
                    'nic_port_mode':self.parameters('nic_port_mode'),
                    'nic_port_link_type':self.parameters('nic_port_link_type'),
                    'asset':TAsset.objects.filter(asset_id=self.parameters('asset'))[0],
                    'nic_port_num':self.parameters('nic_port_num'),
                    'nic_port_level':self.parameters('nic_port_level'),
                    'nic_port_planned_position':TPosition.objects.filter(position_id=self.parameters('nic_port_planned_position'))[0],
                    }
            nic_port_obj.update(**kwargs)
        except:
            raise APIError(-3000)
        return {'id':nic_port_obj.nic_port_id}


class NicPortLink(CoreView):
    '''
    NicPortLink action class;
    '''
    def get_getnicportlinkinfobyid(self):
        '''
        Get request return NicPortLink by id;
        error code -3000
        '''
        try:
            nic_port_link_obj = TNicPortLink.objects.filter(nic_port_link_id=self.url_parameters('id')).exclude(delete_status=db_code_mapping['delete'])
        except:
            raise APIError(-3000)
        data = serializers.serialize("json", nic_port_link_obj)
        return data

    @CheckParameters(['id'])
    def post_delnicportlinkinfobyid(self):
        try:
            nic_port_link_obj = TNicPortLink.objects.filter(nic_port_link_id=self.parameters('id')).exclude(delete_status=db_code_mapping['delete'])[0]
            nic_port_link_obj.delete_status = db_code_mapping['delete']
            nic_port_link_obj.save()
        except:
            raise APIError(-3000)
        return {'id':nic_port_link_obj.nic_port_link_id}


    @CheckParameters(['nic_port_id_upper','nic_port_id_lower','cable_type'])
    def post_addnicportlink(self):
        '''
        Post request add NicPortLink;
        decorator CheckParameters for check json header
        '''
        try:
            kwargs = {
                    'nic_port_link_id':self.create_id(),
                    'nic_port_id_upper':TNicPort.objects.filter(nic_port_id=self.parameters('nic_port_id_upper'))[0],
                    'nic_port_id_lower':TNicPort.objects.filter(nic_port_id=self.parameters('nic_port_id_lower'))[0],
                    'cable_type':self.parameters('cable_type'),
                    }
            obj = TNicPortLink(**kwargs)
            obj.save()
        except:
            raise APIError(-3000)
        return {'id':obj.nic_port_link_id}


    @CheckParameters(['id','nic_port_id_upper','nic_port_id_lower','cable_type'])
    def post_updatenicportlinkinfobyid(self):
        try:
            nic_port_link_obj = TNicPortLink.objects.filter(nic_port_link_id=self.url_parameters('id')).exclude(delete_status=db_code_mapping['delete'])
            kwargs = {
                    'nic_port_id_upper':TNicPort.objects.filter(nic_port_id=self.parameters('nic_port_id_upper'))[0],
                    'nic_port_id_lower':TNicPort.objects.filter(nic_port_id=self.parameters('nic_port_id_lower'))[0],
                    'cable_type':self.parameters('cable_type'),
                    }
            nic_port_link_obj.update(**kwargs)
        except:
            raise APIError(-3000)
        return {'id':nic_port_link_obj.nic_port_link_id}
