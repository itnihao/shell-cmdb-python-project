# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

class TIdc(models.Model):
    IDC_RESOURCE_TYPE_MAPPING = {
            u'租用':1,
            u'自建':0,
    }
    idc_id = models.BigIntegerField(primary_key=True)
    idc_region = models.CharField(max_length=45, blank=True)
    idc_zone = models.CharField(max_length=45, blank=True)
    idc_campus = models.CharField(max_length=45, blank=True)
    idc_address = models.TextField(blank=True)
    idc_phone = models.CharField(max_length=45, blank=True)
    idc_fax = models.CharField(max_length=45, blank=True)
    idc_email = models.CharField(max_length=45, blank=True)
    idc_owner_master_id = models.CharField(max_length=255, blank=True)
    idc_owner_backup_id = models.CharField(max_length=255, blank=True)
    idc_owner_master_id = models.ForeignKey('dpt.TBspUser', related_name='idc_owner_master_id')
    idc_owner_backup_id = models.ForeignKey('dpt.TBspUser', related_name='idc_owner_backup_id')
    idc_contacts = models.CharField(max_length=255, blank=True)
    idc_name = models.CharField(max_length=255, blank=True)
    idc_enable_time = models.DateTimeField(blank=True, null=True)
    idc_due_time = models.DateTimeField(blank=True, null=True)
    idc_resource_type = models.IntegerField(choices=(
        (0, u'自建'),
        (1, u'租用'),
        ), db_index=True, default=1)
    idc_supplier = models.TextField(blank=True)
    delete_status = models.IntegerField(blank=True, null=True)

    class Meta:
        models.Model_table = 't_idc'

class TRack(models.Model):
    RACK_ENERGY_TYPE_MAPPING = {
            u'交直流':0,
            u'交流':1,
    }
    FLAG_MAPPING = {
            u'否':0,
            u'是':1,
            }
    rack_id = models.BigIntegerField(primary_key=True)
    idc_id = models.ForeignKey(TIdc, blank=True, null=True)
    rack_name = models.CharField(max_length=45, blank=True)
    rack_code = models.CharField(max_length=45, blank=True)
    rack_depth = models.IntegerField(blank=True, null=True)
    rack_height = models.IntegerField(blank=True, null=True)
    rack_width = models.IntegerField(blank=True, null=True)
    rack_spec_height = models.CharField(max_length=45, blank=True)
    rack_energy_type = models.IntegerField(choices=(
        (0, u'交直流'),
        (1, u'交流'),
        ), db_index=True, default=0)
    rack_power_max = models.IntegerField(blank=True, null=True)
    rack_power_rating = models.IntegerField(blank=True, null=True)
    rack_virtualization = models.IntegerField(choices=(
        (0, u'否'),
        (1, u'是'),
        ), db_index=True, default=0)
    rack_extranet = models.IntegerField(choices=(
        (0, u'否'),
        (1, u'是'),
        ), db_index=True, default=0)
    delete_status = models.IntegerField(blank=True, null=True)

    class Meta:
        models.Model_table = 't_rack'

class TPosition(models.Model):
    POSITION_STATUS_MAPPING = {
            u'已用':0,
            u'空闲':1,
            u'规划占用':2,
    }
    position_id = models.BigIntegerField(primary_key=True)
    position_num = models.IntegerField(blank=True, null=True)
    rack_id = models.ForeignKey('TRack', blank=True, null=True)
    position_spec_height = models.CharField(max_length=45, blank=True)
    position_status = models.IntegerField(choices=(
        (0, u'已用'),
        (1, u'空闲'),
        (2, u'规划占用'),
        ), db_index=True, default=1)
    start_spec_height = models.IntegerField(blank=True, null=True)
    position_comment =  models.TextField(blank=True)
    delete_status = models.IntegerField(blank=True, null=True)

    class Meta:
        models.Model_table = 't_position'


#class TLogicSection(models.Model):
#    logic_section_id = models.BigIntegerField(primary_key=True)
#    logic_section_name = models.CharField(max_length=45, blank=True)
#    idc = models.ForeignKey(TIdc, blank=True, null=True)
#    logic_section_type = models.ForeignKey('TLogicSectionType', blank=True, null=True)
#    delete_status = models.IntegerField(blank=True, null=True)
#
#    class Meta:
#        models.Model_table = 't_logic_section'
#
#
#class TLogicSectionType(models.Model):
#    logic_section_type_id = models.BigIntegerField(primary_key=True)
#    logic_section_type_name = models.CharField(max_length=45, blank=True)
#    logic_section_type_desc = models.CharField(max_length=45, blank=True)
#    delete_status = models.IntegerField(blank=True, null=True)
#
#    class Meta:
#        models.Model_table = 't_logic_section_type'
#
