# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from django.db import models
from apps.dpt import models as dpt_models

class TAsset(models.Model):
    ASSET_STATUS_MAPPING = {
        u'购买':0,
        u'租用':1,
        u'厂商备机':2,
    }
    DEVICE_TYPE_MAPPING = {
        u'服务器':0,
        u'配件':1,
        u'网络设备':2,
    }
    asset_id = models.BigIntegerField(primary_key=True)
    asset_sn = models.CharField(max_length=45, blank=True)
    asset_num = models.CharField(max_length=45, blank=True)
    asset_warranty_due_time = models.DateTimeField(blank=True, null=True)
    asset_receipt_time = models.DateTimeField(blank=True, null=True)
    asset_on_shelf_time = models.DateTimeField(blank=True, null=True)
    asset_off_shelf_time = models.DateTimeField(blank=True, null=True)
    asset_last_update_time = models.DateTimeField(db_index=True, auto_now_add=True)
    asset_status = models.IntegerField(choices=(
        (0, u'购买'),
        (1, u'租用'),
        (2, u'厂商备机'),
        ), db_index=True, default=0)
    asset_comment = models.TextField(blank=True)
    position_id = models.ForeignKey('idc.TPosition', blank=True, null=True)
    device_type = models.IntegerField(choices=(
        (0, u'服务器'),
        (1, u'配件'),
        (2, u'网络设备')
        ), db_index=True, default=0)
#    order_item_id = models.BigIntegerField(blank=True, null=True)
#    asset_operator_org_id = models.ForeignKey('dpt.TOrg', related_name='asset_operator_org_id')
    asset_operator_org_id = models.CharField(max_length=225, blank=True)
    delete_status = models.IntegerField(blank=True, null=True)

    class Meta:
        models.Model_table = 't_asset'


class TDeviceProducerType(models.Model):
    DEVICE_TYPE_MAPPING = {
        u'服务器':0,
        u'配件':1,
        u'网络设备':2,
        u'存储设备':3,
    }
    device_producer_type_id = models.BigIntegerField(primary_key=True)
    producer_name = models.CharField(max_length=45, blank=True)
    device_type = models.IntegerField(choices=(
        (0, u'服务器'),
        (1, u'配件'),
        (2, u'网络设备'),
        (3, u'存储设备'),
        ), db_index=True, default=0)
    delete_status = models.IntegerField(blank=True, null=True)

    class Meta:
        models.Model_table = 't_device_producer_type'

class TOsType(models.Model):
    os_type_id = models.BigIntegerField(primary_key=True)
    os_type_name = models.CharField(max_length=45, blank=True)
    os_type_version = models.CharField(max_length=45, blank=True)
    os_kernerl_version = models.CharField(max_length=45, blank=True)
    delete_status = models.IntegerField(blank=True, null=True)

    class Meta:
        models.Model_table = 't_os_type'

class TServer(models.Model):
    SERVER_HEALTH_STATUS_MAPPING = {
         u'正常':0,
         u'报修':1,
    }
    SERVER_RUN_STATUS_MAPPING = {
        u'运行':0,
        u'关机':1,
    }
    SERVER_OPERATION_STATUS_MAPPING = {
        u'交付':0,
        u'未交付':1,
    }
    SERVER_TYPE_MAPPING = {
        u'物理机':0,
        u'宿主机':1,
        u'虚拟机':2,
    }
    server_id = models.BigIntegerField(primary_key=True)
    asset_id = models.ForeignKey(TAsset, blank=True, null=True)
    server_comment = models.TextField(blank=True)
    server_health_status = models.IntegerField(choices=(
        (0, u'正常'),
        (1, u'报修'),
        ), db_index=True, default=0)
    server_run_status = models.IntegerField(choices=(
        (0, u'运行'),
        (1, u'关机'),
        ), db_index=True, default=0)
    server_device_type_id = models.ForeignKey('TServerDeviceType', blank=True, null=True)
    inc_server_type_id = models.ForeignKey('TIncServerType', blank=True, null=True)
    server_operation_status = models.IntegerField(choices=(
        (0, u'交付'),
        (1, u'未交付'),
        ), db_index=True, default=0)
    server_host_name = models.CharField(max_length=45, blank=True)
    os_type_id = models.ForeignKey(TOsType, blank=True, null=True)
    server_type = models.IntegerField(choices=(
            (0, u'物理机'),
            (1, u'宿主机'),
            (2, u'虚拟机'),
            ), db_index=True, default=0)
#    server_ads_status = models.IntegerField(blank=True, null=True)
#    server_ads_check_time = models.DateField(blank=True, null=True)
#    server_ads_installed = models.IntegerField(blank=True, null=True)
#    server_ads_update_time = models.DateField(blank=True, null=True)
    delete_status = models.IntegerField(blank=True, null=True)

    class Meta:
        models.Model_table = 't_server'


class TServerDeviceType(models.Model):
    server_type_id = models.BigIntegerField(primary_key=True)
    device_producer_id = models.ForeignKey(TDeviceProducerType, blank=True, null=True)
    server_device_type_name = models.CharField(max_length=45, blank=True)
#    server_hight = models.IntegerField(blank=True, null=True)
    server_hight = models.CharField(max_length=45, blank=True)
    delete_status = models.IntegerField(blank=True, null=True)

    class Meta:
        models.Model_table = 't_server_device_type'


