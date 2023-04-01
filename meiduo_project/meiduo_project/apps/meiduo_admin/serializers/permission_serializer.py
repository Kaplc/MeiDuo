from rest_framework import serializers
from django.contrib.auth.models import Permission, Group

from users.models import User


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


class AdminSerializer(serializers.ModelSerializer):
    """管理员"""

    # user_permissions =
    # groups =

    def create(self, validated_data):
        password = validated_data.get('password')
        # 添加管理员标识
        validated_data['is_staff'] = True
        # 调用父类保存方法
        admin = super().create(validated_data)
        # 密码加密保存数据库
        admin.set_password(password)
        admin.save()
        return admin

    def update(self, instance, validated_data):
        password = validated_data.get('password')
        # 调用父类保存方法
        admin = super().update(instance, validated_data)
        # 密码加密保存数据库
        admin.set_password(password)
        admin.save()
        return admin

    class Meta:
        model = User
        fields = '__all__'
        # 添加字段参数
        extra_kwargs = {
            'password': {
                # 只参与反序列化
                'write_only': True
            }
        }
