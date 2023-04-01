from rest_framework.permissions import IsAdminUser
from rest_framework.viewsets import ModelViewSet

from goods.models import SpecificationOption
from meiduo_admin.serializers import specs_serializer
from meiduo_admin.utils import PageNum


class SpecsOptionsView(ModelViewSet):
    """
        meiduo_admin/specs/options/
        规格管理
    """
    queryset = SpecificationOption.objects.all().order_by('id')
    # 指定序列化器
    serializer_class = specs_serializer.SpecificationOptionSerializer
    pagination_class = PageNum
    permission_classes = [IsAdminUser]