from django.shortcuts import render, redirect
from django.urls import reverse
from django.views import View
from collections import OrderedDict
from goods.models import GoodsChannelGroup, GoodsChannel, GoodsCategory
from goods.utils import get_categories

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

        context = {
            'categories': categories
        }

        return render(request, 'index.html', context)
