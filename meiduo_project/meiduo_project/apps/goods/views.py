import json

from django import http
from django.core.paginator import Paginator
from django.shortcuts import render
from django.views import View
from .contents import *
from goods.models import GoodsCategory, SKU
from goods.utils import get_categories, get_breadcrumb
from meiduo_project.utils.response_code import RETCODE
from .utils import get_categories, get_breadcrumb
import logging

logger = logging.getLogger('django')


class DetailView(View):
    """商品详情"""

    def get(self, request, sku_id):
        """展示商品详情页"""
        # 接收参数
        sku_id = sku_id
        # 校验参数
        try:
            sku = SKU.objects.get(id=sku_id)

        except Exception as e:
            logger.error(e)
            return render(request, '404.html')

        # 获取商品分类
        categories = get_categories()
        # 获取面包屑导航
        breadcrumb = get_breadcrumb(sku.category)
        # jinja2渲染内容
        context = {
            'categories': categories,
            'breadcrumb': breadcrumb,

        }
        return render(request, 'detail_sku.html', context)


class HotGoodsView(View):
    """热销排行"""

    def get(self, request, category_id):
        """展示热销排行"""
        # 查找商品sku
        try:
            # -sales销量降序, 切片取前两个
            skus = SKU.objects.filter(category_id=category_id, is_launched=True).order_by('-sales')[0:2]

        except Exception as e:
            logger.error(e)
            return http.JsonResponse({'code': RETCODE.DBERR, 'errmsg': '热销排行查询失败'})
        # model_list转json数据
        skus_list = []
        for sku in skus:
            skus_list.append({
                'id': sku.id,
                'default_image_url': sku.default_image_url.url,
                'name': sku.name,
                'price': sku.price,
            })
        return http.JsonResponse({
            'code': RETCODE.OK,
            'errmsg': 'OK',
            'hot_skus': skus_list
        })


class ListView(View):
    """商品列表页"""

    def get(self, request, category_id, page_num):
        """展示页面"""
        # 校验查询category_id
        try:
            category = GoodsCategory.objects.get(id=category_id)

        except Exception as e:
            logger.error(e)
            return http.HttpResponseNotFound('未找到数据')
        # 查询商品分类
        categories = get_categories()
        # 查询面包屑导航
        breadcrumb = get_breadcrumb(category)
        # 获取sort排序方式
        sort = request.GET.get('sort')
        # 判断页面排序方式
        if sort == 'price':
            # 价格降序, 默认升序
            sort_field = 'price'
        elif sort == 'hot':
            # 热度降序
            sort_field = '-sales'
        else:
            # 其他情况
            sort = 'default'  # 重置排序参数
            sort_field = 'create_time'
        try:
            # 查询sku商品预览(条件: 商品类别, 是否上架)
            skus = SKU.objects.filter(category_id=category_id, is_launched=True).order_by(sort_field)

        except Exception as e:
            logger.error(e)
            return http.HttpResponseNotFound('找不到商品信息')

        # sku分页
        paginator = Paginator(skus, CONTENT_QUANTITY)  # Paginator(分页内容, 每页数量)
        # 获取每页数据
        try:
            sku_page = paginator.page(page_num)
        except Exception as e:
            logger.error(e)
            return http.HttpResponseNotFound('找不到该页商品信息')
        # 总页数
        total_page = paginator.num_pages
        # jinja渲染内容
        context = {
            'categories': categories,  # 商品分类列表
            'breadcrumb': breadcrumb,  # 面包屑导航
            'sku_page': sku_page,  # 每页数据
            'sort': sort,  # 排序规则
            'page_num': page_num,  # 当前所在页
            'total_page': total_page,  # 总页数
            'category_id': category_id,  # 当前商品类别id
            'category': category,  # 当前商品类别
        }
        for tsku in sku_page:
            id = tsku.id
            url = tsku.default_image_url.url
            name = tsku.name
            pass
        return render(request, 'list.html', context)
