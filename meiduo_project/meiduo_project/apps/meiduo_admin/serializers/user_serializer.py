from rest_framework import serializers
from users.models import User


class UserSerializer(serializers.ModelSerializer):
    """查询用户序列化器"""
    class Meta:
        model = User
        fields = ('id', 'username', 'mobile', 'email')
