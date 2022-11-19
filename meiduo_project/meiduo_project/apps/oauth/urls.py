from django.urls import re_path
from .views import *
app_name = 'oauth'

urlpatterns = [
    re_path(r'qq/login/$', QQAuthURLView.as_view())
]