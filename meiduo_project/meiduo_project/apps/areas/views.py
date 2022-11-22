from django.shortcuts import render
from django.views import View
from .models import Area
from django import http
from utils.response_code import RETCODE
import logging

logger = logging.getLogger('django')


class Areas(View):
    """查询省市区数据"""

    def get(self, request):
        # 接收参数
        area_id = request.GET.get('area_id')
        # 查询数据
        if not area_id:
            # 查询省份
            try:
                model_list = Area.objects.filter(parent_id=None)
                # 模型列表转列表
                province_list = [

                ]
                for i in model_list:
                    add_dict = {
                        'id': i.id,
                        'name': i.name
                    }
                    province_list.append(add_dict)

            except Exception as e:
                logger.error(e)
                return http.JsonResponse({'code': RETCODE.DBERR, 'errmsg': "查询失败"})

            return http.JsonResponse({'code': RETCODE.OK, "errmsg": "OK", 'province_list': province_list})
        else:
            # 查询市区

            pass
        pass
