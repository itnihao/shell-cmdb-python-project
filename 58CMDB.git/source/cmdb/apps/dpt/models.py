from __future__ import unicode_literals


from django.db import models

class TBspOrg(models.Model):
    org_id = models.CharField(primary_key=True, max_length=50)
    org_name = models.CharField(max_length=50, blank=True)
    org_level = models.IntegerField(blank=True, null=True)
    parent_id = models.ForeignKey('TBspOrg', blank=True, null=True)
    class Meta:
        db_table = 't_bsp_org'

class TBspUser(models.Model):
    bsp_user_id = models.CharField(primary_key=True, max_length=22)
    account = models.CharField(max_length=64)
    delete_status = models.CharField(max_length=1)
    nickname = models.CharField(max_length=22)
    # org_id = models.ForeignKey('TBspOrg', blank=True, null=True)
    org = models.ForeignKey('TBspOrg', blank=True, null=True)
    duty_id = models.CharField(max_length=22)
    email = models.CharField(max_length=22)
    mobile = models.CharField(max_length=22)
    gender = models.CharField(max_length=1)
    tel = models.CharField(max_length=22, blank=True)
    child_tel = models.CharField(max_length=22)
    post = models.CharField(max_length=22)
    weixin = models.CharField(max_length=255, blank=True)
    on_board_time = models.CharField(max_length=22)
    employ_id = models.CharField(max_length=22)
    city_id = models.CharField(max_length=22)
    qq = models.CharField(max_length=22)
    leaders = models.CharField(max_length=100)
    description = models.CharField(max_length=200)
    empclassify = models.CharField(max_length=22)
    position_name = models.CharField(max_length=22)
    is_agency = models.CharField(max_length=1)
    ageny_path = models.CharField(max_length=400)
    remark = models.TextField()
    create_time = models.IntegerField(blank=True, null=True)
    update_time = models.IntegerField(blank=True, null=True)

    class Meta:
        db_table = 't_bsp_user'


class TBusline(models.Model):
    busline_id = models.AutoField(primary_key=True)
    busline_code = models.CharField(max_length=255)
    busline_name = models.CharField(max_length=255)
    owner_op = models.ForeignKey('TBspUser', related_name='opowner')
    owner_biz = models.ForeignKey('TBspUser', related_name='bizuser')
    busline_level = models.IntegerField(blank=True, null=True)
    parent = models.ForeignKey('TBusline', related_name='busline')
    is_leaf = models.IntegerField(blank=True, null=True)
    bsp_org = models.ForeignKey('TBspOrg', related_name='bsp_org')
    fullpath = models.CharField(max_length=255, blank=True)
    description = models.CharField(max_length=255, blank=True)
    state = models.IntegerField(blank=True, null=True)

    class Meta:
        db_table = 't_busline'


class TBuslineUser(models.Model):
    busline_user_id = models.BigIntegerField(primary_key=True)
    bsp_user = models.ForeignKey('TBspUser', related_name='bspuserid')
    busline = models.ForeignKey('TBusline', related_name='buslineid')
    role = models.IntegerField(blank=True, null=True)
    state = models.IntegerField(blank=True, null=True)

    class Meta:
        db_table = 't_busline_user'


class TCluster(models.Model):
    cluster_id = models.BigIntegerField(primary_key=True)
    cluster_name = models.CharField(unique=True, max_length=50)
    cluster_code = models.CharField(unique=True, max_length=50)
    busline_id = models.ForeignKey('TBusline', blank=True, null=True)
    busline_owner = models.ForeignKey('TBspUser', related_name='buslineuser')
    op_owner = models.ForeignKey('TBspUser', related_name='opuser')
    create_time = models.DateTimeField(blank=True, null=True)
    update_time = models.DateTimeField(blank=True, null=True)
    cluster_state = models.IntegerField()

    class Meta:
        db_table = 't_cluster'


class TClusterServer(models.Model):
    cluster_server_id = models.BigIntegerField(primary_key=True)
    cluster_id = models.ForeignKey('TCluster', related_name='cluster')
    server_id = models.ForeignKey('server_device.TServer', related_name='server_device')
    add_time = models.DateTimeField(db_index=True, auto_now_add=True)
    state = models.IntegerField(blank=True, null=True)

    class Meta:
        db_table = 't_cluster_server'


class TResourcePool(models.Model):
    #resource_pool_id = models.IntegerField(primary_key=True)
    resource_pool_id = models.AutoField(primary_key=True)
    resource_pool_name = models.CharField(max_length=255)
    description = models.CharField(max_length=255, blank=True)
    state = models.IntegerField(blank=True, null=True)
    create_time = models.DateTimeField(blank=True, null=True)
    creater_id = models.ForeignKey('TBspUser', blank=True, null=True)

    class Meta:
        db_table = 't_resource_pool'


class TResourcePoolServer(models.Model):
    resource_pool_server_id = models.BigIntegerField(primary_key=True)
    resource_pool_id = models.ForeignKey('TResourcePool', blank=True, null=True)
    server_id = models.ForeignKey('server_device.TServer', related_name='server')
    busline_id = models.ForeignKey('TBusline', blank=True, null=True)
    add_time = models.DateTimeField(blank=True, null=True)
    bsp_user_id = models.ForeignKey('TBspUser', related_name='bspuser')

    class Meta:
        db_table = 't_resource_pool_server'

class TClusterUser(models.Model):
    cluster_user_id = models.BigIntegerField(primary_key=True)
    cluster = models.ForeignKey('TCluster', blank=True, null=True)
    bsp_user = models.ForeignKey('TBspUser', blank=True, null=True)
    role = models.IntegerField(blank=True, null=True)
    state = models.IntegerField(blank=True, null=True)
    add_time = models.DateTimeField()
    operation_user = models.ForeignKey('TBspUser', blank=True, null=True, related_name='operation_user')
    start_time = models.DateTimeField(blank=True, null=True)
    end_time = models.DateTimeField(blank=True, null=True)

    class Meta:
        db_table = 't_cluster_user'
