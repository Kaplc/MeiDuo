from django.urls import re_path
from .views import *

app_name = "verify_code"

urlpatterns = [
    # 获取图形验证码
    re_path(r'verify/get_image_codes/(?P<uuid>[\w-]+)/$', ImageCode.as_view()),
    # 发送短信
    re_path(r'verify/send_message_code/(?P<mobile_cli>1[3-9]\d{9})/(?P<image_code>.*)/(?P<uuid>[\w-]+)/$', SMSCodeView.as_view()),


]
