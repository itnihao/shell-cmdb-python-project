from __future__ import unicode_literals

from django.db import models
from apps.server_device.models import TAsset

class TNetDevice(models.Model):
    net_device_id = models.BigIntegerField(primary_key=True)
    net_device_name = models.CharField(max_length=45, blank=True)
    asset = models.ForeignKey(TAsset, blank=True, null=True)
    device_level = models.IntegerField(blank=True, null=True)
    t_net_devicecol = models.CharField(max_length=45, blank=True)
    delete_status = models.IntegerField(blank=True, null=True)

    class Meta:
        models.Model_table = 't_net_device'


class TIdcModule(models.Model):
    module_id = models.BigIntegerField(primary_key=True)
    module_name = models.CharField(max_length=45, blank=True)
    delete_status = models.IntegerField(blank=True, null=True)

    class Meta:
        models.Model_table = 't_idc_module'

class TNicPort(models.Model):
    nic_port_id = models.BigIntegerField(primary_key=True)
    nic_port_name = models.CharField(max_length=45)
    nic_port_speed = models.IntegerField()
    nic_port_transfer_medium = models.IntegerField()
    nic_port_bandwidth = models.IntegerField()
    nic_port_mode = models.IntegerField()
    nic_port_link_type = models.IntegerField()
    asset = models.ForeignKey(TAsset)
    nic_port_num = models.IntegerField()
    nic_port_level = models.IntegerField()
    nic_port_planned_position = models.ForeignKey('idc.TPosition', blank=True, null=True)
    delete_status = models.IntegerField(blank=True, null=True)

    class Meta:
        models.Model_table = 't_nic_port'

class TNicPortLink(models.Model):
    nic_port_link_id = models.BigIntegerField(primary_key=True)
    nic_port_id_upper = models.ForeignKey(TNicPort, related_name='nic_port_id_upper')
    nic_port_id_lower = models.ForeignKey(TNicPort, related_name='nic_port_id_lower')
    cable_type = models.IntegerField()
    delete_status = models.IntegerField(blank=True, null=True)

    class Meta:
        models.Model_table = 't_nic_port_link'

