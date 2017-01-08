from __future__ import unicode_literals

from django.db import models
import time

class TRealaccessory(models.Model):
    accessory_id = models.BigIntegerField(primary_key=True)
    delete_status = models.IntegerField(blank=True, null=True)
    asset_num = models.ForeignKey('server_device.TAsset', blank=True, null=True)
    cpu_capacity = models.CharField(max_length=45, blank=True)
    memory_capacity = models.CharField(max_length=45, blank=True)
    disk_capacity = models.CharField(max_length=45, blank=True)
    net_card_capacity = models.CharField(max_length=45, blank=True)
    cpu_info = models.TextField(blank=True, null=True)
    memory_info = models.TextField(blank=True, null=True)
    disk_info = models.TextField(blank=True, null=True)
    net_card_info = models.TextField(blank=True, null=True)

"""
class TAccessory(models.Model):
    accessory_id = models.BigIntegerField(primary_key=True)
    accessory_status = models.IntegerField(blank=True, null=True)
    delete_status = models.IntegerField(blank=True, null=True)
#    idc_id = models.BigIntegerField(blank=True, null=True)
    idc_id = models.ForeignKey('idc.TIdc', blank=True, null=True)
    sn = models.IntegerField(blank=True, null=True)
    enable_time = models.DateTimeField(blank=True, null=True)
    due_time = models.DateTimeField(blank=True, null=True)
    accessory_type = models.ForeignKey('TAccessoryType')
    store = models.ForeignKey('TAccessoryStore', blank=True, null=True)
    asset_id = models.ForeignKey('server_device.TAsset', blank=True, null=True)
#    brand = models.ForeignKey('TAccessoryBrand', blank=True, null=True)
    brand = models.CharField(max_length=45, blank=True)

    class Meta:
        models.Model_table = 't_accessory'


class TAccessoryBrand(models.Model):
    brand_id = models.BigIntegerField(primary_key=True)
    brand_name = models.CharField(max_length=45, blank=True)
    delete_status = models.IntegerField(blank=True, null=True)

    class Meta:
        models.Model_table = 't_accessory_brand'

class TAccessoryStore(models.Model):
    accessory_store_id = models.BigIntegerField(primary_key=True)
    accessory_store_name = models.CharField(max_length=45, blank=True)
    accessory_store_position = models.CharField(max_length=45, blank=True)
    accessory_store_owner = models.CharField(max_length=45, blank=True)
    accessory_idc = models.ForeignKey('idc.TIdc', blank=True, null=True)
    delete_status = models.IntegerField(blank=True, null=True)

    class Meta:
        models.Model_table = 't_accessory_store'


class TAccessoryType(models.Model):
    accessory_type_id = models.BigIntegerField(primary_key=True)
    accessory_type_name = models.CharField(max_length=45, blank=True)
    delete_status = models.IntegerField(blank=True, null=True)

    class Meta:
        models.Model_table = 't_accessory_type'


class TArrayCard(models.Model):
    accessory = models.ForeignKey(TAccessory, primary_key=True)
    array_card_interface = models.IntegerField(blank=True, null=True)
    array_card_cache = models.IntegerField(blank=True, null=True)
    array_card_buttery = models.IntegerField(blank=True, null=True)
    comment = models.TextField(blank=True)
    version = models.CharField(max_length=45, blank=True)
    cache_status = models.IntegerField(blank=True, null=True)
    strip_size = models.IntegerField(blank=True, null=True)
    read_write_ratio = models.CharField(max_length=45, blank=True)
    array_card_model = models.CharField(max_length=45, blank=True)


    class Meta:
        models.Model_table = 't_array_card'


class TCpu(models.Model):
    accessory = models.ForeignKey(TAccessory, primary_key=True)
    cpu_model = models.CharField(max_length=45, blank=True)
    cpu_core = models.IntegerField(blank=True, null=True)
    cpu_frequency = models.FloatField(blank=True, null=True)
    comment = models.TextField(blank=True)


    class Meta:
        models.Model_table = 't_cpu'


class TDisk(models.Model):
    accessory = models.ForeignKey(TAccessory, primary_key=True)
    disk_capacity = models.IntegerField(blank=True, null=True)
    disk_interface = models.IntegerField(blank=True, null=True)
    comment = models.TextField(blank=True)
    disk_model = models.CharField(max_length=45, blank=True)
    version = models.CharField(max_length=45, blank=True)
    bandwidth = models.IntegerField(blank=True, null=True)
    disk_type = models.IntegerField(blank=True, null=True)


    class Meta:
        models.Model_table = 't_disk'



class TFan(models.Model):
    accessory = models.ForeignKey(TAccessory, primary_key=True)
    fan_redundancy_level = models.IntegerField(blank=True, null=True)
    fan_max_speed = models.IntegerField(blank=True, null=True)
    fan_auto_regulation_support = models.IntegerField(blank=True, null=True)
    fan_position = models.IntegerField(blank=True, null=True)


    class Meta:
        models.Model_table = 't_fan'


class TGpu(models.Model):
    accessory = models.ForeignKey(TAccessory, primary_key=True)
    gpu_core_num = models.IntegerField(blank=True, null=True)
    gpu_memory = models.IntegerField(blank=True, null=True)
    gpu_frequency = models.IntegerField(blank=True, null=True)
    gpu_chip = models.CharField(max_length=45, blank=True)
    gpu_memory_specs = models.CharField(max_length=45, blank=True)
    gpu_power = models.IntegerField(blank=True, null=True)
    gpu_idle_power = models.IntegerField(blank=True, null=True)
    gpu_memory_bandwidth = models.IntegerField(blank=True, null=True)


    class Meta:
        models.Model_table = 't_gpu'


class TGuide(models.Model):
    guide_id = models.IntegerField(primary_key=True)
    comment = models.TextField(blank=True)
    used = models.IntegerField(blank=True, null=True)
    total_count = models.IntegerField(blank=True, null=True)
    guide_model = models.CharField(unique=True, max_length=45, blank=True)
    delete_status = models.IntegerField(blank=True, null=True)


    class Meta:
        models.Model_table = 't_guide'


class THbaCard(models.Model):
    accessory = models.ForeignKey(TAccessory, primary_key=True)
    hba_card_interface = models.IntegerField(blank=True, null=True)
    comment = models.TextField(blank=True)
    version = models.CharField(max_length=45, blank=True)
    hba_card_model = models.CharField(max_length=45, blank=True)


    class Meta:
        models.Model_table = 't_hba_card'


class TMemory(models.Model):
    accessory = models.ForeignKey(TAccessory, primary_key=True)
    memory_capacity = models.IntegerField(blank=True, null=True)
    memroy_frequency = models.IntegerField(blank=True, null=True)
    memory_specs = models.CharField(max_length=45, blank=True)
    comment = models.TextField(blank=True)


    class Meta:
        models.Model_table = 't_memory'


class TMotherBoard(models.Model):
    accessory = models.ForeignKey(TAccessory, primary_key=True)
    mother_board_model = models.CharField(max_length=45, blank=True)
    comment = models.TextField(blank=True)
    version = models.CharField(max_length=45, blank=True)
    pci_count = models.IntegerField(blank=True, null=True)
    pcie_count = models.IntegerField(blank=True, null=True)
    sata_count = models.IntegerField(blank=True, null=True)
    sas_count = models.IntegerField(blank=True, null=True)
    m_2_count = models.IntegerField(blank=True, null=True)
    satadom_count = models.IntegerField(blank=True, null=True)
    lom_count = models.IntegerField(blank=True, null=True)
    dimm_count = models.IntegerField(blank=True, null=True)
    mother_board_chip = models.CharField(max_length=45, blank=True)
    sd_support = models.IntegerField(blank=True, null=True)
    sata_controller_support = models.IntegerField(blank=True, null=True)
    sas_controller_support = models.IntegerField(blank=True, null=True)
    usb_count = models.IntegerField(blank=True, null=True)
    double_bios_protection_support = models.IntegerField(blank=True, null=True)
    asset_entry_support = models.IntegerField(blank=True, null=True)
    command_bios_support = models.IntegerField(blank=True, null=True)


    class Meta:
        models.Model_table = 't_mother_board'



class TNetworkCard(models.Model):
    accessory = models.ForeignKey(TAccessory, primary_key=True)
    speed = models.IntegerField(blank=True, null=True)
    network_card_interface = models.IntegerField(blank=True, null=True)
    network_card_model = models.CharField(max_length=45, blank=True)
    comment = models.TextField(blank=True)
    version = models.CharField(max_length=45, blank=True)
    mac_address = models.CharField(max_length=45, blank=True)
    network_card_ncsi_support = models.IntegerField(blank=True, null=True)
    network_card_pxe_support = models.IntegerField(blank=True, null=True)


    class Meta:
        models.Model_table = 't_network_card'


class TPower(models.Model):
    accessory = models.ForeignKey(TAccessory, primary_key=True)
    power_model = models.CharField(max_length=45, blank=True)
    power_specs = models.IntegerField(blank=True, null=True)
    efficiency = models.IntegerField(blank=True, null=True)
    power_supply = models.IntegerField(blank=True, null=True)
    version = models.CharField(max_length=45, blank=True)


    class Meta:
        models.Model_table = 't_power'

"""
