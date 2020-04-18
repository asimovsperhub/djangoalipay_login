from django.db import models

# Create your models here.


class Userinfo(models.Model):
    # 用户id
    user_id = models.CharField(max_length=50)
    # name
    nike_name = models.CharField(max_length=50)
    # 性别(m,)
    gender = models.CharField(max_length=5)
    # 省份
    province = models.CharField(max_length=20)
    # 城市
    city = models.CharField(max_length=20)
    # 头像链接
    avatar = models.CharField(max_length=200)
    # 用户补充信息

    # 手机
    #phone = models.IntegerField(blank=True,null=True)
    # 邮箱
    emial = models.EmailField(max_length=50, blank=True)
