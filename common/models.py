from django.db import models

# Create your models here.

class Customer(models.Model):
    # 客户名称
    name = models.CharField(max_length=200)
    # 联系电话
    phone = models.CharField(max_length=200)
    # 地址
    address  = models.CharField(max_length=200)