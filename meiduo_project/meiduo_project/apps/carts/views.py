import json

from django import http
from django.shortcuts import render

from goods.models import SKU
from utils.response_code import *
from django.views import View
import logging

logger = logging.getLogger('django')


class CartsView(View):
    """购物车"""

    def get(self, request):
        """展示购物车"""
        pass

    def post(self, request):
        """添加购物车"""
        # 接收参数
        json_str = request.body.decode()
        json_dict = json.loads(json_str)
        sku_id = json_dict.get('sku_id')
        count = json_dict.get('count')
        selected = json_dict.get('selected', True)
        user = request.user
        # 校验参数
        if not all([sku_id, count]):
            return http.JsonResponse({'code': RETCODE.DBERR, 'errmsg': '缺少参数'})
        # skuid是否存在
        try:
            sku = SKU.objects.get(id=sku_id)
        except Exception as e:
            logger.error(e)
            return http.JsonResponse({'code': RETCODE.DBERR, 'errmsg': '缺少skuid参数'})
        # count是否整数
        try:
            count = int(count)
        except Exception as e:
            logger.error(e)
            return http.JsonResponse({'code': RETCODE.DBERR, 'errmsg': 'count参数错误'})
        # selected是否bool
        if not isinstance(selected, bool):
            return http.JsonResponse({'code': RETCODE.DBERR, 'errmsg': 'selected参数错误'})
        if user.is_authenticated:
            # 已登录, redis
            pass
        else:
            # 未登录, cookie
            pass
        pass
