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


class Accessory(CoreView):
    '''
    Accessory action class;
    '''
    def get_getaccessoryinfobyid(self):
        '''
        Get request return Accessory by id;
        error code -3000
        '''
        try:
            obj = TAccessory.objects.filter(accessory_id=self.url_parameters('id')).exclude(delete_status=db_code_mapping['delete'])
        except:
            raise APIError(-3000)
        data = serializers.serialize("json", obj)
        return data

    @CheckParameters(['id'])
    def post_delaccessoryinfobyid(self):
        try:
            obj = TAccessory.objects.filter(accessory_id=self.parameters('id')).exclude(delete_status=db_code_mapping['delete'])[0]
            obj.delete_status = db_code_mapping['delete']
            obj.save()
        except:
            raise APIError(-3000)
        return {'id':obj.accessory_id}


    @CheckParameters(['accessory_status','idc_id','sn','enable_time','due_time','accessory_type','store','asset','brand'])
    def post_addaccessory(self):
        '''
        Post request add Accessory;
        decorator CheckParameters for check json header
        '''
        try:
            kwargs = {
                    'accessory_id':self.create_id(),
                    'idc_id':self.parameters('idc_id'),
                    'accessory_status':self.parameters('accessory_status'),
                    'sn':self.parameters('sn'),
                    'enable_time':datetime.strptime(self.parameters('enable_time'),'%Y-%m-%d'),
                    'due_time':datetime.strptime(self.parameters('due_time'),'%Y-%m-%d'),
                    'accessory_type':TAccessoryType.objects.filter(accessory_type_id=self.parameters('accessory_type'))[0],
                    'asset':TAsset.objects.filter(asset_id=self.parameters('asset'))[0],
                    'brand':TAccessoryBrand.objects.filter(brand_id=self.parameters('brand'))[0],
                    'store':TAccessoryStore.objects.filter(accessory_store_id=self.parameters('store'))[0]
                    }
            obj = TAccessory(**kwargs)
            obj.save()
        except:
            raise APIError(-3000)
        return {'id':obj.accessory_id}


    @CheckParameters(['id','accessory_status','idc_id','sn','enable_time','due_time','accessory_type','store','asset','brand'])
    def post_updateaccessoryinfobyid(self):
        try:
            obj = TAccessory.objects.filter(accessory_id=self.parameters('id')).exclude(delete_status=db_code_mapping['delete'])
            kwargs = {
                    'idc_id':self.parameters('idc_id'),
                    'accessory_status':self.parameters('accessory_status'),
                    'sn':self.parameters('sn'),
                    'enable_time':datetime.strptime(self.parameters('enable_time'), '%Y-%m-%d'),
                    'due_time':datetime.strptime(self.parameters('due_time'), '%Y-%m-%d'),
                    'accessory_type':TAccessoryType.objects.filter(accessory_type_id=self.parameters('accessory_type'))[0],
                    'asset':TAsset.objects.filter(asset_id=self.parameters('asset'))[0],
                    'brand':TAccessoryBrand.objects.filter(brand_id=self.parameters('brand'))[0],
                    'store':TAccessoryStore.objects.filter(accessory_store_id=self.parameters('store'))[0]
                    }
            obj.update(**kwargs)
        except:
            raise APIError(-3000)
        return {'id':obj.accessory_id}


class AccessoryBrand(CoreView):
    def get_getaccessorybrandbyid(self):
        try:
            obj = TAccessoryBrand.objects.filter(brand_id=self.url_parameters('id')).exclude(delete_status=db_code_mapping['delete'])
        except:
            raise APIError(-3000)
        data = serializers.serialize("json", obj)
        return data

    @CheckParameters(['id'])
    def post_delaccessorybrandbyid(self):
        try:
            obj = TAccessoryBrand.objects.filter(brand_id=self.parameters('id')).exclude(delete_status=db_code_mapping['delete'])[0]
            obj.delete_status = db_code_mapping['delete']
            obj.save()
        except:
            raise APIError(-3000)
        return {'id':obj.brand_id}

    @CheckParameters(['brand_name'])
    def post_addaccessorybrand(self):
        try:
            kwargs = {
                    'brand_id':self.create_id(),
                    'brand_name':self.parameters('brand_name')
            }
            obj = TAccessoryBrand(**kwargs)
            obj.save()
        except:
            raise APIError(-3000)
        return {'id':obj.brand_id}

    @CheckParameters(['brand_name','id'])
    def post_updateaccessorybrandbyid(self):
        try:
            obj = TAccessoryBrand.objects.filter(brand_id=self.parameters('id')).exclude(delete_status=db_code_mapping['delete'])
            kwargs = {
                    'brand_name':self.parameters('brand_name')
            }
            obj.update(**kwargs)
        except:
            raise APIError(-3000)
        return {'id':obj.brand_id}


