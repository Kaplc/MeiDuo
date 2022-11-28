from django import http
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views import View
from collections import OrderedDict
from goods.utils import get_categories, get_breadcrumb
from .models import ContentCategory
from goods.models import GoodsCategory

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
        context ={
            'categories': categories,
            'breadcrumb': breadcrumb,
        }
        return render(request, 'list.html', context)


class RedirectIndex(View):
    """重定向到首页"""

    def get(self, request):
        return redirect(reverse('contents:index'))


class IndexView(View):
    """首页广告"""

    def get(self, request):
        """提供首页广告"""
        # 查询商品频道和分类
        categories = get_categories()
        # 查询首页广告数据
        contents = OrderedDict()
        for cat in ContentCategory.objects.all():
            contents[cat.key] = cat.content_set.filter(status=True).order_by('sequence')
        # 定义上下文
        context = {
            'categories': categories,
            'contents': contents,
        }

        return render(request, 'index.html', context)
