from django.db import models
# noinspection PyUnresolvedReferences
from meiduo_project.utils.models import BaseModel


# Create your models here.

class OAuthQQUser(BaseModel):
    """QQ登录用户数据"""
    """
    https://graph.qq.com/oauth2.0/show?which=error&display=pc&error=100010&which=Login&display=pc&response_type=code&client_id=101518219
    &redirect_uri=http%3A%2F%2Fwww.meiduo.site%3A8000%2Foauth_callback&state=%2F
    """
    user = models.ForeignKey('users.User', on_delete=models.CASCADE, verbose_name='用户')
    openid = models.CharField(max_length=64, verbose_name='openid', db_index=True)

    class Meta:
        db_table = 'tb_oauth_qq'
        verbose_name = 'QQ登录用户数据'
        verbose_name_plural = verbose_name

