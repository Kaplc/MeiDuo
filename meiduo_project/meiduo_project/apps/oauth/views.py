from django import http
from django.shortcuts import render

# Create your views here.
from django.views import View


class QQAuthURLView(View):
    """提供QQ登录页面"""
    def get(self, request):

        return http.HttpResponse("OK")

