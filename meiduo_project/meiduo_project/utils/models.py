from django.db import models


class BaseModel(models.Model):
    """创建模型类基类补充字段"""
    creat_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间', )
    update_time = models.DateTimeField(auto_now=True, verbose_name='修改时间')

    class Meta:
        # 说明是抽象类, 用于继承使用, 在迁移时不会创建新表
        abstract = True