class AccessoryStore(CoreView):
    def get_getaccessorystorebyid(self):
        try:
            obj = TAccessoryStore.objects.filter(accessory_store_id=url_parameters('id')).exclude(delete_status=db_code_mapping['delete'])
        except:
            raise APIError(-3000)
        data = serializers.serialize("json", obj)
        return data

    @CheckParameters(['id'])
    def post_delaccessorystorebyid(self):
        try:
            obj = TAccessoryStore.objects.filter(accessory_store_id=parameters('id')).exclude(delete_status=db_code_mapping['delete'])[0]
            obj.delete_status = db_code_mapping['delete']
            obj.save()
        except:
            raise APIError(-3000)
        return {'id':obj.accessory_store_id}

    @CheckParameters(['accessory_store_name','accessory_store_position','accessory_store_owner','accessory_idc'])
    def post_addaccessorystore(self):
        try:
            kwargs = {
                    'accessory_store_id':self.create_id(),
                    'accessory_store_name':self.parameters('accessory_store_name'),
                    'accessory_store_position':self.parameters('accessory_store_position'),
                    'accessory_store_owner':self.parameters('accessory_store_owner'),
                    'accessory_idc':TIdc.objects.filter(idc_id=self.parameters('idc_id'))[0]
            }
            obj = TAccessoryStore(kwargs)
            obj.save()
        except:
            raise APIError(-3000)
        return {'id':obj.accessory_store_id}

    @CheckParameters(['id','accessory_store_name','accessory_store_position','accessory_store_owner','accessory_idc'])
    def post_updateaccessorystorebyid(self):
        try:
            obj = TAccessoryStore.objects.filter(accessory_store_id=self.parameters('id')).exclude(delete_status=db_code_mapping['delete'])
            kwargs = {
                    'accessory_store_name':self.parameters('accessory_store_name'),
                    'accessory_store_position':self.parameters('accessory_store_position'),
                    'accessory_store_owner':self.parameters('accessory_store_owner'),
                    'accessory_idc':TIdc.objects.filter(idc_id=self.parameters('idc_id'))[0]
            }
            obj.update(**kwargs)
        except:
            raise APIError(-3000)
        return {'id':obj.accessory_store_id}


class AccessoryType(CoreView):
    def get_getaccessorytypebyid(self):
        try:
            obj = TAccessoryType.objects.filter(accessory_type_id=self.url_parameters('id')).exclude(delete_status=db_code_mapping['delete'])
        except:
            raise APIError(-3000)
        data = serializers.serialize("json", obj)
        return data

    @CheckParameters(['id'])
    def post_delaccessorytypebyid(self):
        try:
            obj = TAccessoryType.objects.filter(accessory_type_id=self.parameters('id')).exclude(delete_status=db_code_mapping['delete'])[0]
            obj.delete_status = db_code_mapping['delete']
            obj.save()
        except:
            raise APIError(-3000)
        return {'id':obj.accessory_type_id}

    @CheckParameters(['accessory_type_name'])
    def post_addaccessorytype(self):
        try:
            kwargs = {
                    'accessory_type_id':self.create_id(),
                    'accessory_type_name':self.parameters('accessory_type_name')
            }
            obj = TAccessoryType(**kwargs)
            obj.save()
        except:
            raise APIError(-3000)
        return {'id':obj.accessory_type_id}

    @CheckParameters(['id','accessory_type_name'])
    def post_updateaccessorytypebyid(self):
        try:
            obj = TAccessoryType.objects.filter(accessory_type_id=self.parameters('id')).exclude(delete_status=db_code_mapping['delete'])
            kwargs = {
                    'accessory_type_name':self.parameters('accessory_type_name')
            }
            obj.update(**kwargs)
        except:
            raise APIError(-3000)
        return {'id':obj.accessory_type_id}


