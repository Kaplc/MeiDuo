from django.urls import re_path
from .views import *
app_name = 'carts'
urlpatterns =[
    re_path(r'carts/$', CartsView.as_view(), name='carts')
]