from django.shortcuts import render

# Create your views here.
from django.urls import reverse
from django.views import View


class IndexView(View):
    def get(self, request):
        return render(request, 'index.html')


class RegisterView(View):
    """注册"""

    def get(self, request):
        return render(request, 'register.html')