class ArrayCard(CoreView):
    def get_getarraycardbyid(self):
        try:
            accessory_obj = TAccessory.objects.filter(accessory_id=self.url_parameters('id')).exclude(delete_status=db_code_mapping['delete'])[0]
            obj = TArrayCard.objects.filter(accessory=accessory_obj)
        except:
            raise APIError(-3000)
        data = serializers.serialize("json", obj)
        return data

    @CheckParameters(['id'])
    def post_delarraycardbyid(self):
        try:
            obj = TAccessory.objects.filter(accessory_id=self.url_parameters('id')).exclude(delete_status=db_code_mapping['delete'])[0]
            obj.delete_status = db_code_mapping['delete']
            obj.save()
        except:
            raise APIError(-3000)
        return {'id':obj.accessory_id}


    @CheckParameters(['id','array_card_interface','array_card_cache','array_card_buttery','comment','version','cache_status','strip_size','read_write_ratio','array_card_model'])
    def post_addarraycard(self):
        try:
            accessory_obj = TAccessory.objects.filter(accessory_id=self.parameters('id')).exclude(delete_status=db_code_mapping['delete'])[0]
            kwargs = {
                    'accessory':accessory_obj,
                    'array_card_interface':self.parameters('array_card_interface'),
                    'array_card_cache':self.parameters('array_card_cache'),
                    'array_card_buttery':self.parameters('array_card_buttery'),
                    'comment':self.parameters('comment'),
                    'version':self.parameters('version'),
                    'cache_status':self.parameters('cache_status'),
                    'strip_size':self.parameters('strip_size'),
                    'read_write_ratio':self.parameters('read_write_ratio'),
                    'array_card_model':self.parameters('array_card_model')
            }
            obj = TArrayCard(**kwargs)
            obj.save()
        except:
            raise APIError(-3000)
        return {'id':accessory_obj.accessory_id}


    @CheckParameters(['id','array_card_interface','array_card_cache','array_card_buttery','comment','version','cache_status','strip_size','read_write_ratio','array_card_model'])
    def post_updatearraycardbyid(self):
        try:
            accessory_obj = TAccessory.objects.filter(accessory_id=self.parameters('id')).exclude(delete_status=db_code_mapping['delete'])[0]
            obj = TArrayCard.objects.filter(accessory=accessory_obj)
            kwargs = {
                    'array_card_interface':self.parameters('array_card_interface'),
                    'array_card_cache':self.parameters('array_card_cache'),
                    'array_card_buttery':self.parameters('array_card_buttery'),
                    'comment':self.parameters('comment'),
                    'version':self.parameters('version'),
                    'cache_status':self.parameters('cache_status'),
                    'strip_size':self.parameters('strip_size'),
                    'read_write_ratio':self.parameters('read_write_ratio'),
                    'array_card_model':self.parameters('array_card_model')
            }
            obj.update(**kwargs)
        except:
            raise APIError(-3000)
        return {'id':accessory_obj.accessory_id}

class Cpu(CoreView):
    def get_getcpubyid(self):
        try:
            accessory_obj = TAccessory.objects.filter(accessory_id=self.url_parameters('id')).exclude(delete_status=db_code_mapping['delete'])[0]
            obj = TCpu.objects.filter(accessory=accessory_obj)
        except:
            raise APIError(-3000)
        data = serializers.serialize("json", obj)
        return data

    @CheckParameters(['id'])
    def post_delcpubyid(self):
        try:
            obj = TAccessory.objects.filter(accessory_id=self.parameters('id')).exclude(delete_status=db_code_mapping['delete'])[0]
            obj.delete_status = db_code_mapping['delete']
            obj.save()
        except:
            raise APIError(-3000)
        return {'id':obj.accessory_id}

    @CheckParameters(['id','cpu_model','cpu_core','cpu_frequency','cpu_power','comment','platform_type','cpu_ht_support','cpu_vm_support','cpu_memory_channel_num','cpu_max_num','cpu_node_support'])
    def post_addcpu(self):
        try:
            accessory_obj = TAccessory.objects.filter(accessory_id=self.parameters('id')).exclude(delete_status=db_code_mapping['delete'])[0]
            kwargs = {
                    'accessory':accessory_obj,
                    'cpu_model':self.parameters('cpu_model'),
                    'cpu_core':self.parameters('cpu_core'),
                    'cpu_frequency':self.parameters('cpu_frequency'),
                    'cpu_power':self.parameters('cpu_power'),
                    'comment':self.parameters('comment'),
                    'platform_type':self.parameters('platform_type'),
                    'cpu_ht_support':self.parameters('cpu_ht_support'),
                    'cpu_vm_support':self.parameters('cpu_vm_support'),
                    'cpu_memory_channel_num':self.parameters('cpu_memory_channel_num'),
                    'cpu_max_num':self.parameters('cpu_max_num'),
                    'cpu_node_support':self.parameters('cpu_node_support')
            }
            obj = TCpu(**kwargs)
            obj.save()
        except:
            raise APIError(-3000)
        return {'id':accessory_obj.accessory_id}

    @CheckParameters(['id','cpu_model','cpu_core','cpu_frequency','cpu_power','comment','platform_type','cpu_ht_support','cpu_vm_support','cpu_memory_channel_num','cpu_max_num','cpu_node_support'])
    def post_updatecpubyid(self):
        try:
            accessory_obj = TAccessory.objects.filter(accessory_id=self.parameters('id')).exclude(delete_status=db_code_mapping['delete'])[0]
            obj = TCpu.objects.filter(accessory=accessory_obj)
            kwargs = {
                    'cpu_model':self.parameters('cpu_model'),
                    'cpu_core':self.parameters('cpu_core'),
                    'cpu_frequency':self.parameters('cpu_frequency'),
                    'cpu_power':self.parameters('cpu_power'),
                    'comment':self.parameters('comment'),
                    'platform_type':self.parameters('platform_type'),
                    'cpu_ht_support':self.parameters('cpu_ht_support'),
                    'cpu_vm_support':self.parameters('cpu_vm_support'),
                    'cpu_memory_channel_num':self.parameters('cpu_memory_channel_num'),
                    'cpu_max_num':self.parameters('cpu_max_num'),
                    'cpu_node_support':self.parameters('cpu_node_support')
            }
            obj.update(**kwargs)
        except:
            raise APIError(-3000)
        return {'id':accessory_obj.accessory_id}

