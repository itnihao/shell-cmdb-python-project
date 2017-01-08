from django.db import models
from apps.dpt import models as dpt_models


# Create your models here.

class TAuth(models.Model):
    apiid = models.CharField(max_length=45, blank=True)
    script = models.CharField(max_length=32, blank=True)
    token = models.CharField(max_length=45, blank=True)
    exp_time = models.DateTimeField(blank=True, null=True)
    delete_status = models.IntegerField(blank=True, null=True)


class TGroup(models.Model):
    groupid = models.BigIntegerField(primary_key=True)
    groupname = models.CharField(max_length=45, blank=True)
    delete_status = models.IntegerField(blank=True, null=True)

class TUserGroup(models.Model):
    ugid = models.BigIntegerField(primary_key=True)
    user = models.ForeignKey(dpt_models.TBspUser, blank=True, null=True)
    group = models.ForeignKey('TGroup', blank=True, null=True)
    delete_status = models.IntegerField(blank=True, null=True)

class TRole(models.Model):
    roleid = models.BigIntegerField(primary_key=True)
    rolename = models.CharField(max_length=45, blank=True)
    delete_status = models.IntegerField(blank=True, null=True)

class TGroupRole(models.Model):
    grid = models.BigIntegerField(primary_key=True)
    group = models.ForeignKey('TGroup', blank=True, null=True)
    role = models.ForeignKey('TRole', blank=True, null=True)
    delete_status = models.IntegerField(blank=True, null=True)

class TModular(models.Model):
    mid = models.BigIntegerField(primary_key=True)
    modularname = models.CharField(max_length=45, blank=True)
    delete_status = models.IntegerField(blank=True, null=True)


class TPermissionsType(models.Model):
    ptid = models.BigIntegerField(primary_key=True)
    permission = models.CharField(max_length=45, blank=True)
    delete_status = models.IntegerField(blank=True, null=True)

class TOperation(models.Model):
    opid = models.BigIntegerField(primary_key=True)
    name = models.CharField(max_length=45, blank=True)
    key = models.CharField(max_length=45, blank=True)
    uri = models.CharField(max_length=45, blank=True)
    buttonid = models.CharField(max_length=45, blank=True)
    http_method = models.CharField(max_length=45, blank=True)
    permission = models.ForeignKey('TPermissionsType', blank=True, null=True)
    permission_status = models.IntegerField(blank=True, null=True)
    delete_status = models.IntegerField(blank=True, null=True)

class TMenu(models.Model):
    mid = models.BigIntegerField(primary_key=True)
    name = models.CharField(max_length=45, blank=True)
    uri = models.CharField(max_length=45, blank=True)
    delete_status = models.IntegerField(blank=True, null=True)

class TMenuRole(models.Model):
    muid = models.BigIntegerField(primary_key=True)
    role = models.ForeignKey('TRole', blank=True, null=True)
    menu = models.ForeignKey('TMenu', blank=True, null=True)
    delete_status = models.IntegerField(blank=True, null=True)


class TRoleModularPermissionsType(models.Model):
    rmptid = models.BigIntegerField(primary_key=True)
    role = models.ForeignKey('TRole', blank=True, null=True)
    modular = models.ForeignKey('TModular', blank=True, null=True)
    permission = models.ForeignKey('TPermissionsType', blank=True, null=True)
    delete_status = models.IntegerField(blank=True, null=True)

class TModularOperation(models.Model):
    moid = models.BigIntegerField(primary_key=True)
    modular = models.ForeignKey('TModular', blank=True, null=True)
    operation = models.ForeignKey('TOperation', blank=True, null=True)
    delete_status = models.IntegerField(blank=True, null=True)

# class TPerssionsTypeOperation(models.Model):
#     ptoid = models.BigIntegerField(primary_key=True)
#     permission = models.ForeignKey('TPermissionsType', blank=True, null=True)
#     operation = models.ForeignKey('TOperation', blank=True, null=True)
#     delete_status = models.IntegerField(blank=True, null=True)

#class TModularRole(models.Model):
#    mduid = models.BigIntegerField(primary_key=True)
#    modular = models.ForeignKey('TModular', blank=True, null=True)
#    role = models.ForeignKey('TRole', blank=True, null=True)
#    delete_status = models.IntegerField(blank=True, null=True)

#class TPermissionsTypeRole(models.Model):
#    ptrid = models.BigIntegerField(primary_key=True)
#    role = models.ForeignKey('TRole', blank=True, null=True)
#    permission = models.ForeignKey('TPermissionsType', blank=True, null=True)
#    delete_status = models.IntegerField(blank=True, null=True)

#class TModularOperation(models.Model):
#    moid = models.BigIntegerField(primary_key=True)
#    modular = models.ForeignKey('TModular', blank=True, null=True)
#    operation = models.ForeignKey('TOperation', blank=True, null=True)
#    delete_status = models.IntegerField(blank=True, null=True)
