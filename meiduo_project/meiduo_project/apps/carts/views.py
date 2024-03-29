import decimal
import json
from .utils import cookie_to_dict, dict_to_cookie
from django import http
from django.shortcuts import render
from django_redis import get_redis_connection
from goods.models import SKU
from meiduo_project.utils.response_code import *
from django.views import View
import logging

logger = logging.getLogger('django')


class CartsSimpleView(View):
    """简单购物车"""

    def get(self, request):
        """展示简单购物车"""
        user = request.user
        if user.is_authenticated:
            # 登录用户查询redis
            conn_redis = get_redis_connection('carts')
            redis_carts = conn_redis.hgetall('carts_%s' % user.id)
            selected_sku_ids = conn_redis.smembers('selected_%s' % user.id)
            # 构造cookie购物车数据结构方便后续查询
            carts_dict = {}
            for sku_id, count in redis_carts.items():
                selected = 'false'
                for selected_sku_id in selected_sku_ids:

                    if selected_sku_id == sku_id:
                        selected = 'true'
                carts_dict[int(sku_id.decode())] = {
                    'count': int(count.decode()),
                    'selected': selected
                }

        else:
            # 未登录查询cookie
            cookie_carts = request.COOKIES.get('carts')
            if cookie_carts is None:
                return http.JsonResponse({'code': RETCODE.DBERR, 'errmsg': '查询失败'})

            carts_dict = cookie_to_dict(cookie_carts)

        # 查询sku集合
        try:
            carts_sku_ids = carts_dict.keys()
            skus = SKU.objects.filter(id__in=carts_sku_ids)

        except Exception as e:
            logger.error(e)
            return http.JsonResponse({'code': RETCODE.DBERR, 'errmsg': '查询失败'})

        # sku数据列表
        skus_list = []
        for sku in skus:
            for carts_sku_id in carts_sku_ids:
                if sku.id == carts_sku_id:
                    # 构造响应数据sku列表
                    skus_list.append({
                        'id': sku.id,
                        'name': sku.name,
                        'count': carts_dict[sku.id]['count'],
                        'default_image_url': sku.default_image_url.url
                    })

        # 构造响应json
        response_json = {
            'code': RETCODE.OK,
            'errmsg': 'OK',
            'cart_skus': skus_list
        }

        return http.JsonResponse(response_json)


class CartsSelectAllView(View):
    """全选购物车"""

    def put(self, request):
        """全选购物车"""
        # 接收参数
        user = request.user
        json_str = request.body.decode()
        json_dict = json.loads(json_str)
        selected = str(json_dict['selected'])
        if not all([selected]):
            return http.HttpResponseForbidden('缺少参数')
        response = http.JsonResponse({'code': RETCODE.OK, 'errmsg': 'OK'})
        if user.is_authenticated:
            # 已登录
            conn_redis = get_redis_connection('carts')
            # 获取的是dict
            carts_dict = conn_redis.hgetall('carts_%s' % user.id)
            # 获取dict的所有key
            carts_dict_keys = carts_dict.keys()
            # 更新是否勾选
            if selected:
                conn_redis.sadd('selected_%s' % user.id, *carts_dict_keys)
            else:
                conn_redis.srem('selected_%s' % user.id, *carts_dict_keys)

        else:
            # 未登录

            cookie_carts = request.COOKIES.get('carts')
            dict_carts = cookie_to_dict(cookie_carts)
            for carts_sku in dict_carts:
                dict_carts[carts_sku]['selected'] = selected
            cookie_carts = dict_to_cookie(dict_carts)
            response.set_cookie('carts', cookie_carts)
        return response