class Disk(CoreView):
    def get_getdiskbyid(self):
        try:
            accessory_obj = TAccessory.objects.filter(accessory_id=self.url_parameters('id')).exclude(delete_status=db_code_mapping['delete'])[0]
            obj = TDisk.objects.filter(accessory=accessory_obj)
        except:
            raise APIError(-3000)
        data = serializers.serialize("json", obj)
        return data

    @CheckParameters(['id'])
    def post_deldiskbyid(self):
        try:
            obj = TAccessory.objects.filter(accessory_id=self.parameters('id')).exclude(delete_status=db_code_mapping['delete'])[0]
            obj.delete_status = db_code_mapping['delete']
            obj.save()
        except:
            raise APIError(-3000)
        return {'id':obj.accessory_id}

    @CheckParameters(['id','disk_capacity','disk_interface','disk_model','disk_type'])
    def post_adddisk(self):
        try:
            accessory_obj = TAccessory.objects.filter(accessory_id=self.parameters('id')).exclude(delete_status=db_code_mapping['delete'])[0]
            kwargs = {
                    'accessory':accessory_obj,
                    'disk_capacity':self.parameters('disk_capacity'),
                    'disk_interface':self.parameters('disk_interface'),
                    'disk_speed':self.parameters('disk_speed'),
                    'comment':self.parameters('comment'),
                    'disk_model':self.parameters('disk_model'),
                    'version':self.parameters('version'),
                    'bandwidth':self.parameters('bandwidth'),
                    'iops':self.parameters('iops'),
                    'disk_type':self.parameters('disk_type'),
                    'disk_cache':self.parameters('disk_cache'),
                    'disk_chip':self.parameters('disk_chip'),
                    'disk_nand':self.parameters('disk_nand'),
                    'disk_nand_process':self.parameters('disk_nand_process')
            }
            obj = TDisk(**kwargs)
            obj.save()
        except:
            raise APIError(-3000)
        return {'id':accessory_obj.accessory_id}

    @CheckParameters(['id','disk_capacity','disk_interface','disk_model','disk_type'])
    def post_updatediskbyid(self):
        try:
            accessory_obj = TAccessory.objects.filter(accessory_id=self.parameters('id')).exclude(delete_status=db_code_mapping['delete'])[0]
            obj = TDisk.objects.filter(accessory=accessory_obj)
            kwargs = {
                    'disk_capacity':self.parameters('disk_capacity'),
                    'disk_interface':self.parameters('disk_interface'),
                    'disk_speed':self.parameters('disk_speed'),
                    'comment':self.parameters('comment'),
                    'disk_model':self.parameters('disk_model'),
                    'version':self.parameters('version'),
                    'bandwidth':self.parameters('bandwidth'),
                    'iops':self.parameters('iops'),
                    'disk_type':self.parameters('disk_type'),
                    'disk_cache':self.parameters('disk_cache'),
                    'disk_chip':self.parameters('disk_chip'),
                    'disk_nand':self.parameters('disk_nand'),
                    'disk_nand_process':self.parameters('disk_nand_process')
            }
            obj.update(**kwargs)
        except:
            raise APIError(-3000)
        return {'id':accessory_obj.accessory_id}

class Fan(CoreView):
    def get_getfanbyid(self):
        try:
            accessory_obj = TAccessory.objects.filter(accessory_id=self.url_parameters('id')).exclude(delete_status=db_code_mapping['delete'])[0]
            obj = TFan.objects.filter(accessory=accessory_obj)
        except:
            raise APIError(-3000)
        data = serializers.serialize("json", obj)
        return data

    def post_delfanbyid(self):
        try:
            obj = TAccessory.objects.filter(accessory_id=self.parameters('id')).exclude(delete_status=db_code_mapping['delete'])[0]
            obj.delete_status = db_code_mapping['delete']
            obj.save()
        except:
            raise APIError(-3000)
        return {'id':obj.accessory_id}

    @CheckParameters(['id','fan_redundancy_level','fan_max_speed','fan_auto_regulation_support','fan_position'])
    def post_addfan(self):
        try:
            accessory_obj = TAccessory.objects.filter(accessory_id=self.parameters('id')).exclude(delete_status=db_code_mapping['delete'])[0]
            kwargs = {
                    'accessory':accessory_obj,
                    'fan_redundancy_level':self.parameters('fan_redundancy_level'),
                    'fan_max_speed':self.parameters('fan_max_speed'),
                    'fan_auto_regulation_support':self.parameters('fan_auto_regulation_support'),
                    'fan_position':self.parameters('fan_position')
            }
            obj = TFan(**kwargs)
            obj.save()
        except:
            raise APIError(-3000)
        return {'id':accessory_obj.accessory_id}

    @CheckParameters(['id','fan_redundancy_level','fan_max_speed','fan_auto_regulation_support','fan_position'])
    def post_updatefanbyid(self):
        try:
            accessory_obj = TAccessory.objects.filter(accessory_id=self.parameters('id')).exclude(delete_status=db_code_mapping['delete'])[0]
            obj = TFan.objects.filter(accessory=accessory_obj)
            kwargs = {
                    'fan_redundancy_level':self.parameters('fan_redundancy_level'),
                    'fan_max_speed':self.parameters('fan_max_speed'),
                    'fan_auto_regulation_support':self.parameters('fan_auto_regulation_support'),
                    'fan_position':self.parameters('fan_position')
            }
            obj.update(**kwargs)
        except:
            raise APIError(-3000)
        return {'id':accessory_obj.accessory_id}

