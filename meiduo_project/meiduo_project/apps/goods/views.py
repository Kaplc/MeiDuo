from django import http
from django.shortcuts import render

# Create your views here.
from django.views import View

from goods.models import GoodsCategory
from goods.utils import get_categories, get_breadcrumb
import logging

logger = logging.getLogger('django')


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
        # jinja渲染内容
        context = {
            'categories': categories,
            'breadcrumb': breadcrumb,
        }
        return render(request, 'list.html', context)
