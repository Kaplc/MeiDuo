from rest_framework.generics import ListAPIView
from meiduo_admin.serializers.user_serializer import UserSerializer
from meiduo_admin.utils import PageNum
from users.models import User


# ListAPIView继承GenericAPIView、ListModelMixin
class UserView(ListAPIView):
    # 指定使用的序列化器
    serializer_class = UserSerializer
    # 指定分页器
    pagination_class = PageNum

    # 重写获取查询集方法
    def get_queryset(self):
        # 获取传递过来的keyword参数
        keyword = self.request.query_params.get('keyword')

        if keyword == '' or keyword is None:
            # 为空获取所有用户数据
            queryset = User.objects.all().order_by('is_staff')
            return queryset
        else:
            queryset = User.objects.filter(username=keyword).order_by('username')
            return queryset


