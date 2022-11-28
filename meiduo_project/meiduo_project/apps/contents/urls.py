from django.urls import re_path
from .views import *

app_name = 'contents'

urlpatterns = [
    # 首页
    re_path(r'$', IndexView.as_view(), name='index'),
    re_path(r'index.html$', IndexView.as_view()),


]