class Gpu(CoreView):

    def get_getgpubyid(self):
        try:
            accessory_obj = TAccessory.objects.filter(accessory_id=self.url_parameters('id')).exclude(delete_status=db_code_mapping['delete'])
            obj = TGpu.objects.filter(accessory=accessory_obj)
        except:
            raise APIError(-3000)
        data = serializers.serialize("json", obj)
        return data

    @CheckParameters(['id'])
    def post_delgpubyid(self):
        try:
            obj = TAccessory.objects.filter(accessory_id=self.parameters('id')).exclude(delete_status=db_code_mapping['delete'])[0]
            obj.delete_status = db_code_mapping['delete']
            obj.save()
        except:
            raise APIError(-3000)
        return {'id':obj.accessory_id}

    @CheckParameters(['id','gpu_core_num','gpu_memory','gpu_frequency','gpu_chip','gpu_memory_specs','gpu_power','gpu_idle_power','gpu_memory_bandwidth'])
    def post_addgpu(self):
        try:
            accessory_obj = TAccessory.objects.filter(accessory_id=self.parameters('id')).exclude(delete_status=db_code_mapping['delete'])[0]
            kwargs = {
                    'accessory':accessory_obj,
                    'gpu_core_num':self.parameters('gpu_core_num'),
                    'gpu_memory':self.parameters('gpu_memory'),
                    'gpu_frequency':self.parameters('gpu_frequency'),
                    'gpu_chip':self.parameters('gpu_chip'),
                    'gpu_memory_specs':self.parameters('gpu_memory_specs'),
                    'gpu_power':self.parameters('gpu_power'),
                    'gpu_idle_power':self.parameters('gpu_idle_power'),
                    'gpu_memory_bandwidth':self.parameters('gpu_memory_bandwidth')
            }
            obj = TGpu(**kwargs)
            obj.save()
        except:
            raise APIError(-3000)
        return {'id':accessory_obj.accessory_id}

    @CheckParameters(['id','gpu_core_num','gpu_memory','gpu_frequency','gpu_chip','gpu_memory_specs','gpu_power','gpu_idle_power','gpu_memory_bandwidth'])
    def post_updategpubyid(self):
        try:
            accessory_obj = TAccessory.objects.filter(accessory_id=self.parameters('id')).exclude(delete_status=db_code_mapping['delete'])[0]
            obj = TGpu.objects.filter(accessory=accessory_obj)
            kwargs = {
                'gpu_core_num':self.parameters('gpu_core_num'),
                'gpu_memory':self.parameters('gpu_memory'),
                'gpu_frequency':self.parameters('gpu_frequency'),
                'gpu_chip':self.parameters('gpu_chip'),
                'gpu_memory_specs':self.parameters('gpu_memory_specs'),
                'gpu_power':self.parameters('gpu_power'),
                'gpu_idle_power':self.parameters('gpu_idle_power'),
                'gpu_memory_bandwidth':self.parameters('gpu_memory_bandwidth')
            }
            obj.update(**kwargs)
        except:
            raise APIError(-3000)
        return {'id':accessory_obj.accessory_id}

class Guide(CoreView):

    def get_getguidebyid(self):
        try:
            obj = TGuide.objects.filter(guide_id=self.url_parameters('id')).exclude(delete_status=db_code_mapping['delete'])
        except:
            raise APIError(-3000)
        data = serializers.serialize("json", obj)
        return data

    @CheckParameters(['id'])
    def post_delguidebyid(self):
        try:
            obj = TGuide.objects.filter(guide_id=self.parameters('id')).exclude(delete_status=db_code_mapping['delete'])[0]
            obj.delete_status = db_code_mapping['delete']
            obj.save()
        except:
            raise APIError(-3000)
        return {'id':obj.accessory_id}

    @CheckParameters(['comment','used','total_count','guide_model'])
    def post_addguide(self):
        try:
            kwargs = {
                    'guide_id':self.create_id(),
                    'comment':self.parameters('comment'),
                    'used':self.parameters('used'),
                    'total_count':self.parameters('total_count'),
                    'guide_model':self.parameters('guide_model')
            }
            obj = TGuide(**kwargs)
            obj.save()
        except:
            raise APIError(-3000)

        return {'id':obj.guide_id}

    @CheckParameters(['comment','used','total_count','guide_model','id'])
    def post_updateguidebyid(self):
        try:
            obj = TGuide.objects.filter(guide_id=self.parameters('id')).exclude(delete_status=db_code_mapping['delete'])
            kwargs = {
                    'comment':self.parameters('comment'),
                    'used':self.parameters('used'),
                    'total_count':self.parameters('total_count'),
                    'guide_model':self.parameters('guide_model')
            }
            obj.update(**kwargs)
        except:
            raise APIError(-3000)
        return {'id':obj.guide_id}

