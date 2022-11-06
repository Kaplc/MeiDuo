from django.urls import re_path
from .views import *

app_name = 'users'

urlpatterns = [
    re_path(r'^register.html$', RegisterView.as_view(), name='register'),
    re_path(r'^$', IndexView.as_view(), name='index')
]
