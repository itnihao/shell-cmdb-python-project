# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models

class TRealIp(models.Model):
    IP_TYPE_MAPPING = {
        u'内网':0,
        u'外网':1,
        u'管理网':2,
    }
    ip_id = models.BigIntegerField(primary_key=True)
    delete_status = models.IntegerField(blank=True, null=True)
    ip = models.CharField(max_length=255, blank=True)
    gateway = models.CharField(max_length=255, blank=True)
    mask = models.CharField(max_length=255, blank=True)
    ip_type = models.IntegerField(choices=(
        (0, u'内网'),
        (1, u'外网'),
        (2, u'管理网'),
        ), db_index=True, default=0)
    #sn = models.ForeignKey('server_device.TAsset', blank=True, null=True)
    mac = models.CharField(max_length=255, blank=True)


class TAssetIp(models.Model):
    assetip_id = models.BigIntegerField(primary_key=True)
    delete_status = models.IntegerField(blank=True, null=True)
    ip = models.ForeignKey('TRealIp', blank=True, null=True)
    asset = models.ForeignKey('server_device.TAsset', blank=True, null=True)


"""
class TIpAddress(models.Model):
    ip_address_id = models.BigIntegerField(primary_key=True)
    ip_address = models.CharField(max_length=255, blank=True)
    assign_time = models.DateTimeField(blank=True, null=True)
    update_time = models.DateTimeField(blank=True, null=True)
    ip_status = models.IntegerField(blank=True, null=True)
    asset_id = models.IntegerField(blank=True, null=True)
    ip_type = models.IntegerField(blank=True, null=True)
    ip_segment = models.ForeignKey('TIpSegment', blank=True, null=True)
    ip_assigner = models.ForeignKey('dpt.TOrgUser', blank=True, null=True)
    ip_segment_name = models.CharField(max_length=255, blank=True)
    delete_status = models.IntegerField(blank=True, null=True)

    class Meta:
        models.Model_table = 't_ip_address'


class TIpSegment(models.Model):
    ip_segment_id = models.BigIntegerField()
    ip_segment_address = models.CharField(max_length=255, blank=True)
    ip_segment_netmask = models.CharField(max_length=255, blank=True)
    ip_segment_isp = models.CharField(max_length=255, blank=True)
    ip_segment_gateway = models.CharField(max_length=255, blank=True)
    ip_segment_broadcast = models.CharField(max_length=255, blank=True)
    delete_status = models.IntegerField(blank=True, null=True)

    class Meta:
        models.Model_table = 't_ip_segment'
"""
