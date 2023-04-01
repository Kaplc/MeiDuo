from rest_framework import serializers
from django.contrib.auth.models import Permission, Group


class PermissionSerializer(serializers.ModelSerializer):
    """权限表"""

    class Meta:
        model = Permission
        fields = '__all__'


class ContentTypesSerializer(serializers.ModelSerializer):
    """权限类型名称"""

    class Meta:
        model = Permission
        fields = ('id', 'name',)


class GroupSerializer(serializers.ModelSerializer):
    """用户组"""

    class Meta:
        model = Group
        fields = '__all__'
