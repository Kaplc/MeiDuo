from django.urls import re_path
from .views import *

app_name = 'users'

urlpatterns = [
    re_path(r'$', RegisterView.as_view(), name='register'),
    re_path(r'usernames/[a-zA-Z0-9]{8,20}/count/$', UsernameCountView.as_view(), name='check_username_count')
]
