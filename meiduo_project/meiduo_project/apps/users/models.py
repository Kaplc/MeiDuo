from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.


class User(AbstractUser):
    """自定义用户模型类"""
    # 定义字段
    mobile = models.CharField(max_length=11, unique=True, verbose_name='手机号')
    email_active = models.BooleanField(default=False, verbose_name='邮箱验证状态')

    # 后台管理显示
    class Meta:
        db_table = 'tb_user'  # 自定义表名
        verbose_name = '用户'
        verbose_name_plural = verbose_name

    # print(User)显示username
    def __str__(self):
        return self.username


class Area(models.Model):
    """省市区表"""
    name = models.CharField(max_length=20, verbose_name='名称')
    parent = models.ForeignKey('self', on_delete=models.SET_NULL, related_name='subs', null=True, blank=True,
                               verbose_name='上级行政区划')

    class Meta:
        db_table = 'tb_areas'
        verbose_name = '省市区'
        verbose_name_plural = '省市区'

    def __str__(self):
        return self.name

