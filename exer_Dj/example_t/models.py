from __future__ import unicode_literals

from django.db import models

# Create your models here.

class Models_test(models.Model):
    models_id=models.CharField(max_length=255,null=False)
    text=models.CharField(max_length=255,null=False)