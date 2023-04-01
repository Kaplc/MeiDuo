from django.contrib.auth.models import Permission, Group
from rest_framework.decorators import action
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from meiduo_admin.utils import PageNum
from meiduo_admin.serializers import permission_serializer
from users.models import User


class PermissionView(ModelViewSet):
    """
        permission/perms
        权限表
    """
    queryset = Permission.objects.all().order_by('id')
    pagination_class = PageNum
    serializer_class = permission_serializer.PermissionSerializer
    permission_classes = [IsAdminUser]

    def content_types(self, request):
        """
            permission/content_types
            权限表权限名称
        """
        ser = permission_serializer.ContentTypesSerializer(Permission.objects.all().order_by('id'), many=True)
        return Response(ser.data)

    def simple(self):
        """
            meiduo_admin/permission/simple/

        """
        ser = permission_serializer.ContentTypesSerializer(Permission.objects.all().order_by('id'), many=True)
        return Response(ser.data)


class ContentTypesView(ModelViewSet):
    queryset = Permission.objects.all().order_by('id')
    serializer_class = permission_serializer.ContentTypesSerializer
    permission_classes = [IsAdminUser]


class GroupsView(ModelViewSet):
    """
        permission/groups
        权限组
    """
    queryset = Group.objects.all().order_by('id')
    pagination_class = PageNum
    serializer_class = permission_serializer.GroupSerializer
    permission_classes = [IsAdminUser]

    # action装饰器， 前提自动生成路由路由前缀要相同
    @action(methods=['get'], detail=False)
    def simple(self, request):
        ser = permission_serializer.GroupSerializer(Group.objects.all().order_by('id'), many=True)
        return Response(ser.data)


class AdminView(ModelViewSet):
    """
        permission/admins
        管理员管理
    """
    queryset = User.objects.filter(is_staff=True).order_by('id')
    pagination_class = PageNum
    serializer_class = permission_serializer.AdminSerializer
    permission_classes = [IsAdminUser]
