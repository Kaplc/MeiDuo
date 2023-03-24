from django.shortcuts import render
from django import http
from django.views import View


class AdminLogin(View):
    """展示登录界面"""

    def get(self, request):
        return render(request, 'admin_login.html')

    def post(self, request):
        return http.JsonResponse({'code': 'OK'})
