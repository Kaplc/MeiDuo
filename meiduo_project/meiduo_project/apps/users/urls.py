from django.urls import re_path
from .views import *

app_name = 'users'

urlpatterns = [
    re_path(r'$', RegisterView.as_view(), name='register'),
    re_path(r'usernames/(?P<username>[a-zA-Z0-9_-]{5,20})/count/$', UsernameCountView.as_view()),
    re_path(r'mobiles/(?P<mobile>1[3-9]\d{9})/count/$', PhoneCountView.as_view()),
]