class HbaCard(CoreView):

    def get_gethbacardbyid(self):
        try:
            accessory_obj = TAccessory.objects.filter(accessory_id=self.url_parameters('id')).exclude(delete_status=db_code_mapping['delete'])[0]
            obj = THbaCard.objects.filter(accessory=accessory_obj)
        except:
            raise APIError(-3000)
        data = serializers.serialize("json", obj)
        return data

    @CheckParameters(['id'])
    def post_delhbacardbyid(self):
        try:
            accessory_obj = TAccessory.objects.filter(accessory_id=self.parameters('id')).exclude(delete_status=db_code_mapping['delete'])[0]
            obj.delete_status = db_code_mapping['delete']
            obj.save()
        except:
            raise APIError(-3000)
        return {'id':obj.accessory_id}

    @CheckParameters(['id','hba_card_interface','comment','version','hba_card_model'])
    def post_addhbacard(self):
        try:
            accessory_obj = TAccessory.objects.filter(accessory_id=self.parameters('id')).exclude(delete_status=db_code_mapping['delete'])[0]
            kwargs = {
                    'accessory':accessory_obj,
                    'hba_card_interface':self.parameters('hba_card_interface'),
                    'comment':self.parameters('comment'),
                    'version':self.parameters('version'),
                    'hba_card_model':self.parameters('hba_card_model')
            }
            obj = THbaCard(**kwargs)
            obj.save()
        except:
            raise APIError(-3000)
        return {'id':accessory_obj.accessory_id}

    @CheckParameters(['id','hba_card_interface','comment','version','hba_card_model'])
    def post_updatehbacardbyid(self):
        try:
            accessory_obj = TAccessory.objects.filter(accessory_id=self.parameters('id')).exclude(delete_status=db_code_mapping['delete'])[0]
            obj = THbaCard.objects.filter(accessory=accessory_obj)
            kwargs = {
                    'hba_card_interface':self.parameters('hba_card_interface'),
                    'comment':self.parameters('comment'),
                    'version':self.parameters('version'),
                    'hba_card_model':self.parameters('hba_card_model')
            }
            obj.update(**kwargs)
        except:
            raise APIError(-3000)
        return {'id':accessory_obj.accessory_id}

class Memory(CoreView):

    def get_getmemorybyid(self):
        try:
            accessory_obj = TAccessory.objects.filter(accessory_id=self.url_parameters('id')).exclude(delete_status=db_code_mapping['delete'])[0]
            obj = TMemory.objects.filter(accessory=accessory_obj)
        except:
            raise APIError(-3000)
        data = serializers.serialize("json", obj)
        return data

    @CheckParameters(['id'])
    def post_delmemorybyid(self):
        try:
            accessory_obj = TAccessory.objects.filter(accessory_id=self.parameters('id')).exclude(delete_status=db_code_mapping['delete'])[0]
            obj.delete_status = db_code_mapping['delete']
            obj.save()
        except:
            raise APIError(-3000)
        return {'id':obj.accessory_id}

    @CheckParameters(['id','memory_capacity','memroy_frequency','memory_model','memory_specs','comment','memory_ecc_support','memory_channel_num','memory_max_underclocking'])
    def post_addmemory(self):
        try:
            accessory_obj = TAccessory.objects.filter(accessory_id=self.parameters('id')).exclude(delete_status=db_code_mapping['delete'])[0]
            kwargs = {
                    'accessory':accessory_obj,
                    'memory_capacity':self.parameters('memory_capacity'),
                    'memroy_frequency':self.parameters('memroy_frequency'),
                    'memory_model':self.parameters('memory_model'),
                    'memory_specs':self.parameters('memory_specs'),
                    'comment':self.parameters('comment'),
                    'memory_ecc_support':self.parameters('memory_ecc_support'),
                    'memory_channel_num':self.parameters('memory_channel_num'),
                    'memory_max_underclocking':self.parameters('memory_max_underclocking')
            }
            obj = TMemory(**kwargs)
            obj.save()
        except:
            raise APIError(-3000)
        return {'id':accessory_obj.accessory_id}

    @CheckParameters(['id','memory_capacity','memroy_frequency','memory_model','memory_specs','comment','memory_ecc_support','memory_channel_num','memory_max_underclocking'])
    def post_updatememorybyid(self):
        try:
            accessory_obj = TAccessory.objects.filter(accessory_id=self.parameters('id')).exclude(delete_status=db_code_mapping['delete'])
            kwargs = {
                    'memory_capacity':self.parameters('memory_capacity'),
                    'memroy_frequency':self.parameters('memroy_frequency'),
                    'memory_model':self.parameters('memory_model'),
                    'memory_specs':self.parameters('memory_specs'),
                    'comment':self.parameters('comment'),
                    'memory_ecc_support':self.parameters('memory_ecc_support'),
                    'memory_channel_num':self.parameters('memory_channel_num'),
                    'memory_max_underclocking':self.parameters('memory_max_underclocking')
            }
            obj = TMemory.objects.filter(accessory=accessory_obj)
            obj.update(**kwargs)
        except:
            raise APIError(-3000)
        return {'id':accessory_obj.accessory_id}


