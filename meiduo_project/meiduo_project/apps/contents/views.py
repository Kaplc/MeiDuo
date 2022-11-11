from django.shortcuts import render, redirect

# Create your views here.
from django.urls import reverse
from django.views import View


class RedirectIndex(View):
    """重定向到首页"""

    def get(self, request):
        return redirect(reverse('contents:index'))


class IndexView(View):
    """首页"""

    def get(self, request):
        return render(request, 'index.html')
