from rest_framework.generics import ListAPIView, ListCreateAPIView
from rest_framework.permissions import IsAdminUser

from meiduo_admin.serializers.user_serializer import UserSerializer, UserAddSerializer
from meiduo_admin.utils import PageNum
from users.models import User


# ListAPIView继承GenericAPIView、ListModelMixin
class UserView(ListCreateAPIView):
    # 指定分页器
    pagination_class = PageNum
    permission_classes = [IsAdminUser]
    # 序列化器选择方法
    def get_serializer_class(self):

        if self.request.method == 'GET':
            return UserSerializer
        else:
            # POST
            return UserAddSerializer

    # 重写获取查询集方法
    def get_queryset(self):
        # 获取传递过来的keyword参数
        keyword = self.request.query_params.get('keyword')

        if keyword == '' or keyword is None:
            # 为空获取所有用户数据
            queryset = User.objects.all().order_by('is_staff')
            return queryset
        else:
            # 模糊搜索
            queryset = User.objects.filter(username__contains=keyword).order_by('username')
            return queryset
