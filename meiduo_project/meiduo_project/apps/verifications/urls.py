from django.urls import re_path
from .views import *

app_name = "verify_code"

urlpatterns = [
    re_path(r'get_image_codes/(?P<uuid>[\w-]+)/$', ImageCode.as_view()),
    re_path(r'send_message_code/(?P<mobile_cli>1[3-9]\d{9})/(?P<image_code>.*)/(?P<uuid>[\w-]+)/$', SMSCodeView.as_view()),

]