class TServerRepair(models.Model):
    server_repair_id = models.BigIntegerField(primary_key=True)
    asset_id = models.ForeignKey(TAsset, blank=True, null=True)
    repair_start_time = models.DateTimeField(blank=True, null=True)
    repair_end_time = models.DateTimeField(blank=True, null=True)
    repair_context = models.TextField(blank=True, null=True)
    repair_user = models.ForeignKey(dpt_models.TBspUser, blank=True, null=True)
    repair_status = models.IntegerField(blank=True, null=True, default=1)


class TIncServerType(models.Model):
    inc_server_type_id = models.BigIntegerField(primary_key=True)
    inc_server_type_name = models.CharField(max_length=45, blank=True)
    inc_server_code = models.CharField(max_length=255, blank=True)
    delete_status = models.IntegerField(blank=True, null=True)

    class Meta:
        models.Model_table = 't_inc_server_type'

class TServerSelection(models.Model):
    server_selection_id = models.BigIntegerField(primary_key=True)
    inc_server_type = models.ForeignKey(TIncServerType, blank=True, null=True)
    server_device_type = models.ForeignKey(TServerDeviceType, blank=True, null=True)
 #   device_producer_type = models.ForeignKey(TDeviceProducerType, blank=True, null=True)
    server_selection_datetime = models.DateTimeField(blank=True, null=True,auto_now_add=True)
    delete_status = models.IntegerField(blank=True, null=True)

    class Meta:
        models.Model_table = 't_server_selection'


class AssetLog(models.Model):
    logid = models.BigIntegerField(primary_key=True)
    asset_id = models.ForeignKey(TAsset, blank=True, null=True)
    update_time = models.DateTimeField(auto_now=True, auto_now_add=True, blank=True, null=True)
    context = models.TextField(blank=True, null=True)

#class TSelectionVersion(models.Model):
#    server_selection_version_id = models.BigIntegerField(primary_key=True)
#    server_selection_version_start_time = models.DateTimeField(blank=True, null=True)
#    server_selection_version_end_time = models.DateTimeField(blank=True, null=True)
#    server_selection_version_author_id = models.BigIntegerField(blank=True, null=True)
#    server_selection_versionnumber = models.CharField(max_length=45, blank=True)
#    delete_status = models.IntegerField(blank=True, null=True)
#
#    class Meta:
#        models.Model_table = 't_selection_version'


#class TSelectionVersionRecord(models.Model):
#    server_selection_version_record_id = models.BigIntegerField(primary_key=True)
#    server_selection_version = models.ForeignKey(TSelectionVersion, blank=True, null=True)
#    server_selection = models.ForeignKey('TServerSelection', blank=True, null=True)
#    delete_status = models.IntegerField(blank=True, null=True)
#
#    class Meta:
#        models.Model_table = 't_selection_version_record'
#

#class TNetworkInterface(models.Model):
#    network_interface_id = models.BigIntegerField(primary_key=True)
#    server = models.ForeignKey('TServer', blank=True, null=True)
#    network_interface_name = models.CharField(max_length=45, blank=True)
#    network_interface_type = models.IntegerField(blank=True, null=True)
#    delete_status = models.IntegerField(blank=True, null=True)
#
#    class Meta:
#        models.Model_table = 't_network_interface'
#
#
#class TNetworkInterfaceConfig(models.Model):
#    network_interface_config_id = models.BigIntegerField(primary_key=True)
#    network_interface = models.ForeignKey(TNetworkInterface, blank=True, null=True)
#    nic_port = models.ForeignKey('net_device.TNicPort', blank=True, null=True)
#    network_interface_link_type = models.IntegerField(blank=True, null=True)
#    delete_status = models.IntegerField(blank=True, null=True)
#
#    class Meta:
#        models.Model_table = 't_network_interface_config'
#
#
#class TNetworkInterfaceIp(models.Model):
#    network_interface_ip_id = models.BigIntegerField(primary_key=True)
#    network_interface = models.ForeignKey(TNetworkInterface, blank=True, null=True)
#    ip_address = models.CharField(max_length=45, blank=True)
#    delete_status = models.IntegerField(blank=True, null=True)
#
#    class Meta:
#        models.Model_table = 't_network_interface_ip'
#


#class TSlot(models.Model):
#    slot_id = models.BigIntegerField(primary_key=True)
#    access = models.ForeignKey(TAsset, blank=True, null=True)
#    slot_type = models.ForeignKey('TSlotType', blank=True, null=True)
#    slot_face_direction = models.IntegerField(blank=True, null=True)
#    insert_accessory_id = models.BigIntegerField(blank=True, null=True)
#    slot_num = models.CharField(max_length=45, blank=True)
#    delete_status = models.IntegerField(blank=True, null=True)
#
#    class Meta:
#        models.Model_table = 't_slot'
#
#
#class TSlotType(models.Model):
#    slot_type_id = models.BigIntegerField(primary_key=True)
#    slot_type_name = models.CharField(max_length=45, blank=True)
#    slot_spec = models.IntegerField(blank=True, null=True)
#    delete_status = models.IntegerField(blank=True, null=True)
#
#    class Meta:
#        models.Model_table = 't_slot_type'
