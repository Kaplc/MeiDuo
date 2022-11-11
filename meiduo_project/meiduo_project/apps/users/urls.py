from django.urls import re_path
from .views import *

app_name = 'users'

urlpatterns = [
    re_path('$', RegisterView.as_view(), name='register'),
]
