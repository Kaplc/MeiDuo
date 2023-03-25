import logging

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser, AllowAny
from datetime import date

from users.models import User

logger = logging.getLogger('django')


class UserTotalCountView(APIView):
    """返回用户总数"""
    # drf权限认证
    permission_classes = [IsAdminUser]

    def get(self, request):

        # 获取当前日期
        now_day = date.today()

        try:
            count = User.objects.all().count()
        except Exception as e:
            logger.error(e)
            count = None

        return Response({
            'count': count,
            'date': now_day
        })
