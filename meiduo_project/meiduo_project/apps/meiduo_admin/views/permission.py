from django.contrib.auth.models import Permission
from rest_framework.decorators import action
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from meiduo_admin.utils import PageNum
from meiduo_admin.serializers import permission_serializer


class PermissionView(ModelViewSet):
    queryset = Permission.objects.all()
    pagination_class = PageNum
    serializer_class = permission_serializer.PermissionSerializer
    permission_classes = [IsAdminUser]



class ContentTypes(ModelViewSet):
    queryset = Permission.objects.all()
    pagination_class = PageNum
    serializer_class = permission_serializer.ContentTypesSerializer
    permission_classes = [IsAdminUser]
