import logging
from django.utils import timezone
from orders.models import OrderInfo
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser
from datetime import date, timedelta
from goods.models import GoodsVisitCount
from users.models import User
from meiduo_admin.serializers.statistical_serializer import GoodsSerializer

logger = logging.getLogger('django')


class UserTotalCountView(APIView):
    """返回用户总数"""
    # drf权限认证
    permission_classes = [IsAdminUser]

    def get(self, request):

        # 获取当前日期
        now_day = timezone.now().date()

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
        now_day = timezone.now().date()

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


class UserActiveCountView(APIView):
    """日活跃用户"""
    # 指定管理员权限
    permission_classes = [IsAdminUser]

    def get(self, request):
        # 获取当前日期
        now_day = timezone.now().date()

        try:
            # __gte大于等于
            count = User.objects.filter(last_login__gte=now_day, is_staff=False).count()
        except Exception as e:
            logger.error(e)
            count = None

        return Response({
            "count": count,
            "date": now_day
        })


class UserOrderCountView(APIView):
    """日下单"""
    # 指定管理员权限
    permission_classes = [IsAdminUser]

    def get(self, request):
        now_day = timezone.now().date()
        try:
            # __gte大于等于
            count = OrderInfo.objects.filter(create_time__gte=now_day).count()
        except Exception as e:
            logger.error(e)
            count = None

        return Response({
            "count": count,
            "date": now_day
        })


class UserMonthCountView(APIView):
    """月活跃用户+每日"""
    # 指定管理员权限
    permission_classes = [IsAdminUser]

    def get(self, request):
        now_day = timezone.now().date()
        start_date = now_day - timedelta(29)
        # 创建日用户列表
        date_list = []
        try:
            for i in range(30):
                # 下一天日期
                next_date = start_date + timedelta(1)
                count = User.objects.filter(date_joined__gte=start_date, date_joined__lt=next_date,
                                            is_staff=False).count()
                date_list.append({
                    'count': count,
                    'date': start_date
                })
                # 下一天作为当天
                start_date = next_date
        except Exception as e:
            logger.error(e)

        return Response(date_list)


class GoodsDayView(APIView):
    """日分类商品访问量"""
    permission_classes = [IsAdminUser]

    def get(self, request):
        # 获取当天日期
        now_date = timezone.now().date()

        data = GoodsVisitCount.objects.filter(date=now_date)

        # many=True序列化多个对象
        ser = GoodsSerializer(data, many=True)

        return Response(ser.data)
