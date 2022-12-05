from django.shortcuts import render

# Create your views here.
from django.views import View


class CartsView(View):
    """购物车"""
    def get(self, request):
        """展示购物车"""
        pass

    def post(self, request):
        """添加购物车"""
        # 接收参数
        user = request.user

        if user.is_authenticated:
            # 已登录
            pass
        else:
            # 未登录
            pass
        pass
