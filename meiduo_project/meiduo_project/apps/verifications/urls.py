from django.urls import re_path
from .views import *

app_name = "verify_code"

urlpatterns = [
    re_path(r'get_image_codes/(?P<uuid>[\w-]+)/$', ImageCode.as_view()),
re_path(r'check_image_codes/(?P<uuid>[\w-]+)/$', ImageCode.as_view()),

]