class MotherBoard(CoreView):

    def get_getmotherboardbyid(self):
        try:
            accessory_obj = TAccessory.objects.filter(accessory_id=self.url_parameters('id')).exclude(delete_status=db_code_mapping['delete'])[0]
            obj = TMotherBoard.objects.filter(accessory=accessory_obj)
        except:
            raise APIError(-3000)
        data = serializers.serialize("json", obj)
        return data

    @CheckParameters(['id'])
    def post_delmotherboardbyid(self):
        try:
            accessory_obj = TAccessor.objects.filter(accessory_id=self.parameters('id')).exclude(delete_status=db_code_mapping['delete'])[0]
            obj.delete_status = db_code_mapping['delete']
            obj.save()
        except:
            raise APIError(-3000)
        return {'id':obj.accessory_id}

    @CheckParameters(['id','mother_board_model','comment','version','pci_count','pcie_count','sata_count','sas_count','m_2_count','satadom_count','lom_count','dimm_count','mother_board_chip','sd_support','sata_controller_support','sas_controller_support','usb_count','double_bios_protection_support','asset_entry_support','command_bios_support'])
    def post_addmotherboard(self):
        try:
            accessory_obj = TAccessory.objects.filter(accessory_id=self.parameters('id')).exclude(delete_status=db_code_mapping['delete'])[0]
            kwargs = {
                    'accessory':accessory_obj,
                    'mother_board_model':self.parameters('mother_board_model'),
                    'comment':self.parameters('comment'),
                    'version':self.parameters('version'),
                    'pci_count':self.parameters('pci_count'),
                    'pcie_count':self.parameters('pcie_count'),
                    'sata_count':self.parameters('sata_count'),
                    'sas_count':self.parameters('sas_count'),
                    'm_2_count':self.parameters('m_2_count'),
                    'satadom_count':self.parameters('satadom_count'),
                    'lom_count':self.parameters('lom_count'),
                    'dimm_count':self.parameters('dimm_count'),
                    'mother_board_chip':self.parameters('mother_board_chip'),
                    'sd_support':self.parameters('sd_support'),
                    'sata_controller_support':self.parameters('sata_controller_support'),
                    'sas_controller_support':self.parameters('sas_controller_support'),
                    'usb_count':self.parameters('usb_count'),
                    'double_bios_protection_support':self.parameters('double_bios_protection_support'),
                    'asset_entry_support':self.parameters('asset_entry_support'),
                    'command_bios_support':self.parameters('command_bios_support')
            }
            obj = TMotherBoard(**kwargs)
            obj.save()
        except:
            raise APIError(-3000)
        return {'id':accessory_obj.accessory_id}


    @CheckParameters(['id','mother_board_model','comment','version','pci_count','pcie_count','sata_count','sas_count','m_2_count','satadom_count','lom_count','dimm_count','mother_board_chip','sd_support','sata_controller_support','sas_controller_support','usb_count','double_bios_protection_support','asset_entry_support','command_bios_support'])
    def post_updatemotherboardbyid(self):
        try:
            accessory_obj = TAccessory.objects.filter(accessory_id=self.parameters('id')).exclude(delete_status=db_code_mapping['delete'])
            kwargs = {
                    'mother_board_model':self.parameters('mother_board_model'),
                    'comment':self.parameters('comment'),
                    'version':self.parameters('version'),
                    'pci_count':self.parameters('pci_count'),
                    'pcie_count':self.parameters('pcie_count'),
                    'sata_count':self.parameters('sata_count'),
                    'sas_count':self.parameters('sas_count'),
                    'm_2_count':self.parameters('m_2_count'),
                    'satadom_count':self.parameters('satadom_count'),
                    'lom_count':self.parameters('lom_count'),
                    'dimm_count':self.parameters('dimm_count'),
                    'mother_board_chip':self.parameters('mother_board_chip'),
                    'sd_support':self.parameters('sd_support'),
                    'sata_controller_support':self.parameters('sata_controller_support'),
                    'sas_controller_support':self.parameters('sas_controller_support'),
                    'usb_count':self.parameters('usb_count'),
                    'double_bios_protection_support':self.parameters('double_bios_protection_support'),
                    'asset_entry_support':self.parameters('asset_entry_support'),
                    'command_bios_support':self.parameters('command_bios_support')
            }
            obj = TMotherBoard.objects.filter(accessory=accessory_obj)
            obj.update(**kwargs)
        except:
            raise APIError(-3000)
        return {'id':accessory_obj.accessory_id}