class CartsView(View):
    """购物车"""

    def delete(self, request):
        """删除购物车"""
        # 接收参数
        user = request.user
        json_str = request.body.decode()
        json_dict = json.loads(json_str)
        sku_id = json_dict['sku_id']
        # 校验参数
        if not all([sku_id]):
            return http.HttpResponseForbidden('缺少参数')
        # 删除数据
        response = http.JsonResponse({'code': RETCODE.OK, 'errmsg': 'OK'})
        if user.is_authenticated:
            # 已登录
            conn_redis = get_redis_connection('carts')
            pl = conn_redis.pipeline()
            # 删除购物车商品
            pl.hdel('carts_%s' % user.id, sku_id)
            # 删除勾选
            pl.srem('selected_%s' % user.id, sku_id)
            pl.execute()
        else:
            # 未登录
            cookie_carts = request.COOKIES.get('carts')
            dict_carts = cookie_to_dict(cookie_carts)
            del dict_carts[sku_id]
            cookie_carts = dict_to_cookie(dict_carts)
            response.set_cookie('carts', cookie_carts)
        return response

    def put(self, request):
        """修改购物车"""
        # 接收参数
        user = request.user
        json_str = request.body.decode()
        json_dict = json.loads(json_str)
        sku_id = json_dict['sku_id']
        count = json_dict['count']
        selected = json_dict['selected']
        if not all([sku_id, count]):
            return http.HttpResponseForbidden('缺少参数')
        response = http.JsonResponse({'code': RETCODE.OK, 'errmsg': 'OK'})
        if user.is_authenticated:
            # 已登录
            conn_redis = get_redis_connection('carts')
            pl = conn_redis.pipeline()
            # 用新count覆盖
            pl.hset('carts_%s' % user.id, sku_id, count)
            # 更新是否勾选
            if selected:
                pl.sadd('selected_%s' % user.id, sku_id)
            else:
                pl.srem('selected_%s' % user.id, sku_id)
            pl.execute()
        else:
            # 未登录

            cookie_carts = request.COOKIES.get('carts')
            dict_carts = cookie_to_dict(cookie_carts)
            dict_carts[sku_id]['count'] = count
            dict_carts[sku_id]['selected'] = selected
            cookie_carts = dict_to_cookie(dict_carts)
            response.set_cookie('carts', cookie_carts)
        return response

    def get(self, request):
        """展示购物车"""
        user = request.user

        if user.is_authenticated:
            # 登录用户

            conn_redis = get_redis_connection('carts')
            sku_ids = conn_redis.hkeys('carts_%s' % user.id)  # 购物车所有sku
            if not sku_ids:
                context = {
                    'cart_skus': [],
                }
                return render(request, 'cart.html', context)
            try:
                skus = SKU.objects.filter(id__in=sku_ids)
            except Exception as e:
                logger.error(e)
                return render(request, '404.html')

            for sku in skus:

                count = conn_redis.hget('carts_%s' % user.id, sku.id).decode()  # 当前商品的数量
                selected = conn_redis.sismember('selected_%s' % user.id, sku.id)  # 判断是否勾选
                if selected:
                    selected = 'True'
                else:
                    selected = 'False'
                # 数据动态绑定到sku
                sku.selected = selected
                sku.count = count

        else:
            # 未登录用户
            # 获取cookie购物车
            cookie_carts = request.COOKIES.get('carts')

            if not cookie_carts:
                # 没有购物车创建空字典返回
                dict_carts = {}
                cookie_carts = dict_to_cookie(dict_carts)
                context = {
                    'cart_skus': [],
                }
                response = render(request, 'cart.html', context)

                response.set_cookie('carts', cookie_carts)
                return response

            carts_dict = cookie_to_dict(request.COOKIES.get('carts'))
            sku_ids = carts_dict.keys()
            try:
                skus = SKU.objects.filter(id__in=sku_ids)
            except Exception as e:
                logger.error(e)
                return render(request, '404.html')
            for sku in skus:
                sku.count = carts_dict[sku.id]['count']
                sku.selected = str(carts_dict[sku.id]['selected'])

        # 定义购物车sku信息列表
        cart_skus = []
        total_amount = 0
        for sku in skus:
            cart_skus.append({
                'id': sku.id,
                'name': sku.name,
                'count': int(sku.count),
                'selected': sku.selected,
                'default_image_url': sku.default_image_url.url,
                'price': str(sku.price),
                'amount': str(decimal.Decimal(sku.count) * sku.price)
            })
            total_amount += decimal.Decimal(sku.count) * sku.price

        context = {
            'goods_count': len(cart_skus),
            'total_amount': total_amount,
            'cart_skus': cart_skus,
        }

        return render(request, 'cart.html', context)

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
            SKU.objects.get(id=sku_id)
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

        response = http.JsonResponse({'code': RETCODE.OK, 'errmsg': 'OK'})
        if user.is_authenticated:
            # 已登录, redis
            conn_redis = get_redis_connection('carts')
            pl = conn_redis.pipeline()
            # HINCRBY key field increment
            # 为哈希表 key 中的域 field 的值加上增量 increment
            pl.hincrby('carts_%s' % user.id, sku_id, count)
            if selected:
                # selected不为空添加
                pl.sadd('selected_%s' % user.id, sku_id)
            # 执行
            pl.execute()
        else:
            # 未登录, cookie
            # 获取cookie
            cookie_carts = request.COOKIES.get('carts')
            if cookie_carts:
                # 有购物车cookie转dict
                dict_carts = cookie_to_dict(cookie_carts)
            else:
                # 没有购物车创建空字典
                dict_carts = {}
            # 添加数据

            if dict_carts.get(sku_id):
                # skuid重复
                # 增量
                dict_carts[sku_id]['count'] += count
            else:
                # 新商品
                dict_carts[sku_id] = {
                    'count': count,
                }
            dict_carts[sku_id]['selected'] = selected
            cookie_carts = dict_to_cookie(dict_carts)
            response.set_cookie('carts', cookie_carts)

        return response
