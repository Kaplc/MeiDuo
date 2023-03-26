from rest_framework import serializers
from users.models import User
import logging

logger = logging.getLogger('django')


class UserSerializer(serializers.ModelSerializer):
    """查询用户序列化器"""

    class Meta:
        model = User
        fields = ('id', 'username', 'mobile', 'email')


class UserAddSerializer(serializers.ModelSerializer):
    """添加用户数据"""
    # 定义数据保存格式
    username = serializers.CharField(max_length=20, min_length=5)
    # rite_only=True只写入，保存成功不返回
    password = serializers.CharField(write_only=True)

    def create(self, validated_data):
        # '**'字典解析为key-value
        try:
            user = User.objects.create_user(
                **validated_data
            )
            return user
        except Exception as e:
            logger.error(e)

    class Meta:
        model = User
        fields = ('id', 'username', 'mobile', 'email', 'password')