class NetworkCard(CoreView):

    def get_getnetworkcardbyid(self):
        try:
            accessory_obj = TAccessory.objects.filter(accessory_id=self.url_parameters('id')).exclude(delete_status=db_code_mapping['delete'])[0]
            obj = TNetworkCard.objects.filter(accessory=accessory_obj)
        except:
            raise APIError(-3000)
        data = serializers.serialize("json", obj)
        return data

    @CheckParameters(['id'])
    def post_delnetworkcardbyid(self):
        try:
            accessory_obj = TAccessor.objects.filter(accessory_id=self.parameters('id')).exclude(delete_status=db_code_mapping['delete'])[0]
            obj.delete_status = db_code_mapping['delete']
            obj.save()
        except:
            raise APIError(-3000)
        return {'id':obj.accessory_id}

    @CheckParameters(['id','speed','network_card_interface','network_card_model','comment','version','mac_address','network_card_iscsi_support','network_card_ncsi_support','network_card_pxe_support'])
    def post_addnetworkcard(self):
        try:
            accessory_obj = TAccessory.objects.filter(accessory_id=self.parameters('id')).exclude(delete_status=db_code_mapping['delete'])[0]
            kwargs = {
                    'accessory':accessory_obj,
                    'speed':self.parameters('speed'),
                    'network_card_interface':self.parameters('network_card_interface'),
                    'network_card_model':self.parameters('network_card_model'),
                    'comment':self.parameters('comment'),
                    'version':self.parameters('version'),
                    'mac_address':self.parameters('mac_address'),
                    'network_card_iscsi_support':self.parameters('network_card_iscsi_support'),
                    'network_card_ncsi_support':self.parameters('network_card_ncsi_support'),
                    'network_card_pxe_support':self.parameters('network_card_pxe_support')
            }
            obj = TNetworkCard(**kwargs)
            obj.save()
        except:
            raise APIError(-3000)
        return {'id':accessory_obj.accessory_id}

    @CheckParameters(['id','speed','network_card_interface','network_card_model','comment','version','mac_address','network_card_iscsi_support','network_card_ncsi_support','network_card_pxe_support'])
    def post_updatenetworkcardbyid(self):
        try:
            accessory_obj = TAccessory.objects.filter(accessory_id=self.parameters('id')).exclude(delete_status=db_code_mapping['delete'])
            kwargs = {
                    'speed':self.parameters('speed'),
                    'network_card_interface':self.parameters('network_card_interface'),
                    'network_card_model':self.parameters('network_card_model'),
                    'comment':self.parameters('comment'),
                    'version':self.parameters('version'),
                    'mac_address':self.parameters('mac_address'),
                    'network_card_iscsi_support':self.parameters('network_card_iscsi_support'),
                    'network_card_ncsi_support':self.parameters('network_card_ncsi_support'),
                    'network_card_pxe_support':self.parameters('network_card_pxe_support')
            }
            obj = TNetworkCard.objects.filter(accessory=accessory_obj)
            obj.update(**kwargs)
        except:
            return {'id':accessory_obj.accessory_id}



class Power(CoreView):

    def get_getpowerbyid(self):
        try:
            accessory_obj = TAccessory.objects.filter(accessory_id=self.url_parameters('id')).exclude(delete_status=db_code_mapping['delete'])[0]
            obj = TPower.objects.filter(accessory=accessory_obj)
        except:
            raise APIError(-3000)
        data = serializers.serialize("json", obj)
        return data

    @CheckParameters(['id'])
    def post_delpowerbyid(self):
        try:
            accessory_obj = TAccessor.objects.filter(accessory_id=self.parameters('id')).exclude(delete_status=db_code_mapping['delete'])[0]
            obj.delete_status = db_code_mapping['delete']
            obj.save()
        except:
            raise APIError(-3000)
        return {'id':obj.accessory_id}

    @CheckParameters(['id','power_model','power_specs','power_supply','version'])
    def post_addpower(self):
        try:
            accessory_obj = TAccessory.objects.filter(accessory_id=self.parameters('id')).exclude(delete_status=db_code_mapping['delete'])[0]
            kwargs = {
                    'accessory':accessory_obj,
                    'power_model':self.parameters('power_model'),
                    'power_specs':self.parameters('power_specs'),
                    'efficiency':self.parameters('efficiency'),
                    'power_supply':self.parameters('power_supply'),
                    'version':self.parameters('version')
            }
            obj = TPower(**kwargs)
            obj.save()
        except:
            raise APIError(-3000)
        return {'id':accessory_obj.accessory_id}

    @CheckParameters(['id','power_model','power_specs','power_supply','version'])
    def post_updatepowerbyid(self):
        try:
            accessory_obj = TAccessory.objects.filter(accessory_id=self.parameters('id')).exclude(delete_status=db_code_mapping['delete'])
            kwargs = {
                    'power_model':self.parameters('power_model'),
                    'power_specs':self.parameters('power_specs'),
                    'efficiency':self.parameters('efficiency'),
                    'power_supply':self.parameters('power_supply'),
                    'version':self.parameters('version')
            }
            obj = TPower.objects.filter(accessory=accessory_obj)
            obj.update(**kwargs)
        except:
            return {'id':accessory_obj.accessory_id}
