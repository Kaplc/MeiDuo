from django.shortcuts import render
from django.views import View
from .models import Area
from django import http
from django.core.cache import cache
from meiduo_project.utils.response_code import RETCODE
from .contents import CACHE_EXPIRATION
import logging

logger = logging.getLogger('django')


class Areas(View):
    """查询省市区数据"""

    def get(self, request):
        # 接收参数
        area_id = request.GET.get('area_id')
        # 查询数据
        if not area_id:
            # 读取省份缓存数据
            province_list = cache.get('province_list')
            if not province_list:
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
                # 存储缓存数据cache.set('key', 数据, 过期时间)
                cache.set('province_list', province_list, CACHE_EXPIRATION)
            return http.JsonResponse({'code': RETCODE.OK, "errmsg": "OK", 'province_list': province_list})

        else:

            response = cache.get('city_list' + area_id)
            if not response:
                # 查询市区
                try:
                    parent_model_list = Area.objects.get(id=area_id)

                    # 父级查询子行政区数据
                    children_model_list = parent_model_list.subs.all()

                    # 模型列表转列表
                    subs = [

                    ]
                    for i in children_model_list:
                        add_dict = {
                            'id': i.id,
                            'name': i.name
                        }
                        subs.append(add_dict)

                    # 拼接响应数据
                    response = {
                        'code': RETCODE.OK,
                        'errmsg': '查询成功',
                        'sub_data': {
                            'id': parent_model_list.id,
                            'name': parent_model_list.name,
                            'subs': subs
                        }
                    }
                except Exception as e:
                    logger.error(e)
                    return http.JsonResponse({'code': RETCODE.DBERR, 'errmsg': "查询失败"})

                cache.set('city_list' + area_id, response, CACHE_EXPIRATION)

            return http.JsonResponse(response)
