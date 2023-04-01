from rest_framework import serializers
from django.contrib.auth.models import Permission


class PermissionSerializer(serializers.ModelSerializer):
    """权限表"""

    class Meta:
        model = Permission
        fields = '__all__'


class ContentTypesSerializer(serializers.ModelSerializer):
    """权限类型名称"""

    class Meta:
        model = Permission
        fields = ('content_types',)
