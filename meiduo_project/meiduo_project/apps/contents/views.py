from django import http
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views import View
from collections import OrderedDict
from goods.utils import get_categories
from .models import ContentCategory
from carts.utils import dict_to_cookie
import logging

logger = logging.getLogger('django')


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
        response = render(request, 'index.html', context)

        # 判断cookie购物车是否存在
        # cookie_cart = request.COOKIE.get('cart')
        # if cookie_cart is None:
        #     # 写入空cookie购物车
        #     response.set_cookie('carts', dict_to_cookie({}))
        return response
