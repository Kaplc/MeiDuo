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


class UserDayCountView(APIView):
    """日增用户统计"""
    # drf权限认证
    permission_classes = [IsAdminUser]

    def get(self, request):
        # 获取当前日期
        now_day = date.today()

        try:
            # __gte大于等于
            count = User.objects.filter(date_joined__gte=now_day, is_staff=False).count()
        except Exception as e:
            logger.error(e)
            count = None

        return Response({
            "count": count,
            "date": now_day
        })

