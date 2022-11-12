from django.urls import re_path
from .views import IndexView, RedirectIndex

app_name = 'contents'

urlpatterns = [
    re_path(r'^$', IndexView.as_view(), name='index'),
    re_path(r'index.html$', RedirectIndex.as_view()),


]
